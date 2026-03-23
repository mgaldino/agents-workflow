# Data Dictionary

## Dados brutos (raw/)

### vdem_v14_cy_YYYYMMDD.csv

Dados de indices de democracia do V-Dem v14, filtrados para 1990-2020.

| Variavel | Tipo | Descricao | Fonte (id) | Unidade | Valores validos |
|----------|------|-----------|------------|---------|-----------------|
| country_name | str | Nome do pais | vdem_v14 | - | texto |
| country_text_id | str | Codigo ISO 3166-1 alpha-3 | vdem_v14 | - | 3 letras |
| year | int | Ano de referencia | vdem_v14 | - | 1990-2020 |
| v2x_polyarchy | float | Electoral Democracy Index | vdem_v14 | indice 0-1 | [0, 1] |
| v2x_libdem | float | Liberal Democracy Index | vdem_v14 | indice 0-1 | [0, 1] |
| v2x_partipdem | float | Participatory Democracy Index | vdem_v14 | indice 0-1 | [0, 1] |
| v2x_delibdem | float | Deliberative Democracy Index | vdem_v14 | indice 0-1 | [0, 1] |
| v2x_egaldem | float | Egalitarian Democracy Index | vdem_v14 | indice 0-1 | [0, 1] |
| e_regionpol | int | Regiao politica (codificacao V-Dem) | vdem_v14 | categoria | 1-10 |
| e_regiongeo | int | Regiao geografica (codificacao V-Dem) | vdem_v14 | categoria | 1-19 |

### cepii_gravity_YYYYMMDD.csv

Dados de comercio bilateral e variaveis gravitacionais do CEPII, filtrados para 1990-2020.

| Variavel | Tipo | Descricao | Fonte (id) | Unidade | Valores validos |
|----------|------|-----------|------------|---------|-----------------|
| year | int | Ano de referencia | cepii_gravity | - | 1990-2020 |
| iso3_o | str | Codigo ISO3 do pais de origem | cepii_gravity | - | 3 letras |
| iso3_d | str | Codigo ISO3 do pais de destino | cepii_gravity | - | 3 letras |
| country_id_o | int | ID numerico do pais de origem | cepii_gravity | - | inteiro |
| country_id_d | int | ID numerico do pais de destino | cepii_gravity | - | inteiro |
| tradeflow_comtrade_o | float | Exportacoes (reporter=origem) | cepii_gravity | USD correntes | >= 0 |
| tradeflow_comtrade_d | float | Importacoes (reporter=destino) | cepii_gravity | USD correntes | >= 0 |
| tradeflow_baci | float | Fluxo comercial bilateral (BACI) | cepii_gravity | USD correntes | >= 0 |
| distw | float | Distancia ponderada pela populacao | cepii_gravity | km | > 0 |
| contig | int | Contiguidade (fronteira comum) | cepii_gravity | dummy | 0 ou 1 |
| comlang_off | int | Lingua oficial comum | cepii_gravity | dummy | 0 ou 1 |
| colony | int | Relacao colonial historica | cepii_gravity | dummy | 0 ou 1 |
| comcol | int | Colonizador comum | cepii_gravity | dummy | 0 ou 1 |
| gdp_o | float | PIB do pais de origem | cepii_gravity | USD correntes | > 0 |
| gdp_d | float | PIB do pais de destino | cepii_gravity | USD correntes | > 0 |
| pop_o | float | Populacao do pais de origem | cepii_gravity | milhares | > 0 |
| pop_d | float | Populacao do pais de destino | cepii_gravity | milhares | > 0 |
| gatt_o | int | Membro do GATT/WTO (origem) | cepii_gravity | dummy | 0 ou 1 |
| gatt_d | int | Membro do GATT/WTO (destino) | cepii_gravity | dummy | 0 ou 1 |
| rta | int | Acordo comercial regional | cepii_gravity | dummy | 0 ou 1 |

## Dados processados (processed/)

### democracy_trade_panel.csv

Painel bilateral pais_origem-pais_destino-ano com variaveis de comercio e democracia.
Gerado pelo merge de V-Dem com CEPII Gravity via codigos ISO3.

