"""Testes de integração da API com o TestClient do FastAPI.

Os testes de API usam um banco SQLite temporário isolado para não acumular
dados entre execuções — efeito colateral natural da migração de memória→SQLite.
"""
import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def banco_temporario(tmp_path, monkeypatch):
    """Redireciona DB_PATH para um arquivo temporário em cada teste."""
    db_temp = tmp_path / "test.db"
    import src.app.infrastructure.repositorios_sqlite as mod
    monkeypatch.setattr(mod, "DB_PATH", db_temp)
    # Reinicializa o banco no caminho temporário
    mod.inicializar_banco()
    # Reinicializa os repositórios e o composition root para usar o novo caminho
    import src.app.api.dependencias as deps
    deps._categoria_repo = mod.CategoriaRepositorySQLite()
    deps._transacao_repo = mod.TransacaoRepositorySQLite()
    yield


from src.app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_fluxo_basico_de_transacao_e_resumo():
    r1 = client.post(
        "/transacoes",
        json={"tipo": "RECEITA", "descricao": "Salário", "valor": "3000",
              "categoria": "Salário", "data": "2026-06-01"},
    )
    assert r1.status_code == 201
    assert r1.json()["alerta_orcamento"] is False

    r2 = client.post(
        "/transacoes",
        json={"tipo": "DESPESA", "descricao": "Mercado", "valor": "400",
              "categoria": "Alimentação", "data": "2026-06-05"},
    )
    assert r2.status_code == 201

    resumo = client.get("/resumo/mensal", params={"mes": 6, "ano": 2026}).json()
    assert resumo["total_receitas"] == "3000"
    assert resumo["total_despesas"] == "400"


def test_valor_invalido_retorna_422():
    r = client.post(
        "/transacoes",
        json={"tipo": "DESPESA", "descricao": "x", "valor": "-5", "categoria": "Lazer"},
    )
    assert r.status_code == 422
