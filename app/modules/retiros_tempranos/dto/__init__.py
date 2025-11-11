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
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)

from .solicitud_retiro_dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO
)

from .solicitud_retiro_detalle_dto import (
    SolicitudRetiroDetalleCreateDTO,
    SolicitudRetiroDetalleUpdateDTO,
    SolicitudRetiroDetalleResponseDTO
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
    
    # Solicitud Retiro
    "SolicitudRetiroCreateDTO",
    "SolicitudRetiroUpdateDTO",
    "SolicitudRetiroResponseDTO",
    
    # Solicitud Retiro Detalle
    "SolicitudRetiroDetalleCreateDTO",
    "SolicitudRetiroDetalleUpdateDTO",
    "SolicitudRetiroDetalleResponseDTO",
]