| Variavel | Tipo | Descricao | Fonte (id) | Unidade | Valores validos |
|----------|------|-----------|------------|---------|-----------------|
| year | int | Ano de referencia | - | - | 1990-2020 |
| iso3_o | str | Codigo ISO3 do pais de origem | cepii_gravity | - | 3 letras |
| iso3_d | str | Codigo ISO3 do pais de destino | cepii_gravity | - | 3 letras |
| trade_flow | float | Fluxo comercial bilateral (BACI preferido, Comtrade fallback) | cepii_gravity | USD correntes | >= 0 |
| ln_trade | float | Log natural do fluxo comercial | derivado | log(USD) | >= 0 |
| distw | float | Distancia ponderada pela populacao | cepii_gravity | km | > 0 |
| ln_distw | float | Log natural da distancia | derivado | log(km) | > 0 |
| contig | int | Contiguidade (fronteira comum) | cepii_gravity | dummy | 0 ou 1 |
| comlang_off | int | Lingua oficial comum | cepii_gravity | dummy | 0 ou 1 |
| colony | int | Relacao colonial historica | cepii_gravity | dummy | 0 ou 1 |
| comcol | int | Colonizador comum | cepii_gravity | dummy | 0 ou 1 |
| gdp_o | float | PIB do pais de origem | cepii_gravity | USD correntes | > 0 |
| gdp_d | float | PIB do pais de destino | cepii_gravity | USD correntes | > 0 |
| pop_o | float | Populacao do pais de origem | cepii_gravity | milhares | > 0 |
| pop_d | float | Populacao do pais de destino | cepii_gravity | milhares | > 0 |
| gatt_o | int | Membro do GATT/WTO (origem) | cepii_gravity | dummy | 0 ou 1 |
| gatt_d | int | Membro do GATT/WTO (destino) | cepii_gravity | dummy | 0 ou 1 |
| rta | int | Acordo comercial regional | cepii_gravity | dummy | 0 ou 1 |
| polyarchy_o | float | Electoral Democracy Index (origem) | vdem_v14 | indice 0-1 | [0, 1] |
| libdem_o | float | Liberal Democracy Index (origem) | vdem_v14 | indice 0-1 | [0, 1] |
| partipdem_o | float | Participatory Democracy Index (origem) | vdem_v14 | indice 0-1 | [0, 1] |
| delibdem_o | float | Deliberative Democracy Index (origem) | vdem_v14 | indice 0-1 | [0, 1] |
| egaldem_o | float | Egalitarian Democracy Index (origem) | vdem_v14 | indice 0-1 | [0, 1] |
| polyarchy_d | float | Electoral Democracy Index (destino) | vdem_v14 | indice 0-1 | [0, 1] |
| libdem_d | float | Liberal Democracy Index (destino) | vdem_v14 | indice 0-1 | [0, 1] |
| partipdem_d | float | Participatory Democracy Index (destino) | vdem_v14 | indice 0-1 | [0, 1] |
| delibdem_d | float | Deliberative Democracy Index (destino) | vdem_v14 | indice 0-1 | [0, 1] |
| egaldem_d | float | Egalitarian Democracy Index (destino) | vdem_v14 | indice 0-1 | [0, 1] |
| both_democratic | float | Ambos os paises democraticos (polyarchy >= 0.5) | derivado | dummy | 0 ou 1 |
| polyarchy_diff | float | Diferenca absoluta entre polyarchy_o e polyarchy_d | derivado | indice 0-1 | [0, 1] |
| polyarchy_min | float | Menor polyarchy entre o par | derivado | indice 0-1 | [0, 1] |
| polyarchy_max | float | Maior polyarchy entre o par | derivado | indice 0-1 | [0, 1] |
| polyarchy_product | float | Produto de polyarchy_o * polyarchy_d | derivado | indice 0-1 | [0, 1] |

### Notas sobre o merge

- **Chave de merge**: ISO3 alpha-3 + year (V-Dem usa `country_text_id`, Gravity usa `iso3_o`/`iso3_d`)
- **Tipo de merge**: left join (Gravity como base, V-Dem adicionado)
- **Cobertura**: Nem todos os paises/territorios no CEPII tem correspondente no V-Dem (ex: territorios dependentes). Valores missing indicam ausencia no V-Dem.
- **Variaveis derivadas**: Calculadas apos o merge para facilitar analises comuns na literatura de democratic peace e comercio.
