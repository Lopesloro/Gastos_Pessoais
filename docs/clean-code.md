# Clean Code aplicado

Práticas de código limpo presentes no projeto, com exemplos reais.

## Nomes que revelam intenção
- `valor_no_fluxo` deixa claro que é o valor **com sinal** (positivo/negativo),
  não o valor bruto.
- `MonitorDeOrcamento.avaliar()` e `AlertaObserver.notificar()` descrevem
  exatamente o que fazem.
- Sem abreviações obscuras: `transacao`, `categoria`, `resumo_mensal`.

## Funções pequenas e com um nível de abstração
- `TransacaoService.registrar()` lê como uma narrativa: acha categoria → cria
  via Factory → salva → avalia orçamento. Os detalhes ficam em métodos
  auxiliares (`_total_despesas_do_mes`).
- Cada `ResumoStrategy.calcular()` faz uma coisa só.

## Sem números e textos mágicos
- O limite de orçamento é uma constante nomeada `LIMITE_MENSAL` no composition
  root, não um `2000` espalhado pelo código.
- Tipos de transação são um `Enum` (`TipoTransacao`), não strings soltas.

## Ausência de comentários redundantes
- O código é **autoexplicativo**: nomes descritivos e funções pequenas tornam
  comentários desnecessários. Não há comentários repetindo o que o código já
  diz — alinhado ao princípio de R. C. Martin de que o melhor comentário é o
  que você não precisou escrever porque o código já é claro.
- O "porquê" das decisões de design fica registrado na **documentação e nos
  ADRs**, não espalhado em comentários no código.

## Tratamento de erros próximo da borda
- As invariantes do domínio falham cedo (`__post_init__` valida valor > 0 e
  descrição não vazia).
- A camada `api/` traduz `ValueError` do domínio em `HTTP 422`, mantendo o
  domínio agnóstico de HTTP.

## Imutabilidade quando faz sentido
- `Categoria` é `@dataclass(frozen=True)`: identidade estável, menos espaço
  para bugs de estado compartilhado.

## DRY (Don't Repeat Yourself)
- A conversão entidade→DTO está centralizada em `_to_transacao_out()`,
  reutilizada por todas as rotas que devolvem transações.
- A lógica de "qual subclasse instanciar" existe **só** na `TransacaoFactory`.

## Código testável e testado
- 9 testes (`pytest -q`) cobrindo domínio, Factory, Observer, Strategy e API.
- Estrutura em camadas permite testes de unidade sem mocks complexos: basta
  injetar os repositórios em memória.

## Formatação e consistência
- `from __future__ import annotations` + type hints em toda a base.
- Organização previsível: uma responsabilidade por arquivo, imports ordenados.
