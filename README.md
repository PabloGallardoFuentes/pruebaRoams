# API de Simulaciones de Hipotecas

Esta API RESTful permite gestionar clientes y realizar simulaciones de hipotecas.

## 🚀 Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/PabloGallardoFuentes/pruebaRoams.git
cd pruebaRoams
```

### 2️⃣ Crear y activar un entorno virtual

```bash
python -m venv roams  # Crear entorno virtual llamado 'roams'
```

En Windows:

```cmd
roams\Scripts\activate
```
Nota: Si sale error, habilitar la ejecución con 
```cmd
Set-ExecutionPolicy Unrestricted -Scope Process
```

En macOS/Linux:

```bash
source roams/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar la base de datos SQLite
 ```bash
python database.py  # Crea la base de datos y tablas necesarias
```

### 5️⃣ Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor se ejecutará en: http://127.0.0.1:8000

## 📌 Endpoints principales

### 1️⃣ Crear un cliente

**POST** /clientes/
```json
{
  "name": "Juan Pérez",
  "dni": "12345678Z",
  "email": "juan@example.com",
  "capital": 100000
}
```

### 2️⃣ Consultar cliente por DNI

**GET** /clientes/{dni}

Respuesta al ejemplo /clientes/12345678Z

```json
{
  "name": "Juan Pérez",
  "dni": "12345678Z",
  "email": "juan@example.com",
  "capital": 100000
}
```
### 3️⃣ Modificar cliente

**PUT** /clientes/{dni}
```json
{
  "name": "Juan Pérez",
  "dni": "12345678Z",
  "email": "nuevo_correo@example.com",
  "capital": 120000
}
```

### 4️⃣ Eliminar cliente

**DELETE** /clientes/{dni}

### 5️⃣ Simulación de hipoteca

**POST** /cliente/{dni}/simulacion/
```json
{
  "dni": "12345678Z",
  "tae": 5.0,
  "plazo": 20
}
```

Respuesta:
```json
{
  "cuota_mensual": 659.96,
  "importe_total": 158390.4
}
```

## 🛠️ Documentación detallada con Swagger

Después de iniciar el servidor, accede a la documentación interactiva en:

📜 Swagger UI: http://127.0.0.1:8000/docs

📄 Redoc: http://127.0.0.1:8000/redoc

**📌 Notas adicionales**

<u>Base de datos</u>: Usa SQLite (database.db).

<u>Framework</u>: FastAPI.

<u>Servidor ASGI</u>: Uvicorn.

**📜 Licencia**

Este proyecto está bajo la licencia MIT.

**✉️ Autor**: Pablo Gallardo - [pablogallar02@gmail.com]

