# ADR-002 — Usar Factory Method para criar transações

- **Status:** Aceito
- **Data:** 2026-06-01

## Contexto
A API recebe o tipo de transação como string. Receita e Despesa são subclasses
de `Transacao` com comportamento diferente (sinal do valor). É preciso decidir
onde mora a lógica de "qual subclasse instanciar".

## Decisão
Centralizar a criação em `TransacaoFactory.criar()`, que mapeia
`TipoTransacao` → subclasse concreta.

## Consequências
**Positivas:** chamadores não conhecem as subclasses; adicionar um novo tipo
(ex.: Investimento) é uma linha na fábrica (Aberto/Fechado).
**Negativas:** uma indireção a mais — trivial neste caso.

## Alternativas consideradas
- *`if/elif` no serviço*: espalharia a decisão e violaria Aberto/Fechado.
  Rejeitada.
