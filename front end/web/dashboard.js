let mapRef = null;
let markersLayer = null;
let polisLayer = null;
let municipioAtual = null;
let searchTimer;

function fmt(n) {
    if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
    if (n >= 1_000) return (n / 1_000).toFixed(1) + 'k';
    return String(n).padStart(2, '0');
}

function tempoRelativo(isoStr) {
    const diff = Math.floor((Date.now() - new Date(isoStr)) / 60000);
    if (diff < 1) return 'Agora';
    if (diff < 60) return `Há ${diff} min`;
    return `Há ${Math.floor(diff / 60)}h`;
}

const ORIGEM_CONFIG = {
    app_cidadao:  { cor: '#D62828', bg: 'bg-red-50',   text: 'text-[#D62828]', label: 'App Cidadão',  icon: 'smartphone', acao: 'Ver Detalhes' },
    planet_labs:  { cor: '#0077B6', bg: 'bg-blue-50',  text: 'text-[#0077B6]', label: 'Planet Labs',  icon: 'satellite',  acao: 'Auditar'      },
    app_produtor: { cor: '#285430', bg: 'bg-green-50', text: 'text-[#285430]', label: 'App Produtor', icon: 'scan',       acao: 'Ver Atestado' },
};

const PORTE_LABEL = { P: 'Pequeno Porte', M: 'Médio Porte', G: 'Grande Porte' };

async function carregarKPIs(municipio = null) {
    try {
        const params = municipio ? `?municipio=${encodeURIComponent(municipio)}` : '';
        const res = await fetch(`${API}/dashboard/kpis${params}`);
        if (!res.ok) throw new Error(res.status);
        const d = await res.json();
        document.getElementById('kpi-mudas').textContent = fmt(d.mudas_atestadas);
        document.getElementById('kpi-sobrevivencia').textContent = d.sobrevivencia_pct;
        document.getElementById('kpi-drones').textContent = d.drones_ativos;
        document.getElementById('kpi-infracoes').textContent = fmt(d.infracoes_sem_licenca);
        document.getElementById('kpi-selos').textContent = fmt(d.selos_verdes);
    } catch { /* API offline — mantém o traço */ }
}

async function carregarAlertas(municipio = null) {
    const feed = document.getElementById('alert-feed');
    try {
        const params = municipio ? `?municipio=${encodeURIComponent(municipio)}` : '';
        const res = await fetch(`${API}/alertas/${params}`);
        if (!res.ok) throw new Error(res.status);
        const alertas = await res.json();
        if (!alertas.length) {
            feed.innerHTML = `<div class="text-center py-8 text-gray-400 text-xs">Nenhum alerta encontrado${municipio ? ` em ${municipio}` : ''}</div>`;
            return;
        }
        feed.innerHTML = alertas.map(a => {
            const c = ORIGEM_CONFIG[a.origem] || ORIGEM_CONFIG.app_cidadao;
            const isAprovado = a.status_licenca === 'aprovado';
            return `
            <div onclick="location.href='alertas.html'" class="bg-white border rounded-xl p-4 shadow-sm hover:shadow-md transition cursor-pointer relative overflow-hidden" style="border-color:${c.cor}33">
                <div class="absolute left-0 top-0 bottom-0 w-1" style="background:${c.cor}"></div>
                <div class="flex justify-between items-start mb-2">
                    <span class="${c.bg} ${c.text} text-[10px] font-bold px-2 py-0.5 rounded uppercase flex items-center gap-1">
                        <i data-lucide="${c.icon}" class="w-3 h-3"></i> ${c.label}
                    </span>
                    <span class="text-xs font-mono text-gray-400">${tempoRelativo(a.criado_em)}</span>
                </div>
                <h4 class="font-bold text-gray-800 text-sm mb-1">${a.titulo}</h4>
                <p class="text-xs text-gray-600 mb-3 line-clamp-2">${a.descricao}</p>
                <div class="flex justify-between items-center">
                    ${isAprovado
                        ? `<span class="text-[10px] font-bold text-[#D4A017] bg-yellow-50 px-1.5 py-0.5 rounded border border-yellow-200">Emissão Selo Verde</span>`
                        : `<span class="text-[10px] font-mono text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">CAR: ${PORTE_LABEL[a.porte_car]}</span>
                           <button class="text-[#0077B6] text-xs font-bold hover:underline">${c.acao}</button>`
                    }
                </div>
            </div>`;
        }).join('');
        lucide.createIcons();
    } catch {
        feed.innerHTML = '<div class="text-center py-8 text-gray-400 text-xs">API offline — sem alertas</div>';
    }
}

async function carregarNotificacoes() {
    try {
        const res = await fetch(`${API}/notificacoes/nao-lidas/total`);
        if (!res.ok) throw new Error(res.status);
        const { total } = await res.json();
        const badge = document.getElementById('notif-badge');
        if (total > 0) {
            badge.textContent = total;
            badge.classList.remove('hidden');
            badge.classList.add('flex');
        }
    } catch { /* silencioso */ }
}

