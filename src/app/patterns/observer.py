from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from decimal import Decimal

logger = logging.getLogger("alertas")

class AlertaObserver(ABC):
    @abstractmethod
    def notificar(self, total_gasto: Decimal, limite: Decimal) -> None: ...

class AlertaLogObserver(AlertaObserver):

    def notificar(self, total_gasto: Decimal, limite: Decimal) -> None:
        logger.warning(
            "ALERTA: gastos do mês (R$ %.2f) ultrapassaram o limite (R$ %.2f).",
            total_gasto,
            limite,
        )

class AlertaColetorObserver(AlertaObserver):

    def __init__(self) -> None:
        self.mensagens: list[str] = []

    def notificar(self, total_gasto: Decimal, limite: Decimal) -> None:
        self.mensagens.append(
            f"Limite de R$ {limite:.2f} estourado: gasto atual R$ {total_gasto:.2f}."
        )

class MonitorDeOrcamento:

    def __init__(self, limite_mensal: Decimal) -> None:
        self.limite_mensal = limite_mensal
        self._observadores: list[AlertaObserver] = []

    def inscrever(self, observador: AlertaObserver) -> None:
        self._observadores.append(observador)

    def avaliar(self, total_gasto_mes: Decimal) -> bool:
        if total_gasto_mes > self.limite_mensal:
            for observador in self._observadores:
                observador.notificar(total_gasto_mes, self.limite_mensal)
            return True
        return False
