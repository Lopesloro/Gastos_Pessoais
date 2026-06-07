"""Padrão GoF: Observer.

Quando uma despesa é registrada e o total do mês ultrapassa um limite
(orçamento), o sistema precisa avisar — mas o caso de uso que registra a
transação não deve saber *como* o aviso é entregue (log, e-mail, push...).

O `MonitorDeOrcamento` é o Subject: ele guarda observadores e os notifica.
Cada observador (`AlertaObserver`) reage do seu jeito. Acoplamento baixo:
adicionar um novo canal de alerta não muda o código que dispara o alerta.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from decimal import Decimal

logger = logging.getLogger("alertas")


class AlertaObserver(ABC):
    @abstractmethod
    def notificar(self, total_gasto: Decimal, limite: Decimal) -> None: ...


class AlertaLogObserver(AlertaObserver):
    """Registra o estouro de orçamento no log."""

    def notificar(self, total_gasto: Decimal, limite: Decimal) -> None:
        logger.warning(
            "ALERTA: gastos do mês (R$ %.2f) ultrapassaram o limite (R$ %.2f).",
            total_gasto,
            limite,
        )


class AlertaColetorObserver(AlertaObserver):
    """Guarda as mensagens em memória — útil para devolver na resposta da API
    e para asserts em testes, sem depender de e-mail/push reais."""

    def __init__(self) -> None:
        self.mensagens: list[str] = []

    def notificar(self, total_gasto: Decimal, limite: Decimal) -> None:
        self.mensagens.append(
            f"Limite de R$ {limite:.2f} estourado: gasto atual R$ {total_gasto:.2f}."
        )


class MonitorDeOrcamento:
    """Subject do Observer."""

    def __init__(self, limite_mensal: Decimal) -> None:
        self.limite_mensal = limite_mensal
        self._observadores: list[AlertaObserver] = []

    def inscrever(self, observador: AlertaObserver) -> None:
        self._observadores.append(observador)

    def avaliar(self, total_gasto_mes: Decimal) -> bool:
        """Notifica os observadores se o limite foi ultrapassado.

        Retorna True se houve estouro (e portanto alertas foram disparados).
        """
        if total_gasto_mes > self.limite_mensal:
            for observador in self._observadores:
                observador.notificar(total_gasto_mes, self.limite_mensal)
            return True
        return False
