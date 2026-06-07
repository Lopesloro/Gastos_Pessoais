# Controle de Gastos Pessoais

Trabalho final da disciplina **Padrões e Arquitetura de Software** — PUC-Campinas.

Projeto de software com arquitetura justificada, SOLID, Clean Code e padrões GoF (Factory, Strategy, Observer).

> **Documento final (PDF):** [`docs/DOCUMENTO-FINAL.pdf`](docs/DOCUMENTO-FINAL.pdf)

---

## Rodando o projeto (passo a passo)

### Pré-requisitos
- Python 3.11 ou superior instalado
- Git (para clonar o repositório)

### 1. Clonar o repositório

```bash
git clone https://github.com/Lopesloro/Gastos_Pessoais.git
cd Gastos_Pessoais
```

### 2. Criar o ambiente virtual

```bash
# Windows (PowerShell)
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Subir a API

```bash
uvicorn src.app.main:app --reload
```

### 5. Abrir no navegador

| O que abrir | Endereço | Para quem |
|-------------|----------|-----------|
| **Interface do usuário** | http://127.0.0.1:8000 | Cliente final — tela de lançamentos |
| **Swagger UI (API interativa)** | http://127.0.0.1:8000/docs | Testar os endpoints da API |
| **ReDoc (documentação)** | http://127.0.0.1:8000/redoc | Documentação formal da API |

O banco de dados SQLite é criado automaticamente em `data/gastos.db` na primeira execução.

---

## Rodando os testes

```bash
pytest -q
```

Resultado esperado: **9 passed** (testes de domínio, padrões GoF e API).

---

## Stack

| Tecnologia | Uso |
|------------|-----|
| Python 3.11 | Linguagem principal |
| FastAPI | Framework web / API REST |
| Pydantic v2 | Validação de dados na borda |
| SQLite (nativo) | Persistência — banco criado em `data/gastos.db` |
| pytest | Testes automatizados |

---

## Endpoints da API (`/api/v1`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v1/categorias` | Cria categoria |
| `GET` | `/api/v1/categorias` | Lista categorias |
| `POST` | `/api/v1/transacoes` | Registra receita/despesa (dispara alerta se estourar limite) |
| `GET` | `/api/v1/transacoes` | Lista transações |
| `GET` | `/api/v1/resumo/mensal?mes=6&ano=2026` | Resumo mensal (padrão Strategy) |
| `GET` | `/api/v1/resumo/por-categoria` | Saldo por categoria (padrão Strategy) |
| `GET` | `/health` | Healthcheck |

Especificação completa: [`openapi/swagger.yaml`](openapi/swagger.yaml)

---

## Arquitetura — visão rápida

Clean Architecture em 4 camadas (a dependência aponta sempre para dentro):

```
┌──────────────────────────────────────────────────────┐
│  api/          FastAPI: rotas, schemas, DI            │ ← detalhe externo
├──────────────────────────────────────────────────────┤
│  application/  Casos de uso (serviços)               │
├──────────────────────────────────────────────────────┤
│  domain/       Entidades + interfaces de repositório │ ← núcleo puro
└──────────────────────────────────────────────────────┘
   infrastructure/  Adaptadores (SQLite)
   patterns/         Factory · Strategy · Observer
```

---

## Estrutura do repositório

```
/
├── adrs/               5 ADRs (incluindo decisão revertida — ADR-005)
├── diagrams/           Diagramas UML em Mermaid (C4, classes, sequência)
├── docs/               Documentação completa
│   └── DOCUMENTO-FINAL.pdf   ← entregável principal
├── openapi/            swagger.yaml (especificação OpenAPI)
├── src/app/
│   ├── api/            Rotas, schemas, injeção de dependência
│   ├── application/    Casos de uso
│   ├── domain/         Entidades e portas (interfaces)
│   ├── infrastructure/ Repositórios SQLite e em memória
│   └── patterns/       Factory, Strategy, Observer
├── tests/              9 testes automatizados
├── data/               gastos.db (criado automaticamente)
└── requirements.txt
```

---

## Mapa da documentação

| Documento | Conteúdo |
|-----------|----------|
| [`docs/DOCUMENTO-FINAL.pdf`](docs/DOCUMENTO-FINAL.pdf) | **Documento final — 10 seções obrigatórias** |
| [`docs/arquitetura.md`](docs/arquitetura.md) | Plano macro (monólito modular) + plano interno (Clean Architecture) |
| [`docs/atributos-qualidade.md`](docs/atributos-qualidade.md) | 3 atributos ISO 25010 com métricas observáveis |
| [`docs/solid.md`](docs/solid.md) | 5 princípios SOLID com trechos do código |
| [`docs/clean-code.md`](docs/clean-code.md) | Práticas de Clean Code aplicadas |
| [`docs/padroes-gof.md`](docs/padroes-gof.md) | Factory, Strategy, Observer — problema, solução, código |
| [`docs/api.md`](docs/api.md) | Versionamento, erros, paginação, autenticação |
| [`adrs/`](adrs/) | 5 ADRs no formato canônico |
| [`diagrams/`](diagrams/) | Fontes Mermaid dos diagramas |
