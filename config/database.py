import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Usamos 127.0.0.1 explícitamente para evitar resoluciones ambiguas en Windows
DB_USER = os.getenv("POSTGRES_USER", "f1_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "f1_password")
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5433")
DB_NAME = os.getenv("POSTGRES_DB", "f1_telemetry_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_engine():
    """
    Verifica y retorna el motor de conexión a PostgreSQL.
    """
    try:
        connection = engine.connect()
        connection.close()
        logging.info("✅ Conexión a PostgreSQL establecida exitosamente.")
        return engine
    except Exception as e:
        # Forzamos la conversión segura a string para evitar que pete por encodings en Windows
        error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
        logging.error(f"❌ Error de conexión: {error_msg}")
        raise

if __name__ == "__main__":
    get_db_engine()