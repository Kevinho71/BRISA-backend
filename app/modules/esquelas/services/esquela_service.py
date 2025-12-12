# app/modules/esquelas/services/esquela_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.esquelas.models.esquela_models import Esquela
from app.modules.esquelas.repositories.esquela_repository import EsquelaRepository
from app.modules.esquelas.dto.esquela_dto import EsquelaBaseDTO
from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.permission_mapper import puede_ver_todas_esquelas
from app.modules.profesores.models.profesor_models import Profesor
from datetime import date
from typing import Optional


class EsquelaService:

    @staticmethod
    def _resolve_profesor_id(db: Session, id_persona_or_profesor: int) -> Optional[int]:
        """
        Resuelve el `id_profesor` (tabla `profesores`) a partir de:
        - `id_persona` (tabla `personas`) o
        - `id_profesor` (tabla `profesores`).

        Retorna None si no existe un profesor asociado.
        """
        profesor = db.query(Profesor).filter(Profesor.id_persona == id_persona_or_profesor).first()
        if profesor:
            return profesor.id_profesor

        profesor = db.query(Profesor).filter(Profesor.id_profesor == id_persona_or_profesor).first()
        if profesor:
            return profesor.id_profesor

        return None

    @staticmethod
    def listar_esquelas(db: Session, current_user: Usuario = None):
        """
        Lista esquelas según permisos del usuario.
        - Admin/Regente: Ve todas
        - Profesor: Ve solo las que él asignó
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
            )

        # Si puede ver todas, retornar todas
        if puede_ver_todas_esquelas(current_user):
            print(EsquelaRepository.get_all(db))
            return EsquelaRepository.get_all(db)

        # Si es profesor, filtrar por sus esquelas
        if current_user.id_persona:
            id_profesor = EsquelaService._resolve_profesor_id(db, current_user.id_persona)
            if not id_profesor:
                return []
            return EsquelaRepository.get_by_profesor(db, id_profesor)

        # Si no tiene permisos, retornar vacío
        return []

    @staticmethod
    def listar_esquelas_con_filtros(
        db: Session,
        name: Optional[str] = None,
        course_id: Optional[int] = None,
        tipo: Optional[str] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        page: int = 1,
        page_size: int = 10000,
        current_user: Usuario = None
    ):
        """
        Lista esquelas con filtros avanzados según permisos.
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
            )

        # Determinar si debe filtrar por profesor
        id_profesor_filtro = None
        if not puede_ver_todas_esquelas(current_user):
            id_profesor_filtro = EsquelaService._resolve_profesor_id(db, current_user.id_persona)
            if not id_profesor_filtro:
                return {
                    "total": 0,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": 0,
                    "data": []
                }

        return EsquelaRepository.get_with_filters(
            db=db,
            name=name,
            course_id=course_id,
            tipo=tipo,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            year=year,
            month=month,
            page=page,
            page_size=page_size,
            id_profesor=id_profesor_filtro
        )

    @ staticmethod
    def obtener_esquela(db: Session, id: int, current_user: Usuario = None):
        """Obtiene una esquela validando permisos"""
        esquela = EsquelaRepository.get_by_id(db, id)

        if not esquela:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Esquela no encontrada"
            )

        # Validar que el usuario pueda ver esta esquela
        if current_user and not puede_ver_todas_esquelas(current_user):
            id_profesor_usuario = EsquelaService._resolve_profesor_id(db, current_user.id_persona)
            if not id_profesor_usuario or id_profesor_usuario != esquela.id_profesor:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para ver esta esquela"
                )

        return esquela

    @ staticmethod
    def obtener_agregado_por_curso(db: Session, year: Optional[int] = None):
        """
        Obtiene cantidad de esquelas de reconocimiento y orientación por curso
        """
        return EsquelaRepository.get_aggregate_by_course(db, year)

    @ staticmethod
    def obtener_esquelas_estudiante(
        db: Session,
        student_id: int,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene todas las esquelas de un estudiante con conteo de códigos
        """
        return EsquelaRepository.get_by_student_with_date_range(
            db, student_id, fecha_desde, fecha_hasta
        )

    @ staticmethod
    def obtener_agregado_por_periodo(db: Session, group_by: str = "year"):
        """
        Obtiene agregación de esquelas por año o mes
        """
        return EsquelaRepository.get_aggregate_by_year_month(db, group_by)

    @ staticmethod
    def crear_esquela(db: Session, esquela_data, current_user: Usuario = None):
        """
        Crea una nueva esquela con validaciones de permisos y autogeneración de registrador.

        Reglas:
        - id_registrador siempre es current_user.id_persona
        - Si es profesor, id_profesor debe ser su id_persona
        - El profesor debe impartir clases en el curso del estudiante
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
            )

        # El registrador siempre es el usuario autenticado.
        # Si es profesor, se guarda su `id_profesor` (tabla profesores).
        id_registrador_prof = EsquelaService._resolve_profesor_id(db, current_user.id_persona)
        id_registrador = id_registrador_prof if id_registrador_prof else current_user.id_persona

        # Determinar id_profesor según rol
        if puede_ver_todas_esquelas(current_user):
            # Admin/Regente puede especificar cualquier profesor
            if not esquela_data.id_profesor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Debe especificar el profesor para esta esquela"
                )
            # El frontend puede enviar id_persona o id_profesor; resolvemos al id_profesor real
            id_profesor = EsquelaService._resolve_profesor_id(db, esquela_data.id_profesor)
            if not id_profesor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El profesor especificado no existe"
                )
        else:
            # Profesor solo puede crear esquelas en su nombre
            id_profesor_real = EsquelaService._resolve_profesor_id(db, current_user.id_persona)
            if not id_profesor_real:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los profesores pueden registrar esquelas"
                )
            
            # Si se envía un id_profesor, debe coincidir con el real
            if esquela_data.id_profesor and esquela_data.id_profesor != id_profesor_real:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo puede asignar esquelas en su propio nombre"
                )
            id_profesor = id_profesor_real

        # Obtener curso del estudiante
        from app.modules.administracion.repositories.curso_repository import CursoRepository
        curso = CursoRepository.get_curso_by_estudiante(
            db, esquela_data.id_estudiante)

        if not curso:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estudiante no está asignado a ningún curso"
            )

        # Validar que el profesor imparte clases en el curso del estudiante
        from app.modules.administracion.repositories.persona_repository import PersonaRepository
        if not PersonaRepository.es_profesor_del_curso(db, id_profesor, curso.id_curso):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El profesor no imparte clases en el curso {
                    curso.nombre_curso} del estudiante"
            )

        # Crear esquela
        nueva_esquela = Esquela(
            id_estudiante=esquela_data.id_estudiante,
            id_profesor=id_profesor,
            id_registrador=id_registrador,  # Autogenerado
            fecha=esquela_data.fecha,
            observaciones=esquela_data.observaciones
        )

        return EsquelaRepository.create(db, nueva_esquela, esquela_data.codigos)

    @ staticmethod
    def eliminar_esquela(db: Session, id: int):
        esquela = EsquelaRepository.delete(db, id)
        if not esquela:
            raise HTTPException(
                status_code=404, detail="Esquela no encontrada")
        return esquela
