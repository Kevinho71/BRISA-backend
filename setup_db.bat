@echo off
REM Script para configuración rápida de base de datos en Windows
REM Ejecutar como: setup_db.bat

echo.
echo ====================================================
echo CONFIGURACION RAPIDA - BRISA Backend
echo ====================================================
echo.

REM Verificar si .env existe
if not exist ".env" (
    echo [1/6] Creando archivo .env...
    copy .env.example .env
    echo     ✓ Archivo .env creado
    echo.
    echo     ⚠️  IMPORTANTE: Edita .env y configura tus credenciales de MySQL
    echo     DATABASE_URL=mysql+pymysql://root:TU_PASSWORD@localhost:3306/brisa_db
    echo.
    pause
) else (
    echo [1/6] Archivo .env ya existe ✓
)

echo.
echo [2/6] Instalando dependencias Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo     ✗ Error instalando dependencias
    pause
    exit /b 1
)
echo     ✓ Dependencias instaladas

echo.
echo [3/6] Probando conexión a MySQL...
python scripts/db_utils.py test
if errorlevel 1 (
    echo.
    echo     ✗ No se pudo conectar a MySQL
    echo.
    echo     Por favor verifica:
    echo     1. MySQL está corriendo
    echo     2. Las credenciales en .env son correctas
    echo     3. La base de datos 'brisa_db' existe
    echo.
    echo     Para crear la base de datos ejecuta:
    echo     mysql -u root -p -e "CREATE DATABASE brisa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo.
    pause
    exit /b 1
)

echo.
echo [4/6] ¿Quieres ejecutar el esquema SQL? (Esto creará las tablas)
echo     Opción: mysql -u root -p brisa_db ^< docs/brisa_tablas.sql
set /p ejecutar_schema="Ejecutar ahora? (S/N): "
if /i "%ejecutar_schema%"=="S" (
    echo     Ejecutando esquema...
    REM Nota: Puede requerir ingresar password
    mysql -u root -p brisa_db < docs/brisa_tablas.sql
    if errorlevel 1 (
        echo     ✗ Error ejecutando esquema
    ) else (
        echo     ✓ Esquema ejecutado correctamente
    )
) else (
    echo     - Saltado (ejecutar manualmente después)
)

echo.
echo [5/6] ¿Quieres cargar los datos de prueba?
echo     Archivo: docs/seed_data.sql
set /p cargar_datos="Cargar datos de prueba? (S/N): "
if /i "%cargar_datos%"=="S" (
    echo     Cargando datos...
    mysql -u root -p brisa_db < docs/seed_data.sql
    if errorlevel 1 (
        echo     ✗ Error cargando datos
    ) else (
        echo     ✓ Datos de prueba cargados
    )
) else (
    echo     - Saltado
)

echo.
echo [6/6] Configuración completada!
echo.
echo ====================================================
echo SIGUIENTE PASO: Iniciar la aplicación
echo ====================================================
echo.
echo Ejecuta: python run.py
echo.
echo La API estará disponible en:
echo   🌐 API: http://localhost:8000
echo   📖 Docs: http://localhost:8000/docs
echo   ❤️  Health: http://localhost:8000/api/health
echo.
echo ====================================================
echo.
pause
