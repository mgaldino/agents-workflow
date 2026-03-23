# Data Dictionary -- OECD Trade Tariffs (2000-2010)

## oecd_tariffs_panel.csv

Dataset principal processado: painel de tarifas comerciais de paises da OCDE, 2000-2010.

| Variavel | Tipo | Descricao | Fonte (id) | Unidade | Valores validos |
|----------|------|-----------|------------|---------|-----------------|
| country_code | str | Codigo ISO 3166-1 alpha-3 do pais | - | - | 3 letras (ex: USA, DEU, JPN) |
| country_name | str | Nome do pais em ingles | - | - | texto |
| year | int | Ano de referencia | - | - | 2000-2010 |
| mfn_simple_avg | float | Media simples da tarifa MFN aplicada (todos os produtos) | wits_trains | percentual ad valorem | >= 0 |
| mfn_weighted_avg | float | Media ponderada pelo comercio da tarifa MFN aplicada | wits_trains | percentual ad valorem | >= 0 |
| bound_simple_avg | float | Media simples da tarifa consolidada (bound) | wto_tariff_profiles | percentual ad valorem | >= 0 |
| binding_coverage | float | Percentual das linhas tarifarias com consolidacao | wto_tariff_profiles | percentual (0-100) | 0-100 |
| total_tariff_lines | int | Numero total de linhas tarifarias | wits_trains | contagem | > 0 |
| dutiable_lines_pct | float | Percentual de linhas tarifarias com imposto > 0 | wits_trains | percentual (0-100) | 0-100 |
| ag_mfn_simple_avg | float | Media simples MFN para produtos agricolas | wits_trains | percentual ad valorem | >= 0 |
| nonag_mfn_simple_avg | float | Media simples MFN para produtos nao-agricolas | wits_trains | percentual ad valorem | >= 0 |
| oecd_tariff_indicator | float | Indicador agregado de politica tarifaria OCDE | oecd_tariffs | indice | varia |

## Notas

- **MFN (Most Favoured Nation)**: tarifa aplicada de forma nao-discriminatoria a todos os parceiros comerciais membros da OMC.
- **Bound tariff**: tarifa maxima que um pais se comprometeu a nao exceder nas negociacoes da OMC.
- **Ad valorem**: tarifa expressa como percentual do valor do produto importado.
- Dados agricolas seguem a definicao do Acordo sobre Agricultura da OMC (Anexo 1).
- Dados nao-agricolas excluem petroleo (HS 27) em algumas fontes.
- A media ponderada usa o comercio bilateral como peso, o que pode subestimar tarifas em produtos com comercio reduzido (tariff suppression effect).
