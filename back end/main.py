from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routers import users, alertas, scanner, dashboard, mapa, propriedades, notificacoes, solicitacoes, viveiros, relatorios
from services.scanner_restauracao import ScannerRestauracao


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização síncrona do scanner (fallback mock quando modelo não está disponível)
    ScannerRestauracao.inicializar()
    yield


app = FastAPI(title="HACKAMARH API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(alertas.router)
app.include_router(scanner.router)
app.include_router(dashboard.router)
app.include_router(mapa.router)
app.include_router(propriedades.router)
app.include_router(notificacoes.router)
app.include_router(solicitacoes.router)
app.include_router(viveiros.router)
app.include_router(relatorios.router)

STATIC_DIR = Path(__file__).resolve().parent.parent / "front end" / "web"

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/{path_name:path}")
async def serve_static(path_name: str, request: Request):
    file_path = STATIC_DIR / path_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(STATIC_DIR / "index.html")
