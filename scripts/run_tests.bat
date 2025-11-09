@echo off
REM run_tests.bat - Script para ejecutar tests en Windows

echo ========================================
echo   SUITE DE TESTING - BACKEND API
echo ========================================
echo.

REM Verificar que requirements.txt existe
if not exist "requirements.txt" (
    echo Error: requirements.txt no encontrado
    echo Ejecuta este script desde el directorio raiz del proyecto
    exit /b 1
)

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo [OK] Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo [AVISO] No se encontro entorno virtual (venv)
)

REM Instalar dependencias de testing
echo [OK] Instalando dependencias de testing...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo   1. TESTS UNITARIOS
echo ========================================
pytest tests/test_auth_service.py -v --tb=short -m unit

echo.
echo ========================================
echo   2. TESTS DE ENDPOINTS
echo ========================================
pytest tests/test_auth_endpoints.py -v --tb=short

echo.
echo ========================================
echo   3. TESTS DE ROLES Y PERMISOS
echo ========================================
pytest tests/test_roles_permisos.py -v --tb=short

echo.
echo ========================================
echo   4. TESTS DE INTEGRACION
echo ========================================
pytest tests/test_integration.py -v --tb=short -m integration

echo.
echo ========================================
echo   5. TESTS COMPLETOS CON COBERTURA
echo ========================================
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

echo.
echo ========================================
echo   [OK] TESTS COMPLETADOS
echo ========================================
echo.
echo Reporte de cobertura generado en: htmlcov\index.html
echo Abre el archivo en tu navegador para ver el reporte detallado
echo.

REM Abrir reporte automaticamente
start htmlcov\index.html

pause