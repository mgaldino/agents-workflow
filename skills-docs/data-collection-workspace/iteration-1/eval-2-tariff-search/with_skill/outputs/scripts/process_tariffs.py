#!/usr/bin/env python3
"""Processamento e consolidacao de dados tarifarios de multiplas fontes.

Este script le os dados brutos baixados pelos scripts download_*.py,
limpa e harmoniza as variaveis, e gera um painel consolidado em CSV.

Entrada: raw/wits_tariffs_oecd_*.csv, raw/wto_tariffs_oecd_*.csv, raw/oecd_tariff_indicators_*.csv
Saida: processed/oecd_tariffs_panel.csv
"""

import logging
from pathlib import Path
from datetime import datetime
import glob

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# OECD country name mapping
OECD_COUNTRY_NAMES = {
    "AUS": "Australia", "AUT": "Austria", "BEL": "Belgium", "CAN": "Canada",
    "CHL": "Chile", "CZE": "Czech Republic", "DNK": "Denmark", "EST": "Estonia",
    "FIN": "Finland", "FRA": "France", "DEU": "Germany", "GRC": "Greece",
    "HUN": "Hungary", "ISL": "Iceland", "IRL": "Ireland", "ISR": "Israel",
    "ITA": "Italy", "JPN": "Japan", "KOR": "Korea", "LUX": "Luxembourg",
    "MEX": "Mexico", "NLD": "Netherlands", "NZL": "New Zealand", "NOR": "Norway",
    "POL": "Poland", "PRT": "Portugal", "SVK": "Slovak Republic", "SVN": "Slovenia",
    "ESP": "Spain", "SWE": "Sweden", "CHE": "Switzerland", "TUR": "Turkey",
    "GBR": "United Kingdom", "USA": "United States",
}


def load_latest_raw(pattern: str) -> pd.DataFrame | None:
    """Load the most recently downloaded raw file matching a glob pattern.

    Parameters
    ----------
    pattern : str
        Glob pattern relative to RAW_DIR

    Returns
    -------
    pd.DataFrame or None
        DataFrame from the most recent file, or None if no files found
    """
    files = sorted(RAW_DIR.glob(pattern))
    if not files:
        logger.warning(f"No files matching {pattern} in {RAW_DIR}")
        return None
    latest = files[-1]
    logger.info(f"Loading: {latest}")
    return pd.read_csv(latest)


def process_wits(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize WITS tariff data.

    Parameters
    ----------
    df : pd.DataFrame
        Raw WITS data

    Returns
    -------
    pd.DataFrame
        Cleaned data with standard column names
    """
    cols = {
        "country_code": "country_code",
        "year": "year",
        "mfn_simple_avg": "mfn_simple_avg",
        "mfn_weighted_avg": "mfn_weighted_avg",
        "bound_simple_avg": "bound_simple_avg",
        "total_tariff_lines": "total_tariff_lines",
    }
    df = df.rename(columns=cols)
    df = df[list(cols.values())].copy()
    df["year"] = df["year"].astype(int)
    df["country_name"] = df["country_code"].map(OECD_COUNTRY_NAMES)
    return df


def process_wto(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize WTO tariff data.

    Parameters
    ----------
    df : pd.DataFrame
        Raw WTO data

    Returns
    -------
    pd.DataFrame
        Cleaned data with binding coverage and agricultural breakdown
    """
    # WTO data may have different column names depending on API response
    # This is a template for the expected structure
    result_cols = [
        "country_code", "year", "bound_simple_avg",
        "binding_coverage", "ag_mfn_simple_avg", "nonag_mfn_simple_avg"
    ]

    # Process based on indicator_code column
    pivoted = df.pivot_table(
        index=["ReportingEconomy", "Year"],
        columns="indicator_code",
        values="Value",
        aggfunc="first",
    ).reset_index()

    pivoted = pivoted.rename(columns={
        "ReportingEconomy": "country_code",
        "Year": "year",
        "HS_M_0030": "ag_mfn_simple_avg",
        "HS_M_0040": "nonag_mfn_simple_avg",
        "HS_M_0050": "binding_coverage",
    })

    return pivoted


def merge_sources() -> pd.DataFrame:
    """Merge data from WITS and WTO into a single panel.

    Returns
    -------
    pd.DataFrame
        Consolidated tariff panel for OECD countries, 2000-2010
    """
    # Load WITS as primary source
    wits_df = load_latest_raw("wits_tariffs_oecd_*.csv")
    wto_df = load_latest_raw("wto_tariffs_oecd_*.csv")

    if wits_df is not None:
        panel = process_wits(wits_df)
    else:
        logger.warning("WITS data not available. Creating empty panel.")
        panel = pd.DataFrame(columns=[
            "country_code", "country_name", "year",
            "mfn_simple_avg", "mfn_weighted_avg"
        ])

    # Merge WTO data if available
    if wto_df is not None:
        wto_clean = process_wto(wto_df)
        panel = panel.merge(
            wto_clean[["country_code", "year", "binding_coverage",
                        "ag_mfn_simple_avg", "nonag_mfn_simple_avg"]],
            on=["country_code", "year"],
            how="left",
        )

    # Sort
    panel = panel.sort_values(["country_code", "year"]).reset_index(drop=True)

    return panel


def process():
    """Main processing function."""
    logger.info("Processando dados tarifarios OCDE (2000-2010)...")

    panel = merge_sources()

    if panel.empty:
        logger.error("Nenhum dado para processar. Execute os scripts de download primeiro.")
        return None

    output_path = PROCESSED_DIR / "oecd_tariffs_panel.csv"
    panel.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Painel salvo em {output_path}")
    logger.info(
        f"Dimensoes: {len(panel)} linhas, {len(panel.columns)} colunas, "
        f"{panel['country_code'].nunique()} paises, "
        f"{panel['year'].nunique()} anos"
    )

    # Summary statistics
    logger.info("\nResumo das tarifas medias por ano:")
    if "mfn_simple_avg" in panel.columns:
        summary = panel.groupby("year")["mfn_simple_avg"].agg(["mean", "min", "max"])
        logger.info(f"\n{summary}")

    return output_path


if __name__ == "__main__":
    process()
