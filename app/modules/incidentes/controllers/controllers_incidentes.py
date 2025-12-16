# app/modules/incidentes/controllers/controllers_incidentes.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os, shutil
from typing import Optional, List
import traceback

from app.core.database import get_db
from app.modules.incidentes.dto.dto_areas import AreaCreateDTO, AreaUpdateDTO
from app.modules.incidentes.dto.dto_situaciones import SituacionCreateDTO, SituacionUpdateDTO
from app.modules.incidentes.dto.dto_incidentes import IncidenteCreateDTO, IncidenteResponseDTO
# from app.modules.incidentes.dto.dto_modificaciones import ModificacionUpdate
# from app.modules.incidentes.dto.dto_derivaciones import DerivarIncidente

from app.modules.incidentes.services.services_areas import AreaService
from app.modules.incidentes.services.services_situaciones import SituacionService
# from app.modules.incidentes.services.services_adjuntos import AdjuntoService
from app.modules.incidentes.services.services_incidentes import IncidenteService
# from app.modules.incidentes.services.services_modificaciones import ModificacionesService
# from app.modules.incidentes.services.services_derivaciones import DerivacionesService

from app.modules.incidentes.dto.dto_incidentes import IncidenteCreateDTO, IncidenteResponseDTO
from app.modules.incidentes.services.services_temporal import get_estudiantes_service
from app.modules.incidentes.dto.dto_temporal import EstudianteSimple

from app.modules.incidentes.services.services_temporal import get_profesores_service
from app.modules.incidentes.dto.dto_temporal import ProfesorSimple

from app.modules.incidentes.services.services_temporal import get_situaciones_service
from app.modules.incidentes.dto.dto_temporal import SituacionSimple

from app.modules.incidentes.services.services_temporal import get_roles_service
from app.modules.incidentes.dto.dto_temporal import RolSimple

from app.modules.incidentes.services.services_temporal import get_usuarios_por_rol_service
from app.modules.incidentes.dto.dto_temporal import UsuarioSimple

from app.modules.incidentes.dto.dto_modificaciones import (
    IncidenteUpdateDTO,
    ModificacionResponseDTO
)

from app.modules.incidentes.services.services_incidentes import IncidenteService
from app.modules.incidentes.services.services_modificaciones import historial_incidente_service

from app.modules.incidentes.dto.dto_adjuntos import AdjuntoRead
from app.modules.incidentes.services.services_adjuntos import AdjuntoService

from app.modules.incidentes.services.services_detalles import DetallesService
from app.modules.incidentes.dto.dto_detalles import IncidenteDetalles

from app.modules.incidentes.services.services_derivaciones import DerivacionService
from app.modules.incidentes.dto.dto_derivaciones import DerivacionCreate, DerivacionRead

from app.modules.incidentes.services.services_notificaciones import NotificacionService
from app.modules.incidentes.dto.dto_notificaiones import (
    NotificacionOutDTO
)

from app.modules.auth.services.auth_service import get_current_user_dependency

router = APIRouter(prefix="/Incidentes", tags=["Incidentes"])

MEDIA_DIR = os.getenv("MEDIA_DIR", "uploads")
os.makedirs(MEDIA_DIR, exist_ok=True)

DIRECTOR_ROLE_ID = 1
DIRECTOR_NAMES = {"director", "director de nivel", "direccion", "dirección"}

def _norm(value) -> str:
    return str(value or "").strip().lower()

def require_director(current_user=Depends(get_current_user_dependency)):
    # 0) admin pasa
    if bool(getattr(current_user, "es_administrador", False)):
        return current_user

    # 1) rol directo como string (si existe)
    rol_txt = _norm(getattr(current_user, "rol", None))
    if rol_txt and any(name in rol_txt for name in DIRECTOR_NAMES):
        return current_user

    # 2) roles[] (si existe)
    roles = getattr(current_user, "roles", None) or []
    for r in roles:
        is_active = getattr(r, "is_active", True)
        if is_active is False:
            continue

        rid = getattr(r, "id_rol", None) or getattr(r, "id", None) or getattr(r, "role_id", None)
        rname = _norm(getattr(r, "nombre", None) or getattr(r, "nombre_rol", None) or getattr(r, "rol", None) or r)

        if rid == DIRECTOR_ROLE_ID:
            return current_user
        if rname and any(name in rname for name in DIRECTOR_NAMES):
            return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Solo el Director puede realizar esta acción"
    )

