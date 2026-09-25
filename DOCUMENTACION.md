# Práctica 2: Pan del Alba

## Objetivo

Crear una página web básica para una panadería con Flask y Jinja2. Registrar pedidos en SQLite y conservar la base de datos mediante un volumen de Docker. Construir la imagen con un Dockerfile y ejecutar el servicio con Docker Compose.

## Herramientas

- **Flask:** microframework de Python que atiende las solicitudes HTTP y procesa el formulario.
- **Jinja2:** motor de plantillas utilizado por Flask para mostrar productos y pedidos en HTML.
- **SQLite:** base de datos en un archivo `panaderia.db`.
- **Dockerfile:** receta para construir la imagen con Python y Flask.
- **Docker Compose:** configura el servicio, el puerto 5000 y el volumen de datos.

## Prompts por apartado

Estos prompts se redactaron para guiar la construcción de esta práctica. Puedes incluirlos en el documento como prompts de trabajo; si el profesor solicita pruebas de la conversación con IA, añade capturas de los prompts que realmente envíes.

### 1. Idea y estructura

> Quiero hacer una práctica de Docker con una página web sencilla para una panadería. Propón una estructura de proyecto con Flask, plantillas Jinja2, CSS, SQLite, Dockerfile y Docker Compose. La web debe mostrar productos y permitir guardar pedidos.

**Resultado esperado:** estructura de carpetas y responsabilidad de cada archivo.

### 2. Diseño visual con Jinja2

> Diseña una página para una panadería llamada Pan del Alba usando HTML, CSS y plantillas Jinja2. Debe mostrar productos con precios, un formulario para registrar pedidos y una lista de pedidos guardados. Haz que se adapte a celular.

**Resultado esperado:** `templates/index.html` y `static/style.css`.

### 3. Flask y SQLite

> Crea una aplicación Flask que muestre productos, reciba un formulario de pedido y guarde nombre del cliente, producto, cantidad, total y fecha en SQLite. Valida los datos del formulario y muestra los últimos pedidos en la página.

**Resultado esperado:** `app.py`, tabla `pedidos` y formulario funcional.

### 4. Dockerfile

> Escribe un Dockerfile para una aplicación Flask de Python. Debe instalar las dependencias de requirements.txt, copiar la aplicación, exponer el puerto 5000 y arrancar el servidor. La base SQLite estará en /app/data/panaderia.db.

**Resultado esperado:** imagen construida con `docker compose up --build` o `docker build`.

### 5. Docker Compose y volumen

> Escribe un docker-compose.yml para la web Flask. Publica el puerto 5000 y monta un volumen con nombre en /app/data, de modo que panaderia.db permanezca aunque se elimine y recree el contenedor.

**Resultado esperado:** servicio `web` y volumen `pedidos_data`.

### 6. Comprobación

> Explica cómo probar la página, registrar un pedido y demostrar que sigue guardado después de ejecutar docker compose down y docker compose up -d. Incluye los comandos para ver los contenedores, registros y volúmenes.

**Resultado esperado:** evidencia de que la aplicación responde y SQLite conserva los datos.

## Cómo funciona

1. El navegador abre `http://localhost:5000`.
2. Flask muestra `templates/index.html` y le entrega la lista de productos y los pedidos obtenidos de SQLite.
3. Al enviar el formulario, Flask valida los datos e inserta el pedido en `panaderia.db`.
4. Compose monta el volumen `pedidos_data` en `/app/data`. El archivo de la base queda en ese volumen.
5. Al recrear el contenedor, Flask vuelve a leer el mismo archivo SQLite del volumen.

## Comandos para la demostración

Abre Docker Desktop. En una terminal situada en la carpeta `panaderia`, ejecuta:

```powershell
docker compose up --build -d
docker compose ps
docker compose logs web
docker volume ls
```

Registra un pedido en `http://localhost:5000` y anota lo que aparece en la sección **Pedidos recientes**. Luego ejecuta:

```powershell
docker compose down
docker compose up -d
```

Recarga la página y verifica que el pedido siga presente. No uses `docker compose down --volumes`, porque ese comando borra los datos.

## Capturas que debes añadir al PDF final

1. Página principal con catálogo de productos.
2. Formulario y pedido visible en **Pedidos recientes**.
3. Terminal con `docker compose ps` y el servicio en ejecución.
4. Pedido visible después de recrear el contenedor.
5. Si el profesor lo pide, vista de **Volumes** en Docker Desktop o salida de `docker volume ls`.

Las capturas deben hacerse durante tu ejecución real; no se incluyen imágenes inventadas en esta documentación.

## GitHub

Crea un repositorio vacío en GitHub y copia su URL. Desde la carpeta `panaderia`:

```powershell
git init
git add .
git commit -m "Práctica 2: panadería Flask con Docker y SQLite"
git branch -M main
git remote add origin URL_DE_TU_REPOSITORIO
git push -u origin main
```

Sustituye `URL_DE_TU_REPOSITORIO` por la URL real. Si Git pide tu nombre o correo, configúralos con tus datos.

## Conclusión

La práctica muestra la diferencia entre la imagen, el contenedor y el volumen: la imagen contiene la aplicación; el contenedor la ejecuta; el volumen conserva la base de datos cuando el contenedor se recrea.
