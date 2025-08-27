from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco
DATABASE_URL = 'sqlite:///cars.db'

# Cria o motor de conexão com o banco
engine = create_engine(DATABASE_URL)

# Configura de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declara tabelas do meu banco de dados
Base = declarative_base()


# Dependência para obter a sessão e garantir que será fechada no fim
def get_session():
    session = SessionLocal()
    try:
        yield session  # fornece a sessão para uso
    finally:
        session.close()  # garante que fecha depois
