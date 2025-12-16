"""
DTOs para el módulo de Retiros Tempranos
"""

from .estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO
)

from .apoderado_dto import (
    ApoderadoCreateDTO,
    ApoderadoUpdateDTO,
    ApoderadoResponseDTO
)

from .estudiante_apoderado_dto import (
    EstudianteApoderadoCreateDTO,
    EstudianteApoderadoUpdateDTO,
    EstudianteApoderadoResponseDTO
)

from .motivo_retiro_dto import (
    MotivoRetiroCreateDTO,
    MotivoRetiroUpdateDTO,
    MotivoRetiroResponseDTO,
    SeveridadEnum
)

from .autorizacion_retiro_dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO,
    DecisionEnum
)

from .registro_salida_dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaMasivoCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)

from .solicitud_retiro_dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO,
    EstadoSolicitudEnum,
    RecibirSolicitudDTO,
    DerivarSolicitudDTO,
    AprobarRechazarSolicitudDTO,
    CancelarSolicitudDTO
)

from .solicitud_retiro_masivo_dto import (
    SolicitudRetiroMasivoCreateDTO,
    SolicitudRetiroMasivoUpdateDTO,
    SolicitudRetiroMasivoResponseDTO,
    SolicitudRetiroMasivoDetalladaResponseDTO,
    DetalleSolicitudMasivoCreateDTO,
    DetalleSolicitudMasivoResponseDTO,
    EstadoSolicitudMasivaEnum,
    RecibirSolicitudMasivaDTO,
    DerivarSolicitudMasivaDTO,
    AprobarRechazarSolicitudMasivaDTO,
    CancelarSolicitudMasivaDTO
)

__all__ = [
    # Estudiante
    "EstudianteCreateDTO",
    "EstudianteUpdateDTO",
    "EstudianteResponseDTO",
    
    # Apoderado
    "ApoderadoCreateDTO",
    "ApoderadoUpdateDTO",
    "ApoderadoResponseDTO",
    
    # Estudiante-Apoderado
    "EstudianteApoderadoCreateDTO",
    "EstudianteApoderadoUpdateDTO",
    "EstudianteApoderadoResponseDTO",
    
    # Motivo Retiro
    "MotivoRetiroCreateDTO",
    "MotivoRetiroUpdateDTO",
    "MotivoRetiroResponseDTO",
    "SeveridadEnum",
    
    # Autorización Retiro
    "AutorizacionRetiroCreateDTO",
    "AutorizacionRetiroUpdateDTO",
    "AutorizacionRetiroResponseDTO",
    "DecisionEnum",
    
    # Registro Salida
    "RegistroSalidaCreateDTO",
    "RegistroSalidaUpdateDTO",
    "RegistroSalidaResponseDTO",
    "RegistroSalidaMasivoCreateDTO",
    
    # Solicitud Retiro
    "SolicitudRetiroCreateDTO",
    "SolicitudRetiroUpdateDTO",
    "SolicitudRetiroResponseDTO",
    "EstadoSolicitudEnum",
    "RecibirSolicitudDTO",
    "DerivarSolicitudDTO",
    "AprobarRechazarSolicitudDTO",
    "CancelarSolicitudDTO",
    
    # Solicitud Retiro Masivo
    "SolicitudRetiroMasivoCreateDTO",
    "SolicitudRetiroMasivoUpdateDTO",
    "SolicitudRetiroMasivoResponseDTO",
    "SolicitudRetiroMasivoDetalladaResponseDTO",
    "DetalleSolicitudMasivoCreateDTO",
    "DetalleSolicitudMasivoResponseDTO",
    "EstadoSolicitudMasivaEnum",
    "RecibirSolicitudMasivaDTO",
    "DerivarSolicitudMasivaDTO",
    "AprobarRechazarSolicitudMasivaDTO",
    "CancelarSolicitudMasivaDTO",
]
