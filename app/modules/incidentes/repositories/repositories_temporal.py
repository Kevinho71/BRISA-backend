# app\modules\incidentes\repositories\repositories_temporal.py
from sqlalchemy.orm import Session
from app.modules.administracion.models.persona_models import Estudiante
from app.modules.incidentes.models.models_incidentes import SituacionIncidente
from app.shared.models import Persona
from app.modules.usuarios.models.usuario_models import Usuario, Rol, Persona1, usuario_roles_table


def get_estudiantes_repo(db: Session):
    estudiantes = db.query(Estudiante).all()
    return [
        {"id": e.id_estudiante, "nombre": e.nombre_completo}
        for e in estudiantes
    ]

def get_profesores_repo(db: Session):
    profesores = (
        db.query(Persona)
        .filter(Persona.tipo_persona == "profesor")
        .all()
    )

    resultados = []
    for p in profesores:
        nombre = " ".join([
            p.nombres,
            p.apellido_paterno,
            p.apellido_materno or ""
        ]).strip()

        resultados.append({
            "id": p.id_persona,
            "nombre": nombre,
        })

    return resultados

def get_situaciones_repo(db: Session):
    situaciones = db.query(SituacionIncidente).all()
    return [
        {
            "id": s.id_situacion,
            "nombre": s.nombre_situacion,
            "nivel": s.nivel_gravedad,
        }
        for s in situaciones
    ]

def get_roles_repo(db: Session):
    roles = db.query(Rol).filter(Rol.is_active == True).all()
    return [{"id": r.id_rol, "nombre": r.nombre} for r in roles]

def get_usuarios_por_rol_repo(db: Session, rol_nombre: str):
    rol = (
        db.query(Rol)
        .filter(Rol.nombre == rol_nombre)
        .filter(Rol.is_active == True)
        .first()
    )
    if not rol:
        return []

    filas = (
        db.query(Usuario, Persona1)
        .join(usuario_roles_table, usuario_roles_table.c.id_usuario == Usuario.id_usuario)
        .join(Persona1, Persona1.id_persona == Usuario.id_persona)
        .filter(usuario_roles_table.c.id_rol == rol.id_rol)
        .filter(usuario_roles_table.c.estado == "activo")
        .filter(Usuario.is_active == True)
        .all()
    )

    resultados = []
    for u, p in filas:
        nombre = " ".join([
            p.nombres,
            p.apellido_paterno,
            p.apellido_materno or ""
        ]).strip()

        resultados.append({
            "id": u.id_usuario,
            "nombre": nombre,
        })

    return resultados