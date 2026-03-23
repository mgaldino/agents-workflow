#!/usr/bin/env python3
"""
Download tariff data from the WTO Tariff and Trade Data (TTD) portal.

The WTO TTD portal (https://ttd.wto.org/en) provides tariff profiles
for 170+ economies. Data can be downloaded via the web interface or
via their bulk download feature.

This script automates the download using the WTO's data download endpoints.

Usage:
    pip install requests pandas
    python download_wto_tariffs.py

Output:
    oecd_tariffs_wto_2000_2010.csv

Notes:
    - The WTO TTD API may require accepting terms of use.
    - For bulk downloads, visit https://ttd.wto.org/en/download directly.
    - WTO data includes MFN applied, bound rates, and duty-free shares.
"""

import requests
import pandas as pd
import time
import os

# OECD countries with WTO member codes
# WTO uses ISO3 alpha codes
OECD_ISO3 = [
    "AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "FIN", "FRA", "DEU",
    "GRC", "HUN", "ISL", "IRL", "ITA", "JPN", "KOR", "LUX", "MEX", "NLD",
    "NZL", "NOR", "POL", "PRT", "SVK", "ESP", "SWE", "CHE", "TUR", "GBR",
    "USA",
]

# Note: Many EU member states report tariffs as "European Union" (EU/EEC)
# in the WTO system. Individual country queries may redirect to the EU entry.
EU_MEMBERS_IN_OECD = {
    "AUT", "BEL", "CZE", "DNK", "FIN", "FRA", "DEU", "GRC", "HUN",
    "IRL", "ITA", "LUX", "NLD", "POL", "PRT", "SVK", "ESP", "SWE", "GBR",
}

# For WTO tariff queries, EU members should use the EU reporter code
# Non-EU OECD members report individually
NON_EU_OECD = [c for c in OECD_ISO3 if c not in EU_MEMBERS_IN_OECD]
# Add EU as a single entity
REPORTERS = NON_EU_OECD + ["EEC"]  # EEC is sometimes used for EU in WTO data

YEARS = range(2000, 2011)


def download_wto_tariff_profiles():
    """
    Download tariff profile data from WTO TTD.

    The WTO TTD provides several endpoints. This function uses the
    data download feature which provides CSV files.

    Note: The exact API structure may change. Check https://ttd.wto.org/en
    for the latest documentation.
    """
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # WTO TTD API base URL (this is approximate; actual endpoints may differ)
    base_url = "https://ttd.wto.org/api"

    # Example: download tariff summary indicators
    # The actual endpoint structure needs to be verified against current WTO API docs
    all_data = []

    for reporter in REPORTERS:
        for year in YEARS:
            url = f"{base_url}/tariff-summary"
            params = {
                "reporter": reporter,
                "year": year,
                "indicator": "MFN_AVG",  # MFN simple average
                "format": "json",
            }

            try:
                print(f"Fetching {reporter}, {year}...")
                response = requests.get(url, params=params, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    if data:
                        all_data.append({
                            "reporter": reporter,
                            "year": year,
                            "data": data,
                        })
                        print(f"  -> OK")
                else:
                    print(f"  -> HTTP {response.status_code}")

            except requests.RequestException as e:
                print(f"  -> Error: {e}")

            time.sleep(1)

    if all_data:
        # Process and save (structure depends on actual API response)
        print(f"\nDownloaded {len(all_data)} records")
        # Save raw JSON responses for further processing
        import json
        raw_path = os.path.join(output_dir, "wto_tariff_raw.json")
        with open(raw_path, "w") as f:
            json.dump(all_data, f, indent=2)
        print(f"Raw data saved to {raw_path}")
    else:
        print("\nNo data downloaded. The WTO TTD API structure may have changed.")
        print("Alternative: visit https://ttd.wto.org/en/download for manual bulk download.")


def alternative_manual_download_instructions():
    """
    Print instructions for manual download from WTO TTD portal.
    This is often the most reliable approach.
    """
    print("""
    ================================================================
    MANUAL DOWNLOAD INSTRUCTIONS -- WTO Tariff and Trade Data (TTD)
    ================================================================

    1. Go to https://ttd.wto.org/en

    2. Select "Download" from the top menu, or go directly to:
       https://ttd.wto.org/en/download

    3. Configure your query:
       - Reporter: Select OECD countries (or "European Union" for EU members)
       - Year: 2000 to 2010
       - Product: All products (or specific HS chapters)
       - Duty type: MFN Applied

    4. Click "Download" to get a CSV/Excel file

    5. For EU member states (Austria, Belgium, Czech Republic, Denmark,
       Finland, France, Germany, Greece, Hungary, Ireland, Italy,
       Luxembourg, Netherlands, Poland, Portugal, Slovak Republic,
       Spain, Sweden, United Kingdom):
       -> Use "European Union" as the reporter, since EU members
          share a common external tariff (Common External Tariff, CET).

    6. Non-EU OECD members report individually:
       Australia, Canada, Chile, Iceland, Japan, Korea, Mexico,
       New Zealand, Norway, Switzerland, Turkey, United States.

    ================================================================
    """)


def main():
    print("WTO Tariff and Trade Data Downloader")
    print("=" * 50)

    # Print manual download instructions (most reliable method)
    alternative_manual_download_instructions()

    # Attempt API download
    print("\nAttempting API download (may fail if endpoint has changed)...")
    download_wto_tariff_profiles()


if __name__ == "__main__":
    main()
