from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Literal, List, Optional

# --- Usuários Internos e Governamentais ---

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

    model_config = {"from_attributes": True}


# --- App Canindé: Produtores Rurais ---

class UsuarioProdutorBase(BaseModel):
    nome: str
    numero_car: str
    device_token: str | None = None

class UsuarioProdutorCriar(UsuarioProdutorBase):
    id: str  # ID vindo do Firebase Auth no Flutter

class UsuarioProdutorAtualizar(BaseModel):
    nome: str | None = None
    numero_car: str | None = None
    status_prad: Literal["em_dia", "atrasado"] | None = None
    device_token: str | None = None

class UsuarioProdutorResposta(UsuarioProdutorBase):
    id: str
    status_prad: Literal["em_dia", "atrasado"]
    created_at: datetime

    model_config = {"from_attributes": True}


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


# --- Alertas Cidadão (RN01) ---

class AlertaCidadaoCriar(BaseModel):
    usuario_id: str = "anonimo"
    latitude: float
    longitude: float
    exatidao_gps: float
    url_foto: str

class AlertaCidadaoResposta(BaseModel):
    id_alerta: str
    usuario_id: str
    exatidao_gps: float | None
    url_foto: str
    timestamp_captura: datetime
    status_webhook: bool

    model_config = {"from_attributes": True}


# --- Propriedades ---

class PropriedadeResposta(BaseModel):
    numero_car: str
    municipio: str
    produtor: str
    porte: Literal["P", "M", "G"]


# --- Reservas Viveiro (RN05) ---

class ReservaViveiroCriar(BaseModel):
    id_reserva: str  # Código alfa-numérico do QR Code
    produtor_id: str
    especie_id: str
    viveiro_origem: str
    quantidade: int

class ReservaViveiroAtualizarStatus(BaseModel):
    status: Literal["reservado", "retirado", "cancelado"]

class ReservaViveiroResposta(BaseModel):
    id_reserva: str
    produtor_id: str
    especie_id: str
    viveiro_origem: str
    quantidade: int
    status: Literal["reservado", "retirado", "cancelado"]
    data_solicitacao: datetime

    model_config = {"from_attributes": True}


# --- Leituras PRAD (RN04) ---

class LeituraPRADCriar(BaseModel):
    produtor_id: str
    especie_id: str
    altura_estimada_cm: float
    saude_muda: Literal["saudavel", "doente", "morta"]
    url_foto_comprobatoria: str
    latitude: float
    longitude: float
    sincronizado: bool = True

class LeituraPRADResposta(BaseModel):
    id_leitura: str
    produtor_id: str
    especie_id: str
    altura_estimada_cm: float
    saude_muda: Literal["saudavel", "doente", "morta"]
    url_foto_comprobatoria: str
    sincronizado: bool
    timestamp_leitura: datetime

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}

# --- Viveiros / Kanban ---

class SemeaduraCriar(BaseModel):
    especie: str
    viveiro: str
    destino: str = "A definir"

class LoteResposta(BaseModel):
    id: int
    lote: str
    especie: str
    viveiro: str
    destino: str
    germinacao_pct: float
    dias_restantes: int
    estagio: str

