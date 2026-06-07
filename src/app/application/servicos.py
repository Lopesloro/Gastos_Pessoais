"""Casos de uso (camada de aplicação).

Orquestram entidades, repositórios e padrões para realizar as ações do
usuário. Dependem apenas de *abstrações* (interfaces de repositório), nunca
de implementações concretas — quem injeta o repositório concreto é a
camada de composição (api/dependencias.py). Isso é Inversão de Dependência
na prática e mantém os serviços testáveis isoladamente.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from ..domain.entidades import Categoria, TipoTransacao, Transacao
from ..domain.repositorios import CategoriaRepository, TransacaoRepository
from ..patterns.factory import TransacaoFactory
from ..patterns.observer import MonitorDeOrcamento
from ..patterns.strategy import (
    ResumoMensalStrategy,
    ResumoPorCategoriaStrategy,
    ResumoStrategy,
)


class CategoriaService:
    def __init__(self, repo: CategoriaRepository) -> None:
        self._repo = repo

    def criar(self, nome: str) -> Categoria:
        existente = self._repo.buscar_por_nome(nome)
        if existente:
            return existente
        return self._repo.salvar(Categoria(nome=nome.strip()))

    def listar(self) -> list[Categoria]:
        return self._repo.listar()


class TransacaoService:
    """Registra transações e dispara alertas de orçamento via Observer."""

    def __init__(
        self,
        transacao_repo: TransacaoRepository,
        categoria_repo: CategoriaRepository,
        monitor: MonitorDeOrcamento,
    ) -> None:
        self._transacao_repo = transacao_repo
        self._categoria_repo = categoria_repo
        self._monitor = monitor

    def registrar(
        self,
        tipo: TipoTransacao,
        descricao: str,
        valor: Decimal,
        nome_categoria: str,
        data: date | None = None,
    ) -> tuple[Transacao, bool]:
        """Registra a transação e avalia o orçamento do mês.

        Retorna a transação criada e um booleano indicando se o limite do mês
        foi estourado (alerta disparado).
        """
        categoria = self._categoria_repo.buscar_por_nome(nome_categoria)
        if categoria is None:
            categoria = self._categoria_repo.salvar(Categoria(nome=nome_categoria.strip()))

        # Factory decide a subclasse concreta (Receita/Despesa).
        transacao = TransacaoFactory.criar(tipo, descricao, valor, categoria, data)
        self._transacao_repo.salvar(transacao)

        alerta_disparado = False
        if transacao.tipo == TipoTransacao.DESPESA:
            total_gasto_mes = self._total_despesas_do_mes(transacao.data)
            alerta_disparado = self._monitor.avaliar(total_gasto_mes)

        return transacao, alerta_disparado

    def listar(self) -> list[Transacao]:
        return self._transacao_repo.listar()

    def _total_despesas_do_mes(self, dia: date) -> Decimal:
        return sum(
            (
                t.valor
                for t in self._transacao_repo.listar()
                if t.tipo == TipoTransacao.DESPESA
                and t.data.month == dia.month
                and t.data.year == dia.year
            ),
            Decimal("0"),
        )


class ResumoService:
    """Gera resumos delegando o cálculo à Strategy escolhida."""

    def __init__(self, transacao_repo: TransacaoRepository) -> None:
        self._transacao_repo = transacao_repo

    def gerar(self, strategy: ResumoStrategy) -> dict:
        return strategy.calcular(self._transacao_repo.listar())

    def resumo_mensal(self, mes: int, ano: int) -> dict:
        return self.gerar(ResumoMensalStrategy(mes, ano))

    def resumo_por_categoria(self) -> dict:
        return self.gerar(ResumoPorCategoriaStrategy())
