"""Implementações de repositório com SQLite.

Adaptadores concretos que satisfazem as portas definidas em domain/repositorios.py.
O banco de dados é criado automaticamente em data/gastos.db na primeira execução.
O módulo sqlite3 é nativo do Python — sem dependências extras.
"""
from __future__ import annotations

import sqlite3
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from ..domain.entidades import Categoria, Despesa, Receita, TipoTransacao, Transacao
from ..domain.repositorios import CategoriaRepository, TransacaoRepository

DB_PATH = Path(__file__).parent.parent.parent.parent / "data" / "gastos.db"


def _conexao() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco() -> None:
    """Cria as tabelas se ainda não existirem."""
    with _conexao() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS categorias (
                id   TEXT PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS transacoes (
                id         TEXT PRIMARY KEY,
                tipo       TEXT NOT NULL CHECK (tipo IN ('RECEITA','DESPESA')),
                descricao  TEXT NOT NULL,
                valor      TEXT NOT NULL,
                categoria  TEXT NOT NULL REFERENCES categorias(nome),
                data       TEXT NOT NULL
            );
        """)


class CategoriaRepositorySQLite(CategoriaRepository):
    def salvar(self, categoria: Categoria) -> Categoria:
        with _conexao() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO categorias (id, nome) VALUES (?, ?)",
                (str(categoria.id), categoria.nome),
            )
        return categoria

    def listar(self) -> list[Categoria]:
        with _conexao() as conn:
            rows = conn.execute("SELECT id, nome FROM categorias ORDER BY nome").fetchall()
        return [Categoria(nome=r["nome"], id=UUID(r["id"])) for r in rows]

    def buscar_por_nome(self, nome: str) -> Categoria | None:
        with _conexao() as conn:
            row = conn.execute(
                "SELECT id, nome FROM categorias WHERE LOWER(nome) = LOWER(?)", (nome,)
            ).fetchone()
        return Categoria(nome=row["nome"], id=UUID(row["id"])) if row else None


class TransacaoRepositorySQLite(TransacaoRepository):
    def salvar(self, transacao: Transacao) -> Transacao:
        with _conexao() as conn:
            conn.execute(
                """INSERT INTO transacoes (id, tipo, descricao, valor, categoria, data)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    str(transacao.id),
                    transacao.tipo.value,
                    transacao.descricao,
                    str(transacao.valor),
                    transacao.categoria.nome,
                    transacao.data.isoformat(),
                ),
            )
        return transacao

    def listar(self) -> list[Transacao]:
        with _conexao() as conn:
            rows = conn.execute(
                """SELECT t.id, t.tipo, t.descricao, t.valor, t.data,
                          c.id as cat_id, c.nome as cat_nome
                   FROM transacoes t
                   JOIN categorias c ON c.nome = t.categoria
                   ORDER BY t.data DESC"""
            ).fetchall()

        resultado = []
        for r in rows:
            categoria = Categoria(nome=r["cat_nome"], id=UUID(r["cat_id"]))
            cls = Receita if r["tipo"] == TipoTransacao.RECEITA.value else Despesa
            resultado.append(
                cls(
                    descricao=r["descricao"],
                    valor=Decimal(r["valor"]),
                    categoria=categoria,
                    data=date.fromisoformat(r["data"]),
                    id=UUID(r["id"]),
                )
            )
        return resultado
