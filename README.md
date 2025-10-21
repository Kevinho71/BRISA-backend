# BRISA Backend API

Backend API REST desarrollado en FastAPI para el sistema de gestión institucional BRISA de la Universidad Católica Boliviana. 
Arquitectura modular diseñada para desarrollo colaborativo entre múltiples equipos.

## 🏗️ Estructura del Proyecto

```
BRISA-backend/
├── app/
│   ├── __init__.py              # Inicialización del paquete y registro de routers
│   ├── config/
│   │   ├── config.py           # Configuraciones por ambiente
│   │   └── database.py         # Configuración de base de datos (SQLAlchemy)
│   ├── core/
│   │   ├── dependencies.py     # Dependencias, seguridad (JWT), CORS
│   │   └── utils.py            # Utilidades generales
│   ├── shared/                 # Elementos compartidos entre módulos
│   │   ├── models/             # Modelos base (BaseModel, PersonaBase)
│   │   ├── dto/                # Esquemas base Pydantic compartidos
│   │   ├── services/           # Servicios base y de auditoría
│   │   ├── validators/         # Validadores personalizados
│   │   ├── exceptions/         # Excepciones personalizadas
│   │   └── auth/               # Dependencias/middlewares de autenticación
│   └── modules/                # Módulos funcionales del sistema
│       ├── health/             # Health checks y monitoreo
│       ├── usuarios/           # Usuarios, Roles y Permisos
│       │   ├── controllers/    # Controladores HTTP (routers FastAPI)
│       │   ├── services/       # Lógica de negocio
│       │   ├── repositories/   # Acceso a datos
│       │   ├── dto/            # Esquemas de validación (Pydantic)
│       │   └── models/         # Modelos de base de datos (SQLAlchemy)
│       ├── estudiantes/        # Estudiantes y Cursos
│       ├── profesores/         # Profesores y Materias  
│       ├── retiros_tempranos/  # Gestión de retiros tempranos
│       ├── incidentes/         # Incidentes y Bienestar Estudiantil
│       ├── esquelas/           # Reconocimientos y Orientación
│       ├── administracion/     # Administración general
│       └── reportes/           # Reportes e integración
├── tests/                      # Tests unitarios e integración
├── docs/                       # Documentación del proyecto
├── venv/                       # Entorno virtual (no en git)
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno (local)
├── .env.example                # Plantilla de variables
├── .gitignore
├── README.md
└── run.py                      # Punto de entrada (Uvicorn)
```

## 📋 Módulos del Sistema

Todos los módulos están listos para implementación con su estructura MVC completa:

### MÓDULO 1: Usuarios, Roles y Permisos 🏗️
- Responsable: Sistema base de autenticación
- Carpeta: `app/modules/usuarios/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 2: Estudiantes y Cursos 🏗️
- Responsable: Gestión académica de estudiantes  
- Carpeta: `app/modules/estudiantes/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 3: Profesores y Materias 🏗️
- Responsable: Gestión docente
- Carpeta: `app/modules/profesores/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 4: Retiros Tempranos 🏗️
- Responsable: Proceso de retiros
- Carpeta: `app/modules/retiros_tempranos/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 5: Incidentes / Bienestar Estudiantil 🏗️
- Responsable: Bienestar estudiantil
- Carpeta: `app/modules/incidentes/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 6: Esquelas (Reconocimiento y Orientación) 🏗️
- Responsable: Comunicaciones institucionales
- Carpeta: `app/modules/esquelas/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 7: Administración 🏗️
- Responsable: Gestión administrativa
- Carpeta: `app/modules/administracion/`
- Estado: Estructura creada - Pendiente implementación

### MÓDULO 8: Integración y Reportes 🏗️
- Responsable: Reportería y dashboards
- Carpeta: `app/modules/reportes/`
- Estado: Estructura creada - Pendiente implementación

## 🚀 Configuración del Entorno

### 1. Clonar el repositorio

