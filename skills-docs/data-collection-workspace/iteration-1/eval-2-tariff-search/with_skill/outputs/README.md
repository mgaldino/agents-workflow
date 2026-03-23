# Dados -- Tarifas Comerciais de Paises da OCDE (2000-2010)

## Como reproduzir a coleta

1. Instalar dependencias: `pip install -r scripts/requirements.txt`
2. Configurar credenciais: copie `.env.example` para `.env` e preencha (apenas CEPII requer credencial obrigatoria)
3. Executar scripts na ordem:
   - `python scripts/download_wits.py` (fonte principal: UNCTAD TRAINS via WITS)
   - `python scripts/download_oecd.py` (complemento: indicadores OCDE via SDMX)
   - `python scripts/download_wto.py` (complemento: WTO tariff profiles)
   - `python scripts/download_dataverse.py` (busca: Harvard Dataverse)
   - `python scripts/download_cepii.py` (opcional: tarifas bilaterais MAcMap, requer registro)
   - `python scripts/process_tariffs.py` (consolidacao do painel final)
4. Verificar integridade: `sha256sum -c checksums.sha256`

## Fontes

Ver detalhes completos em `docs/SOURCES.yaml`.

| Fonte | Acesso | Credencial? | Script | Prioridade |
|-------|--------|-------------|--------|------------|
| WITS / UNCTAD TRAINS | API | Nao | download_wits.py | Principal |
| OECD Data Explorer | API (SDMX) | Nao | download_oecd.py | Complemento |
| WTO Tariff Profiles | API/Bulk | Opcional | download_wto.py | Complemento |
| Harvard Dataverse | API | Opcional | download_dataverse.py | Exploratoria |
| CEPII MAcMap-HS6 | Bulk download | Sim | download_cepii.py | Opcional (bilateral) |

## Estrutura de diretorios

```
outputs/
├── raw/                         # Dados brutos (nunca modificar)
│   ├── wits_tariffs_oecd_SAMPLE.csv
│   └── (arquivos baixados pelos scripts)
├── processed/                   # CSVs consolidados
│   └── oecd_tariffs_panel_SAMPLE.csv
├── scripts/
│   ├── download_wits.py         # UNCTAD TRAINS via World Bank WITS
│   ├── download_oecd.py         # OECD SDMX API
│   ├── download_wto.py          # WTO data portal
│   ├── download_dataverse.py    # Harvard Dataverse search
│   ├── download_cepii.py        # CEPII MAcMap (bilateral tariffs)
│   ├── process_tariffs.py       # Consolidacao do painel
│   └── requirements.txt         # Dependencias Python
├── docs/
│   ├── SOURCES.yaml             # Manifesto de fontes
│   └── DATA_DICTIONARY.md       # Dicionario de variaveis
├── .env.example                 # Template de credenciais
├── .gitignore                   # Exclui .env e arquivos grandes
├── checksums.sha256             # Integridade dos arquivos
└── README.md                    # Este arquivo
```

## Notas sobre as fontes

### Recomendacao principal: WITS / UNCTAD TRAINS
A fonte mais completa para tarifas MFN aplicadas de paises da OCDE (2000-2010).
Acesso gratuito via API, sem necessidade de credenciais. Cobre todos os 34 paises
da OCDE com dados anuais ao nivel de produto (HS6) ou agregado.

### CEPII MAcMap (opcional)
So necessario se a pesquisa requer tarifas *bilaterais* (incluindo preferencias
de acordos comerciais). Disponivel apenas para anos de referencia (2001, 2004, 2007, 2010).
Requer registro gratuito no site da CEPII.

### Harvard Dataverse
O script de busca encontra datasets de replicacao que podem conter dados tarifarios
ja tratados. Util para comparacao ou para encontrar variaveis derivadas usadas em
artigos especificos. A busca por "trade tariffs OECD" retorna datasets relevantes.

## Ultima coleta

Data: 2026-03-13
Autor: (preencher)
