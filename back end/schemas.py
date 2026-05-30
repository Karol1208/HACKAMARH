from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Literal

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


# --- Dashboard ---

class KPIs(BaseModel):
    mudas_atestadas: int
    sobrevivencia_pct: float
    drones_ativos: int
    infracoes_sem_licenca: int
    selos_verdes: int


# --- Mapa ---

class PontoMapa(BaseModel):
    lat: float
    lng: float
    tipo: Literal["foco_incendio", "drone", "propriedade"]
    titulo: str
    descricao: str

class PoligonoMapa(BaseModel):
    coordenadas: list[list[float]]
    titulo: str
    descricao: str
    status: str


# --- Alertas ---

class AlertaResposta(BaseModel):
    id: int
    origem: Literal["app_cidadao", "planet_labs", "app_produtor"]
    titulo: str
    descricao: str
    porte_car: Literal["P", "M", "G"]
    status_licenca: Literal["ativa", "vencida", "sem_licenca", "aprovado"]
    criado_em: datetime


# --- Propriedades ---

class PropriedadeResposta(BaseModel):
    numero_car: str
    municipio: str
    produtor: str
    porte: Literal["P", "M", "G"]


# --- Notificações ---

class NotificacaoResposta(BaseModel):
    id: int
    titulo: str
    tipo: Literal["alerta", "infração", "aprovacao"]
    lida: bool
    criado_em: datetime


# --- Solicitações de Acesso ---

OrgaoLotacao = Literal["semarh", "naturatins", "bombeiros", "sedesc"]
StatusSolicitacao = Literal["pendente", "aprovada", "rejeitada"]

class SolicitacaoCriar(BaseModel):
    nome: str
    email: EmailStr
    orgao: OrgaoLotacao
    matricula: str

    @field_validator("email")
    @classmethod
    def validar_email_institucional(cls, v: str) -> str:
        # Apenas emails institucionais do governo do Tocantins são aceitos
        if not v.endswith("@to.gov.br"):
            raise ValueError("E-mail deve ser institucional (@to.gov.br)")
        return v

class SolicitacaoResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr
    orgao: OrgaoLotacao
    matricula: str
    status: StatusSolicitacao
    criado_em: datetime
