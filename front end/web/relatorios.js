function toast(msg, tipo) {
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;padding:12px 20px;border-radius:12px;font-size:14px;font-weight:700;color:white;box-shadow:0 10px 30px rgba(0,0,0,.2)';
    t.style.background = tipo === 'erro' ? '#D62828' : '#285430';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

function fmt(n) {
    if (n >= 1000000) return 'R$ ' + (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'k t';
    return n.toLocaleString('pt-BR');
}

// --- KPIs ---
async function carregarKPIs() {
    try {
        const d = await fetch(API + '/relatorios/kpis').then(r => r.json());
        document.getElementById('kpi-area').textContent    = d.area_restaurada_ha.toLocaleString('pt-BR') + ' ha';
        document.getElementById('kpi-co2').textContent     = (d.co2_sequestrado_t / 1000).toFixed(1) + 'k t';
        document.getElementById('kpi-selos').textContent   = d.selos_verdes.toLocaleString('pt-BR');
        document.getElementById('kpi-creditos').textContent = 'R$ ' + (d.creditos_carbono_brl / 1000000).toFixed(1) + 'M';
    } catch(e) {}
}

// --- Lista de relatórios ---
const COR = {
    cerrado: { bg: '#285430', light: 'rgba(40,84,48,0.1)', text: '#285430' },
    jalapao: { bg: '#D4A017', light: 'rgba(212,160,23,0.1)', text: '#D4A017' },
    river:   { bg: '#0077B6', light: 'rgba(0,119,182,0.1)', text: '#0077B6' },
    fire:    { bg: '#D62828', light: 'rgba(214,40,40,0.1)', text: '#D62828' },
};

async function carregarRelatorios() {
    const lista = document.getElementById('lista-relatorios');
    try {
        const relatorios = await fetch(API + '/relatorios/').then(r => r.json());
        lista.innerHTML = '';
        relatorios.forEach(rel => lista.appendChild(criarLinhaRelatorio(rel)));
        lucide.createIcons();
    } catch(e) {
        lista.innerHTML = '<div class="px-6 py-8 text-center text-gray-400 text-sm">API offline — sem relatórios</div>';
    }
}

function criarLinhaRelatorio(rel) {
    const cor = COR[rel.cor] || COR.cerrado;

    const row = document.createElement('div');
    row.className = 'px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition';

    const esq = document.createElement('div');
    esq.className = 'flex items-center gap-4';

    const iconeBox = document.createElement('div');
    iconeBox.className = 'w-10 h-10 rounded-xl flex items-center justify-center shrink-0';
    iconeBox.style.background = cor.light;
    iconeBox.style.color = cor.text;
    const ic = document.createElement('i');
    ic.setAttribute('data-lucide', rel.icone);
    ic.className = 'w-5 h-5';
    iconeBox.appendChild(ic);

    const info = document.createElement('div');
    const titulo = document.createElement('p');
    titulo.className = 'font-bold text-gray-900 text-sm';
    titulo.textContent = rel.titulo;
    const sub = document.createElement('p');
    sub.className = 'text-xs text-gray-500 mt-0.5';
    sub.textContent = rel.descricao + ' · Gerado em ' + rel.gerado_em;
    info.appendChild(titulo);
    info.appendChild(sub);

    esq.appendChild(iconeBox);
    esq.appendChild(info);

    const btn = document.createElement('button');
    btn.className = 'text-[#0077B6] text-xs font-bold bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg border border-blue-200 transition flex items-center gap-1.5';
    btn.onclick = () => baixarRelatorio(rel.id, rel.titulo);
    const icDown = document.createElement('i');
    icDown.setAttribute('data-lucide', 'download');
    icDown.className = 'w-3 h-3';
    btn.appendChild(icDown);
    btn.appendChild(document.createTextNode(' Baixar'));

    row.appendChild(esq);
    row.appendChild(btn);
    return row;
}

// --- Ações ---
async function baixarRelatorio(id, titulo) {
    try {
        const d = await fetch(API + '/relatorios/' + id + '/dados').then(r => r.json());
        const linhas = [['Campo', 'Valor'], ...d.linhas.map(l => [l.campo, l.valor])];
        const csv = linhas.map(r => r.join(';')).join('\n');
        const a = document.createElement('a');
        a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent('﻿' + csv);
        a.download = titulo.replace(/[^a-z0-9]/gi, '_') + '.csv';
        a.click();
        toast('Download iniciado: ' + titulo);
    } catch(e) { toast('Erro ao baixar relatório', 'erro'); }
}

// CSV — exporta KPIs + lista de relatórios em um arquivo .csv
async function exportarCSV() {
    toast('Gerando CSV...');
    try {
        const [kpis, relatorios] = await Promise.all([
            fetch(API + '/relatorios/kpis').then(r => r.json()),
            fetch(API + '/relatorios/').then(r => r.json()),
        ]);
        const linhas = [
            ['Secao', 'Campo', 'Valor'],
            ['KPIs', 'Area Restaurada (ha)', kpis.area_restaurada_ha],
            ['KPIs', 'CO2 Sequestrado (t)', kpis.co2_sequestrado_t],
            ['KPIs', 'Selos Verdes', kpis.selos_verdes],
            ['KPIs', 'Creditos de Carbono (BRL)', kpis.creditos_carbono_brl],
            ...relatorios.map(r => ['Relatorio', r.titulo, r.descricao + ' | Gerado em: ' + r.gerado_em]),
        ];
        const csv = linhas.map(r => r.join(';')).join('\n');
        const a = document.createElement('a');
        a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent('﻿' + csv);
        a.download = `Caninde_ESG_${new Date().getFullYear()}.csv`;
        a.click();
        toast('CSV exportado com sucesso!');
    } catch(e) { toast('Erro ao exportar CSV', 'erro'); }
}

// Baixar Dossiê por zona específica
async function baixarDossieZona(zona) {
    toast('Gerando dossiê da zona...');
    try {
        const res = await fetch(`${API}/relatorios/dossie?zona=${zona}`);
        if (!res.ok) throw new Error('status ' + res.status);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Dossie_Caninde_${zona}_${new Date().getFullYear()}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
        toast('Dossiê baixado com sucesso!');
    } catch(e) { toast('API offline — dossiê indisponível', 'erro'); }
}

// Exportar PDF — imprime a visão atual da página (KPIs + relatórios carregados)
function exportarPDF() {
    toast('Gerando PDF do relatório atual...');
    setTimeout(() => window.print(), 500);
}

// Baixar Dossiê PDF — documento consolidado por zonas gerado pelo servidor
async function baixarDossiePDF() {
    toast('Solicitando Dossiê Completo ao servidor...');
    try {
        const res = await fetch(API + '/relatorios/dossie');
        if (!res.ok) throw new Error('status ' + res.status);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Dossie_Caninde_' + new Date().getFullYear() + '.pdf';
        a.click();
        URL.revokeObjectURL(url);
        toast('Dossiê baixado com sucesso!');
    } catch(e) {
        toast('API offline — dossiê indisponível', 'erro');
    }
}


// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    carregarKPIs();
    carregarRelatorios();
});
