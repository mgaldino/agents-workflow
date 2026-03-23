"""
generate_sample_data.py
Generate realistic sample/mock data files to demonstrate the expected output
format of the V-Dem and CEPII Gravity datasets and their merge.

This script can be run standalone to produce sample CSVs without needing
to download the real data.
"""

import os
import csv
import random
import itertools

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Seed for reproducibility
random.seed(42)

# Sample countries (mix of democracies, autocracies, various regions)
COUNTRIES = [
    ("USA", "United States", 0.87, 0.80, 21427700, 331003),
    ("GBR", "United Kingdom", 0.87, 0.82, 2827100, 67886),
    ("DEU", "Germany", 0.89, 0.84, 3845600, 83784),
    ("FRA", "France", 0.86, 0.80, 2715500, 65274),
    ("BRA", "Brazil", 0.73, 0.58, 1839800, 212559),
    ("IND", "India", 0.57, 0.38, 2868900, 1380004),
    ("CHN", "China", 0.06, 0.03, 14722800, 1439324),
    ("RUS", "Russia", 0.28, 0.10, 1483500, 145934),
    ("ZAF", "South Africa", 0.72, 0.60, 351400, 59309),
    ("MEX", "Mexico", 0.63, 0.42, 1268900, 128933),
    ("JPN", "Japan", 0.82, 0.74, 5081800, 126476),
    ("KOR", "Korea, Republic of", 0.80, 0.72, 1642400, 51269),
    ("NGA", "Nigeria", 0.42, 0.25, 448100, 206140),
    ("SAU", "Saudi Arabia", 0.02, 0.01, 792967, 34814),
    ("ARG", "Argentina", 0.73, 0.55, 449663, 45196),
    ("TUR", "Turkey", 0.35, 0.16, 761425, 84339),
    ("IDN", "Indonesia", 0.56, 0.40, 1119190, 273524),
    ("EGY", "Egypt", 0.18, 0.07, 303175, 102334),
    ("POL", "Poland", 0.78, 0.65, 592164, 37847),
    ("CHL", "Chile", 0.83, 0.74, 282318, 19116),
]

# Distance matrix (approximate, in km)
DISTANCES = {
    ("USA", "GBR"): 5570, ("USA", "DEU"): 6330, ("USA", "FRA"): 5840,
    ("USA", "BRA"): 6820, ("USA", "IND"): 13400, ("USA", "CHN"): 10960,
    ("USA", "RUS"): 7520, ("USA", "ZAF"): 12560, ("USA", "MEX"): 1960,
    ("USA", "JPN"): 10840, ("USA", "KOR"): 10960, ("USA", "NGA"): 8440,
    ("USA", "SAU"): 10680, ("USA", "ARG"): 8530, ("USA", "TUR"): 8530,
    ("GBR", "DEU"): 930, ("GBR", "FRA"): 340, ("GBR", "BRA"): 8470,
    ("GBR", "CHN"): 7780, ("BRA", "ARG"): 1970, ("DEU", "FRA"): 450,
    ("DEU", "POL"): 520, ("CHN", "JPN"): 2100, ("CHN", "KOR"): 960,
    ("CHN", "IND"): 2980, ("JPN", "KOR"): 1160, ("IND", "SAU"): 3050,
}

YEARS = list(range(1990, 2021))
SAMPLE_YEARS = [1990, 1995, 2000, 2005, 2010, 2015, 2020]


def add_noise(val, std=0.03, lower=0, upper=1):
    """Add Gaussian noise, clipped to [lower, upper]."""
    return max(lower, min(upper, val + random.gauss(0, std)))


def get_distance(iso_a, iso_b):
    """Get distance or generate a plausible one."""
    if (iso_a, iso_b) in DISTANCES:
        return DISTANCES[(iso_a, iso_b)]
    if (iso_b, iso_a) in DISTANCES:
        return DISTANCES[(iso_b, iso_a)]
    return random.randint(2000, 18000)


