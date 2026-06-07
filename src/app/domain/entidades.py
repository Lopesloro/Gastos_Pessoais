"""Entidades do domínio.

Camada mais interna da Clean Architecture: não conhece banco de dados,
framework web ou qualquer detalhe de infraestrutura. Só regras de negócio.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4


class TipoTransacao(str, Enum):
    """Tipos possíveis de uma transação financeira."""

    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


@dataclass(frozen=True)
class Categoria:
    """Categoria de uma transação (ex.: Alimentação, Salário, Lazer).

    `frozen=True` torna a entidade imutável: uma vez criada, não muda de
    identidade. Isso reduz bugs e facilita o raciocínio sobre o estado.
    """

    nome: str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.nome or not self.nome.strip():
            raise ValueError("Categoria precisa de um nome.")


@dataclass
class Transacao:
    """Classe base de uma transação financeira.

    Subclasses (Receita/Despesa) definem o `tipo` e a regra de `valor_no_fluxo`,
    usada nos cálculos de resumo. Esse polimorfismo é o que permite que a camada
    de aplicação trate receitas e despesas de forma uniforme (princípio aberto/
    fechado e substituição de Liskov).
    """

    descricao: str
    valor: Decimal
    categoria: Categoria
    data: date = field(default_factory=date.today)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.valor <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
        if not self.descricao or not self.descricao.strip():
            raise ValueError("A transação precisa de uma descrição.")

    @property
    def tipo(self) -> TipoTransacao:  # pragma: no cover - sobrescrito
        raise NotImplementedError

    @property
    def valor_no_fluxo(self) -> Decimal:
        """Valor com sinal: positivo para receita, negativo para despesa."""
        raise NotImplementedError


@dataclass
class Receita(Transacao):
    @property
    def tipo(self) -> TipoTransacao:
        return TipoTransacao.RECEITA

    @property
    def valor_no_fluxo(self) -> Decimal:
        return self.valor


@dataclass
class Despesa(Transacao):
    @property
    def tipo(self) -> TipoTransacao:
        return TipoTransacao.DESPESA

    @property
    def valor_no_fluxo(self) -> Decimal:
        return -self.valor
