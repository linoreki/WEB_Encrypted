import sqlite3
from werkzeug.security import generate_password_hash

# Crear un archivo de base de datos llamado app.db
db_path = 'app.db'  # Cambia la ruta si es necesario
connection = sqlite3.connect(db_path)

# Crear un cursor
cursor = connection.cursor()

# Crear las tablas necesarias: User, Contact y Message
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    public_key TEXT NOT NULL,
    private_key TEXT NOT NULL,
    password_hash TEXT NOT NULL  -- Agregar este campo para la contraseña hasheada
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    contact_public_key TEXT NOT NULL,
    contact_username TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    room TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender_id INTEGER,
    FOREIGN KEY (sender_id) REFERENCES user (id)
)
''')

# Insertar un usuario de prueba con contraseña
username = 'testuser'
password = 'testpassword'  # Contraseña de prueba
public_key = 'test_public_key'
private_key = 'test_private_key'
password_hash = generate_password_hash(password)  # Generar el hash de la contraseña

cursor.execute('''
INSERT OR IGNORE INTO user (username, public_key, private_key, password_hash) VALUES (?, ?, ?, ?)
''', (username, public_key, private_key, password_hash))

# Insertar un contacto de prueba
cursor.execute('''
INSERT INTO contact (user_id, contact_public_key, contact_username) VALUES
(1, 'contact_public_key', 'contactuser')
''')

# Guardar los cambios y cerrar la conexión
connection.commit()
connection.close()

print("Base de datos creada con éxito.")
