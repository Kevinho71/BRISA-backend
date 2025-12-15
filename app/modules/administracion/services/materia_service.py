from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.administracion.repositories.materia_repository import MateriaRepository
from app.modules.administracion.dto.materia_dto import MateriaCreateDTO, MateriaUpdateDTO

class MateriaService:
    @staticmethod
    def listar_materias(db: Session):
        return MateriaRepository.get_all(db)

    @staticmethod
    def obtener_materia(db: Session, materia_id: int):
        materia = MateriaRepository.get_by_id(db, materia_id)
        if not materia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Materia no encontrada"
            )
        return materia

    @staticmethod
    def crear_materia(db: Session, materia_dto: MateriaCreateDTO):
        return MateriaRepository.create(db, materia_dto)

    @staticmethod
    def actualizar_materia(db: Session, materia_id: int, materia_dto: MateriaUpdateDTO):
        materia = MateriaRepository.get_by_id(db, materia_id)
        if not materia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Materia no encontrada"
            )
        return MateriaRepository.update(db, materia_id, materia_dto)

    @staticmethod
    def eliminar_materia(db: Session, materia_id: int):
        materia = MateriaRepository.get_by_id(db, materia_id)
        if not materia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Materia no encontrada"
            )
        # La eliminación en cascada de asignaciones se maneja en la base de datos
        return MateriaRepository.delete(db, materia_id)
