"""Interfaces (portas) de repositório.

Definir os repositórios como ABCs no domínio é a chave do princípio de
Inversão de Dependência (o "D" do SOLID): a camada de aplicação depende
desta abstração, e a infraestrutura é que se adapta a ela — nunca o
contrário. Trocar o armazenamento (memória, SQLite, PostgreSQL) não toca
nem o domínio nem os casos de uso.
"""
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