@router.get("/permisos/director")
def permiso_director(current_user=Depends(get_current_user_dependency)):
    try:
        require_director(current_user)
        return {"isDirector": True}
    except HTTPException:
        return {"isDirector": False}

#----AREAS----

@router.get("/areas")
def obtener_areas(db: Session = Depends(get_db)):
    svc = AreaService()
    return svc.listar_areas(db)

@router.get("/areas/{id_area}")
def obtener_area(id_area: int, db: Session = Depends(get_db)):
    svc = AreaService()
    return svc.obtener_area(db, id_area)

@router.post("/areas", status_code=201)
def crear_area(
    dto: AreaCreateDTO,
    db: Session = Depends(get_db),
    _user=Depends(require_director)
):
    svc = AreaService()
    return svc.crear_area(db, dto)

@router.put("/areas/{id_area}")
def actualizar_area(
    id_area: int,
    dto: AreaUpdateDTO,
    db: Session = Depends(get_db),
    _user=Depends(require_director)
):
    svc = AreaService()
    return svc.actualizar_area(db, id_area, dto)

@router.delete("/areas/{id_area}")
def eliminar_area(
    id_area: int,
    db: Session = Depends(get_db),
    _user=Depends(require_director)
):
    svc = AreaService()
    return svc.eliminar_area(db, id_area)

#----AREAS----


#----SITUACIONES----

@router.get("/situaciones")
def listar_todas_situaciones(db: Session = Depends(get_db)):
    svc = SituacionService(db)
    return svc.listar_todas()

# POST — crear nueva situación
@router.post("/situaciones", status_code=201)
def crear_situacion(dto: SituacionCreateDTO, db: Session = Depends(get_db)):
    svc = SituacionService(db)
    return svc.crear(dto)

# PATCH — actualizar una situación (SOLO DIRECTOR)
@router.patch("/situaciones/{id_situacion}")
def actualizar_situacion(
    id_situacion: int,
    dto: SituacionUpdateDTO,
    db: Session = Depends(get_db),
    _user=Depends(require_director)
):
    svc = SituacionService(db)
    return svc.actualizar(id_situacion, dto)


# DELETE — eliminar una situación (SOLO DIRECTOR)
@router.delete("/situaciones/{id_situacion}")
def eliminar_situacion(
    id_situacion: int,
    db: Session = Depends(get_db),
    _user=Depends(require_director)
):
    svc = SituacionService(db)
    return svc.eliminar(id_situacion)

#----SITUACIONES----


#----INCIDENTES----
@router.get("/incidentes", response_model=List[IncidenteResponseDTO])
def obtener_incidentes(db: Session = Depends(get_db)):
    service = IncidenteService(db)
    return service.obtener_incidentes()

@router.post("/incidentes", response_model=IncidenteResponseDTO)
def crear_incidente(dto: IncidenteCreateDTO, db: Session = Depends(get_db)):
    service = IncidenteService(db)
    nuevo = service.crear_incidente(dto)
    return IncidenteResponseDTO(
        id_incidente=nuevo.id_incidente,
        fecha=nuevo.fecha,
        antecedentes=nuevo.antecedentes,
        acciones_tomadas=nuevo.acciones_tomadas,
        seguimiento=nuevo.seguimiento,
        estado=nuevo.estado,
        id_responsable=nuevo.id_responsable,
        responsable_usuario=nuevo.responsable.usuario if nuevo.responsable else None
    )
#----INCIDENTES----


#----DETALLES----
@router.get("/detalles/{id_incidente}", response_model=IncidenteDetalles)
def obtener_detalles(id_incidente: int, db: Session = Depends(get_db)):
    service = DetallesService(db)
    data = service.obtener_detalles(id_incidente)

    if not data:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    return data
#----DETALLES----


#----TEMPORALES----
# --- Estudiantes ---
@router.get("/estudiantes-temporal", response_model=list[EstudianteSimple])
def listar_estudiantes(db: Session = Depends(get_db)):
    return get_estudiantes_service(db)

