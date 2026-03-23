# Transcript: Coleta de dados -- Democracia e Comercio Internacional

## Tarefa

O usuario solicitou dados para pesquisar a relacao entre democracia e comercio internacional, especificando:
- **Fonte 1**: V-Dem para indices de democracia
- **Fonte 2**: CEPII Gravity para fluxos de comercio bilateral
- **Cobertura**: global
- **Periodo**: 1990-2020

## Passo 1: Entender a necessidade (Skill workflow step 1)

Analisei os requisitos:
- **Pergunta de pesquisa**: Relacao entre democracia e comercio internacional
- **Unidade de analise**: par bilateral pais_origem-pais_destino-ano
- **Periodo temporal**: 1990-2020
- **Cobertura geografica**: global
- **Fontes ja especificadas**: V-Dem (democracia) e CEPII Gravity (comercio)

O usuario ja definiu as fontes, entao nao foi necessario descobrir fontes alternativas.

## Passo 2: Descobrir fontes (Skill workflow step 2)

As duas fontes solicitadas sao fontes primarias bem conhecidas na literatura:

### V-Dem (Varieties of Democracy) v14
- **URL**: https://www.v-dem.net/data/the-v-dem-dataset/
- **Acesso**: Bulk download (CSV/Stata), sem credencial
- **Licenca**: CC BY-SA 4.0
- **Variaveis relevantes**: v2x_polyarchy (Electoral Democracy), v2x_libdem (Liberal Democracy), v2x_partipdem (Participatory), v2x_delibdem (Deliberative), v2x_egaldem (Egalitarian)
- **Cobertura**: 202 paises, 1789-2023

### CEPII Gravity Dataset
- **URL**: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8
- **Acesso**: Bulk download, sem credencial obrigatoria (registro gratuito pode ser necessario)
- **Licenca**: Uso livre para pesquisa academica
- **Variaveis relevantes**: tradeflow_baci (fluxo bilateral), distw (distancia), contig, comlang_off, colony, comcol, rta, gdp, pop
- **Cobertura**: ~200 paises, pares bilaterais, 1948-2020

Ambas as fontes sao acessiveis por download direto, sem API keys.

## Passo 3: Configurar o projeto (Skill workflow step 3)

Criei a estrutura de diretorios conforme o padrao da skill:

```
outputs/
├── raw/                                   # Dados brutos (amostras)
│   ├── vdem_v14_cy_20260313_SAMPLE.csv
│   └── cepii_gravity_20260313_SAMPLE.csv
├── processed/                             # CSV processado (amostra)
│   └── democracy_trade_panel_SAMPLE.csv
├── scripts/
│   ├── download_vdem.py
│   ├── download_cepii_gravity.py
│   ├── process_merge.py
│   └── requirements.txt
├── docs/
│   ├── SOURCES.yaml
│   └── DATA_DICTIONARY.md
├── .env.example
├── .gitignore
├── checksums.sha256
└── README.md
```

## Passo 4: Gestao de credenciais (Skill workflow step 4)

Nenhuma das fontes exige credenciais obrigatorias. Criei `.env.example` com template vazio (preparado para expansao futura) e verifiquei que `.gitignore` exclui `.env`.

## Passo 5: Escrever scripts de download (Skill workflow step 5)

### download_vdem.py
- Baixa o V-Dem v14 Country-Year Full+Others (CSV zipado)
- Extrai do ZIP e filtra apenas variaveis de interesse e periodo 1990-2020
- Inclui retry com backoff exponencial e barra de progresso
- Salva com data no nome do arquivo para versionamento

### download_cepii_gravity.py
- Baixa o CEPII Gravity dataset (CSV zipado, ~800MB)
- Le em chunks de 100k linhas para gerenciar memoria
- Filtra periodo 1990-2020 durante a leitura
- Seleciona variaveis gravitacionais padrao + fluxos comerciais
- Inclui retry com backoff e barra de progresso

### process_merge.py
- Carrega ambos os datasets brutos
- Cria variavel consolidada de comercio (BACI preferido, Comtrade fallback)
- Faz merge bilateral via ISO3 + year:
  - Merge 1: Democracia do pais de ORIGEM (iso3_o)
  - Merge 2: Democracia do pais de DESTINO (iso3_d)
- Calcula variaveis derivadas: both_democratic, polyarchy_diff, polyarchy_min, polyarchy_max, polyarchy_product
- Gera logaritmos de trade e distancia (padrao em modelos gravitacionais)

