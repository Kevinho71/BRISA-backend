# app\modules\incidentes\services\services_temporal.py
from sqlalchemy.orm import Session
from app.modules.incidentes.repositories.repositories_temporal import get_estudiantes_repo, get_situaciones_repo, get_profesores_repo, get_roles_repo, get_usuarios_por_rol_repo

def get_estudiantes_service(db: Session):
    return get_estudiantes_repo(db)

def get_profesores_service(db: Session):
    return get_profesores_repo(db)

def get_situaciones_service(db: Session):
    return get_situaciones_repo(db)

def get_roles_service(db: Session):
    return get_roles_repo(db)

def get_usuarios_por_rol_service(db: Session, rol_nombre: str):
    return get_usuarios_por_rol_repo(db, rol_nombre)