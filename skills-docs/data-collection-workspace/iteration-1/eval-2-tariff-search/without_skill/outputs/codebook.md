# Codebook: OECD Tariff Data 2000-2010

## File: oecd_tariffs_wdi_2000_2010.csv

### Source
World Bank World Development Indicators (WDI)
https://data.worldbank.org/

### Unit of observation
Country-year

### Coverage
- Countries: 31 OECD member countries (as of 2010)
- Years: 2000-2010

### Variables

| Variable | Type | Description |
|----------|------|-------------|
| `country_code` | string (ISO3) | ISO 3166-1 alpha-3 country code |
| `country_name` | string | Country name |
| `year` | integer | Calendar year |
| `tariff_weighted_mean_all_products` | float (%) | Tariff rate, applied, weighted mean, all products. The weighted mean applied tariff is the average of effectively applied rates weighted by the product import shares corresponding to each partner country. WDI indicator: TM.TAX.MRCH.WM.AR.ZS |
| `tariff_simple_mean_all_products` | float (%) | Tariff rate, applied, simple mean, all products. Simple mean tariff is the unweighted average of effectively applied rates for all products subject to tariffs. WDI indicator: TM.TAX.MRCH.SM.AR.ZS |
| `tariff_weighted_mean_manufactured` | float (%) | Tariff rate, applied, weighted mean, manufactured products. Manufactured products are commodity groups 5-8 of SITC revision 3. WDI indicator: TM.TAX.MRCH.WM.FN.ZS |
| `tariff_weighted_mean_primary` | float (%) | Tariff rate, applied, weighted mean, primary products. Primary products are commodity groups 0-4 and 68 of SITC revision 3. WDI indicator: TM.TAX.TCOM.WM.AR.ZS |

### Missing values
- Represented as empty cells (CSV) or NaN (pandas)
- Missing data is common for smaller economies and earlier years
- EU member states may report tariffs only at the EU level for certain years

### Notes on EU members
EU member states in the OECD share a Common External Tariff (CET). In the WDI
data, each EU member country has the same tariff rates because the EU applies
tariffs uniformly. The countries are:

Austria, Belgium, Czech Republic, Denmark, Finland, France, Germany, Greece,
Hungary, Ireland, Italy, Luxembourg, Netherlands, Poland, Portugal, Slovak
Republic, Spain, Sweden, United Kingdom.

For analysis where you want to avoid pseudo-replication, consider using
"European Union" as a single entity instead of individual EU members.

### OECD Members (ISO3 codes, as of 2010)

| ISO3 | Country | EU member (2010) |
|------|---------|------------------|
| AUS | Australia | No |
| AUT | Austria | Yes |
| BEL | Belgium | Yes |
| CAN | Canada | No |
| CHL | Chile | No |
| CZE | Czech Republic | Yes |
| DNK | Denmark | Yes |
| FIN | Finland | Yes |
| FRA | France | Yes |
| DEU | Germany | Yes |
| GRC | Greece | Yes |
| HUN | Hungary | Yes |
| ISL | Iceland | No |
| IRL | Ireland | Yes |
| ITA | Italy | Yes |
| JPN | Japan | No |
| KOR | Korea, Rep. | No |
| LUX | Luxembourg | Yes |
| MEX | Mexico | No |
| NLD | Netherlands | Yes |
| NZL | New Zealand | No |
| NOR | Norway | No |
| POL | Poland | Yes |
| PRT | Portugal | Yes |
| SVK | Slovak Republic | Yes |
| ESP | Spain | Yes |
| SWE | Sweden | Yes |
| CHE | Switzerland | No |
| TUR | Turkey | No |
| GBR | United Kingdom | Yes |
| USA | United States | No |

### Citation

World Bank. "World Development Indicators." Washington, D.C.: The World Bank.
https://data.worldbank.org/

Original source: World Trade Organization (WTO) and UNCTAD TRAINS database.
