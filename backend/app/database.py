from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Buscamos a URL do banco das variáveis de ambiente para segurança
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/funcionarios")

# O motor que gerencia a comunicação 
engine = create_engine(DATABASE_URL)

# Fábrica de sessões: cada requisição terá sua própria "conversa" com o banco 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que todos os nossos modelos vão herdar 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()