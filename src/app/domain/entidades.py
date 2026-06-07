from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

class TipoTransacao(str, Enum):

    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

@dataclass(frozen=True)
class Categoria:

    nome: str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.nome or not self.nome.strip():
            raise ValueError("Categoria precisa de um nome.")

@dataclass
class Transacao:

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
    def tipo(self) -> TipoTransacao:
        raise NotImplementedError

    @property
    def valor_no_fluxo(self) -> Decimal:
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
