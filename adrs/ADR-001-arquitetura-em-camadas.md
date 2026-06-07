# ADR-001 — Adotar Clean Architecture em camadas

- **Status:** Aceito
- **Data:** 2026-06-01

## Contexto
O projeto precisa ser manutenível, testável e permitir trocar o mecanismo de
armazenamento (requisito da disciplina). Um design "tudo nas rotas"
(controllers gordos) acoplaria regra de negócio ao framework web e ao banco.

## Decisão
Adotar **Clean Architecture** com quatro camadas (domínio, aplicação,
infraestrutura, interface) e a **regra de dependência** apontando para dentro.
As interfaces de repositório (portas) ficam no domínio; a infraestrutura as
implementa.

## Consequências
**Positivas:** baixo acoplamento, testes sem infra, troca de banco barata,
SOLID naturalmente atendido (sobretudo o "D").
**Negativas:** mais arquivos e indireção para um domínio pequeno — custo
aceito em troca de manutenibilidade e clareza didática.

## Alternativas consideradas
- *Arquitetura em script único / MVC com controllers gordos*: mais rápido de
  escrever, mas acopla tudo e prejudica testabilidade. Rejeitada.
