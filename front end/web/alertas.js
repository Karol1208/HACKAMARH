const API = 'http://127.0.0.1:8000';

let todosAlertas = [];
let filtroRisco = 'Todos os Riscos';
let filtroPorte = 'Qualquer Porte';

function tempoRelativo(iso) {
    const diff = Math.floor((Date.now() - new Date(iso)) / 60000);
    if (diff < 1) return 'Agora';
    if (diff < 60) return `Há ${diff}m`;
    return `Há ${Math.floor(diff / 60)}h`;
}

const ORIGEM = {
    app_cidadao:  { label: 'App Cidadão',  icon: 'smartphone', cor: '#D62828', bg: '#FEF2F2' },
    planet_labs:  { label: 'Planet Labs',  icon: 'satellite',  cor: '#D97706', bg: '#FFFBEB' },
    app_produtor: { label: 'App Produtor', icon: 'scan',       cor: '#285430', bg: '#F0FDF4' },
};

const STATUS_BADGE = {
    sem_licenca: `<span class="badge-danger px-2.5 py-1 rounded text-[10px] font-bold uppercase">Urgente - Fogo</span>`,
    vencida:     `<span class="badge-warning px-2.5 py-1 rounded text-[10px] font-bold uppercase">Desmate S/ Licença</span>`,
    ativa:       `<span class="badge-success px-2.5 py-1 rounded text-[10px] font-bold uppercase">Licença Ativa</span>`,
    aprovado:    `<span class="bg-yellow-50 text-yellow-700 border border-yellow-200 px-2.5 py-1 rounded text-[10px] font-bold uppercase">PRAD Aprovado</span>`,
};

const PORTE_LABEL = { P: 'Pequeno', M: 'Médio', G: 'Grande' };
const PREFIXO    = { app_cidadao: 'INC', planet_labs: 'SWP', app_produtor: 'PRAD' };

function acaoBotao(a) {
    if (a.origem === 'app_cidadao')
        return `<button onclick="analisarEXIF(${a.id})" class="text-[#0077B6] font-bold text-xs bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg border border-blue-200 transition flex items-center gap-1.5 ml-auto"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg> Analisar EXIF</button>`;
    if (a.origem === 'planet_labs')
        return `<button onclick="gerarAuto(${a.id})" class="text-gray-700 font-bold text-xs bg-white hover:bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-300 transition flex items-center gap-1.5 ml-auto shadow-sm"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg> Gerar Auto (Multa)</button>`;
    return `<span class="text-[10px] font-bold text-yellow-700 bg-yellow-50 px-2 py-1 rounded border border-yellow-200">Emissão Selo Verde</span>`;
}

