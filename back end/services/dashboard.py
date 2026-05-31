from schemas import KPIs
from connection import Conexao

class DashboardService:
    """Consolida os indicadores exibidos nos KPI cards do painel principal."""

    def obter_kpis(self) -> KPIs:
        infracoes = 0
        with Conexao() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM alertas_sistema WHERE status_licenca = 'sem_licenca';")
                res = cur.fetchone()
                if res and 'count' in res:
                    infracoes = res['count']
                elif res:
                    # depending on RealDictCursor it could be count or fetchone()[0]
                    infracoes = list(res.values())[0]

        return KPIs(
            mudas_atestadas=1_200_000,
            sobrevivencia_pct=92.0,
            drones_ativos=14,
            infracoes_sem_licenca=infracoes,
            selos_verdes=452,
        )
