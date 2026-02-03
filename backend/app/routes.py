import base64
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas

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
