# backend/app/main.py
from fastapi import FastAPI

app = FastAPI() # Inicializa a instância do framework [cite: 74]

@app.get("/health") # Rota de diagnóstico para verificar se o container está vivo [cite: 76]
def health_check():
    return {"status": "healthy", "version": "1.0.0"} 