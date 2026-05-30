from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCriar(UsuarioBase):
    senha: str

class UsuarioAtualizar(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None

class UsuarioResposta(UsuarioBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
