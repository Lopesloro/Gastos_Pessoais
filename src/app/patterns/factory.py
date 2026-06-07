from __future__ import annotations

from datetime import date
from decimal import Decimal

from ..domain.entidades import (
    Categoria,
    Despesa,
    Receita,
    TipoTransacao,
    Transacao,
)

class TransacaoFactory:
    @staticmethod
    def criar(
        tipo: TipoTransacao,
        descricao: str,
        valor: Decimal,
        categoria: Categoria,
        data: date | None = None,
    ) -> Transacao:
        data = data or date.today()
        construtores = {
            TipoTransacao.RECEITA: Receita,
            TipoTransacao.DESPESA: Despesa,
        }
        try:
            construtor = construtores[tipo]
        except KeyError as exc:
            raise ValueError(f"Tipo de transação inválido: {tipo}") from exc

        return construtor(
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            data=data,
        )
