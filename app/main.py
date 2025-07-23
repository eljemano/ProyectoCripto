import psycopg2
import os
import time
# import requests # Comenta si no tienes requests o no lo usas en la parte de BD

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Comentar las líneas de Ollama para esta prueba
# OLLAMA_URL_REMOTE = os.getenv("OLLAMA_URL_REMOTE")
# print(f"DEBUG: Intentando conectar a Ollama en {OLLAMA_URL_REMOTE}")

print(f"DEBUG: Conectando a DB_HOST={DB_HOST}, DB_NAME={DB_NAME}, DB_USER={DB_USER}")


conn = None
for i in range(10): # Aumentar reintentos para dar tiempo a DB
    try:
        print(f"Intentando conectar a la base de datos (Intento {i+1}/10)...")
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        print("¡Conexión a la base de datos exitosa!")
        break
    except psycopg2.OperationalError as e:
        print(f"Error de conexión a DB: {e}. Reintentando en 5 segundos...")
        time.sleep(5)
    except Exception as e:
        print(f"Ocurrió un error inesperado al conectar a DB: {e}")
        break

if conn:
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS crypto_prices (id SERIAL PRIMARY KEY, symbol VARCHAR(10) NOT NULL, price NUMERIC(20, 8) NOT NULL, timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, api_response JSONB);")
        conn.commit()
        print("Tabla 'crypto_prices' verificada/creada.")

        # Lógica para interactuar con Ollama (TEMPORALMENTE COMENTADO PARA ESTA PRUEBA)
        # try:
        #     # ... tu código de Ollama ...
        # except Exception as e:
        #     print(f"Error al llamar a Ollama: {e}")


    except Exception as e:
        print(f"Error durante las operaciones de DB: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()
        print("Conexiones cerradas.")
else:
    print("No se pudo establecer conexión con la base de datos.")

print("Aplicación Python iniciada y realizando tareas iniciales (sin Ollama).")
# Mantén el script corriendo indefinidamente si es una aplicación de servicio
# while True:
#     time.sleep(60)