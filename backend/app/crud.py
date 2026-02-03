import io
#import uuid
from sqlalchemy.orm import Session
from . import models, schemas


def criar_funcionario(db: Session, func: schemas.FuncionarioCreate, foto: bytes | None, pdf: bytes | None ):

    #token_unico = str(uuid.uuid4())
    #url_perfil = f"{base_url}/perfil/{token_unico}"
    #qrcode_gerado = gerar_qrcode_bytes(url_perfil)
    
    db_func = models.Funcionario(
        nome=func.nome,
        cargo=func.cargo,
        foto=foto,
        #certificado_pdf=pdf,
        #uuid_perfil=token_unico, 
        #qrcode_img=qrcode_gerado
    )

    db.add(db_func)
    db.commit()
    db.refresh(db_func)
    return db_func

def listar_funcionarios(db: Session):
    return db.query(models.Funcionario).all()

def buscar_por_id(db: Session, funcionario_id: int):
    return db.query(models.Funcionario).filter(models.Funcionario.id == funcionario_id).first()

def excluir_funcionario(db: Session, funcionario_id: int):
    db_func = buscar_por_id(db, funcionario_id)
    if db_func:
        db.delete(db_func)
        db.commit()
    return db_func

def atualizar_funcionario(db: Session, funcionario_id: int, func_update: schemas.FuncionarioCreate, foto: bytes | None, pdf: bytes | None):
    db_func = buscar_por_id(db, funcionario_id)
    if db_func:
        db_func.nome = func_update.nome
        db_func.cargo = func_update.cargo
        # Só atualiza a foto ou PDF se novos arquivos forem enviados
        if foto:
            db_func.foto = foto
        if pdf:
            db_func.certificado_pdf = pdf
        db.commit()
        db.refresh(db_func)
    return db_func
