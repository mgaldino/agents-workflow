# Transcript: Democracy and International Trade Data Collection

## Task
Collect data from V-Dem (democracy indices) and CEPII Gravity (bilateral trade flows) for research on the relationship between democracy and international trade, with global coverage for 1990-2020.

## Data Sources

### Source 1: V-Dem (Varieties of Democracy)
- **URL**: https://v-dem.net/
- **Dataset**: V-Dem Country-Year Full+Others (v14)
- **Download URL**: https://v-dem.net/documents/24/V-Dem-CY-Full+Others-v14.csv.zip
- **Structure**: Country-year panel (one row per country per year)
- **Coverage**: ~202 countries, 1789-present (filtered to 1990-2020)
- **Key variables selected**:
  - `v2x_polyarchy`: Electoral Democracy Index (0-1)
  - `v2x_libdem`: Liberal Democracy Index (0-1)
  - `v2x_partipdem`: Participatory Democracy Index (0-1)
  - `v2x_delibdem`: Deliberative Democracy Index (0-1)
  - `v2x_egaldem`: Egalitarian Democracy Index (0-1)
  - Plus component indices for robustness checks

### Source 2: CEPII Gravity
- **URL**: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8
- **Dataset**: Gravity_csv_V202211
- **Download URL**: http://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip
- **Structure**: Dyad-year panel (one row per directed country-pair per year)
- **Coverage**: ~200 countries, 1948-2019 (extended to 2020 in some versions)
- **Key variables selected**:
  - Trade flows: `tradeflow_baci`, `tradeflow_comtrade_o/d`, `tradeflow_imf_o/d`
  - Distance: `distw`, `dist`
  - Gravity controls: `contig`, `comlang_off`, `colony`, `comcol`, `rta`
  - Economic: `gdp_o/d`, `gdpcap_o/d`, `pop_o/d`

## Steps Taken

### Step 1: Created download script for V-Dem (`01_download_vdem.py`)
- Downloads the V-Dem Country-Year CSV from the official V-Dem website
- Extracts democracy indices and identifiers
- Filters to 1990-2020
- Renames `country_text_id` to `iso3` for easier merging
- Saves as `vdem_democracy_1990_2020.csv`

### Step 2: Created download script for CEPII Gravity (`02_download_cepii_gravity.py`)
- Downloads the CEPII Gravity CSV from the official CEPII data portal
- Extracts trade flows, distance, cultural/geographic, and economic variables
- Creates unified `trade_flow` variable (preferring BACI, then Comtrade, then IMF)
- Filters to 1990-2020
- Saves as `cepii_gravity_1990_2020.csv`

### Step 3: Created merge script (`03_merge_democracy_trade.py`)
- **Merge strategy**: V-Dem is country-year; CEPII Gravity is dyad-year. V-Dem is merged into Gravity TWICE:
  - Once matching `iso3_o` + `year` (origin country democracy)
  - Once matching `iso3_d` + `year` (destination country democracy)
- Handles ISO3 code mismatches between datasets (e.g., Palestine: PSG vs PSE)
- Creates derived variables:
  - `democracy_diff_polyarchy`: |polyarchy_o - polyarchy_d|
  - `democracy_avg_polyarchy`: mean of pair
  - `democracy_min_polyarchy`: weakest-link measure
  - `both_democratic`: binary indicator (both >= 0.5)
  - `democracy_diff_libdem`: liberal democracy difference
- Outputs full merged dataset and analytical subset (complete cases only)
- Prints merge diagnostics (match rates, unmatched countries, missing data)

### Step 4: Created sample data generator (`generate_sample_data.py`)
- Generates realistic mock data for 20 countries across all years
- Simulates V-Dem scores with appropriate ranges per country type
- Simulates CEPII Gravity trade flows using rough gravity equation
- Performs the merge to create sample merged output

### Step 5: Created sample data files
Since HTTP requests cannot be made, hand-crafted sample CSV files demonstrating expected formats:
- `vdem_democracy_1990_2020.csv`: 20 countries x 7 years = 140 rows
- `cepii_gravity_1990_2020.csv`: Selected country pairs x 3 years = 84 rows
- `democracy_trade_merged_full.csv`: 73 rows of merged dyad-year data
- `democracy_trade_analytical.csv`: Subset of 21 representative rows

### Step 6: Created data dictionary (`data_dictionary.csv`)
- Documents every variable in the merged dataset
- Includes source, type, range, and descriptions

## Output Files

| File | Description |
|------|-------------|
| `01_download_vdem.py` | Python script to download and process V-Dem data |
| `02_download_cepii_gravity.py` | Python script to download and process CEPII Gravity data |
| `03_merge_democracy_trade.py` | Python script to merge V-Dem into Gravity (origin + destination) |
| `generate_sample_data.py` | Script to generate sample/mock data demonstrating expected formats |
| `vdem_democracy_1990_2020.csv` | Sample V-Dem data (20 countries, 1990-2020) |
| `cepii_gravity_1990_2020.csv` | Sample CEPII Gravity data (selected dyads, 2000/2010/2020) |
| `democracy_trade_merged_full.csv` | Sample merged dataset (73 dyad-year observations) |
| `democracy_trade_analytical.csv` | Sample analytical subset (21 complete observations) |
| `data_dictionary.csv` | Data dictionary for all variables |
| `requirements.txt` | Python dependencies |

## Merge Key Details

- **Join key**: ISO 3166-1 alpha-3 country code + year
- **V-Dem field**: `country_text_id` (renamed to `iso3`)
- **CEPII fields**: `iso3_o` (origin) and `iso3_d` (destination)
- **Known ISO3 mismatches**: Palestine (PSG/PSE), Somaliland (SML/SOM), Kosovo (XKX/KOS)
- **Expected match rate**: ~95%+ for major trading nations; small territories/dependencies may not match

## Notes for Real Execution

1. The CEPII Gravity download URL may change with new data releases. Check the CEPII website for the latest version.
2. V-Dem version 14 is current as of 2024. Check https://v-dem.net for updates.
3. The full merged dataset (all country pairs, all years) will be very large (~2-4 million rows). Consider using `chunksize` in pandas or filtering to specific country sets if memory is a concern.
4. The CEPII Gravity dataset's temporal coverage may not fully extend to 2020 in all versions. The most recent version (V202211) covers up to 2019. For 2020, supplementary trade data from UN Comtrade or BACI may be needed.
5. Run scripts in order: `01_download_vdem.py` -> `02_download_cepii_gravity.py` -> `03_merge_democracy_trade.py`
