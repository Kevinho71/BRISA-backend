from pydantic import BaseModel

class EstudianteSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class ProfesorSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class SituacionSimple(BaseModel):
    id: int
    nombre: str
    nivel: str

    class Config:
        from_attributes = True
