@echo off
echo ========================================
echo    SUBIR PROYECTO A GITHUB
echo ========================================
echo.

REM Inicializar Git
echo [1/5] Inicializando repositorio Git...
git init
echo.

REM Agregar archivos
echo [2/5] Agregando archivos al staging...
git add .
echo.

REM Hacer commit
echo [3/5] Creando commit inicial...
git commit -m "Initial commit: Asistente Virtual con IA y voz natural"
echo.

REM Instrucciones
echo [4/5] CREA TU REPOSITORIO EN GITHUB:
echo.
echo 1. Ve a: https://github.com/new
echo 2. Nombre: asistente-virtual-ia
echo 3. Descripcion: Asistente virtual con IA conversacional
echo 4. Selecciona: Public
echo 5. NO marques README ni .gitignore
echo 6. Clic en "Create repository"
echo.
echo Presiona ENTER cuando hayas creado el repositorio...
pause > nul

REM Pedir usuario
echo.
set /p GITHUB_USER="Ingresa tu usuario de GitHub: "
echo.

REM Conectar con GitHub
echo [5/5] Conectando con GitHub...
git remote add origin https://github.com/%GITHUB_USER%/asistente-virtual-ia.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo    COMPLETADO!
echo ========================================
echo.
echo Tu proyecto esta en:
echo https://github.com/%GITHUB_USER%/asistente-virtual-ia
echo.
echo Siguiente paso: Ve a DEPLOYMENT_GUIDE.md para deployar en vivo
echo.
pause
