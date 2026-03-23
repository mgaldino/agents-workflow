#!/usr/bin/env python3
"""Download de dados tarifarios do portal de dados da OMC (WTO).

Fonte: https://data.wto.org/
Documentacao: https://apiportal.wto.org/
Acesso: API REST (com chave opcional) / bulk download
Credenciais: opcional (WTO_API_KEY em .env para limites maiores)
Ultima execucao: 2026-03-13

O portal de dados da OMC oferece tarifas MFN aplicadas e consolidadas
para todos os membros da OMC. Este script baixa dados agregados por
pais-ano-setor para paises da OCDE no periodo 2000-2010.
"""

import logging
import time
import os
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# WTO API base URL
WTO_API_BASE = "https://api.wto.org/timeseries/v1"

# WTO API key (optional, increases rate limits)
WTO_API_KEY = os.getenv("WTO_API_KEY")

# OECD member ISO3 codes
OECD_COUNTRIES = [
    "AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA",
    "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LUX",
    "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "ESP", "SWE",
    "CHE", "TUR", "GBR", "USA"
]

# WTO indicator codes for tariff data
TARIFF_INDICATORS = [
    "HS_M_0010",  # MFN Simple Average duty - All products
    "HS_M_0020",  # MFN Trade Weighted Average duty - All products
    "HS_M_0030",  # MFN Simple Average duty - Agricultural products
    "HS_M_0040",  # MFN Simple Average duty - Non-agricultural products
    "HS_M_0050",  # Binding coverage (%)
]


def fetch_wto_tariff_data(
    indicator: str,
    reporting_economies: list[str],
    start_year: int = 2000,
    end_year: int = 2010,
    max_retries: int = 3,
) -> pd.DataFrame | None:
    """Fetch tariff indicator data from WTO Timeseries API.

    Parameters
    ----------
    indicator : str
        WTO indicator code
    reporting_economies : list[str]
        List of ISO3 country codes
    start_year : int
        Start year (inclusive)
    end_year : int
        End year (inclusive)
    max_retries : int
        Maximum retries with exponential backoff

    Returns
    -------
    pd.DataFrame or None
        DataFrame with tariff data
    """
    headers = {"Content-Type": "application/json"}
    if WTO_API_KEY:
        headers["Ocp-Apim-Subscription-Key"] = WTO_API_KEY

    params = {
        "i": indicator,
        "r": ",".join(reporting_economies),
        "ps": ",".join(str(y) for y in range(start_year, end_year + 1)),
        "pc": "Total",  # All products aggregate
        "spc": "false",
        "fmt": "json",
        "mode": "full",
        "dec": "default",
        "off": 0,
        "max": 10000,
        "head": "H",
        "lang": 1,  # English
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"{WTO_API_BASE}/data",
                params=params,
                headers=headers,
                timeout=60,
            )

            if response.status_code == 200:
                data = response.json()
                if "Dataset" in data and data["Dataset"]:
                    df = pd.DataFrame(data["Dataset"])
                    return df
                else:
                    logger.warning(f"Empty dataset for indicator {indicator}")
                    return None

            elif response.status_code == 429:
                wait_time = 2 ** (attempt + 1)
                logger.warning(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)

            else:
                logger.error(
                    f"HTTP {response.status_code} for {indicator}: "
                    f"{response.text[:200]}"
                )
                return None

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** (attempt + 1)
            logger.error(f"Request error: {e}. Retry in {wait_time}s")
            time.sleep(wait_time)

    return None


def download():
    """Main download function: fetch all tariff indicators for OECD countries."""
    logger.info("Iniciando download de tarifas WTO para OCDE (2000-2010)...")

    all_frames = []

    for indicator in tqdm(TARIFF_INDICATORS, desc="WTO indicators"):
        logger.info(f"Downloading indicator: {indicator}")
        df = fetch_wto_tariff_data(indicator, OECD_COUNTRIES)
        if df is not None:
            df["indicator_code"] = indicator
            all_frames.append(df)
        time.sleep(1)  # Rate limiting

    if not all_frames:
        logger.error("Nenhum dado baixado da WTO.")
        return None

    combined = pd.concat(all_frames, ignore_index=True)

    output_path = RAW_DIR / f"wto_tariffs_oecd_{datetime.now():%Y%m%d}.csv"
    combined.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Salvo em {output_path}")
    logger.info(f"Total: {len(combined)} registros")

    return output_path


if __name__ == "__main__":
    download()
