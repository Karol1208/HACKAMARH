import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # ALTERADO AQUI

# 1. Ler configuração via variáveis de ambiente
host = os.getenv('DB_HOST', '127.0.0.1')
port = os.getenv('DB_PORT', '5432')
database = os.getenv('DB_NAME', 'hackamarh')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD')
if not password:
    raise RuntimeError("Variável de ambiente DB_PASSWORD não definida. Configure antes de iniciar o servidor.")

# 2. Montar a URL de conexão que o SQLAlchemy e o GeoAlchemy2 precisam
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# 3. Criar o Engine de conexão
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # Testa a conexão antes de usá-la (evita quedas)
)

# 4. Criar a fábrica de sessões para as rotas do FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. A Base que seus modelos em models.py herdam
Base = declarative_base()

# Função auxiliar para suas rotas obterem uma conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

