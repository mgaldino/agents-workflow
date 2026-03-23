# Dados -- Painel America Latina (PIB per capita e Populacao)

## Descricao

Painel pais-ano com PIB per capita (USD correntes) e populacao total para 20 paises da America Latina, cobrindo o periodo 2000-2023. Fonte: World Bank World Development Indicators (WDI).

## Estrutura do projeto

```
data/
├── raw/                              # Dados brutos (JSONs da API do World Bank)
├── processed/
│   └── painel_latam.csv              # Painel consolidado (CSV UTF-8)
├── scripts/
│   ├── download_worldbank.py         # Download via API do World Bank
│   ├── process_worldbank.py          # Limpeza e consolidacao
│   └── requirements.txt              # Dependencias Python
├── docs/
│   ├── SOURCES.yaml                  # Manifesto de fontes
│   └── DATA_DICTIONARY.md            # Dicionario de variaveis
├── .env.example                      # Template de credenciais
├── .gitignore                        # Exclusoes do git
├── checksums.sha256                  # Integridade dos arquivos
└── README.md                         # Este arquivo
```

## Como reproduzir a coleta

1. Criar e ativar ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r scripts/requirements.txt
   ```

3. Configurar credenciais (opcional -- a API do World Bank nao requer):
   ```bash
   cp .env.example .env
   ```

4. Executar scripts na ordem:
   ```bash
   python scripts/download_worldbank.py
   python scripts/process_worldbank.py
   ```

5. Verificar integridade:
   ```bash
   sha256sum -c checksums.sha256
   ```

## Fontes

Ver detalhes completos em `docs/SOURCES.yaml`.

| Fonte | Acesso | Credencial? | Script |
|-------|--------|-------------|--------|
| World Bank WDI | API v2 (JSON) | Nao | download_worldbank.py |

## Indicadores

| Codigo WDI | Variavel no painel | Descricao |
|------------|-------------------|-----------|
| NY.GDP.PCAP.CD | gdp_per_capita_current_usd | PIB per capita (USD correntes) |
| SP.POP.TOTL | population_total | Populacao total |

## Cobertura

- **Paises**: 20 (ARG, BOL, BRA, CHL, COL, CRI, CUB, DOM, ECU, SLV, GTM, HTI, HND, MEX, NIC, PAN, PRY, PER, URY, VEN)
- **Periodo**: 2000-2023
- **Unidade de analise**: pais-ano
- **Linhas esperadas**: 480 (20 paises x 24 anos)

## Ultima coleta

Data: 2026-03-13
Autor: Manoel Galdino (via Claude data-collection skill)
