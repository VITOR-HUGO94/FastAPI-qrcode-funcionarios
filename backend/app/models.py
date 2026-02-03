from sqlalchemy import Column, Integer, String, LargeBinary
from .database import Base
import uuid

class Funcionario(Base):
    __tablename__ = "funcionarios" # Nome da tabela no Postgres 

    id = Column(Integer, primary_key=True, index=True) 
    nome = Column(String, nullable=False) 
    cargo = Column(String, nullable=False) 
    foto = Column(LargeBinary) 
    certificado_pdf = Column(LargeBinary)

    # Geramos o UUID automaticamente se não for fornecido 
    uuid_perfil = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    qrcode_img = Column(LargeBinary) 