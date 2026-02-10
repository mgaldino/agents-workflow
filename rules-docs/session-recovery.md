---
paths:
  - "**/*"
---

# Session Recovery Protocol

**Após compressão de contexto ou início de nova sessão, execute este protocolo.**

## Passos

1. **Ler CLAUDE.md** na raiz do projeto
2. **Ler MEMORY.md** em `~/.claude/projects/.../memory/MEMORY.md`
3. **Verificar planos recentes**:
   ```
   ls quality_reports/plans/ | sort -r | head -5
   ```
   Ler o mais recente. Verificar seu status (DRAFT/APPROVED/COMPLETED).
4. **Verificar estado do git**:
   ```
   git log --oneline -10
   git diff --stat
   git status
   ```
5. **Declarar entendimento**: Dizer ao usuário o que você entende ser a tarefa atual e o estado do projeto. Pedir confirmação antes de continuar.

## Quando ativar

- Após qualquer compressão automática de contexto
- No início de qualquer nova sessão Claude Code
- Quando o usuário diz "continue de onde parou" ou similar
- Quando o contexto parece incompleto ou confuso

## Prioridade de fontes

1. Plano mais recente em `quality_reports/plans/` (mais específico)
2. `MEMORY.md` (notas persistentes)
3. `CLAUDE.md` (convenções do projeto)
4. `git log` e `git diff` (estado do código)
