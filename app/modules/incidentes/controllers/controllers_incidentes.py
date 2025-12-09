# app/modules/incidentes/controllers/controllers_incidentes.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os, shutil
from typing import Optional, List
import traceback
from app.core.extensions import get_db

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
    NotificacionCreateDTO,
    NotificacionOutDTO
)

router = APIRouter(prefix="/Incidentes", tags=["Incidentes"])

MEDIA_DIR = os.getenv("MEDIA_DIR", "uploads")
os.makedirs(MEDIA_DIR, exist_ok=True)

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
def crear_area(dto: AreaCreateDTO, db: Session = Depends(get_db)):
    svc = AreaService()
    return svc.crear_area(db, dto)


@router.put("/areas/{id_area}")
def actualizar_area(id_area: int, dto: AreaUpdateDTO, db: Session = Depends(get_db)):
    svc = AreaService()
    return svc.actualizar_area(db, id_area, dto)


@router.delete("/areas/{id_area}")
def eliminar_area(id_area: int, db: Session = Depends(get_db)):
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

# PATCH — actualizar una situación
@router.patch("/situaciones/{id_situacion}")
def actualizar_situacion(id_situacion: int, dto: SituacionUpdateDTO, db: Session = Depends(get_db)):
    svc = SituacionService(db)
    return svc.actualizar(id_situacion, dto)

# DELETE — eliminar una situación
@router.delete("/situaciones/{id_situacion}")
def eliminar_situacion(id_situacion: int, db: Session = Depends(get_db)):
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
    return nuevo
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
#----NOTIFICACIONES----