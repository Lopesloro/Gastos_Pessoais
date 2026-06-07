from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from .api.rotas import router

STATIC_DIR = Path(__file__).parent / "static"

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

app.include_router(router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health", tags=["Infra"])
def health() -> dict:
    return {"status": "ok"}
