# SOLID aplicado

Cada princípio com **onde** está no código e **por que** o exemplo se encaixa.

## S — Single Responsibility (Responsabilidade Única)

> Uma classe deve ter um, e apenas um, motivo para mudar.

- `CategoriaRepositoryMemoria` só persiste categorias.
- `TransacaoService` só orquestra o registro de transações.
- `ResumoMensalStrategy` só calcula o resumo mensal.

Os DTOs (`api/schemas.py`) separam a representação HTTP das entidades de
negócio (`domain/entidades.py`): mudar o JSON da API não altera a regra de
negócio, e vice-versa. São motivos de mudança diferentes, em classes
diferentes.

## O — Open/Closed (Aberto/Fechado)

> Aberto para extensão, fechado para modificação.

`patterns/strategy.py`: para adicionar um novo relatório, cria-se uma nova
classe que implementa `ResumoStrategy`. O `ResumoService` **não muda**:

```python
class ResumoService:
    def gerar(self, strategy: ResumoStrategy) -> dict:
        return strategy.calcular(self._transacao_repo.listar())
```

O mesmo vale para a `TransacaoFactory`: novos tipos de transação entram pelo
dicionário de construtores, sem reescrever a lógica existente.

## L — Liskov Substitution (Substituição de Liskov)

> Subtipos devem ser substituíveis por seus tipos base sem quebrar o programa.

`Receita` e `Despesa` são `Transacao`. Qualquer código que recebe `Transacao`
(repositórios, estratégias de resumo) funciona com ambas, pois ambas honram o
contrato `tipo` e `valor_no_fluxo`. A diferença está só no **sinal** do valor:

```python
Receita(...).valor_no_fluxo  #  +valor
Despesa(...).valor_no_fluxo  #  -valor
```

`ResumoPorCategoriaStrategy` soma `valor_no_fluxo` sem perguntar o tipo
concreto — substituição de Liskov pura.

## I — Interface Segregation (Segregação de Interface)

> Clientes não devem depender de métodos que não usam.

As portas são pequenas e focadas. `CategoriaRepository` e
`TransacaoRepository` são **interfaces separadas** em vez de um
"RepositorioGigante". O `AlertaObserver` expõe um único método (`notificar`).
Cada cliente depende só do que precisa.

## D — Dependency Inversion (Inversão de Dependência)

> Módulos de alto nível não devem depender de módulos de baixo nível; ambos
> dependem de abstrações.

O caso de uso (alto nível) depende da **abstração** `TransacaoRepository`
(definida no domínio), não da classe concreta de infraestrutura:

```python
# application/servicos.py  (alto nível)
def __init__(self, transacao_repo: TransacaoRepository): ...

# infrastructure/repositorios_memoria.py  (baixo nível)
class TransacaoRepositoryMemoria(TransacaoRepository): ...

# api/dependencias.py  (composition root injeta a concreta)
TransacaoService(_transacao_repo, _categoria_repo, _monitor)
```

É esse princípio que torna o ADR-005 (trocar o banco) barato e os testes
independentes de infraestrutura.
