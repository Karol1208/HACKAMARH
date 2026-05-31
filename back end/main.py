import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from routers import users, alertas, scanner, dashboard, mapa, propriedades, notificacoes, solicitacoes, viveiros, relatorios
from services.scanner_restauracao import ScannerRestauracao


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização síncrona do scanner (fallback mock quando modelo não está disponível)
    ScannerRestauracao.inicializar()
    yield


app = FastAPI(title="HACKAMARH API", lifespan=lifespan)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    return response

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_UPLOAD_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail": "Arquivo muito grande. Limite máximo: 10 MB."}
            )
    return await call_next(request)

# Origens permitidas — em produção, defina ALLOWED_ORIGINS com a URL real
_raw_origins = os.getenv(
    'ALLOWED_ORIGINS',
    'http://localhost:8000,http://127.0.0.1:8000,'
    'http://localhost:5500,http://127.0.0.1:5500,'
    'http://10.0.2.2:8000'
)
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(',') if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
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
    file_path = (STATIC_DIR / path_name).resolve()
    try:
        file_path.relative_to(STATIC_DIR.resolve())
    except ValueError:
        # Tentativa de path traversal — retorna index
        return FileResponse(STATIC_DIR / "index.html")
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(STATIC_DIR / "index.html")
