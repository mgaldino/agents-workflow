#!/usr/bin/env python3
"""Download de PIB per capita e populacao da America Latina via World Bank API.

Fonte: https://databank.worldbank.org/source/world-development-indicators
API docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
Acesso: API (wbgapi)
Credenciais: nao
Ultima execucao: 2026-03-13
"""

import logging
import time
from pathlib import Path
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Codigos ISO alpha-3 dos paises da America Latina
LATAM_COUNTRIES = [
    "ARG",  # Argentina
    "BOL",  # Bolivia
    "BRA",  # Brasil
    "CHL",  # Chile
    "COL",  # Colombia
    "CRI",  # Costa Rica
    "CUB",  # Cuba
    "DOM",  # Republica Dominicana
    "ECU",  # Equador
    "SLV",  # El Salvador
    "GTM",  # Guatemala
    "HTI",  # Haiti
    "HND",  # Honduras
    "MEX",  # Mexico
    "NIC",  # Nicaragua
    "PAN",  # Panama
    "PRY",  # Paraguai
    "PER",  # Peru
    "URY",  # Uruguai
    "VEN",  # Venezuela
]

# Indicadores do World Development Indicators
INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "SP.POP.TOTL": "population_total",
}

START_YEAR = 2000
END_YEAR = 2023

# Base URL da API v2 do World Bank
BASE_URL = "https://api.worldbank.org/v2"


def create_session():
    """Cria sessao HTTP com retry e backoff exponencial."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_indicator(session, indicator_code, countries, start_year, end_year):
    """Baixa um indicador para uma lista de paises via World Bank API v2.

    A API retorna dados paginados em JSON. Iteramos todas as paginas.
    """
    country_str = ";".join(countries)
    url = f"{BASE_URL}/country/{country_str}/indicator/{indicator_code}"
    params = {
        "date": f"{start_year}:{end_year}",
        "format": "json",
        "per_page": 1000,
        "page": 1,
    }

    all_records = []
    page = 1

    while True:
        params["page"] = page
        logger.info(f"  Baixando {indicator_code} - pagina {page}...")
        resp = session.get(url, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # A API retorna [metadata, records]. Se records for None, acabou.
        if len(data) < 2 or data[1] is None:
            break

        metadata = data[0]
        records = data[1]
        all_records.extend(records)

        total_pages = metadata.get("pages", 1)
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)  # Rate limiting educado

    logger.info(f"  {indicator_code}: {len(all_records)} registros baixados.")
    return all_records


def download():
    """Funcao principal de download."""
    logger.info("Iniciando download do World Bank WDI...")
    logger.info(f"Paises: {len(LATAM_COUNTRIES)}, Periodo: {START_YEAR}-{END_YEAR}")
    logger.info(f"Indicadores: {list(INDICATORS.keys())}")

    session = create_session()
    timestamp = datetime.now().strftime("%Y%m%d")

    all_data = {}
    for indicator_code, indicator_name in tqdm(INDICATORS.items(), desc="Indicadores"):
        records = fetch_indicator(
            session, indicator_code, LATAM_COUNTRIES, START_YEAR, END_YEAR
        )
        all_data[indicator_code] = records

        # Salvar bruto por indicador (JSON)
        import json

        raw_path = RAW_DIR / f"worldbank_{indicator_code}_{timestamp}.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        logger.info(f"Salvo bruto: {raw_path}")

    logger.info("Download completo.")
    return all_data


if __name__ == "__main__":
    download()
