# 📤 Instrucciones para Subir a GitHub y Desplegar

## 🚀 Paso 1: Subir a GitHub

### 1.1 Crear repositorio en GitHub
1. Ve a [github.com](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** (arriba derecha) → **"New repository"**
3. Nombre del repositorio: `asistente-virtual-ia` (o el que prefieras)
4. Descripción: `Asistente virtual con IA usando Google Gemini y síntesis de voz`
5. Selecciona **Public** (o Private si lo prefieres)
6. **NO** marques "Add a README file" (ya tenemos uno)
7. Haz clic en **"Create repository"**

### 1.2 Conectar y subir el código

Copia y ejecuta estos comandos en tu terminal (CMD):

```cmd
# Conectar con tu repositorio de GitHub
git remote add origin https://github.com/TU_USUARIO/asistente-virtual-ia.git

# Subir el código
git push -u origin main
```

**Nota:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

Si te pide credenciales:
- Usuario: tu nombre de usuario de GitHub
- Contraseña: usa un **Personal Access Token** (no tu contraseña normal)
  - Para crear un token: Settings → Developer settings → Personal access tokens → Generate new token

---

## 🌐 Paso 2: Desplegar en Render.com (GRATIS)

### 2.1 Crear cuenta en Render
1. Ve a [render.com](https://render.com)
2. Haz clic en **"Get Started for Free"**
3. Regístrate con tu cuenta de GitHub (recomendado)

### 2.2 Crear Web Service
1. En el dashboard de Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub:
   - Haz clic en **"Connect a repository"**
   - Selecciona tu repositorio `asistente-virtual-ia`
3. Configura el servicio:
   - **Name:** `asistente-virtual-ia` (o el que prefieras)
   - **Region:** Selecciona la más cercana (ej: Oregon, USA)
   - **Branch:** `main`
   - **Root Directory:** (déjalo vacío)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app` (Render lo detecta automáticamente)

### 2.3 Configurar Variables de Entorno
En la sección **"Environment Variables"**, agrega:

| KEY | VALUE |
|-----|-------|
| `GEMINI_API_KEY` | Tu API key de Google Gemini |
| `FLASK_ENV` | `production` |
| `IA_PROVIDER` | `gemini` |
| `MOTOR_VOZ` | `gtts` |
| `GTTS_SPEED` | `1.25` |

### 2.4 Desplegar
1. Haz clic en **"Create Web Service"**
2. Render automáticamente:
   - Clonará tu repositorio
   - Instalará las dependencias
   - Desplegará la aplicación
3. Espera 2-5 minutos...
4. ¡Tu app estará en vivo! 🎉

Tu URL será algo como: `https://asistente-virtual-ia.onrender.com`

---

## 🔄 Actualizar la Aplicación

Cada vez que hagas cambios:

```cmd
# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de tus cambios"

# Subir a GitHub
git push origin main
```

**Render automáticamente detectará los cambios y redesplegará tu app.**

---

## 🛠️ Alternativas de Despliegue

### Railway.app (GRATIS - Fácil)
1. Ve a [railway.app](https://railway.app)
2. Crea proyecto desde GitHub
3. Agrega las mismas variables de entorno
4. Deploy automático

### Heroku (Tiene capa gratuita limitada)
```cmd
# Instalar Heroku CLI
# Descargar de: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create asistente-virtual-ia

# Configurar variables de entorno
heroku config:set GEMINI_API_KEY=tu_api_key
heroku config:set FLASK_ENV=production
heroku config:set IA_PROVIDER=gemini
heroku config:set MOTOR_VOZ=gtts

# Deploy
git push heroku main

# Abrir en navegador
heroku open
```

---

## ⚠️ Importante: Seguridad

### ✅ NUNCA subas a GitHub:
- ❌ `config_ia.py` (contiene tu API key)
- ❌ Archivos `.env` con credenciales
- ❌ Claves privadas o tokens

### ✅ El archivo `.gitignore` ya protege:
```
config_ia.py
*.pyc
__pycache__/
static/temp/*.mp3
.env
```

### ✅ Siempre usa variables de entorno en producción:
- En Render/Railway/Heroku: Configura en el panel web
- En local: Usa `config_ia.py` (no versionado)

---

## 📊 Verificar que Funciona

Después de desplegar:

1. Abre la URL de tu app (ej: `https://asistente-virtual-ia.onrender.com`)
2. Escribe un mensaje: "Hola, ¿cómo estás?"
3. Activa la voz con el botón 🔊
4. Verifica que:
   - ✅ La IA responde correctamente
   - ✅ La voz funciona (puede tardar un poco en la primera carga)
   - ✅ No hay errores en la consola

---

## 🐛 Solución de Problemas

### Error: "Application Error"
- Revisa los logs en Render: Dashboard → tu servicio → "Logs"
- Verifica que todas las variables de entorno estén configuradas

### Error: "No module named 'pygame'"
- Render puede tener problemas con pygame
- Solución: La voz funciona usando subprocesos, pero en producción puede que no se reproduzca (limitación de servidores sin audio)

### La voz no funciona en producción
- **Normal:** Los servidores web no tienen salida de audio
- **Solución:** La app genera el audio, pero el navegador del usuario lo reproduce
- Si necesitas audio del lado del servidor, considera servicios especializados

---

## 🎉 ¡Listo!

Tu asistente virtual ya está en vivo y accesible desde cualquier parte del mundo.

**Comparte tu URL:**
```
https://tu-app.onrender.com
```

¡Disfruta de tu asistente virtual con IA! 🤖✨
