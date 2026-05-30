from fastapi import FastAPI
from routers import users

app = FastAPI(title="HACKAMARH API")

app.include_router(users.router)
