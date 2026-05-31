from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from PIL import Image
from services.alerta_cidadao import AlertaCidadao
from schemas import AlertaResposta
from connection import Conexao
from security import verificar_rate_limit

router = APIRouter(prefix="/alertas", tags=["alertas"])

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
async def reportar_incendio(
    imagem: UploadFile = File(...),
    _: None = Depends(verificar_rate_limit),
):
    dados = await imagem.read()
    try:
        Image.open(BytesIO(dados)).verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida")

    resultado = AlertaCidadao().processar_e_disparar(dados)

    if not resultado["sucesso"]:
        raise HTTPException(status_code=422, detail=resultado["motivo"])

    return resultado
