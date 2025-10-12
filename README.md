# BRISA Backend API

Backend API REST desarrollado en Flask para el sistema de gestión institucional BRISA de la Universidad Católica Boliviana. 
Arquitectura modular diseñada para desarrollo colaborativo entre múltiples equipos.

## 🏗️ Estructura del Proyecto

```
BRISA_BACKEND/
├── app/
│   ├── __init__.py              # Factory de la aplicación Flask
│   ├── config/
│   │   ├── config.py           # Configuraciones por ambiente
│   │   └── database.py         # Configuración de base de datos
│   ├── core/
│   │   ├── extensions.py       # Extensiones Flask (DB, JWT, CORS)
│   │   └── utils.py           # Utilidades generales
│   ├── shared/                 # Elementos compartidos entre módulos
│   │   ├── models/            # Modelos base (BaseModel, PersonaBase)
│   │   ├── dto/               # DTOs base y esquemas compartidos
│   │   ├── services/          # Servicios base y de auditoría
│   │   ├── validators/        # Validadores personalizados
│   │   ├── exceptions/        # Excepciones personalizadas
│   │   └── decorators/        # Decoradores de autenticación
│   └── modules/               # Módulos funcionales del sistema
│       ├── health/           # Health checks y monitoreo
│       ├── usuarios/         # Usuarios, Roles y Permisos
│       │   ├── controllers/  # Controladores HTTP
│       │   ├── services/     # Lógica de negocio
│       │   ├── repositories/ # Acceso a datos
│       │   ├── dto/         # Esquemas de validación
│       │   └── models/      # Modelos de base de datos
│       ├── estudiantes/      # Estudiantes y Cursos
│       ├── profesores/       # Profesores y Materias  
│       ├── retiros_tempranos/ # Gestión de retiros tempranos
│       ├── incidentes/       # Incidentes y Bienestar Estudiantil
│       ├── esquelas/         # Reconocimientos y Orientación
│       ├── administracion/   # Administración general
│       └── reportes/         # Reportes e integración
├── tests/                    # Tests unitarios e integración
├── docs/                     # Documentación del proyecto
├── venv/                     # Entorno virtual (no en git)
├── requirements.txt          # Dependencias Python
├── .env                     # Variables de entorno (local)
├── .env.example             # Plantilla de variables
├── .gitignore
├── README.md
└── run.py                   # Punto de entrada
```

## 📋 Módulos del Sistema

Todos los módulos están listos para implementación con su estructura MVC completa:

### MÓDULO 1: Usuarios, Roles y Permisos 🏗️
- **Responsable**: Sistema base de autenticación
- **Carpeta**: `app/modules/usuarios/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 2: Estudiantes y Cursos 🏗️
- **Responsable**: Gestión académica de estudiantes  
- **Carpeta**: `app/modules/estudiantes/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 3: Profesores y Materias 🏗️
- **Responsable**: Gestión docente
- **Carpeta**: `app/modules/profesores/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 4: Retiros Tempranos 🏗️
- **Responsable**: Proceso de retiros
- **Carpeta**: `app/modules/retiros_tempranos/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 5: Incidentes / Bienestar Estudiantil 🏗️
- **Responsable**: Bienestar estudiantil
- **Carpeta**: `app/modules/incidentes/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 6: Esquelas (Reconocimiento y Orientación) 🏗️
- **Responsable**: Comunicaciones institucionales
- **Carpeta**: `app/modules/esquelas/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 7: Administración 🏗️
- **Responsable**: Gestión administrativa
- **Carpeta**: `app/modules/administracion/`
- **Estado**: Estructura creada - Pendiente implementación

### MÓDULO 8: Integración y Reportes 🏗️
- **Responsable**: Reportería y dashboards
- **Carpeta**: `app/modules/reportes/`
- **Estado**: Estructura creada - Pendiente implementación

## 🚀 Configuración del Entorno

### 1. Clonar el repositorio

```bash
# Clonar el repositorio
git clone https://github.com/tu-organizacion/BRISA_BACKEND.git

# Ingresar al directorio del proyecto
cd BRISA_BACKEND
```

### 2. Prerrequisitos
- Python 3.8+
- MySQL 8.0+ 
- Git

