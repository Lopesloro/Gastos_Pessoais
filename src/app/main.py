"""Ponto de entrada da aplicação FastAPI."""
from __future__ import annotations

import logging

from fastapi import FastAPI

from .api.rotas import router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Controle de Gastos Pessoais",
    description=(
        "API REST para registrar receitas e despesas por categoria e ver "
        "resumos mensais. Projeto acadêmico demonstrando Clean Architecture, "
        "SOLID, Clean Code e padrões GoF (Factory, Strategy, Observer)."
    ),
    version="1.0.0",
)

app.include_router(router)


@app.get("/health", tags=["Infra"])
def health() -> dict:
    return {"status": "ok"}
