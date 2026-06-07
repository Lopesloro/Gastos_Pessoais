"""Padrão GoF: Factory Method.

Centraliza a criação de transações. A camada de API recebe um `tipo` como
string ("RECEITA"/"DESPESA") e delega à fábrica a decisão de qual subclasse
concreta instanciar. Assim, quem chama não precisa conhecer Receita/Despesa,
e adicionar um novo tipo de transação no futuro exige mudar só a fábrica
(princípio aberto/fechado).
"""
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
        except KeyError as exc:  # pragma: no cover - proteção
            raise ValueError(f"Tipo de transação inválido: {tipo}") from exc

        return construtor(
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            data=data,
        )
