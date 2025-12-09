from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Cargo(Base):
    """Modelo mínimo para la tabla cargos (compatibilidad con FK)."""
    __tablename__ = "cargos"
    __table_args__ = {"extend_existing": True}

    id_cargo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cargo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    nivel_jerarquico = Column(Integer, nullable=True, default=1)
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Cargo(id={self.id_cargo}, nombre={self.nombre_cargo})>"
