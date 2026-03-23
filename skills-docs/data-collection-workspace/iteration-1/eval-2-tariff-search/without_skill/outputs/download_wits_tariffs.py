#!/usr/bin/env python3
"""
Download product-level (HS6) tariff data from WITS/TRAINS via the
world_trade_data Python package.

This script downloads MFN applied tariff rates for OECD countries at
the HS 2-digit (chapter) level for 2000-2010.

Usage:
    pip install world_trade_data pandas
    python download_wits_tariffs.py

Output:
    oecd_tariffs_wits_hs2_2000_2010.csv

Notes:
    - The WITS API has rate limits. This script includes delays between requests.
    - The API does not allow "All Reporter + All Partners" in a single query.
    - For HS6-level data, you would need to iterate over product codes as well.
    - Estimated tariff data may have better coverage than reported data.
"""

import pandas as pd
import time
import os
import sys

try:
    import world_trade_data as wits
except ImportError:
    print("Please install: pip install world_trade_data")
    sys.exit(1)

# OECD member countries (ISO3 numeric codes used by WITS)
# These are the UN M49 / ISO 3166-1 numeric codes
OECD_COUNTRIES = {
    "036": "Australia",
    "040": "Austria",
    "056": "Belgium",
    "124": "Canada",
    "152": "Chile",
    "203": "Czech Republic",
    "208": "Denmark",
    "246": "Finland",
    "250": "France",
    "276": "Germany",
    "300": "Greece",
    "348": "Hungary",
    "352": "Iceland",
    "372": "Ireland",
    "380": "Italy",
    "392": "Japan",
    "410": "Korea, Rep.",
    "442": "Luxembourg",
    "484": "Mexico",
    "528": "Netherlands",
    "554": "New Zealand",
    "578": "Norway",
    "616": "Poland",
    "620": "Portugal",
    "703": "Slovak Republic",
    "724": "Spain",
    "752": "Sweden",
    "756": "Switzerland",
    "792": "Turkey",
    "826": "United Kingdom",
    "840": "United States",
}

YEARS = range(2000, 2011)

# HS 2-digit product chapters (01-97, excluding 77 which is reserved)
HS2_CHAPTERS = [f"{i:02d}" for i in range(1, 98) if i != 77]


def download_estimated_tariffs():
    """
    Download estimated tariff data (better coverage) for OECD countries.
    Uses aggregate product code '000' for all products.
    """
    output_dir = os.path.dirname(os.path.abspath(__file__))
    all_data = []
    errors = []

    total = len(OECD_COUNTRIES) * len(YEARS)
    count = 0

    for country_code, country_name in OECD_COUNTRIES.items():
        for year in YEARS:
            count += 1
            print(f"[{count}/{total}] {country_name} ({country_code}), {year}...")

            try:
                # Get estimated tariff for all products (aggregate)
                df = wits.get_tariff_estimated(
                    reporter=country_code,
                    partner="000",  # World aggregate
                    product="all",  # All HS2 chapters
                )

                if df is not None and not df.empty:
                    # Filter to the requested year if year column exists
                    if "Year" in df.columns:
                        df_year = df[df["Year"] == year]
                    else:
                        df_year = df

                    df_year = df_year.copy()
                    df_year["reporter_code"] = country_code
                    df_year["reporter_name"] = country_name
                    df_year["year"] = year
                    all_data.append(df_year)
                    print(f"  -> {len(df_year)} rows")
                else:
                    print(f"  -> No data")

            except Exception as e:
                error_msg = f"{country_name} {year}: {str(e)}"
                errors.append(error_msg)
                print(f"  -> ERROR: {e}")

            # Respect rate limits
            time.sleep(1.5)

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        output_path = os.path.join(output_dir, "oecd_tariffs_wits_estimated_2000_2010.csv")
        result.to_csv(output_path, index=False)
        print(f"\nSaved {len(result)} rows to {output_path}")
    else:
        print("\nNo data downloaded.")

    if errors:
        error_path = os.path.join(output_dir, "wits_download_errors.log")
        with open(error_path, "w") as f:
            f.write("\n".join(errors))
        print(f"Errors logged to {error_path}")


def download_reported_tariffs_by_chapter():
    """
    Download reported tariff data at HS2 chapter level.
    This is more granular but may have more missing data.

    WARNING: This generates a LOT of API calls
    (31 countries x 11 years x ~96 chapters = ~32,000+ calls).
    Consider running for a subset of countries/years first.
    """
    output_dir = os.path.dirname(os.path.abspath(__file__))
    all_data = []

    # For demonstration, just do a few countries
    demo_countries = {"840": "United States", "276": "Germany", "392": "Japan"}

    for country_code, country_name in demo_countries.items():
        for year in [2000, 2005, 2010]:  # Sample years
            print(f"\n{country_name}, {year}:")
            try:
                df = wits.get_tariff_reported(
                    reporter=country_code,
                    partner="all",
                    product="all",
                )

                if df is not None and not df.empty:
                    df = df.copy()
                    df["reporter_code"] = country_code
                    df["reporter_name"] = country_name
                    df["year"] = year
                    all_data.append(df)
                    print(f"  -> {len(df)} rows")

            except Exception as e:
                print(f"  -> ERROR: {e}")

            time.sleep(2)

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        output_path = os.path.join(output_dir, "oecd_tariffs_wits_reported_sample.csv")
        result.to_csv(output_path, index=False)
        print(f"\nSaved {len(result)} rows to {output_path}")


def main():
    print("=" * 60)
    print("WITS/TRAINS Tariff Data Downloader for OECD Countries")
    print("=" * 60)

    print("\n--- Phase 1: Estimated Tariffs (All Products, Aggregate) ---")
    download_estimated_tariffs()

    # Uncomment if you also want HS2-level reported tariffs (slow):
    # print("\n--- Phase 2: Reported Tariffs by HS2 Chapter (Sample) ---")
    # download_reported_tariffs_by_chapter()


if __name__ == "__main__":
    main()
