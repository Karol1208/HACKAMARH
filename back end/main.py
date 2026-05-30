from fastapi import FastAPI
from routers import users, alertas, scanner, dashboard, mapa, propriedades, notificacoes, solicitacoes
from services.scanner_restauracao import ScannerRestauracao

app = FastAPI(title="HACKAMARH API")

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
