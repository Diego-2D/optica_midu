import sqlite3
from pathlib import Path

# Definimos la ruta de la base de datos relativa a la raíz del proyecto
DB_PATH = Path(__file__).resolve().parent.parent / "optica_midu.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection():
    """Crea y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Permite acceder a las columnas por su nombre además de por índice
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa la base de datos ejecutando el archivo schema.sql."""
    if not DB_PATH.exists():
        print("Creando la base de datos por primera vez...")

    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_script = f.read()

    with conn:
        conn.executescript(schema_script)

    conn.close()
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()