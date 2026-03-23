"""
Download GDP per capita (current US$) and Population data for Latin American countries
from the World Bank API (WDI - World Development Indicators).

Indicators:
  - NY.GDP.PCAP.CD: GDP per capita (current US$)
  - SP.POP.TOTL: Population, total

Coverage: All Latin American countries, 2000-2023.

Usage:
    pip install wbgapi pandas
    python download_wb_data.py

Output:
    - latam_gdp_pcap_population_panel.csv  (long format: country-year panel)
    - latam_gdp_pcap_wide.csv              (wide format for GDP per capita)
    - latam_population_wide.csv            (wide format for population)
"""

import wbgapi as wb
import pandas as pd
import os

# --------------------------------------------------------------------------- #
# 1. Define Latin American countries (ISO-3 codes)
# --------------------------------------------------------------------------- #
LATAM_COUNTRIES = [
    "ARG",  # Argentina
    "BOL",  # Bolivia
    "BRA",  # Brazil
    "CHL",  # Chile
    "COL",  # Colombia
    "CRI",  # Costa Rica
    "CUB",  # Cuba
    "DOM",  # Dominican Republic
    "ECU",  # Ecuador
    "SLV",  # El Salvador
    "GTM",  # Guatemala
    "HTI",  # Haiti
    "HND",  # Honduras
    "MEX",  # Mexico
    "NIC",  # Nicaragua
    "PAN",  # Panama
    "PRY",  # Paraguay
    "PER",  # Peru
    "URY",  # Uruguay
    "VEN",  # Venezuela
]

INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "SP.POP.TOTL": "population",
}

YEAR_RANGE = range(2000, 2024)  # 2000 to 2023 inclusive

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- #
# 2. Download data via wbgapi
# --------------------------------------------------------------------------- #
def download_data():
    """Download GDP per capita and population from World Bank API."""

    frames = []

    for wb_code, col_name in INDICATORS.items():
        print(f"Downloading {col_name} ({wb_code})...")
        df = wb.data.DataFrame(
            wb_code,
            economy=LATAM_COUNTRIES,
            time=YEAR_RANGE,
            labels=True,
            columns="series",
            numericTimeKeys=True,
        )
        # The DataFrame comes with economies as rows and years as columns.
        # Reset index to get a long-format panel.
        df = df.reset_index()
        df = df.melt(
            id_vars=["economy", "Economy"],
            var_name="year",
            value_name=col_name,
        )
        df.rename(columns={"economy": "iso3", "Economy": "country_name"}, inplace=True)
        df["year"] = df["year"].astype(int)
        frames.append(df.set_index(["iso3", "country_name", "year"]))

    # Merge all indicators
    panel = frames[0].join(frames[1:], how="outer").reset_index()
    panel.sort_values(["iso3", "year"], inplace=True)

    return panel


# --------------------------------------------------------------------------- #
# 3. Alternative download using pandas_datareader / direct URL
# --------------------------------------------------------------------------- #
def download_data_alternative():
    """
    Alternative approach: download CSV directly from the World Bank bulk
    download page. Useful if wbgapi is not available.
    """
    import urllib.request
    import zipfile
    import io

    base_url = "https://api.worldbank.org/v2/en/indicator/{}?downloadformat=csv"

    all_data = []

    for wb_code, col_name in INDICATORS.items():
        url = base_url.format(wb_code)
        print(f"Downloading {col_name} from {url}...")
        response = urllib.request.urlopen(url)
        zip_content = io.BytesIO(response.read())

        with zipfile.ZipFile(zip_content) as z:
            # Find the main data CSV (starts with "API_")
            csv_name = [n for n in z.namelist() if n.startswith("API_")][0]
            with z.open(csv_name) as f:
                df = pd.read_csv(f, skiprows=4)

        # Filter to Latin American countries
        df = df[df["Country Code"].isin(LATAM_COUNTRIES)]

        # Reshape: wide -> long
        year_cols = [str(y) for y in YEAR_RANGE]
        id_cols = ["Country Name", "Country Code"]
        df_long = df[id_cols + year_cols].melt(
            id_vars=id_cols, var_name="year", value_name=col_name
        )
        df_long.rename(
            columns={"Country Code": "iso3", "Country Name": "country_name"},
            inplace=True,
        )
        df_long["year"] = df_long["year"].astype(int)
        all_data.append(df_long.set_index(["iso3", "country_name", "year"]))

    panel = all_data[0].join(all_data[1:], how="outer").reset_index()
    panel.sort_values(["iso3", "year"], inplace=True)
    return panel


# --------------------------------------------------------------------------- #
# 4. Save outputs
# --------------------------------------------------------------------------- #
def save_outputs(panel: pd.DataFrame):
    """Save panel in long and wide formats."""

    # Long format (panel)
    long_path = os.path.join(OUTPUT_DIR, "latam_gdp_pcap_population_panel.csv")
    panel.to_csv(long_path, index=False)
    print(f"Saved long-format panel: {long_path}")

    # Wide format - GDP per capita
    gdp_wide = panel.pivot_table(
        index=["iso3", "country_name"],
        columns="year",
        values="gdp_per_capita_current_usd",
    )
    gdp_wide.columns = [f"gdp_pcap_{y}" for y in gdp_wide.columns]
    gdp_wide_path = os.path.join(OUTPUT_DIR, "latam_gdp_pcap_wide.csv")
    gdp_wide.to_csv(gdp_wide_path)
    print(f"Saved GDP per capita wide: {gdp_wide_path}")

    # Wide format - Population
    pop_wide = panel.pivot_table(
        index=["iso3", "country_name"],
        columns="year",
        values="population",
    )
    pop_wide.columns = [f"pop_{y}" for y in pop_wide.columns]
    pop_wide_path = os.path.join(OUTPUT_DIR, "latam_population_wide.csv")
    pop_wide.to_csv(pop_wide_path)
    print(f"Saved population wide: {pop_wide_path}")


# --------------------------------------------------------------------------- #
# 5. Main
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        panel = download_data()
    except ImportError:
        print("wbgapi not found; using alternative download method...")
        panel = download_data_alternative()

    save_outputs(panel)

    print(f"\nPanel shape: {panel.shape}")
    print(f"Countries: {panel['iso3'].nunique()}")
    print(f"Years: {sorted(panel['year'].unique())}")
    print("\nSample rows:")
    print(panel.head(10).to_string(index=False))
    print("\nDone.")
