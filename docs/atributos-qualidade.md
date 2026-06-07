# Atributos de Qualidade

Atributos priorizados para este projeto, justificativa da prioridade e como a
arquitetura/código os atendem de forma **demonstrável**.

| Prioridade | Atributo | Por que importa aqui | Como foi atendido |
|-----------|----------|----------------------|-------------------|
| 1 | **Manutenibilidade** | Trabalho acadêmico que precisa evoluir (novos relatórios, novos tipos de transação, troca de banco). | Clean Architecture + SOLID + padrões GoF isolam mudanças. Ex.: novo relatório = nova `ResumoStrategy`, sem tocar no que existe. |
| 2 | **Testabilidade** | Provar que as regras funcionam sem depender de infra. | Inversão de dependência: serviços recebem repositórios abstratos. 9 testes rodam sem banco nem servidor (`pytest -q`). |
| 3 | **Modificabilidade / Portabilidade** | Requisito do enunciado de poder trocar o armazenamento. | Repositórios são portas (ABC). Trocar memória→PostgreSQL afeta 1 classe + 1 linha (ADR-005). |
| 4 | **Confiabilidade / Alertas** | Estourar o orçamento sem aviso seria uma falha funcional. | Padrão Observer (`MonitorDeOrcamento`) notifica ao ultrapassar o limite; coberto por teste. |
| 5 | **Usabilidade (DX/API)** | A API precisa ser clara para quem consome. | FastAPI gera Swagger/OpenAPI automático em `/docs`; DTOs com exemplos; validação com mensagens HTTP 422. |

## Como cada atributo é evidenciado

### Manutenibilidade e Modificabilidade
- **Cenário:** adicionar "resumo anual".
  **Esforço:** criar `ResumoAnualStrategy` em `patterns/strategy.py` e expor uma
  rota. Zero alteração em entidades, repositórios ou nos outros resumos.
- **Cenário:** adicionar tipo de transação "Investimento".
  **Esforço:** nova subclasse + uma entrada no dicionário da `TransacaoFactory`.

### Testabilidade
- `tests/test_dominio_e_padroes.py` injeta `*RepositoryMemoria` e testa regra
  pura. `tests/test_api.py` usa `TestClient` sem subir servidor real.

### Confiabilidade (alertas)
- `test_monitor_dispara_alerta_ao_estourar_limite` prova o comportamento do
  Observer; o campo `alerta_orcamento` na resposta de `POST /transacoes`
  expõe isso ao cliente.

## Trade-offs assumidos

| Decisão | Ganho | Custo aceito |
|---------|-------|--------------|
| Armazenamento em memória | Simplicidade, projeto roda na hora, foco em arquitetura | Dados não persistem entre execuções (aceitável no escopo acadêmico) |
| Camadas + abstrações | Manutenibilidade e testabilidade altas | Mais arquivos/indireção para um domínio pequeno |
| FastAPI/Pydantic na borda | Validação e docs grátis | Acoplamento da camada `api/` ao framework (isolado, não vaza para o domínio) |
