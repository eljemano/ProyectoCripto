# Usa una imagen base de Python
FROM python:3.13-slim-bookworm
#FROM python:3.11.8-bullseye PARA EL DOCKER DE RASPBERRY

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema necesarias para PostgreSQL (cliente)
# Esto es crucial para que psycopg2-binary funcione correctamente con la BD
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos e instala las dependencias de Python
# Esto garantiza que las dependencias se instalen antes de copiar el codigo completo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copia el cOdigo de la aplicaciON
COPY . .

# Define el comando por defecto para ejecutar tu aplicacion
# AsegUrate de que app/main.py sea el punto de entrada principal
CMD ["python", "app/main.py"]

