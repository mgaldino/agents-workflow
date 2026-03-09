# GUIA RÁPIDO

Este guia é para quem não programa, mas precisa usar as skills no Codex.

## Pasta certa no repositório

Use somente:

- `codex-agents/`

Ignore para uso operacional:

- `skills-docs/`
- `rules-docs/`
- outras pastas de documentação interna

## 1) Instalar

Use o passo a passo do [README.md](README.md) para instalar as skills com um único prompt.

## 2) Fluxo padrão de trabalho

Use sempre esta sequência:

1. `al-triagem`
2. skill de produção (`al-falas`, `al-legis` ou `al-convidados`)
3. `al-critica`
4. `al-fontes`
5. `al-entrega`

Regra central:
- Quem implementa não avalia.
- Quem avalia não implementa.

## 3) Exemplo de uso diário

Prompt simples para começar:

```text
Use al-triagem para este caso:
- cliente/contexto: Demo interna Alandar
- tema: Proteção infantil digital
- caso de uso: falas
- modo crise: sim
- janela geográfica: Brasil federal
- janela temporal: últimas 24h
- objetivo da entrega: alerta executivo
- formato de saída: docx
```

## 4) Como saber que deu certo

Você deve ver:

1. Plano do caso com pipeline roteado.
2. Log de validação.
3. Entregável editável (`.docx`, e `.xlsx` quando solicitado).

## 5) Erros comuns

- Skill não encontrada:
  - Reinstale as skills via prompt do README.
- Saída incompleta:
  - Verifique se informou todos os 8 campos da triagem.
- Confusão de papéis:
  - Reforce que `al-critica` só avalia e não reescreve.
