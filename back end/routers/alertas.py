from fastapi import APIRouter, HTTPException, UploadFile, File
from services.alerta_cidadao import AlertaCidadao

router = APIRouter(prefix="/alertas", tags=["alertas"])

@router.post("/incendio")
async def reportar_incendio(imagem: UploadFile = File(...)):
    if not imagem.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")

    dados = await imagem.read()
    resultado = AlertaCidadao().processar_e_disparar(dados)

    if not resultado["sucesso"]:
        raise HTTPException(status_code=422, detail=resultado["motivo"])

    return resultado
