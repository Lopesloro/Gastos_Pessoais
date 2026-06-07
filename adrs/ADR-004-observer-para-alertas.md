# ADR-004 — Usar Observer para alertas de orçamento

- **Status:** Aceito
- **Data:** 2026-06-02

## Contexto
Quando uma despesa faz os gastos do mês ultrapassarem o limite, o usuário deve
ser alertado. O canal de alerta pode mudar (log agora; e-mail/push depois) e o
caso de uso que registra a transação não deve depender desse detalhe.

## Decisão
Aplicar o padrão **Observer**: `MonitorDeOrcamento` (Subject) notifica
observadores inscritos (`AlertaLogObserver`, `AlertaColetorObserver`) quando o
limite é estourado.

## Consequências
**Positivas:** baixo acoplamento; adicionar um canal novo não muda o disparo
do alerta; comportamento testável e exposto via campo `alerta_orcamento`.
**Negativas:** indireção extra entre quem dispara e quem trata o alerta.

## Alternativas consideradas
- *Enviar o alerta direto dentro do serviço*: acoplaria a regra ao canal e
  dificultaria testes e extensão. Rejeitada.
