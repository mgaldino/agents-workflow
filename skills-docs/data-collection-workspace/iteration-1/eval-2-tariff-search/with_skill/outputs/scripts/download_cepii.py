#!/usr/bin/env python3
"""Download de tarifas bilaterais do CEPII MAcMap-HS6.

Fonte: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele.asp
Acesso: bulk download (requer registro)
Credenciais: sim (CEPII_USERNAME e CEPII_PASSWORD em .env)
Ultima execucao: 2026-03-13

O MAcMap-HS6 fornece equivalentes ad valorem de tarifas bilaterais
incluindo acordos preferenciais, no nivel HS6. Disponivel para anos
de referencia: 2001, 2004, 2007, 2010, 2013, 2016, 2019.
Dentro do periodo 2000-2010, cobre: 2001, 2004, 2007, 2010.
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

CEPII_USERNAME = os.getenv("CEPII_USERNAME")
CEPII_PASSWORD = os.getenv("CEPII_PASSWORD")

# CEPII MAcMap download URLs (benchmark years within 2000-2010)
MACMAP_YEARS = {
    2001: "http://www.cepii.fr/DATA_DOWNLOAD/MAcMap/MAcMap_HS6_V2_2001.zip",
    2004: "http://www.cepii.fr/DATA_DOWNLOAD/MAcMap/MAcMap_HS6_V3_2004.zip",
    2007: "http://www.cepii.fr/DATA_DOWNLOAD/MAcMap/MAcMap_HS6_V3_2007.zip",
    2010: "http://www.cepii.fr/DATA_DOWNLOAD/MAcMap/MAcMap_HS6_V3_2010.zip",
}


def authenticate_cepii() -> requests.Session | None:
    """Authenticate with CEPII website and return session.

    Returns
    -------
    requests.Session or None
        Authenticated session, or None if credentials are missing/invalid
    """
    if not CEPII_USERNAME or not CEPII_PASSWORD:
        logger.error(
            "CEPII credentials not found. Set CEPII_USERNAME and CEPII_PASSWORD "
            "in .env file. Register at: http://www.cepii.fr/"
        )
        return None

    session = requests.Session()
    login_url = "http://www.cepii.fr/CEPII/en/login.asp"

    try:
        response = session.post(
            login_url,
            data={
                "login": CEPII_USERNAME,
                "password": CEPII_PASSWORD,
            },
            timeout=30,
        )
        if response.status_code == 200 and "logout" in response.text.lower():
            logger.info("CEPII authentication successful.")
            return session
        else:
            logger.error("CEPII authentication failed. Check credentials.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Authentication error: {e}")
        return None


def download_macmap_year(
    session: requests.Session, year: int, url: str, max_retries: int = 3
) -> Path | None:
    """Download MAcMap-HS6 data for a single benchmark year.

    Parameters
    ----------
    session : requests.Session
        Authenticated CEPII session
    year : int
        Benchmark year
    url : str
        Download URL
    max_retries : int
        Maximum retries with exponential backoff

    Returns
    -------
    Path or None
        Path to downloaded ZIP file, or None if failed
    """
    output_path = RAW_DIR / f"macmap_hs6_{year}_{datetime.now():%Y%m%d}.zip"

    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=300, stream=True)

            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                if output_path.stat().st_size > 0:
                    size_mb = output_path.stat().st_size / (1024 * 1024)
                    logger.info(f"MAcMap {year}: {size_mb:.1f} MB saved to {output_path}")
                    return output_path
                else:
                    logger.error(f"Downloaded file is empty: {output_path}")
                    output_path.unlink()
                    return None

            elif response.status_code == 403:
                logger.error(f"Access denied for MAcMap {year}. Check CEPII subscription.")
                return None
            else:
                logger.error(f"HTTP {response.status_code} for MAcMap {year}")

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** (attempt + 1)
            logger.error(f"Download error for {year}: {e}. Retry in {wait_time}s")
            time.sleep(wait_time)

    return None


def download():
    """Main function: authenticate and download MAcMap for all benchmark years."""
    logger.info("Iniciando download do CEPII MAcMap-HS6 (2001, 2004, 2007, 2010)...")

    session = authenticate_cepii()
    if not session:
        logger.error(
            "Nao foi possivel autenticar no CEPII. Configure as credenciais em .env"
        )
        return None

    downloaded_files = []
    for year, url in MACMAP_YEARS.items():
        logger.info(f"Downloading MAcMap-HS6 for {year}...")
        result = download_macmap_year(session, year, url)
        if result:
            downloaded_files.append(result)
        time.sleep(2)

    logger.info(f"Download concluido: {len(downloaded_files)}/{len(MACMAP_YEARS)} arquivos")
    return downloaded_files


if __name__ == "__main__":
    download()
