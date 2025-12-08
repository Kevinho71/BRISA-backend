# Guía de Desarrollo por Equipos

## Estructura de Módulos

Cada equipo tiene su propio módulo dentro de `app/modules/equipoX/` con la siguiente estructura:

```
equipoX/
├── __init__.py          # Exporta el blueprint del módulo
├── routes.py           # Define las rutas/endpoints del equipo
├── models.py           # Modelos de base de datos específicos
└── services.py         # Lógica de negocio del equipo
```

## Convenciones de URLs

Cada equipo tiene un prefijo de URL asignado:

- **Equipo 1**: `/api/equipo1/`
- **Equipo 2**: `/api/equipo2/`  
- **Equipo 3**: `/api/equipo3/`

## Ejemplo de Implementación

### 1. Definir Rutas (`routes.py`)

```python
from flask import Blueprint, request
from app.core.utils import success_response, error_response
from .services import MiServicio

equipo1_bp = Blueprint('equipo1', __name__)

@equipo1_bp.route('/mi-endpoint', methods=['GET'])
def mi_endpoint():
    data = MiServicio.obtener_datos()
    return success_response(data, "Datos obtenidos exitosamente")
```

### 2. Definir Modelos (`models.py`)

```python
from app.core.database import get_db


class MiModelo(db.Model):
    __tablename__ = 'mi_tabla'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    # ... otros campos
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            # ... otros campos
        }
```

### 3. Lógica de Negocio (`services.py`)

```python
from .models import MiModelo
from app.core.extensions import db

class MiServicio:
    
    @staticmethod
    def obtener_datos():
        items = MiModelo.query.all()
        return [item.to_dict() for item in items]
    
    @staticmethod
    def crear_item(data):
        item = MiModelo(**data)
        db.session.add(item)
        db.session.commit()
        return item
```

## Utilidades Disponibles

### Respuestas Estándar

```python
from app.core.utils import success_response, error_response

# Respuesta exitosa
return success_response(data, "Mensaje de éxito")

# Respuesta de error
return error_response("Mensaje de error", 400)
```

### Validación de JSON

```python
from app.core.utils import validate_json

@equipo1_bp.route('/endpoint', methods=['POST'])
@validate_json(['campo_requerido', 'otro_campo'])
def mi_endpoint():
    # El decorador valida que los campos estén presentes
    data = request.get_json()
    # ... procesar datos
```

## Mejores Prácticas

1. **Separación de Responsabilidades**:
   - `routes.py`: Solo manejo de HTTP (request/response)
   - `services.py`: Lógica de negocio
   - `models.py`: Definición de datos

2. **Nomenclatura**:
   - Usar nombres descriptivos
   - Seguir convenciones de Python (snake_case)
   - Prefijos claros para evitar conflictos

3. **Documentación**:
   - Docstrings en todas las funciones
   - Comentarios para lógica compleja
   - Ejemplos de uso en endpoints

4. **Testing**:
   - Test para cada endpoint
   - Test para servicios críticos
   - Mocks para dependencias externas

## Comandos Útiles

### Activar entorno virtual
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac  
source venv/bin/activate
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar aplicación
```bash
python run.py
```

### Ejecutar tests
```bash
pytest
pytest tests/test_equipo1.py  # Tests específicos
```

### Migraciones de BD
```bash
flask db init      # Primera vez
flask db migrate   # Generar migración
flask db upgrade   # Aplicar migración
```