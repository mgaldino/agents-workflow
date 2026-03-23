# Dados -- Democracia e Comercio Internacional

Coleta de dados para pesquisa sobre a relacao entre democracia e comercio internacional.
Combina indices de democracia (V-Dem) com fluxos de comercio bilateral (CEPII Gravity)
para construir um painel global no nivel pais_origem-pais_destino-ano, cobrindo 1990-2020.

## Estrutura do diretorio

```
data/
├── raw/                              # Dados brutos (nunca modificar)
│   ├── vdem_v14_cy_YYYYMMDD.csv      # V-Dem indices de democracia
│   └── cepii_gravity_YYYYMMDD.csv    # CEPII fluxos bilaterais
├── processed/                        # CSVs limpos
│   └── democracy_trade_panel.csv     # Painel final (merge V-Dem + Gravity)
├── scripts/
│   ├── download_vdem.py              # Download do V-Dem v14
│   ├── download_cepii_gravity.py     # Download do CEPII Gravity
│   ├── process_merge.py              # Merge e processamento
│   └── requirements.txt              # Dependencias Python
├── docs/
│   ├── SOURCES.yaml                  # Manifesto de fontes
│   └── DATA_DICTIONARY.md            # Dicionario de variaveis
├── .env.example                      # Template de credenciais
├── .gitignore                        # Exclui .env e arquivos grandes
├── checksums.sha256                  # Integridade dos arquivos
└── README.md                         # Este arquivo
```

## Como reproduzir a coleta

### Pre-requisitos

- Python 3.8+
- pip

### Passo a passo

1. Instalar dependencias:
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. Configurar credenciais (opcional -- nenhuma fonte atual exige):
   ```bash
   cp .env.example .env
   # Editar .env se necessario
   ```

3. Executar scripts na ordem:
   ```bash
   python scripts/download_vdem.py
   python scripts/download_cepii_gravity.py
   python scripts/process_merge.py
   ```

4. Verificar integridade:
   ```bash
   sha256sum -c checksums.sha256
   ```

### Notas sobre o download

- **V-Dem**: Download direto do site (~250MB compactado). Nenhuma credencial necessaria.
- **CEPII Gravity**: Download direto (~800MB compactado). Pode ser necessario registro
  gratuito no site do CEPII. Se o download automatico falhar, baixe manualmente de
  http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8 e coloque o CSV em `raw/`.

## Fontes

Ver detalhes completos em `docs/SOURCES.yaml`.

| Fonte | Acesso | Credencial? | Script |
|-------|--------|-------------|--------|
| V-Dem v14 (Country-Year) | Bulk download | Nao | download_vdem.py |
| CEPII Gravity | Bulk download | Nao | download_cepii_gravity.py |

## Variaveis principais

### Democracia (V-Dem)
- **v2x_polyarchy**: Electoral Democracy Index (0-1)
- **v2x_libdem**: Liberal Democracy Index (0-1)
- **v2x_partipdem**: Participatory Democracy Index (0-1)
- **v2x_delibdem**: Deliberative Democracy Index (0-1)
- **v2x_egaldem**: Egalitarian Democracy Index (0-1)

### Comercio (CEPII Gravity)
- **tradeflow_baci**: Fluxo de comercio bilateral (USD, reconciliado pelo BACI)
- **distw**: Distancia ponderada pela populacao (km)
- **contig, comlang_off, colony, comcol**: Variaveis gravitacionais tradicionais
- **rta**: Acordo comercial regional

### Derivadas (no painel final)
- **both_democratic**: Dummy para pares onde ambos os paises tem polyarchy >= 0.5
- **polyarchy_diff**: Diferenca absoluta de democracia entre parceiros
- **polyarchy_product**: Produto dos indices (interacao)

Ver dicionario completo em `docs/DATA_DICTIONARY.md`.

## Citacoes

### V-Dem
Coppedge, Michael, John Gerring, Carl Henrik Knutsen, Staffan I. Lindberg,
Jan Teorell, et al. 2024. "V-Dem Dataset v14." Varieties of Democracy
(V-Dem) Project. https://doi.org/10.23696/vdemds24

### CEPII Gravity
Head, Keith, and Thierry Mayer. 2014. "Gravity Equations: Workhorse, Toolkit,
and Cookbook." In Handbook of International Economics, Vol. 4.
Dataset: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8

## Ultima coleta

Data: 2026-03-13
Autor: [a preencher]
