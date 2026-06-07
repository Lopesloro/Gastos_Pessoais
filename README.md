# Controle de Gastos Pessoais

Trabalho final da disciplina — projeto de software com **arquitetura
justificada**, **SOLID**, **Clean Code** e **padrões GoF**.

O sistema permite ao usuário registrar **receitas** e **despesas** por
**categoria**, ver **resumos mensais** e receber **alertas** quando os gastos
do mês ultrapassam um limite (orçamento).

## Stack

- **Python 3.11** + **FastAPI** (API REST com OpenAPI/Swagger automático)
- **Pydantic v2** (validação na borda)
- **pytest** (testes de unidade e integração)
- Armazenamento **em memória** (trocável — ver [ADR-005](docs/adr/ADR-005-sqlite-para-postgresql.md))

## Como rodar

```bash
# 1. criar e ativar o ambiente virtual (Windows PowerShell)
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. instalar dependências
pip install -r requirements.txt

# 3. subir a API
uvicorn src.app.main:app --reload

# 4. abrir a documentação interativa (Swagger UI)
#    http://127.0.0.1:8000/docs
```

## Como testar

```bash
pytest -q
```

## Arquitetura (visão rápida)

Clean Architecture em 4 camadas, com a regra de dependência apontando sempre
para dentro (infra → aplicação → domínio):

```
            ┌─────────────────────────────────────────┐
            │  api/  (FastAPI: rotas, schemas, DI)     │  ← detalhes externos
            ├─────────────────────────────────────────┤
            │  application/  (casos de uso/serviços)   │
            ├─────────────────────────────────────────┤
            │  domain/  (entidades + interfaces repo)  │  ← núcleo, sem deps
            └─────────────────────────────────────────┘
   infrastructure/  implementa as interfaces do domínio (adaptadores)
   patterns/        Factory, Strategy, Observer
```

Detalhes e justificativas em [`docs/arquitetura.md`](docs/arquitetura.md).

## Mapa da documentação

| Documento | Conteúdo |
|-----------|----------|
| [docs/arquitetura.md](docs/arquitetura.md) | Estilo arquitetural, camadas, diagrama, regra de dependência |
| [docs/atributos-qualidade.md](docs/atributos-qualidade.md) | Atributos de qualidade priorizados e como foram atendidos |
| [docs/solid.md](docs/solid.md) | Os 5 princípios SOLID com exemplos do próprio código |
| [docs/clean-code.md](docs/clean-code.md) | Práticas de Clean Code aplicadas |
| [docs/padroes-gof.md](docs/padroes-gof.md) | Factory, Strategy e Observer: problema, solução, onde estão |
| [docs/adr/](docs/adr/) | 5 ADRs (incluindo uma decisão **revertida**) |
| [openapi/swagger.yaml](openapi/swagger.yaml) | Especificação OpenAPI da API |

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/categorias` | Cria categoria |
| GET | `/categorias` | Lista categorias |
| POST | `/transacoes` | Registra receita/despesa (dispara alerta se estourar limite) |
| GET | `/transacoes` | Lista transações |
| GET | `/resumo/mensal?mes=&ano=` | Resumo mensal (Strategy) |
| GET | `/resumo/por-categoria` | Saldo por categoria (Strategy) |
| GET | `/health` | Healthcheck |