function renderTabela() {
    const RISCO_MAP = { 'Crítico (Fogo)': 'sem_licenca', 'Alto (Desmate)': 'vencida' };
    const PORTE_MAP = { 'Grande Porte': 'G', 'Médio Porte': 'M' };

    let lista = todosAlertas.filter(a => {
        if (filtroRisco !== 'Todos os Riscos' && a.status_licenca !== RISCO_MAP[filtroRisco]) return false;
        if (filtroPorte !== 'Qualquer Porte' && a.porte_car !== PORTE_MAP[filtroPorte]) return false;
        return true;
    });

    const tbody = document.getElementById('tabela-body');
    if (!lista.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="px-6 py-8 text-center text-gray-400 text-xs">Nenhum alerta para este filtro</td></tr>`;
        return;
    }

    tbody.innerHTML = lista.map(a => {
        const o = ORIGEM[a.origem];
        const dt = new Date(a.criado_em);
        const hora = dt.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        const id = `${PREFIXO[a.origem]}-2026-${String(a.id).padStart(3,'0')}`;
        return `
        <tr class="hover:bg-blue-50/30 transition">
            <td class="px-6 py-4"><span class="font-mono font-bold text-gray-900">${id}</span><span class="block text-[10px] text-gray-500 mt-0.5">Hoje, ${hora}</span></td>
            <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                    <div class="w-7 h-7 rounded-lg flex items-center justify-center border" style="background:${o.bg};color:${o.cor};border-color:${o.cor}33">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${iconSVG(o.icon)}</svg>
                    </div>
                    <span class="font-bold text-gray-700">${o.label}</span>
                </div>
            </td>
            <td class="px-6 py-4"><span class="font-bold text-gray-800 line-clamp-1">${a.titulo}</span><span class="block text-[10px] text-gray-500 font-mono mt-0.5">CAR: ${PORTE_LABEL[a.porte_car]} Porte</span></td>
            <td class="px-6 py-4">${STATUS_BADGE[a.status_licenca] || ''}</td>
            <td class="px-6 py-4 text-right">${acaoBotao(a)}</td>
        </tr>`;
    }).join('');
}

function renderTriagem() {
    const feed  = document.getElementById('triagem-feed');
    const badge = document.getElementById('triagem-count');
    const pendentes = todosAlertas.filter(a => a.status_licenca !== 'aprovado');
    badge.textContent = `${pendentes.length} Alerta${pendentes.length !== 1 ? 's' : ''}`;

    feed.innerHTML = todosAlertas.map(a => {
        const isAprovado  = a.status_licenca === 'aprovado';
        const borderCor   = isAprovado ? '#285430' : a.status_licenca === 'sem_licenca' ? '#D62828' : '#D97706';
        const badgeHtml   = isAprovado
            ? `<span class="text-[9px] font-bold text-[#285430] px-1.5 py-0.5 rounded border border-green-300 bg-green-50 uppercase">Ronda OK</span>`
            : a.status_licenca === 'sem_licenca'
            ? `<span class="badge-danger text-[9px] font-bold px-1.5 py-0.5 rounded uppercase">Fogo Confirmado</span>`
            : `<span class="badge-warning text-[9px] font-bold px-1.5 py-0.5 rounded uppercase">Licença Vencida</span>`;
        return `
        <div class="bg-white border-l-4 rounded-xl p-3 shadow-sm hover:shadow-md transition cursor-pointer border border-gray-100 group" style="border-left-color:${borderCor}">
            <div class="flex justify-between items-start mb-1">${badgeHtml}<span class="text-[10px] text-gray-400 font-mono">${tempoRelativo(a.criado_em)}</span></div>
            <h4 class="font-bold text-sm text-gray-800 mt-1 group-hover:text-[#0077B6] transition">${a.titulo}</h4>
            <p class="text-[11px] text-gray-500 font-mono mt-1 line-clamp-1">${a.descricao}</p>
        </div>`;
    }).join('');
}

function iconSVG(name) {
    const icons = {
        smartphone: '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
        satellite:  '<path d="M13 7 9 3 5 7l4 4"/><path d="m17 11 4 4-4 4-4-4"/><path d="m8 12 4 4 6-6"/><path d="m2 2 20 20"/>',
        scan:       '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><rect width="10" height="8" x="7" y="8" rx="1"/>',
    };
    return icons[name] || '';
}

function analisarEXIF(id) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async e => {
        const file = e.target.files[0];
        if (!file) return;
        const form = new FormData();
        form.append('imagem', file);
        const btn = document.getElementById('btn-sweep');
        btn.textContent = 'Analisando EXIF...';
        try {
            const res  = await fetch(`${API}/alertas/incendio`, { method: 'POST', body: form });
            const data = await res.json();
            alert(data.simulado
                ? `Simulado (sem URL de webhook)\nPayload: ${JSON.stringify(data.payload, null, 2)}`
                : `Alerta enviado ao Corpo de Bombeiros!\nStatus: ${data.status_code}`);
        } catch { alert('Erro ao comunicar com a API.'); }
        finally { btn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg> Forçar Varredura (Sweep)'; }
    };
    input.click();
}

function gerarAuto(id) {
    if (confirm(`Confirma a geração do Auto de Infração para o incidente #${id}?\n\nEssa ação registrará a multa no sistema.`))
        alert('Auto de Infração registrado com sucesso!\n(Integração com sistema de multas em desenvolvimento)');
}

async function forcarVarredura() {
    const btn = document.getElementById('btn-sweep');
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg> Varrendo...`;
    await new Promise(r => setTimeout(r, 1800));
    await carregarAlertas();
    btn.disabled = false;
    btn.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg> Forçar Varredura (Sweep)`;
}

async function carregarAlertas() {
    try {
        const res = await fetch(`${API}/alertas/`);
        todosAlertas = await res.json();
    } catch { todosAlertas = []; }
    renderTabela();
    renderTriagem();
}

let activeDropdown = null;

function toggleDropdown(id) {
    const menu = document.getElementById(`${id}-menu`);
    const icon = document.getElementById(`${id}-icon`);
    if (activeDropdown && activeDropdown !== id) {
        document.getElementById(`${activeDropdown}-menu`).classList.add('opacity-0');
        setTimeout(() => document.getElementById(`${activeDropdown}-menu`).classList.add('hidden'), 200);
        document.getElementById(`${activeDropdown}-icon`).classList.remove('rotate-180');
    }
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        setTimeout(() => menu.classList.remove('opacity-0'), 10);
        icon.classList.add('rotate-180');
        activeDropdown = id;
    } else {
        menu.classList.add('opacity-0');
        setTimeout(() => menu.classList.add('hidden'), 200);
        icon.classList.remove('rotate-180');
        activeDropdown = null;
    }
}

