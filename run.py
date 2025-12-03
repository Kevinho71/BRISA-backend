"""
Punto de entrada principal para la aplicación BRISA Backend
"""
import os
import uvicorn
from app.main import app  

# Obtener configuración del entorno
config_name = os.environ.get('ENV', 'development')


if __name__ == '__main__':
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENV", "development") == "development"
    
    print(f"🚀 Iniciando BRISA Backend API en puerto {port}")
    print(f"📝 Entorno: {config_name}")
    print(f"🔧 Auto-reload: {reload}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"📖 Docs: http://localhost:{port}/docs")
    print(f"❤️  Health Check: http://localhost:{port}/api/health")
    
    uvicorn.run(
        "run:app",
        host='127.0.0.1',
        port=port,
        reload=reload,
        log_level="info"
    )