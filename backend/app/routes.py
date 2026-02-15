import base64
from . import models, auth, crud, schemas 
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import get_db, SessionLocal

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

templates = Jinja2Templates(directory="/frontend/templates")



# Filtro customizado para exibir imagens bytes no HTML
def base64_filter(data):
    if not data: return ""
    return base64.b64encode(data).decode('utf-8')

templates.env.filters["b64encode"] = base64_filter

#Rota para exibir a lista (index.html)
@router.get("/", response_class=HTMLResponse)
async def listar_view(request: Request, db: Session = Depends(get_db)):
    funcionarios = crud.listar_funcionarios(db)
    return templates.TemplateResponse("index.html", {"request": request,"funcionarios": funcionarios})

@router.post("/cadastrar", response_class=HTMLResponse)
async def cadastrar_funcionario(
    nome: str = Form(...),
    cargo: str = Form(...),
    foto: UploadFile = File(None),
    certificado: UploadFile = File(None),
    db: Session = Depends(get_db),
    #current_user: models.User = Depends(auth.get_current_user)
    
):
    foto_bytes = await foto.read() if foto else None
    pdf_bytes = await certificado.read() if certificado else None

    obj_create = schemas.FuncionarioCreate(nome=nome, cargo=cargo)

    crud.criar_funcionario(db, obj_create, foto_bytes, pdf_bytes, base_url="http://localhost:8000")

    return RedirectResponse(url="/", status_code=303)


@router.get("/novo", response_class=HTMLResponse)
async def novo_funcionario(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@router.get("/editar/{funcionario_id}", response_class=HTMLResponse)
async def editar_funcionario(
    request: Request,
    funcionario_id: int,
    db: Session = Depends(get_db)
):
    funcionario = crud.buscar_por_id(db, funcionario_id)

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return templates.TemplateResponse("editar.html", {"request": request, "f": funcionario})


@router.post("/atualizar/{funcionario_id}")
async def atualizar_funcionario(
    funcionario_id: int,
    nome: str = Form(...),
    cargo: str = Form(...),
    foto: UploadFile = File(None),
    certificado: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    foto_bytes = await foto.read() if foto else None
    pdf_bytes = await certificado.read() if certificado else None

    obj_update = schemas.FuncionarioCreate(
        nome=nome,
        cargo=cargo
    )

    funcionario = crud.atualizar_funcionario(
        db,
        funcionario_id,
        obj_update,
        foto_bytes,
        pdf_bytes
    )

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return RedirectResponse(url="/", status_code=303)

@router.post("/excluir/{funcionario_id}")
async def excluir_funcionario(
    funcionario_id: int,
    db: Session = Depends(get_db)
):
    funcionario = crud.excluir_funcionario(db, funcionario_id)

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return RedirectResponse(url="/", status_code=303)


@router.get("/perfil/{uuid_perfil}", response_class=HTMLResponse)
async def visualizar_perfil(request: Request, uuid_perfil: str, db: Session = Depends(get_db)):
    # 1. Busca o funcionário pelo UUID (usando a função do CRUD)
    funcionario = crud.buscar_por_uuid(db, uuid_perfil)
    
    # 2. Se não encontrar, lança erro 404
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    # 3. Renderiza o template exclusivo de perfil
    return templates.TemplateResponse("perfil.html", {"request": request, "f": funcionario})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/token") # O nome padrão costuma ser /token ou /login
async def login_para_acesso_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Busca o usuário no banco
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Valida o usuário e a senha (usando o hash que criamos na auth.py)
    if not user or not auth.verificar_senha(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Cria o "envelope" do token (o campo 'sub' é o padrão para o identificador)
    access_token = auth.criar_token_acesso(data={"sub": user.username})

    # 4. Retorna o token seguindo o padrão OAuth2
    return {"access_token": access_token, "token_type": "bearer"}