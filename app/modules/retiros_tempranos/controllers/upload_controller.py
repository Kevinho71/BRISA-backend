"""
app/modules/retiros_tempranos/controllers/upload_controller.py
Endpoint para subir fotos de evidencia de retiros tempranos
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from pathlib import Path
import uuid
import os
from datetime import datetime
from app.shared.decorators.auth_decorators import get_current_user, require_permissions
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/retiros-tempranos/upload", tags=["Upload de Evidencias"])

# Configuración de almacenamiento
UPLOAD_DIR = Path("uploads/retiros_tempranos/evidencias")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Crear directorio si no existe
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/evidencia", status_code=status.HTTP_201_CREATED)
@require_permissions("apoderado", "profesor", "recepcion", "regente")
async def subir_foto_evidencia(
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, GIF, WEBP)"),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **[APODERADO/PROFESOR/RECEPCIÓN/REGENTE]** Subir foto de evidencia para solicitud de retiro
    
    **Características:**
    - Formatos permitidos: JPG, JPEG, PNG, GIF, WEBP
    - Tamaño máximo: 5MB
    - Nombre único con UUID para evitar colisiones
    - Retorna URL/path para usar en la solicitud
    
    **Flujo:**
    1. El usuario sube la foto ANTES de crear la solicitud
    2. Obtiene la URL de la respuesta
    3. Usa esa URL en el campo `foto_evidencia` al crear la solicitud
    
    **Ejemplo de uso:**
    ```
    POST /api/retiros-tempranos/upload/evidencia
    Content-Type: multipart/form-data
    
    file: [archivo binario]
    ```
    
    **Respuesta:**
    ```json
    {
        "success": true,
        "message": "Foto subida exitosamente",
        "data": {
            "url": "/uploads/retiros_tempranos/evidencias/2025-12-15_abc123.jpg",
            "filename": "2025-12-15_abc123.jpg",
            "original_filename": "foto.jpg",
            "size_bytes": 245678,
            "uploaded_by": 41,
            "uploaded_at": "2025-12-15T15:30:00"
        }
    }
    ```
    """
    
    # 1. Validar extensión
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato no permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 2. Validar tamaño
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Archivo muy grande. Tamaño máximo: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # 3. Generar nombre único
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    unique_id = str(uuid.uuid4())[:8]
    new_filename = f"{timestamp}_{unique_id}{file_ext}"
    file_path = UPLOAD_DIR / new_filename
    
    # 4. Guardar archivo
    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar archivo: {str(e)}"
        )
    
    # 5. Construir URL pública
    # En producción, esto podría ser una URL completa: https://api.ejemplo.com/uploads/...
    relative_path = f"/uploads/retiros_tempranos/evidencias/{new_filename}"
    
    return {
        "success": True,
        "message": "Foto de evidencia subida exitosamente",
        "data": {
            "url": relative_path,  # Este es el valor para foto_evidencia
            "filename": new_filename,
            "original_filename": file.filename,
            "size_bytes": file_size,
            "uploaded_by": current_user.id_usuario,
            "uploaded_at": datetime.now().isoformat()
        }
    }


@router.delete("/evidencia/{filename}")
@require_permissions("apoderado","admin", "regente", "recepcion")
async def eliminar_foto_evidencia(
    filename: str,
    current_user: Usuario = Depends(get_current_user)
):
    """
    **[ADMIN/REGENTE/RECEPCIÓN]** Eliminar una foto de evidencia
    
    Usado cuando se cancela una solicitud o se sube una foto incorrecta.
    """
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado"
        )
    
    # Validar que el archivo está en el directorio correcto (seguridad)
    if not str(file_path.resolve()).startswith(str(UPLOAD_DIR.resolve())):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado"
        )
    
    try:
        os.remove(file_path)
        return {
            "success": True,
            "message": f"Archivo {filename} eliminado exitosamente"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar archivo: {str(e)}"
        )
