# Transcript: OECD Trade Tariff Data Search (2000-2010)

## Task
Find data on commercial tariffs for OECD countries in the 2000-2010 period, checking Harvard Dataverse and other academic databases.

## Steps Taken

### Step 1: Web Search -- Harvard Dataverse
Searched for "Harvard Dataverse OECD trade tariffs data 2000-2010".

**Findings:**
- Harvard Dataverse does NOT have a single, canonical OECD tariff panel dataset for 2000-2010.
- The Atlas of Economic Complexity (Harvard Growth Lab) is hosted on Dataverse but focuses on trade flows, not tariffs.
- Found several replication packages from academic papers that contain tariff-related data, but none is a ready-to-use OECD tariff panel.

### Step 2: Web Search -- OECD and Academic Databases
Searched for "OECD commercial tariffs dataset academic download 2000 2010".

**Findings:**
- OECD Data Explorer (data-explorer.oecd.org) has trade data, became Open Access in July 2024.
- WTO Tariff and Trade Data (TTD) portal covers 170+ economies from 1996 onwards.
- World Bank WITS / UNCTAD TRAINS is the most comprehensive tariff database.

### Step 3: Web Search -- WITS/TRAINS
Searched for "World Bank TRAINS WITS tariff data OECD countries download".

**Findings:**
- WITS (wits.worldbank.org) aggregates data from UNCTAD TRAINS and other sources.
- UNCTAD TRAINS provides MFN applied and preferential tariffs at HS 6-digit level since 1988.
- Free access, but registration required for the web interface.
- API available at wits.worldbank.org/API/V1/.
- Python package `world_trade_data` wraps the WITS API.

### Step 4: Web Search -- Harvard Dataverse Replication Datasets
Searched for "Harvard Dataverse tariff trade protection dataset replication".

**Findings -- specific datasets:**
1. "Tariff Passthrough at the Border and at the Store" (DOI: 10.7910/DVN/JV7FCH)
2. "Trade Policy and Global Sourcing: A Rationale for Tariff Escalation" (DOI: 10.7910/DVN/10RLRZ)
3. "The Environmental Bias of Trade Policy" (DOI: 10.7910/DVN/CTUS2E)
4. "Economic Crises and Trade Policy Competition" (DOI: 10.7910/DVN/SVWMB5)
5. "Asset Specificity, Corporate Protection and Trade Policy" (DOI: 10.7910/DVN/1WZRY2)

These are replication packages, not standalone tariff databases.

### Step 5: Web Search -- WITS Python API
Searched for "WITS API bulk download tariff data Python script example".

**Findings:**
- `world_trade_data` Python package on GitHub (github.com/mwouts/world_trade_data)
- Key functions: `get_tariff_reported()`, `get_tariff_estimated()`, `get_indicator()`
- API has query size limits (max 2 "All" dimensions per query).
- SDMX-based API also available.

### Step 6: Web Search -- World Bank WDI API
Searched for "World Bank API indicator TM.TAX.MRCH.WM.AR.ZS download Python OECD countries".

**Findings:**
- WDI indicator TM.TAX.MRCH.WM.AR.ZS = "Tariff rate, applied, weighted mean, all products (%)"
- API is free, no authentication required.
- Endpoint: `https://api.worldbank.org/v2/country/{iso2}/indicator/{indicator}?date=2000:2010&format=json`
- Direct URL for OECD aggregate: data.worldbank.org/indicator/TM.TAX.MRCH.WM.AR.ZS?locations=OE
- Python libraries: `wbpy`, `wbdata`, or plain `requests`.

### Step 7: Web Search -- WTO TTD Download
Searched for "OECD tariff database MFN applied weighted mean 2000-2010 download CSV".

**Findings:**
- WTO TTD has a dedicated download page: ttd.wto.org/en/download
- World Bank Data Portal confirmed as best for country-year aggregate data.
- Our World in Data also provides the WDI tariff data with easy CSV downloads.

## Outputs Created

1. **README_data_sources.md** -- Comprehensive guide to all identified data sources, organized in three tiers (primary databases, Harvard Dataverse replication data, supplementary sources), with URLs, API details, and recommendations.

2. **download_wdi_tariffs.py** -- Python script to download aggregate tariff rates from World Bank WDI API for all 31 OECD countries, 2000-2010, for 4 tariff indicators. No authentication required.

3. **download_wits_tariffs.py** -- Python script to download product-level tariff data from WITS/TRAINS using the `world_trade_data` package. Covers estimated and reported tariffs.

4. **download_wto_tariffs.py** -- Python script for WTO TTD data, including manual download instructions (more reliable than API for this source).

5. **download_harvard_dataverse.py** -- Python script to search and download replication datasets from Harvard Dataverse using their REST API.

6. **download_tariffs.R** -- R script using the `WDI` package to download the same data (alternative for R users).

7. **sample_oecd_tariffs_wdi_2000_2010.csv** -- Mock/sample data file showing the expected output format from the WDI download script. Contains 9 countries x 11 years with 4 tariff indicators.

8. **codebook.md** -- Data documentation including variable definitions, WDI indicator codes, coverage notes, EU membership flags, and citation information.

## Key Recommendations

1. **Best single source for aggregate analysis**: World Bank WDI via API (`download_wdi_tariffs.py`). Easiest to access, covers all OECD countries, no registration needed.

2. **Best for product-level analysis**: WITS / UNCTAD TRAINS (`download_wits_tariffs.py`). HS6-level granularity, but requires iteration over countries/years due to API limits.

3. **Harvard Dataverse**: No standalone OECD tariff panel exists. Replication packages from specific papers may contain useful pre-processed data, but you would need to inspect each one for coverage.

4. **Important caveat for EU members**: 19 of the 31 OECD members (as of 2010) are EU members and share a Common External Tariff. For panel analysis, consider treating EU as a single entity to avoid pseudo-replication.
