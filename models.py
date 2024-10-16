from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime  # Asegúrate de que esto esté presente

db = SQLAlchemy()
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     public_key = db.Column(db.Text, nullable=False)
#     private_key = db.Column(db.Text, nullable=False)
#     contacts = db.Column(db.Text)  # Campo opcional para contactos

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    private_key = db.Column(db.Text, nullable=False)
    contacts = db.relationship('Contact', backref='user', lazy=True)
    messages = db.relationship('Message', backref='sender', lazy=True)  # Relación para mensajes
    password_hash = db.Column(db.String(128), nullable=False)  # Asegúrate de que esto esté aquí

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_public_key = db.Column(db.Text, nullable=False)
    contact_username = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    room = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Usar sender_id para la relación

    # Esta línea se debe eliminar para evitar el conflicto:
    # user = db.relationship('User', backref='messages')  