def generate_vdem_sample():
    """Generate sample V-Dem data: country-year panel."""
    rows = []
    for iso3, name, polyarchy_2020, libdem_2020, _, _ in COUNTRIES:
        for year in YEARS:
            # Simulate gradual democratization or backsliding
            year_offset = (year - 2020) / 100
            poly = add_noise(polyarchy_2020 + year_offset * random.uniform(-0.5, 0.3))
            lib = add_noise(libdem_2020 + year_offset * random.uniform(-0.5, 0.3))
            partip = add_noise(poly * 0.85 + random.gauss(0, 0.05))
            delib = add_noise(poly * 0.80 + random.gauss(0, 0.06))
            egal = add_noise(poly * 0.75 + random.gauss(0, 0.07))

            rows.append({
                "country_name": name,
                "iso3": iso3,
                "year": year,
                "v2x_polyarchy": round(poly, 3),
                "v2x_libdem": round(lib, 3),
                "v2x_partipdem": round(partip, 3),
                "v2x_delibdem": round(delib, 3),
                "v2x_egaldem": round(egal, 3),
                "v2x_freexp_altinf": round(add_noise(poly * 0.9), 3),
                "v2x_frassoc_thick": round(add_noise(poly * 0.88), 3),
                "v2x_suffr": round(min(1.0, poly + 0.15 + random.gauss(0, 0.02)), 3),
                "v2xel_frefair": round(add_noise(poly * 0.92), 3),
                "v2x_liberal": round(add_noise(lib * 1.05), 3),
                "v2xcl_rol": round(add_noise(lib * 0.95), 3),
                "v2x_jucon": round(add_noise(lib * 0.90), 3),
                "v2xlg_legcon": round(add_noise(lib * 0.88), 3),
            })

    outpath = os.path.join(OUTPUT_DIR, "vdem_democracy_1990_2020.csv")
    fieldnames = list(rows[0].keys())
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated V-Dem sample: {outpath}")
    print(f"  {len(rows)} rows, {len(COUNTRIES)} countries, {len(YEARS)} years")
    return rows


def generate_gravity_sample():
    """Generate sample CEPII Gravity data: dyad-year panel."""
    rows = []
    country_data = {c[0]: c for c in COUNTRIES}

    # Generate for all directed pairs, sample years only (to keep size manageable)
    for (iso_o, iso_d) in itertools.permutations([c[0] for c in COUNTRIES], 2):
        for year in SAMPLE_YEARS:
            c_o = country_data[iso_o]
            c_d = country_data[iso_d]

            dist = get_distance(iso_o, iso_d)

            # Simulate trade using a rough gravity model: proportional to GDP,
            # inversely proportional to distance
            gdp_o = c_o[4] * (0.6 + 0.4 * (year - 1990) / 30) * random.uniform(0.85, 1.15)
            gdp_d = c_d[4] * (0.6 + 0.4 * (year - 1990) / 30) * random.uniform(0.85, 1.15)

            # Gravity equation: T_ij ~ GDP_i * GDP_j / dist_ij^1.1
            base_trade = (gdp_o * gdp_d) / (dist ** 1.1) * 0.00001
            trade_flow = max(0, base_trade * random.uniform(0.3, 3.0))

            # Contiguity
            contig = 1 if dist < 500 else 0

            # Common language (simplified)
            english_speakers = {"USA", "GBR", "ZAF", "NGA", "IND"}
            spanish_speakers = {"MEX", "ARG", "CHL"}
            comlang = 1 if (
                (iso_o in english_speakers and iso_d in english_speakers)
                or (iso_o in spanish_speakers and iso_d in spanish_speakers)
            ) else 0

            # Colony
            colony_pairs = {("GBR", "USA"), ("GBR", "IND"), ("GBR", "ZAF"),
                           ("GBR", "NGA"), ("FRA", "EGY"), ("USA", "GBR")}
            colony = 1 if (iso_o, iso_d) in colony_pairs or (iso_d, iso_o) in colony_pairs else 0

            # RTA (simplified)
            eu = {"DEU", "FRA", "GBR", "POL"}  # GBR pre-Brexit for most of period
            rta = 1 if (iso_o in eu and iso_d in eu) else 0

            pop_o = c_o[5] * (0.85 + 0.15 * (year - 1990) / 30) * 1000
            pop_d = c_d[5] * (0.85 + 0.15 * (year - 1990) / 30) * 1000

            rows.append({
                "iso3_o": iso_o,
                "iso3_d": iso_d,
                "year": year,
                "tradeflow_baci": round(trade_flow, 2),
                "tradeflow_comtrade_o": round(trade_flow * random.uniform(0.9, 1.1), 2),
                "tradeflow_comtrade_d": round(trade_flow * random.uniform(0.9, 1.1), 2),
                "trade_flow": round(trade_flow, 2),
                "distw": round(dist * random.uniform(0.95, 1.05), 1),
                "dist": dist,
                "contig": contig,
                "comlang_off": comlang,
                "comlang_ethno": comlang,
                "colony": colony,
                "comcol": 0,
                "rta": rta,
                "gdp_o": round(gdp_o, 2),
                "gdp_d": round(gdp_d, 2),
                "gdpcap_o": round(gdp_o * 1e6 / pop_o, 2) if pop_o > 0 else None,
                "gdpcap_d": round(gdp_d * 1e6 / pop_d, 2) if pop_d > 0 else None,
                "pop_o": round(pop_o),
                "pop_d": round(pop_d),
                "landlocked_o": 0,
                "landlocked_d": 0,
            })

    outpath = os.path.join(OUTPUT_DIR, "cepii_gravity_1990_2020.csv")
    fieldnames = list(rows[0].keys())
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated Gravity sample: {outpath}")
    print(f"  {len(rows)} rows, {len(COUNTRIES)} countries, {len(SAMPLE_YEARS)} years")
    return rows


