import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Conexión a la base de datos
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Datos del usuario
nombre = "Admin"
email = "admin@marvisoft.com"
password = "Marvisoft"

# Crear hash de la contraseña
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Insertar usuario en la tabla
sql = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
cursor.execute(sql, (nombre, email, hashed.decode('utf-8')))

conn.commit()
cursor.close()
conn.close()

print("✅ Usuario creado exitosamente con contraseña segura")
