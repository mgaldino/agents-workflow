"""
02_download_cepii_gravity.py
Download CEPII Gravity dataset for bilateral trade flows.

The CEPII Gravity dataset is a comprehensive database of bilateral trade and
gravity variables (distance, colonial ties, common language, etc.) widely used
in international trade research.

Source: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8
Dataset: Gravity (current version)
Documentation: http://www.cepii.fr/CEPII/en/publications/wp/abstract.asp?NoDoc=3877

Key variables extracted:
- iso3_o, iso3_d: Origin and destination ISO3 codes
- year: Year
- tradeflow_comtrade_o, tradeflow_comtrade_d: Trade flows from UN Comtrade
- tradeflow_baci: Trade flow from BACI (CEPII's cleaned Comtrade data)
- distw, distw_harmonic: Weighted distance measures
- contig: Contiguity (shared border)
- comlang_off: Common official language
- colony: Colonial relationship
- comcol: Common colonizer
- col45: Colony after 1945
- rta: Regional trade agreement
- gdp_o, gdp_d: GDP of origin and destination
- pop_o, pop_d: Population
"""

import os
import zipfile
import io
import pandas as pd
import requests

# ── Configuration ──────────────────────────────────────────────────────
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
# CEPII Gravity dataset URL (updated periodically; check CEPII website)
GRAVITY_URL = "http://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip"
# Alternative direct links
GRAVITY_ALT_URLS = [
    "https://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip",
    "http://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202102.zip",
]
YEAR_MIN = 1990
YEAR_MAX = 2020

# Variables to keep
GRAVITY_VARS = [
    # Identifiers
    "iso3_o",          # Origin country ISO3
    "iso3_d",          # Destination country ISO3
    "country_id_o",    # Origin country numeric ID
    "country_id_d",    # Destination country numeric ID
    "year",
    # Trade flows
    "tradeflow_comtrade_o",  # Trade flow reported by origin (exports)
    "tradeflow_comtrade_d",  # Trade flow reported by destination (imports)
    "tradeflow_baci",        # Trade flow from BACI
    "tradeflow_imf_o",       # Trade flow from IMF (origin-reported)
    "tradeflow_imf_d",       # Trade flow from IMF (destination-reported)
    # Distance measures
    "distw",                 # Weighted distance (pop-weighted, km)
    "dist",                  # Simple distance between capitals
    "distcap",               # Distance between capitals
    # Geographic/cultural variables
    "contig",                # Contiguity (=1 if shared border)
    "comlang_off",           # Common official language
    "comlang_ethno",         # Common language (ethnological)
    "colony",                # Ever in colonial relationship
    "comcol",                # Common colonizer
    "col45",                 # Colony after 1945
    "smctry",                # Same country (historically)
    # Economic variables
    "gdp_o",                 # GDP origin (current USD)
    "gdp_d",                 # GDP destination (current USD)
    "gdpcap_o",              # GDP per capita origin
    "gdpcap_d",              # GDP per capita destination
    "pop_o",                 # Population origin
    "pop_d",                 # Population destination
    # Trade agreements
    "rta",                   # Regional trade agreement (=1 if yes)
    "rta_type",              # Type of RTA
    # Other controls
    "comrelig",              # Common religion index
    "heg_o",                 # Origin is regional hegemon
    "heg_d",                 # Destination is regional hegemon
    "landlocked_o",          # Origin is landlocked
    "landlocked_d",          # Destination is landlocked
]


def download_gravity():
    """
    Download the CEPII Gravity dataset.
    Returns a pandas DataFrame.
    """
    urls_to_try = [GRAVITY_URL] + GRAVITY_ALT_URLS

    for url in urls_to_try:
        try:
            print(f"Downloading CEPII Gravity from {url} ...")
            response = requests.get(url, timeout=600)
            response.raise_for_status()

            with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
                # The main file is usually named Gravity_V*.csv
                csv_name = [f for f in csv_files if "Gravity" in f and "Notes" not in f]
                if csv_name:
                    csv_name = csv_name[0]
                else:
                    csv_name = csv_files[0]

                print(f"  Extracting {csv_name} ...")
                with zf.open(csv_name) as csv_file:
                    df = pd.read_csv(csv_file, low_memory=False)

            print(f"  Raw dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
            return df

        except Exception as e:
            print(f"  Failed: {e}")
            continue

    raise RuntimeError("All download URLs failed. Please download manually from http://www.cepii.fr/")


def process_gravity(df):
    """
    Filter to 1990-2020, select key variables, handle missing trade flows.
    """
    # Filter years
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)].copy()
    print(f"  After year filter ({YEAR_MIN}-{YEAR_MAX}): {df.shape[0]:,} rows")

    # Select variables (keep only those that exist)
    available_vars = [v for v in GRAVITY_VARS if v in df.columns]
    missing_vars = [v for v in GRAVITY_VARS if v not in df.columns]
    if missing_vars:
        print(f"  Warning: variables not found: {missing_vars}")

    df = df[available_vars].copy()

    # Create a unified trade flow variable (prefer BACI, then Comtrade, then IMF)
    trade_cols = ["tradeflow_baci", "tradeflow_comtrade_o", "tradeflow_comtrade_d",
                  "tradeflow_imf_o", "tradeflow_imf_d"]
    existing_trade = [c for c in trade_cols if c in df.columns]
    if existing_trade:
        df["trade_flow"] = df[existing_trade[0]]
        for col in existing_trade[1:]:
            df["trade_flow"] = df["trade_flow"].fillna(df[col])
        print(f"  Unified trade_flow: {df['trade_flow'].notna().sum():,} non-null values")

    # Sort
    df = df.sort_values(["iso3_o", "iso3_d", "year"]).reset_index(drop=True)

    return df


def main():
    # Download
    df_raw = download_gravity()

    # Process
    df = process_gravity(df_raw)

    # Save
    outpath = os.path.join(OUTPUT_DIR, "cepii_gravity_1990_2020.csv")
    df.to_csv(outpath, index=False)
    print(f"\nSaved: {outpath}")
    print(f"  Shape: {df.shape}")
    print(f"  Country pairs: {df.groupby(['iso3_o', 'iso3_d']).ngroups:,}")
    print(f"  Year range: {df['year'].min()}-{df['year'].max()}")
    print(f"\nSample:\n{df.head()}")

    return df


if __name__ == "__main__":
    main()
