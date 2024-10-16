// Obtén el ID de usuario de alguna manera
const userId = /* ID del usuario autenticado, puedes obtenerlo de un elemento oculto o desde una variable global */;

// Conectar a Socket.IO
const socket = io.connect('http://localhost:5000', {
    auth: {
        user_id: userId // Envía el ID del usuario al conectarse
    }
});

// Elementos del DOM
const messageInput = document.getElementById('message-input');
const messageButton = document.getElementById('send-message');
const messagesContainer = document.getElementById('messages');
const roomInput = document.getElementById('room-input');
const joinRoomButton = document.getElementById('join-room');
const leaveRoomButton = document.getElementById('leave-room');
const roomDisplay = document.getElementById('room-display');
let currentRoom = null;

// Función para enviar un mensaje
messageButton.addEventListener('click', () => {
    const message = messageInput.value;
    if (currentRoom && message) {
        socket.emit('send_message', { room: currentRoom, message: message });
        messageInput.value = ''; // Limpiar el campo de entrada
    }
});

// Función para unirse a una sala
joinRoomButton.addEventListener('click', () => {
    const room = roomInput.value;
    if (room) {
        currentRoom = room; // Establecer la sala actual
        socket.emit('join', { room: room });
        roomDisplay.innerText = `Sala: ${room}`; // Mostrar la sala actual
        roomInput.value = ''; // Limpiar el campo de entrada
    }
});

// Función para abandonar la sala
leaveRoomButton.addEventListener('click', () => {
    if (currentRoom) {
        socket.emit('leave', { room: currentRoom });
        currentRoom = null; // Limpiar la sala actual
        roomDisplay.innerText = ''; // Limpiar la visualización de la sala
    }
});

// Escuchar los mensajes recibidos
socket.on('receive_message', (data) => {
    const messageElement = document.createElement('div');
    messageElement.innerText = `${data.username}: ${data.message}`;
    messagesContainer.appendChild(messageElement);
});

// Escuchar cuando se une una sala
socket.on('join', (data) => {
    const joinMessage = document.createElement('div');
    joinMessage.innerText = data.message;
    messagesContainer.appendChild(joinMessage);
});

// Escuchar cuando alguien sale de la sala
socket.on('leave', (data) => {
    const leaveMessage = document.createElement('div');
    leaveMessage.innerText = data.message;
    messagesContainer.appendChild(leaveMessage);
});

// Opcional: Scroll automático hacia abajo en el contenedor de mensajes
const scrollToBottom = () => {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

// Agregar el evento de scroll automático al recibir un mensaje
socket.on('receive_message', (data) => {
    scrollToBottom();
});
