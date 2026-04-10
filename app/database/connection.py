import sqlite3
import sys
import os
from pathlib import Path

# --- LÓGICA DE RUTA PARA EJECUTABLE ---
# Si el programa está "congelado" (es un .exe o binario de Mac)
if getattr(sys, 'frozen', False):
    # Usamos la ruta donde reside el archivo ejecutable que el usuario abrió
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Si estamos ejecutando el script .py normal en desarrollo
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Definimos la ruta final de la base de datos
DB_PATH = BASE_DIR / "tesoreria_datos.db"

def obtener_conexion():
    """Establece conexión con la base de datos SQLite local."""
    try:
        # SQLite crea el archivo automáticamente en DB_PATH si no existe
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as e:
        print(f"❌ Error de SQLite: {e}")
        return None

def inicializar_base_de_datos():
    """
    Crea la tabla necesaria si el usuario abre el programa por primera vez.
    Esto asegura que el archivo .db sea funcional desde el segundo 1.
    """
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            # Usamos INTEGER PRIMARY KEY AUTOINCREMENT para el ID en SQLite
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tesoreria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    anio INTEGER,
                    mes TEXT,
                    capital_liquido REAL,
                    inversion REAL,
                    total REAL
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
        finally:
            conn.close()