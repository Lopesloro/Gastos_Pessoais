# ADR-005 — Persistência: de SQLite para PostgreSQL (decisão revertida)

- **Status:** **Revertido / Substituído** (originalmente Aceito em 2026-06-03,
  revertido em 2026-06-05)
- **Data:** 2026-06-05

> Este ADR documenta intencionalmente uma **decisão que mudou ao longo do
> tempo**, para evidenciar a evolução do raciocínio arquitetural.

## Contexto
Para persistir transações e categorias, inicialmente decidiu-se usar **SQLite**
(arquivo local, zero configuração) — ADR-005 v1, *Aceito* em 2026-06-03.

Pouco depois, ao revisar os atributos de qualidade, levantou-se a hipótese de
já migrar para **PostgreSQL**, antecipando concorrência e múltiplos usuários.

## Decisão (evolução)
1. **v1 (2026-06-03) — Aceito:** usar SQLite via repositório concreto.
2. **v2 (2026-06-05) — Revertido:** **não** introduzir banco agora. Para o
   escopo (projeto acadêmico, foco em arquitetura e padrões), um banco real
   adicionaria configuração, dependências e migrações sem agregar ao objetivo
   da disciplina. PostgreSQL fica como evolução futura documentada.

A decisão final é: **manter o armazenamento atrás da porta abstrata
`*Repository`, com implementação em memória** (`*RepositoryMemoria`).

## Por que a reversão foi barata
Graças ao ADR-001 (Inversão de Dependência), o armazenamento sempre esteve
atrás de uma interface. Trocar a implementação **não afeta** domínio,
aplicação nem API. A migração futura para SQLite/PostgreSQL será:

1. criar `TransacaoRepositoryPostgres(TransacaoRepository)` em
   `infrastructure/`;
2. trocar **uma linha** em `api/dependencias.py`.

## Consequências
**Positivas:** projeto roda sem setup; foco no que a disciplina avalia;
caminho de migração claro e de baixo risco.
**Negativas:** dados não persistem entre execuções — aceitável no escopo;
mitigado pelo design que permite plugar persistência quando necessário.

## Alternativas consideradas
- *SQLite agora* (v1): persistência simples, mas adiciona migrações/ORM sem
  ganho para os objetivos atuais. Adiada.
- *PostgreSQL agora*: superdimensionado para o escopo. Rejeitada por ora.
