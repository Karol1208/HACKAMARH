from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, alertas, scanner, dashboard, mapa, propriedades, notificacoes, solicitacoes, viveiros, relatorios
from services.scanner_restauracao import ScannerRestauracao

app = FastAPI(title="HACKAMARH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    ScannerRestauracao.inicializar()

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
