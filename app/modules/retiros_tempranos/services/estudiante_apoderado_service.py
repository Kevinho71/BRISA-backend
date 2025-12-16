from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.EstudianteApoderado import EstudianteApoderado
from app.modules.retiros_tempranos.models.Apoderado import Apoderado
from app.modules.usuarios.models.usuario_models import Usuario
from app.modules.retiros_tempranos.repositories import IEstudianteApoderadoRepository
from app.modules.retiros_tempranos.dto import (
    EstudianteApoderadoCreateDTO,
    EstudianteApoderadoUpdateDTO,
    EstudianteApoderadoResponseDTO,
)
from app.shared.services.base_services import BaseService


class EstudianteApoderadoService(BaseService):
    def __init__(self, repository: IEstudianteApoderadoRepository, db: Session = None):
        self.repository = repository
        self.db = db

    def create_relacion(self, relacion_dto: EstudianteApoderadoCreateDTO) -> EstudianteApoderadoResponseDTO:
        """Crear una nueva relación estudiante-apoderado"""
        # Verificar si la relación ya existe
        existing = self.repository.get_by_ids(relacion_dto.id_estudiante, relacion_dto.id_apoderado)
        if existing:
            raise HTTPException(status_code=400, detail="La relación ya existe")
        
        relacion = EstudianteApoderado(
            id_estudiante=relacion_dto.id_estudiante,
            id_apoderado=relacion_dto.id_apoderado,
            parentesco=relacion_dto.parentesco,
            es_contacto_principal=relacion_dto.es_contacto_principal,
        )
        creada = self.repository.create(relacion)
        return EstudianteApoderadoResponseDTO.model_validate(creada)

    def get_relacion(self, id_estudiante: int, id_apoderado: int) -> EstudianteApoderadoResponseDTO:
        """Obtener una relación específica estudiante-apoderado"""
        relacion = self.repository.get_by_ids(id_estudiante, id_apoderado)
        if not relacion:
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return EstudianteApoderadoResponseDTO.model_validate(relacion)

    def get_apoderados_by_estudiante(self, id_estudiante: int) -> List[EstudianteApoderadoResponseDTO]:
        """Obtener todos los apoderados de un estudiante"""
        relaciones = self.repository.get_by_estudiante(id_estudiante)
        return [EstudianteApoderadoResponseDTO.model_validate(r) for r in relaciones]

    def get_estudiantes_by_apoderado(self, id_apoderado: int) -> List[EstudianteApoderadoResponseDTO]:
        """Obtener todos los estudiantes de un apoderado"""
        relaciones = self.repository.get_by_apoderado(id_apoderado)
        return [EstudianteApoderadoResponseDTO.model_validate(r) for r in relaciones]

    def get_estudiantes_by_usuario(self, id_usuario: int) -> List[EstudianteApoderadoResponseDTO]:
        """Obtener todos los estudiantes de un apoderado usando id_usuario"""
        if not self.db:
            raise HTTPException(status_code=500, detail="Sesión de base de datos no disponible")
        
        # Paso 1: Buscar el usuario por id_usuario para obtener id_persona
        usuario = self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        
        if not usuario:
            # Usuario no encontrado, retornar lista vacía
            return []
        
        # Paso 2: Buscar el apoderado por id_persona
        apoderado = self.db.query(Apoderado).filter(Apoderado.id_persona == usuario.id_persona).first()
        
        if not apoderado:
            # Apoderado no encontrado, retornar lista vacía
            return []
        
        # Paso 3: Obtener los estudiantes usando el id_apoderado real
        relaciones = self.repository.get_by_apoderado(apoderado.id_apoderado)
        return [EstudianteApoderadoResponseDTO.model_validate(r) for r in relaciones]

    def get_contacto_principal(self, id_estudiante: int) -> EstudianteApoderadoResponseDTO:
        """Obtener el apoderado de contacto principal de un estudiante"""
        relacion = self.repository.get_contacto_principal(id_estudiante)
        if not relacion:
            raise HTTPException(status_code=404, detail="No se encontró contacto principal")
        return EstudianteApoderadoResponseDTO.model_validate(relacion)

    def set_contacto_principal(self, id_estudiante: int, id_apoderado: int) -> EstudianteApoderadoResponseDTO:
        """Establecer un apoderado como contacto principal"""
        # Verificar que la relación existe
        relacion = self.repository.get_by_ids(id_estudiante, id_apoderado)
        if not relacion:
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        
        updated = self.repository.set_contacto_principal(id_estudiante, id_apoderado)
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo establecer como contacto principal")
        return EstudianteApoderadoResponseDTO.model_validate(updated)

    def update_relacion(
        self, id_estudiante: int, id_apoderado: int, relacion_dto: EstudianteApoderadoUpdateDTO
    ) -> EstudianteApoderadoResponseDTO:
        """Actualizar una relación estudiante-apoderado"""
        existing = self.repository.get_by_ids(id_estudiante, id_apoderado)
        if not existing:
            raise HTTPException(status_code=404, detail="Relación no encontrada")

        updated = self.repository.update(
            id_estudiante, id_apoderado, relacion_dto.model_dump(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la relación")
        return EstudianteApoderadoResponseDTO.model_validate(updated)

    def delete_relacion(self, id_estudiante: int, id_apoderado: int) -> bool:
        """Eliminar una relación estudiante-apoderado"""
        existing = self.repository.get_by_ids(id_estudiante, id_apoderado)
        if not existing:
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return self.repository.delete(id_estudiante, id_apoderado)
