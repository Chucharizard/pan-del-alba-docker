# Práctica 2: Pan del Alba

## Objetivo

Crear una página web básica para una panadería con Flask y Jinja2. Registrar pedidos en SQLite y conservar la base de datos mediante un volumen de Docker. Construir la imagen con un Dockerfile y ejecutar el servicio con Docker Compose.

## Herramientas

- **Flask:** microframework de Python que atiende las solicitudes HTTP y procesa el formulario.
- **Jinja2:** motor de plantillas utilizado por Flask para mostrar productos y pedidos en HTML.
- **SQLite:** base de datos en un archivo `panaderia.db`.
- **Dockerfile:** receta para construir la imagen con Python y Flask.
- **Docker Compose:** configura el servicio, el puerto 5000 y el volumen de datos.

## Procedimiento: creación de la imagen y del contenedor

Todos los comandos se ejecutan en una terminal abierta **dentro de la carpeta `panaderia`**, donde están `Dockerfile` y `docker-compose.yml`. Docker Desktop debe estar iniciado.

### Paso 1. Preparar los archivos de la aplicación

Se crearon `app.py`, `requirements.txt`, `templates/index.html` y `static/style.css`. `app.py` inicia Flask en el puerto 5000 y usa la variable `DATABASE_PATH` para ubicar el archivo SQLite. `requirements.txt` indica que hay que instalar Flask. Las carpetas `templates` y `static` contienen la página Jinja2 y el CSS.

**Comprobación:** en esta carpeta deben verse esos archivos antes de construir la imagen.

### Paso 2. Escribir el Dockerfile

El archivo [Dockerfile](Dockerfile) contiene estas instrucciones:

| Instrucción | Función |
| --- | --- |
| `FROM python:3.12-slim` | Usa Python como base de la imagen. |
| `WORKDIR /app` | Establece la carpeta de trabajo dentro de la imagen. |
| `COPY requirements.txt .` y `RUN pip install ...` | Copia e instala Flask. |
| `COPY app.py .`, `COPY templates/ ...`, `COPY static/ ...` | Añade el código y el diseño de la web. |
| `ENV DATABASE_PATH=/app/data/panaderia.db` | Indica dónde guardar la base de datos. |
| `EXPOSE 5000` | Documenta el puerto usado por Flask. |
| `CMD ["python", "app.py"]` | Arranca la aplicación al iniciar el contenedor. |

`EXPOSE` solo documenta el puerto interno. La publicación hacia la computadora se hace en Compose.

### Paso 3. Escribir Docker Compose y definir el volumen

El archivo [docker-compose.yml](docker-compose.yml) define el servicio `web`. `build: .` señala el Dockerfile de esta carpeta; `ports: "5000:5000"` conecta el puerto de la computadora con el del contenedor; `DATABASE_PATH` apunta a `/app/data/panaderia.db`; y `pedidos_data:/app/data` monta el volumen donde queda SQLite.

Se puede revisar la configuración sin crear nada:

```powershell
docker compose config
```

**Resultado esperado:** aparecen el servicio `web`, el puerto 5000 y el volumen `pedidos_data` montado en `/app/data`.

### Paso 4. Construir la imagen

```powershell
docker compose build
docker image ls panaderia-web
```

`docker compose build` lee el Dockerfile, descarga la base Python si hace falta, instala Flask y crea la imagen local `panaderia-web`. El segundo comando permite comprobar que la imagen existe. **En este paso todavía no se crea el contenedor.**

### Paso 5. Crear e iniciar el contenedor

```powershell
docker compose up -d
docker compose ps
docker compose logs web
```

`up -d` crea e inicia el contenedor `panaderia-web-1`, además de la red y el volumen si aún no existen. `ps` debe mostrar el estado `running` y el puerto `5000:5000`. En `logs web` debe aparecer que Flask atiende en el puerto 5000.

### Paso 6. Probar la página y guardar un pedido

Abre <http://localhost:5000>. Comprueba el catálogo, llena el formulario y envía un pedido. Debe aparecer en **Pedidos recientes**. En la prueba realizada se guardaron tres marraquetas para `Pedido de prueba`, con total **Bs 6**.

### Paso 7. Demostrar que los datos sobreviven al contenedor

```powershell
docker compose down
docker compose up -d
docker compose ps
```

`down` elimina el contenedor y la red, pero conserva el volumen. `up -d` crea otro contenedor y monta el mismo volumen. Al recargar <http://localhost:5000>, el pedido debe seguir en **Pedidos recientes**. En nuestra ejecución el ID del contenedor cambió de `4481c631a587` a `53ee6d7e382a` y el pedido permaneció.

### Paso 8. Verificar el volumen

```powershell
docker volume ls
docker volume inspect panaderia_pedidos_data
```

Compose creó el volumen con el nombre completo `panaderia_pedidos_data`. Ahí se conserva el archivo SQLite que Flask usa en `/app/data/panaderia.db`. Para detener el proyecto conservando los datos, usa `docker compose down`. **No uses `docker compose down --volumes` durante esta demostración**, porque ese comando sí elimina el volumen.

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

## Capturas realizadas

1. [Página de la panadería con el pedido persistente](evidencias/web-despues.png).
2. [Contenedor recreado y en ejecución en Docker Desktop](evidencias/docker-contenedor-despues.png).
3. [Volumen `panaderia_pedidos_data` en Docker Desktop](evidencias/docker-volumen.png).
4. [Vista inicial de la página](evidencias/web-pedidos-antes.png).

Para comprobar la persistencia se creó el pedido de prueba `Marraqueta · 3 unidades`, se ejecutó `docker compose down` y después `docker compose up -d`. El ID del contenedor cambió de `4481c631a587` a `53ee6d7e382a`; al recargar la página el pedido seguía visible. El volumen permaneció como `panaderia_pedidos_data`.

## GitHub

Repositorio público: <https://github.com/Chucharizard/pan-del-alba-docker>.

El historial se construyó por etapas:

1. `feat: crear web de panaderia con Flask y SQLite`
2. `build: contenerizar la app y persistir pedidos en volumen`
3. `docs: explicar arquitectura, prompts y prueba de volumen`
4. `docs: añadir evidencias reales y PDF de entrega`
5. `docs: documentar creacion de imagen y contenedor paso a paso`

## Conclusión

La práctica muestra la diferencia entre la imagen, el contenedor y el volumen: la imagen contiene la aplicación; el contenedor la ejecuta; el volumen conserva la base de datos cuando el contenedor se recrea.
