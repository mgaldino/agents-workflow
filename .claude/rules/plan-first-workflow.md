---
paths:
  - "**/*"
---

# Plan-First Workflow

**Para qualquer tarefa não-trivial, entre em plan mode antes de escrever código.**

## O Protocolo

1. **Enter Plan Mode** — use `EnterPlanMode`
2. **Checar MEMORY.md** — ler entries relevantes para a tarefa
3. **Rascunhar o plano** — que mudanças, quais arquivos, em que ordem
4. **Salvar em disco** — escrever em `quality_reports/plans/YYYY-MM-DD_descricao-curta.md`
5. **Apresentar ao usuário** — esperar aprovação
6. **Exit plan mode** — somente após aprovação
7. **Implementar via orchestrator** — ver `orchestrator-protocol.md` ou `research-pipeline`

## Planos em Disco

Planos sobrevivem à compressão de contexto. Salvar todo plano em:

```
quality_reports/plans/YYYY-MM-DD_descricao-curta.md
```

Formato do arquivo de plano:

```markdown
# Plano: [título]

**Status**: DRAFT | APPROVED | COMPLETED
**Data**: YYYY-MM-DD

## Objetivo
[O que será feito]

## Abordagem
[Como será feito]

## Arquivos a modificar
- [ ] arquivo1.R — [o que muda]
- [ ] arquivo2.Rmd — [o que muda]

## Verificação
- [ ] [Como verificar que funcionou]
```

## Context Management

- Preferir auto-compressão sobre `/clear`
- Salvar contexto importante em disco antes de perder
- `/clear` apenas quando contexto está genuinamente poluído

## Session Recovery

Após compressão ou nova sessão:
1. Ler `CLAUDE.md` + plano mais recente em `quality_reports/plans/`
2. Checar `git log --oneline -10` e `git diff`
3. Declarar o que você entende ser a tarefa atual
