from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.alerta_cidadao import AlertaCidadao
from schemas import AlertaResposta
from datetime import datetime

router = APIRouter(prefix="/alertas", tags=["alertas"])

@router.get("/", response_model=list[AlertaResposta])
def listar_alertas():
    # Mock — substituir por SELECT na tabela de alertas quando o banco estiver pronto
    return [
        AlertaResposta(id=1, origem="app_cidadao", titulo="Foco de Calor Confirmado",
            descricao="Denúncia georreferenciada no município de Lagoa da Confusão. Protege (Bombeiros) acionado.",
            porte_car="G", status_licenca="sem_licenca", criado_em=datetime(2026, 5, 30, 14, 32)),
        AlertaResposta(id=2, origem="planet_labs", titulo="Supressão Vegetal (Sweep)",
            descricao="Alteração de biomassa detectada. Status da Licença: VENCIDA. Auto de infração em rascunho.",
            porte_car="M", status_licenca="vencida", criado_em=datetime(2026, 5, 30, 14, 15)),
        AlertaResposta(id=3, origem="app_produtor", titulo="Atestado PRAD Aprovado",
            descricao="Lote Viveiro Palmas atingiu 1.5m. Curva de crescimento atestada por IA.",
            porte_car="P", status_licenca="aprovado", criado_em=datetime(2026, 5, 30, 13, 32)),
    ]

@router.post("/incendio")
async def reportar_incendio(imagem: UploadFile = File(...)):
    if not imagem.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")

    dados = await imagem.read()
    resultado = AlertaCidadao().processar_e_disparar(dados)

    if not resultado["sucesso"]:
        raise HTTPException(status_code=422, detail=resultado["motivo"])

    return resultado
