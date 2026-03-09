# GUIA CRIAR SKILL

Guia prático para criar ou editar skills da equipe.

## Pasta oficial de trabalho

Crie e edite skills somente dentro de:

- `codex-agents/skills/`

Não use `skills-docs/` para operação da equipe. Essa pasta pode conter materiais de referência e não o pacote ativo de produção.

## 1) Convenção de nomes

Use nomes mnemônicos curtos:

- Prefixo obrigatório: `al-`
- Exemplo: `al-triagem`, `al-legis`, `al-falas`

## 2) Estrutura mínima

Cada skill deve ter:

1. `SKILL.md`
2. `agents/openai.yaml`
3. `scripts/` (opcional, quando houver automação)

## 3) Template de `SKILL.md`

```md
---
name: al-nome-da-skill
description: O que a skill faz e quando usar.
---

# al-nome-da-skill

## 1) Entrada mínima
- campo_1
- campo_2

## 2) Regras
- regra_1
- regra_2

## 3) Entregáveis
- arquivo_1
- arquivo_2

## 4) Limites da skill
- o que ela não deve fazer
```

## 4) Template de `agents/openai.yaml`

```yaml
interface:
  display_name: "AL Nome"
  short_description: "Resumo curto da skill"
  default_prompt: "Instrução padrão para iniciar a skill."
```

## 5) Critérios de qualidade antes de publicar

1. Nome curto e memorável.
2. Escopo claro (entrada, regras, saída, limites).
3. Sem mistura de papéis (implementação x avaliação).
4. Script testado, se existir.
5. Texto em português correto e com acentuação.

## 6) Atualização de skill existente

1. Edite o `SKILL.md`.
2. Ajuste o `openai.yaml` se necessário.
3. Rode testes do script, se houver.
4. Atualize exemplos em [EXEMPLOS_PROMPTS.md](EXEMPLOS_PROMPTS.md) quando mudar interface.
