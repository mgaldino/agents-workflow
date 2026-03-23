#!/usr/bin/env python3
"""Processamento dos dados brutos do World Bank WDI em painel pais-ano.

Le os JSONs brutos em raw/, limpa e consolida em um unico CSV
em processed/painel_latam.csv.

Ultima execucao: 2026-03-13
"""

import json
import logging
from pathlib import Path
from glob import glob

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "SP.POP.TOTL": "population_total",
}


def load_latest_raw(indicator_code):
    """Carrega o arquivo JSON bruto mais recente para um indicador."""
    pattern = str(RAW_DIR / f"worldbank_{indicator_code}_*.json")
    files = sorted(glob(pattern))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo bruto para {indicator_code} em {RAW_DIR}")
    latest = files[-1]
    logger.info(f"Carregando {latest}")
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_records(records, indicator_code):
    """Converte registros da API do World Bank em DataFrame."""
    rows = []
    for rec in records:
        if rec is None:
            continue
        rows.append({
            "country_code": rec.get("countryiso3code", rec.get("country", {}).get("id", "")),
            "country_name": rec.get("country", {}).get("value", ""),
            "year": int(rec.get("date", 0)),
            INDICATORS[indicator_code]: rec.get("value"),
        })
    df = pd.DataFrame(rows)
    return df


def process():
    """Funcao principal de processamento."""
    logger.info("Iniciando processamento dos dados do World Bank...")

    dfs = []
    for indicator_code in INDICATORS:
        records = load_latest_raw(indicator_code)
        df = parse_records(records, indicator_code)
        dfs.append(df)

    # Merge dos indicadores no painel pais-ano
    panel = dfs[0]
    for df in dfs[1:]:
        panel = pd.merge(
            panel,
            df.drop(columns=["country_name"], errors="ignore"),
            on=["country_code", "year"],
            how="outer",
        )

    # Ordenar
    panel = panel.sort_values(["country_code", "year"]).reset_index(drop=True)

    # Validacoes basicas
    n_countries = panel["country_code"].nunique()
    n_years = panel["year"].nunique()
    n_rows = len(panel)
    logger.info(f"Painel: {n_countries} paises x {n_years} anos = {n_rows} linhas")

    # Checar missing
    for col in INDICATORS.values():
        n_missing = panel[col].isna().sum()
        pct_missing = 100 * n_missing / n_rows
        logger.info(f"  {col}: {n_missing} missing ({pct_missing:.1f}%)")

    # Salvar
    output_path = PROCESSED_DIR / "painel_latam.csv"
    panel.to_csv(output_path, index=False, encoding="utf-8")
    logger.info(f"Salvo: {output_path}")

    # Resumo
    logger.info(f"\nResumo do painel:")
    logger.info(f"  Paises: {n_countries}")
    logger.info(f"  Periodo: {panel['year'].min()}-{panel['year'].max()}")
    logger.info(f"  Linhas: {n_rows}")
    logger.info(f"  Colunas: {list(panel.columns)}")

    return panel


if __name__ == "__main__":
    process()