async function carregarMapa(municipio = null) {
    if (!mapRef || !markersLayer || !polisLayer) return;
    markersLayer.clearLayers();
    polisLayer.clearLayers();
    try {
        const params = municipio ? `?municipio=${encodeURIComponent(municipio)}` : '';
        const [pontos, poligonos] = await Promise.all([
            fetch(`${API}/mapa/pontos${params}`).then(r => r.json()),
            fetch(`${API}/mapa/poligonos${params}`).then(r => r.json()),
        ]);
        pontos.forEach(p => {
            const icon = p.tipo === 'foco_incendio' ? FIRE_ICON : DRONE_ICON;
            L.marker([p.lat, p.lng], { icon })
                .addTo(markersLayer)
                .bindPopup(`<b>${p.titulo}</b><br><span style="font-size:11px;color:#555">${p.descricao}</span>`);
        });
        poligonos.forEach(p => {
            L.polygon(p.coordenadas, { color: '#285430', fillColor: '#285430', fillOpacity: 0.2, weight: 2, dashArray: '5,5' })
                .addTo(polisLayer)
                .bindPopup(`<b>${p.titulo}</b><br><span style="font-size:11px;color:#285430;font-weight:bold">${p.descricao}</span>`);
        });
        if (municipio) {
            if (poligonos.length) {
                const allCoords = poligonos.flatMap(p => p.coordenadas);
                if (allCoords.length) mapRef.fitBounds(allCoords, { padding: [40, 40] });
            } else if (pontos.length) {
                const bounds = L.latLngBounds(pontos.map(p => [p.lat, p.lng]));
                mapRef.fitBounds(bounds, { padding: [60, 60] });
            }
        }
    } catch { /* API offline */ }
}

function filtrarPorMunicipio(municipio, car) {
    municipioAtual = municipio;
    document.getElementById('search-results').classList.add('hidden');
    document.getElementById('search-input').value = municipio;

    document.getElementById('location-text').textContent = `${municipio} | Varredura Ativa`;

    const badge = document.getElementById('filter-badge');
    document.getElementById('filter-badge-text').textContent = municipio;
    badge.classList.remove('hidden');
    badge.classList.add('flex');
    lucide.createIcons();

    carregarKPIs(municipio);
    carregarAlertas(municipio);
    carregarMapa(municipio);
}

function limparFiltro() {
    municipioAtual = null;
    document.getElementById('search-input').value = '';
    document.getElementById('location-text').textContent = 'Estado do Tocantins | Varredura Ativa';

    const badge = document.getElementById('filter-badge');
    badge.classList.add('hidden');
    badge.classList.remove('flex');

    if (mapRef) mapRef.setView([-10.1833, -48.3333], 6);

    carregarKPIs();
    carregarAlertas();
    carregarMapa();
}

document.getElementById('search-input').addEventListener('input', e => {
    clearTimeout(searchTimer);
    const q = e.target.value.trim();
    const results = document.getElementById('search-results');
    if (q.length < 2) { results.classList.add('hidden'); return; }
    searchTimer = setTimeout(async () => {
        try {
            const res = await fetch(`${API}/propriedades/busca?q=${encodeURIComponent(q)}`);
            if (!res.ok) throw new Error(res.status);
            const data = await res.json();
            if (!data.length) { results.classList.add('hidden'); return; }
            results.innerHTML = data.map(p => `
                <div class="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-0 text-sm search-result-item"
                     data-municipio="${p.municipio}" data-car="${p.numero_car}">
                    <p class="font-bold text-gray-800">${p.municipio} <span class="text-[10px] font-normal text-gray-400 ml-1">${p.porte === 'G' ? 'Grande' : p.porte === 'M' ? 'Médio' : 'Pequeno'} Porte</span></p>
                    <p class="text-[10px] font-mono text-gray-500 mt-0.5">${p.numero_car}</p>
                </div>`).join('');
            results.classList.remove('hidden');
            results.querySelectorAll('.search-result-item').forEach(item => {
                item.addEventListener('click', () => filtrarPorMunicipio(item.dataset.municipio, item.dataset.car));
            });
        } catch { results.classList.add('hidden'); }
    }, 350);
});

document.addEventListener('click', e => {
    if (!e.target.closest('#search-input') && !e.target.closest('#search-results'))
        document.getElementById('search-results').classList.add('hidden');
});

const FIRE_ICON = L.divIcon({ className: '', iconSize: [24,24], iconAnchor: [12,12],
    html: `<div style="width:24px;height:24px;background:#D62828;border-radius:50%;border:2px solid white;display:flex;align-items:center;justify-content:center;box-shadow:0 0 15px rgba(214,40,40,.6)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg></div>`
});
const DRONE_ICON = L.divIcon({ className: '', iconSize: [24,24], iconAnchor: [12,12],
    html: `<div style="width:24px;height:24px;background:#0077B6;border-radius:50%;border:2px solid white;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.2)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-1.6-.3-3.2.2-4.2 1.3-.7.8-.9 1.9-.4 2.8l4 6.6 4.3 4.3 6.6 4c.9.5 2 .3 2.8-.4 1.1-1 1.6-2.6 1.3-4.2z"/><path d="m11 13 4-4"/></svg></div>`
});

document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();

    mapRef = L.map('map', { zoomControl: false }).setView([-10.1833, -48.3333], 6);
    L.control.zoom({ position: 'bottomright' }).addTo(mapRef);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO', subdomains: 'abcd', maxZoom: 20
    }).addTo(mapRef);

    markersLayer = L.layerGroup().addTo(mapRef);
    polisLayer = L.layerGroup().addTo(mapRef);

    await Promise.all([carregarKPIs(), carregarAlertas(), carregarNotificacoes(), carregarMapa()]);
});
