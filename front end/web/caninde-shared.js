const _API = 'http://127.0.0.1:8000';

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

document.addEventListener('DOMContentLoaded', atualizarBadgeAlertas);
