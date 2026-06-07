from datetime import date
from decimal import Decimal

import pytest

from src.app.application.servicos import ResumoService, TransacaoService
from src.app.domain.entidades import (
    Categoria,
    Despesa,
    Receita,
    TipoTransacao,
)
from src.app.infrastructure.repositorios_memoria import (
    CategoriaRepositoryMemoria,
    TransacaoRepositoryMemoria,
)
from src.app.patterns.factory import TransacaoFactory
from src.app.patterns.observer import (
    AlertaColetorObserver,
    MonitorDeOrcamento,
)

def test_valor_negativo_e_rejeitado():
    with pytest.raises(ValueError):
        Despesa(descricao="x", valor=Decimal("-1"), categoria=Categoria("Lazer"))

def test_valor_no_fluxo_tem_sinal_correto():
    cat = Categoria("Salário")
    assert Receita("Salário", Decimal("100"), cat).valor_no_fluxo == Decimal("100")
    assert Despesa("Mercado", Decimal("40"), cat).valor_no_fluxo == Decimal("-40")

def test_factory_cria_subclasse_correta():
    cat = Categoria("Transporte")
    receita = TransacaoFactory.criar(TipoTransacao.RECEITA, "Freela", Decimal("500"), cat)
    despesa = TransacaoFactory.criar(TipoTransacao.DESPESA, "Uber", Decimal("20"), cat)
    assert isinstance(receita, Receita)
    assert isinstance(despesa, Despesa)

def test_monitor_dispara_alerta_ao_estourar_limite():
    coletor = AlertaColetorObserver()
    monitor = MonitorDeOrcamento(Decimal("100"))
    monitor.inscrever(coletor)

    assert monitor.avaliar(Decimal("80")) is False
    assert monitor.avaliar(Decimal("150")) is True
    assert len(coletor.mensagens) == 1

def _service_com_dados():
    transacao_repo = TransacaoRepositoryMemoria()
    categoria_repo = CategoriaRepositoryMemoria()
    monitor = MonitorDeOrcamento(Decimal("1000"))
    service = TransacaoService(transacao_repo, categoria_repo, monitor)

    service.registrar(TipoTransacao.RECEITA, "Salário", Decimal("3000"), "Salário", date(2026, 6, 1))
    service.registrar(TipoTransacao.DESPESA, "Mercado", Decimal("400"), "Alimentação", date(2026, 6, 5))
    service.registrar(TipoTransacao.DESPESA, "Cinema", Decimal("60"), "Lazer", date(2026, 6, 7))
    return ResumoService(transacao_repo)

def test_resumo_mensal():
    resumo = _service_com_dados().resumo_mensal(6, 2026)
    assert resumo["total_receitas"] == Decimal("3000")
    assert resumo["total_despesas"] == Decimal("460")
    assert resumo["saldo"] == Decimal("2540")

def test_resumo_por_categoria():
    resumo = _service_com_dados().resumo_por_categoria()
    saldos = {c["categoria"]: c["saldo"] for c in resumo["categorias"]}
    assert saldos["Salário"] == Decimal("3000")
    assert saldos["Alimentação"] == Decimal("-400")
    assert saldos["Lazer"] == Decimal("-60")
