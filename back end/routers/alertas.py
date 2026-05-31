from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.alerta_cidadao import AlertaCidadao
from schemas import AlertaResposta
from datetime import datetime

router = APIRouter(prefix="/alertas", tags=["alertas"])

from connection import Conexao

@router.get("/total")
def total_alertas():
    try:
        with Conexao() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS total FROM alertas_sistema")
                row = cur.fetchone()
                return {"total": row["total"]}
    except Exception:
        return {"total": 0}

@router.get("/", response_model=list[AlertaResposta])
def listar_alertas():
    with Conexao() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, origem, titulo, descricao, porte_car, status_licenca, criado_em FROM alertas_sistema ORDER BY criado_em DESC")
            return [AlertaResposta(**r) for r in cur.fetchall()]

@router.post("/incendio")
async def reportar_incendio(imagem: UploadFile = File(...)):
    if not imagem.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")

    dados = await imagem.read()
    resultado = AlertaCidadao().processar_e_disparar(dados)

    if not resultado["sucesso"]:
        raise HTTPException(status_code=422, detail=resultado["motivo"])

    return resultado
