"""
CloudSalud Copiloto ESE - Application Entrypoint
Servidor FastAPI con soporte para endpoints REST, WebSockets, RAG, Text-to-SQL y frontend integrado.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.seed_data import seed_database
from app.api.chat import router as chat_router
from app.api.dashboard import router as dashboard_router
from app.api.audit import router as audit_router
from app.api.implementation import router as implementation_router

app = FastAPI(
    title="CloudSalud - Copiloto Gerencial para ESE en Colombia",
    description="Asistente de IA Estratégico, Proactivo y Especializado para Gerentes de Hospitales Públicos (ESE)",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar y poblar base de datos en el inicio
@app.on_event("startup")
def on_startup():
    print("Iniciando CloudSalud ESE Engine...")
    seed_database()
    print("Base de datos verificada y lista.")

# Registrar rutas de API
app.include_router(chat_router)
app.include_router(dashboard_router)
app.include_router(audit_router)
app.include_router(implementation_router)

# Servir Frontend Estático
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
