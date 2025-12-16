# app/modules/administracion/models/administrativo_models.py
##
"""Modelos para administrativos"""

from sqlalchemy import Column, Integer, String, ForeignKey, Time, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Administrativo(Base):
    """
    Modelo para la tabla administrativos
    Relaciona personas con cargos administrativos
    """
    __tablename__ = "administrativos"
    __table_args__ = {'extend_existing': True}

    id_administrativo = Column(Integer, primary_key=True, autoincrement=True)
    id_persona = Column(Integer, ForeignKey("personas.id_persona", ondelete="CASCADE"), nullable=False, unique=True)
    id_cargo = Column(Integer, ForeignKey("cargos.id_cargo"), nullable=False)
    horario_entrada = Column(Time, nullable=True, default="08:00:00")
    horario_salida = Column(Time, nullable=True, default="16:00:00")
    area_trabajo = Column(String(100), nullable=True)
    observaciones = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Administrativo(id_administrativo={self.id_administrativo}, id_persona={self.id_persona})>"

