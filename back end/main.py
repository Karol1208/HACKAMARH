from fastapi import FastAPI
from routers import users, alertas, scanner
from services.scanner_restauracao import ScannerRestauracao

app = FastAPI(title="HACKAMARH API")

# Carrega o modelo YOLOv8 uma vez ao subir a API
@app.on_event("startup")
def startup():
    ScannerRestauracao.inicializar()

app.include_router(users.router)
app.include_router(alertas.router)
app.include_router(scanner.router)