### 3. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Windows)
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
-- Crear base de datos
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

### 7. Inicializar base de datos

```bash
# Inicializar estructura
flask init-db

# Poblar con datos iniciales (opcional)
flask seed-db
```

### 8. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🔗 Endpoints Disponibles

### Sistema ✅
- **GET** `/api/health` - Estado de la API
- **GET** `/api/status` - Estado detallado del sistema

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
├── __init__.py          # Identificación del módulo
├── controllers/         # Controladores HTTP (endpoints)
│   ├── __init__.py
│   └── [modulo]_controller.py
├── services/           # Lógica de negocio  
│   ├── __init__.py
│   └── [modulo]_service.py
├── repositories/       # Acceso a datos
│   ├── __init__.py
│   └── [modulo]_repository.py
├── dto/               # Esquemas de validación
│   ├── __init__.py
│   └── [modulo]_dto.py
└── models/            # Modelos de base de datos
    ├── __init__.py
    └── [modulo]_models.py
```

### 🔧 Pasos para Implementar un Módulo

1. **Definir modelos** en `models/[modulo]_models.py`
2. **Crear DTOs** para validación en `dto/[modulo]_dto.py`
3. **Implementar repository** para acceso a datos
4. **Desarrollar services** con lógica de negocio
5. **Crear controllers** con endpoints HTTP
6. **Registrar blueprint** en `app/__init__.py`

### 📚 Recursos Compartidos Disponibles

- **Modelos base**: `app/shared/models/base_models.py`
- **DTOs base**: `app/shared/dto/base_dto.py`
- **Validadores**: `app/shared/validators/custom_validators.py`
- **Excepciones**: `app/shared/exceptions/custom_exceptions.py`
- **Decoradores**: `app/shared/decorators/auth_decorators.py`

### ⚡ Comandos CLI Disponibles

```bash
# Inicializar base de datos
flask init-db

# Resetear base de datos
flask reset-db
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

#### **Estructura de cada módulo:**
```
app/modules/[nombre_modulo]/
├── __init__.py                    # Identificación del módulo
├── controllers/                   # 🎯 CONTROLADORES HTTP
│   ├── __init__.py
│   └── [modulo]_controller.py    # Endpoints REST, validación de entrada
├── services/                      # 💼 LÓGICA DE NEGOCIO
│   ├── __init__.py  
│   └── [modulo]_service.py       # Reglas de negocio, orchestración
├── repositories/                  # 🗄️ ACCESO A DATOS
│   ├── __init__.py
│   └── [modulo]_repository.py    # Consultas DB, CRUD operations
├── dto/                          # 📝 ESQUEMAS DE VALIDACIÓN
│   ├── __init__.py
│   └── [modulo]_dto.py          # Marshmallow schemas, validación
└── models/                       # 🏗️ MODELOS DE BASE DE DATOS
    ├── __init__.py
    └── [modulo]_models.py       # SQLAlchemy models, relaciones
```

#### **¿Qué va en cada carpeta?**

**📁 Controllers** - Capa de presentación HTTP:
- Definición de endpoints (rutas)
- Validación de parámetros de entrada
- Manejo de códigos de respuesta HTTP
- Uso de decoradores de autenticación
- **NO** lógica de negocio aquí

**📁 Services** - Capa de lógica de negocio:
- Reglas de negocio complejas
- Orchestración entre diferentes repositories
- Validaciones de negocio
- Transformaciones de datos
- Manejo de transacciones

**📁 Repositories** - Capa de acceso a datos:
- Operaciones CRUD (Create, Read, Update, Delete)
- Consultas complejas a la base de datos
- Filtros y paginación
- **NO** lógica de negocio aquí

**📁 DTOs** - Esquemas de datos:
- Validación de entrada con Marshmallow
- Serialización de respuestas
- Transformación de tipos de datos
- Documentación implícita de la API

**📁 Models** - Definición de datos:
- Modelos de SQLAlchemy
- Relaciones entre tablas
- Validaciones a nivel de base de datos
- Métodos auxiliares del modelo

### 🌊 GitFlow - Flujo de Ramas

#### **Estructura de Ramas:**
```
main/master     ← Producción (solo releases)
└── develop     ← Desarrollo principal (integración)
    ├── feature/modulo1-login
    ├── feature/modulo2-estudiantes  
    ├── feature/modulo3-profesores
    └── hotfix/bug-critical
```

