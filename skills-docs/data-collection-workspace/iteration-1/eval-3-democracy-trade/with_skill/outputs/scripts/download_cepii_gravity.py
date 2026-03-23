#!/usr/bin/env python3
"""Download de dados de comercio bilateral do CEPII Gravity dataset.

Fonte: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8
Acesso: bulk download (registro gratuito pode ser necessario)
Credenciais: nao (download direto do CSV/DTA)
Ultima execucao: 2026-03-13

O CEPII Gravity dataset e a base de referencia para modelos gravitacionais de
comercio internacional. Contem fluxos bilaterais de comercio e variaveis
gravitacionais (distancia, lingua comum, fronteira, colonizacao, etc.).

Versao: Gravity dataset (atualizado periodicamente)
URL de documentacao: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8

Variaveis principais:
- tradeflow_comtrade_o: Exportacoes (reporter = origin)
- tradeflow_comtrade_d: Importacoes (reporter = destination)
- tradeflow_baci: Fluxo de comercio bilateral (BACI)
- distw: Distancia ponderada pela populacao
- contig: Contiguidade (fronteira comum)
- comlang_off: Lingua oficial comum
- colony: Relacao colonial
- comcol: Colonizador comum
- gdp_o / gdp_d: PIB do pais de origem / destino
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

# CEPII Gravity dataset download URL
# Nota: o CEPII pode exigir registro gratuito. Se o download direto falhar,
# acesse http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8
# e baixe manualmente o arquivo Gravity_csv_V202211.zip (ou versao mais recente).
GRAVITY_URL = "http://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip"

# Alternativa: dados ja processados em Stata
# GRAVITY_DTA_URL = "http://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_dta_V202211.zip"

# Variaveis de interesse
VARIABLES_OF_INTEREST = [
    "year",
    "iso3_o",            # ISO3 pais de origem
    "iso3_d",            # ISO3 pais de destino
    "country_id_o",      # ID numerico origem
    "country_id_d",      # ID numerico destino
    "tradeflow_comtrade_o",  # Exportacoes (reporter=origin, USD)
    "tradeflow_comtrade_d",  # Importacoes (reporter=dest, USD)
    "tradeflow_baci",    # Fluxo comercial BACI (USD)
    "distw",             # Distancia ponderada pop (km)
    "contig",            # Contiguidade (0/1)
    "comlang_off",       # Lingua oficial comum (0/1)
    "colony",            # Relacao colonial (0/1)
    "comcol",            # Colonizador comum (0/1)
    "gdp_o",             # PIB origem (USD)
    "gdp_d",             # PIB destino (USD)
    "pop_o",             # Populacao origem
    "pop_d",             # Populacao destino
    "gatt_o",            # Membro GATT/WTO origem
    "gatt_d",            # Membro GATT/WTO destino
    "rta",               # Acordo comercial regional (0/1)
]

YEAR_MIN = 1990
YEAR_MAX = 2020


def download_with_retry(url, max_retries=3, timeout=300):
    """Baixa arquivo com retry e backoff exponencial."""
    import time

    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa {attempt + 1}/{max_retries} de download...")
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            content = io.BytesIO()
            with tqdm(total=total_size, unit="B", unit_scale=True, desc="CEPII Gravity") as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    content.write(chunk)
                    pbar.update(len(chunk))

            content.seek(0)
            return content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Erro na tentativa {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait = 2 ** attempt * 5
                logger.info(f"Aguardando {wait}s antes de tentar novamente...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Falha apos {max_retries} tentativas: {e}")


def download():
    """Funcao principal de download do CEPII Gravity."""
    logger.info("Iniciando download do CEPII Gravity dataset...")

    # Baixar o arquivo ZIP
    zip_content = download_with_retry(GRAVITY_URL)

    # Extrair CSV do ZIP
    logger.info("Extraindo CSV do arquivo ZIP...")
    with zipfile.ZipFile(zip_content) as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        if not csv_files:
            raise RuntimeError("Nenhum arquivo CSV encontrado no ZIP")

        # O arquivo principal e geralmente Gravity_V202211.csv
        csv_filename = csv_files[0]
        logger.info(f"Lendo {csv_filename}... (arquivo grande, pode demorar)")

        with zf.open(csv_filename) as csv_file:
            # Ler em chunks para lidar com arquivo grande (~1.5GB descompactado)
            chunks = []
            for chunk in pd.read_csv(
                csv_file,
                encoding="utf-8",
                chunksize=100_000,
                usecols=lambda col: col in VARIABLES_OF_INTEREST,
            ):
                # Filtrar periodo durante a leitura para economizar memoria
                chunk = chunk[(chunk["year"] >= YEAR_MIN) & (chunk["year"] <= YEAR_MAX)]
                chunks.append(chunk)

            df = pd.concat(chunks, ignore_index=True)

    logger.info(f"Dataset filtrado: {len(df)} pares bilaterais-ano")
    logger.info(f"Paises de origem: {df['iso3_o'].nunique()}")
    logger.info(f"Paises de destino: {df['iso3_d'].nunique()}")

    # Salvar arquivo raw
    today = datetime.now().strftime("%Y%m%d")
    output_path = RAW_DIR / f"cepii_gravity_{today}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Salvo em {output_path}")
    logger.info(f"Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas")
    logger.info(f"Anos: {df['year'].min()}-{df['year'].max()}")

    return output_path


if __name__ == "__main__":
    download()
