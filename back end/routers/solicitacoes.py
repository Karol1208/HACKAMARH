from fastapi import APIRouter, HTTPException
from services.solicitacoes import SolicitacoesService
from schemas import SolicitacaoCriar, SolicitacaoResposta

router = APIRouter(prefix="/solicitacoes", tags=["solicitações de acesso"])

@router.post("/", response_model=SolicitacaoResposta, status_code=201)
def solicitar_acesso(dados: SolicitacaoCriar):
    return SolicitacoesService().criar(dados)

@router.get("/pendentes", response_model=list[SolicitacaoResposta])
def listar_pendentes():
    return SolicitacoesService().listar_pendentes()

@router.patch("/{solicitacao_id}/aprovar", response_model=SolicitacaoResposta)
def aprovar(solicitacao_id: int):
    resultado = SolicitacoesService().aprovar(solicitacao_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return resultado

@router.patch("/{solicitacao_id}/rejeitar", response_model=SolicitacaoResposta)
def rejeitar(solicitacao_id: int):
    resultado = SolicitacoesService().rejeitar(solicitacao_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return resultado
