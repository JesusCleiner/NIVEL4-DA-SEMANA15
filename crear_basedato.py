import sqlite3

# Nombre del archivo de la base de datos
db_file = "desarrollo_web.db"

# Conectar y crear la base de datos
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Crear tabla productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
);
""")

conn.commit()
conn.close()

print(f"✅ Base de datos '{db_file}' creada con la tabla 'productos'.")
