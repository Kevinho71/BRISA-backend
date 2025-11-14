"""
USO:
    python scripts/migrate_passwords_direct.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt

# CONEXIÓN DIRECTA (cambiar según tu configuración)
DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/bienestar_estudiantil?charset=utf8mb4"

print("=" * 60)
print("MIGRACIÓN DE CONTRASEÑAS - CONEXIÓN DIRECTA")
print("=" * 60)
print(f"\n🔌 Conectando a: {DATABASE_URL.split('@')[1]}")

# Crea engine y session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def hash_password(password: str) -> str:
    """Hashear contraseña con bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def es_hash_bcrypt(password: str) -> bool:
    """Verificar si ya está hasheada"""
    if not password:
        return False
    return password.startswith(('$2a$', '$2b$', '$2y$')) and len(password) == 60


def crear_tabla_backup(db):
    """Crear tabla temporal para backup"""
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS usuarios_password_backup (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL,
                usuario VARCHAR(50),
                -- password_original VARCHAR(255),
                password_hasheada VARCHAR(255),
                fecha_migracion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            )
        """))
        db.commit()
        print("✅ Tabla de backup creada")
    except Exception as e:
        print(f"⚠️  Error al crear tabla backup: {e}")
        db.rollback()


def migrar_contraseñas():
    """Migrar contraseñas de texto plano a hash"""
    
    db = SessionLocal()
    
    try:
        # Crea tabla de backup
        crear_tabla_backup(db)
        
        # Obtiene los usuarios
        result = db.execute(text("SELECT id_usuario, usuario, password FROM usuarios"))
        usuarios = result.fetchall()
        
        if not usuarios:
            print("⚠️  No se encontraron usuarios")
            return
        
        print(f"\n📊 Total de usuarios: {len(usuarios)}")
        print("\n🔄 Procesando usuarios...\n")
        
        migradas = 0
        ya_hasheadas = 0
        errores = 0
        
        for usuario in usuarios:
            id_usuario, username, password = usuario
            
            try:
                # Verifica si ya está hasheada
                if es_hash_bcrypt(password):
                    print(f"⏭  '{username}' - Ya tiene hash bcrypt")
                    ya_hasheadas += 1
                    continue
                
                print(f"🔐 '{username}' - Password plana: '{password}'")
                
                # Hashear
                password_hasheada = hash_password(password)
                
                # Backup
                db.execute(text("""
                    INSERT INTO usuarios_password_backup 
                    (id_usuario, usuario, password_original, password_hasheada)
                    VALUES (:id_usuario, :usuario, :password_original, :password_hasheada)
                """), {
                    'id_usuario': id_usuario,
                    'usuario': username,
                    'password_original': password,
                    'password_hasheada': password_hasheada
                })
                
                # Actualizar
                db.execute(text("""
                    UPDATE usuarios 
                    SET password = :password_hasheada 
                    WHERE id_usuario = :id_usuario
                """), {
                    'password_hasheada': password_hasheada,
                    'id_usuario': id_usuario
                })
                
                db.commit()
                print(f"   ✅ Migrada exitosamente")
                migradas += 1
                
            except Exception as e:
                print(f"   X Error: {e}")
                db.rollback()
                errores += 1
        
        # Resumen
        print("\n" + "=" * 60)
        print("📋 RESUMEN")
        print("=" * 60)
        print(f"- Migradas:           {migradas}")
        print(f"-  Ya hasheadas:       {ya_hasheadas}")
        print(f"X Errores:            {errores}")
        print(f"- Total:              {len(usuarios)}")
        print("=" * 60)
        
        if migradas > 0:
            print(f"\n - Backup en: usuarios_password_backup")
            
    except Exception as e:
        print(f"\n X Error general: {e}")
        db.rollback()
    finally:
        db.close()


def verificar_migracion():
    """Verificar estado de las contraseñas"""
    
    print("\n" + "=" * 60)
    print("VERIFICACIÓN")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        result = db.execute(text("""
            SELECT usuario, password,
                   CASE 
                       WHEN password LIKE '$2%' THEN 'HASH'
                       ELSE 'PLANO'
                   END as estado
            FROM usuarios
        """))
        
        usuarios = result.fetchall()
        
        con_hash = sum(1 for u in usuarios if u[2] == 'HASH')
        sin_hash = sum(1 for u in usuarios if u[2] == 'PLANO')
        
        print(f"\n / Con hash:    {con_hash}")
        print(f"X Sin hash:    {sin_hash}")
        
        if sin_hash > 0:
            print("\n⚠️  Usuarios sin hash:")
            for u in usuarios:
                if u[2] == 'PLANO':
                    print(f"   - {u[0]}")
        else:
            print("\n¡Todas las contraseñas hasheadas!")
            
    except Exception as e:
        print(f"\nX Error: {e}")
    finally:
        db.close()


def mostrar_backup():
    """Mostrar tabla de backup"""
    
    print("\n" + "=" * 60)
    print("BACKUP")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        result = db.execute(text("""
            SELECT usuario, password_original, 
                   DATE_FORMAT(fecha_migracion, '%Y-%m-%d %H:%i:%s') as fecha
            FROM usuarios_password_backup
            ORDER BY fecha_migracion DESC
        """))
        
        backups = result.fetchall()
        
        if not backups:
            print("\n -!!-  No hay registros de backup")
            return
        
        print(f"\n📋 Total: {len(backups)}\n")
        print(f"{'Usuario':<20} {'Password Original':<20} {'Fecha'}")
        print("-" * 70)
        
        for b in backups:
            print(f"{b[0]:<20} {b[1]:<20} {b[2]}")
            
    except Exception as e:
        print(f"\n X Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--verificar', action='store_true')
    parser.add_argument('--backup', action='store_true')
    
    args = parser.parse_args()
    
    if args.verificar:
        verificar_migracion()
    elif args.backup:
        mostrar_backup()
    else:
        print("\n⚠️  Este script modificará TODAS las contraseñas")
        print("   Se creará backup automático\n")
        
        respuesta = input("¿Continuar? (SI/no): ")
        
        if respuesta.upper() == 'SI':
            migrar_contraseñas()
            verificar_migracion()
        else:
            print("\nX Cancelado")
    
    print("\n" + "=" * 60)