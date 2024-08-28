# Starlette-FastAPI Project

Este proyecto es una API RESTful simple construida con FastAPI que permite crear, leer, actualizar y eliminar (CRUD) elementos en una base de datos MongoDB. La API utiliza `motor`, un cliente asíncrono para MongoDB, para manejar la conexión a la base de datos.

## Estructura del Proyecto

- `main.py`: Contiene las rutas y la lógica principal de la API.
- `database.py`: Configura la conexión a la base de datos MongoDB utilizando `motor`.
- `models.py`: Define los modelos de datos utilizados para crear y validar los datos de los elementos.
- `schemas.py`: Define los esquemas Pydantic utilizados para la serialización y deserialización de los datos.
- `.venv/`: Entorno virtual para el proyecto (ignorando en el repositorio).
- `__pycache__/`: Archivos de caché de Python (ignorando en el repositorio).

## Endpoints

La API tiene los siguientes endpoints:

- **POST /items/**: Crea un nuevo elemento en la base de datos.
- **GET /items/**: Devuelve una lista de todos los elementos en la base de datos.
- **GET /items/{id}**: Devuelve un solo elemento basado en su ID.
- **PUT /items/{id}**: Actualiza un elemento existente basado en su ID.
- **DELETE /items/{id}**: Elimina un elemento basado en su ID.

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/DiegoLerma/starlette-fastapi.git
    cd starlette-fastapi
    ```

2. **Crea y activa un entorno virtual:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # En Windows, usa `.venv\Scripts\activate`
    ```

3. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configura MongoDB:**

   Asegúrate de que MongoDB esté instalado y en ejecución. La API se conecta a una instancia de MongoDB en `mongodb://127.0.0.1:27017` por defecto, y utiliza una base de datos llamada `starlet_db` con una colección `items`.

5. **Ejecuta la aplicación:**

    ```bash
    uvicorn main:app --reload
    ```

   La aplicación estará disponible en `http://127.0.0.1:8000`.

## Uso

Puedes interactuar con la API utilizando herramientas como [Postman](https://www.postman.com/) o `curl`, o visitando la documentación automática generada por FastAPI disponible en `http://127.0.0.1:8000/docs` o `http://127.0.0.1:8000/redoc`.

### Ejemplo de uso con `curl`

- **Crear un elemento:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/items/" -H "Content-Type: application/json" -d '{"name": "Item1", "description": "A new item", "price": 9.99}'
    ```

- **Listar todos los elementos:**

    ```bash
    curl -X GET "http://127.0.0.1:8000/items/"
    ```

- **Obtener un elemento por ID:**

    ```bash
    curl -X GET "http://127.0.0.1:8000/items/{id}"
    ```

- **Actualizar un elemento:**

    ```bash
    curl -X PUT "http://127.0.0.1:8000/items/{id}" -H "Content-Type: application/json" -d '{"name": "Updated Item", "price": 19.99}'
    ```

- **Eliminar un elemento:**

    ```bash
    curl -X DELETE "http://127.0.0.1:8000/items/{id}"
    ```

## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios.
4. Haz un commit de tus cambios (`git commit -am 'Añadir nueva característica'`).
5. Sube la rama (`git push origin feature/nueva-caracteristica`).
6. Crea un nuevo Pull Request.
