from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import get_connection
import bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta_flask"  # Necesaria para mensajes flash

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
# Ruta de Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Conectar a la base de datos
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            # Verificar contraseña hasheada
            if bcrypt.checkpw(password.encode('utf-8'), usuario["password"].encode('utf-8')):
                flash(f"Bienvenido {usuario['nombre']}!", "success")
                return redirect(url_for("inicio"))
            else:
                flash("Contraseña incorrecta", "danger")
        else:
            flash("Usuario no encontrado", "danger")

    return render_template("login.html")

# -----------------------------
# Ruta para probar la conexión con la base de datos
# -----------------------------
@app.route("/test_db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"✅ Conectado a la base de datos: {db_name[0]}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# -----------------------------
# Ejecutar la aplicación
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
