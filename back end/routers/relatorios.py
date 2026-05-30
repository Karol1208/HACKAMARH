from fastapi import APIRouter

router = APIRouter(prefix="/relatorios", tags=["relatorios"])

_RELATORIOS = [
    {"id": 1, "titulo": "PRAD Consolidado — Maio 2026",    "descricao": "1.247 propriedades", "gerado_em": "30/05/2026", "tipo": "prad",    "icone": "file-text",  "cor": "cerrado"},
    {"id": 2, "titulo": "Selos Verdes B2B — Q1 2026",      "descricao": "452 produtores elegíveis", "gerado_em": "01/04/2026", "tipo": "selos",   "icone": "leaf",       "cor": "jalapao"},
    {"id": 3, "titulo": "Créditos de Carbono — Anual 2025","descricao": "12.400 tCO₂",        "gerado_em": "31/12/2025", "tipo": "carbono",  "icone": "bar-chart-2","cor": "river"},
    {"id": 4, "titulo": "Infrações Ambientais — Maio 2026","descricao": "8 autos lavrados",   "gerado_em": "29/05/2026", "tipo": "infracoes","icone": "alert-triangle","cor": "fire"},
]

@router.get("/kpis")
def kpis():
    # Mock — substituir por queries reais
    return {
        "area_restaurada_ha": 4280,
        "co2_sequestrado_t": 12400,
        "selos_verdes": 452,
        "creditos_carbono_brl": 2100000,
    }

@router.get("/")
def listar():
    return _RELATORIOS

@router.get("/{relatorio_id}/dados")
def dados_relatorio(relatorio_id: int):
    rel = next((r for r in _RELATORIOS if r["id"] == relatorio_id), None)
    if not rel:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    # Mock dos dados tabulares para download
    return {"relatorio": rel, "linhas": [
        {"campo": "Período", "valor": rel["gerado_em"]},
        {"campo": "Tipo",    "valor": rel["tipo"].upper()},
        {"campo": "Resumo",  "valor": rel["descricao"]},
        {"campo": "Status",  "valor": "Consolidado"},
    ]}
