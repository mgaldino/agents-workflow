# Agents Workflow

Repositório para organizar skills e fluxos de trabalho com Codex/Claude para projetos de análise, monitoramento e entrega.

## Pasta oficial para uso no Codex

Para instalação e uso no dia a dia, considere **apenas**:

- `codex-agents/`

Todo o restante do repositório (`skills-docs/`, `rules-docs/`, etc.) não deve ser usado para instalação operacional das skills da equipe.

## Começar rápido (sem conhecimento técnico)

1. Abra o Codex no seu computador.
2. Copie e cole o prompt abaixo.
3. Aguarde a instalação e leia o resumo final que o Codex mostrar.

```text
Quero instalar as skills da Alandar neste computador.

Faça tudo automaticamente:
1) Verifique se existe a pasta ~/.codex/skills.
2) Faça backup das skills locais em ~/.codex/skills_backup_<datahora>.
3) Tente clonar o repositório https://github.com/mgaldino/agents-workflow.git para /tmp/alandar-skills.
4) Se git não estiver disponível, baixe o ZIP da branch main via HTTPS, extraia em /tmp/alandar-skills.
5) Use somente /tmp/alandar-skills/codex-agents como origem.
6) Copie para ~/.codex/skills/ apenas o conteúdo de /tmp/alandar-skills/codex-agents/skills/.
7) Se /tmp/alandar-skills/codex-agents/skills não existir, pare e me avise.
8) Liste as skills instaladas no final.
9) Me diga exatamente o que foi feito e qualquer erro.

Não use skills-docs, rules-docs ou outras pastas do repositório para instalação.

Não altere nada fora de ~/.codex/skills e /tmp.
```

## Guias

- Uso no dia a dia: [GUIA_RAPIDO.md](GUIA_RAPIDO.md)
- Criar e editar skills: [GUIA_CRIAR_SKILL.md](GUIA_CRIAR_SKILL.md)
- Biblioteca de prompts: [EXEMPLOS_PROMPTS.md](EXEMPLOS_PROMPTS.md)

## Estrutura recomendada para skills da equipe

- Caminho base: `codex-agents/skills/`
- `al-triagem`: intake e roteamento
- `al-convidados`: lista priorizada de convidados
- `al-legis`: monitoramento legislativo
- `al-falas`: monitoramento de falas
- `al-critica`: avaliação independente
- `al-fontes`: verificação de fontes
- `al-entrega`: empacotamento final de entregáveis
