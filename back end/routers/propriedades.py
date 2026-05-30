from fastapi import APIRouter, Query
from schemas import PropriedadeResposta

router = APIRouter(prefix="/propriedades", tags=["propriedades"])

@router.get("/busca", response_model=list[PropriedadeResposta])
def buscar(q: str = Query(..., min_length=2, description="Nº CAR ou município")):
    # Mock — substituir por query no banco filtrando numero_car ou municipio
    mock = [
        PropriedadeResposta(numero_car="TO-1720400-ABC123", municipio="Lagoa da Confusão", produtor="João Silva", porte="G"),
        PropriedadeResposta(numero_car="TO-1720400-DEF456", municipio="Palmas", produtor="Maria Santos", porte="M"),
        PropriedadeResposta(numero_car="TO-1720400-GHI789", municipio="Araguaína", produtor="Carlos Souza", porte="P"),
    ]
    return [p for p in mock if q.lower() in p.numero_car.lower() or q.lower() in p.municipio.lower()]
