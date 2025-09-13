# -*- coding: utf-8 -*-
import os
import sys
import locale
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
# CORRECCION: Se cambia la importacion relativa a absoluta
from app.databases.models import Base

# Configuracion defensiva de encoding
if sys.version_info[0] == 3:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def get_db_engine() -> Engine:
    """
    Funcion que crea y retorna el 'engine' de la base de datos
    utilizando las variables de entorno.
    """
    # --- Configuracion de la conexion a la base de datos ---
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    # Construir la URL de conexion de forma dinamica
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?client_encoding=utf8"

    # Crear el 'engine' que gestionara la conexion a la BD
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        return engine
    except Exception as e:
        print(f"Error al crear el engine de la base de datos: {str(e)}")
        sys.exit(1)

def create_db_tables(engine: Engine):
    """Crea todas las tablas en la base de datos a partir de los modelos de SQLAlchemy."""
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente")

def get_db(engine: Engine):
    """
    Funcion de ayuda para obtener una sesion de la base de datos.
    Se puede usar con 'with' o en frameworks como FastAPI.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
