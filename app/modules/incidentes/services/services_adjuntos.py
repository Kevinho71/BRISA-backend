# app\modules\incidentes\services\services_adjuntos.py
import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.modules.incidentes.repositories.repositories_adjuntos import AdjuntoRepository

UPLOAD_DIR = "uploads/incidentes"

TIPOS_PERMITIDOS = [
    "image/jpeg", "image/jpg", "image/png",
    "audio/mpeg", "audio/mp3",
    "video/mp4",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain"
]

class AdjuntoService:

    def __init__(self, db: Session):
        self.repo = AdjuntoRepository(db)

    def subir(self, id_incidente: int, archivo: UploadFile, subido_por: int):
        if archivo.content_type not in TIPOS_PERMITIDOS:
            raise Exception(f"Tipo no permitido: {archivo.content_type}")

        carpeta = f"{UPLOAD_DIR}/{id_incidente}"
        os.makedirs(carpeta, exist_ok=True)

        ruta_archivo = f"{carpeta}/{archivo.filename}"

        with open(ruta_archivo, "wb") as f:
            shutil.copyfileobj(archivo.file, f)

        data = {
            "id_incidente": id_incidente,
            "nombre_archivo": archivo.filename,
            "ruta": ruta_archivo,
            "tipo_mime": archivo.content_type,
            "id_subido_por": subido_por,
        }

        return self.repo.crear(data)

    def listar_por_incidente(self, id_incidente: int):
        return self.repo.obtener_por_incidente(id_incidente)

    def descargar(self, id_adjunto: int):
        return self.repo.obtener_por_id(id_adjunto)
    

    def borrar_por_id(self, id_adjunto: int):
        adj = self.repo.obtener_por_id(id_adjunto)
        if not adj:
            return False

        # borrar físico
        if adj.ruta and os.path.exists(adj.ruta):
            os.remove(adj.ruta)

        # si carpeta queda vacía eliminarla
        carpeta = os.path.dirname(adj.ruta)
        if os.path.isdir(carpeta) and len(os.listdir(carpeta)) == 0:
            os.rmdir(carpeta)

        self.repo.borrar_por_id(id_adjunto)
        return True
