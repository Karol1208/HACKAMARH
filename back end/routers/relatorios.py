import io
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from fpdf import FPDF

router = APIRouter(prefix="/relatorios", tags=["relatorios"])

_RELATORIOS = [
    {"id": 1, "titulo": "PRAD Consolidado — Maio 2026",    "descricao": "1.247 propriedades", "gerado_em": "30/05/2026", "tipo": "prad",    "icone": "file-text",  "cor": "cerrado"},
    {"id": 2, "titulo": "Selos Verdes B2B — Q1 2026",      "descricao": "452 produtores elegíveis", "gerado_em": "01/04/2026", "tipo": "selos",   "icone": "leaf",       "cor": "jalapao"},
    {"id": 3, "titulo": "Créditos de Carbono — Anual 2025","descricao": "12.400 tCO₂",        "gerado_em": "31/12/2025", "tipo": "carbono",  "icone": "bar-chart-2","cor": "river"},
    {"id": 4, "titulo": "Infrações Ambientais — Maio 2026","descricao": "8 autos lavrados",   "gerado_em": "29/05/2026", "tipo": "infracoes","icone": "alert-triangle","cor": "fire"},
]

_ZONAS = [
    {"slug": "tocantins", "nome": "Bacia do Rio Tocantins (APPs)", "dados": "14.5 MB · 24 Drones Envolvidos"},
    {"slug": "jalapao",   "nome": "Parque Estadual do Jalapão",    "dados": "8.2 MB · Imagens de Satélite (Planet)"},
]

@router.get("/dossie")
def dossie_completo(zona: Optional[str] = Query(None, description="Slug da zona: 'tocantins' ou 'jalapao'")):
    zona_filtro = next((z for z in _ZONAS if z["slug"] == zona), None) if zona else None
    kpi = {
        "area_restaurada_ha": 4280,
        "co2_sequestrado_t": 12400,
        "selos_verdes": 452,
        "creditos_carbono_brl": 2100000,
    }

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Cabeçalho
    pdf.set_fill_color(40, 84, 48)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, "Projeto Caninde - SEMARH / TO", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(10, 20)
    subtitulo = f"Dossie: {zona_filtro['nome']}" if zona_filtro else "Dossie Completo de Impacto GCF"
    pdf.cell(0, 6, f"{subtitulo}  |  Gerado em {date.today().strftime('%d/%m/%Y')}")

    pdf.set_text_color(30, 30, 30)
    pdf.ln(20)

    # KPIs
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_fill_color(240, 248, 240)
    pdf.cell(0, 8, "Indicadores ESG (Ano Base 2026)", ln=True, fill=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"  Area Restaurada:     {kpi['area_restaurada_ha']:,} ha".replace(",", "."), ln=True)
    pdf.cell(0, 7, f"  CO2 Sequestrado:     {kpi['co2_sequestrado_t']:,} t".replace(",", "."), ln=True)
    pdf.cell(0, 7, f"  Selos Verdes:        {kpi['selos_verdes']:,} produtores elegíveis".replace(",", "."), ln=True)
    pdf.cell(0, 7, f"  Creditos de Carbono: R$ {kpi['creditos_carbono_brl']/1_000_000:.1f}M", ln=True)
    pdf.ln(5)

    # Relatórios
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_fill_color(240, 248, 240)
    pdf.cell(0, 8, "Relatorios Consolidados", ln=True, fill=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    for rel in _RELATORIOS:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, f"  {rel['titulo']}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"    {rel['descricao']}  |  Gerado em: {rel['gerado_em']}", ln=True)
        pdf.ln(1)
    pdf.ln(4)

    # Zonas de Impacto
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_fill_color(240, 248, 240)
    pdf.cell(0, 8, "Zonas de Impacto Geografico", ln=True, fill=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    zonas_exibir = [zona_filtro] if zona_filtro else _ZONAS
    for z in zonas_exibir:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, f"  {z['nome']}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"    {z['dados']}", ln=True)
        pdf.ln(1)

    # Rodapé
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "Dados auditaveis e criptografados via Blockchain — Projeto Caninde / SEMARH-TO", ln=True, align="C")

    buf = io.BytesIO(pdf.output())
    slug_nome = f"_{zona_filtro['slug']}" if zona_filtro else ""
    filename = f"Dossie_Caninde{slug_nome}_{date.today().year}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

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