def generate_merged_sample():
    """Generate the merged dataset by combining sample V-Dem + Gravity."""
    # Read back the generated files
    vdem_path = os.path.join(OUTPUT_DIR, "vdem_democracy_1990_2020.csv")
    gravity_path = os.path.join(OUTPUT_DIR, "cepii_gravity_1990_2020.csv")

    # Read V-Dem
    vdem_rows = {}
    with open(vdem_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["iso3"], int(row["year"]))
            vdem_rows[key] = row

    # Read Gravity
    with open(gravity_path, "r") as f:
        reader = csv.DictReader(f)
        gravity_rows = list(reader)
        gravity_fields = reader.fieldnames

    # Democracy columns to merge
    demo_cols = [c for c in list(vdem_rows.values())[0].keys()
                 if c.startswith("v2x_") or c.startswith("v2xcl_")
                 or c.startswith("v2xel_") or c.startswith("v2xlg_")]

    # Merge
    merged_rows = []
    for grow in gravity_rows:
        merged = dict(grow)
        year = int(grow["year"])

        # Origin democracy
        key_o = (grow["iso3_o"], year)
        if key_o in vdem_rows:
            for col in demo_cols:
                merged[f"{col}_o"] = vdem_rows[key_o].get(col, "")
        else:
            for col in demo_cols:
                merged[f"{col}_o"] = ""

        # Destination democracy
        key_d = (grow["iso3_d"], year)
        if key_d in vdem_rows:
            for col in demo_cols:
                merged[f"{col}_d"] = vdem_rows[key_d].get(col, "")
        else:
            for col in demo_cols:
                merged[f"{col}_d"] = ""

        # Derived variables
        try:
            poly_o = float(merged.get("v2x_polyarchy_o", ""))
            poly_d = float(merged.get("v2x_polyarchy_d", ""))
            merged["democracy_diff_polyarchy"] = round(abs(poly_o - poly_d), 3)
            merged["democracy_avg_polyarchy"] = round((poly_o + poly_d) / 2, 3)
            merged["democracy_min_polyarchy"] = round(min(poly_o, poly_d), 3)
            merged["both_democratic"] = 1 if poly_o >= 0.5 and poly_d >= 0.5 else 0
        except (ValueError, TypeError):
            merged["democracy_diff_polyarchy"] = ""
            merged["democracy_avg_polyarchy"] = ""
            merged["democracy_min_polyarchy"] = ""
            merged["both_democratic"] = ""

        try:
            lib_o = float(merged.get("v2x_libdem_o", ""))
            lib_d = float(merged.get("v2x_libdem_d", ""))
            merged["democracy_diff_libdem"] = round(abs(lib_o - lib_d), 3)
        except (ValueError, TypeError):
            merged["democracy_diff_libdem"] = ""

        merged_rows.append(merged)

    # Determine field names
    merged_fields = list(gravity_fields)
    for col in demo_cols:
        merged_fields.append(f"{col}_o")
    for col in demo_cols:
        merged_fields.append(f"{col}_d")
    merged_fields.extend([
        "democracy_diff_polyarchy", "democracy_avg_polyarchy",
        "democracy_min_polyarchy", "both_democratic", "democracy_diff_libdem"
    ])

    # Save full merged
    outpath = os.path.join(OUTPUT_DIR, "democracy_trade_merged_full.csv")
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=merged_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged_rows)

    print(f"Generated merged dataset: {outpath}")
    print(f"  {len(merged_rows)} rows")

    # Save analytical subset (rows with complete trade + democracy data)
    analytical = [r for r in merged_rows
                  if r.get("trade_flow", "") and r.get("v2x_polyarchy_o", "")
                  and r.get("v2x_polyarchy_d", "")]
    outpath_analytical = os.path.join(OUTPUT_DIR, "democracy_trade_analytical.csv")
    with open(outpath_analytical, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=merged_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(analytical)

    print(f"Generated analytical subset: {outpath_analytical}")
    print(f"  {len(analytical)} rows")


if __name__ == "__main__":
    generate_vdem_sample()
    generate_gravity_sample()
    generate_merged_sample()
    print("\nAll sample data generated successfully.")
