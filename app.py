from flask import Flask, render_template, request, jsonify, send_file
import datetime
import wikipedia
import pyttsx3
import threading
import webbrowser
import os
import requests
import json
import random
from collections import Counter
import string
import re
import tempfile
import time
import subprocess
import sys
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)

# ============= CONFIGURACIÓN DE IA =============
# Intentar cargar desde config_ia.py (desarrollo local)
# O desde variables de entorno (producción)
try:
    from config_ia import (
        IA_PROVIDER, GEMINI_API_KEY, 
        GEMINI_MODEL, VELOCIDAD_VOZ, VOLUMEN_VOZ,
        MOTOR_VOZ, GTTS_LANG, GTTS_SLOW, GTTS_SPEED
    )
    print("\n" + "🔧"*30)
    print("✅ Configuración cargada desde config_ia.py")
    print(f"   🤖 Proveedor IA: {IA_PROVIDER}")
    print(f"   🎤 Motor de voz: {MOTOR_VOZ}")
    print(f"   🌍 Idioma gTTS: {GTTS_LANG}")
    print(f"   ⚡ Velocidad gTTS: {GTTS_SPEED}x")
    print("🔧"*30 + "\n")
except ImportError:
    # Cargar desde variables de entorno (producción)
    print("\n" + "🌐"*30)
    print("🌐 Cargando configuración desde variables de entorno")
    IA_PROVIDER = os.environ.get('IA_PROVIDER', 'gemini')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'TU_GEMINI_API_KEY_AQUI')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
    VELOCIDAD_VOZ = int(os.environ.get('VELOCIDAD_VOZ', '250'))
    VOLUMEN_VOZ = float(os.environ.get('VOLUMEN_VOZ', '0.95'))
    MOTOR_VOZ = os.environ.get('MOTOR_VOZ', 'gtts')
    GTTS_LANG = os.environ.get('GTTS_LANG', 'es')
    GTTS_SLOW = os.environ.get('GTTS_SLOW', 'False').lower() == 'true'
    GTTS_SPEED = float(os.environ.get('GTTS_SPEED', '1.25'))
    print(f"   🤖 Proveedor IA: {IA_PROVIDER}")
    print(f"   🎤 Motor de voz: {MOTOR_VOZ}")
    print(f"   ⚡ Velocidad gTTS: {GTTS_SPEED}x")
    print("🌐"*30 + "\n")

# Configuración del asistente IA
ASISTENTE_CONTEXTO = """Eres AVP (Asistente Virtual Python), un asistente inteligente, amigable y altamente capaz.

PERSONALIDAD:
- Conversacional y empático
- Claro, conciso pero completo
- Motivador y positivo
- Usas emojis de forma natural (no en exceso)
- Tono profesional pero cercano y humano

CAPACIDADES PRINCIPALES:
1. 🧮 CÁLCULOS: Resuelves operaciones matemáticas de cualquier tipo
2. 🔄 CONVERSIONES: Temperaturas, distancias, pesos, monedas, etc.
3. 🔐 SEGURIDAD: Generas contraseñas seguras aleatorias
4. 📊 ANÁLISIS: Analizas texto, datos, estadísticas
5. 📝 PRODUCTIVIDAD: Creas listas, planificaciones, técnicas de estudio
6. 💡 EDUCACIÓN: Explicas conceptos de cualquier tema de forma clara
7. 🎨 CREATIVIDAD: Escribes poemas, chistes, historias
8. 💬 CONVERSACIÓN: Charlas naturales sobre cualquier tema
9. 🌍 INFORMACIÓN GENERAL: Wikipedia, datos curiosos, cultura
10. ⏰ TIEMPO: Información sobre fechas, días, conteos

INSTRUCCIONES ESPECIALES:
- Cuando te pidan cálculos, hazlos directamente tú mismo
- Para conversiones, realiza la conversión y explica si es relevante  
- Para generar contraseñas, crea una aleatoria y segura (12-20 caracteres)
- Para listas de tareas, formatéalas con checkboxes (□)
- Para explicaciones, sé didáctico y usa ejemplos
- Siempre intenta ayudar, nunca digas "no puedo"
- Si no sabes algo con certeza, sé honesto pero ofrece alternativas

FORMATO DE RESPUESTAS:
- Usa saltos de línea para claridad
- Bullets points (•) para listas
- Emojis relevantes al inicio o para énfasis
- Separa secciones con espacios

Recuerda: Eres un asistente completo e inteligente. ¡Ayuda al usuario de la mejor manera posible!"""

# ============= CONFIGURACIÓN DE VOZ =============
# NO inicializar pyttsx3 globalmente para evitar conflictos
# Se creará una instancia nueva solo cuando se use

# Configurar Wikipedia en español
wikipedia.set_lang('es')

