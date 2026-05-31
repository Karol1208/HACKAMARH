const _API = 'http://127.0.0.1:8000';

// ── Badge de alertas ─────────────────────────────────────────────────────────
async function atualizarBadgeAlertas() {
    try {
        const { total } = await fetch(`${_API}/alertas/total`).then(r => r.json());
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

// ── Sessão do usuário ────────────────────────────────────────────────────────
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

    // Redireciona para login se não autenticado (exceto nas páginas públicas)
    if (!user && !path.includes('login') && !path.includes('cadastro')) {
        location.href = 'login.html';
        return;
    }

    const nomeEl  = document.getElementById('user-nome');
    const credEl  = document.getElementById('user-credencial');
    const avatarEl = document.getElementById('user-avatar');
    const areaEl  = document.getElementById('user-profile-area');

    if (!nomeEl || !user) return;

    // Atualiza textos
    nomeEl.textContent = user.nome;
    credEl.textContent = 'ID: ' + user.credencial;

    // Atualiza avatar
    if (avatarEl) {
        if (avatarEl.tagName === 'IMG') {
            avatarEl.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.nome)}&background=285430&color=fff`;
            avatarEl.alt = user.nome;
        } else {
            avatarEl.textContent = iniciais(user.nome);
        }
    }

    // Injeta dropdown de logout
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

// ── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    atualizarBadgeAlertas();
    carregarPerfil();
});
