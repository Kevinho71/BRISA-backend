# BRISA Backend API

Backend API REST desarrollado en FastAPI para el sistema de gestión institucional BRISA de la Universidad Católica Boliviana. 
Arquitectura modular diseñada para desarrollo colaborativo entre múltiples equipos.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.13+
- MySQL 8.0+ 
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Kevinho71/BRISA-backend.git
cd BRISA-backend
```

2. **Crear y activar entorno virtual**
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Windows - PowerShell)
.\.venv\Scripts\Activate

# Activar entorno virtual (Linux/Mac)
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Copiar `.env.example` a `.env` y configurar según necesites.

5. **Ejecutar el servidor**
```bash
python run.py
```

El servidor estará disponible en:
- http://localhost:8000
- Documentación: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
BRISA-backend/
├── app/
│   ├── modules/
│   │   ├── retiros_tempranos/  # ✅ IMPLEMENTADO
│   │   ├── usuarios/          
│   │   ├── estudiantes/        
│   │   └── ... otros módulos
│   ├── core/              # Configuración y utilidades
│   └── shared/            # Recursos compartidos
├── docs/                  # Documentación
└── tests/                 # Tests unitarios
```

## 🔧 Módulos

### ✅ Retiros Tempranos (IMPLEMENTADO)
- 35 endpoints REST activos
- Gestión completa de solicitudes de retiro
- Workflow: recibida → derivada → aprobada/rechazada

### 🏗️ Otros Módulos (En desarrollo)
Ver estructura completa en la documentación.

## 🛠️ Tecnologías

- FastAPI, SQLAlchemy, Pydantic
- MySQL, Alembic, PyMySQL
- JWT para autenticación

## 👥 Equipo

- **Kevinho71** - kevin.guzman@ucb.edu.bo

## 📝 Commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección
- `docs:` Documentación