```bash
# Clonar el repositorio
git clone https://github.com/Kevinho71/BRISA-backend.git

# Ingresar al directorio del proyecto
cd BRISA-backend
```

### 2. Prerrequisitos
- Python 3.13+
- MySQL 8.0+ 
- Git

### 3. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Windows - PowerShell)
.\.venv\Scripts\Activate

# Activar entorno virtual (Linux/Mac)
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos MySQL

```sql
-- Crear base de datos y usuario
CREATE DATABASE brisa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'brisa_user'@'localhost' IDENTIFIED BY 'brisa_password';
GRANT ALL PRIVILEGES ON brisa_db.* TO 'brisa_user'@'localhost';
FLUSH PRIVILEGES;
```

### 6. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones de MySQL
```

Ejemplo de variables:
```
APP_ENV=development
SECRET_KEY=tu_clave_secreta
DATABASE_URL=mysql+pymysql://brisa_user:brisa_password@localhost:3306/brisa_db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 7. Inicializar base de datos

Con Alembic (recomendado para FastAPI/SQLAlchemy):

```bash
# Aplicar migraciones
alembic upgrade head

# (Opcional) Generar nueva migración tras cambios en modelos
alembic revision --autogenerate -m "tu mensaje de migración"

# (Opcional) Poblar con datos iniciales
python scripts/seed_db.py
```

### 8. Ejecutar la aplicación

```bash
# Modo desarrollo con autoreload
uvicorn run:app --host 127.0.0.1 --port 8000 --reload
```

La aplicación estará disponible en:
- http://localhost:8000
- Documentación interactiva OpenAPI: http://localhost:8000/docs
- Documentación alternativa ReDoc: http://localhost:8000/redoc

## 🔗 Endpoints Disponibles

### Sistema ✅
- GET `/api/health` - Estado de la API
- GET `/api/status` - Estado detallado del sistema

### Módulos 🏗️
Cada equipo implementará sus endpoints siguiendo la estructura:
- `/api/usuarios/*` - Módulo 1: Usuarios, Roles y Permisos
- `/api/estudiantes/*` - Módulo 2: Estudiantes y Cursos  
- `/api/profesores/*` - Módulo 3: Profesores y Materias
- `/api/retiros/*` - Módulo 4: Retiros Tempranos
- `/api/incidentes/*` - Módulo 5: Incidentes / Bienestar  
- `/api/esquelas/*` - Módulo 6: Esquelas y Orientación
- `/api/admin/*` - Módulo 7: Administración
- `/api/reportes/*` - Módulo 8: Reportes e Integración

## 👥 Guía para Equipos de Desarrollo

### 📁 Estructura de Cada Módulo

Cada módulo tiene la siguiente estructura MVC profesional:

```
app/modules/[nombre_modulo]/
├── __init__.py             # Identificación del módulo
├── controllers/            # Controladores HTTP (routers FastAPI)
│   ├── __init__.py
│   └── [modulo]_controller.py
├── services/               # Lógica de negocio  
│   ├── __init__.py
│   └── [modulo]_service.py
├── repositories/           # Acceso a datos
│   ├── __init__.py
│   └── [modulo]_repository.py
├── dto/                    # Esquemas de validación (Pydantic)
│   ├── __init__.py
│   └── [modulo]_dto.py
└── models/                 # Modelos de base de datos (SQLAlchemy)
    ├── __init__.py
    └── [modulo]_models.py
```

### 🔧 Pasos para Implementar un Módulo

1. Definir modelos en `models/[modulo]_models.py` (SQLAlchemy)
2. Crear DTOs (Pydantic) en `dto/[modulo]_dto.py`
3. Implementar repository para acceso a datos (sesión/queries)
4. Desarrollar services con lógica de negocio
5. Crear controllers con routers FastAPI (endpoints HTTP)
6. Incluir el router en la aplicación (p. ej. en `run.py` o `app/__init__.py`)

### 📚 Recursos Compartidos Disponibles

