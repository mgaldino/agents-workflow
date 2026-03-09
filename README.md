# Agents Workflow

Repositório para organizar skills e fluxos de trabalho com Codex/Claude para projetos de análise, monitoramento e entrega.

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
5) Copie para ~/.codex/skills/ apenas as skills definidas para a equipe.
6) Liste as skills instaladas no final.
7) Me diga exatamente o que foi feito e qualquer erro.

Não altere nada fora de ~/.codex/skills e /tmp.
```

## Guias

- Uso no dia a dia: [GUIA_RAPIDO.md](GUIA_RAPIDO.md)
- Criar e editar skills: [GUIA_CRIAR_SKILL.md](GUIA_CRIAR_SKILL.md)
- Biblioteca de prompts: [EXEMPLOS_PROMPTS.md](EXEMPLOS_PROMPTS.md)

## Estrutura recomendada para skills da equipe

- `al-triagem`: intake e roteamento
- `al-convidados`: lista priorizada de convidados
- `al-legis`: monitoramento legislativo
- `al-falas`: monitoramento de falas
- `al-critica`: avaliação independente
- `al-fontes`: verificação de fontes
- `al-entrega`: empacotamento final de entregáveis
