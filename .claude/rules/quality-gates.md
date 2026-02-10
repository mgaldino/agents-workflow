---
paths:
  - "**/*.R"
  - "**/*.Rmd"
  - "**/*.py"
  - "**/*.qmd"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** — bom o suficiente para salvar
- **90/100 = PR / Circular** — pronto para compartilhar
- **95/100 = Excelência** — aspiracional

## R Scripts (.R)

| Severidade | Issue | Dedução |
|------------|-------|---------|
| Crítico | Erro de sintaxe (script não roda) | -100 |
| Crítico | Bug no domínio (especificação errada, variável trocada) | -30 |
| Crítico | Caminhos absolutos hardcoded | -20 |
| Crítico | Erros-padrão inadequados ao design (ex: OLS quando deveria clusterizar) | -20 |
| Major | `set.seed()` faltando quando há aleatorização | -10 |
| Major | Pacotes não carregados no início | -5 |
| Major | Resultados não formatados para publicação (tabelas brutas) | -5 |
| Major | Variáveis de controle sem justificativa teórica | -5 |
| Minor | Mistura de `|>` e `%>%` | -2 |
| Minor | Nomes de variáveis não descritivos | -2 |
| Minor | Código duplicado que poderia ser função | -1 |
| Minor | Comentários insuficientes em decisões metodológicas | -1 |

## Python Scripts (.py)

| Severidade | Issue | Dedução |
|------------|-------|---------|
| Crítico | Erro de sintaxe / import falha | -100 |
| Crítico | Bug no domínio (especificação errada) | -30 |
| Crítico | Caminhos absolutos hardcoded | -20 |
| Crítico | Erros-padrão inadequados ao design | -20 |
| Major | Seed faltando quando há aleatorização | -10 |
| Major | Sem type hints em funções | -5 |
| Major | Resultados não formatados | -5 |
| Minor | Imports desorganizados | -2 |
| Minor | `.apply()` onde operação vetorizada existe | -2 |
| Minor | Sem docstrings | -1 |

## RMarkdown / Quarto (.Rmd, .qmd)

| Severidade | Issue | Dedução |
|------------|-------|---------|
| Crítico | Não compila | -100 |
| Crítico | Citação quebrada (@chave não existe no .bib) | -15 |
| Crítico | Typo em equação | -10 |
| Major | Referência cruzada quebrada (Tabela X não existe) | -5 |
| Major | Inconsistência de notação | -3 |
| Major | Erro gramatical | -3 |
| Minor | Typo em texto | -1 |
| Minor | Formatação inconsistente | -1 |

## Manuscritos (conteúdo acadêmico)

| Severidade | Issue | Dedução |
|------------|-------|---------|
| Crítico | Conclusão não sustentada pela evidência | -25 |
| Crítico | Mecanismo causal implausível ou não especificado | -20 |
| Crítico | Estratégia de identificação com falha evidente | -20 |
| Major | Explicações alternativas não consideradas | -10 |
| Major | Cherry-picking de especificações | -10 |
| Major | Generalização além do escopo dos dados | -5 |
| Major | Literatura relevante não citada | -5 |
| Minor | Hedging insuficiente | -2 |
| Minor | Transições fracas entre seções | -1 |

## Enforcement

- **Score < 80**: Bloquear. Listar issues blocking.
- **80 ≤ Score < 90**: Permitir commit, alertar. Listar recomendações.
- **Score ≥ 90**: Pronto para circular/submeter.
- Usuário pode override com justificativa.
