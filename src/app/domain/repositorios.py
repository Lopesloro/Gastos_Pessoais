from __future__ import annotations

from abc import ABC, abstractmethod

from .entidades import Categoria, Transacao

class CategoriaRepository(ABC):
    @abstractmethod
    def salvar(self, categoria: Categoria) -> Categoria: ...

    @abstractmethod
    def listar(self) -> list[Categoria]: ...

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Categoria | None: ...

class TransacaoRepository(ABC):
    @abstractmethod
    def salvar(self, transacao: Transacao) -> Transacao: ...

    @abstractmethod
    def listar(self) -> list[Transacao]: ...
