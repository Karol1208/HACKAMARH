const API = 'http://127.0.0.1:8000';

let board = { solicitacoes: [], em_preparo: [], prontas: [] };
let filtroViveiro = 'Todos os Viveiros (4)';

function fmt(n) {
    return n >= 1000 ? (n / 1000).toFixed(0) + 'k' : n;
}

function toast(msg, tipo) {
    const t = document.createElement('div');
    t.className = 'fixed bottom-6 right-6 z-[999] px-5 py-3 rounded-xl text-sm font-bold shadow-xl text-white';
    t.style.background = tipo === 'erro' ? '#D62828' : '#285430';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

async function carregarKPIs() {
    try {
        const d = await fetch(API + '/viveiros/kpis').then(r => r.json());
        document.getElementById('kpi-estoque').textContent = fmt(d.estoque_total);
        document.getElementById('kpi-prontas').textContent = fmt(d.prontas);
        document.getElementById('kpi-especie').textContent = d.especie_mais_pedida;
        document.getElementById('kpi-especie-popular').textContent = d.especie_mais_pedida_popular;
        document.getElementById('kpi-alerta-especie').textContent = d.alerta_especie;
        document.getElementById('kpi-alerta-qtd').textContent = 'Apenas ' + d.alerta_quantidade.toLocaleString('pt-BR') + ' un.';
    } catch(e) {}
}

function renderBoard() {
    const filtrar = list => filtroViveiro === 'Todos os Viveiros (4)'
        ? list
        : list.filter(c => (c.viveiro || '').includes(filtroViveiro.replace('Viveiro ', '')));

    const busca = document.getElementById('busca-input').value.toLowerCase();
    const filtrarBusca = list => busca.length < 2 ? list
        : list.filter(c => JSON.stringify(c).toLowerCase().includes(busca));

    renderSolicitacoes(filtrarBusca(board.solicitacoes));
    renderPreparo(filtrarBusca(filtrar(board.em_preparo)));
    renderProntas(filtrarBusca(filtrar(board.prontas)));
}

function criarBadge(text, cls) {
    const s = document.createElement('span');
    s.className = cls + ' text-[9px] px-2 py-0.5 rounded font-bold uppercase tracking-wider';
    s.textContent = text;
    return s;
}

function renderSolicitacoes(lista) {
    const col = document.getElementById('col-solicitacoes');
    col.closest('.flex-col').querySelector('span.rounded-full').textContent = lista.length;
    col.innerHTML = '';
    if (!lista.length) {
        col.innerHTML = '<div class="text-center py-6 text-gray-400 text-xs">Nenhuma solicitação</div>';
        return;
    }
    lista.forEach(s => {
        const card = document.createElement('div');
        card.className = 'glass-card rounded-xl p-4 cursor-grab' + (s.tipo.includes('PRAD') ? ' border-l-4 border-l-[#0077B6]' : '');

        const header = document.createElement('div');
        header.className = 'flex justify-between items-start mb-2';
        header.appendChild(criarBadge(s.tipo, s.tipo.includes('PRAD') ? 'badge-prad' : 'badge-voluntario'));
        const data = document.createElement('span');
        data.className = 'text-[10px] text-gray-400 font-mono';
        data.textContent = s.data;
        header.appendChild(data);

        const nome = document.createElement('p');
        nome.className = 'font-bold text-sm text-gray-900 mb-1';
        nome.textContent = s.nome;

        const desc = document.createElement('p');
        desc.className = 'text-xs text-gray-600 mb-3 line-clamp-2';
        desc.textContent = s.descricao;

        const footer = document.createElement('div');
        footer.className = 'flex flex-col sm:flex-row sm:justify-between sm:items-center pt-3 border-t border-gray-100 gap-3';

        const car = document.createElement('span');
        car.className = 'text-[10px] text-gray-500 font-mono bg-gray-100 px-1.5 py-0.5 rounded';
        car.textContent = s.car;

        const btns = document.createElement('div');
        btns.className = 'flex gap-2';

        const btnRejeitar = document.createElement('button');
        btnRejeitar.className = 'flex-1 sm:flex-none text-xs font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 px-3 py-1.5 rounded-lg transition';
        btnRejeitar.textContent = 'Rejeitar';
        btnRejeitar.onclick = () => rejeitarSolicitacao(s.id);

        const btnAvaliar = document.createElement('button');
        btnAvaliar.className = 'flex-1 sm:flex-none text-xs font-bold text-white bg-[#0077B6] hover:bg-blue-700 px-3 py-1.5 rounded-lg transition shadow-sm';
        btnAvaliar.textContent = 'Avaliar';
        btnAvaliar.onclick = () => aprovarSolicitacao(s.id);

        btns.appendChild(btnRejeitar);
        btns.appendChild(btnAvaliar);
        footer.appendChild(car);
        footer.appendChild(btns);

        card.appendChild(header);
        card.appendChild(nome);
        card.appendChild(desc);
        card.appendChild(footer);
        col.appendChild(card);
    });
}

function renderPreparo(lista) {
    const col = document.getElementById('col-preparo');
    col.closest('.flex-col').querySelector('span.rounded-full').textContent = lista.length;
    col.innerHTML = '';
    if (!lista.length) {
        col.innerHTML = '<div class="text-center py-6 text-gray-400 text-xs">Nenhum lote em preparo</div>';
        return;
    }
    lista.forEach(l => {
        const card = document.createElement('div');
        card.className = 'glass-card rounded-xl p-4';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'flex justify-between items-center mb-3';
        const vivBadge = document.createElement('span');
        vivBadge.className = 'text-[9px] font-bold text-brand-cerrado bg-green-50 border border-green-100 px-1.5 py-0.5 rounded uppercase';
        vivBadge.textContent = 'Viveiro ' + l.viveiro;
        headerDiv.appendChild(vivBadge);

        const titulo = document.createElement('p');
        titulo.className = 'font-bold text-sm text-gray-900';
        titulo.textContent = 'Lote #' + l.lote + ' - ' + l.especie;

        const dest = document.createElement('p');
        dest.className = 'text-xs text-gray-500 mb-3';
        dest.textContent = 'Destinado a: ' + l.destino;

        const progressBox = document.createElement('div');
        progressBox.className = 'bg-gray-50 p-2.5 rounded-lg border border-gray-100';
        progressBox.innerHTML =
            '<div class="flex justify-between text-[10px] font-bold mb-1.5"><span class="text-gray-600">Germinação</span><span style="color:#D4A017">' + l.germinacao_pct + '%</span></div>' +
            '<div class="w-full bg-gray-200 rounded-full h-1.5"><div style="width:' + l.germinacao_pct + '%;background:#D4A017" class="h-1.5 rounded-full"></div></div>' +
            '<p class="text-[9px] text-gray-500 mt-1.5 text-right font-mono">Restam ' + l.dias_restantes + ' dias</p>';

        const btnMover = document.createElement('button');
        btnMover.className = 'w-full mt-3 flex items-center justify-center gap-2 py-2.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-gray-700 hover:bg-gray-50 transition shadow-sm';
        btnMover.textContent = 'Mover para Prontas';
        btnMover.onclick = () => moverParaProntas(l.id);

        card.appendChild(headerDiv);
        card.appendChild(titulo);
        card.appendChild(dest);
        card.appendChild(progressBox);
        card.appendChild(btnMover);
        col.appendChild(card);
    });
}

function renderProntas(lista) {
    const col = document.getElementById('col-prontas');
    col.closest('.flex-col').querySelector('span.rounded-full').textContent = lista.length;
    col.innerHTML = '';
    if (!lista.length) {
        col.innerHTML = '<div class="text-center py-6 text-gray-400 text-xs">Nenhum lote pronto</div>';
        return;
    }
    lista.forEach(l => {
        const card = document.createElement('div');
        card.id = 'pronta-' + l.id;
        card.className = 'glass-card rounded-xl p-4 border-l-4 border-l-[#285430]';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'flex justify-between items-start mb-3';
        const badge = criarBadge('QR Code Gerado', 'badge-gerado');
        headerDiv.appendChild(badge);

        const titulo = document.createElement('p');
        titulo.className = 'font-bold text-sm text-gray-900';
        titulo.textContent = 'Lote #' + l.lote + ' - ' + l.especie;

        const info = document.createElement('div');
        info.className = 'mt-3 space-y-2 text-xs';
        [
            ['Quantidade', (l.quantidade || 0).toLocaleString('pt-BR') + ' un.'],
            ['Destino', l.destino],
            ['Viveiro', l.viveiro],
        ].forEach(([label, value]) => {
            const row = document.createElement('div');
            row.className = 'flex justify-between text-gray-600';
            row.innerHTML = '<span>' + label + ':</span><span class="font-bold text-gray-900">' + value + '</span>';
            info.appendChild(row);
        });

        const footer = document.createElement('div');
        footer.className = 'mt-4 pt-3 border-t border-gray-100 flex gap-2';

        const btnPrint = document.createElement('button');
        btnPrint.className = 'flex-1 py-2.5 bg-white border border-gray-200 hover:bg-gray-50 rounded-lg text-xs font-bold text-gray-700 transition shadow-sm';
        btnPrint.textContent = 'Imprimir';
        btnPrint.onclick = () => imprimirLote(l.id);

        const btnBaixa = document.createElement('button');
        btnBaixa.className = 'flex-1 py-2.5 bg-[#285430] hover:bg-green-800 text-white rounded-lg text-xs font-bold transition shadow-sm';
        btnBaixa.textContent = 'Dar Baixa';
        btnBaixa.onclick = () => darBaixa(l.id);

        footer.appendChild(btnPrint);
        footer.appendChild(btnBaixa);

        card.appendChild(headerDiv);
        card.appendChild(titulo);
        card.appendChild(info);
        card.appendChild(footer);
        col.appendChild(card);
    });
}

async function aprovarSolicitacao(id) {
    if (!confirm('Aprovar esta solicitação e liberar as mudas?')) return;
    try {
        await fetch(API + '/viveiros/solicitacoes/' + id + '/aprovar', { method: 'PATCH' });
        board.solicitacoes = board.solicitacoes.filter(s => s.id !== id);
        renderBoard();
        toast('Solicitação aprovada — lote em preparação');
    } catch(e) { toast('Erro ao comunicar com a API', 'erro'); }
}

async function rejeitarSolicitacao(id) {
    if (!confirm('Rejeitar esta solicitação?')) return;
    try {
        await fetch(API + '/viveiros/solicitacoes/' + id + '/rejeitar', { method: 'PATCH' });
        board.solicitacoes = board.solicitacoes.filter(s => s.id !== id);
        renderBoard();
        toast('Solicitação rejeitada');
    } catch(e) { toast('Erro ao comunicar com a API', 'erro'); }
}

async function moverParaProntas(id) {
    try {
        await fetch(API + '/viveiros/lotes/' + id + '/mover-para-prontas', { method: 'PATCH' });
        const lote = board.em_preparo.find(l => l.id === id);
        board.em_preparo = board.em_preparo.filter(l => l.id !== id);
        if (lote) board.prontas.push(Object.assign({}, lote, { quantidade: 0, id: id + 100 }));
        renderBoard();
        toast('Lote movido para Prontas');
    } catch(e) { toast('Erro ao comunicar com a API', 'erro'); }
}

function imprimirLote(id) {
    const lote = board.prontas.find(l => l.id === id);
    if (!lote) return;
    const w = window.open('', '_blank');
    const body = w.document.body;
    body.style.cssText = 'font-family:monospace;padding:32px';
    const lines = [
        'CANINDÉ — Comprovante de Lote',
        '---',
        'Lote: #' + lote.lote,
        'Espécie: ' + lote.especie,
        'Quantidade: ' + (lote.quantidade || 0) + ' un.',
        'Destino: ' + lote.destino,
        'Viveiro: ' + lote.viveiro,
        'Data: ' + new Date().toLocaleDateString('pt-BR'),
    ];
    lines.forEach(line => {
        const p = w.document.createElement('p');
        p.textContent = line;
        body.appendChild(p);
    });
    w.print();
}

async function darBaixa(id) {
    if (!confirm('Confirmar baixa do lote? Isso registra a entrega no sistema.')) return;
    try {
        await fetch(API + '/viveiros/lotes/' + id + '/dar-baixa', { method: 'PATCH' });
        const card = document.getElementById('pronta-' + id);
        if (card) {
            card.style.cssText = 'opacity:0;transform:scale(0.95);transition:all 0.3s';
            setTimeout(() => {
                board.prontas = board.prontas.filter(l => l.id !== id);
                renderBoard();
            }, 300);
        }
        toast('Baixa registrada com sucesso');
    } catch(e) { toast('Erro ao comunicar com a API', 'erro'); }
}

function abrirModal() {
    document.getElementById('modal-semeadura').classList.remove('hidden');
}

function fecharModal() {
    document.getElementById('modal-semeadura').classList.add('hidden');
    document.getElementById('form-semeadura').reset();
}

function toggleDropdown() {
    const menu = document.getElementById('dropdown-menu');
    const icon = document.getElementById('dropdown-icon');
    const isOpen = !menu.classList.contains('hidden');
    if (isOpen) {
        menu.classList.add('opacity-0');
        icon.classList.remove('rotate-180');
        setTimeout(() => menu.classList.add('hidden'), 200);
    } else {
        menu.classList.remove('hidden');
        setTimeout(() => menu.classList.remove('opacity-0'), 10);
        icon.classList.add('rotate-180');
    }
}

function selectOption(text) {
    filtroViveiro = text;
    const sel = document.getElementById('dropdown-selected');
    sel.textContent = text;
    toggleDropdown();
    renderBoard();
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('-translate-x-full');
    document.getElementById('mobile-overlay').classList.toggle('active');
}

document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();

    document.querySelectorAll('button').forEach(btn => {
        if (btn.textContent.includes('Nova Semeadura') || btn.querySelector('i[data-lucide="plus"]'))
            btn.addEventListener('click', abrirModal);
    });

    document.getElementById('btn-exportar')?.addEventListener('click', () => {
        const rows = [['Coluna', 'Lote', 'Especie', 'Viveiro', 'Destino']];
        board.em_preparo.forEach(l => rows.push(['Em Preparo', l.lote, l.especie, l.viveiro, l.destino]));
        board.prontas.forEach(l => rows.push(['Prontas', l.lote, l.especie, l.viveiro, l.destino]));
        const csv = rows.map(r => r.join(';')).join('\n');
        const a = document.createElement('a');
        a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent('﻿' + csv);
        a.download = 'viveiros_caninde.csv';
        a.click();
        toast('CSV exportado com sucesso!');
    });

    document.getElementById('busca-input').addEventListener('input', () => renderBoard());

    document.getElementById('form-semeadura').addEventListener('submit', async e => {
        e.preventDefault();
        const especie = document.getElementById('s-especie').value;
        const viveiro = document.getElementById('s-viveiro').value;
        const destino = document.getElementById('s-destino').value || 'A definir';
        
        try {
            await fetch(API + '/viveiros/lotes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ especie, viveiro, destino })
            });
            board = await fetch(API + '/viveiros/board').then(r => r.json());
            renderBoard();
            fecharModal();
            toast('Semeadura de ' + especie + ' registrada no Viveiro ' + viveiro);
        } catch(err) {
            toast('Erro ao salvar no servidor', 'erro');
        }
    });

    document.addEventListener('click', e => {
        const w = document.getElementById('dropdown-wrapper');
        const menu = document.getElementById('dropdown-menu');
        if (w && !w.contains(e.target) && !menu.classList.contains('hidden')) toggleDropdown();
    });

    await carregarKPIs();
    try {
        board = await fetch(API + '/viveiros/board').then(r => r.json());
    } catch(e) {}
    renderBoard();
});
