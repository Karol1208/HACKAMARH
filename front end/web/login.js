document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    document.querySelector('button[type="button"]').addEventListener('click', function() {
        const inp = document.getElementById('password');
        inp.type = inp.type === 'password' ? 'text' : 'password';
    });

    document.getElementById('form-login').addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = this.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.textContent = 'Autenticando...';

        const credencial = document.getElementById('email').value.trim();
        const senha      = document.getElementById('password').value;

        if (!credencial || !senha) {
            mostrarErroLogin('Preencha todos os campos.');
            btn.disabled = false;
            btn.innerHTML = 'Autenticar Acesso';
            return;
        }

        await new Promise(r => setTimeout(r, 800));

        // Deriva nome de exibição a partir da credencial
        let nome = credencial;
        if (credencial.includes('@')) {
            nome = credencial.split('@')[0].replace(/[._]/g, ' ');
        }
        nome = nome.replace(/\b\w/g, c => c.toUpperCase());

        localStorage.setItem('caninde_user', JSON.stringify({ credencial, nome }));
        window.location.href = 'dashboard.html';
    });
});

function mostrarErroLogin(msg) {
    let el = document.getElementById('erro-login');
    if (!el) {
        el = document.createElement('p');
        el.id = 'erro-login';
        el.className = 'text-xs text-red-600 font-medium text-center mt-2';
        document.getElementById('form-login').appendChild(el);
    }
    el.textContent = msg;
}
