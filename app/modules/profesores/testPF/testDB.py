import sys
import os

# ===================================================================
# Ajuste del path para que Python encuentre el módulo 'app' desde cualquier ubicación
# ===================================================================
# Obtiene la ruta absoluta del directorio raíz del proyecto (BRISA-backend)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.append(project_root)

# Ahora sí podemos importar el engine
from app.core.database import engine

# ===================================================================
# Prueba exclusiva de conexión a la base de datos
# ===================================================================
try:
    connection = engine.connect()
    print("✅ Conexión a la base de datos establecida correctamente")
    connection.close()
except Exception as e:
    print("❌ ERROR: No se pudo conectar a la base de datos:")
    print(e)