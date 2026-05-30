from fastapi import APIRouter
from services.notificacoes import NotificacoesService
from schemas import NotificacaoResposta

router = APIRouter(prefix="/notificacoes", tags=["notificações"])

@router.get("/nao-lidas", response_model=list[NotificacaoResposta])
def listar_nao_lidas():
    return NotificacoesService().listar_nao_lidas()

@router.get("/nao-lidas/total")
def total_nao_lidas():
    return {"total": NotificacoesService().total_nao_lidas()}
