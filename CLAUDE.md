# Projeto de Pesquisa — Ciência Política, RI e Econometria

## Skills disponíveis

| Comando | Descrição | Edita arquivos? |
|---------|-----------|-----------------|
| `/data-analysis-r` | Análise de dados end-to-end em R (fixest, tidyverse, modelsummary) | Sim |
| `/data-analysis-python` | Análise de dados em Python (pandas, statsmodels, pyfixest) | Sim |
| `/review-r` | Revisão de qualidade de código R | Não |
| `/review-python` | Revisão de qualidade de código Python | Não |
| `/compile-rmd` | Compilar RMarkdown para PDF ou HTML | Não* |
| `/proofread` | Revisão de gramática, typos e consistência | Não |
| `/deploy` | Render RMarkdown + deploy GitHub Pages | Sim |
| `/lit-review` | Revisão de literatura sistemática + gaps | Não |
| `/research-ideation` | Gerar questões de pesquisa + estratégias empíricas | Não |
| `/review-paper` | Revisão de manuscrito estilo referee | Não |
| `/interview-me` | Entrevista interativa para refinar ideias | Não |
| `/devils-advocate` | Desafiar argumentos e apresentações | Não |
| `/visual-audit` | Auditoria visual de slides | Não |
| `/slide-excellence` | Revisão multi-dimensão de slides | Não |
| `/pedagogy-review` | Revisão de narrativa, notação e pacing | Não |
| `/validate-bib` | Validar referências cruzadas de citações | Não |
| `/abstract-annotator` | Anotar abstract: 5 elementos essenciais + score + sugestões de corte | Não |
| **`/research-pipeline`** | **Pipeline automático: review → fix → review (agentes separados)** | **Sim** |

*`/compile-rmd` gera arquivos de output mas não edita o .Rmd fonte.

## Pipeline automático (`/research-pipeline`)

Orquestra agentes separados em loop — quem revisa nunca implementa, quem implementa nunca revisa. Scoring numérico 0-100 com quality gates.

```
Estágio 1: Reviewer avalia código (score) → Implementador corrige → loop (max 5x, threshold ≥80)
Estágio 2: Reviewer ataca argumento (score) → Implementador reforça → loop (max 5x, threshold ≥80)
Estágio 3: Reviewer propõe correções → Usuário aprova → Implementador aplica (threshold ≥90)
```

**Just Do It Mode**: diga "manda ver" para pular aprovações e auto-commit se score ≥ 80.

Uso: `/research-pipeline paper.Rmd` ou `/research-pipeline analysis.R paper.Rmd`

## Rules (automáticas)

Arquivos em `.claude/rules/` são carregados automaticamente:

| Rule | O que faz |
|------|-----------|
| `quality-gates.md` | Rubrica de scoring 0-100 com deduções por tipo de issue |
| `plan-first-workflow.md` | Salvar planos em `quality_reports/plans/` antes de implementar |
| `session-recovery.md` | Recuperar contexto após compressão ou nova sessão |

## Convenções do projeto

- **R**: tidyverse style, pipe `|>`, fixest para regressões, modelsummary para tabelas
- **Python**: PEP 8, type hints, pathlib para caminhos, pyfixest quando possível
- **Caminhos**: usar `here::here()` (R) ou `pathlib.Path` (Python)
- **Reprodutibilidade**: sempre `set.seed()` / `numpy.random.default_rng(seed)`
- **Erros-padrão**: sempre especificar e documentar tipo (cluster, robust, HC)
- **Planos**: salvar em `quality_reports/plans/YYYY-MM-DD_descricao.md`
- **Relatórios**: pipeline reports em `quality_reports/`
