from schemas import KPIs


class DashboardService:
    """Consolida os indicadores exibidos nos KPI cards do painel principal."""

    def obter_kpis(self) -> KPIs:
        # Mock — substituir por queries reais quando o banco estiver estruturado
        return KPIs(
            mudas_atestadas=1_200_000,
            sobrevivencia_pct=92.0,
            drones_ativos=14,
            infracoes_sem_licenca=3,
            selos_verdes=452,
        )
