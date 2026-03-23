# Dicionario de Dados

## painel_latam.csv

Painel pais-ano com PIB per capita e populacao para 20 paises da America Latina, 2000-2023.

| Variavel | Tipo | Descricao | Fonte (id) | Unidade | Valores validos |
|----------|------|-----------|------------|---------|-----------------|
| country_code | str | Codigo ISO 3166-1 alpha-3 do pais | - | - | 3 letras maiusculas (ex: BRA, ARG, MEX) |
| country_name | str | Nome do pais em ingles (conforme World Bank) | worldbank_wdi | - | texto |
| year | int | Ano de referencia | - | - | 2000-2023 |
| gdp_per_capita_current_usd | float | PIB per capita em dolares americanos correntes | worldbank_wdi | USD correntes | > 0 (pode ser NaN se dado indisponivel) |
| population_total | float | Populacao total estimada no meio do ano | worldbank_wdi | pessoas | > 0 (pode ser NaN se dado indisponivel) |

### Notas

- **PIB per capita (NY.GDP.PCAP.CD)**: Produto Interno Bruto dividido pela populacao de meio de ano. Dados em dolares americanos correntes. Nao ajustado por paridade de poder de compra (PPP). Para comparacoes reais ao longo do tempo, considere usar a serie em dolares constantes (NY.GDP.PCAP.KD).

- **Populacao (SP.POP.TOTL)**: Baseada na definicao de facto de populacao, contando todos os residentes independente de status legal ou cidadania. Valores sao estimativas de meio de ano.

- **Missing values**: Alguns paises podem ter dados faltantes em anos especificos, especialmente Venezuela (anos recentes) e Cuba. Esses aparecem como NaN no CSV.

### Paises cobertos

| Codigo | Pais |
|--------|------|
| ARG | Argentina |
| BOL | Bolivia |
| BRA | Brasil |
| CHL | Chile |
| COL | Colombia |
| CRI | Costa Rica |
| CUB | Cuba |
| DOM | Republica Dominicana |
| ECU | Equador |
| SLV | El Salvador |
| GTM | Guatemala |
| HTI | Haiti |
| HND | Honduras |
| MEX | Mexico |
| NIC | Nicaragua |
| PAN | Panama |
| PRY | Paraguai |
| PER | Peru |
| URY | Uruguai |
| VEN | Venezuela |
