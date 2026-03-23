"""
03_merge_democracy_trade.py
Merge V-Dem democracy indices with CEPII Gravity bilateral trade data.

Merging strategy:
- V-Dem is country-year (one row per country per year)
- CEPII Gravity is dyad-year (one row per country-pair per year)
- We merge V-Dem TWICE into Gravity: once for origin, once for destination
- Join key: ISO3 code + year

Output: A dyad-year panel with democracy indices for both trade partners
plus all gravity/trade variables.
"""

import os
import pandas as pd
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data():
    """Load the two processed datasets."""
    vdem_path = os.path.join(OUTPUT_DIR, "vdem_democracy_1990_2020.csv")
    gravity_path = os.path.join(OUTPUT_DIR, "cepii_gravity_1990_2020.csv")

    print("Loading V-Dem data...")
    vdem = pd.read_csv(vdem_path)
    print(f"  V-Dem: {vdem.shape[0]:,} rows, {vdem['iso3'].nunique()} countries")

    print("Loading CEPII Gravity data...")
    gravity = pd.read_csv(gravity_path)
    print(f"  Gravity: {gravity.shape[0]:,} rows")

    return vdem, gravity


def prepare_vdem_for_merge(vdem):
    """
    Prepare V-Dem for merging: select key columns, handle ISO3 mismatches.
    """
    # Democracy index columns (everything starting with v2x_, v2xcl_, v2xel_, v2xlg_)
    demo_cols = [c for c in vdem.columns
                 if c.startswith("v2x_") or c.startswith("v2xcl_")
                 or c.startswith("v2xel_") or c.startswith("v2xlg_")]
    id_cols = ["iso3", "year", "country_name"]
    if "COWcode" in vdem.columns:
        id_cols.append("COWcode")

    vdem = vdem[[c for c in id_cols + demo_cols if c in vdem.columns]].copy()

    # Handle known ISO3 mismatches between V-Dem and CEPII
    # V-Dem uses some non-standard codes; map them to CEPII conventions
    iso3_map = {
        "XKX": "XKX",  # Kosovo (sometimes KOS)
        "PSG": "PSE",  # Palestine (V-Dem uses PSG, CEPII uses PSE)
        "ZZB": "ZAN",  # Zanzibar (not always in CEPII)
        "SML": "SOM",  # Somaliland -> Somalia in most datasets
    }
    vdem["iso3"] = vdem["iso3"].replace(iso3_map)

    return vdem


def merge_datasets(vdem, gravity):
    """
    Merge V-Dem into Gravity twice: once for origin, once for destination.
    """
    vdem_clean = prepare_vdem_for_merge(vdem)

    # Columns to merge (democracy indices only, not country_name which would clash)
    demo_cols = [c for c in vdem_clean.columns
                 if c.startswith("v2x_") or c.startswith("v2xcl_")
                 or c.startswith("v2xel_") or c.startswith("v2xlg_")]
    merge_cols = ["iso3", "year"] + demo_cols

    # ── Merge for ORIGIN country ──────────────────────────────────────
    vdem_origin = vdem_clean[merge_cols].copy()
    vdem_origin = vdem_origin.rename(columns={c: f"{c}_o" for c in demo_cols})
    vdem_origin = vdem_origin.rename(columns={"iso3": "iso3_o"})

    print(f"\nMerging V-Dem for origin countries...")
    merged = gravity.merge(vdem_origin, on=["iso3_o", "year"], how="left")
    n_matched_o = merged[f"{demo_cols[0]}_o"].notna().sum()
    print(f"  Matched: {n_matched_o:,} / {len(merged):,} rows ({100*n_matched_o/len(merged):.1f}%)")

    # ── Merge for DESTINATION country ────────────────────────────────
    vdem_dest = vdem_clean[merge_cols].copy()
    vdem_dest = vdem_dest.rename(columns={c: f"{c}_d" for c in demo_cols})
    vdem_dest = vdem_dest.rename(columns={"iso3": "iso3_d"})

    print(f"Merging V-Dem for destination countries...")
    merged = merged.merge(vdem_dest, on=["iso3_d", "year"], how="left")
    n_matched_d = merged[f"{demo_cols[0]}_d"].notna().sum()
    print(f"  Matched: {n_matched_d:,} / {len(merged):,} rows ({100*n_matched_d/len(merged):.1f}%)")

    # ── Create derived variables ─────────────────────────────────────
    # Absolute difference in democracy (useful for research on democratic similarity)
    if "v2x_polyarchy_o" in merged.columns and "v2x_polyarchy_d" in merged.columns:
        merged["democracy_diff_polyarchy"] = (
            merged["v2x_polyarchy_o"] - merged["v2x_polyarchy_d"]
        ).abs()
        merged["democracy_avg_polyarchy"] = (
            merged["v2x_polyarchy_o"] + merged["v2x_polyarchy_d"]
        ) / 2
        merged["democracy_min_polyarchy"] = merged[
            ["v2x_polyarchy_o", "v2x_polyarchy_d"]
        ].min(axis=1)
        merged["both_democratic"] = (
            (merged["v2x_polyarchy_o"] >= 0.5) & (merged["v2x_polyarchy_d"] >= 0.5)
        ).astype(int)

    if "v2x_libdem_o" in merged.columns and "v2x_libdem_d" in merged.columns:
        merged["democracy_diff_libdem"] = (
            merged["v2x_libdem_o"] - merged["v2x_libdem_d"]
        ).abs()

    return merged


