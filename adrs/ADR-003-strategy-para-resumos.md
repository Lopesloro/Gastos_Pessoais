# ADR-003 — Usar Strategy para os resumos

- **Status:** Aceito
- **Data:** 2026-06-02

## Contexto
Há mais de uma forma de resumir as finanças (mensal, por categoria) e a
tendência é surgirem mais (anual, por período). Concentrar tudo num método com
`if/elif` tornaria esse método um ponto de modificação constante.

## Decisão
Modelar cada algoritmo de resumo como uma `ResumoStrategy` intercambiável,
executada por um `ResumoService` genérico.

## Consequências
**Positivas:** novo relatório = nova classe, sem alterar as existentes;
estratégias testáveis isoladamente.
**Negativas:** uma classe por relatório — desejável aqui.

## Alternativas consideradas
- *Métodos fixos no serviço*: simples no começo, mas acumula condicionais e
  viola Responsabilidade Única. Rejeitada.
