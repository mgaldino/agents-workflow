# EXEMPLOS DE PROMPTS

Prompts prontos para copiar e colar no Codex.

## 1) Instalar skills no computador

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

## 2) Rodar triagem completa

```text
Use al-triagem para abrir um caso novo com estes dados:
- cliente_contexto: Demo interna Alandar
- tema: Proteção infantil digital
- caso_uso: falas
- modo_crise: sim
- janela_geografica: Brasil federal
- janela_temporal: últimas 24h
- objetivo_entrega: alerta executivo
- formato_saida: docx

No fim, mostre o plano de execução e os caminhos dos arquivos gerados.
```

## 3) Rodar monitoramento de falas

```text
Use al-falas para monitorar stakeholders sobre proteção infantil digital no Brasil federal.
Use janela temporal de últimas 24h e gere:
- alertas_falas.csv
- alertas_falas.md
- validacao_falas.md
```

## 4) Rodar monitoramento legislativo

```text
Use al-legis para monitorar PLs de proteção infantil digital.
Valide regras lógicas de datas e valores, e gere:
- alertas_legislacao.csv
- alertas_legislacao.md
- validacao_dados.md
```

## 5) Rodar avaliação independente

```text
Use al-critica para avaliar este relatório sem reescrever o conteúdo.
Entregue:
- score geral
- achados por prioridade
- recomendações de ajuste para o implementador
```

## 6) Rodar verificação de fontes

```text
Use al-fontes para verificar a base de fontes.
Cheque URL, data de acesso, duplicidade e campos faltantes.
Entregue:
- fontes_validadas.csv
- verificacao_fontes.md
```

## 7) Empacotar entrega final

```text
Use al-entrega para gerar pacote final com:
- entrega_cliente.docx
- anexo_tecnico.xlsx
- log_entrega.md
```
