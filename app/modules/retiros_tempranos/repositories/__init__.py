"""
Repositories para el módulo de Retiros Tempranos
"""

# Interfaces
from .estudiante_repository_interface import IEstudianteRepository
from .apoderado_repository_interface import IApoderadoRepository
from .motivo_retiro_repository_interface import IMotivoRetiroRepository
from .autorizacion_retiro_repository_interface import IAutorizacionRetiroRepository
from .registro_salida_repository_interface import IRegistroSalidaRepository
from .solicitud_retiro_repository_interface import ISolicitudRetiroRepository
from .solicitud_retiro_detalle_repository_interface import ISolicitudRetiroDetalleRepository

# Implementaciones
from .estudiante_repository import EstudianteRepository
from .apoderado_repository import ApoderadoRepository
from .motivo_retiro_repository import MotivoRetiroRepository
from .autorizacion_retiro_repository import AutorizacionRetiroRepository
from .registro_salida_repository import RegistroSalidaRepository
from .solicitud_retiro_repository import SolicitudRetiroRepository
from .solicitud_retiro_detalle_repository import SolicitudRetiroDetalleRepository

__all__ = [
    # Interfaces
    "IEstudianteRepository",
    "IApoderadoRepository",
    "IMotivoRetiroRepository",
    "IAutorizacionRetiroRepository",
    "IRegistroSalidaRepository",
    "ISolicitudRetiroRepository",
    "ISolicitudRetiroDetalleRepository",
    
    # Implementaciones
    "EstudianteRepository",
    "ApoderadoRepository",
    "MotivoRetiroRepository",
    "AutorizacionRetiroRepository",
    "RegistroSalidaRepository",
    "SolicitudRetiroRepository",
    "SolicitudRetiroDetalleRepository",
]
