from datetime import datetime
from schemas import SolicitacaoCriar, SolicitacaoResposta


class SolicitacoesService:
    """Gerencia o ciclo de vida das solicitações de acesso ao sistema Canindé."""

    def criar(self, dados: SolicitacaoCriar) -> SolicitacaoResposta:
        # Mock — substituir por INSERT na tabela solicitacoes_acesso
        return SolicitacaoResposta(
            id=1,
            nome=dados.nome,
            email=dados.email,
            orgao=dados.orgao,
            matricula=dados.matricula,
            status="pendente",
            criado_em=datetime.utcnow(),
        )

    def listar_pendentes(self) -> list[SolicitacaoResposta]:
        # Mock — substituir por SELECT WHERE status = 'pendente'
        return []

    def aprovar(self, solicitacao_id: int) -> SolicitacaoResposta | None:
        # Mock — substituir por UPDATE status = 'aprovada' + criação do usuário no sistema
        return None

    def rejeitar(self, solicitacao_id: int) -> SolicitacaoResposta | None:
        # Mock — substituir por UPDATE status = 'rejeitada'
        return None
