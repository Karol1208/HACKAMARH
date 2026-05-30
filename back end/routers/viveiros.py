from fastapi import APIRouter

router = APIRouter(prefix="/viveiros", tags=["viveiros"])

@router.get("/kpis")
def kpis():
    # Mock — substituir por queries reais quando o banco estiver pronto
    return {
        "estoque_total": 145000,
        "prontas": 32400,
        "especie_mais_pedida": "Parkia platycephala",
        "especie_mais_pedida_popular": "Fava de Bolota",
        "alerta_especie": "Ipê Amarelo",
        "alerta_quantidade": 1200,
    }

@router.get("/board")
def board():
    return {
        "solicitacoes": [
            {"id": 1, "tipo": "PRAD Obrigatório", "nome": "Fazenda Boi Verde",
             "descricao": "500 mudas (Parkia platycephala e Ipê). Recuperação de APP.",
             "car": "TO-882...", "data": "Hoje"},
            {"id": 2, "tipo": "Plantio Voluntário", "nome": "Associação Quilombola",
             "descricao": "200 mudas frutíferas do Cerrado (Pequi e Buriti).",
             "car": "Região Jalapão", "data": "Ontem"},
        ],
        "em_preparo": [
            {"id": 10, "lote": "902", "especie": "Ipê Amarelo", "viveiro": "Palmas",
             "destino": "Múltiplos Produtores", "germinacao_pct": 45, "dias_restantes": 45},
        ],
        "prontas": [
            {"id": 20, "lote": "881", "especie": "Misto Cerrado", "viveiro": "Araguaína",
             "quantidade": 1200, "destino": "Faz. Rio Claro"},
        ],
    }

@router.patch("/solicitacoes/{solicitacao_id}/aprovar")
def aprovar_solicitacao(solicitacao_id: int):
    return {"id": solicitacao_id, "status": "aprovada"}

@router.patch("/solicitacoes/{solicitacao_id}/rejeitar")
def rejeitar_solicitacao(solicitacao_id: int):
    return {"id": solicitacao_id, "status": "rejeitada"}

@router.patch("/lotes/{lote_id}/mover-para-prontas")
def mover_para_prontas(lote_id: int):
    return {"id": lote_id, "status": "pronta"}

@router.patch("/lotes/{lote_id}/dar-baixa")
def dar_baixa(lote_id: int):
    return {"id": lote_id, "status": "baixa_registrada"}
