from __future__ import annotations

from ..domain.entidades import Categoria, Transacao
from ..domain.repositorios import CategoriaRepository, TransacaoRepository

class CategoriaRepositoryMemoria(CategoriaRepository):
    def __init__(self) -> None:
        self._dados: dict[str, Categoria] = {}

    def salvar(self, categoria: Categoria) -> Categoria:
        self._dados[categoria.nome.lower()] = categoria
        return categoria

    def listar(self) -> list[Categoria]:
        return list(self._dados.values())

    def buscar_por_nome(self, nome: str) -> Categoria | None:
        return self._dados.get(nome.lower())

class TransacaoRepositoryMemoria(TransacaoRepository):
    def __init__(self) -> None:
        self._dados: list[Transacao] = []

    def salvar(self, transacao: Transacao) -> Transacao:
        self._dados.append(transacao)
        return transacao

    def listar(self) -> list[Transacao]:
        return list(self._dados)
