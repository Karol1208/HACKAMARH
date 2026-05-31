from fastapi import APIRouter, Depends, HTTPException
from services.solicitacoes import SolicitacoesService
from schemas import SolicitacaoCriar, SolicitacaoResposta
from security import verificar_chave_admin

router = APIRouter(prefix="/solicitacoes", tags=["solicitações de acesso"])

@router.post("/", response_model=SolicitacaoResposta, status_code=201)
def solicitar_acesso(dados: SolicitacaoCriar):
    return SolicitacoesService().criar(dados)

@router.get("/pendentes", response_model=list[SolicitacaoResposta], dependencies=[Depends(verificar_chave_admin)])
def listar_pendentes():
    return SolicitacoesService().listar_pendentes()

@router.patch("/{solicitacao_id}/aprovar", response_model=SolicitacaoResposta, dependencies=[Depends(verificar_chave_admin)])
def aprovar(solicitacao_id: int):
    resultado = SolicitacoesService().aprovar(solicitacao_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return resultado

@router.patch("/{solicitacao_id}/rejeitar", response_model=SolicitacaoResposta, dependencies=[Depends(verificar_chave_admin)])
def rejeitar(solicitacao_id: int):
    resultado = SolicitacoesService().rejeitar(solicitacao_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return resultado
