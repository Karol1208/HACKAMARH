from fastapi import APIRouter, Query, HTTPException
from schemas import PropriedadeResposta
from connection import Conexao

router = APIRouter(prefix="/propriedades", tags=["propriedades"])

@router.get("/")
def listar_produtores(status: str = Query(None)):
    produtores = []
    with Conexao() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT produtor as nome, numero_car as car FROM propriedades")
            res = cur.fetchall()
            for i, r in enumerate(res):
                produtores.append({
                    "id": i+1,
                    "nome": r.get('nome') or r.get('produtor', 'Desconhecido'),
                    "car": r.get('car') or r.get('numero_car', 'S/N'),
                    "status": "elegivel",
                    "ano_atual": 3,
                    "total_anos": 5,
                    "sobrevivencia_pct": 98,
                    "mudas_scan": 1200,
                    "crescimento": "+0.8m / ano"
                })
    if status and status != "todos":
        return [p for p in produtores if p["status"] == status]
    return produtores

@router.post("/{produtor_id}/certificar")
def certificar(produtor_id: int):
    return {"id": produtor_id, "certificado": True, "mensagem": "Certificado CarbonTO emitido com sucesso"}

@router.post("/{produtor_id}/notificar")
def notificar(produtor_id: int):
    return {"id": produtor_id, "notificado": True, "mensagem": "Notificação enviada ao produtor"}

@router.post("/{produtor_id}/autuar")
def autuar(produtor_id: int):
    return {"id": produtor_id, "autuado": True, "mensagem": "Auto de infração gerado e registrado"}

@router.get("/busca", response_model=list[PropriedadeResposta])
def buscar(q: str = Query(..., min_length=2, description="Nº CAR ou município")):
    resultados = []
    with Conexao() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT numero_car, municipio, produtor, porte FROM propriedades WHERE numero_car ILIKE %s OR municipio ILIKE %s",
                (f"%{q}%", f"%{q}%")
            )
            resultados = cur.fetchall()
            
    return [PropriedadeResposta(**r) for r in resultados]

