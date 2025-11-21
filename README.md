# 🤖 Asistente Virtual con IA

Asistente virtual inteligente desarrollado en Python con Flask que utiliza Google Gemini AI y síntesis de voz natural.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características

- 🧠 **IA Conversacional Avanzada**: Integración con Google Gemini AI (gratis)
- 🎨 **Interfaz Web Moderna**: Diseño responsive con animaciones fluidas
- 🗣️ **Voz Natural Humana**: Google Text-to-Speech (gTTS) con velocidad ajustable
- ⚡ **Respuestas Rápidas**: Procesamiento asíncrono sin bloqueos
- 🎵 **Audio Optimizado**: Reproducción con pygame y control de velocidad

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/python_av.git
cd python_av
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar API Keys

```bash
# Copia el archivo de ejemplo
copy config_ia.example.py config_ia.py

# Edita config_ia.py y agrega tus API keys
```

**Para obtener tu API key GRATIS:**
- **Google Gemini**: https://makersuite.google.com/app/apikey

### 5. Ejecutar la Aplicación

```bash
python app.py
```

Abre tu navegador en: `http://localhost:5000`

## 🎯 Configuración

Edita `config_ia.py` con tu API key de Gemini:

```python
IA_PROVIDER = 'gemini'
GEMINI_API_KEY = 'tu_api_key_aqui'

# Configuración de voz
MOTOR_VOZ = 'gtts'  # Voz natural de Google
GTTS_SPEED = 1.25   # Velocidad: 1.0=normal, 1.25=25% más rápido
```

## 🗣️ Ajustar Velocidad de Voz

Si la voz es muy lenta o rápida, edita `GTTS_SPEED` en `config_ia.py`:

```python
GTTS_SPEED = 1.0   # Normal
GTTS_SPEED = 1.25  # 25% más rápido
GTTS_SPEED = 1.5   # 50% más rápido
GTTS_SPEED = 2.0   # Doble velocidad
```

## 💬 Ejemplos de Uso

Con IA activada, puedes hacer preguntas naturales:

- "¿Qué es la inteligencia artificial?"
- "Explícame cómo funciona Python"
- "Dame consejos para aprender programación"
- "¿Cuál es la capital de Francia?"
- "Cuéntame un chiste"

## 📦 Dependencias Principales

- Flask 3.0.0 - Framework web
- google-generativeai - Google Gemini AI
- gTTS - Síntesis de voz natural
- pygame - Reproducción de audio
- wikipedia - Búsquedas en Wikipedia

## 🌐 Deployment en Producción

### Render (GRATIS)

1. Crea cuenta en [Render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Configura las variables de entorno:
   - `GEMINI_API_KEY`: tu API key
   - `PYTHON_VERSION`: 3.11.0
4. Deploy automático en cada push

### Railway (GRATIS)

1. Crea cuenta en [Railway.app](https://railway.app)
2. Nuevo proyecto desde GitHub
3. Agrega variables de entorno
4. Deploy automático

### PythonAnywhere

1. Sube tu código
2. Crea una Web App con Flask
3. Configura el WSGI file
4. Reinicia la app

## 📁 Estructura del Proyecto

```
python_av/
├── app.py                    # Aplicación Flask principal
├── config_ia.py              # Configuración (NO subir a GitHub)
├── config_ia.example.py      # Plantilla de configuración
├── requirements.txt          # Dependencias
├── .gitignore               # Archivos ignorados
├── README.md                # Esta documentación
├── templates/
│   └── index.html           # Interfaz web
└── static/
    ├── style.css            # Estilos
    └── script.js            # JavaScript
```

## 🔒 Seguridad

**⚠️ IMPORTANTE**: Nunca subas `config_ia.py` con tus API keys a GitHub.

El archivo `.gitignore` ya está configurado para proteger:
- `config_ia.py` (contiene tus keys)
- Archivos temporales de audio
- Cache de Python

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📝 Licencia

Proyecto educativo bajo Licencia MIT.

## 👨‍💻 Autor

Proyecto universitario - Asistente Virtual con IA

## 🐛 Problemas Comunes

### La voz no funciona
- Verifica que pygame esté instalado: `pip install pygame`
- Asegúrate de tener altavoces conectados

### Error de API key
- Confirma que `config_ia.py` existe (copia desde `config_ia.example.py`)
- Verifica que tu API key sea válida

### Error al instalar pygame en Windows
```bash
pip install --upgrade pip
pip install pygame --pre
```

## 📧 Soporte

Si encuentras problemas, abre un [Issue en GitHub](https://github.com/TU_USUARIO/python_av/issues).
