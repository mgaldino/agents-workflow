#!/usr/bin/env python3
"""Download de indices de democracia do V-Dem (Varieties of Democracy).

Fonte: https://www.v-dem.net/data/the-v-dem-dataset/
Acesso: bulk download (CSV/Stata disponivel no site, ou via API GitHub)
Credenciais: nao
Ultima execucao: 2026-03-13

O V-Dem disponibiliza o dataset completo para download em seu site.
Este script baixa a versao CSV compactada do dataset Country-Year (V-Dem Full+Others).
Alternativamente, o pacote `vdemdata` em R pode ser usado.

Variaveis selecionadas:
- v2x_polyarchy: Electoral Democracy Index (0-1)
- v2x_libdem: Liberal Democracy Index (0-1)
- v2x_partipdem: Participatory Democracy Index (0-1)
- v2x_delibdem: Deliberative Democracy Index (0-1)
- v2x_egaldem: Egalitarian Democracy Index (0-1)
"""

import logging
import zipfile
import io
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# V-Dem download URL — V-Dem v14 (Country-Year: V-Dem Full+Others)
# Nota: o URL pode mudar entre versoes. Verificar em https://www.v-dem.net/data/the-v-dem-dataset/
VDEM_URL = "https://v-dem.net/media/datasets/V-Dem-CY-Full+Others-v14.csv.zip"

# Variaveis de interesse para selecionar do dataset completo
VARIABLES_OF_INTEREST = [
    "country_name",
    "country_text_id",  # ISO 3166-1 alpha-3
    "year",
    "v2x_polyarchy",    # Electoral Democracy Index
    "v2x_libdem",       # Liberal Democracy Index
    "v2x_partipdem",    # Participatory Democracy Index
    "v2x_delibdem",     # Deliberative Democracy Index
    "v2x_egaldem",      # Egalitarian Democracy Index
    "e_regionpol",      # Region (political)
    "e_regiongeo",      # Region (geographic)
]

# Periodo de interesse
YEAR_MIN = 1990
YEAR_MAX = 2020


def download_with_retry(url, max_retries=3, timeout=120):
    """Baixa arquivo com retry e backoff exponencial."""
    import time

    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa {attempt + 1}/{max_retries} de download...")
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()

            # Ler com barra de progresso
            total_size = int(response.headers.get("content-length", 0))
            content = io.BytesIO()
            with tqdm(total=total_size, unit="B", unit_scale=True, desc="V-Dem") as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    content.write(chunk)
                    pbar.update(len(chunk))

            content.seek(0)
            return content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Erro na tentativa {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait = 2 ** attempt * 5  # 5s, 10s, 20s
                logger.info(f"Aguardando {wait}s antes de tentar novamente...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Falha apos {max_retries} tentativas: {e}")


def download():
    """Funcao principal de download do V-Dem."""
    logger.info("Iniciando download do V-Dem v14 (Country-Year Full+Others)...")

    # Baixar o arquivo ZIP
    zip_content = download_with_retry(VDEM_URL)

    # Extrair CSV do ZIP
    logger.info("Extraindo CSV do arquivo ZIP...")
    with zipfile.ZipFile(zip_content) as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        if not csv_files:
            raise RuntimeError("Nenhum arquivo CSV encontrado no ZIP")
        csv_filename = csv_files[0]
        logger.info(f"Lendo {csv_filename}...")

        with zf.open(csv_filename) as csv_file:
            # Ler apenas as colunas de interesse para economizar memoria
            df = pd.read_csv(csv_file, usecols=VARIABLES_OF_INTEREST, encoding="utf-8")

    # Filtrar periodo
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]

    logger.info(f"Dataset filtrado: {len(df)} observacoes, {df['country_text_id'].nunique()} paises, {YEAR_MIN}-{YEAR_MAX}")

    # Salvar arquivo raw (CSV filtrado por periodo e variaveis)
    today = datetime.now().strftime("%Y%m%d")
    output_path = RAW_DIR / f"vdem_v14_cy_{today}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Salvo em {output_path}")
    logger.info(f"Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas")
    logger.info(f"Paises: {df['country_text_id'].nunique()}")
    logger.info(f"Anos: {df['year'].min()}-{df['year'].max()}")

    return output_path


if __name__ == "__main__":
    download()
