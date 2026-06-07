# ADR-005 — Persistência: SQLite implementado; PostgreSQL como evolução futura

- **Status:** Accepted (revisado — anteriormente Superseded)
- **Data original:** 2026-06-03  |  **Revisão:** 2026-06-07

> Este ADR documenta uma **decisão que evoluiu ao longo do desenvolvimento**,
> evidenciando o raciocínio arquitetural em movimento.

## Histórico de versões

| Data | Status | Decisão |
|------|--------|---------|
| 2026-06-03 | Accepted (v1) | Usar SQLite via repositório concreto. |
| 2026-06-05 | Superseded | Revertido temporariamente: manter memória enquanto a porta abstrata era validada. |
| 2026-06-07 | **Accepted (v3)** | **SQLite implementado** (`infrastructure/repositorios_sqlite.py`). PostgreSQL como evolução futura. |

## Contexto

O armazenamento em memória era suficiente para validar a arquitetura, mas não
atende ao requisito de **persistência entre execuções** — um usuário que
reinicia a aplicação perderia todos os dados.

## Decisão

Implementar **SQLite** como mecanismo de persistência, usando o módulo `sqlite3`
nativo do Python (sem ORM, sem dependência extra). O banco é criado
automaticamente em `data/gastos.db` na primeira execução.

A troca foi realizada mudando **apenas** `api/dependencias.py` (composition root)
e adicionando `infrastructure/repositorios_sqlite.py` — **zero alteração** em
domínio, aplicação ou padrões. Isso comprova empiricamente que a Inversão de
Dependência (ADR-001) funcionou.

## Consequências

**Positivas:**
- Dados persistem entre execuções.
- Sem dependência externa: `sqlite3` é nativo do Python 3.x.
- Prova da resiliência arquitetural: trocar o repositório não afetou nenhuma
  regra de negócio.

**Negativas:**
- SQLite não suporta múltiplos escritores simultâneos — sem impacto no escopo
  mono-usuário atual.
- SQL escrito à mão (simples para o domínio atual).

## Evolução futura: PostgreSQL

Migrar para PostgreSQL exigirá apenas:
1. Criar `infrastructure/repositorios_postgres.py` implementando as mesmas portas.
2. Trocar **uma linha** em `api/dependencias.py`.

## Alternativas consideradas

- *Permanecer em memória*: dados não persistem — rejeitada.
- *PostgreSQL diretamente*: servidor externo sem ganho no escopo atual — adiada.
- *SQLAlchemy (ORM)*: dependência desnecessária para domínio pequeno — rejeitada.
