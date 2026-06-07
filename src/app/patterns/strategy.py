from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from decimal import Decimal

from ..domain.entidades import TipoTransacao, Transacao

class ResumoStrategy(ABC):
    @abstractmethod
    def calcular(self, transacoes: list[Transacao]) -> dict: ...

class ResumoMensalStrategy(ResumoStrategy):

    def __init__(self, mes: int, ano: int) -> None:
        self.mes = mes
        self.ano = ano

    def calcular(self, transacoes: list[Transacao]) -> dict:
        do_periodo = [
            t for t in transacoes if t.data.month == self.mes and t.data.year == self.ano
        ]
        receitas = sum(
            (t.valor for t in do_periodo if t.tipo == TipoTransacao.RECEITA),
            Decimal("0"),
        )
        despesas = sum(
            (t.valor for t in do_periodo if t.tipo == TipoTransacao.DESPESA),
            Decimal("0"),
        )
        return {
            "tipo_resumo": "mensal",
            "mes": self.mes,
            "ano": self.ano,
            "total_receitas": receitas,
            "total_despesas": despesas,
            "saldo": receitas - despesas,
            "quantidade_transacoes": len(do_periodo),
        }

class ResumoPorCategoriaStrategy(ResumoStrategy):

    def calcular(self, transacoes: list[Transacao]) -> dict:
        por_categoria: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        for t in transacoes:
            por_categoria[t.categoria.nome] += t.valor_no_fluxo

        return {
            "tipo_resumo": "por_categoria",
            "categorias": [
                {"categoria": nome, "saldo": saldo}
                for nome, saldo in sorted(por_categoria.items())
            ],
        }
