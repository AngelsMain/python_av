# 📋 GUÍA COMPLETA: SUBIR A GITHUB Y DEPLOYMENT

## 🎯 PASO 1: Preparar el Proyecto

✅ Ya completado:
- Archivos de documentación eliminados
- `.gitignore` creado (protege config_ia.py)
- `config_ia.example.py` creado (plantilla sin API keys)
- `README.md` actualizado
- `Procfile` y `runtime.txt` para deployment
- `requirements.txt` actualizado con todas las dependencias

## 🚀 PASO 2: Subir a GitHub

### 2.1 Inicializar Git (si no lo has hecho)

```bash
cd c:\Users\Lenovo\OneDrive\Desktop\python_av
git init
```

### 2.2 Agregar todos los archivos

```bash
git add .
```

### 2.3 Hacer el primer commit

```bash
git commit -m "Initial commit: Asistente Virtual con IA"
```

### 2.4 Crear repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en el botón "+" arriba a la derecha
3. Selecciona "New repository"
4. Nombre: `asistente-virtual-ia` (o el que prefieras)
5. Descripción: "Asistente virtual con IA conversacional (Gemini/OpenAI) y voz natural"
6. Selecciona "Public"
7. **NO** marques "Add README" ni "Add .gitignore" (ya los tenemos)
8. Haz clic en "Create repository"

### 2.5 Conectar tu proyecto local con GitHub

Copia los comandos que GitHub te muestra (algo como esto):

```bash
git remote add origin https://github.com/TU_USUARIO/asistente-virtual-ia.git
git branch -M main
git push -u origin main
```

**¡Listo!** Tu código ya está en GitHub 🎉

## 🌐 PASO 3: Deployment en Vivo

### OPCIÓN A: Render (RECOMENDADA - 100% GRATIS)

1. **Crear cuenta en Render**
   - Ve a https://render.com
   - Regístrate con tu cuenta de GitHub

2. **Crear nuevo Web Service**
   - Dashboard → "New +" → "Web Service"
   - Selecciona "Build and deploy from a Git repository"
   - Conecta tu repositorio `asistente-virtual-ia`
   - Clic en "Connect"

3. **Configurar el servicio**
   - **Name**: `asistente-virtual-ia` (o el que quieras)
   - **Region**: Elige el más cercano a ti
   - **Branch**: `main`
   - **Root Directory**: (dejar en blanco)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. **Agregar Variables de Entorno**
   - En la sección "Environment Variables", haz clic en "Add Environment Variable"
   - Agrega estas variables:

   ```
   GEMINI_API_KEY = tu_api_key_de_gemini_aqui
   IA_PROVIDER = gemini
   MOTOR_VOZ = gtts
   GTTS_SPEED = 1.5
   ```

5. **Deploy**
   - Clic en "Create Web Service"
   - Espera 5-10 minutos mientras se construye
   - ¡Tu app estará en vivo en una URL como: `https://asistente-virtual-ia.onrender.com`

### OPCIÓN B: Railway (GRATIS - MUY FÁCIL)

1. **Crear cuenta en Railway**
   - Ve a https://railway.app
   - Regístrate con tu cuenta de GitHub

2. **Nuevo proyecto**
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configurar variables de entorno**
   - En el dashboard del proyecto, ve a "Variables"
   - Agrega:
     ```
     GEMINI_API_KEY = tu_api_key
     IA_PROVIDER = gemini
     MOTOR_VOZ = gtts
     ```

4. **Deploy automático**
   - Railway detecta Flask automáticamente
   - En 2-3 minutos tendrás tu URL

### OPCIÓN C: PythonAnywhere (GRATIS con limitaciones)

1. **Crear cuenta**
   - Ve a https://www.pythonanywhere.com
   - Regístrate (plan gratuito)

2. **Subir archivos**
   - Dashboard → "Files"
   - Sube tu carpeta `python_av`
   - O usa la consola bash y clona desde GitHub:
     ```bash
     git clone https://github.com/TU_USUARIO/asistente-virtual-ia.git
     cd asistente-virtual-ia
     pip install -r requirements.txt
     ```

3. **Crear Web App**
   - Dashboard → "Web"
   - "Add a new web app"
   - Python 3.10
   - Flask
   - Path: `/home/TU_USUARIO/asistente-virtual-ia`

4. **Configurar WSGI**
   - Edita el archivo WSGI:
     ```python
     import sys
     path = '/home/TU_USUARIO/asistente-virtual-ia'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

5. **Variables de entorno**
   - En el bash de PythonAnywhere:
     ```bash
     echo "export GEMINI_API_KEY='tu_api_key'" >> ~/.bashrc
     source ~/.bashrc
     ```

6. **Reload**
   - Botón "Reload" en la pestaña Web
   - Tu app estará en: `https://TU_USUARIO.pythonanywhere.com`

## ⚠️ IMPORTANTE: Configuración de API Keys

### Para Render y Railway:
Las variables de entorno ya están configuradas en el dashboard.

### Para PythonAnywhere:
Edita `config_ia.py` en el servidor o usa variables de entorno.

## 🔧 Comandos Git Útiles

### Ver estado
```bash
git status
```

### Hacer cambios y subirlos
```bash
git add .
git commit -m "Descripción de cambios"
git push
```

### Ver historial
```bash
git log --oneline
```

### Crear nueva rama
```bash
git checkout -b feature/nueva-funcionalidad
```

## 📱 Probar tu App en Vivo

Una vez deployada, prueba:
1. Abre la URL en tu navegador
2. Escribe: "Hola, ¿cómo estás?"
3. La IA debería responder
4. Haz clic en "🔊 Escuchar" para probar la voz

## 🐛 Solución de Problemas Comunes

### Error: "config_ia.py not found"
- Asegúrate de crear las variables de entorno en el dashboard
- O modifica `app.py` para usar variables de entorno:
  ```python
  import os
  GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'tu_key_aqui')
  ```

### Error: pygame no funciona en servidor
- **Nota**: La voz puede no funcionar en algunos servidores gratuitos
- Solo funciona si el servidor tiene soporte de audio
- Alternativa: Ofrecer solo texto en producción

### La app se duerme (Render free tier)
- Los planes gratuitos se duermen después de 15 minutos sin uso
- La primera carga tomará ~30 segundos
- Considera upgrade a plan pago (~$7/mes) si necesitas 24/7

## 🎉 ¡Felicidades!

Tu asistente virtual ya está:
- ✅ En GitHub (código respaldado)
- ✅ En vivo en internet
- ✅ Con IA conversacional
- ✅ Con voz natural

¡Comparte tu URL con tus profesores y compañeros! 🚀
