import sys
import os

# Hacer que Python reconozca la carpeta raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.core.database import SessionLocal
from app.modules.usuarios.models import Usuario
from app.shared.security import hash_password

def resetear_passwords():
    db = SessionLocal()
    try:
        nueva_password = hash_password("1234")
        db.query(Usuario).update({Usuario.password: nueva_password})
        db.commit()
        print("✅ Todas las contraseñas fueron reestablecidas a 1234")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        db.close()

resetear_passwords()
