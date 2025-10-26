let vozActivada = false;
let modoIA = 'local'; // Se actualizará al cargar

// Función para detectar el modo de IA
async function detectarModoIA() {
    try {
        const response = await fetch('/config_status');
        const data = await response.json();
        modoIA = data.modo;
        
        const statusDiv = document.getElementById('ia-status');
        if (data.modo === 'local') {
            statusDiv.innerHTML = '<span class="status-local">🔧 Modo Local</span>';
        } else {
            const emoji = data.modo === 'openai' ? '🚀' : '✨';
            statusDiv.innerHTML = `<span class="status-ia">${emoji} IA Activada (${data.modo.toUpperCase()})</span>`;
        }
    } catch (error) {
        console.error('Error al detectar modo IA:', error);
    }
}

// Función para obtener la hora actual
function obtenerHora() {
    const ahora = new Date();
    return ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

// Función para agregar mensaje al chat
function agregarMensaje(texto, esUsuario = false) {
    const chatMessages = document.getElementById('chat-messages');
    const mensaje = document.createElement('div');
    mensaje.className = `message ${esUsuario ? 'user-message' : 'bot-message'}`;
    
    const contenido = document.createElement('div');
    contenido.className = 'message-content';
    contenido.innerHTML = `<strong>${esUsuario ? 'Tú' : 'Asistente'}:</strong> ${texto}`;
    
    const hora = document.createElement('div');
    hora.className = 'message-time';
    hora.textContent = obtenerHora();
    
    mensaje.appendChild(contenido);
    mensaje.appendChild(hora);
    chatMessages.appendChild(mensaje);
    
    // Scroll automático al último mensaje
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para enviar comando al servidor
async function enviarComando() {
    const input = document.getElementById('user-input');
    const comando = input.value.trim();
    
    if (!comando) {
        return;
    }
    
    // Agregar mensaje del usuario PRIMERO
    agregarMensaje(comando, true);
    
    // Limpiar input INMEDIATAMENTE
    input.value = '';
    
    // Mostrar mensaje de carga
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = 'loading-message';
    loadingDiv.innerHTML = `
        <div class="message-content">
            <strong>Asistente:</strong> <span class="loading">Procesando...</span>
        </div>
    `;
    document.getElementById('chat-messages').appendChild(loadingDiv);
    document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
    
    try {
        // Enviar solicitud al servidor
        const response = await fetch('/procesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                comando: comando,
                hablar: vozActivada
            })
        });
        
        const data = await response.json();
        
        // Eliminar mensaje de carga
        const loading = document.getElementById('loading-message');
        if (loading) {
            loading.remove();
        }
        
        // Agregar respuesta del asistente
        agregarMensaje(data.respuesta, false);
        
    } catch (error) {
        // Eliminar mensaje de carga
        const loading = document.getElementById('loading-message');
        if (loading) {
            loading.remove();
        }
        
        agregarMensaje('Lo siento, hubo un error al procesar tu comando. ¿El servidor está corriendo?', false);
        console.error('Error:', error);
    }
}

// Función para activar/desactivar voz
function toggleVoz() {
    vozActivada = !vozActivada;
    const voiceBtn = document.getElementById('voice-btn');
    
    if (vozActivada) {
        voiceBtn.classList.add('active');
        voiceBtn.textContent = '🔊';
        agregarMensaje('Voz activada. El asistente hablará sus respuestas.', false);
    } else {
        voiceBtn.classList.remove('active');
        voiceBtn.textContent = '🔇';
        agregarMensaje('Voz desactivada.', false);
    }
}

// Función para probar comandos de ejemplo
function probarComando(comando) {
    const input = document.getElementById('user-input');
    input.value = comando;
    input.focus();
}

// Event listener para Enter
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('user-input');
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            enviarComando();
        }
    });
    
    // Enfocar el input al cargar
    input.focus();
    
    // Detectar modo de IA
    detectarModoIA();
});

// Event listener para el botón de enviar
document.addEventListener('DOMContentLoaded', function() {
    const sendBtn = document.getElementById('send-btn');
    sendBtn.addEventListener('click', enviarComando);
});
