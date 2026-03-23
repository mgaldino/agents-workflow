"""
Validate the downloaded Latin America GDP/Population panel data.

Checks:
  1. All 20 expected countries are present.
  2. All years 2000-2023 are present for each country.
  3. No unexpected negative values.
  4. GDP per capita is in a plausible range.
  5. Population is in a plausible range.
  6. Missing value report.

Usage:
    python validate_data.py latam_gdp_pcap_population_panel.csv
"""

import sys
import os
import pandas as pd

EXPECTED_COUNTRIES = {
    "ARG", "BOL", "BRA", "CHL", "COL", "CRI", "CUB", "DOM",
    "ECU", "SLV", "GTM", "HTI", "HND", "MEX", "NIC", "PAN",
    "PRY", "PER", "URY", "VEN",
}
EXPECTED_YEARS = set(range(2000, 2024))
N_COUNTRIES = 20
N_YEARS = 24


def validate(filepath: str):
    print(f"Validating: {filepath}\n")
    df = pd.read_csv(filepath)

    errors = []
    warnings = []

    # ---- Basic structure ------------------------------------------------- #
    required_cols = {"iso3", "country_name", "year",
                     "gdp_per_capita_current_usd", "population"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
        print("FATAL: Missing columns. Cannot proceed.")
        return False

    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Expected: {N_COUNTRIES * N_YEARS} rows (20 countries x 24 years)\n")

    # ---- Country coverage ------------------------------------------------ #
    found_countries = set(df["iso3"].unique())
    missing_countries = EXPECTED_COUNTRIES - found_countries
    extra_countries = found_countries - EXPECTED_COUNTRIES

    if missing_countries:
        errors.append(f"Missing countries: {missing_countries}")
    if extra_countries:
        warnings.append(f"Extra countries (unexpected): {extra_countries}")
    print(f"Countries found: {len(found_countries)} / {N_COUNTRIES}")

    # ---- Year coverage --------------------------------------------------- #
    found_years = set(df["year"].unique())
    missing_years = EXPECTED_YEARS - found_years
    if missing_years:
        errors.append(f"Missing years (global): {sorted(missing_years)}")
    print(f"Years found: {min(found_years)}-{max(found_years)} "
          f"({len(found_years)} unique)\n")

    # ---- Per-country year completeness ----------------------------------- #
    for iso3 in sorted(EXPECTED_COUNTRIES & found_countries):
        country_years = set(df.loc[df["iso3"] == iso3, "year"])
        gap = EXPECTED_YEARS - country_years
        if gap:
            warnings.append(f"{iso3}: missing years {sorted(gap)}")

    # ---- Missing values -------------------------------------------------- #
    gdp_na = df["gdp_per_capita_current_usd"].isna().sum()
    pop_na = df["population"].isna().sum()
    print(f"Missing GDP per capita: {gdp_na} / {len(df)}")
    print(f"Missing population:     {pop_na} / {len(df)}\n")

    if gdp_na > 0:
        na_rows = df[df["gdp_per_capita_current_usd"].isna()]
        warnings.append(
            f"GDP NA in: {na_rows[['iso3','year']].values.tolist()}"
        )
    if pop_na > 0:
        na_rows = df[df["population"].isna()]
        warnings.append(
            f"Population NA in: {na_rows[['iso3','year']].values.tolist()}"
        )

    # ---- Plausibility checks --------------------------------------------- #
    gdp_vals = df["gdp_per_capita_current_usd"].dropna()
    pop_vals = df["population"].dropna()

    if (gdp_vals < 0).any():
        errors.append("Negative GDP per capita values found!")
    if (pop_vals < 0).any():
        errors.append("Negative population values found!")

    # GDP per capita: Haiti ~$500 to Chile/Uruguay ~$20k is the range
    if gdp_vals.min() < 50:
        warnings.append(f"Very low GDP per capita: {gdp_vals.min():.2f}")
    if gdp_vals.max() > 50000:
        warnings.append(f"Very high GDP per capita: {gdp_vals.max():.2f}")

    # Population: Uruguay ~3M to Brazil ~215M
    if pop_vals.min() < 500_000:
        warnings.append(f"Very low population: {pop_vals.min():.0f}")
    if pop_vals.max() > 300_000_000:
        warnings.append(f"Very high population: {pop_vals.max():.0f}")

    # ---- Summary --------------------------------------------------------- #
    print("=" * 60)
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")
    else:
        print("\nNo errors found.")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")
    else:
        print("No warnings.")

    print("\n" + "=" * 60)
    ok = len(errors) == 0
    print(f"RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default path
        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "latam_gdp_pcap_population_panel.csv",
        )
    else:
        filepath = sys.argv[1]

    success = validate(filepath)
    sys.exit(0 if success else 1)
