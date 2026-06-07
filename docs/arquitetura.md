# Arquitetura de Software

## Plano macro — decomposição em unidades implantáveis

O sistema é um **monólito modular** (uma única unidade implantável, organizada
internamente em módulos/camadas bem separados), **não** um conjunto de
microsserviços.

**Justificativa (vinculada à seção de atributos de qualidade):**
- O atributo prioritário é **manutenibilidade**, não escalabilidade. Não há
  requisito de escalar partes do sistema de forma independente, o que é a
  principal razão para adotar microsserviços.
- **Tamanho/maturidade da equipe:** equipe pequena e domínio enxuto.
  Microsserviços trariam custo de operação (deploys múltiplos, comunicação em
  rede, observabilidade distribuída) sem benefício para os atributos
  declarados — seria *over-engineering*.
- O monólito **modular** preserva a opção futura: como cada módulo já tem
  fronteiras claras (domínio, aplicação, infraestrutura), extrair um serviço
  depois seria viável se o contexto mudar.

> Resumo: **macro = monólito modular**; **interno = Clean Architecture em
> camadas** (detalhado a seguir).

## Plano interno — estilo arquitetural escolhido

**Clean Architecture / Arquitetura em Camadas** (variante hexagonal — portas e
adaptadores). Quatro camadas concêntricas, com uma única regra: **as
dependências apontam sempre para dentro**. O núcleo (domínio) não conhece
ninguém; os detalhes (web, banco, bibliotecas) ficam na borda e dependem do
núcleo, nunca o contrário.

```
┌──────────────────────────────────────────────────────────┐
│ infrastructure/  +  api/        (Frameworks & Drivers)    │
│  ┌────────────────────────────────────────────────────┐  │
│  │ application/                  (Casos de Uso)        │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ domain/        (Entidades + regras + portas)  │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
        fluxo de dependência  ───────────────►  para dentro
```

## Camadas e responsabilidades

| Camada | Pasta | Conhece | Responsabilidade |
|--------|-------|---------|------------------|
| Domínio | `src/app/domain/` | nada | Entidades (`Categoria`, `Transacao`, `Receita`, `Despesa`), regras de negócio invariantes e **interfaces** de repositório (portas). |
| Aplicação | `src/app/application/` | só o domínio | Casos de uso (`TransacaoService`, `ResumoService`, `CategoriaService`). Orquestram entidades e padrões. |
| Padrões | `src/app/patterns/` | domínio | Factory, Strategy, Observer — peças reutilizáveis de design. |
| Infraestrutura | `src/app/infrastructure/` | domínio | Adaptadores que implementam as portas: SQLite (produção) e memória (testes). |
| Interface (API) | `src/app/api/` | aplicação + domínio | FastAPI: rotas, schemas (DTOs) e *composition root* (injeção de dependência). |

## A regra de dependência na prática

O caso de uso `TransacaoService` recebe um `TransacaoRepository` —
**a interface abstrata do domínio**, não a implementação concreta:

```python
# application/servicos.py
def __init__(self, transacao_repo: TransacaoRepository, ...):
    self._transacao_repo = transacao_repo
```

Quem decide qual implementação concreta entra é o *composition root*
(`api/dependencias.py`), a camada mais externa. Resultado:

- O domínio e os casos de uso **não importam nada de infraestrutura nem de
  FastAPI**. Pode-se verificar: não há `import fastapi` fora de `api/`.
- Trocar memória → SQLite → PostgreSQL é trocar **uma classe** na infra e
  **uma linha** no composition root. Nenhuma regra de negócio muda.
- Testar regra de negócio não exige banco nem servidor (ver `tests/`).

## Decisões arquiteturais (ADRs)

As decisões estão registradas em [`/adrs`](../adrs/), incluindo uma decisão
que **evoluiu** ao longo do desenvolvimento (ADR-005: memória → SQLite
implementado → PostgreSQL como evolução futura) para evidenciar a evolução do
raciocínio arquitetural.

## Diagrama de fluxo de uma requisição

`POST /transacoes` (registrar uma despesa):

```
HTTP JSON
   │
   ▼
api/rotas.py ──valida com──► api/schemas.py (Pydantic)
   │
   ▼ (DTO)
application/TransacaoService.registrar()
   │  ├─► patterns/TransacaoFactory.criar()        (cria Receita/Despesa)
   │  ├─► domain/TransacaoRepository.salvar()       (porta → infra)
   │  └─► patterns/MonitorDeOrcamento.avaliar()     (Observer: alerta)
   ▼
api/rotas.py ──serializa──► TransacaoCriadaOut ──► HTTP 201 JSON
```
