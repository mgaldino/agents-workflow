#!/usr/bin/env python3
"""Download de tarifas MFN aplicadas para paises da OCDE (2000-2010) via WITS API.

Fonte: https://wits.worldbank.org/witsapiintro.aspx?lang=en
Acesso: API (SDMX REST)
Credenciais: nao
Ultima execucao: 2026-03-13

A API do WITS fornece dados de tarifas do UNCTAD TRAINS e do WTO IDB.
Este script baixa a media simples e ponderada da tarifa MFN aplicada
para todos os paises da OCDE, ano a ano, no periodo 2000-2010.
"""

import logging
import time
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# OECD member countries (ISO3 codes) as of 2010
OECD_COUNTRIES = [
    "AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA",
    "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LUX",
    "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "ESP", "SWE",
    "CHE", "TUR", "GBR", "USA"
]

YEARS = list(range(2000, 2011))

# WITS API base URL
WITS_API_BASE = "https://wits.worldbank.org/API/V1/SDMX/V21"


def fetch_tariff_data(country: str, year: int, max_retries: int = 3) -> dict | None:
    """Fetch aggregate tariff data for a single country-year from WITS API.

    Uses the WITS SDMX API to retrieve MFN applied tariff summary statistics.

    Parameters
    ----------
    country : str
        ISO3 country code
    year : int
        Reference year
    max_retries : int
        Maximum number of retries with exponential backoff

    Returns
    -------
    dict or None
        Dictionary with tariff indicators, or None if request failed
    """
    # WITS API endpoint for tariff data
    # datasource=1 -> TRAINS, duty_type=MFN, product=Total (all products)
    url = (
        f"https://wits.worldbank.org/API/V1/wits/datasource/tradestats-tariff/"
        f"reporter/{country}/year/{year}/partner/000/product/Total/"
        f"indicator/AHS-SMPL-AVRG;AHS-WGHTD-AVRG;BND-SMPL-AVRG;TTLN-TRDVL"
    )

    headers = {"Accept": "application/json"}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                return _parse_wits_response(data, country, year)
            elif response.status_code == 404:
                logger.warning(f"No data for {country}/{year} (404)")
                return None
            elif response.status_code == 429:
                wait_time = 2 ** (attempt + 1)
                logger.warning(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.warning(
                    f"HTTP {response.status_code} for {country}/{year}"
                )
                return None

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** (attempt + 1)
            logger.error(f"Request error for {country}/{year}: {e}. Retry in {wait_time}s")
            time.sleep(wait_time)

    logger.error(f"Failed after {max_retries} retries: {country}/{year}")
    return None


def _parse_wits_response(data: dict, country: str, year: int) -> dict:
    """Parse WITS JSON response into a flat dictionary.

    Parameters
    ----------
    data : dict
        JSON response from WITS API
    country : str
        ISO3 country code
    year : int
        Reference year

    Returns
    -------
    dict
        Parsed tariff data
    """
    result = {
        "country_code": country,
        "year": year,
        "mfn_simple_avg": None,
        "mfn_weighted_avg": None,
        "bound_simple_avg": None,
        "total_tariff_lines": None,
    }

    # Parse the response structure (actual structure depends on WITS API version)
    try:
        if isinstance(data, dict) and "wits" in data:
            indicators = data["wits"].get("indicators", [])
            for ind in indicators:
                code = ind.get("indicatorcode", "")
                value = ind.get("value")
                if code == "AHS-SMPL-AVRG":
                    result["mfn_simple_avg"] = float(value) if value else None
                elif code == "AHS-WGHTD-AVRG":
                    result["mfn_weighted_avg"] = float(value) if value else None
                elif code == "BND-SMPL-AVRG":
                    result["bound_simple_avg"] = float(value) if value else None
                elif code == "TTLN-TRDVL":
                    result["total_tariff_lines"] = int(value) if value else None
    except (KeyError, TypeError, ValueError) as e:
        logger.warning(f"Parse error for {country}/{year}: {e}")

    return result


def download():
    """Main download function: iterates over OECD countries and years 2000-2010."""
    logger.info("Iniciando download de tarifas WITS/TRAINS para OCDE (2000-2010)...")

    all_records = []
    total_requests = len(OECD_COUNTRIES) * len(YEARS)

    with tqdm(total=total_requests, desc="Downloading tariff data") as pbar:
        for country in OECD_COUNTRIES:
            for year in YEARS:
                record = fetch_tariff_data(country, year)
                if record:
                    all_records.append(record)
                pbar.update(1)
                # Rate limiting: be polite to the API
                time.sleep(0.5)

    if not all_records:
        logger.error("Nenhum dado baixado. Verifique a conexao e a API.")
        return None

    df = pd.DataFrame(all_records)

    # Save raw data with date stamp
    output_path = RAW_DIR / f"wits_tariffs_oecd_{datetime.now():%Y%m%d}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Salvo em {output_path}")
    logger.info(f"Total: {len(df)} registros ({df['country_code'].nunique()} paises)")

    return output_path


if __name__ == "__main__":
    download()
