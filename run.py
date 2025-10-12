"""
Punto de entrada principal para la aplicación BRISA Backend
"""

import os
from app import create_app

# Obtener configuración del entorno
config_name = os.environ.get('FLASK_ENV', 'development')

# Crear aplicación
app = create_app(config_name)

if __name__ == '__main__':
    # Configuración para desarrollo
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Iniciando BRISA Backend API en puerto {port}")
    print(f"📝 Entorno: {config_name}")
    print(f"🔧 Debug: {debug}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"❤️  Health Check: http://localhost:{port}/api/health")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )