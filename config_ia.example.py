# ============================================
# CONFIGURACIÓN DE INTELIGENCIA ARTIFICIAL
# ============================================

"""
Este archivo es una PLANTILLA. Para usarlo:
1. Copia este archivo y renómbralo a: config_ia.py
2. Completa tus API keys
3. Elige tu proveedor de IA
"""

# ============= ELIGE TU PROVEEDOR =============
# Opciones: 'local', 'openai', 'gemini'
IA_PROVIDER = 'gemini'

# ============= OPENAI (ChatGPT) =============
# 🔗 Obtén tu API key en: https://platform.openai.com/api-keys
OPENAI_API_KEY = 'TU_OPENAI_API_KEY_AQUI'
OPENAI_MODEL = 'gpt-3.5-turbo'  # O 'gpt-4' si tienes acceso

# ============= GOOGLE GEMINI =============
# 🔗 Obtén tu API key GRATIS en: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = 'TU_GEMINI_API_KEY_AQUI'
GEMINI_MODEL = 'gemini-2.0-flash'

# ============= CONFIGURACIÓN DE VOZ =============
MOTOR_VOZ = 'gtts'  # 'gtts' (Google - Natural) o 'pyttsx3' (Local - Robótico)

# Configuración para pyttsx3
VELOCIDAD_VOZ = 160
VOLUMEN_VOZ = 0.95

# Configuración para gTTS
GTTS_LANG = 'es'
GTTS_SLOW = False
GTTS_SPEED = 2.0  # 1.0 = normal, 1.5 = 50% más rápido, 2.0 = doble velocidad