## Passo 6: Documentar fontes -- SOURCES.yaml (Skill workflow step 6)

Criei entradas completas para ambas as fontes com todos os campos obrigatorios:
- id, name, provider, url, access_method, license, download_script, date_accessed
- Incluindo tambem: citation, variables_used, temporal_coverage, geographic_coverage, unit_of_analysis

## Passo 7: Documentar variaveis -- DATA_DICTIONARY.md (Skill workflow step 7)

Documentei tres tabelas:
1. **vdem_v14_cy_YYYYMMDD.csv**: 10 variaveis (raw)
2. **cepii_gravity_YYYYMMDD.csv**: 20 variaveis (raw)
3. **democracy_trade_panel.csv**: ~35 variaveis (processed, incluindo derivadas)

Cada variavel com: tipo, descricao, fonte (vinculada ao id em SOURCES.yaml), unidade, valores validos.

## Passo 8: Validar e gerar checksums (Skill workflow step 8)

Criei checksums.sha256 com instrucoes de como regenerar apos o download real. Como os dados sao amostras simuladas, os checksums sao placeholders com instrucoes.

## Passo 9: Gerar README.md (Skill workflow step 9)

Criei README completo com:
- Estrutura de diretorios
- Instrucoes de reproducao passo a passo
- Tabela resumo das fontes
- Descricao das variaveis principais
- Citacoes bibliograficas

## Passo 10: Dados de amostra (simulacao)

Como nao e possivel fazer HTTP requests reais neste ambiente, criei arquivos de amostra:

### vdem_v14_cy_20260313_SAMPLE.csv
- 8 paises (USA, BRA, DEU, CHN, JPN, IND, ZAF, RUS) x 7 periodos (1990-2020 em intervalos de 5 anos)
- 56 observacoes representativas com valores realistas

### cepii_gravity_20260313_SAMPLE.csv
- 31 pares bilaterais representativos (incluindo pares USA-CHN, BRA-CHN, DEU-CHN, etc.)
- Valores realistas de comercio, distancia e variaveis gravitacionais
- Cobre 1990, 2000, 2010, 2020

### democracy_trade_panel_SAMPLE.csv
- 15 observacoes mostrando o formato final apos merge
- Demonstra as variaveis derivadas (both_democratic, polyarchy_diff, etc.)
- Mostra como os indices de democracia aparecem para ambos os parceiros (o/d)

## Arquivos criados

Total de 13 arquivos:

| Arquivo | Descricao |
|---------|-----------|
| scripts/download_vdem.py | Script de download do V-Dem v14 |
| scripts/download_cepii_gravity.py | Script de download do CEPII Gravity |
| scripts/process_merge.py | Script de merge e processamento |
| scripts/requirements.txt | Dependencias Python |
| docs/SOURCES.yaml | Manifesto de fontes |
| docs/DATA_DICTIONARY.md | Dicionario de variaveis |
| .env.example | Template de credenciais |
| .gitignore | Exclusoes de versionamento |
| checksums.sha256 | Integridade dos arquivos |
| README.md | Instrucoes de reproducao |
| raw/vdem_v14_cy_20260313_SAMPLE.csv | Amostra V-Dem |
| raw/cepii_gravity_20260313_SAMPLE.csv | Amostra CEPII Gravity |
| processed/democracy_trade_panel_SAMPLE.csv | Amostra painel final |

## Decisoes de design

1. **Merge bilateral**: O V-Dem e no nivel pais-ano, mas o Gravity e bilateral (pais_o-pais_d-ano). O merge e feito duas vezes: uma para o pais de origem, outra para o de destino. Isso permite analisar como a democracia de AMBOS os parceiros afeta o comercio.

2. **Variaveis derivadas**: Inclui both_democratic, polyarchy_diff, polyarchy_product porque sao amplamente usadas na literatura sobre "democratic peace" e comercio (Mansfield, Milner & Rosendorff 2000; Yu 2010).

3. **Log de comercio e distancia**: Padrao em modelos gravitacionais. O script de processamento gera ln_trade e ln_distw automaticamente.

4. **Multiplos indices de democracia**: Inclui os 5 indices de alto nivel do V-Dem (nao apenas polyarchy) para permitir robustez com diferentes conceituacoes de democracia.

5. **BACI vs Comtrade**: O CEPII oferece duas medidas de comercio. Preferimos BACI (reconciliado) com fallback para Comtrade.
