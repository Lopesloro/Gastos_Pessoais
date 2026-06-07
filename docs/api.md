# Design de API

## Estilo escolhido: REST + OpenAPI 3.x

**Justificativa.** O domínio é orientado a **recursos** com operações CRUD
claras (categorias, transações) e consultas (resumos). REST mapeia isso
naturalmente em recursos + verbos HTTP, é amplamente conhecido e, com FastAPI,
gera a especificação **OpenAPI 3.1** automaticamente (em
[`openapi/swagger.yaml`](../openapi/swagger.yaml)) e uma UI interativa em
`/docs`. GraphQL seria sobredimensionado (não há grafos de consulta complexos)
e gRPC não se aplica (consumidor é um navegador).

A especificação formal completa está versionada no repositório:
[`openapi/swagger.yaml`](../openapi/swagger.yaml).

## Recursos e operações

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/categorias` | Cria categoria |
| GET | `/categorias` | Lista categorias |
| POST | `/transacoes` | Registra receita/despesa (avalia orçamento → alerta) |
| GET | `/transacoes` | Lista transações |
| GET | `/resumo/mensal?mes=&ano=` | Resumo mensal (padrão Strategy) |
| GET | `/resumo/por-categoria` | Saldo por categoria (padrão Strategy) |
| GET | `/health` | Healthcheck |

## Estratégia de versionamento

Adotado **versionamento por caminho de URL** com prefixo de versão maior
(*major*): a versão atual é a `v1` e a evolução planejada é prefixar as rotas
com `/api/v1`. A escolha por URL (em vez de header ou modelo sem versão da
Stripe) privilegia **clareza e descoberta**: a versão fica visível na própria
URL e em qualquer log, o que é didaticamente mais transparente. A regra:

- Mudanças **retrocompatíveis** (novo campo opcional, nova rota) **não** mudam
  a versão.
- Mudanças **quebra-contrato** (remoção/renomeação de campo, mudança de
  semântica) incrementam para `/api/v2`, mantendo `/api/v1` durante a
  transição.

## Convenções de erro

Erros seguem os códigos de status HTTP e o corpo padrão do FastAPI:

```json
{ "detail": "O valor da transação deve ser positivo." }
```

| Situação | Status | Corpo |
|----------|--------|-------|
| Validação de schema (tipo/campo inválido) | `422 Unprocessable Entity` | `detail` com lista de erros por campo |
| Violação de regra de domínio (ex.: valor ≤ 0) | `422 Unprocessable Entity` | `detail` com a mensagem da regra |
| Recurso/rota inexistente | `404 Not Found` | `detail: "Not Found"` |
| Sucesso na criação | `201 Created` | recurso criado |

A camada de API traduz exceções de domínio (`ValueError`) em `HTTP 422`,
mantendo o domínio agnóstico de HTTP (ver `api/rotas.py`).

## Paginação

As coleções atuais (`GET /categorias`, `GET /transacoes`) retornam a lista
completa — adequado ao volume de um único usuário. A estratégia **planejada**
para quando o volume crescer é paginação por *offset/limit* via query string,
retrocompatível (parâmetros opcionais com padrão):

```
GET /transacoes?limite=50&deslocamento=0
```

## Autenticação

O escopo atual é **mono-usuário local**, portanto não há autenticação — decisão
consciente registrada nos atributos de qualidade (Segurança despriorizada). A
evolução planejada, caso o sistema se torne multiusuário, é **OAuth2 com Bearer
Token (JWT)**, nativamente suportado pelo FastAPI via `OAuth2PasswordBearer`,
protegendo as rotas de escrita.
