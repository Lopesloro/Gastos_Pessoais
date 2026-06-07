# Atributos de Qualidade (ISO/IEC 25010:2023)

Dos oito atributos do modelo de qualidade de produto da ISO/IEC 25010:2023,
três foram eleitos como **prioritários** para este sistema. Para cada um:
justificativa da prioridade, decisões arquiteturais que o atendem e métrica
observável.

## 1º — Manutenibilidade (*Maintainability*)

**Por que é o nº 1 (e não outro).** Este é um projeto acadêmico cujo objetivo
declarado é *evoluir e demonstrar decisões de design*: novos relatórios, novos
tipos de transação e troca de armazenamento são esperados. Performance e
escalabilidade não são prioridade porque a carga é de um único usuário local —
otimizá-las seria esforço sem retorno. A manutenibilidade é o atributo que o
próprio enunciado da disciplina exercita.

**Decisões arquiteturais que respondem a ela.**
- Clean Architecture em camadas com a regra de dependência apontando para
  dentro (ADR-001): mudanças em infraestrutura não tocam o domínio.
- Padrões GoF (Factory, Strategy, Observer) isolam pontos de variação.
- SOLID, em especial Inversão de Dependência via repositórios abstratos.

**Métrica observável.** Adicionar um novo relatório (ex.: resumo anual) ou um
novo tipo de transação deve exigir alteração em **≤ 2 arquivos** e **nenhuma
modificação** em classes existentes (apenas adição). Hoje: novo relatório = 1
classe nova em `patterns/strategy.py`; novo tipo = 1 subclasse + 1 linha na
fábrica.

## 2º — Testabilidade (subcaracterística de Manutenibilidade)

**Por que é prioritário.** Para sustentar a evolução com segurança, é preciso
provar que as regras de negócio continuam corretas sem depender de
infraestrutura (banco, servidor). A testabilidade também é valorizada
explicitamente nos critérios de avaliação (Clean Code).

**Decisões arquiteturais que respondem a ela.**
- Serviços recebem repositórios pela **abstração** (interface), permitindo
  injetar implementações em memória nos testes.
- Domínio sem dependências de framework: entidades testáveis isoladamente.

**Métrica observável.** Cobertura das regras centrais (domínio, Factory,
Strategy, Observer e casos de uso) por testes automatizados que rodem **sem
banco e sem servidor**, em **< 5 s**. Hoje: **9 testes, ~1,7 s**, `pytest -q`.

## 3º — Confiabilidade (*Reliability*) — foco em alertas de orçamento

**Por que é prioritário.** A função de valor do sistema é ajudar o usuário a
não estourar o orçamento. Registrar uma despesa que ultrapassa o limite **sem
avisar** seria uma falha funcional silenciosa — pior do que um erro visível.

**Decisões arquiteturais que respondem a ela.**
- Padrão Observer (`MonitorDeOrcamento`): toda despesa registrada dispara a
  avaliação do orçamento do mês; o alerta é desacoplado do canal de entrega
  (ADR-004).
- Validação de invariantes no domínio (`valor > 0`, descrição não vazia),
  falhando cedo e de forma explícita (HTTP 422).

**Métrica observável.** Taxa de alertas perdidos = **0%**: toda despesa que faz
o total mensal exceder o limite deve disparar alerta. Verificado pelo teste
`test_monitor_dispara_alerta_ao_estourar_limite` e pelo campo
`alerta_orcamento` retornado em `POST /transacoes`.

---

## Atributos conscientemente despriorizados

| Atributo | Por que não é prioridade aqui |
|----------|-------------------------------|
| Performance / Eficiência | Um usuário local, dados em memória; latência já é desprezível. |
| Escalabilidade | Não há requisito de múltiplos usuários simultâneos no escopo. |
| Segurança | Sem dados sensíveis de terceiros nem multiusuário no escopo atual (autenticação fica registrada como evolução futura — ver doc de API). |
| Portabilidade | Atendida de graça pela abstração de repositório, mas não é o foco. |

## Trade-offs assumidos

| Decisão | Ganho (atributo favorecido) | Custo aceito |
|---------|-----------------------------|--------------|
| Armazenamento em memória | Simplicidade, testabilidade | Sem persistência entre execuções |
| Camadas + abstrações | Manutenibilidade, testabilidade | Mais arquivos/indireção num domínio pequeno |
| FastAPI/Pydantic na borda | Confiabilidade (validação), usabilidade da API | Acoplamento da camada `api/` ao framework (isolado) |
