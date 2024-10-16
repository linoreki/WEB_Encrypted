from flask import Flask, session, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from models import db, User, Contact, Message  # Asegúrate de que todos los modelos estén importados
from routes import main as main_blueprint

# Inicializar las extensiones
socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Registrar el blueprint de las rutas
    app.register_blueprint(main_blueprint)

    # Crear la base de datos si no existe
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Manejar conexiones de Socket.IO
@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        print(f'Usuario {current_user.username} conectado')

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        print(f'Usuario {current_user.username} desconectado')

@socketio.on('send_message')
@login_required
def handle_send_message(data):
    room = data['room']
    message_content = data['message']

    # Guardar el mensaje en la base de datos
    new_message = Message(content=message_content, room=room, sender_id=current_user.id)
    db.session.add(new_message)
    db.session.commit()

    # Emitir el mensaje a la sala
    emit('receive_message', {'message': message_content, 'username': current_user.username}, room=room)

@socketio.on('join')
@login_required
def handle_join(data):
    username = current_user.username
    room = data['room']
    join_room(room)
    emit('receive_message', {'message': f'{username} ha entrado en la conversación.'}, room=room)

@socketio.on('leave')
@login_required
def handle_leave(data):
    username = current_user.username
    room = data['room']
    leave_room(room)
    emit('receive_message', {'message': f'{username} ha salido de la conversación.'}, room=room)

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)
