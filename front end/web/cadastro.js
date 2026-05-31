const API = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    document.getElementById('form-cadastro').addEventListener('submit', async e => {
        e.preventDefault();

        const btn = e.target.querySelector('button[type="submit"]');
        const textoOriginal = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = 'Enviando...';

        const payload = {
            nome:      document.getElementById('c-nome').value,
            email:     document.getElementById('c-email').value,
            orgao:     document.getElementById('c-orgao').value,
            matricula: document.getElementById('c-matricula').value,
        };

        try {
            const res = await fetch(API + '/solicitacoes/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (res.status === 201) {
                mostrarSucesso();
            } else {
                const err = await res.json();
                mostrarErro(err.detail || 'Erro ao enviar solicitação.');
                btn.disabled = false;
                btn.innerHTML = textoOriginal;
                lucide.createIcons();
            }
        } catch(err) {
            mostrarErro('Não foi possível conectar à API. Tente novamente.');
            btn.disabled = false;
            btn.innerHTML = textoOriginal;
            lucide.createIcons();
        }
    });
});

function mostrarSucesso() {
    const form = document.getElementById('form-cadastro');
    form.innerHTML =
        '<div class="text-center py-8">' +
        '<div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">' +
        '<i data-lucide="check-circle-2" class="w-8 h-8 text-[#285430]"></i>' +
        '</div>' +
        '<h3 class="font-display font-extrabold text-xl text-gray-900 mb-2">Solicitação Enviada!</h3>' +
        '<p class="text-sm text-gray-500 mb-6">Sua solicitação foi registrada e aguarda aprovação da Auditoria SEMARH.</p>' +
        '<a href="login.html" class="inline-flex items-center gap-2 bg-[#0077B6] hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl transition">' +
        'Voltar ao Login</a>' +
        '</div>';
    lucide.createIcons();
}

function mostrarErro(msg) {
    let el = document.getElementById('erro-msg');
    if (!el) {
        el = document.createElement('p');
        el.id = 'erro-msg';
        el.className = 'text-sm text-red-600 font-medium text-center mt-2';
        document.getElementById('form-cadastro').appendChild(el);
    }
    el.textContent = msg;
}
