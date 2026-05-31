# Projeto Canindé: Guardião do Cerrado - Backend (API)

Bem-vindo ao repositório do Backend do **Projeto Canindé: Guardião do Cerrado**. Este sistema é o núcleo do projeto, responsável por fornecer os dados e a lógica de negócios focada na Restauração Ecológica, Monitoramento de Áreas Degradadas (Eixo 2) e integração para auditorias e certificações B2B/B2G.

## Tecnologias e Bibliotecas

A stack principal foi definida para proporcionar máxima escalabilidade, velocidade e capacidades geoespaciais e de inteligência artificial. O ecossistema é baseado em **Python**.

### Bibliotecas Principais (`requirements.txt`)
- `fastapi`: Framework web de alta performance para a construção de APIs.
- `uvicorn`: Servidor ASGI de alta performance para rodar o FastAPI.
- `pydantic[email]`: Validação de dados de alto desempenho (incluindo schemas de e-mail).
- `psycopg2-binary`: Adaptador de banco de dados PostgreSQL para Python (utilizado pelo PostGIS).
- `geoalchemy2`: Extensão do SQLAlchemy para lidar com tipos geoespaciais e operações do PostGIS (vital para o algoritmo Sweep Line e RN02).
- `shapely`: Biblioteca para manipulação e análise de dados geométricos planares.
- `Pillow`: (PIL) Biblioteca para manipulação, processamento e abertura de imagens.
- `ultralytics`: Framework de Visão Computacional utilizado (YOLOv8) para estimativa e análise de mudas (RN05).
- `httpx`: Cliente HTTP assíncrono para Python (usado em integrações externas e webhooks).
- `fpdf2`: Biblioteca de geração de PDFs, utilizada para emissão de dossiês e relatórios de impacto ambiental.

## Como Iniciar o Sistema de Forma Profissional

Para garantir o funcionamento pleno das rotas, bancos e IA, siga os passos abaixo:

### 1. Pré-requisitos
- **Python 3.10+**
- **PostgreSQL com extensão PostGIS** (para dados georreferenciados)
- **Git**

### 2. Configuração do Ambiente
1. Clone ou acesse o repositório e navegue até a pasta `back end`.
2. Recomenda-se a criação de um ambiente virtual (venv):
   ```bash
   python -m venv venv
   # No Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # No Linux/Mac
   source venv/bin/activate
   ```
3. Instale as dependências exigidas:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente necessárias (ex: `DATABASE_URL`, credenciais). *(Consulte o arquivo `.env.example` caso exista)*.

### 3. Execução da API
Com o ambiente configurado, inicie o servidor com o comando:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- A API estará disponível em: `http://localhost:8000`
- Documentação interativa (Swagger UI) disponível em: `http://localhost:8000/docs`

## Notas de Desenvolvimento

> **Análise Técnica: Bug na Exportação (Gestão de Viveiros)**
> Na página "Gestão de Viveiro", foi relatado que o botão "Exportar" não está executando a funcionalidade esperada. 
> 
> **Diagnóstico:** A biblioteca `fpdf2` está instalada e existe uma infraestrutura inicial de relatórios no backend (`relatorios.py`). No entanto, analisando o `viveiros.js` no Frontend, constatou-se que o botão está configurado para gerar e baixar um arquivo `.csv` utilizando apenas JavaScript do lado do cliente, sem fazer qualquer chamada para a API Backend. Não há um endpoint `/viveiros/exportar` configurado em `viveiros.py` para interceptar esse pedido e compilar os dados em PDF via `fpdf2`.
> 
> **Resolução Recomendada:**
> 1. Criar um novo endpoint `GET /viveiros/exportar` no backend.
> 2. Utilizar a biblioteca `fpdf2` (ou similar) para montar o relatório PDF/CSV real consultando o banco.
> 3. Atualizar o `viveiros.js` no frontend, substituindo a lógica atual por um `fetch()` ou ancoragem (tag `<a>`) apontando para o novo endpoint do backend.

---
**Equipe:** WB Projects Design & Dev
