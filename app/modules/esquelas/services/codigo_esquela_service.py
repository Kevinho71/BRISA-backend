# app/modules/esquelas/services/codigo_esquela_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.modules.esquelas.models.esquela_models import CodigoEsquela
from app.modules.esquelas.repositories.codigo_esquela_repository import CodigoEsquelaRepository
from app.modules.esquelas.dto.codigo_esquela_dto import (
    CodigoEsquelaCreateDTO,
    CodigoEsquelaUpdateDTO
)


class CodigoEsquelaService:
    """Servicio para lógica de negocio de códigos de esquela"""

    @staticmethod
    def listar_codigos(db: Session) -> List[CodigoEsquela]:
        """Listar todos los códigos de esquela"""
        return CodigoEsquelaRepository.get_all(db)

    @staticmethod
    def listar_por_tipo(db: Session, tipo: str) -> List[CodigoEsquela]:
        """Listar códigos por tipo (reconocimiento u orientacion)"""
        if tipo not in ['reconocimiento', 'orientacion']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo debe ser 'reconocimiento' u 'orientacion'"
            )
        return CodigoEsquelaRepository.get_by_tipo(db, tipo)

    @staticmethod
    def obtener_codigo(db: Session, id_codigo: int) -> CodigoEsquela:
        """Obtener un código por ID"""
        codigo = CodigoEsquelaRepository.get_by_id(db, id_codigo)
        if not codigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código de esquela no encontrado"
            )
        return codigo

    @staticmethod
    def crear_codigo(db: Session, codigo_data: CodigoEsquelaCreateDTO) -> CodigoEsquela:
        """Crear un nuevo código de esquela"""
        # Validar tipo
        if codigo_data.tipo not in ['reconocimiento', 'orientacion']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo debe ser 'reconocimiento' u 'orientacion'"
            )

        # Verificar que el código no exista
        codigo_existente = CodigoEsquelaRepository.get_by_codigo(db, codigo_data.codigo)
        if codigo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El código '{codigo_data.codigo}' ya existe"
            )

        nuevo_codigo = CodigoEsquela(
            tipo=codigo_data.tipo,
            codigo=codigo_data.codigo,
            descripcion=codigo_data.descripcion
        )
        return CodigoEsquelaRepository.create(db, nuevo_codigo)

    @staticmethod
    def actualizar_codigo(
        db: Session,
        id_codigo: int,
        codigo_data: CodigoEsquelaUpdateDTO
    ) -> CodigoEsquela:
        """Actualizar un código de esquela"""
        codigo = CodigoEsquelaRepository.get_by_id(db, id_codigo)
        if not codigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código de esquela no encontrado"
            )

        # Actualizar campos si se proporcionan
        if codigo_data.tipo is not None:
            if codigo_data.tipo not in ['reconocimiento', 'orientacion']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tipo debe ser 'reconocimiento' u 'orientacion'"
                )
            codigo.tipo = codigo_data.tipo

        if codigo_data.codigo is not None:
            # Verificar que el nuevo código no exista
            codigo_existente = CodigoEsquelaRepository.get_by_codigo(db, codigo_data.codigo)
            if codigo_existente and codigo_existente.id_codigo != id_codigo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El código '{codigo_data.codigo}' ya existe"
                )
            codigo.codigo = codigo_data.codigo

        if codigo_data.descripcion is not None:
            codigo.descripcion = codigo_data.descripcion

        return CodigoEsquelaRepository.update(db, codigo)

    @staticmethod
    def eliminar_codigo(db: Session, id_codigo: int) -> CodigoEsquela:
        """Eliminar un código de esquela"""
        codigo = CodigoEsquelaRepository.delete(db, id_codigo)
        if not codigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código de esquela no encontrado"
            )
        return codigo
