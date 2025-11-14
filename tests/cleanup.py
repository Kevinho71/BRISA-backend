"""
tests/cleanup.py
Script para limpiar archivos de test problemáticos y caché
"""
import os
import glob
import shutil

def cleanup_test_files():
    """Limpiar archivos de caché y temporales"""
    
    print("🧹 Iniciando limpieza de archivos de test...\n")
    
    # Directorios de caché a eliminar
    cache_dirs = [
        '.pytest_cache',
        '__pycache__',
        'tests/__pycache__',
        'app/__pycache__',
        'htmlcov',
        '.coverage'
    ]
    
    removed_count = 0
    
    # Eliminar directorios de caché
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                if os.path.isfile(cache_dir):
                    os.remove(cache_dir)
                    print(f"✓ Eliminado archivo: {cache_dir}")
                else:
                    shutil.rmtree(cache_dir)
                    print(f"✓ Eliminado directorio: {cache_dir}")
                removed_count += 1
            except Exception as e:
                print(f"✗ Error al eliminar {cache_dir}: {e}")
    
    # Eliminar archivos .pyc recursivamente
    pyc_count = 0
    for pyc_file in glob.glob('**/*.pyc', recursive=True):
        try:
            os.remove(pyc_file)
            pyc_count += 1
        except Exception as e:
            print(f"✗ Error al eliminar {pyc_file}: {e}")
    
    if pyc_count > 0:
        print(f"✓ Eliminados {pyc_count} archivos .pyc")
    
    # Eliminar archivos __pycache__ recursivamente
    pycache_count = 0
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    pycache_count += 1
                except Exception as e:
                    print(f"✗ Error al eliminar {dir_path}: {e}")
    
    if pycache_count > 0:
        print(f"✓ Eliminados {pycache_count} directorios __pycache__")
    
    # Eliminar archivos de base de datos SQLite de test
    db_files = glob.glob('*.db')
    for db_file in db_files:
        if 'test' in db_file.lower():
            try:
                os.remove(db_file)
                print(f"✓ Eliminada base de datos de test: {db_file}")
            except Exception as e:
                print(f"✗ Error al eliminar {db_file}: {e}")
    
    print(f"\n✅ Limpieza completada: {removed_count} elementos principales eliminados")
    print("\n💡 Ahora puedes ejecutar los tests con: pytest tests/ -v")

if __name__ == "__main__":
    cleanup_test_files()