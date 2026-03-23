"""
01_download_vdem.py
Download V-Dem (Varieties of Democracy) dataset and extract democracy indices.

V-Dem provides the most comprehensive democracy measurement dataset,
covering 202 countries from 1789 to the present.

Source: https://v-dem.net/
Dataset: V-Dem Full+Others (Country-Year)
Documentation: https://v-dem.net/documents/38/v-dem_codebook_v14.pdf

Key variables extracted:
- v2x_polyarchy: Electoral Democracy Index (0-1)
- v2x_libdem: Liberal Democracy Index (0-1)
- v2x_partipdem: Participatory Democracy Index (0-1)
- v2x_delibdem: Deliberative Democracy Index (0-1)
- v2x_egaldem: Egalitarian Democracy Index (0-1)
- country_name, country_text_id (ISO 3166-1 alpha-3), year
"""

import os
import zipfile
import io
import pandas as pd
import requests

# ── Configuration ──────────────────────────────────────────────────────
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
VDEM_URL = "https://v-dem.net/documents/24/V-Dem-CY-Full+Others-v14.csv.zip"
# Alternative: use the vdemdata R package or the GitHub mirror
VDEM_GITHUB_URL = "https://github.com/vdeminstitute/vdemdata/raw/master/data/vdem.rda"
YEAR_MIN = 1990
YEAR_MAX = 2020

# Variables to keep (democracy indices + identifiers)
VDEM_VARS = [
    "country_name",
    "country_text_id",  # ISO 3166-1 alpha-3 code
    "COWcode",           # Correlates of War country code
    "year",
    # High-level democracy indices
    "v2x_polyarchy",     # Electoral Democracy Index
    "v2x_libdem",        # Liberal Democracy Index
    "v2x_partipdem",     # Participatory Democracy Index
    "v2x_delibdem",      # Deliberative Democracy Index
    "v2x_egaldem",       # Egalitarian Democracy Index
    # Component indices (useful for robustness checks)
    "v2x_freexp_altinf", # Freedom of Expression and Alt. Sources of Info
    "v2x_frassoc_thick", # Freedom of Association (thick)
    "v2x_suffr",         # Share of population with suffrage
    "v2xel_frefair",     # Clean Elections Index
    "v2x_elecoff",       # Elected Officials Index
    "v2x_liberal",       # Liberal Component Index
    "v2xcl_rol",         # Rule of Law Index
    "v2x_jucon",         # Judicial Constraints on the Executive
    "v2xlg_legcon",      # Legislative Constraints on the Executive
    "v2x_partip",        # Participatory Component Index
    "v2x_egal",          # Egalitarian Component Index
]


def download_vdem_csv():
    """
    Download the V-Dem Country-Year dataset from the official website.
    Returns a pandas DataFrame.
    """
    print(f"Downloading V-Dem dataset from {VDEM_URL} ...")
    response = requests.get(VDEM_URL, timeout=300)
    response.raise_for_status()

    # The download is a ZIP file containing one CSV
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        csv_name = [f for f in zf.namelist() if f.endswith(".csv")][0]
        print(f"  Extracting {csv_name} ...")
        with zf.open(csv_name) as csv_file:
            df = pd.read_csv(csv_file, low_memory=False)

    print(f"  Raw dataset: {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def download_vdem_alternative():
    """
    Alternative: use the vdemdata Python wrapper or direct CSV from GitHub.
    This is a fallback if the main URL changes.
    """
    # Option 1: pip install vdemdata (unofficial)
    # import vdemdata
    # df = vdemdata.load()

    # Option 2: Direct CSV link (may vary by version)
    alt_url = "https://raw.githubusercontent.com/vdeminstitute/vdemdata/master/inst/extdata/V-Dem-CY-Full+Others-v14.csv"
    print(f"Trying alternative URL: {alt_url}")
    df = pd.read_csv(alt_url, low_memory=False)
    return df


def process_vdem(df):
    """
    Filter to 1990-2020, select key democracy variables, clean up.
    """
    # Filter years
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)].copy()
    print(f"  After year filter ({YEAR_MIN}-{YEAR_MAX}): {df.shape[0]} rows")

    # Select variables (keep only those that exist in the dataset)
    available_vars = [v for v in VDEM_VARS if v in df.columns]
    missing_vars = [v for v in VDEM_VARS if v not in df.columns]
    if missing_vars:
        print(f"  Warning: variables not found in dataset: {missing_vars}")

    df = df[available_vars].copy()

    # Rename country_text_id to iso3 for easier merging
    df = df.rename(columns={"country_text_id": "iso3"})

    # Drop rows where all democracy indices are NaN
    democracy_cols = [c for c in df.columns if c.startswith("v2x_") or c.startswith("v2xcl_") or c.startswith("v2xlg_") or c.startswith("v2xel_")]
    df = df.dropna(subset=democracy_cols, how="all")
    print(f"  After dropping all-NaN democracy rows: {df.shape[0]} rows")

    # Sort
    df = df.sort_values(["iso3", "year"]).reset_index(drop=True)

    return df


def main():
    # Download
    try:
        df_raw = download_vdem_csv()
    except Exception as e:
        print(f"Primary download failed: {e}")
        print("Trying alternative source...")
        df_raw = download_vdem_alternative()

    # Process
    df = process_vdem(df_raw)

    # Save
    outpath = os.path.join(OUTPUT_DIR, "vdem_democracy_1990_2020.csv")
    df.to_csv(outpath, index=False)
    print(f"\nSaved: {outpath}")
    print(f"  Shape: {df.shape}")
    print(f"  Countries: {df['iso3'].nunique()}")
    print(f"  Year range: {df['year'].min()}-{df['year'].max()}")
    print(f"\nSample:\n{df.head()}")

    return df


if __name__ == "__main__":
    main()
