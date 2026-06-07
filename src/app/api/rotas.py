from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ..application.servicos import (
    CategoriaService,
    ResumoService,
    TransacaoService,
)
from ..domain.entidades import Transacao
from . import dependencias as deps
from .schemas import (
    CategoriaIn,
    CategoriaOut,
    TransacaoCriadaOut,
    TransacaoIn,
    TransacaoOut,
)

router = APIRouter()

def _to_transacao_out(t: Transacao) -> TransacaoOut:
    return TransacaoOut(
        id=t.id,
        tipo=t.tipo,
        descricao=t.descricao,
        valor=t.valor,
        categoria=t.categoria.nome,
        data=t.data,
    )

@router.post("/categorias", response_model=CategoriaOut, status_code=201, tags=["Categorias"])
def criar_categoria(
    body: CategoriaIn,
    service: CategoriaService = Depends(deps.get_categoria_service),
) -> CategoriaOut:
    categoria = service.criar(body.nome)
    return CategoriaOut(id=categoria.id, nome=categoria.nome)

@router.get("/categorias", response_model=list[CategoriaOut], tags=["Categorias"])
def listar_categorias(
    service: CategoriaService = Depends(deps.get_categoria_service),
) -> list[CategoriaOut]:
    return [CategoriaOut(id=c.id, nome=c.nome) for c in service.listar()]

@router.post(
    "/transacoes", response_model=TransacaoCriadaOut, status_code=201, tags=["Transações"]
)
def registrar_transacao(
    body: TransacaoIn,
    service: TransacaoService = Depends(deps.get_transacao_service),
) -> TransacaoCriadaOut:
    try:
        transacao, alerta = service.registrar(
            tipo=body.tipo,
            descricao=body.descricao,
            valor=body.valor,
            nome_categoria=body.categoria,
            data=body.data,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return TransacaoCriadaOut(
        transacao=_to_transacao_out(transacao),
        alerta_orcamento=alerta,
    )

@router.get("/transacoes", response_model=list[TransacaoOut], tags=["Transações"])
def listar_transacoes(
    service: TransacaoService = Depends(deps.get_transacao_service),
) -> list[TransacaoOut]:
    return [_to_transacao_out(t) for t in service.listar()]

@router.get("/resumo/mensal", tags=["Resumo"])
def resumo_mensal(
    mes: int = Query(..., ge=1, le=12),
    ano: int = Query(..., ge=2000, le=2100),
    service: ResumoService = Depends(deps.get_resumo_service),
) -> dict:
    return service.resumo_mensal(mes, ano)

@router.get("/resumo/por-categoria", tags=["Resumo"])
def resumo_por_categoria(
    service: ResumoService = Depends(deps.get_resumo_service),
) -> dict:
    return service.resumo_por_categoria()
