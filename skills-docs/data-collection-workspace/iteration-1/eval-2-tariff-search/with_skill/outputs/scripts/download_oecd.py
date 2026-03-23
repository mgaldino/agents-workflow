#!/usr/bin/env python3
"""Download de indicadores de politica tarifaria da OCDE via SDMX API.

Fonte: https://data-explorer.oecd.org/
API docs: https://data.oecd.org/api/sdmx-json-documentation/
Acesso: API (SDMX REST)
Credenciais: nao
Ultima execucao: 2026-03-13

A OECD Data Explorer fornece indicadores agregados de politica comercial
para paises membros. Este script usa a nova API SDMX (sdmx.oecd.org)
para baixar dados de tarifas e indicadores de politica comercial.
"""

import logging
import time
from pathlib import Path
from datetime import datetime
from io import StringIO

import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# OECD SDMX API base
OECD_SDMX_BASE = "https://sdmx.oecd.org/public/rest"

# OECD countries ISO2 codes (OECD uses ISO2 in their API)
OECD_ISO2 = [
    "AU", "AT", "BE", "CA", "CL", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IS", "IE", "IL", "IT", "JP", "KR", "LU",
    "MX", "NL", "NZ", "NO", "PL", "PT", "SK", "SI", "ES", "SE",
    "CH", "TR", "GB", "US"
]


def download_oecd_trade_policy(max_retries: int = 3) -> Path | None:
    """Download OECD trade policy indicators via SDMX REST API.

    The OECD SDMX API provides data in CSV format when requested.
    We query the Trade Policy dataset for all OECD members, 2000-2010.

    Parameters
    ----------
    max_retries : int
        Maximum number of retries with exponential backoff

    Returns
    -------
    Path or None
        Path to saved CSV file, or None if download failed
    """
    # Build the SDMX query URL
    # Agency: OECD.TAD (Trade and Agriculture Directorate)
    # Dataflow: DSD_TRADE@DF_TARIFFS (tariff indicators)
    # Filter: all OECD countries, annual frequency, 2000-2010
    countries = "+".join(OECD_ISO2)

    url = (
        f"{OECD_SDMX_BASE}/data/"
        f"OECD.TAD,DSD_TRADE@DF_TARIFFS,1.0/"
        f"{countries}.A..."
        f"?startPeriod=2000&endPeriod=2010"
        f"&dimensionAtObservation=AllDimensions"
        f"&format=csvfilewithlabels"
    )

    logger.info(f"Requesting OECD tariff data...")
    logger.info(f"URL: {url}")

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=120)

            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                output_path = RAW_DIR / f"oecd_tariff_indicators_{datetime.now():%Y%m%d}.csv"
                df.to_csv(output_path, index=False, encoding="utf-8")
                logger.info(f"Salvo em {output_path}")
                logger.info(f"Total: {len(df)} observacoes")
                return output_path

            elif response.status_code == 404:
                logger.warning(
                    "Dataset nao encontrado. Tentando dataflow alternativo..."
                )
                # Try alternative dataflow identifier
                return _try_alternative_dataflow(countries)

            elif response.status_code == 429:
                wait_time = 2 ** (attempt + 1)
                logger.warning(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)

            else:
                logger.error(f"HTTP {response.status_code}: {response.text[:200]}")
                return None

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** (attempt + 1)
            logger.error(f"Request error: {e}. Retry in {wait_time}s")
            time.sleep(wait_time)

    logger.error(f"Failed after {max_retries} retries")
    return None


def _try_alternative_dataflow(countries: str) -> Path | None:
    """Try alternative OECD dataflow identifiers for tariff data.

    OECD dataset identifiers change over time. This function tries
    several known identifiers.

    Parameters
    ----------
    countries : str
        '+'-joined string of ISO2 country codes

    Returns
    -------
    Path or None
        Path to saved CSV file, or None if all attempts failed
    """
    alternative_flows = [
        "OECD.TAD,DSD_TRADE@DF_MFN_TARIFF,1.0",
        "OECD.SDD.TPS,DSD_TRADE@DF_TARIFF_INDICATORS,1.0",
        "OECD.TAD,DSD_TIVA@DF_TARIFFS,1.0",
    ]

    for flow in alternative_flows:
        url = (
            f"{OECD_SDMX_BASE}/data/{flow}/{countries}.A..."
            f"?startPeriod=2000&endPeriod=2010"
            f"&dimensionAtObservation=AllDimensions"
            f"&format=csvfilewithlabels"
        )
        logger.info(f"Trying alternative: {flow}")

        try:
            response = requests.get(url, timeout=120)
            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                output_path = RAW_DIR / f"oecd_tariff_indicators_{datetime.now():%Y%m%d}.csv"
                df.to_csv(output_path, index=False, encoding="utf-8")
                logger.info(f"Salvo em {output_path} (via {flow})")
                return output_path
        except requests.exceptions.RequestException:
            continue

    logger.error("Nenhum dataflow alternativo funcionou.")
    logger.info(
        "Recomendacao: use o OECD Data Explorer (https://data-explorer.oecd.org/) "
        "para localizar o identificador correto do dataset de tarifas."
    )
    return None


def download():
    """Main entry point."""
    logger.info("Iniciando download de indicadores tarifarios OCDE (2000-2010)...")
    result = download_oecd_trade_policy()
    if result:
        logger.info("Download concluido com sucesso.")
    else:
        logger.warning(
            "Download falhou. Alternativa: usar download_wits.py que cobre os mesmos paises."
        )
    return result


if __name__ == "__main__":
    download()
