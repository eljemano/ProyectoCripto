# Este script automatiza la configuración del entorno virtual.

# Paso 1: Establece la política de ejecución para permitir la ejecución de scripts en esta sesión.
# 'Bypass' es menos restrictivo que 'RemoteSigned', pero es seguro para un script local.
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Paso 2: Verifica si la carpeta del entorno virtual (.venv) existe y la elimina.
if (Test-Path -Path ".venv") {
    Write-Host "Eliminando la carpeta .venv..."
    Remove-Item -Recurse -Force .venv
    Write-Host "Carpeta .venv eliminada."
} else {
    Write-Host "La carpeta .venv no existe. No se requiere eliminación."
}

# Paso 3: Crea un nuevo entorno virtual.
Write-Host "Creando un nuevo entorno virtual..."
python -m venv .venv
Write-Host "Entorno virtual creado."

# Paso 4: Activa el nuevo entorno virtual.
Write-Host "Activando el entorno virtual..."
.\.venv\Scripts\Activate.ps1

# Paso 5: Instala las dependencias del archivo requirements.txt.
Write-Host "Instalando las dependencias..."
pip install -r requirements.txt

Write-Host "¡La configuración del entorno virtual ha finalizado!"