#### **Comandos Git para GitFlow:**

**1️⃣ Configuración inicial:**
```bash
# Clonar y configurar repositorio
git clone [url-repositorio]
cd BRISA_BACKEND
git checkout develop  # Trabajar desde develop
```

**2️⃣ Crear feature para tu módulo:**
```bash
# Crear nueva feature desde develop
git checkout develop
git pull origin develop
git checkout -b feature/modulo[X]-[funcionalidad]

# Ejemplo para módulo de usuarios:
git checkout -b feature/modulo1-autenticacion
```

**3️⃣ Desarrollo en tu feature:**
```bash
# Hacer cambios y commits frecuentes
git add .
git commit -m "feat: implementar login de usuarios"
git commit -m "feat: agregar validación de JWT"
git commit -m "test: añadir tests de autenticación"

# Subir cambios regularmente
git push origin feature/modulo1-autenticacion
```

**4️⃣ Integración con develop:**
```bash
# Antes de merge, actualizar con develop
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

**5️⃣ Hotfixes críticos:**
```bash
# Para bugs urgentes en producción
git checkout main
git checkout -b hotfix/descripcion-bug
# ... hacer fix
git checkout main
git merge hotfix/descripcion-bug
git checkout develop  
git merge hotfix/descripcion-bug
```

#### **Convenciones de Commits:**
```bash
# Formato: tipo(scope): descripción
feat(usuarios): implementar endpoint de login
fix(estudiantes): corregir validación de cédula  
docs(readme): actualizar guía de instalación
test(profesores): añadir tests unitarios
refactor(shared): optimizar validadores
```

#### **Pull Requests:**
1. **Crear PR** desde tu feature hacia `develop`
2. **Título descriptivo**: `[MÓDULO X] Descripción de funcionalidad`
3. **Descripción detallada**: Qué hace, cómo probarlo
4. **Revisar conflictos** antes de solicitar review
5. **Tests pasando** - verificar que no rompe nada
6. **Asignar reviewers** de otros módulos

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

**Resumen del flujo de trabajo:**
1. **Feature branch**: `git checkout -b feature/modulo[X]-[funcionalidad]`
2. **Commits descriptivos**: Usar convenciones de commits
3. **Pull Request**: Desde feature hacia `develop`
4. **Code Review**: Revisión por otros miembros del equipo
5. **Tests**: Asegurar que todos los tests pasen
6. **Merge**: Integración a develop después de aprobación

Ver sección **📋 FORMA DE TRABAJO** para detalles completos del GitFlow.

## Variables de Entorno

- `FLASK_ENV`: Entorno de la aplicación (development, production)
- `SECRET_KEY`: Clave secreta para JWT y sesiones
- `DATABASE_URL`: URL de conexión a la base de datos
- `CORS_ORIGINS`: Orígenes permitidos para CORS

## 💡 Ejemplo Práctico - Módulo de Usuarios

**Estructura de archivos del equipo del Módulo 1:**
```
app/modules/usuarios/
├── models/usuario_models.py       # Usuario, Rol, Permiso
├── dto/usuario_dto.py            # UsuarioCreateDTO, LoginDTO  
├── repositories/usuario_repository.py  # UsuarioRepository
├── services/usuario_service.py   # UsuarioService, AuthService
└── controllers/usuario_controller.py   # /api/auth/*, /api/usuarios/*
```

**Flujo de desarrollo del Módulo 1:**
```bash
# 1. Crear feature branch
git checkout -b feature/modulo1-sistema-autenticacion

# 2. Implementar archivos en orden:
# - models/ → dto/ → repositories/ → services/ → controllers/

# 3. Registrar blueprint en app/__init__.py
# 4. Commits por cada funcionalidad completada  
# 5. Push y crear Pull Request a develop
```

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM para base de datos
- **Flask-Migrate**: Migraciones de base de datos
- **Flask-JWT-Extended**: Autenticación JWT
- **Flask-CORS**: Manejo de CORS
- **Marshmallow**: Serialización/deserialización
- **PyMySQL**: Conector MySQL para Python
- **Pytest**: Framework de testing