- Modelos base: `app/shared/models/base_models.py`
- DTOs base (Pydantic): `app/shared/dto/base_dto.py`
- Validadores: `app/shared/validators/custom_validators.py`
- Excepciones: `app/shared/exceptions/custom_exceptions.py`
- Autenticación: `app/shared/auth/dependencies.py` (dependencias/guards para JWT)

### ⚡ Comandos CLI Disponibles

```bash
# Migraciones de base de datos con Alembic
alembic revision --autogenerate -m "mensaje"
alembic upgrade head
alembic downgrade -1

# (Opcional) Poblar datos
python scripts/seed_db.py
```

### 🎯 Convenciones de Código

- Seguir PEP 8 para estilo de código
- Usar docstrings en todas las funciones
- Nomenclatura en español para el dominio de negocio
- Nombres descriptivos para variables y funciones
- Crear tests para funcionalidades críticas

## Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app

# Ejecutar tests de un módulo específico
pytest tests/test_equipo1.py
```

## 📋 FORMA DE TRABAJO

### 🗂️ Organización de Carpetas y Contenido

#### Estructura de cada módulo:
```
app/modules/[nombre_modulo]/
├── __init__.py
├── controllers/                   # 🎯 CONTROLADORES HTTP (APIRouter)
│   ├── __init__.py
│   └── [modulo]_controller.py     # Endpoints REST, validación de entrada
├── services/                      # 💼 LÓGICA DE NEGOCIO
│   ├── __init__.py  
│   └── [modulo]_service.py        # Reglas de negocio, orquestación
├── repositories/                  # 🗄️ ACCESO A DATOS
│   ├── __init__.py
│   └── [modulo]_repository.py     # Consultas DB, CRUD operations
├── dto/                           # 📝 ESQUEMAS DE VALIDACIÓN
│   ├── __init__.py
│   └── [modulo]_dto.py            # Pydantic models, validación
└── models/                        # 🏗️ MODELOS DE BASE DE DATOS
    ├── __init__.py
    └── [modulo]_models.py         # SQLAlchemy models, relaciones
```

#### ¿Qué va en cada carpeta?

- Controllers (APIRouter) - Capa de presentación HTTP:
  - Definición de rutas y respuestas
  - Validación de entrada con Pydantic
  - Manejo de códigos de respuesta HTTP
  - Dependencias de autenticación/autorización
  - NO lógica de negocio aquí

- Services - Capa de lógica de negocio:
  - Reglas de negocio
  - Orquestación entre repositories
  - Validaciones de negocio y transacciones

- Repositories - Capa de acceso a datos:
  - CRUD con SQLAlchemy
  - Consultas complejas, filtros, paginación
  - NO lógica de negocio aquí

- DTOs (Pydantic) - Esquemas de datos:
  - Validación de entrada y salida
  - Serialización de respuestas
  - Tipado estricto

- Models (SQLAlchemy) - Definición de datos:
  - Tablas y relaciones
  - Restricciones y constraints
  - Métodos auxiliares del modelo

### 🌊 GitFlow - Flujo de Ramas

#### Estructura de Ramas:
```
main/master     ← Línea estable (solo releases)
└── develop     ← Desarrollo principal (integración)
    ├── feature/modulo1-login
    ├── feature/modulo2-estudiantes  
    ├── feature/modulo3-profesores
    └── hotfix/bug-critical
```

#### Comandos Git para GitFlow:

1️⃣ Configuración inicial:
```bash
git clone https://github.com/Kevinho71/BRISA-backend.git
cd BRISA-backend
git checkout develop
```

2️⃣ Crear feature para tu módulo:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/modulo[X]-[funcionalidad]

# Ejemplo para módulo de usuarios:
git checkout -b feature/modulo1-autenticacion
```

3️⃣ Desarrollo en tu feature:
```bash
git add .
git commit -m "feat: implementar login de usuarios"
git commit -m "feat: agregar validación de JWT"
git commit -m "test: añadir tests de autenticación"

git push origin feature/modulo1-autenticacion
```

