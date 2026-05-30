from fastapi import APIRouter
from services.dashboard import DashboardService
from schemas import KPIs

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/kpis", response_model=KPIs)
def obter_kpis():
    return DashboardService().obter_kpis()
