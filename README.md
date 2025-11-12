# BRISA Backend - API REST

Backend del sistema BRISA (Bienestar Estudiantil) desarrollado con FastAPI y MySQL.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Kevinho71/BRISA-backend.git
cd BRISA-backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **¡Listo para usar!**

El archivo `.env` ya está configurado con las credenciales de la base de datos compartida en Aiven Cloud. No necesitas configurar nada más.

### Ejecutar el servidor

```bash
python main.py
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez el servidor esté corriendo, puedes acceder a:

- **Swagger UI (Interactivo)**: http://localhost:8000/docs
- **ReDoc (Documentación)**: http://localhost:8000/redoc

## 🗄️ Base de Datos

El proyecto está conectado a una base de datos MySQL en **Aiven Cloud**:
- **Host**: bienestarestudiantil-hola.e.aivencloud.com:19241
- **Base de datos**: defaultdb
- **Usuario**: avnadmin
- **Conexión SSL**: Configurada automáticamente

⚠️ **Nota**: Las credenciales están compartidas en el archivo `.env` del repositorio para facilitar el desarrollo en equipo. Todos los miembros tienen acceso de lectura/escritura.

## 📁 Estructura del Proyecto

```
BRISA_BACKEND/
├── controllers/          # Endpoints de la API (rutas)
├── services/            # Lógica de negocio
├── repositories/        # Acceso a datos (DAL)
├── models/              # Modelos de base de datos (SQLAlchemy)
├── dtos/                # Data Transfer Objects (Pydantic)
├── database/            # Configuración de conexión a BD
├── docs/                # Documentación y migraciones SQL
├── .env                 # Variables de entorno (COMPARTIDO)
├── main.py              # Punto de entrada de la aplicación
└── requirements.txt     # Dependencias del proyecto
```

## 🔧 Módulos Disponibles

### Retiros Tempranos
Gestión completa de solicitudes de retiro temprano de estudiantes:
- **35 endpoints REST** organizados en 5 categorías
- Workflow simplificado: recibida → derivada → aprobada/rechazada
- Ver documentación detallada en: `docs/CAMBIOS_SIMPLIFICACION_FLUJO.md`

### Otros módulos
*(Agregar según se implementen)*

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **MySQL** - Base de datos relacional
- **PyMySQL** - Driver de conexión a MySQL
- **CORS** - Configurado para desarrollo frontend

## 👥 Equipo de Desarrollo

- **Kevinho71** - kevin.guzman@ucb.edu.bo

## 📝 Notas para Desarrolladores

### Ramas
- `main` - Rama principal (producción)
- `retiros` - Desarrollo del módulo de retiros tempranos
- Crear ramas feature para nuevas funcionalidades

### Migraciones de Base de Datos
Las migraciones SQL se encuentran en la carpeta `docs/`:
- `migration_solicitudes_flujo_aprobacion.sql` - Campos de workflow
- `migration_simplificacion_flujo.sql` - Actualización de ENUMs
- `migration_eliminar_foto_retirante.sql` - Eliminación de columna obsoleta

### Commits
Usar convención de commits semánticos:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `refactor:` - Refactorización de código
- `test:` - Pruebas

## 🔐 Seguridad

⚠️ **Importante**: Este proyecto comparte las credenciales de desarrollo para facilitar el trabajo en equipo. Para producción, usar variables de entorno seguras y nunca compartir credenciales en el repositorio.

## 📞 Soporte

Para cualquier duda o problema, contactar al equipo de desarrollo.