4️⃣ Integración con develop:
```bash
git checkout develop
git pull origin develop
git checkout feature/modulo1-autenticacion
git rebase develop

# Resolver conflictos si existen
git add .
git rebase --continue

# Merge a develop
git checkout develop
git merge feature/modulo1-autenticacion
git push origin develop

# Eliminar feature branch
git branch -d feature/modulo1-autenticacion
git push origin --delete feature/modulo1-autenticacion
```

5️⃣ Hotfixes críticos:
```bash
git checkout main
git checkout -b hotfix/descripcion-bug
# ... hacer fix
git checkout main
git merge hotfix/descripcion-bug
git checkout develop  
git merge hotfix/descripcion-bug
```

#### Convenciones de Commits:
```bash
# Formato: tipo(scope): descripción
feat(usuarios): implementar endpoint de login
fix(estudiantes): corregir validación de cédula  
docs(readme): actualizar guía de instalación
test(profesores): añadir tests unitarios
refactor(shared): optimizar validadores
```

#### Pull Requests:
1. Crear PR desde tu feature hacia `develop`
2. Título descriptivo: `[MÓDULO X] Descripción de funcionalidad`
3. Descripción detallada: Qué hace, cómo probarlo
4. Revisar conflictos antes de solicitar review
5. Tests pasando
6. Asignar reviewers de otros módulos

### 🔄 Flujo de Trabajo Diario

```bash
# 🌅 Al iniciar el día
git checkout develop
git pull origin develop
git checkout tu-feature-branch
git rebase develop

# 💻 Durante el desarrollo  
git add .
git commit -m "feat: descripción específica"
git push origin tu-feature-branch

# 🌙 Al finalizar el día
git push origin tu-feature-branch  # Backup de tu trabajo
```

## 🤝 Contribución

Resumen del flujo de trabajo:
1. Feature branch: `git checkout -b feature/modulo[X]-[funcionalidad]`
2. Commits descriptivos: usar convenciones
3. Pull Request: desde feature hacia `develop`
4. Code Review: por el equipo
5. Tests: asegurar que pasen
6. Merge: integrar a `develop` tras aprobación

Ver sección FORMA DE TRABAJO para detalles del GitFlow.

## Variables de Entorno

- APP_ENV: Entorno de la aplicación (development, production)
- SECRET_KEY: Clave secreta para JWT
- DATABASE_URL: URL de conexión a la base de datos (ej. mysql+pymysql://user:pass@host:3306/db)
- CORS_ORIGINS: Orígenes permitidos para CORS (separados por comas)

## 💡 Ejemplo Práctico - Módulo de Usuarios

Estructura de archivos del equipo del Módulo 1:
```
app/modules/usuarios/
├── models/usuario_models.py                  # Usuario, Rol, Permiso
├── dto/usuario_dto.py                        # UsuarioCreateDTO, LoginDTO (Pydantic)  
├── repositories/usuario_repository.py        # UsuarioRepository (SQLAlchemy)
├── services/usuario_service.py               # UsuarioService, AuthService
└── controllers/usuario_controller.py         # /api/auth/*, /api/usuarios/* (APIRouter)
```

Flujo de desarrollo del Módulo 1:
```bash
# 1. Crear feature branch
git checkout -b feature/modulo1-sistema-autenticacion

# 2. Implementar archivos en orden:
# - models/ → dto/ → repositories/ → services/ → controllers/

# 3. Incluir el router en run.py o en app/__init__.py
# 4. Commits por cada funcionalidad completada  
# 5. Push y crear Pull Request a develop
```

## 🛠️ Tecnologías Utilizadas

- FastAPI: Framework web
- Uvicorn: ASGI server
- SQLAlchemy: ORM para base de datos
- Alembic: Migraciones de base de datos
- Pydantic: Validación y tipado de datos
- PyMySQL: Conector MySQL para Python
- PyJWT o python-jose: Autenticación JWT
- Pytest: Framework de testing