def diagnostics(merged):
    """Print merge diagnostics and data quality info."""
    print("\n" + "=" * 60)
    print("MERGE DIAGNOSTICS")
    print("=" * 60)
    print(f"Final dataset shape: {merged.shape}")
    print(f"Year range: {merged['year'].min()}-{merged['year'].max()}")
    print(f"Unique origin countries: {merged['iso3_o'].nunique()}")
    print(f"Unique destination countries: {merged['iso3_d'].nunique()}")

    # Check for unmatched countries
    demo_col = "v2x_polyarchy_o"
    if demo_col in merged.columns:
        unmatched_o = merged[merged[demo_col].isna()]["iso3_o"].unique()
        unmatched_d = merged[merged["v2x_polyarchy_d"].isna()]["iso3_d"].unique()
        print(f"\nOrigin countries without V-Dem data: {len(unmatched_o)}")
        if len(unmatched_o) <= 20:
            print(f"  {sorted(unmatched_o)}")
        print(f"Destination countries without V-Dem data: {len(unmatched_d)}")
        if len(unmatched_d) <= 20:
            print(f"  {sorted(unmatched_d)}")

    # Missing data summary
    print("\nMissing data (% of rows):")
    key_cols = ["trade_flow", "v2x_polyarchy_o", "v2x_polyarchy_d",
                "v2x_libdem_o", "v2x_libdem_d", "gdp_o", "gdp_d"]
    for col in key_cols:
        if col in merged.columns:
            pct_miss = 100 * merged[col].isna().mean()
            print(f"  {col}: {pct_miss:.1f}%")


def main():
    vdem, gravity = load_data()
    merged = merge_datasets(vdem, gravity)
    diagnostics(merged)

    # Save full merged dataset
    outpath_full = os.path.join(OUTPUT_DIR, "democracy_trade_merged_full.csv")
    merged.to_csv(outpath_full, index=False)
    print(f"\nSaved full dataset: {outpath_full}")

    # Save a smaller analytical dataset (only rows with both trade + democracy data)
    key_cols_needed = ["trade_flow", "v2x_polyarchy_o", "v2x_polyarchy_d"]
    existing_key = [c for c in key_cols_needed if c in merged.columns]
    if existing_key:
        analytical = merged.dropna(subset=existing_key)
        outpath_analytical = os.path.join(OUTPUT_DIR, "democracy_trade_analytical.csv")
        analytical.to_csv(outpath_analytical, index=False)
        print(f"Saved analytical subset: {outpath_analytical}")
        print(f"  Shape: {analytical.shape}")

    return merged


if __name__ == "__main__":
    main()