# --- Profesores ---
@router.get("/profesores-temporal", response_model=list[ProfesorSimple])
def listar_profesores(db: Session = Depends(get_db)):
    return get_profesores_service(db)

# --- Situaciones ---
@router.get("/situaciones-temporal", response_model=list[SituacionSimple])
def listar_situaciones(db: Session = Depends(get_db)):
    return get_situaciones_service(db)

# --- Roles ---
@router.get("/roles-temporal", response_model=list[RolSimple])
def listar_roles(db: Session = Depends(get_db)):
    return get_roles_service(db)

# --- Usuarios por Rol ---
@router.get("/usuarios-por-rol-temporal/{rol_nombre}", response_model=list[UsuarioSimple])
def listar_usuarios_por_rol(rol_nombre: str, db: Session = Depends(get_db)):
    return get_usuarios_por_rol_service(db, rol_nombre)
#----TEMPORALES----


#----MODIFICACIONES----
@router.patch("/modificaciones/{id_incidente}")
def modificar_incidente(id_incidente: int, dto: IncidenteUpdateDTO, db: Session = Depends(get_db)):
    service = IncidenteService(db)
    return service.modificar_incidente(id_incidente, dto)


@router.get("/modificaciones/{id_incidente}", response_model=list[ModificacionResponseDTO])
def obtener_historial(id_incidente: int, db: Session = Depends(get_db)):
    return historial_incidente_service(db, id_incidente)
#----MODIFICACIONES----


#----ADJUNTOS----
# SUBIR ADJUNTO
@router.post("/adjuntos/{id_incidente}", response_model=AdjuntoRead)
def subir_adjunto(
    id_incidente: int,
    archivo: UploadFile = File(...),
    id_subido_por: int | None = None,
    db: Session = Depends(get_db)
):
    service = AdjuntoService(db)
    return service.subir(id_incidente, archivo, id_subido_por)


# LISTAR POR INCIDENTE
@router.get("/adjuntos/{id_incidente}", response_model=list[AdjuntoRead])
def listar_adjuntos(id_incidente: int, db: Session = Depends(get_db)):
    service = AdjuntoService(db)
    return service.listar_por_incidente(id_incidente)


# DESCARGAR ARCHIVO POR ID
@router.get("/adjuntos/{id_adjunto}")
def descargar_adjunto(id_adjunto: int, db: Session = Depends(get_db)):
    service = AdjuntoService(db)
    adj = service.descargar(id_adjunto)

    if not adj:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(path=adj.ruta, filename=adj.nombre_archivo, media_type=adj.tipo_mime)


# BORRAR ARCHIVO POR ID
@router.delete("/adjuntos/{id_adjunto}")
def borrar_adjunto(id_adjunto: int, db: Session = Depends(get_db)):
    service = AdjuntoService(db)
    ok = service.borrar_por_id(id_adjunto)

    if not ok:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")

    return {"mensaje": "Adjunto eliminado", "id": id_adjunto}


#----ADJUNTOS----

#----DERIVACIONES----
@router.post("/derivaciones/{id_incidente}", response_model=DerivacionRead)
def crear_derivacion(id_incidente: int, data: DerivacionCreate, db: Session = Depends(get_db)):
    service = DerivacionService(db)
    try:
        return service.derivar(id_incidente, data)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))

#----DERIVACIONES----

#----NOTIFICACIONES----
@router.get("/notificaciones/{id_usuario}", response_model=list[NotificacionOutDTO])
def listar_notificaciones(
    id_usuario: int,
    solo_no_leidas: bool = False,
    limit: int | None = None,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)
    return service.listar_por_usuario(id_usuario, solo_no_leidas, limit)


@router.patch("/notificaciones/{id_notificacion}/leer", response_model=NotificacionOutDTO)
def marcar_notificacion_leida(
    id_notificacion: int,
    id_usuario: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)
    return service.marcar_como_leida(id_notificacion, id_usuario_actual=id_usuario)


@router.patch("/notificaciones/{id_usuario}/leer-todas")
def marcar_todas_leidas(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)
    cantidad = service.marcar_todas_como_leidas(id_usuario)
    return {"mensaje": "Notificaciones marcadas como leídas", "cantidad": cantidad}
