# Pan del Alba - Práctica 2 de Docker

Página de panadería hecha con Flask, plantillas Jinja2 y SQLite. Los pedidos se guardan en una base de datos dentro de un volumen de Docker.

## Archivos

| Archivo | Función |
| --- | --- |
| `app.py` | Servidor Flask, productos, formulario y base de datos SQLite. |
| `templates/index.html` | Página HTML con contenido dinámico de Jinja2. |
| `static/style.css` | Diseño de la página. |
| `requirements.txt` | Dependencia de Flask. |
| `Dockerfile` | Instrucciones para construir la imagen. |
| `docker-compose.yml` | Servicio web, puerto y volumen persistente. |

## Ejecutar con Docker

Abre una terminal **en esta carpeta `panaderia`** y asegúrate de que Docker Desktop esté iniciado. Primero construye la imagen y luego crea el contenedor:

```powershell
docker compose build
docker compose up -d
```

Abre <http://localhost:5000>. Para ver registros y estado:

```powershell
docker compose ps
docker compose logs web
```

Para detener el servicio sin borrar los pedidos:

```powershell
docker compose down
```

## Demostrar el volumen

1. Abre la web y registra un pedido.
2. Comprueba que aparece en **Pedidos recientes**.
3. En la terminal, ejecuta `docker compose down`.
4. Vuelve a ejecutar `docker compose up -d`.
5. Recarga <http://localhost:5000>: el pedido debe seguir ahí.

El volumen se llama `pedidos_data` en el archivo Compose. Docker le añade el nombre del proyecto, normalmente `panaderia_pedidos_data`. Se monta en `/app/data`, donde Flask guarda `/app/data/panaderia.db`.

**Importante:** `docker compose down --volumes` sí borra el volumen y los pedidos. No lo uses durante la demostración de persistencia.

## Construir y ejecutar sin Compose

```powershell
docker build -t panaderia:v1 .
docker volume create panaderia_pedidos
docker run -d --name panaderia-web -p 5000:5000 -v panaderia_pedidos:/app/data panaderia:v1
```

Si Compose ya está usando el puerto 5000, detenlo antes con `docker compose down`.

## Documentación y entrega

Lee [DOCUMENTACION.md](DOCUMENTACION.md) para los ocho pasos de creación en Docker, los prompts por apartado, la prueba del volumen y las capturas reales. También incluye un recorrido adicional por terminal inspirado en la práctica 2 del docente: `docker build`, `docker run`, bind mount, red personalizada y Compose, adaptados a Flask. El PDF de entrega se guarda en `output/pdf/`.

Repositorio: <https://github.com/Chucharizard/pan-del-alba-docker>. La base de datos local `.db` está excluida por `.gitignore`; las imágenes de evidencia sí forman parte del repositorio.