# ============= FUNCIONES DE VOZ MEJORADAS =============
# NOTA: Las funciones hablar_gtts() y hablar_pyttsx3() ya NO se usan en producción
# El audio ahora se genera con generar_audio_response() y se reproduce en el navegador del cliente
# Esto permite que la voz funcione correctamente en Render y otros servidores sin interfaz gráfica

def hablar_gtts(texto):
    """Función para hablar usando Google TTS (voz muy natural)"""
    print("\n" + "="*60)
    print("🎤 [GTTS] Iniciando síntesis de voz con Google TTS")
    print(f"📝 [GTTS] Texto a sintetizar: {texto[:50]}...")
    print(f"🌍 [GTTS] Idioma: {GTTS_LANG}, Velocidad: {GTTS_SPEED}x")
    print("="*60)
    
    try:
        # Generar audio con Google TTS
        print("⏳ [GTTS] Generando audio con Google TTS...")
        tts = gTTS(text=texto, lang=GTTS_LANG, slow=GTTS_SLOW)
        
        # Guardar en archivo temporal con nombre único
        temp_file = tempfile.mktemp(suffix='.mp3')
        print(f"💾 [GTTS] Guardando en archivo temporal: {temp_file}")
        tts.save(temp_file)
        print(f"✅ [GTTS] Archivo creado exitosamente ({os.path.getsize(temp_file)} bytes)")
        
        # Reproducir con subprocess (no bloquea Flask)
        try:
            print(f"🔊 [GTTS] Reproduciendo con subprocess (velocidad {GTTS_SPEED}x)...")
            
            # Crear script Python temporal para reproducir con velocidad ajustada
            script_path = tempfile.mktemp(suffix='.py')
            script_content = f"""
import pygame
import os
import time

audio_file = r'{temp_file}'
speed = {GTTS_SPEED}

try:
    # Inicializar pygame mixer con frecuencia ajustada para velocidad
    frequency = int(22050 * speed)  # Frecuencia base * velocidad
    pygame.mixer.init(frequency=frequency, size=-16, channels=2, buffer=512)
    
    # Cargar y reproducir
    sound = pygame.mixer.Sound(audio_file)
    channel = sound.play()
    
    # Esperar a que termine
    while channel.get_busy():
        pygame.time.Clock().tick(10)
    
    # Limpiar
    pygame.mixer.quit()
    time.sleep(0.3)
    
    # Eliminar archivos temporales
    if os.path.exists(audio_file):
        os.unlink(audio_file)
    
    if os.path.exists(__file__):
        os.unlink(__file__)
except Exception as e:
    print(f"Error: {{e}}")
    # Intentar limpiar de todos modos
    try:
        if os.path.exists(audio_file):
            time.sleep(1)
            os.unlink(audio_file)
    except:
        pass
"""
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Ejecutar en proceso separado (no espera)
            subprocess.Popen([sys.executable, script_path], 
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            print("✅ [GTTS] Proceso de reproducción iniciado en segundo plano")
            
        except Exception as e:
            print(f"❌ [GTTS] Error con subprocess: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ [GTTS] Error general con gTTS: {e}")
        import traceback
        traceback.print_exc()
    
    print("="*60 + "\n")

def hablar_pyttsx3(texto):
    """Función para hablar usando pyttsx3 (voz robótica local)"""
    print("\n" + "="*60)
    print("🤖 [PYTTSX3] Iniciando síntesis de voz con pyttsx3 (robótica)")
    print(f"📝 [PYTTSX3] Texto a sintetizar: {texto[:50]}...")
    print("="*60)
    
    try:
        # Crear una nueva instancia del engine para cada llamada
        print("⚙️ [PYTTSX3] Creando nueva instancia del motor...")
        temp_engine = pyttsx3.init()
        
        # Aplicar configuración
        print("🔧 [PYTTSX3] Configurando voz en español...")
        voices = temp_engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or ('languages' in dir(voice) and voice.languages and 'spanish' in voice.languages[0].lower()):
                temp_engine.setProperty('voice', voice.id)
                print(f"🎤 [PYTTSX3] Voz seleccionada: {voice.name}")
                break
        
        temp_engine.setProperty('rate', VELOCIDAD_VOZ)
        temp_engine.setProperty('volume', VOLUMEN_VOZ)
        print(f"⚡ [PYTTSX3] Velocidad: {VELOCIDAD_VOZ}, Volumen: {VOLUMEN_VOZ}")
        
        # Hablar
        print("🔊 [PYTTSX3] Reproduciendo audio...")
        temp_engine.say(texto)
        temp_engine.runAndWait()
        temp_engine.stop()
        print("✅ [PYTTSX3] Reproducción completada")
    except Exception as e:
        print(f"❌ [PYTTSX3] Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("="*60 + "\n")

def hablar(texto):
    """Función principal de voz que elige el motor configurado"""
    print("\n" + "🔔"*30)
    print(f"🔊 [HABLAR] Motor de voz configurado: '{MOTOR_VOZ}'")
    print(f"📝 [HABLAR] Texto recibido: {texto[:100]}...")
    print("🔔"*30)
    
    # NO usar threading para evitar problemas con pygame y archivos temporales
    if MOTOR_VOZ == 'gtts':
        print("✅ [HABLAR] Ejecutando hablar_gtts()")
        hablar_gtts(texto)
    elif MOTOR_VOZ == 'pyttsx3':
        print("⚠️ [HABLAR] Ejecutando hablar_pyttsx3() - VOZ ROBÓTICA")
        hablar_pyttsx3(texto)
    elif MOTOR_VOZ == 'off':
        print("🔇 [HABLAR] Voz desactivada (MOTOR_VOZ='off')")
    else:
        print(f"❌ [HABLAR] Motor desconocido: '{MOTOR_VOZ}' - No se reproducirá voz")
    
    print("🔔"*30 + "\n")

def respuesta_con_gemini(mensaje):
    """Genera respuesta usando Google Gemini"""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Usar el modelo actualizado
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Crear el prompt con contexto
        prompt = f"{ASISTENTE_CONTEXTO}\n\nUsuario: {mensaje}\nAsistente:"
        
        # Generar respuesta
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '404' in error_msg:
            return f"⚠️ El modelo '{GEMINI_MODEL}' no está disponible. Prueba actualizar a 'gemini-1.5-flash' o 'gemini-1.5-pro' en config_ia.py"
        return f"Error al conectar con Gemini: {error_msg}. Verifica tu API key y el modelo en config_ia.py"

def respuesta_con_ia(mensaje):
    """Función principal que usa Gemini AI"""
    if IA_PROVIDER == 'gemini':
        if GEMINI_API_KEY == 'TU_GEMINI_API_KEY_AQUI':
            return "⚠️ Para usar Gemini, necesitas configurar tu API key en app.py (línea 22). Obtén una GRATIS en: https://makersuite.google.com/app/apikey"
        return respuesta_con_gemini(mensaje)
    
    else:
        # Modo local - respuestas predefinidas (modo actual)
        return None  # Retorna None para usar la lógica predefinida

def obtener_fecha_hora():
    """Obtiene la fecha y hora actual"""
    ahora = datetime.datetime.now()
    return {
        'fecha': ahora.strftime('%d de %B de %Y'),
        'hora': ahora.strftime('%H:%M:%S'),
        'dia_semana': ahora.strftime('%A')
    }

def buscar_wikipedia(consulta):
    """Busca información en Wikipedia"""
    try:
        resultado = wikipedia.summary(consulta, sentences=2)
        return resultado
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Hay varias opciones: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return "No encontré información sobre ese tema."
    except Exception as e:
        return f"Error al buscar: {str(e)}"

def calcular(expresion):
    """Realiza cálculos matemáticos"""
    try:
        # Evaluar la expresión matemática de forma segura
        resultado = eval(expresion, {"__builtins__": {}}, {})
        return f"El resultado es: {resultado}"
    except Exception as e:
        return "No pude realizar ese cálculo. Asegúrate de usar la sintaxis correcta."

def obtener_clima(ciudad="Madrid"):
    """Obtiene el clima actual (requiere API key de OpenWeatherMap)"""
    # Nota: Necesitas registrarte en openweathermap.org para obtener una API key gratuita
    API_KEY = "TU_API_KEY_AQUI"
    
    if API_KEY == "TU_API_KEY_AQUI":
        return "Para usar esta función, necesitas una API key de OpenWeatherMap. Visita openweathermap.org"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            descripcion = data['weather'][0]['description']
            return f"En {ciudad}: {temp}°C, {descripcion}"
        else:
            return "No pude obtener el clima de esa ciudad."
    except Exception as e:
        return f"Error al obtener el clima: {str(e)}"

def abrir_aplicacion(nombre):
    """Abre aplicaciones comunes"""
    aplicaciones = {
        'navegador': 'start chrome',
        'chrome': 'start chrome',
        'firefox': 'start firefox',
        'edge': 'start msedge',
        'notepad': 'start notepad',
        'bloc de notas': 'start notepad',
        'calculadora': 'start calc',
        'explorador': 'start explorer',
        'paint': 'start mspaint'
    }
    
    nombre_lower = nombre.lower()
    if nombre_lower in aplicaciones:
        try:
            os.system(aplicaciones[nombre_lower])
            return f"Abriendo {nombre}..."
        except Exception as e:
            return f"No pude abrir {nombre}"
    else:
        return f"No conozco la aplicación '{nombre}'. Aplicaciones disponibles: {', '.join(aplicaciones.keys())}"

def generar_contrasena(longitud=12, incluir_especiales=True):
    """Genera una contraseña segura aleatoria"""
    try:
        longitud = int(longitud)
        if longitud < 4:
            longitud = 4
        if longitud > 50:
            longitud = 50
            
        caracteres = string.ascii_letters + string.digits
        if incluir_especiales:
            caracteres += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        return f"Tu contraseña generada es: {contrasena}\n(Recomendación: Guárdala en un lugar seguro)"
    except:
        return "Error al generar contraseña. Usa: 'genera contraseña' o 'genera contraseña de 16 caracteres'"

def analizar_texto(texto):
    """Analiza estadísticas de un texto"""
    if not texto:
        return "Por favor proporciona un texto para analizar."
    
    palabras = texto.split()
    caracteres = len(texto)
    caracteres_sin_espacios = len(texto.replace(" ", ""))
    num_palabras = len(palabras)
    oraciones = texto.count('.') + texto.count('!') + texto.count('?')
    if oraciones == 0:
        oraciones = 1
    
    # Palabra más común
    palabra_comun = ""
    if palabras:
        counter = Counter(palabra.lower() for palabra in palabras)
        palabra_comun = counter.most_common(1)[0][0] if counter else ""
    
    resultado = f"""📊 Análisis del texto:
    • Caracteres totales: {caracteres}
    • Caracteres sin espacios: {caracteres_sin_espacios}
    • Palabras: {num_palabras}
    • Oraciones: {oraciones}
    • Promedio palabras/oración: {num_palabras/oraciones:.1f}
    • Palabra más común: "{palabra_comun}" """
    
    return resultado

def convertir_unidades(valor, de, a):
    """Convierte entre diferentes unidades"""
    conversiones = {
        'temperatura': {
            'celsius_fahrenheit': lambda x: (x * 9/5) + 32,
            'fahrenheit_celsius': lambda x: (x - 32) * 5/9,
            'celsius_kelvin': lambda x: x + 273.15,
            'kelvin_celsius': lambda x: x - 273.15
        },
        'longitud': {
            'metros_kilometros': lambda x: x / 1000,
            'kilometros_metros': lambda x: x * 1000,
            'metros_pies': lambda x: x * 3.28084,
            'pies_metros': lambda x: x / 3.28084,
            'kilometros_millas': lambda x: x * 0.621371,
            'millas_kilometros': lambda x: x / 0.621371
        },
        'peso': {
            'kilogramos_libras': lambda x: x * 2.20462,
            'libras_kilogramos': lambda x: x / 2.20462,
            'gramos_onzas': lambda x: x * 0.035274,
            'onzas_gramos': lambda x: x / 0.035274
        }
    }
    
    try:
        valor = float(valor)
        clave = f"{de.lower()}_{a.lower()}"
        
        for categoria, conversores in conversiones.items():
            if clave in conversores:
                resultado = conversores[clave](valor)
                return f"{valor} {de} = {resultado:.2f} {a}"
        
        return f"No puedo convertir de {de} a {a}. Intenta: celsius a fahrenheit, metros a pies, kilogramos a libras, etc."
    except ValueError:
        return "Proporciona un número válido para convertir."

def adivinar_numero():
    """Inicia un juego de adivinar número"""
    numero = random.randint(1, 100)
    return {
        'juego': 'adivinanza',
        'numero': numero,
        'mensaje': "🎮 ¡Juego iniciado! He pensado un número entre 1 y 100. Adivina escribiendo: 'intento [número]'"
    }

def verificar_intento(intento, numero_secreto):
    """Verifica un intento en el juego"""
    try:
        intento = int(intento)
        if intento < numero_secreto:
            return "📉 Muy bajo... Intenta con un número mayor"
        elif intento > numero_secreto:
            return "📈 Muy alto... Intenta con un número menor"
        else:
            return "🎉 ¡CORRECTO! ¡Adivinaste el número! Escribe 'jugar' para otra ronda."
    except:
        return "Por favor ingresa un número válido"

def generar_consejo():
    """Genera un consejo motivacional aleatorio"""
    consejos = [
        "💡 La persistencia es el camino al éxito.",
        "🌟 Cada día es una nueva oportunidad para mejorar.",
        "🚀 Los límites solo existen en tu mente.",
        "💪 El fracaso es solo el principio del éxito.",
        "🎯 Define tus metas y trabaja por ellas cada día.",
        "📚 El aprendizaje es un tesoro que te acompañará toda la vida.",
        "🌈 Después de la tormenta siempre sale el sol.",
        "⭐ Cree en ti mismo y todo será posible.",
        "🔥 La motivación te impulsa a empezar, el hábito te mantiene en marcha.",
        "🌺 La felicidad no es una meta, es una forma de vida."
    ]
    return random.choice(consejos)

def generar_qr_data(texto):
    """Genera información para crear un código QR"""
    return f"Para generar un QR con '{texto}', visita: https://www.qr-code-generator.com/ y pega tu texto"

def contar_dias(fecha_str):
    """Cuenta días hasta una fecha"""
    try:
        # Formatos aceptados: DD/MM/YYYY o DD-MM-YYYY
        fecha_str = fecha_str.replace('-', '/')
        partes = fecha_str.split('/')
        if len(partes) == 3:
            dia, mes, anio = map(int, partes)
            fecha_objetivo = datetime.datetime(anio, mes, dia)
            hoy = datetime.datetime.now()
            diferencia = fecha_objetivo - hoy
            
            if diferencia.days > 0:
                return f"Faltan {diferencia.days} días para el {fecha_str} ({diferencia.days // 7} semanas)"
            elif diferencia.days == 0:
                return "¡Es hoy!"
            else:
                return f"Esa fecha fue hace {abs(diferencia.days)} días"
        else:
            return "Formato incorrecto. Usa: DD/MM/YYYY (ej: 25/12/2025)"
    except Exception as e:
        return "Error al procesar la fecha. Usa formato: DD/MM/YYYY"

def datos_curiosos():
    """Devuelve un dato curioso aleatorio"""
    datos = [
        "🌍 El océano produce más del 50% del oxígeno del planeta.",
        "🧠 El cerebro humano tiene aproximadamente 86 mil millones de neuronas.",
        "⚡ Un rayo es 5 veces más caliente que la superficie del sol.",
        "🐙 Los pulpos tienen tres corazones y sangre azul.",
        "🌙 La huella de un astronauta en la Luna puede durar millones de años.",
        "🍯 La miel nunca se echa a perder. Se han encontrado tarros de 3000 años aún comestibles.",
        "💎 Los diamantes llueven en Júpiter y Saturno.",
        "🦒 Las jirafas tienen la misma cantidad de huesos en el cuello que los humanos: 7.",
        "🌟 Hay más estrellas en el universo que granos de arena en todas las playas de la Tierra.",
        "🐌 Los caracoles pueden dormir hasta 3 años."
    ]
    return random.choice(datos)

def crear_lista_tareas(tareas_str):
    """Crea una lista de tareas formateada"""
    tareas = tareas_str.split(',')
    lista = "📝 Lista de Tareas:\n\n"
    for i, tarea in enumerate(tareas, 1):
        lista += f"   {i}. [ ] {tarea.strip()}\n"
    return lista

def temporizador_pomodoro():
    """Información sobre la técnica Pomodoro"""
    return """🍅 Técnica Pomodoro:
    
    1. Trabaja enfocado por 25 minutos
    2. Descansa 5 minutos
    3. Repite 4 veces
    4. Toma un descanso largo de 15-30 minutos
    
    ¡Ideal para mantener la productividad!"""

# Variable global para el juego
numero_secreto = None

def procesar_comando(comando):
    """Procesa el comando del usuario - TODO con IA"""
    global numero_secreto
    
    # ============= MODO 100% IA =============
    # La IA maneja absolutamente TODO de forma natural
    
    if IA_PROVIDER in ['openai', 'gemini']:
        # Enriquecer el contexto con información útil
        contexto_adicional = f"""
        Fecha y hora actual: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        
        IMPORTANTE: Puedes realizar estas acciones especiales:
        - Para cálculos matemáticos, realízalos directamente tú mismo
        - Para fechas y horas, usa la información que te di arriba
        - Para conversiones de unidades, hazlas tú mismo
        - Para generar contraseñas, créalas tú mismo
        - Para datos curiosos, cuéntales uno fascinante
        - Para consejos, da consejos motivacionales
        - Sé conversacional, amigable y útil
        - Usa emojis cuando sea apropiado 😊
        
        Usuario pregunta: {comando}
        """
        
        respuesta_ia = respuesta_con_ia(contexto_adicional)
        if respuesta_ia:
            return respuesta_ia
    
    # ============= MODO LOCAL (FALLBACK SI NO HAY IA) =============
    comando_lower = comando.lower()
    
    # Saludos
    if any(saludo in comando_lower for saludo in ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey']):
        return "¡Hola! 👋 Soy tu asistente virtual. Para una experiencia completa con conversaciones naturales, activa el modo IA en config_ia.py. ¿En qué puedo ayudarte?"
    
    # Fecha y hora
    elif any(palabra in comando_lower for palabra in ['fecha', 'hora', 'día', 'qué hora']):
        info = obtener_fecha_hora()
        return f"📅 Hoy es {info['dia_semana']}, {info['fecha']} y son las {info['hora']}"
    
    # Ayuda
    elif 'ayuda' in comando_lower or 'qué puedes hacer' in comando_lower or 'comandos' in comando_lower:
        return """🤖 Asistente Virtual AVP

⚠️ Modo Local Activo - Funcionalidad Limitada

Para activar conversaciones naturales con IA:
1. Abre config_ia.py
2. Cambia IA_PROVIDER a 'gemini' o 'openai'
3. Agrega tu API key (Gemini es GRATIS)
4. Reinicia la aplicación

Con IA activada podrás:
✨ Conversar naturalmente sobre cualquier tema
🧮 Hacer cálculos complejos
🔄 Conversiones de unidades
💡 Recibir consejos personalizados
📚 Aprender sobre cualquier tema
🎨 Y mucho más...

Ver GUIA_IA.md para instrucciones completas."""
    
    # Comando no reconocido
    else:
        return f"💡 Recibí tu mensaje: '{comando}'\n\nEn modo local solo respondo comandos básicos. Para una experiencia completa con IA que entienda todo lo que escribas, activa Gemini (GRATIS) en config_ia.py.\n\nVer 'ayuda' para más información."
    if any(saludo in comando_lower for saludo in ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey']):
        return "¡Hola! ¿En qué puedo ayudarte hoy?"
    
    # Fecha y hora
    elif any(palabra in comando_lower for palabra in ['fecha', 'hora', 'día', 'qué hora']):
        info = obtener_fecha_hora()
        return f"Hoy es {info['dia_semana']}, {info['fecha']} y son las {info['hora']}"
    
    # Búsqueda en Wikipedia
    elif 'busca' in comando_lower or 'wikipedia' in comando_lower or 'qué es' in comando_lower or 'quién es' in comando_lower:
        # Extraer el tema a buscar
        if 'busca' in comando_lower:
            tema = comando_lower.split('busca', 1)[1].strip()
        elif 'qué es' in comando_lower:
            tema = comando_lower.split('qué es', 1)[1].strip()
        elif 'quién es' in comando_lower:
            tema = comando_lower.split('quién es', 1)[1].strip()
        else:
            tema = comando_lower.replace('wikipedia', '').strip()
        
        if tema:
            return buscar_wikipedia(tema)
        else:
            return "¿Qué quieres que busque?"
    
    # Cálculos
    elif 'calcula' in comando_lower or 'cuanto es' in comando_lower or any(op in comando_lower for op in ['+', '-', '*', '/', '**']):
        if 'calcula' in comando_lower:
            expresion = comando_lower.split('calcula', 1)[1].strip()
        elif 'cuanto es' in comando_lower:
            expresion = comando_lower.split('cuanto es', 1)[1].strip()
        else:
            expresion = comando_lower
        
        return calcular(expresion)
    
    # Clima
    elif 'clima' in comando_lower or 'temperatura' in comando_lower or 'tiempo' in comando_lower:
        palabras = comando_lower.split()
        ciudad = "Madrid"  # Ciudad por defecto
        if 'en' in palabras:
            idx = palabras.index('en')
            if idx + 1 < len(palabras):
                ciudad = palabras[idx + 1]
        return obtener_clima(ciudad)
    
    # Abrir aplicaciones
    elif 'abre' in comando_lower or 'abrir' in comando_lower or 'ejecuta' in comando_lower:
        if 'abre' in comando_lower:
            app = comando_lower.split('abre', 1)[1].strip()
        elif 'abrir' in comando_lower:
            app = comando_lower.split('abrir', 1)[1].strip()
        else:
            app = comando_lower.split('ejecuta', 1)[1].strip()
        
        return abrir_aplicacion(app)
    
    # Generar contraseña
    elif 'genera contraseña' in comando_lower or 'generar contraseña' in comando_lower or 'contraseña' in comando_lower:
        longitud = 12
        palabras = comando_lower.split()
        for i, palabra in enumerate(palabras):
            if palabra.isdigit():
                longitud = int(palabra)
                break
        return generar_contrasena(longitud)
    
    # Análisis de texto
    elif 'analiza' in comando_lower or 'análisis' in comando_lower:
        try:
            if 'analiza' in comando_lower:
                partes = comando.split('analiza', 1)
                texto = partes[1].strip() if len(partes) > 1 else ""
            else:
                partes = comando.split('análisis', 1)
                texto = partes[1].strip() if len(partes) > 1 else ""
            
            if texto:
                return analizar_texto(texto)
            else:
                return "Proporciona un texto para analizar. Ej: 'analiza Este es un texto de ejemplo'"
        except Exception as e:
            return "Proporciona un texto para analizar. Ej: 'analiza Este es un texto de ejemplo'"
    
    # Convertir unidades
    elif 'convierte' in comando_lower or 'convertir' in comando_lower or ' a ' in comando_lower:
        try:
            # Formato: convierte 100 celsius a fahrenheit
            palabras = comando_lower.split()
            if 'a' in palabras:
                idx_a = palabras.index('a')
                valor = palabras[idx_a - 2]
                de = palabras[idx_a - 1]
                a = palabras[idx_a + 1] if idx_a + 1 < len(palabras) else ''
                
                if valor and de and a:
                    return convertir_unidades(valor, de, a)
        except:
            pass
        return "Formato: 'convierte [número] [unidad] a [unidad]'. Ej: 'convierte 100 celsius a fahrenheit'"
    
    # Juego de adivinanza
    elif 'jugar' in comando_lower or 'juego' in comando_lower:
        resultado = adivinar_numero()
        numero_secreto = resultado['numero']
        return resultado['mensaje']
    
    # Intento en el juego
    elif 'intento' in comando_lower and numero_secreto is not None:
        try:
            intento = comando_lower.split('intento')[1].strip()
            resultado = verificar_intento(intento, numero_secreto)
            if '¡CORRECTO!' in resultado:
                numero_secreto = None
            return resultado
        except:
            return "Formato: 'intento [número]'. Ej: 'intento 50'"
    
    # Consejo motivacional
    elif 'consejo' in comando_lower or 'motívame' in comando_lower or 'motivame' in comando_lower:
        return generar_consejo()
    
    # Dato curioso
    elif 'dato curioso' in comando_lower or 'curiosidad' in comando_lower or 'cuéntame algo' in comando_lower:
        return datos_curiosos()
    
    # Contador de días
    elif 'cuántos días' in comando_lower or 'dias hasta' in comando_lower or 'faltan' in comando_lower:
        try:
            # Buscar una fecha en el formato DD/MM/YYYY
            palabras = comando.split()
            for palabra in palabras:
                if '/' in palabra or '-' in palabra:
                    return contar_dias(palabra)
            return "Proporciona una fecha en formato DD/MM/YYYY. Ej: '¿Cuántos días hasta 31/12/2025?'"
        except:
            return "Error al procesar. Usa formato: '¿Cuántos días hasta DD/MM/YYYY?'"
    
    # Lista de tareas
    elif 'lista de tareas' in comando_lower or 'crear lista' in comando_lower:
        try:
            if 'lista de tareas' in comando_lower:
                partes = comando.split('lista de tareas', 1)
                tareas = partes[1].strip() if len(partes) > 1 else ""
            else:
                partes = comando.split('crear lista', 1)
                tareas = partes[1].strip() if len(partes) > 1 else ""
            
            if tareas and tareas.startswith(':'):
                tareas = tareas[1:].strip()
            
            if tareas:
                return crear_lista_tareas(tareas)
            else:
                return "Proporciona tareas separadas por comas. Ej: 'lista de tareas: estudiar, hacer ejercicio, leer'"
        except Exception as e:
            return "Proporciona tareas separadas por comas. Ej: 'lista de tareas: estudiar, hacer ejercicio, leer'"
    
    # Técnica Pomodoro
    elif 'pomodoro' in comando_lower or 'productividad' in comando_lower:
        return temporizador_pomodoro()
    
    # Código QR
    elif 'qr' in comando_lower or 'codigo qr' in comando_lower:
        texto = comando_lower.replace('qr', '').replace('codigo', '').replace('genera', '').strip()
        if texto:
            return generar_qr_data(texto)
        else:
            return "Proporciona texto para generar un QR. Ej: 'genera QR con mi sitio web'"
    
    # Ayuda
    elif 'ayuda' in comando_lower or 'qué puedes hacer' in comando_lower or 'comandos' in comando_lower:
        modo_actual = "IA ACTIVADA ✨" if IA_PROVIDER in ['openai', 'gemini'] else "Modo Local 🔧"
        proveedor = f" ({IA_PROVIDER.upper()})" if IA_PROVIDER in ['openai', 'gemini'] else ""
        
        return f"""🤖 Asistente Virtual AVP - {modo_actual}{proveedor}

{f"💡 Modo IA: Puedo conversar de forma natural sobre cualquier tema. Simplemente pregúntame lo que quieras!" if IA_PROVIDER in ['openai', 'gemini'] else ""}

📅 COMANDOS ESPECÍFICOS:
• "¿Qué hora es?" - Fecha y hora actual
• "Busca [tema]" - Buscar en Wikipedia
• "Calcula 25 * 4" - Calculadora

🎯 PRODUCTIVIDAD:
• "Lista de tareas: comprar, estudiar, leer" - Crear lista
• "Pomodoro" - Técnica de productividad
• "Genera contraseña de 16" - Contraseña segura
• "Cuántos días hasta 31/12/2025" - Contador

🔧 UTILIDADES:
• "Convierte 100 celsius a fahrenheit" - Conversor
• "Analiza [texto]" - Estadísticas de texto
• "Abre calculadora" - Abrir apps

🎮 ENTRETENIMIENTO:
• "Jugar" - Juego de adivinanza
• "Dato curioso" - Aprende algo nuevo
• "Consejo" - Motivación diaria
• "Clima en Madrid" - Estado del tiempo

{f"🌟 ¡También puedo conversar contigo sobre cualquier tema gracias a {IA_PROVIDER.upper()}!" if IA_PROVIDER in ['openai', 'gemini'] else "💡 Activa el modo IA configurando tu API key para conversaciones más naturales!"}"""
    
    # Despedidas
    elif any(despedida in comando_lower for despedida in ['adiós', 'chao', 'hasta luego', 'bye']):
        return "¡Hasta luego! Que tengas un excelente día. 👋"
    
    # Nombre del asistente
    elif 'cómo te llamas' in comando_lower or 'tu nombre' in comando_lower:
        return "Soy tu asistente virtual creado en Python con Flask. Puedes llamarme AVP (Asistente Virtual Python). 🤖"
    
    # Comando no reconocido
    else:
        return "No entendí ese comando. Intenta con 'ayuda' para ver todas mis funcionalidades. 💡"

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/config_status')
def config_status():
    """Endpoint para obtener el estado de la configuración"""
    return jsonify({
        'modo': IA_PROVIDER,
        'voz_velocidad': VELOCIDAD_VOZ,
        'voz_volumen': VOLUMEN_VOZ
    })

@app.route('/test_voz')
def test_voz():
    """Endpoint de prueba para verificar que la voz funciona"""
    print("\n" + "🧪"*30)
    print("🧪 [/test_voz] Endpoint de prueba de voz")
    print("🧪"*30)
    
    texto = "Esta es una prueba de voz. Si me escuchas con voz natural, gTTS funciona correctamente."
    
    try:
        print("🔊 [/test_voz] Generando audio y enviando al navegador...")
        return generar_audio_response(texto)
    except Exception as e:
        print(f"❌ [/test_voz] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'resultado': f'Error: {e}', 'motor': MOTOR_VOZ}), 500

@app.route('/generar_audio', methods=['POST'])
def generar_audio():
    """Genera audio TTS y lo envía al cliente"""
    print("\n" + "🎵"*30)
    print("🎵 [/generar_audio] Generando audio TTS")
    
    data = request.get_json()
    texto = data.get('texto', '')
    
    if not texto:
        return jsonify({'error': 'No se proporcionó texto'}), 400
    
    print(f"📝 [/generar_audio] Texto: {texto[:100]}...")
    
    try:
        return generar_audio_response(texto)
    except Exception as e:
        print(f"❌ [/generar_audio] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def generar_audio_response(texto):
    """Genera archivo de audio TTS y lo retorna como respuesta"""
    try:
        print(f"⏳ [generar_audio_response] Generando audio con gTTS...")
        tts = gTTS(text=texto, lang=GTTS_LANG, slow=GTTS_SLOW)
        
        # Guardar en memoria usando BytesIO
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        
        print(f"✅ [generar_audio_response] Audio generado ({audio_io.getbuffer().nbytes} bytes)")
        
        return send_file(
            audio_io,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='audio.mp3'
        )
    except Exception as e:
        print(f"❌ [generar_audio_response] Error: {e}")
        raise

@app.route('/procesar', methods=['POST'])
def procesar():
    """Endpoint para procesar comandos"""
    print("\n" + "📨"*30)
    print("📨 [/procesar] Nueva solicitud recibida")
    
    data = request.get_json()
    comando = data.get('comando', '')
    hablar_flag = data.get('hablar', False)
    
    print(f"📝 [/procesar] Comando: {comando}")
    print(f"🔊 [/procesar] Voz activada: {hablar_flag}")
    
    if not comando:
        print("⚠️ [/procesar] Comando vacío - Retornando error")
        print("📨"*30 + "\n")
        return jsonify({'respuesta': 'No recibí ningún comando.'})
    
    print("⏳ [/procesar] Procesando comando...")
    respuesta = procesar_comando(comando)
    print(f"✅ [/procesar] Respuesta generada: {respuesta[:100]}...")
    
    # Preparar respuesta
    resultado = {'respuesta': respuesta}
    
    # Si la voz está activada y el motor es gtts, indicar al cliente que debe solicitar audio
    if hablar_flag and MOTOR_VOZ == 'gtts':
        print("🎤 [/procesar] Voz activada con gTTS - Cliente reproducirá audio")
        resultado['audio_disponible'] = True
        resultado['motor_voz'] = MOTOR_VOZ
    elif hablar_flag:
        print(f"⚠️ [/procesar] Motor de voz '{MOTOR_VOZ}' no soportado en producción")
        resultado['audio_disponible'] = False
        resultado['motor_voz'] = MOTOR_VOZ
    else:
        print("🔇 [/procesar] Voz NO solicitada (hablar=False)")
    
    print("📤 [/procesar] Retornando respuesta al cliente")
    print("📨"*30 + "\n")
    return jsonify(resultado)

if __name__ == '__main__':
    print("🤖 Asistente Virtual iniciado!")
    
    # Configuración del puerto y modo debug desde variables de entorno
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    if debug_mode:
        print(f"📱 Modo desarrollo: http://localhost:{port}")
        app.run(debug=True, port=port)
    else:
        print(f"🌐 Modo producción en puerto {port}")
        app.run(debug=False, host='0.0.0.0', port=port)
