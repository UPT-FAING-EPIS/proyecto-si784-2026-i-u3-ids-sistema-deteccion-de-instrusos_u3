@echo off
setlocal

cd /d "%~dp0"

echo ==========================================
echo  Creando ejecutable TrafficWatch IDS
echo ==========================================
echo.

python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo No se pudo instalar PyInstaller.
    pause
    exit /b 1
)

python -m PyInstaller ^
  --noconfirm ^
  --name TrafficWatchIDS ^
  --add-data "web\templates;web\templates" ^
  --add-data "suricata;suricata" ^
  --add-data "config.json;." ^
  trafficwatch_desktop.py

if errorlevel 1 (
    echo No se pudo crear el ejecutable.
    pause
    exit /b 1
)

echo.
echo Ejecutable creado en:
echo %CD%\dist\TrafficWatchIDS\TrafficWatchIDS.exe
echo.
pause