function selectOption(dropdownId, text) {
    const span = document.getElementById(`${dropdownId}-selected`);
    const icon = dropdownId === 'dd-risco' ? 'filter' : 'layers';
    span.innerHTML = `<i data-lucide="${icon}" class="w-3 h-3 text-[#0077B6]"></i> ${text}`;
    lucide.createIcons();
    toggleDropdown(dropdownId);
    if (dropdownId === 'dd-risco') filtroRisco = text;
    else filtroPorte = text;
    renderTabela();
}

document.addEventListener('click', e => {
    if (activeDropdown && !document.getElementById(`${activeDropdown}-wrapper`).contains(e.target))
        toggleDropdown(activeDropdown);
    if (!e.target.closest('#search-input') && !e.target.closest('#search-results'))
        document.getElementById('search-results').classList.add('hidden');
});

let searchTimer;
document.getElementById('search-input').addEventListener('input', e => {
    clearTimeout(searchTimer);
    const q = e.target.value.trim();
    const results = document.getElementById('search-results');
    if (q.length < 2) { results.classList.add('hidden'); return; }
    searchTimer = setTimeout(async () => {
        try {
            const res  = await fetch(`${API}/propriedades/busca?q=${encodeURIComponent(q)}`);
            const data = await res.json();
            if (!data.length) { results.classList.add('hidden'); return; }
            results.innerHTML = data.map(p => `
                <div class="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-0 text-sm" onclick="location.href='produtores.html'">
                    <p class="font-bold text-gray-800">${p.municipio} <span class="text-[10px] font-normal text-gray-400 ml-1">${p.porte === 'G' ? 'Grande' : p.porte === 'M' ? 'Médio' : 'Pequeno'} Porte</span></p>
                    <p class="text-[10px] font-mono text-gray-500 mt-0.5">${p.numero_car}</p>
                </div>`).join('');
            results.classList.remove('hidden');
        } catch { results.classList.add('hidden'); }
    }, 350);
});

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('-translate-x-full');
    document.getElementById('mobile-overlay').classList.toggle('active');
}

const FIRE_ICON = L.divIcon({ className: '', iconSize: [32,32], iconAnchor: [16,16],
    html: `<div style="width:32px;height:32px;background:#D62828;border-radius:50%;border:2px solid white;display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(214,40,40,.8)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg></div>`
});
const DRONE_ICON = L.divIcon({ className: '', iconSize: [24,24], iconAnchor: [12,12],
    html: `<div style="width:24px;height:24px;background:#285430;border-radius:50%;border:2px solid white;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.2)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="m11 13 4-4"/><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-1.6-.3-3.2.2-4.2 1.3-.7.8-.9 1.9-.4 2.8l4 6.6 4.3 4.3 6.6 4c.9.5 2 .3 2.8-.4 1.1-1 1.6-2.6 1.3-4.2z"/></svg></div>`
});

document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();

    const map = L.map('map', { zoomControl: false }).setView([-10.7938, -49.6225], 7);
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO', subdomains: 'abcd', maxZoom: 20
    }).addTo(map);

    try {
        const [pontos, poligonos] = await Promise.all([
            fetch(`${API}/mapa/pontos`).then(r => r.json()),
            fetch(`${API}/mapa/poligonos`).then(r => r.json()),
        ]);
        pontos.forEach(p => {
            const icon = p.tipo === 'foco_incendio' ? FIRE_ICON : DRONE_ICON;
            L.marker([p.lat, p.lng], { icon }).addTo(map)
                .bindPopup(`<b>${p.titulo}</b><br><span style="font-size:11px;color:#555">${p.descricao}</span>`);
        });
        poligonos.forEach(p => {
            L.polygon(p.coordenadas, { color: '#D4A017', fillColor: '#D4A017', fillOpacity: 0.3, weight: 2 })
                .addTo(map)
                .bindPopup(`<b>${p.titulo}</b><br><span style="font-size:11px">${p.descricao}</span>`);
        });
    } catch { /* API offline */ }

    await carregarAlertas();
});
