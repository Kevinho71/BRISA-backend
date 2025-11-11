# 🔧 Guía de Configuración de Base de Datos

## ✅ Requisitos Previos

1. **MySQL Server** instalado y corriendo
2. **Python 3.9+** instalado
3. **Dependencias** instaladas

## 📋 Pasos de Configuración

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Crear la Base de Datos en MySQL

Abre MySQL y ejecuta:

```sql
CREATE DATABASE brisa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O desde la terminal:

```bash
mysql -u root -p -e "CREATE DATABASE brisa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. Configurar Credenciales

Edita el archivo `.env` en la raíz del proyecto y actualiza:

```env
DATABASE_URL=mysql+pymysql://TU_USUARIO:TU_PASSWORD@localhost:3306/brisa_db
```

Reemplaza:
- `TU_USUARIO` → tu usuario de MySQL (generalmente `root`)
- `TU_PASSWORD` → tu contraseña de MySQL

**Ejemplo:**
```env
DATABASE_URL=mysql+pymysql://root:mipassword123@localhost:3306/brisa_db
```

### 4. Probar la Conexión

```bash
python scripts/db_utils.py test
```

Deberías ver:
```
✅ Conexión a base de datos exitosa
📍 Base de datos actual: brisa_db
🔢 Versión de MySQL: 8.0.x
```

### 5. Crear las Tablas del Esquema

Tienes dos opciones:

#### Opción A: Ejecutar el script SQL directamente

```bash
mysql -u root -p brisa_db < docs/brisa_tablas.sql
```

#### Opción B: Usar SQLAlchemy (desde los modelos Python)

```bash
python scripts/db_utils.py create
```

⚠️ **Nota**: La Opción A es recomendada porque el SQL ya tiene todas las tablas, índices y constraints definidos.

### 6. Cargar Datos de Prueba

```bash
mysql -u root -p brisa_db < docs/seed_data.sql
```

Esto insertará:
- 7 Personas (profesores/administrativos)
- 10 Estudiantes
- 5 Cursos
- 8 Materias
- 8 Apoderados
- 15 Relaciones estudiante-apoderado
- 5 Motivos de retiro
- Y más...

### 7. Iniciar la Aplicación

```bash
python run.py
```

La API estará disponible en:
- 🌐 **API**: http://localhost:8000
- 📖 **Documentación**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/api/health

## 🛠️ Comandos Útiles

### Probar conexión
```bash
python scripts/db_utils.py test
```

### Crear tablas (solo si usas Opción B)
```bash
python scripts/db_utils.py create
```

### Resetear base de datos (⚠️ elimina todos los datos)
```bash
python scripts/db_utils.py reset
```

### Ver ayuda
```bash
python scripts/db_utils.py help
```

## ❌ Solución de Problemas

### Error: "Access denied for user"
**Causa**: Credenciales incorrectas en `.env`

**Solución**: Verifica tu usuario y contraseña de MySQL

### Error: "Unknown database 'brisa_db'"
**Causa**: La base de datos no existe

**Solución**: Ejecuta el paso 2 para crear la base de datos

### Error: "Can't connect to MySQL server"
**Causa**: MySQL no está corriendo

**Solución**: 
- Windows: Inicia el servicio MySQL desde Servicios
- Mac/Linux: `sudo service mysql start`

### Error: "No module named 'pymysql'"
**Causa**: Dependencias no instaladas

**Solución**: `pip install -r requirements.txt`

### Error: "Table 'X' already exists"
**Causa**: Intentando crear tablas que ya existen

**Solución**: 
- Si quieres recrear: `python scripts/db_utils.py reset`
- Si quieres mantener: ignora el error o comenta las líneas de creación

## 📝 Estructura de Archivos

```
BRISA_BACKEND/
├── .env                          # Configuración (NO subir a git)
├── .env.example                  # Plantilla de configuración
├── requirements.txt              # Dependencias Python
├── run.py                        # Punto de entrada
├── app/
│   ├── __init__.py              # Factory de la app
│   ├── config/
│   │   ├── config.py            # Configuraciones por entorno
│   │   └── database.py          # Utilidades de BD
│   └── core/
│       └── extensions.py        # Inicialización de SQLAlchemy
├── docs/
│   ├── brisa_tablas.sql         # Esquema completo de BD
│   └── seed_data.sql            # Datos de prueba
└── scripts/
    └── db_utils.py              # Utilidades para gestión de BD
```

## 🎯 Próximos Pasos

1. ✅ Configurar conexión ← **ESTÁS AQUÍ**
2. ⏭️ Crear base de datos
3. ⏭️ Ejecutar esquema SQL
4. ⏭️ Cargar datos de prueba
5. ⏭️ Probar endpoints en /docs

## 💡 Tips

- **Desarrollo**: Usa `ENV=development` en `.env` para ver las queries SQL
- **Producción**: Cambia a `ENV=production` y desactiva SQLALCHEMY_ECHO
- **Testing**: Usa una base de datos separada para tests
- **Migraciones**: Considera usar Alembic para cambios futuros en el esquema

## 🆘 ¿Necesitas Ayuda?

Si encuentras problemas, verifica:
1. ✅ MySQL está corriendo
2. ✅ Base de datos `brisa_db` existe
3. ✅ Credenciales en `.env` son correctas
4. ✅ Puerto 3306 está disponible
5. ✅ Dependencias están instaladas
