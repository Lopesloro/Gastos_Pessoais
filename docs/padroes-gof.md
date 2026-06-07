# Padrões de Projeto GoF

Três padrões da Gang of Four aplicados de forma justificada. Para cada um:
**problema**, **solução**, **onde está** e **como é demonstrado**.

---

## 1. Factory Method (Criacional)

**Problema.** A API recebe o tipo da transação como texto (`"RECEITA"` /
`"DESPESA"`). Espalhar `if tipo == ... else ...` por todo lugar que cria
transação acopla os chamadores às subclasses concretas e dificulta adicionar
novos tipos.

**Solução.** Concentrar a criação em uma fábrica que, dado o `TipoTransacao`,
decide qual subclasse instanciar.

**Onde:** [`src/app/patterns/factory.py`](../src/app/patterns/factory.py) —
`TransacaoFactory.criar()`.
Usado por `TransacaoService.registrar()`.

**Benefício / SOLID:** Aberto/Fechado — novo tipo de transação entra pelo
dicionário de construtores, sem mexer em quem chama.

**Demonstração:** `test_factory_cria_subclasse_correta`.

---

## 2. Strategy (Comportamental)

**Problema.** Existem várias formas de resumir as finanças (por mês, por
categoria, e potencialmente anual). Um único método com `if/elif` por tipo de
relatório viraria um ponto de modificação constante e frágil.

**Solução.** Cada algoritmo de resumo é uma estratégia intercambiável que
implementa a interface `ResumoStrategy`. O `ResumoService` recebe a estratégia
e apenas a executa.

**Onde:** [`src/app/patterns/strategy.py`](../src/app/patterns/strategy.py) —
`ResumoStrategy`, `ResumoMensalStrategy`, `ResumoPorCategoriaStrategy`.
Usado por `ResumoService`.

**Benefício / SOLID:** Aberto/Fechado + Responsabilidade Única — novo relatório
é uma classe nova, sem tocar nas existentes.

**Demonstração:** `test_resumo_mensal`, `test_resumo_por_categoria`.

---

## 3. Observer (Comportamental)

**Problema.** Ao registrar uma despesa que estoura o orçamento do mês, o
sistema deve **alertar** — mas o caso de uso não deve saber *como* o alerta é
entregue (log hoje; e-mail/push amanhã). Acoplar o canal de notificação à
regra de negócio é frágil.

**Solução.** `MonitorDeOrcamento` é o *Subject*: mantém uma lista de
observadores e os notifica quando o limite é ultrapassado. Cada
`AlertaObserver` reage do seu jeito (`AlertaLogObserver`,
`AlertaColetorObserver`).

**Onde:** [`src/app/patterns/observer.py`](../src/app/patterns/observer.py).
Inscrição dos observadores em `api/dependencias.py`; disparo em
`TransacaoService.registrar()`.

**Benefício / SOLID:** baixo acoplamento + Aberto/Fechado — adicionar um canal
de alerta (ex.: `AlertaEmailObserver`) não muda o código que dispara o alerta.

**Demonstração:** `test_monitor_dispara_alerta_ao_estourar_limite`; e o campo
`alerta_orcamento` na resposta de `POST /transacoes`.

---

## Resumo

| Padrão | Tipo | Arquivo | Problema que resolve |
|--------|------|---------|----------------------|
| Factory Method | Criacional | `patterns/factory.py` | Criar Receita/Despesa sem acoplar chamadores |
| Strategy | Comportamental | `patterns/strategy.py` | Múltiplos algoritmos de resumo intercambiáveis |
| Observer | Comportamental | `patterns/observer.py` | Alertar sobre estouro de orçamento sem acoplar o canal |
