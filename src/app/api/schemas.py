"""Schemas de entrada/saída da API (DTOs com Pydantic).

Ficam na borda do sistema: convertem JSON <-> tipos. Mantêm o domínio
livre de detalhes do framework web — entidades não herdam de BaseModel.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from ..domain.entidades import TipoTransacao


class CategoriaIn(BaseModel):
    nome: str = Field(..., min_length=1, examples=["Alimentação"])


class CategoriaOut(BaseModel):
    id: UUID
    nome: str


class TransacaoIn(BaseModel):
    tipo: TipoTransacao
    descricao: str = Field(..., min_length=1, examples=["Almoço"])
    valor: Decimal = Field(..., gt=0, examples=["35.90"])
    categoria: str = Field(..., min_length=1, examples=["Alimentação"])
    data: date | None = None


class TransacaoOut(BaseModel):
    id: UUID
    tipo: TipoTransacao
    descricao: str
    valor: Decimal
    categoria: str
    data: date


class TransacaoCriadaOut(BaseModel):
    transacao: TransacaoOut
    alerta_orcamento: bool = Field(
        ..., description="True se esta despesa estourou o limite mensal."
    )
