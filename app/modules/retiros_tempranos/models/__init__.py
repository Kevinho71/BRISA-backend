"""
Modelos para el módulo de Retiros Tempranos
"""

# Importar Estudiante desde administracion (modelo compartido)
from app.modules.administracion.models.persona_models import Estudiante
from .Apoderado import Apoderado
from .EstudianteApoderado import EstudianteApoderado
from .MotivoRetiro import MotivoRetiro, SeveridadEnum
from .AutorizacionesRetiro import AutorizacionRetiro, DecisionEnum
from .SolicitudRetiro import SolicitudRetiro, EstadoSolicitudEnum, TipoSolicitudEnum
from .SolicitudRetiroMasivo import SolicitudRetiroMasivo, EstadoSolicitudMasivaEnum
from .DetalleSolicitudRetiroMasivo import DetalleSolicitudRetiroMasivo
from .RegistroSalida import RegistroSalida, TipoRegistroEnum

__all__ = [
    "Estudiante",
    "Apoderado",
    "EstudianteApoderado",
    "MotivoRetiro",
    "SeveridadEnum",
    "AutorizacionRetiro",
    "DecisionEnum",
    "SolicitudRetiro",
    "EstadoSolicitudEnum",
    "TipoSolicitudEnum",
    "SolicitudRetiroMasivo",
    "EstadoSolicitudMasivaEnum",
    "DetalleSolicitudRetiroMasivo",
    "RegistroSalida",
    "TipoRegistroEnum",
]

