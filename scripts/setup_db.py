# Inicializacion de la base de datos

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

#Cargar variables desde .env
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def create_database_if_not_exists():
    #"""Crea la base de datos en Postgres si no existe, con UTF-8."""
    # Conexion al motor postgres "general", no a crypto_db
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres", isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname=:name"), {"name": DB_NAME})
        exists = result.scalar()
        if not exists:
            print(f"Nueva instalacion, creando BD: {DB_NAME} ...")
            conn.execute(text(f"CREATE DATABASE {DB_NAME} WITH ENCODING 'UTF8' TEMPLATE template0"))
        else:
            print(f"La BD: {DB_NAME} ya existe")


if __name__ == "__main__":
    create_database_if_not_exists()
