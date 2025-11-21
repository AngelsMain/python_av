# ============================================
# CONFIGURACIÓN DE INTELIGENCIA ARTIFICIAL
# ============================================

"""
Este archivo es una PLANTILLA. Para usarlo:
1. Copia este archivo y renómbralo a: config_ia.py
2. Completa tus API keys
3. Elige tu proveedor de IA
"""

# ============= PROVEEDOR DE IA =============
IA_PROVIDER = 'gemini'

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
GTTS_SPEED = 1.25  # 1.0 = normal, 1.25 = 25% más rápido (recomendado)
