from datetime import datetime
from schemas import SolicitacaoCriar, SolicitacaoResposta
from connection import Conexao


class SolicitacoesService:
    """Gerencia o ciclo de vida das solicitações de acesso ao sistema Canindé."""

    def criar(self, dados: SolicitacaoCriar) -> SolicitacaoResposta:
        with Conexao() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO solicitacoes_acesso (nome, email, orgao, matricula, status) VALUES (%s, %s, %s, %s, 'pendente') RETURNING id, nome, email, orgao, matricula, status, criado_em",
                    (dados.nome, dados.email, dados.orgao, dados.matricula)
                )
                res = cur.fetchone()
                return SolicitacaoResposta(**res)

    def listar_pendentes(self) -> list[SolicitacaoResposta]:
        with Conexao() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nome, email, orgao, matricula, status, criado_em FROM solicitacoes_acesso WHERE status = 'pendente'")
                return [SolicitacaoResposta(**r) for r in cur.fetchall()]

    def aprovar(self, solicitacao_id: int) -> SolicitacaoResposta | None:
        with Conexao() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE solicitacoes_acesso SET status = 'aprovada' WHERE id = %s RETURNING id, nome, email, orgao, matricula, status, criado_em", (solicitacao_id,))
                res = cur.fetchone()
                if res:
                    return SolicitacaoResposta(**res)
        return None

    def rejeitar(self, solicitacao_id: int) -> SolicitacaoResposta | None:
        with Conexao() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE solicitacoes_acesso SET status = 'rejeitada' WHERE id = %s RETURNING id, nome, email, orgao, matricula, status, criado_em", (solicitacao_id,))
                res = cur.fetchone()
                if res:
                    return SolicitacaoResposta(**res)
        return None
