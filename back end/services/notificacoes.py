from datetime import datetime
from schemas import NotificacaoResposta


class NotificacoesService:
    """Gerencia o feed de notificações do painel administrativo."""

    def listar_nao_lidas(self) -> list[NotificacaoResposta]:
        # Mock — virá da tabela de notificações vinculada aos alertas gerados
        return [
            NotificacaoResposta(
                id=1,
                titulo="Foco de calor confirmado em Lagoa da Confusão",
                tipo="alerta",
                lida=False,
                criado_em=datetime(2026, 5, 30, 10, 0),
            ),
            NotificacaoResposta(
                id=2,
                titulo="Licença vencida detectada — Supressão Vegetal (Sweep)",
                tipo="infração",
                lida=False,
                criado_em=datetime(2026, 5, 30, 9, 45),
            ),
            NotificacaoResposta(
                id=3,
                titulo="Atestado PRAD aprovado — Lote Viveiro Palmas",
                tipo="aprovacao",
                lida=False,
                criado_em=datetime(2026, 5, 30, 9, 0),
            ),
        ]

    def total_nao_lidas(self) -> int:
        return len(self.listar_nao_lidas())
