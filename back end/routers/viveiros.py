from fastapi import APIRouter, HTTPException, status
from connection import Conexao
import schemas
import random

router = APIRouter(prefix="/viveiros", tags=["viveiros"])

def get_conexao():
    return Conexao()

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

@router.post("/lotes", status_code=status.HTTP_201_CREATED)
def criar_lote(semeadura: schemas.SemeaduraCriar):
    with get_conexao() as conn:
        with conn.cursor() as cur:
            # Encontrar ou criar especie
            cur.execute("SELECT id FROM especies_nativas WHERE nome_popular = %s OR nome_cientifico = %s LIMIT 1", (semeadura.especie, semeadura.especie))
            esp = cur.fetchone()
            if not esp:
                cur.execute("INSERT INTO especies_nativas (nome_cientifico, nome_popular) VALUES (%s, %s) RETURNING id", (semeadura.especie + " (Cientifico)", semeadura.especie))
                esp_id = cur.fetchone()['id']
            else:
                esp_id = esp['id']

            # Encontrar ou criar viveiro
            cur.execute("SELECT id FROM viveiros WHERE nome = %s LIMIT 1", (semeadura.viveiro,))
            viv = cur.fetchone()
            if not viv:
                cur.execute("INSERT INTO viveiros (nome) VALUES (%s) RETURNING id", (semeadura.viveiro,))
                viv_id = cur.fetchone()['id']
            else:
                viv_id = viv['id']

            codigo = str(random.randint(100, 999))
            
            cur.execute("""
                INSERT INTO lotes_semeadura (codigo_lote, viveiro_id, especie_id, destino, estagio)
                VALUES (%s, %s, %s, %s, 'Em_Preparo') RETURNING id
            """, (codigo, viv_id, esp_id, semeadura.destino))
            lote_id = cur.fetchone()['id']
            
    return {"message": "Semeadura registrada", "id": lote_id}

@router.get("/board")
def board():
    # As solicitacoes e prontas vamos manter mockadas por agora, 
    # focando em 'em_preparo' que vem do banco.
    em_preparo = []
    
    with get_conexao() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT l.id, l.codigo_lote as lote, e.nome_popular as especie, v.nome as viveiro, 
                       l.destino, l.percentual_germinacao as germinacao_pct, l.dias_restantes
                FROM lotes_semeadura l
                JOIN viveiros v ON l.viveiro_id = v.id
                JOIN especies_nativas e ON l.especie_id = e.id
                WHERE l.estagio = 'Em_Preparo'
            """)
            em_preparo = cur.fetchall()

    return {
        "solicitacoes": [
            {"id": 1, "tipo": "PRAD Obrigatório", "nome": "Fazenda Boi Verde",
             "descricao": "500 mudas (Parkia platycephala e Ipê). Recuperação de APP.",
             "car": "TO-882...", "data": "Hoje"},
            {"id": 2, "tipo": "Plantio Voluntário", "nome": "Associação Quilombola",
             "descricao": "200 mudas frutíferas do Cerrado (Pequi e Buriti).",
             "car": "Região Jalapão", "data": "Ontem"},
        ],
        "em_preparo": em_preparo,
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
    with get_conexao() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE lotes_semeadura SET estagio = 'Pronto' WHERE id = %s", (lote_id,))
    return {"id": lote_id, "status": "pronta"}

@router.patch("/lotes/{lote_id}/dar-baixa")
def dar_baixa(lote_id: int):
    with get_conexao() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE lotes_semeadura SET estagio = 'Entregue' WHERE id = %s", (lote_id,))
    return {"id": lote_id, "status": "baixa_registrada"}
