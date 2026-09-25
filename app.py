import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


PRODUCTOS = [
    {"id": "marraqueta", "nombre": "Marraqueta", "precio": 2, "icono": "🥖", "descripcion": "Crujiente por fuera, suave por dentro."},
    {"id": "croissant", "nombre": "Croissant", "precio": 8, "icono": "🥐", "descripcion": "Hojaldre dorado para acompañar tu café."},
    {"id": "pan_chocolate", "nombre": "Pan de chocolate", "precio": 10, "icono": "🍫", "descripcion": "Una pausa dulce recién salida del horno."},
    {"id": "galletas", "nombre": "Galletas caseras", "precio": 6, "icono": "🍪", "descripcion": "Hechas en casa, perfectas para compartir."},
]
PRODUCTOS_POR_ID = {producto["id"]: producto for producto in PRODUCTOS}


@contextmanager
def conectar(ruta):
    conexion = sqlite3.connect(ruta)
    try:
        yield conexion
        conexion.commit()
    finally:
        conexion.close()


def create_app(database_path=None):
    app = Flask(__name__)
    ruta_bd = Path(database_path or os.environ.get("DATABASE_PATH", "data/panaderia.db"))
    ruta_bd.parent.mkdir(parents=True, exist_ok=True)
    app.config["DATABASE_PATH"] = str(ruta_bd)

    with conectar(ruta_bd) as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                total INTEGER NOT NULL,
                fecha TEXT NOT NULL
            )
            """
        )

    @app.get("/")
    def inicio():
        with conectar(app.config["DATABASE_PATH"]) as conexion:
            conexion.row_factory = sqlite3.Row
            pedidos = conexion.execute(
                "SELECT cliente, producto, cantidad, total, fecha "
                "FROM pedidos ORDER BY id DESC LIMIT 10"
            ).fetchall()
        return render_template(
            "index.html",
            productos=PRODUCTOS,
            pedidos=pedidos,
            exito=request.args.get("ok") == "1",
            error=None,
            valores={},
        )

    @app.post("/pedidos")
    def guardar_pedido():
        cliente = request.form.get("cliente", "").strip()
        producto_id = request.form.get("producto", "")
        cantidad_texto = request.form.get("cantidad", "")
        producto = PRODUCTOS_POR_ID.get(producto_id)

        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            cantidad = 0

        error = None
        if not cliente or len(cliente) > 80:
            error = "Escribe tu nombre (máximo 80 caracteres)."
        elif producto is None:
            error = "Selecciona un producto válido."
        elif not 1 <= cantidad <= 50:
            error = "La cantidad debe estar entre 1 y 50."

        if error:
            with conectar(app.config["DATABASE_PATH"]) as conexion:
                conexion.row_factory = sqlite3.Row
                pedidos = conexion.execute(
                    "SELECT cliente, producto, cantidad, total, fecha "
                    "FROM pedidos ORDER BY id DESC LIMIT 10"
                ).fetchall()
            return render_template(
                "index.html",
                productos=PRODUCTOS,
                pedidos=pedidos,
                exito=False,
                error=error,
                valores=request.form,
            ), 400

        with conectar(app.config["DATABASE_PATH"]) as conexion:
            conexion.execute(
                "INSERT INTO pedidos (cliente, producto, cantidad, total, fecha) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    cliente,
                    producto["nombre"],
                    cantidad,
                    producto["precio"] * cantidad,
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                ),
            )
        return redirect(url_for("inicio", ok=1) + "#pedidos")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
