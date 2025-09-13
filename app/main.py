# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import traceback
import locale

#sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
#sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)

# Resto de tu código, incluyendo la carga de variables de entorno
# Añadir la carpeta raiz del proyecto a la ruta de Python
project_root = str(Path(__file__).parent.parent)

if project_root not in sys.path:
    sys.path.insert(0, str(project_root))

def load_environment_variables():
    """Carga variables de entorno desde .env en la raiz del proyecto"""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        raise FileNotFoundError(f"Archivo .env no encontrado en {env_path}")
    
    load_dotenv(dotenv_path=env_path, encoding='utf-8') 
    print("Variables cargadas desde:", env_path)

if __name__ == "__main__":
    try:
        load_environment_variables()
        
        # Verificacion explicita de variables.
        required_vars = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"Faltan variables: {missing_vars}. Por favor, revise su archivo .env.")
        else:
            print("Variables de entorno criticas:")
            for var in required_vars:
                print(f"{var}: {os.getenv(var)}")
             #RETIRAR SI FUNCIONA MODELS.PY Y DABATASE.PY
            from app.databases.database import get_db_engine, create_db_tables
            #from app.databases.db_unificado import get_db_engine, create_db_tables

            
            engine = get_db_engine()
            create_db_tables(engine)
            
    except Exception as e:
        print(f"Error al iniciar la aplicacion: {str(e)}")
        traceback.print_exc()
