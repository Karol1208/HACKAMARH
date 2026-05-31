from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from PIL import Image
from services.scanner_restauracao import ScannerRestauracao
from security import verificar_rate_limit

router = APIRouter(prefix="/scanner", tags=["scanner"])

@router.post("/muda")
async def analisar_muda(
    imagem: UploadFile = File(...),
    _: None = Depends(verificar_rate_limit),
):
    dados = await imagem.read()
    try:
        Image.open(BytesIO(dados)).verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida")
    scanner = ScannerRestauracao()
    return scanner.analisar(dados)
