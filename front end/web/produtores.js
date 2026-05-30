const API = 'http://127.0.0.1:8000';

let todosProductores = [];
let filtroStatus = 'todos';
let buscaTexto = '';

function toast(msg, tipo) {
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;padding:12px 20px;border-radius:12px;font-size:14px;font-weight:700;color:white;box-shadow:0 10px 30px rgba(0,0,0,.2)';
    t.style.background = tipo === 'erro' ? '#D62828' : '#285430';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

// --- KPIs do hero ---
async function carregarKPIs() {
    try {
        const d = await fetch(API + '/dashboard/kpis').then(r => r.json());
        const elSelos = document.getElementById('kpi-selos');
        const elSob = document.getElementById('kpi-sobrevivencia');
        if (elSelos) elSelos.textContent = d.selos_verdes.toLocaleString('pt-BR');
        if (elSob) elSob.textContent = d.sobrevivencia_pct + '%';
    } catch(e) {}
}

// --- Carrega e renderiza produtores ---
async function carregarProdutores() {
    try {
        todosProductores = await fetch(API + '/propriedades/').then(r => r.json());
    } catch(e) { todosProductores = []; }
    renderProdutores();
}

function renderProdutores() {
    const grid = document.getElementById('grid-produtores');
    if (!grid) return;

    let lista = todosProductores;

    if (filtroStatus !== 'todos') {
        lista = lista.filter(p => p.status === filtroStatus);
    }

    if (buscaTexto.length >= 2) {
        const q = buscaTexto.toLowerCase();
        lista = lista.filter(p =>
            p.nome.toLowerCase().includes(q) ||
            p.car.toLowerCase().includes(q)
        );
    }

    grid.innerHTML = '';

    if (!lista.length) {
        const empty = document.createElement('div');
        empty.className = 'col-span-3 text-center py-16 text-gray-400';
        empty.textContent = 'Nenhum produtor encontrado';
        grid.appendChild(empty);
        return;
    }

    lista.forEach(p => grid.appendChild(criarCard(p)));
    lucide.createIcons();
}

function criarCard(p) {
    const cores = {
        elegivel: { faixa: '#285430', badge: 'bg-green-50 text-[#285430]', icone: 'check-circle-2' },
        atrasado: { faixa: '#D62828', badge: 'bg-red-50 text-[#D62828]',   icone: 'alert-triangle'  },
        pendente: { faixa: '#0077B6', badge: 'bg-blue-50 text-[#0077B6]',  icone: 'clock'           },
    };
    const labels = { elegivel: 'Elegível Selo Verde', atrasado: 'Leitura Atrasada', pendente: 'Leitura Recebida' };
    const c = cores[p.status] || cores.pendente;

    const card = document.createElement('div');
    card.className = 'bg-white rounded-3xl p-8 border border-gray-200 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between';

    // faixa lateral
    const faixa = document.createElement('div');
    faixa.className = 'absolute left-0 top-0 bottom-0 w-1.5';
    faixa.style.background = c.faixa;
    card.appendChild(faixa);

    // header do card
    const header = document.createElement('div');
    header.className = 'mb-6';

    const topRow = document.createElement('div');
    topRow.className = 'flex justify-between items-start mb-3 pl-2';

    const badge = document.createElement('span');
    badge.className = c.badge + ' text-[10px] font-bold px-2.5 py-1 rounded uppercase tracking-wider flex items-center gap-1';
    const badgeIcon = document.createElement('i');
    badgeIcon.setAttribute('data-lucide', c.icone);
    badgeIcon.className = 'w-3 h-3';
    badge.appendChild(badgeIcon);
    badge.appendChild(document.createTextNode(' ' + labels[p.status]));

    const ano = document.createElement('span');
    ano.className = 'text-xs text-gray-400 font-mono';
    ano.textContent = 'Ano ' + p.ano_atual + '/' + p.total_anos;

    topRow.appendChild(badge);
    topRow.appendChild(ano);

    const nome = document.createElement('h4');
    nome.className = 'font-display font-extrabold text-gray-900 text-xl pl-2 leading-tight';
    nome.textContent = p.nome;

    const car = document.createElement('p');
    car.className = 'text-xs text-gray-500 font-mono mb-4 pl-2 mt-1';
    car.textContent = 'CAR: ' + p.car;

    header.appendChild(topRow);
    header.appendChild(nome);
    header.appendChild(car);
    card.appendChild(header);

    // bloco de dados IA
    const dadosIA = criarDadosIA(p, c);
    card.appendChild(dadosIA);

    // botões de ação
    const btnArea = criarBotoes(p);
    card.appendChild(btnArea);

    return card;
}

function criarDadosIA(p, c) {
    const box = document.createElement('div');

    if (p.status === 'atrasado') {
        box.className = 'bg-red-50/50 p-4 rounded-2xl border border-red-100 mb-8 flex items-start gap-4';
        const icone = document.createElement('i');
        icone.setAttribute('data-lucide', 'smartphone-off');
        icone.className = 'text-[#D62828] w-8 h-8 shrink-0 mt-1';
        const texto = document.createElement('div');
        const t1 = document.createElement('p');
        t1.className = 'text-xs font-bold text-gray-900 mb-1.5';
        t1.textContent = 'App: Sem dados no período';
        const t2 = document.createElement('p');
        t2.className = 'text-[11px] text-gray-600 leading-relaxed';
        t2.textContent = 'Produtor não realizou o escaneamento anual. Risco de multa automática.';
        texto.appendChild(t1);
        texto.appendChild(t2);
        box.appendChild(icone);
        box.appendChild(texto);
    } else {
        box.className = 'flex items-center gap-5 bg-gray-50/50 p-4 rounded-2xl border border-gray-100 mb-8';

        // gráfico circular
        const chartWrap = document.createElement('div');
        chartWrap.className = 'w-16 h-16 shrink-0 relative flex items-center justify-center';
        chartWrap.innerHTML =
            '<svg viewBox="0 0 36 36" style="width:64px;height:64px;color:' + c.faixa + '">' +
            '<path style="fill:none;stroke:#eee;stroke-width:3.8" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>' +
            '<path style="fill:none;stroke:' + c.faixa + ';stroke-width:2.8;stroke-linecap:round;stroke-dasharray:' + p.sobrevivencia_pct + ',100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>' +
            '</svg>' +
            '<span style="position:absolute;font-weight:800;font-size:11px;color:#374151">' + p.sobrevivencia_pct + '%</span>';

        const info = document.createElement('div');
        info.className = 'flex-1 space-y-2';

        const label = document.createElement('p');
        label.className = 'text-[10px] text-gray-500 font-bold uppercase tracking-wide';
        label.textContent = p.ano_atual === 1 ? 'Primeiro Escaneamento' : 'Sobrevivência Florestal';

        const row1 = criarInfoRow('Scan App:', p.mudas_scan.toLocaleString('pt-BR') + ' Mudas');
        const row2 = criarInfoRow('Crescimento IA:', p.crescimento || '—');

        info.appendChild(label);
        info.appendChild(row1);
        info.appendChild(row2);
        box.appendChild(chartWrap);
        box.appendChild(info);
    }

    return box;
}

function criarInfoRow(label, valor) {
    const row = document.createElement('div');
    row.className = 'flex justify-between text-xs';
    const l = document.createElement('span');
    l.className = 'text-gray-600';
    l.textContent = label;
    const v = document.createElement('span');
    v.className = 'font-bold text-gray-900';
    v.textContent = valor;
    row.appendChild(l);
    row.appendChild(v);
    return row;
}

function criarBotoes(p) {
    const wrap = document.createElement('div');
    wrap.className = 'mt-auto';

    if (p.status === 'elegivel') {
        const btn = document.createElement('button');
        btn.className = 'w-full bg-[#D4A017] hover:bg-yellow-600 text-white text-sm font-bold py-3.5 rounded-xl transition shadow-lg flex items-center justify-center gap-2';
        const ic = document.createElement('i');
        ic.setAttribute('data-lucide', 'award');
        ic.className = 'w-4 h-4';
        btn.appendChild(ic);
        btn.appendChild(document.createTextNode(' Emitir Certificado CarbonTO'));
        btn.onclick = () => emitirCertificado(p.id, p.nome);
        wrap.appendChild(btn);

    } else if (p.status === 'atrasado') {
        const row = document.createElement('div');
        row.className = 'flex gap-3';

        const btnNotif = document.createElement('button');
        btnNotif.className = 'flex-1 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-sm font-bold py-3.5 rounded-xl transition shadow-sm flex items-center justify-center gap-2';
        const icN = document.createElement('i');
        icN.setAttribute('data-lucide', 'mail');
        icN.className = 'w-4 h-4';
        btnNotif.appendChild(icN);
        btnNotif.appendChild(document.createTextNode(' Notificar'));
        btnNotif.onclick = () => notificarProdutor(p.id, p.nome);

        const btnAutuar = document.createElement('button');
        btnAutuar.className = 'flex-1 bg-red-50 border border-red-200 hover:bg-red-100 text-[#D62828] text-sm font-bold py-3.5 rounded-xl transition flex items-center justify-center gap-2';
        const icA = document.createElement('i');
        icA.setAttribute('data-lucide', 'gavel');
        icA.className = 'w-4 h-4';
        btnAutuar.appendChild(icA);
        btnAutuar.appendChild(document.createTextNode(' Autuar'));
        btnAutuar.onclick = () => autuarProdutor(p.id, p.nome);

        row.appendChild(btnNotif);
        row.appendChild(btnAutuar);
        wrap.appendChild(row);

    } else {
        const btn = document.createElement('button');
        btn.className = 'w-full bg-[#0077B6] hover:bg-blue-700 text-white text-sm font-bold py-3.5 rounded-xl transition shadow-md flex items-center justify-center gap-2';
        const ic = document.createElement('i');
        ic.setAttribute('data-lucide', 'eye');
        ic.className = 'w-4 h-4';
        btn.appendChild(ic);
        btn.appendChild(document.createTextNode(' Auditar Fotos'));
        btn.onclick = () => auditarFotos(p.id, p.nome);
        wrap.appendChild(btn);
    }

    return wrap;
}

// --- Ações ---
async function emitirCertificado(id, nome) {
    if (!confirm('Emitir Certificado CarbonTO para "' + nome + '"?')) return;
    try {
        const d = await fetch(API + '/propriedades/' + id + '/certificar', { method: 'POST' }).then(r => r.json());
        toast(d.mensagem);
    } catch(e) { toast('Erro ao emitir certificado', 'erro'); }
}

async function notificarProdutor(id, nome) {
    if (!confirm('Enviar notificação de pendência para "' + nome + '"?')) return;
    try {
        const d = await fetch(API + '/propriedades/' + id + '/notificar', { method: 'POST' }).then(r => r.json());
        toast(d.mensagem);
    } catch(e) { toast('Erro ao notificar', 'erro'); }
}

async function autuarProdutor(id, nome) {
    if (!confirm('Gerar Auto de Infração para "' + nome + '"?\n\nEssa ação é irreversível.')) return;
    try {
        const d = await fetch(API + '/propriedades/' + id + '/autuar', { method: 'POST' }).then(r => r.json());
        toast(d.mensagem);
    } catch(e) { toast('Erro ao autuar', 'erro'); }
}

function auditarFotos(id, nome) {
    toast('Abrindo módulo de auditoria para ' + nome + '...');
    // futura navegação para tela de auditoria de imagens
}

// --- Dropdown de status ---
let activeDropdown = null;

function toggleDropdown(id) {
    const menu = document.getElementById(id + '-menu');
    const icon = document.getElementById(id + '-icon');
    if (activeDropdown && activeDropdown !== id) {
        const prev = document.getElementById(activeDropdown + '-menu');
        if (prev) { prev.classList.add('opacity-0'); setTimeout(() => prev.classList.add('hidden'), 200); }
        const prevIcon = document.getElementById(activeDropdown + '-icon');
        if (prevIcon) prevIcon.classList.remove('rotate-180');
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

function selectOption(dropdownId, text, iconName, colorClass) {
    colorClass = colorClass || 'text-[#D4A017]';
    const span = document.getElementById(dropdownId + '-selected');
    span.innerHTML = '<i data-lucide="' + iconName + '" class="w-4 h-4 ' + colorClass + '"></i> ' + text;
    lucide.createIcons();
    toggleDropdown(dropdownId);

    const map = { 'Todos os Status': 'todos', 'Elegível / Aprovado': 'elegivel', 'Pendente de Leitura': 'pendente', 'Atrasado / Risco': 'atrasado' };
    filtroStatus = map[text] || 'todos';
    renderProdutores();
}

// --- Busca ---
let searchTimer;
function iniciarBusca(input) {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
        buscaTexto = input.value;
        renderProdutores();
    }, 300);
}

// --- Sidebar mobile ---
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('-translate-x-full');
    document.getElementById('mobile-overlay').classList.toggle('active');
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    document.addEventListener('click', e => {
        if (activeDropdown) {
            const w = document.getElementById(activeDropdown + '-wrapper');
            if (w && !w.contains(e.target)) toggleDropdown(activeDropdown);
        }
    });

    carregarKPIs();
    carregarProdutores();
});
