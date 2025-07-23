FROM python:3.13-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
# EXPOSE 8000 # Solo si tu app es una API web
CMD ["python", "main.py"]