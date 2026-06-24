import os
import time
import psycopg2
from contextlib import contextmanager
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "postgres"),
    "dbname": os.environ.get("DB_NAME", "inventario"),
    "user": os.environ.get("DB_USER", "appuser"),
    "password": os.environ.get("DB_PASSWORD", ""),
}

@contextmanager
def db_cursor():
    """Abre conexión + cursor, hace commit/rollback y CIERRA siempre la conexión."""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    for _ in range(30):
        try:
            with db_cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS productos (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        cantidad INTEGER NOT NULL DEFAULT 0,
                        precio NUMERIC(10,2) NOT NULL DEFAULT 0
                    )
                """)
            print("Base de datos lista.", flush=True)
            return
        except Exception as e:
            print(f"Esperando a la base de datos... ({e})", flush=True)
            time.sleep(2)
    raise RuntimeError("No se pudo conectar a la base de datos")

@app.route("/api/health")
def health():
    try:
        with db_cursor() as cur:
            cur.execute("SELECT 1")
        return jsonify(status="ok")
    except Exception:
        return jsonify(status="db-no-disponible"), 503

@app.route("/api/productos", methods=["GET"])
def listar():
    with db_cursor() as cur:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos ORDER BY id")
        productos = [
            {"id": r[0], "nombre": r[1], "cantidad": r[2], "precio": float(r[3])}
            for r in cur.fetchall()
        ]
    return jsonify(productos)

@app.route("/api/productos", methods=["POST"])
def crear():
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get("nombre") or "").strip()
    if not nombre or len(nombre) > 100:
        return jsonify(error="El nombre es obligatorio (máx. 100 caracteres)"), 400
    try:
        cantidad = int(datos.get("cantidad", 0))
        precio = float(datos.get("precio", 0))
    except (TypeError, ValueError):
        return jsonify(error="Cantidad y precio deben ser numéricos"), 400
    if cantidad < 0 or precio < 0:
        return jsonify(error="Cantidad y precio no pueden ser negativos"), 400
    with db_cursor() as cur:
        cur.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s) RETURNING id",
            (nombre, cantidad, precio),
        )
        nuevo_id = cur.fetchone()[0]
    return jsonify(id=nuevo_id, nombre=nombre, cantidad=cantidad, precio=precio), 201

@app.route("/api/productos/<int:producto_id>", methods=["DELETE"])
def borrar(producto_id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        borrado = cur.rowcount
    if borrado == 0:
        return jsonify(error="Producto no encontrado"), 404
    return jsonify(status="borrado"), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)