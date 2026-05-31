import enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry  # Essencial para lidar com o PostGIS (LatLng do Flutter)
from database import Base

# ==========================================
# 1. DEFINIÇÃO DOS ENUMS (Regras de Negócio)
# ==========================================

class StatusPrad(str, enum.Enum):
    em_dia = "em_dia"
    atrasado = "atrasado"

class SaudeMuda(str, enum.Enum):
    saudavel = "saudavel"
    doente = "doente"
    morta = "morta"

class StatusReserva(str, enum.Enum):
    reservado = "reservado"
    retirado = "retirado"
    cancelado = "cancelado"


# ==========================================
# 2. MODELOS DAS TABELAS (SQLAlchemy ORM)
# ==========================================

class UsuarioProdutor(Base):
    """
    Mapeia a tabela 'usuarios_produtores'.
    Responsável pelo gerenciamento do perfil do produtor rural,
    armazenando o ID gerado pelo Firebase Auth e o token de Push Notifications.
    """
    __tablename__ = "usuarios_produtores"

    id = Column(String(255), primary_key=True, index=True)  # UID do Firebase Auth enviado pelo Flutter
    nome = Column(String(150), nullable=False)
    numero_car = Column(String(100), nullable=False, index=True)  # Vinculo com o CAR do Tocantins
    status_prad = Column(Enum(StatusPrad, name="status_prad_enum"), default=StatusPrad.em_dia, nullable=False)
    device_token = Column(String(255), nullable=True)  # Token do FCM (Firebase Cloud Messaging)
    created_at = Column(DateTime, server_default=func.now())

    # Relacionamentos (Facilita buscas associadas na API)
    reservas = relationship("ReservaViveiro", back_populates="produtor", cascade="all, delete-orphan")
    leituras = relationship("LeituraPRAD", back_populates="produtor", cascade="all, delete-orphan")


class AlertaCidadao(Base):
    """
    Mapeia a tabela 'alertas_cidadao'.
    Módulo RN01 - Armazena denúncias georreferenciadas enviadas por cidadãos
    ou produtores (inclusive de forma anônima).
    """
    __tablename__ = "alertas_cidadao"

    id_alerta = Column(String(36), primary_key=True, server_default=func.gen_random_uuid())  # UUID nativo do banco
    usuario_id = Column(String(255), default="anonimo", nullable=False)  # 'anonimo' ou ID do Usuário
    
    # Campo Geográfico do PostGIS (Armazena Point com SRID 4326 - WGS84)
    geom_localizacao = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    
    exatidao_gps = Column(Float, nullable=True)  # Margem de erro em metros extraída do Flutter
    url_foto = Column(String(255), nullable=False)  # URL pública do bucket S3 ou Firebase Storage
    timestamp_captura = Column(DateTime, server_default=func.now(), nullable=False)
    status_webhook = Column(Boolean, default=False, nullable=False)  # Confirmação de envio ao CBM-TO (Sistema Protege)


class ReservaViveiro(Base):
    """
    Mapeia a tabela 'reservas_viveiro'.
    Módulo RN05 - Controla o fluxo de retirada de mudas nativas via QR Code.
    """
    __tablename__ = "reservas_viveiro"

    id_reserva = Column(String(50), primary_key=True)  # Conteúdo lido/gerado pelo QR Code (Ex: 'TK-881-A')
    produtor_id = Column(String(255), ForeignKey("usuarios_produtores.id", ondelete="CASCADE"), nullable=False)
    especie_id = Column(String(100), nullable=False)  # Chave de identificação da muda no catálogo
    viveiro_origem = Column(String(100), nullable=False)  # Ex: 'Viveiro Gurupi', 'Viveiro Palmas'
    quantidade = Column(Integer, nullable=False)
    status = Column(Enum(StatusReserva, name="status_reserva_enum"), default=StatusReserva.reservado, nullable=False)
    data_solicitacao = Column(DateTime, server_default=func.now(), nullable=False)

    # Relacionamento Reverso
    produtor = relationship("UsuarioProdutor", back_populates="reservas")


class LeituraPRAD(Base):
    """
    Mapeia a tabela 'leituras_prad'.
    Módulo RN04 - Auditoria Inteligente e Scanner de Restauração com Realidade Aumentada.
    """
    __tablename__ = "leitures_prad"

    id_leitura = Column(String(36), primary_key=True, server_default=func.gen_random_uuid())
    produtor_id = Column(String(255), ForeignKey("usuarios_produtores.id", ondelete="CASCADE"), nullable=False)
    especie_id = Column(String(100), nullable=False)
    altura_estimada_cm = Column(Float, nullable=False)  # Mapeado pela Visão Computacional / Régua A4
    saude_muda = Column(Enum(SaudeMuda, name="saude_muda_enum"), default=SaudeMuda.saudavel, nullable=False)
    url_foto_comprobatoria = Column(String(255), nullable=False)  # Imagem com a folha de referência
    
    # Validação Geográfica: Garante que a foto foi tirada dentro dos limites da fazenda
    geom_gps = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    
    sincronizado = Column(Boolean, default=True, nullable=False)  # Flag para o controle de sincronia local (SQLite -> Nuvem)
    timestamp_leitura = Column(DateTime, server_default=func.now(), nullable=False)

    # Relacionamento Reverso
    produtor = relationship("UsuarioProdutor", back_populates="leituras")