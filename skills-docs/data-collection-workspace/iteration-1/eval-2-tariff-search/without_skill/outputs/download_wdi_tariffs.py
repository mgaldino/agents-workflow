#!/usr/bin/env python3
"""
Download OECD tariff data from World Bank World Development Indicators (WDI) API.

Indicator: TM.TAX.MRCH.WM.AR.ZS
    Tariff rate, applied, weighted mean, all products (%)

Coverage: OECD member countries, 2000-2010
API: World Bank Indicators API v2 (no authentication required)

Usage:
    pip install requests pandas
    python download_wdi_tariffs.py

Output:
    oecd_tariffs_wdi_2000_2010.csv
"""

import requests
import pandas as pd
import time
import os

# OECD member countries as of 2010 (30 members before Chile joined in 2010)
# ISO2 codes used by World Bank API
OECD_COUNTRIES = {
    "AU": "Australia",
    "AT": "Austria",
    "BE": "Belgium",
    "CA": "Canada",
    "CL": "Chile",        # joined May 2010
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HU": "Hungary",
    "IS": "Iceland",
    "IE": "Ireland",
    "IT": "Italy",
    "JP": "Japan",
    "KR": "Korea, Rep.",
    "LU": "Luxembourg",
    "MX": "Mexico",
    "NL": "Netherlands",
    "NZ": "New Zealand",
    "NO": "Norway",
    "PL": "Poland",
    "PT": "Portugal",
    "SK": "Slovak Republic",
    "ES": "Spain",
    "SE": "Sweden",
    "CH": "Switzerland",
    "TR": "Turkey",
    "GB": "United Kingdom",
    "US": "United States",
}

# WDI Tariff indicators
INDICATORS = {
    "TM.TAX.MRCH.WM.AR.ZS": "tariff_weighted_mean_all_products",
    "TM.TAX.MRCH.SM.AR.ZS": "tariff_simple_mean_all_products",
    "TM.TAX.MRCH.WM.FN.ZS": "tariff_weighted_mean_manufactured",
    "TM.TAX.TCOM.WM.AR.ZS": "tariff_weighted_mean_primary",
}

BASE_URL = "https://api.worldbank.org/v2"
START_YEAR = 2000
END_YEAR = 2010


def fetch_indicator(indicator_code: str, countries: str, start: int, end: int) -> list:
    """
    Fetch a single indicator from the World Bank API for a group of countries.

    Parameters
    ----------
    indicator_code : str
        WDI indicator code (e.g., 'TM.TAX.MRCH.WM.AR.ZS')
    countries : str
        Semicolon-separated ISO2 country codes (e.g., 'US;CA;DE')
    start : int
        Start year
    end : int
        End year

    Returns
    -------
    list of dict
        Each dict has keys: country_code, country_name, year, value
    """
    url = f"{BASE_URL}/country/{countries}/indicator/{indicator_code}"
    params = {
        "date": f"{start}:{end}",
        "format": "json",
        "per_page": 1000,
    }

    all_records = []
    page = 1

    while True:
        params["page"] = page
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching {indicator_code} page {page}: {e}")
            break

        # World Bank API returns [metadata, data]
        if len(data) < 2 or data[1] is None:
            break

        metadata = data[0]
        records = data[1]

        for record in records:
            all_records.append({
                "country_code": record["countryiso3code"],
                "country_name": record["country"]["value"],
                "year": int(record["date"]),
                "value": record["value"],
                "indicator": indicator_code,
            })

        # Check if there are more pages
        total_pages = metadata.get("pages", 1)
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)  # Be polite to the API

    return all_records


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Build country string for API (semicolon-separated ISO2 codes)
    country_str = ";".join(OECD_COUNTRIES.keys())

    all_data = []

    for indicator_code, indicator_name in INDICATORS.items():
        print(f"Fetching {indicator_name} ({indicator_code})...")
        records = fetch_indicator(indicator_code, country_str, START_YEAR, END_YEAR)
        for r in records:
            r["indicator_name"] = indicator_name
        all_data.extend(records)
        print(f"  -> {len(records)} records")
        time.sleep(1)

    # Create DataFrame
    df = pd.DataFrame(all_data)

    if df.empty:
        print("WARNING: No data retrieved. Check your internet connection.")
        return

    # Pivot to wide format: one row per country-year, columns for each indicator
    df_wide = df.pivot_table(
        index=["country_code", "country_name", "year"],
        columns="indicator_name",
        values="value",
    ).reset_index()

    # Flatten column names
    df_wide.columns.name = None

    # Sort
    df_wide = df_wide.sort_values(["country_code", "year"]).reset_index(drop=True)

    # Save
    output_path = os.path.join(output_dir, "oecd_tariffs_wdi_2000_2010.csv")
    df_wide.to_csv(output_path, index=False)
    print(f"\nSaved {len(df_wide)} rows to {output_path}")

    # Also save the long format
    output_long = os.path.join(output_dir, "oecd_tariffs_wdi_2000_2010_long.csv")
    df_long = df[["country_code", "country_name", "year", "indicator_name", "value"]]
    df_long = df_long.sort_values(["country_code", "year", "indicator_name"]).reset_index(drop=True)
    df_long.to_csv(output_long, index=False)
    print(f"Saved {len(df_long)} rows (long format) to {output_long}")

    # Print summary
    print("\n--- Summary ---")
    print(f"Countries: {df_wide['country_code'].nunique()}")
    print(f"Years: {sorted(df_wide['year'].unique())}")
    print(f"Indicators: {list(INDICATORS.values())}")
    print(f"\nMissing values per indicator:")
    for col in INDICATORS.values():
        if col in df_wide.columns:
            n_missing = df_wide[col].isna().sum()
            n_total = len(df_wide)
            print(f"  {col}: {n_missing}/{n_total} missing ({100*n_missing/n_total:.1f}%)")


if __name__ == "__main__":
    main()
