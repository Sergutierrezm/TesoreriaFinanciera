import sqlite3
from pathlib import Path

# Definimos la ruta donde se guardará la base de datos
# Al usar Path(__file__), nos aseguramos de que se cree en la carpeta del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "tesoreria_datos.db"

def obtener_conexion():
    """Establece conexión con la base de datos SQLite local."""
    try:
        # SQLite crea el archivo automáticamente si no existe al intentar conectar
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as e:
        print(f"❌ Error de SQLite: {e}")
        return None

def inicializar_base_de_datos():
    """
    Crea la tabla necesaria si el usuario abre el programa por primera vez.
    Esto hace que el programa sea 'independiente'.
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

