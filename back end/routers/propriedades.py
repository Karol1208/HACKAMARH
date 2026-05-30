from fastapi import APIRouter, Query, HTTPException
from schemas import PropriedadeResposta

router = APIRouter(prefix="/propriedades", tags=["propriedades"])

_PRODUTORES = [
    {"id": 1, "nome": "Agropecuária Vale S/A",  "car": "TO-49211288...", "status": "elegivel",  "ano_atual": 3, "total_anos": 5, "sobrevivencia_pct": 98,  "mudas_scan": 1200, "crescimento": "+0.8m / ano"},
    {"id": 2, "nome": "Fazenda Três Rios",       "car": "TO-11294422...", "status": "atrasado",  "ano_atual": 2, "total_anos": 5, "sobrevivencia_pct": 0,   "mudas_scan": 0,    "crescimento": None},
    {"id": 3, "nome": "Associação Nova Era",     "car": "14.552.122/...", "status": "pendente",  "ano_atual": 1, "total_anos": 5, "sobrevivencia_pct": 100, "mudas_scan": 200,  "crescimento": "Aguardando IA"},
    {"id": 4, "nome": "Sítio Boa Esperança",     "car": "TO-83920100...", "status": "elegivel",  "ano_atual": 5, "total_anos": 5, "sobrevivencia_pct": 87,  "mudas_scan": 800,  "crescimento": "+0.6m / ano"},
    {"id": 5, "nome": "Fazenda Cerrado Vivo",    "car": "TO-72810055...", "status": "pendente",  "ano_atual": 1, "total_anos": 5, "sobrevivencia_pct": 74,  "mudas_scan": 350,  "crescimento": "Aguardando IA"},
    {"id": 6, "nome": "Coop. Araguaia Verde",    "car": "TO-19283746...", "status": "atrasado",  "ano_atual": 4, "total_anos": 5, "sobrevivencia_pct": 0,   "mudas_scan": 0,    "crescimento": None},
]

@router.get("/")
def listar_produtores(status: str = Query(None)):
    # Mock — substituir por SELECT na tabela de produtores
    if status and status != "todos":
        return [p for p in _PRODUTORES if p["status"] == status]
    return _PRODUTORES

@router.post("/{produtor_id}/certificar")
def certificar(produtor_id: int):
    p = next((p for p in _PRODUTORES if p["id"] == produtor_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return {"id": produtor_id, "certificado": True, "mensagem": "Certificado CarbonTO emitido com sucesso"}

@router.post("/{produtor_id}/notificar")
def notificar(produtor_id: int):
    p = next((p for p in _PRODUTORES if p["id"] == produtor_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return {"id": produtor_id, "notificado": True, "mensagem": "Notificação enviada ao produtor"}

@router.post("/{produtor_id}/autuar")
def autuar(produtor_id: int):
    p = next((p for p in _PRODUTORES if p["id"] == produtor_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return {"id": produtor_id, "autuado": True, "mensagem": "Auto de infração gerado e registrado"}

@router.get("/busca", response_model=list[PropriedadeResposta])
def buscar(q: str = Query(..., min_length=2, description="Nº CAR ou município")):
    # Mock — substituir por query no banco filtrando numero_car ou municipio
    mock = [
        PropriedadeResposta(numero_car="TO-1720400-ABC123", municipio="Lagoa da Confusão", produtor="João Silva", porte="G"),
        PropriedadeResposta(numero_car="TO-1720400-DEF456", municipio="Palmas", produtor="Maria Santos", porte="M"),
        PropriedadeResposta(numero_car="TO-1720400-GHI789", municipio="Araguaína", produtor="Carlos Souza", porte="P"),
    ]
    return [p for p in mock if q.lower() in p.numero_car.lower() or q.lower() in p.municipio.lower()]
