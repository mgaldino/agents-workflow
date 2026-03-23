#!/usr/bin/env python3
"""Busca e download de datasets de tarifas no Harvard Dataverse.

Fonte: https://dataverse.harvard.edu/
API docs: https://guides.dataverse.org/en/latest/api/
Acesso: API REST
Credenciais: opcional (DATAVERSE_API_TOKEN em .env para limites maiores)
Ultima execucao: 2026-03-13

Este script busca datasets relacionados a tarifas comerciais no Harvard
Dataverse e faz download dos arquivos relevantes. A API do Dataverse
permite busca por palavras-chave e download programatico.
"""

import logging
import os
import time
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

DATAVERSE_BASE = "https://dataverse.harvard.edu"
DATAVERSE_API_TOKEN = os.getenv("DATAVERSE_API_TOKEN")

SEARCH_QUERIES = [
    "trade tariffs OECD",
    "MFN tariff rates",
    "commercial tariffs developing countries",
    "trade policy WTO tariffs",
]


def search_dataverse(
    query: str, max_results: int = 10, max_retries: int = 3
) -> list[dict]:
    """Search Harvard Dataverse for datasets matching a query.

    Parameters
    ----------
    query : str
        Search query string
    max_results : int
        Maximum number of results to return
    max_retries : int
        Maximum retries with exponential backoff

    Returns
    -------
    list[dict]
        List of dataset metadata dictionaries
    """
    url = f"{DATAVERSE_BASE}/api/search"
    params = {
        "q": query,
        "type": "dataset",
        "per_page": max_results,
        "sort": "date",
        "order": "desc",
    }
    headers = {}
    if DATAVERSE_API_TOKEN:
        headers["X-Dataverse-key"] = DATAVERSE_API_TOKEN

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                items = data.get("data", {}).get("items", [])
                logger.info(f"Found {len(items)} datasets for query: '{query}'")
                return items
            elif response.status_code == 429:
                wait_time = 2 ** (attempt + 1)
                logger.warning(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"HTTP {response.status_code}: {response.text[:200]}")
                return []
        except requests.exceptions.RequestException as e:
            wait_time = 2 ** (attempt + 1)
            logger.error(f"Request error: {e}. Retry in {wait_time}s")
            time.sleep(wait_time)

    return []


def get_dataset_files(doi: str) -> list[dict]:
    """Get list of files in a Dataverse dataset.

    Parameters
    ----------
    doi : str
        Dataset persistent identifier (DOI)

    Returns
    -------
    list[dict]
        List of file metadata dictionaries
    """
    url = f"{DATAVERSE_BASE}/api/datasets/:persistentId/"
    params = {"persistentId": doi}
    headers = {}
    if DATAVERSE_API_TOKEN:
        headers["X-Dataverse-key"] = DATAVERSE_API_TOKEN

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            files = data.get("data", {}).get("latestVersion", {}).get("files", [])
            return files
        else:
            logger.error(f"HTTP {response.status_code} for DOI {doi}")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return []


def download_file(file_id: int, filename: str) -> Path | None:
    """Download a file from Harvard Dataverse by file ID.

    Parameters
    ----------
    file_id : int
        Dataverse file ID
    filename : str
        Name to save the file as

    Returns
    -------
    Path or None
        Path to downloaded file, or None if failed
    """
    url = f"{DATAVERSE_BASE}/api/access/datafile/{file_id}"
    headers = {}
    if DATAVERSE_API_TOKEN:
        headers["X-Dataverse-key"] = DATAVERSE_API_TOKEN

    try:
        response = requests.get(url, headers=headers, timeout=120, stream=True)
        if response.status_code == 200:
            output_path = RAW_DIR / filename
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Downloaded: {output_path}")
            return output_path
        else:
            logger.error(f"HTTP {response.status_code} downloading file {file_id}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Download error: {e}")
        return None


def download():
    """Main function: search for tariff datasets and download relevant files."""
    logger.info("Buscando datasets de tarifas no Harvard Dataverse...")

    all_datasets = []
    for query in SEARCH_QUERIES:
        results = search_dataverse(query)
        all_datasets.extend(results)
        time.sleep(1)

    # Deduplicate by global_id
    seen_ids = set()
    unique_datasets = []
    for ds in all_datasets:
        gid = ds.get("global_id", "")
        if gid and gid not in seen_ids:
            seen_ids.add(gid)
            unique_datasets.append(ds)

    logger.info(f"Total de {len(unique_datasets)} datasets unicos encontrados.")

    # Save search results as a catalog
    catalog_path = RAW_DIR / f"dataverse_search_results_{datetime.now():%Y%m%d}.txt"
    with open(catalog_path, "w", encoding="utf-8") as f:
        f.write("# Harvard Dataverse Search Results: Trade Tariffs\n")
        f.write(f"# Date: {datetime.now():%Y-%m-%d}\n\n")
        for ds in unique_datasets:
            f.write(f"Title: {ds.get('name', 'N/A')}\n")
            f.write(f"DOI: {ds.get('global_id', 'N/A')}\n")
            f.write(f"Description: {ds.get('description', 'N/A')[:200]}\n")
            f.write(f"Published: {ds.get('published_at', 'N/A')}\n")
            f.write(f"URL: {ds.get('url', 'N/A')}\n")
            f.write("-" * 60 + "\n\n")

    logger.info(f"Catalogo de busca salvo em {catalog_path}")

    # For targeted downloads, the user should review the catalog and specify
    # which datasets to download. Example:
    # download_file(file_id=12345, filename="reinhardt_tariffs.tab")

    return catalog_path


if __name__ == "__main__":
    download()
