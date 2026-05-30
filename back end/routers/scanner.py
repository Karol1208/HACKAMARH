from fastapi import APIRouter, HTTPException, UploadFile, File
from services.scanner_restauracao import ScannerRestauracao

router = APIRouter(prefix="/scanner", tags=["scanner"])

@router.post("/muda")
async def analisar_muda(imagem: UploadFile = File(...)):
    if not imagem.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")

    dados = await imagem.read()
    scanner = ScannerRestauracao()
    return scanner.analisar(dados)
