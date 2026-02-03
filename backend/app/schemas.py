from pydantic import BaseModel
from typing import Optional

class FuncionarioBase(BaseModel):
    nome: str 
    cargo: str 

class FuncionarioCreate(FuncionarioBase):
    pass # Por enquanto, criar usa os mesmos campos da base 

class Funcionario(FuncionarioBase):
    id: int 
    #uuid_perfil: str 

    class Config:
        # Essencial para que o Pydantic entenda objetos do SQLAlchemy 
        from_attributes = True