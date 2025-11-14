from fastapi import FastAPI, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi import Depends

# NUEVA LÍNEA 1: Importar el registro de handlers
from app.shared.exceptions.custom_exceptions import register_exception_handlers

# Importar routers
from app.modules.usuarios.controllers import usuario_controller
from app.modules.auth.controllers import auth_controller
from app.modules.bitacora.controllers import bitacora_controller
from app.modules.esquelas.controllers import esquela_controller, codigo_esquela_controller
from app.modules.administracion.controllers import curso_controller, estudiante_controller
from app.modules.administracion.controllers.persona_controller import (
    estudiantes_router, profesores_router, registradores_router
)
#from app.modules.reportes.controllers import reportes_controller
from app.modules.usuarios.models.usuario_models import Usuario
from app.modules.auth.services.auth_service import AuthService
from sqlalchemy.orm import Session
from app.core.database import get_db
# from app.core.extensions import router as auth_router  # Comentado: usar auth_controller en su lugar

load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title=os.getenv("API_TITLE", "API Bienestar Estudiantil"),
    version=os.getenv("API_VERSION", "1.0.0"),
    description="Sistema completo de gestión de usuarios, roles, permisos y bitácora"
)

# Configurar CORS
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

# NUEVA LÍNEA 2: Registrar manejadores de excepciones personalizadas
register_exception_handlers(app)

# Incluir routers
app.include_router(auth_controller.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(usuario_controller.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(bitacora_controller.router, prefix="/api/bitacora", tags=["Bitácora"])
app.include_router(esquela_controller.router, prefix="/api")
app.include_router(codigo_esquela_controller.router, prefix="/api")
app.include_router(curso_controller.router, prefix="/api")
app.include_router(estudiante_controller.router, prefix="/api")
app.include_router(estudiantes_router, prefix="/api")
app.include_router(profesores_router, prefix="/api")
app.include_router(registradores_router, prefix="/api")
#app.include_router(reportes_controller.router, prefix="/api/reportes", tags=["Reportes"])

@app.get("/")
def read_root():
    """Endpoint raíz de bienvenida"""
    return {
        "status": "success",
        "message": "Bienvenido a la API de Bienestar Estudiantil",
        "version": os.getenv("API_VERSION", "1.0.0")
    }

@app.get("/health")
def health_check():
    """Health check del servidor"""
    return {"status": "ok", "message": "API en funcionamiento"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# Alias temporal para mantener get_current_user
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> Usuario:
    token = authorization.replace("Bearer ", "")
    return AuthService.get_current_user(db, token)


@app.get("/debug-token")
def debug_token(current_user: Usuario = Depends(get_current_user)):
    return {"user": current_user.usuario}