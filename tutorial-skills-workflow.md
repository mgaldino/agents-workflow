# Tutorial rápido: usando skills em uma pesquisa com short paper

Imagine que você tem um projeto com:
```
meu-projeto/
├── paper.Rmd          # seu short paper
├── analysis.R         # script de análise
├── data/              # dados
└── references.bib
```

## 1. `/review-r analysis.R` — Auditar seu código

Rode isso primeiro. Você recebe um relatório com nota (A-F) cobrindo:
- A especificação econométrica está correta?
- Erros-padrão são adequados ao design?
- Código é reproduzível (`set.seed`, `here::here`)?
- Resultados estão formatados para publicação?

**Quando usar**: antes de circular o paper, ou quando revisitar código antigo.

**Exemplo concreto de invocação**:
```
/review-r analysis.R
```
Você recebe o relatório, corrige o que faz sentido, e segue.

---

## 2. `/review-paper paper.Rmd` — Dois pareceristas independentes

Simula o processo editorial de um top journal (APSR, AJPS, JOP) com **dois pareceristas rodando em paralelo**, cada um com ênfase distinta:

**Parecerista 1 — "O Teórico"** (pergunta guia: "por que eu deveria me importar?")
- Contribuição e originalidade
- **Framing teórico**: RQ teórica vs empírica, scope conditions, generalização
- Argumento e mecanismo causal (plausibilidade teórica)
- Narrativa e estrutura do paper
- Referências substantivas

**Parecerista 2 — "O Metodólogo"** (pergunta guia: "como você sabe que é causal?")
- Estratégia de identificação (DiD, IV, RDD, matching...)
- Dados e mensuração
- Especificação econométrica e erros-padrão
- Robustez e resultados
- Referências metodológicas

Ao final, o editor consolida numa **Carta Editorial** com: decisão, pontos de consenso, divergências, e as 3-5 prioridades para revisão.

Se o paper perguntar "qual o efeito das enchentes do RS sobre reeleição?", o Parecerista 1 vai apontar como major comment e sugerir reformular no nível teórico. Se os erros-padrão estiverem errados, o Parecerista 2 pega.

**Exemplo**:
```
/review-paper paper.Rmd
```

---

## 3. `/devils-advocate paper.Rmd` — Estressar seu argumento

Depois que o código está sólido, passe o paper pelo devil's advocate. Ele vai atacar:
- Lógica interna (saltos, falácias)
- Mecanismo causal (endogeneidade, causalidade reversa)
- Evidência empírica (cherry-picking, robustez)
- Generalização (vai além do que os dados permitem?)

Cada crítica vem com severidade (Alta/Média/Baixa) e como você poderia responder.

**Quando usar**: antes de submeter a um journal ou apresentar em seminário. Simula o referee mais duro que você pode encontrar.

**Exemplo**:
```
/devils-advocate paper.Rmd
```

---

## 4. `/interview-me` — Refinar a ideia via conversa

Este é diferente dos outros: é **interativo**. Ele faz UMA pergunta por vez no estilo orientador socrático:

1. "O que te motivou a pensar nesse tema?"
2. "Qual é a variação que você quer explicar?"
3. "O que a literatura já sabe sobre isso?"
4. "Qual seu mecanismo causal?"
5. "Como você identifica o efeito?"

No final, sintetiza tudo em: pergunta de pesquisa, argumento, estratégia empírica, contribuição, próximos passos.

**Quando usar**: no início, quando a ideia ainda está se formando, ou quando você sente que o argumento está confuso e quer clarear.

**Exemplo**:
```
/interview-me efeito de emendas parlamentares sobre reeleição de prefeitos
```

---

## Modo manual vs modo pipeline

### Modo manual: você no controle

Rode cada skill separadamente e decida o que corrigir:

```
/interview-me [tema]          ← clarear o argumento
        ↓
/review-r analysis.R          ← garantir que o código está sólido
        ↓
/review-paper paper.Rmd       ← referee report (inclui framing teórico)
        ↓
/devils-advocate paper.Rmd    ← estressar antes de submeter
        ↓
/proofread paper.Rmd          ← limpeza final
```

### Modo pipeline: automático estilo Pedro Santana

```
/research-pipeline paper.Rmd
```

Isso dispara um pipeline automatizado com **separação estrita de papéis** e **scoring numérico (0-100)**:

- **Agente Reviewer** avalia (só lê, nunca edita) e dá score
- **Agente Implementador** corrige (só implementa o que o reviewer pediu)
- Roda em **loop** (max 5 rounds) até score atingir o threshold

```
┌─────────────────────────────────────────────────────┐
│ Estágio 1: Código R                                 │
│   Reviewer dá score → Implementador corrige → loop  │
│   Aprovado quando score ≥ 80/100                    │
│   Max 5 rounds                                      │
├─────────────────────────────────────────────────────┤
│ Estágio 2: Devil's Advocate                         │
│   Reviewer ataca + score → Implementador reforça    │
│   Aprovado quando score ≥ 80/100                    │
│   Max 5 rounds                                      │
├─────────────────────────────────────────────────────┤
│ Estágio 3: Proofread (3 fases)                      │
│   Fase 1: Reviewer propõe correções (sem editar)    │
│   Fase 2: Você aprova quais correções aplicar       │
│   Fase 3: Implementador aplica só as aprovadas      │
│   Aprovado quando score ≥ 90/100                    │
└─────────────────────────────────────────────────────┘
```

A regra de ouro: **quem dá parecer nunca implementa, quem implementa nunca dá parecer.**

### "Manda ver" mode

Se não quer aprovar cada etapa manualmente:
```
/research-pipeline paper.Rmd manda ver
```
Pula a aprovação no proofread e auto-commit se score final ≥ 80.

### Quality gates

O scoring é baseado em rubrica (`.claude/rules/quality-gates.md`):
- Começa em 100, deduz por issue
- **< 80**: bloqueia, precisa corrigir
- **80-89**: OK para commit
- **≥ 90**: pronto para submeter

Relatórios ficam salvos em `quality_reports/`.

### Planos persistem em disco

Todo plano de execução é salvo em `quality_reports/plans/`. Se o contexto comprimir ou você abrir nova sessão, o Claude recupera de lá.

### Quando usar cada modo?

| Situação | Modo |
|----------|------|
| Explorando ideias, início de projeto | Manual (`/interview-me`) |
| Quer controle fino sobre cada correção | Manual (skills individuais) |
| Só código R, sem paper | **Pipeline simplificado** (auto-detecta) |
| Paper quase pronto, quer polir antes de submeter | **Pipeline completo** |
| Revisão completa pré-submissão sem interrupções | **Pipeline + "manda ver"** |
