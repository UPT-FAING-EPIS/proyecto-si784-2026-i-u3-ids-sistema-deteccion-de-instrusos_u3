@echo off
cd /d "%~dp0"

echo.
echo Iniciando IDS PRO Dashboard
echo Ubicacion del proyecto:
echo %CD%
echo.
echo Ejecutando:
echo   python run_dashboard.py
echo.
echo Dashboard:
echo   http://127.0.0.1:5000
echo.

python run_dashboard.py

echo.
echo El dashboard se detuvo o no pudo iniciar.
echo La ventana queda abierta para revisar mensajes.
echo.

cmd /k
