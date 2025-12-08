# app/modules/esquelas/repositories/codigo_esquela_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.esquelas.models.esquela_models import CodigoEsquela


class CodigoEsquelaRepository:
    """Repositorio para operaciones CRUD de CodigoEsquela"""

    @staticmethod
    def get_all(db: Session) -> List[CodigoEsquela]:
        """Obtener todos los códigos de esquela"""
        return db.query(CodigoEsquela).all()

    @staticmethod
    def get_by_id(db: Session, id_codigo: int) -> Optional[CodigoEsquela]:
        """Obtener un código por ID"""
        return db.query(CodigoEsquela).filter(CodigoEsquela.id_codigo == id_codigo).first()

    @staticmethod
    def get_by_codigo(db: Session, codigo: str) -> Optional[CodigoEsquela]:
        """Obtener un código por su código único (ej: R01, O01)"""
        return db.query(CodigoEsquela).filter(CodigoEsquela.codigo == codigo).first()

    @staticmethod
    def get_by_tipo(db: Session, tipo: str) -> List[CodigoEsquela]:
        """Obtener códigos por tipo (reconocimiento u orientacion)"""
        return db.query(CodigoEsquela).filter(CodigoEsquela.tipo == tipo).all()

    @staticmethod
    def create(db: Session, codigo_esquela: CodigoEsquela) -> CodigoEsquela:
        """Crear un nuevo código de esquela"""
        db.add(codigo_esquela)
        db.commit()
        db.refresh(codigo_esquela)
        return codigo_esquela

    @staticmethod
    def update(db: Session, codigo_esquela: CodigoEsquela) -> CodigoEsquela:
        """Actualizar un código de esquela"""
        db.commit()
        db.refresh(codigo_esquela)
        return codigo_esquela

    @staticmethod
    def delete(db: Session, id_codigo: int) -> Optional[CodigoEsquela]:
        """Eliminar un código de esquela"""
        codigo = CodigoEsquelaRepository.get_by_id(db, id_codigo)
        if codigo:
            db.delete(codigo)
            db.commit()
        return codigo
