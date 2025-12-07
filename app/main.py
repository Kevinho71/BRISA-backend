# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# Middleware JWT
from app.core.middleware.jwt_middleware import JWTMiddleware

# Exception handlers
from app.shared.exceptions.custom_exceptions import register_exception_handlers

# Routers
from app.modules.auth.controllers import auth_controller
from app.modules.usuarios.controllers import usuario_controller
from app.modules.bitacora.controllers import bitacora_controller
# from app.modules.reportes.controllers import reportes_controller
from app.modules.incidentes.controllers import controllers_incidentes

load_dotenv()

# ========================= LOGGING =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("uvicorn")

# ========================= APP =========================
app = FastAPI(
    title=os.getenv("API_TITLE", "API Bienestar Estudiantil"),
    version=os.getenv("API_VERSION", "1.0.0"),
    description="Sistema de gestión de usuarios, roles, permisos y bitácora",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ========================= MIDDLEWARE =========================

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Middleware (DESPUÉS de CORS)
app.add_middleware(JWTMiddleware)

# ========================= EXCEPTION HANDLERS =========================
register_exception_handlers(app)

# ========================= ROUTERS =========================
app.include_router(auth_controller.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(usuario_controller.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(bitacora_controller.router, prefix="/api/bitacora", tags=["Bitácora"])
# app.include_router(reportes_controller.router, prefix="/api/reportes", tags=["Reportes"])
app.include_router(controllers_incidentes.router, prefix="/api/incidentes", tags=["Incidentes"])

# ========================= ROOT =========================
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Bienvenido a la API de Bienestar Estudiantil",
        "version": os.getenv("API_VERSION", "1.0.0")
    }

# ========================= HEALTH CHECK =========================
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API funcionando"}

# ========================= STARTUP/SHUTDOWN =========================
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Iniciando API Bienestar Estudiantil")
    logger.info("🔐 Middleware JWT cargado")
    logger.info("📦 Routers cargados correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 API cerrándose")

# ========================= DEBUG TOKEN (Opcional para desarrollo) =========================
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.services.auth_service import AuthService

@app.get("/debug-token")
def debug_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = AuthService.get_current_user(db, token)
    return {"user": user.usuario}

# ========================= RUN SERVER (dev) =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
