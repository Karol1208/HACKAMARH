# Projeto Canindé: Guardião do Cerrado - Frontend (Web)

Bem-vindo ao repositório do Frontend do **Projeto Canindé: Guardião do Cerrado**. Este sistema web fornece um painel interativo (Dashboard ESG) para o monitoramento da restauração ecológica, gestão de viveiros e acompanhamento de alertas ambientais no estado do Tocantins.

## Tecnologias e Stack
- **HTML5, CSS3, JavaScript (Vanilla):** Estrutura, estilização customizada e interatividade leve.
- **Tailwind CSS:** Framework utilitário para estilização rápida e responsiva, configurado com a Identidade Visual COP30.
- **Lucide Icons:** Biblioteca de ícones elegantes e consistentes.

## Estrutura de Arquivos
- `index.html`, `login.html`: Páginas de acesso.
- `dashboard.html`: Painel principal de indicadores ESG e alertas.
- `gestao_viveiro.html`: Interface para gestão de estoque e distribuição de mudas.
- `alertas.html`: Módulo para monitoramento de alertas e ocorrências (IA/Satélite).
- `relatorios.html`: Emissão de dossiês e selos B2B.

## Como Iniciar o Sistema (Web)

1. **Requisitos:** Um navegador web moderno (Chrome, Edge, Firefox, Safari) e um servidor local simples.
2. **Execução Local (Live Server):**
   - Recomendamos a utilização da extensão **Live Server** no VS Code.
   - Alternativamente, utilizando Python, abra o terminal na pasta `front end/web` e execute:
     ```bash
     python -m http.server 5500
     ```
3. **Acesso:**
   - Abra o navegador e acesse `http://localhost:5500`.
   - O sistema fará a comunicação automática com o Backend (FastAPI) rodando na porta padrão.

## Nota de Manutenção (Bug Report)
> **Gestão de Viveiros - Botão "Exportar"**
> Atualmente, o botão "Exportar" na página de Gestão de Viveiros (`gestao_viveiro.html` / `viveiros.js`) está gerando um arquivo CSV estático via JavaScript no cliente (front-end). Ele **não** está se comunicando com o Backend para utilizar as bibliotecas de geração de relatórios (como o `fpdf2`). Para correção, a função do botão deve ser atualizada para realizar uma requisição `GET` ao Backend (ex: `/viveiros/exportar`) que processará o documento com os dados reais do banco.

---
**Equipe:** WB Projects Design & Dev
