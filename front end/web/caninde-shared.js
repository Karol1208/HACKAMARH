// Variável de API centralizada — usada por todos os JS da aplicação
const API = 'http://127.0.0.1:8000';

// ── Sidebar dinâmica ──────────────────────────────────────────────────────────
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('-translate-x-full');
    document.getElementById('mobile-overlay').classList.toggle('active');
}

function renderSidebar() {
    const placeholder = document.getElementById('sidebar-placeholder');
    if (!placeholder) return;

    const paginaAtiva = placeholder.dataset.paginaAtiva || '';

    const navItems = [
        { id: 'dashboard',  href: 'dashboard.html',     icon: 'layout-dashboard', label: 'Visão Geral' },
        { id: 'alertas',    href: 'alertas.html',        icon: 'crosshair',        label: 'Alertas IA (Sweep)', badge: true },
        { id: 'viveiros',   href: 'gestao_viveiro.html', icon: 'sprout',           label: 'Gestão de Viveiros' },
        { id: 'produtores', href: 'produtores.html',     icon: 'users',            label: 'Produtores (CAR)' },
        { id: 'relatorios', href: 'relatorios.html',     icon: 'bar-chart-2',      label: 'Relatórios ESG' },
    ];

    const navHTML = navItems.map(item => {
        const active = item.id === paginaAtiva;
        const cls = active
            ? 'flex items-center gap-3 px-4 py-3 bg-brand-cerrado text-white rounded-xl shadow-md transition group'
            : 'flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-white hover:text-brand-cerrado rounded-xl transition group';
        const iconCls = active ? 'w-5 h-5 shrink-0' : 'w-5 h-5 shrink-0 group-hover:scale-110 transition';
        const badgeHTML = item.badge
            ? `<span id="alertas-badge" class="ml-auto bg-brand-fire text-white text-[10px] font-bold px-2 py-0.5 rounded-full">3</span>`
            : '';
        return `<a href="${item.href}" class="${cls}"><i data-lucide="${item.icon}" class="${iconCls}"></i><span class="font-medium text-sm">${item.label}</span>${badgeHTML}</a>`;
    }).join('');

    placeholder.outerHTML = `
        <div id="mobile-overlay" class="fixed inset-0 bg-brand-cerrado/40 backdrop-blur-sm z-30 overlay lg:hidden" onclick="toggleSidebar()"></div>
        <aside id="sidebar" class="fixed inset-y-0 left-0 transform -translate-x-full lg:relative lg:translate-x-0 w-64 shrink-0 glass-panel border-r border-gray-200 flex flex-col justify-between z-40 transition-transform duration-300 ease-in-out">
            <div>
                <div class="h-20 flex items-center justify-between lg:justify-start px-6 border-b border-gray-100">
                    <div class="flex items-center gap-3">
                        <div class="relative w-14 h-14 flex items-center justify-center shrink-0">
                            <img src="logo.png" alt="Logo Canindé" class="w-full h-full object-contain">
                        </div>
                        <div>
                            <h1 class="font-display font-extrabold text-xl text-brand-cerrado leading-none">Canindé</h1>
                            <span class="text-[9px] uppercase tracking-widest text-gray-500 font-bold">SEMARH / TO</span>
                        </div>
                    </div>
                    <button onclick="toggleSidebar()" class="lg:hidden text-gray-400 hover:text-gray-700 bg-gray-50 rounded-lg p-1.5 border border-gray-200">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                </div>
                <nav class="mt-6 px-3 space-y-2">${navHTML}</nav>
            </div>
            <div class="p-4 border-t border-gray-100">
                <div id="user-profile-area" class="flex items-center gap-3 bg-white/50 p-3 rounded-xl border border-gray-100">
                    <img id="user-avatar" src="https://ui-avatars.com/api/?name=Admin&background=285430&color=fff" alt="Avatar" class="w-10 h-10 rounded-full border-2 border-white shadow-sm shrink-0">
                    <div>
                        <p id="user-nome" class="text-sm font-bold text-gray-800 leading-tight">Carregando...</p>
                        <p id="user-credencial" class="text-[10px] text-gray-500 font-mono">—</p>
                    </div>
                </div>
            </div>
        </aside>`;
}

// ── Badge de alertas ──────────────────────────────────────────────────────────
async function atualizarBadgeAlertas() {
    try {
        const res = await fetch(`${API}/alertas/total`);
        if (!res.ok) return;
        const { total } = await res.json();
        const badge = document.getElementById('alertas-badge');
        if (!badge) return;
        if (total > 0) {
            badge.textContent = total;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    } catch { /* API offline — mantém estado atual */ }
}

// ── Sessão do usuário ─────────────────────────────────────────────────────────
function getUsuario() {
    try { return JSON.parse(localStorage.getItem('caninde_user')); }
    catch { return null; }
}

function iniciais(str) {
    const partes = str.replace(/@.*/, '').split(/[\s\-_]+/).filter(Boolean);
    return partes.length >= 2
        ? (partes[0][0] + partes[1][0]).toUpperCase()
        : str.slice(0, 2).toUpperCase();
}

function sairDoSistema() {
    localStorage.removeItem('caninde_user');
    location.href = 'login.html';
}

function carregarPerfil() {
    const path = location.pathname;
    const user = getUsuario();

    if (!user && !path.includes('login') && !path.includes('cadastro')) {
        location.href = 'login.html';
        return;
    }

    const nomeEl   = document.getElementById('user-nome');
    const credEl   = document.getElementById('user-credencial');
    const avatarEl = document.getElementById('user-avatar');
    const areaEl   = document.getElementById('user-profile-area');

    if (!nomeEl || !credEl || !user) return;

    nomeEl.textContent = user.nome;
    credEl.textContent = 'ID: ' + user.credencial;

    if (avatarEl) {
        if (avatarEl.tagName === 'IMG') {
            avatarEl.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.nome)}&background=285430&color=fff`;
            avatarEl.alt = user.nome;
        } else {
            avatarEl.textContent = iniciais(user.nome);
        }
    }

    if (!areaEl) return;
    areaEl.style.cursor = 'pointer';

    const wrapper = areaEl.parentElement;
    wrapper.style.position = 'relative';

    const menu = document.createElement('div');
    menu.id = 'logout-menu';
    menu.className = 'hidden absolute bottom-full left-0 right-0 mb-2 bg-white border border-gray-200 rounded-xl shadow-xl overflow-hidden z-50';
    menu.innerHTML = `
        <div class="px-4 py-3 border-b border-gray-100">
            <p class="text-xs font-bold text-gray-800 truncate">${user.nome}</p>
            <p class="text-[10px] text-gray-500 font-mono">ID: ${user.credencial}</p>
        </div>
        <button onclick="sairDoSistema()" class="w-full flex items-center gap-3 px-4 py-3 text-sm font-bold text-red-600 hover:bg-red-50 transition">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Sair do Sistema
        </button>`;
    wrapper.appendChild(menu);

    areaEl.addEventListener('click', e => {
        e.stopPropagation();
        menu.classList.toggle('hidden');
    });
    document.addEventListener('click', () => menu.classList.add('hidden'));
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    renderSidebar();        // 1. injeta sidebar (antes de tudo)
    lucide.createIcons();   // 2. renderiza ícones do sidebar
    atualizarBadgeAlertas(); // 3. conta alertas reais
    carregarPerfil();       // 4. preenche usuário logado
});
