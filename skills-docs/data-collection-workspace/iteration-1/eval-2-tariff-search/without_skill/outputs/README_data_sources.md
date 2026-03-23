# OECD Trade Tariff Data Sources (2000-2010)

## Summary

This document describes the best available sources for commercial tariff data
for OECD countries in the 2000-2010 period. Three tiers of sources are
recommended: primary databases (best for systematic downloads), Harvard
Dataverse replication datasets (useful for pre-processed academic data), and
supplementary portals.

---

## Tier 1: Primary Databases (Recommended)

### 1. World Bank - World Development Indicators (WDI)

- **Indicator**: `TM.TAX.MRCH.WM.AR.ZS` -- Tariff rate, applied, weighted mean, all products (%)
- **Coverage**: OECD countries, 2000-2010 (and beyond)
- **Access**: Free, no API key required
- **URL**: https://data.worldbank.org/indicator/TM.TAX.MRCH.WM.AR.ZS?locations=OE
- **API endpoint**: `https://api.worldbank.org/v2/country/{iso2}/indicator/TM.TAX.MRCH.WM.AR.ZS?date=2000:2010&format=json`
- **Why recommended**: Easiest to access programmatically. Provides aggregate
  weighted mean tariff for each country-year. Excellent for panel analysis.
- **Limitations**: Only aggregate (all products). For sector-level tariffs, use WITS.

Additional WDI tariff indicators:
- `TM.TAX.MRCH.SM.AR.ZS` -- Simple mean, all products
- `TM.TAX.MRCH.WM.FN.ZS` -- Weighted mean, manufactured products
- `TM.TAX.TCOM.WM.AR.ZS` -- Weighted mean, primary products
- `TM.TAX.MANF.WM.AR.ZS` -- Weighted mean, manufactured products

### 2. World Bank WITS / UNCTAD TRAINS

- **Coverage**: MFN applied and preferential tariffs at HS 6-digit level
- **Access**: Free (registration required for WITS website; API is open)
- **URL**: https://wits.worldbank.org/
- **API base**: `https://wits.worldbank.org/API/V1/`
- **Python package**: `world_trade_data` (pip install world_trade_data)
- **Why recommended**: Most granular tariff data available. Covers tariff lines
  at HS6 level for all OECD countries. Supports MFN, applied, and preferential rates.
- **Limitations**: API has query size limits (max 2 "All" dimensions per query).
  Bulk downloads require iteration over countries/years.

### 3. WTO Tariff and Trade Data (TTD)

- **Coverage**: Tariff profiles for 170+ economies, from 1996 onwards
- **Access**: Free
- **URL**: https://ttd.wto.org/en
- **Download**: https://ttd.wto.org/en/download
- **Why recommended**: Official WTO data. Includes MFN trade-weighted averages,
  bound rates, and duty-free shares by product group.
- **Limitations**: Less convenient for programmatic access than WDI API.

---

## Tier 2: Harvard Dataverse -- Replication Datasets

Harvard Dataverse does NOT have a single, canonical OECD tariff panel dataset.
However, several replication packages contain pre-processed tariff data that may
be useful:

### Relevant Datasets Found

1. **"Tariff Passthrough at the Border and at the Store"**
   - DOI: `10.7910/DVN/JV7FCH`
   - URL: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JV7FCH
   - Content: US tariff passthrough micro data (US-focused, may include OECD partner data)

2. **"Trade Policy and Global Sourcing: A Rationale for Tariff Escalation"**
   - DOI: `10.7910/DVN/10RLRZ`
   - URL: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/10RLRZ
   - Content: Tariff escalation data across countries

3. **"The Environmental Bias of Trade Policy"**
   - DOI: `10.7910/DVN/CTUS2E`
   - URL: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/CTUS2E
   - Content: Cross-country trade policy data including tariff measures

4. **"Economic Crises and Trade Policy Competition"**
   - DOI: `10.7910/DVN/SVWMB5`
   - URL: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SVWMB5
   - Content: Trade policy competition data across countries

5. **Atlas of Economic Complexity (Harvard Growth Lab)**
   - URL: https://dataverse.harvard.edu/dataverse/atlas
   - Download: https://atlas.hks.harvard.edu/data-downloads
   - Content: Trade flows (HS classification), not tariffs per se, but useful
     as a complement for trade volume weighting.

### Caveat on Harvard Dataverse

None of these datasets is a clean "OECD tariff panel 2000-2010" ready to use.
They are replication packages for specific papers. You would need to inspect
each one to see if the underlying tariff data covers your exact scope. For a
systematic, comprehensive dataset, the Tier 1 sources (WDI, WITS, WTO) are
far more appropriate.

---

## Tier 3: Supplementary Sources

### Our World in Data
- **URL**: https://ourworldindata.org/grapher/tariff-rate-applied-weighted-mean-all-products
- Uses World Bank WDI data underneath, but provides nice visualizations and
  easy CSV downloads.

### OECD Data Explorer
- **URL**: https://data-explorer.oecd.org/
- Trade in Goods and Services data. Some tariff-related indicators available.
- Content became Open Access in July 2024.

---

## Recommendation

For a research project needing OECD tariff data 2000-2010:

1. **Start with World Bank WDI** via API for aggregate country-year tariff rates.
   This gives you a clean panel with minimal effort (see `download_wdi_tariffs.py`).

2. **Use WITS/TRAINS** if you need product-level (HS6) tariff data
   (see `download_wits_tariffs.py`).

3. **Check Harvard Dataverse replication packages** if you need data that has
   already been cleaned and matched to specific economic outcomes for a
   particular study's methodology.

4. **Download WTO TTD data** for official bound rates and tariff profiles
   (see `download_wto_tariffs.py`).
