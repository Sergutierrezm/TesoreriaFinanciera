import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path


# Busca el archivo .env en la raíz del proyecto
ruta_env = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=ruta_env)
# ----------------------------

def obtener_conexion():
    try:
        # Opcional: print(f"Conectando a: {os.getenv('DB_NAME')}") 
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        return conexion
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: No se pudo conectar a Postgres.")
        print(f"🔍 Detalles: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

