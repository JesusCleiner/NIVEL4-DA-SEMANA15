import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# -----------------------------
# Cargar variables de entorno
# -----------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_flask")
DB_FILE = os.getenv("DB_FILE", "desarrollo_web.db")

# -----------------------------
# Función para conectar a SQLite
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    return conn

# -----------------------------
# Crear tabla productos si no existe
# -----------------------------
def crear_tabla():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

crear_tabla()  # Crear tabla al iniciar

# -----------------------------
# Ruta de Inicio
# -----------------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")

# -----------------------------
# Ruta de Acerca de Nosotros
# -----------------------------
@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

# -----------------------------
# Ruta de Contacto
# -----------------------------
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

# -----------------------------
# Ruta de Movimientos (CRUD Productos)
# -----------------------------
@app.route("/movimiento", methods=["GET", "POST"])
def movimiento():
    conn = get_connection()
    cursor = conn.cursor()

    # Crear producto
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        try:
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre, precio, stock)
            )
            conn.commit()
            flash("Producto agregado correctamente", "success")
        except Exception as e:
            flash(f"Error al agregar producto: {str(e)}", "danger")

    # Leer productos
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("movimiento.html", productos=productos)

# -----------------------------
# Ruta para editar producto
# -----------------------------
@app.route("/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        try:
            cursor.execute(
                "UPDATE productos SET nombre=?, precio=?, stock=? WHERE id_producto=?",
                (nombre, precio, stock, id_producto)
            )
            conn.commit()
            flash("Producto actualizado correctamente", "success")
            cursor.close()
            conn.close()
            return redirect(url_for("movimiento"))
        except Exception as e:
            flash(f"Error al actualizar producto: {str(e)}", "danger")

    # Obtener datos actuales del producto
    cursor.execute("SELECT * FROM productos WHERE id_producto=?", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("editar_producto.html", producto=producto)

# -----------------------------
# Ruta para eliminar producto
# -----------------------------
@app.route("/eliminar/<int:id_producto>")
def eliminar_producto(id_producto):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=?", (id_producto,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Producto eliminado correctamente", "success")
    except Exception as e:
        flash(f"Error al eliminar producto: {str(e)}", "danger")
    return redirect(url_for("movimiento"))

# -----------------------------
# Ejecutar la aplicación
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
