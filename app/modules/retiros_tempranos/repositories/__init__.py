"""
Repositories para el módulo de Retiros Tempranos
"""

# Interfaces
from .estudiante_repository_interface import IEstudianteRepository
from .apoderado_repository_interface import IApoderadoRepository
from .estudiante_apoderado_repository_interface import IEstudianteApoderadoRepository
from .motivo_retiro_repository_interface import IMotivoRetiroRepository
from .autorizacion_retiro_repository_interface import IAutorizacionRetiroRepository
from .registro_salida_repository_interface import IRegistroSalidaRepository
from .solicitud_retiro_repository_interface import ISolicitudRetiroRepository
from .solicitud_retiro_masivo_repository_interface import SolicitudRetiroMasivoRepositoryInterface
from .detalle_solicitud_retiro_masivo_repository_interface import DetalleSolicitudRetiroMasivoRepositoryInterface

# Implementaciones
from .estudiante_repository import EstudianteRepository
from .apoderado_repository import ApoderadoRepository
from .estudiante_apoderado_repository import EstudianteApoderadoRepository
from .motivo_retiro_repository import MotivoRetiroRepository
from .autorizacion_retiro_repository import AutorizacionRetiroRepository
from .registro_salida_repository import RegistroSalidaRepository
from .solicitud_retiro_repository import SolicitudRetiroRepository
from .solicitud_retiro_masivo_repository import SolicitudRetiroMasivoRepository
from .detalle_solicitud_retiro_masivo_repository import DetalleSolicitudRetiroMasivoRepository

__all__ = [
    # Interfaces
    "IEstudianteRepository",
    "IApoderadoRepository",
    "IEstudianteApoderadoRepository",
    "IMotivoRetiroRepository",
    "IAutorizacionRetiroRepository",
    "IRegistroSalidaRepository",
    "ISolicitudRetiroRepository",
    "SolicitudRetiroMasivoRepositoryInterface",
    "DetalleSolicitudRetiroMasivoRepositoryInterface",
    
    # Implementaciones
    "EstudianteRepository",
    "ApoderadoRepository",
    "EstudianteApoderadoRepository",
    "MotivoRetiroRepository",
    "AutorizacionRetiroRepository",
    "RegistroSalidaRepository",
    "SolicitudRetiroRepository",
    "SolicitudRetiroMasivoRepository",
    "DetalleSolicitudRetiroMasivoRepository",
]
