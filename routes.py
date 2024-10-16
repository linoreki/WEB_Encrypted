from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Message
from utils import generate_key_pair

main = Blueprint('main', __name__)

# Ruta para la página de inicio
@main.route('/')
def index():
    return render_template('base.html')

# Ruta de registro de usuarios
from werkzeug.security import generate_password_hash

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Obtener la contraseña
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El usuario ya existe. Intenta con otro nombre de usuario.')
            return redirect(url_for('main.register'))

        try:
            # Generar par de claves asimétricas
            print("Generando claves asimétricas...")
            public_key, private_key = generate_key_pair()
            print(f"Claves generadas - Public Key: {public_key}")

            # Hashear la contraseña
            print("Hasheando la contraseña...")
            hashed_password = generate_password_hash(password)

            # Crear el nuevo usuario
            print("Creando nuevo usuario...")
            new_user = User(
                username=username, 
                public_key=public_key, 
                private_key=private_key,
                password_hash=hashed_password
            )

            # Agregar el usuario a la base de datos
            db.session.add(new_user)
            db.session.commit()

            flash('Registro exitoso. Tu clave pública es: {}'.format(public_key))
            return render_template('registration_success.html', public_key=public_key)
        
        except Exception as e:
            print(f"Error durante el registro: {e}")
            db.session.rollback()  # Revertir cambios si algo falla
            flash('Error al registrar. Por favor, intenta nuevamente.')
            return redirect(url_for('main.register'))

    return render_template('register.html')

# Ruta de inicio de sesión
from werkzeug.security import check_password_hash

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.chat'))
        else:
            flash('Usuario o contraseña incorrectos.')
            return redirect(url_for('main.login'))

    return render_template('login.html')

# Ruta para cerrar sesión
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Ruta para crear una sala
@main.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        public_key = request.form['public_key']
        flash(f'Sala "{room_name}" creada con la clave pública: {public_key}.')
        return redirect(url_for('main.chat', room=room_name))

    return render_template('create_room.html')

# Ruta para unirse a una sala
@main.route('/join_room', methods=['GET', 'POST'])
@login_required
def join_room_view():
    if request.method == 'POST':
        room_name = request.form['room_name']
        public_key = request.form['public_key']
        return redirect(url_for('main.chat', room=room_name))

    return render_template('join_room.html')

# Ruta para la página de chat
@main.route('/chat')
@login_required
def chat():
    room = request.args.get('room')
    messages = Message.query.filter_by(room=room).order_by(Message.timestamp).all()
    return render_template('chat.html', messages=messages, room=room)

# Ruta para gestionar claves
@main.route('/keys')
@login_required
def keys():
    return render_template('keys.html', public_key=current_user.public_key)

# Ruta para regenerar clave pública/privada
@main.route('/regenerate_key', methods=['POST'])
@login_required
def regenerate_key():
    public_key, private_key = generate_key_pair()
    
    current_user.public_key = public_key
    current_user.private_key = private_key
    db.session.commit()

    flash('Tus claves han sido regeneradas.')
    return redirect(url_for('main.keys'))

# Ruta para agregar un contacto
@main.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        public_key = request.form['public_key']
        
        if current_user.contacts:
            current_user.contacts += f",{public_key}"
        else:
            current_user.contacts = public_key
        db.session.commit()

        flash('Contacto agregado correctamente.')
        return redirect(url_for('main.chat'))

    return render_template('add_contact.html')
