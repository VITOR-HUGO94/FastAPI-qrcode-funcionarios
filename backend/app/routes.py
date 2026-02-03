import base64
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.app.models import User
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas
from fastapi import HTTPException
from .auth import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="/frontend/templates")

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

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
    current_user: User = Depends(get_current_user)
    
):
    foto_bytes = await foto.read() if foto else None
    pdf_bytes = await certificado.read() if certificado else None

    obj_create = schemas.FuncionarioCreate(nome=nome, cargo=cargo)

    crud.criar_funcionario(db, obj_create, foto_bytes, pdf_bytes, base_url="http://localhost:8000")

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

