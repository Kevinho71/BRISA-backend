# app/main.py
from fastapi import Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy.orm import Session

# Middleware JWT
from app.core.middleware.jwt_middleware import JWTMiddleware

# DB
from app.core.database import get_db

# Exception handlers
from app.shared.exceptions.custom_exceptions import register_exception_handlers

# Routers
from app.modules.auth.controllers import auth_controller
from app.modules.usuarios.controllers import usuario_controller
from app.modules.bitacora.controllers import bitacora_controller
from app.modules.esquelas.controllers import esquela_controller, codigo_esquela_controller
from app.modules.administracion.controllers import curso_controller
from app.modules.administracion.controllers import administrativo_controller
from app.modules.administracion.controllers import materia_controller
from app.modules.reportes.controllers import reporte_controller
from app.modules.incidentes.controllers import controllers_incidentes

# ✅ NUEVO: Router de profesores
from app.modules.profesores.controllers import profesor_controller

# ✅ NUEVO: Routers de Retiros Tempranos
from app.modules.retiros_tempranos.controllers import (
    motivo_retiro_controller,
    solicitud_retiro_controller,
    solicitud_retiro_masivo_controller,
    registro_salida_controller,
    autorizacion_retiro_controller,
    estudiante_apoderado_controller
)

# ✅ NUEVO: Routers de Estudiantes, Cursos y Asignaciones
from app.modules.estudiantes.controllers import estudiante_controller
from app.modules.cursos.controllers import curso_controller as nuevo_curso_controller
from app.modules.estudiantes_cursos.controllers import asignacion_controller

# Servicios
from app.modules.auth.services.auth_service import AuthService

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

from fastapi import Request

# ========================= MIDDLEWARE =========================

# Orden de ejecución: INVERSO al orden de declaración
# 1. CORS (última línea, se ejecuta primero)
# 2. JWT (se ejecuta segundo, valida token e inyecta usuario)
# Middlewares se ejecutan en orden INVERSO cuando se agregan con add_middleware

app.add_middleware(JWTMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================= EXCEPTION HANDLERS =========================
register_exception_handlers(app)

# ========================= ROUTERS =========================
app.include_router(auth_controller.router,    prefix="/api/auth",     tags=["Autenticación"])
app.include_router(usuario_controller.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(bitacora_controller.router, prefix="/api/bitacora", tags=["Bitácora"])

# Routes SIA
app.include_router(controllers_incidentes.router, prefix="/api/incidentes", tags=["Incidentes"])

# Nuevos módulos
app.include_router(esquela_controller.router, prefix="/api") 
app.include_router(codigo_esquela_controller.router, prefix="/api")
app.include_router(curso_controller.router, prefix="/api")
app.include_router(materia_controller.router, prefix="/api")
app.include_router(administrativo_controller.router)
app.include_router(reporte_controller.router, prefix="/api")

# ✅ NUEVO: Profesores
app.include_router(profesor_controller.router, prefix="/api", tags=["Profesores"])

# ✅ NUEVO: Retiros Tempranos
from app.modules.retiros_tempranos.controllers import upload_controller
app.include_router(motivo_retiro_controller.router)
app.include_router(solicitud_retiro_controller.router)
app.include_router(solicitud_retiro_masivo_controller.router)
app.include_router(registro_salida_controller.router)
app.include_router(autorizacion_retiro_controller.router)
app.include_router(estudiante_apoderado_controller.router)
app.include_router(upload_controller.router)

# ✅ NUEVO: Estudiantes, Cursos y Asignaciones
app.include_router(estudiante_controller.router, prefix="/api", tags=["Estudiantes"])
app.include_router(nuevo_curso_controller.router, prefix="/api", tags=["Cursos"])
app.include_router(asignacion_controller.router, prefix="/api", tags=["Asignaciones"])

# ✅ INCIDENCIAS EXACTAMENTE COMO TU FRONT LAS USA
app.include_router(
    controllers_incidentes.router,
    prefix="/api", 
    tags=["Incidentes"]
)

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
    logger.info("👨‍🏫 Módulo de Profesores cargado")
    logger.info("🚸 Módulo de Retiros Tempranos cargado")
    logger.info("👨‍🎓 Módulo de Estudiantes cargado")
    logger.info("📚 Módulo de Cursos cargado")
    logger.info("🔗 Módulo de Asignaciones cargado")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 API cerrándose")

# ========================= ARCHIVOS ESTÁTICOS =========================
# Servir archivos subidos (fotos de evidencia, etc.)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ========================= DEBUG TOKEN =========================
@app.get("/debug-token")
def debug_token(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "") if authorization else ""
    user = AuthService.get_current_user(db, token)
    return {"user": user.usuario}

# ========================= RUN SERVER =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)