# backend/app/main.py
from fastapi import FastAPI
from .routes import router # Importa o router do seu arquivo routes.py
from .database import engine, Base # Importa a engine para criar as tabelas

Base.metadata.create_all(bind=engine)
app = FastAPI() # Inicializa a instância do framework 
app.include_router(router)
@app.get("/health") # Rota de diagnóstico para verificar se o container está vivo
def health_check():
    return {"status": "healthy", "version": "1.0.0"} 