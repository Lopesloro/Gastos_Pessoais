"""Composition root: monta o grafo de objetos e injeta dependências.

É o único lugar que conhece as implementações concretas (repositórios em
memória, observers concretos). Todas as outras camadas recebem suas
dependências por construtor. Trocar o armazenamento ou os canais de alerta
significa mudar apenas este arquivo.
"""
from __future__ import annotations

from decimal import Decimal

from ..application.servicos import (
    CategoriaService,
    ResumoService,
    TransacaoService,
)
from ..infrastructure.repositorios_memoria import (
    CategoriaRepositoryMemoria,
    TransacaoRepositoryMemoria,
)
from ..patterns.observer import (
    AlertaColetorObserver,
    AlertaLogObserver,
    MonitorDeOrcamento,
)

# Limite mensal de despesas (orçamento). Em produção viria de configuração.
LIMITE_MENSAL = Decimal("2000.00")

# Instâncias únicas (singletons simples) que persistem durante a execução.
_categoria_repo = CategoriaRepositoryMemoria()
_transacao_repo = TransacaoRepositoryMemoria()

_coletor_alertas = AlertaColetorObserver()
_monitor = MonitorDeOrcamento(LIMITE_MENSAL)
_monitor.inscrever(AlertaLogObserver())
_monitor.inscrever(_coletor_alertas)


def get_categoria_service() -> CategoriaService:
    return CategoriaService(_categoria_repo)


def get_transacao_service() -> TransacaoService:
    return TransacaoService(_transacao_repo, _categoria_repo, _monitor)


def get_resumo_service() -> ResumoService:
    return ResumoService(_transacao_repo)
