from fastapi import APIRouter
from services.mapa import MapaService
from schemas import PontoMapa, PoligonoMapa

router = APIRouter(prefix="/mapa", tags=["mapa"])

@router.get("/pontos", response_model=list[PontoMapa])
def obter_pontos():
    return MapaService().obter_pontos()

@router.get("/poligonos", response_model=list[PoligonoMapa])
def obter_poligonos():
    return MapaService().obter_poligonos()
