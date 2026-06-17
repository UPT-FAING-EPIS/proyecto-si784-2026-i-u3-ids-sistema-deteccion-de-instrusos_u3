@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "DASHBOARD_URL=http://127.0.0.1:5000"
set "SURICATA_EXE=C:\Program Files\Suricata\suricata.exe"
set "SURICATA_CONFIG=C:\Program Files\Suricata\suricata.yaml"
set "SURICATA_RULES=%PROJECT_DIR%suricata\local.rules"
set "SURICATA_LOGS=%PROJECT_DIR%logs\suricata"
set "PYTHON_CMD=python"

cd /d "%PROJECT_DIR%"

echo ==========================================
echo  TrafficWatch IDS
echo ==========================================
echo.
echo Iniciando dashboard...

if exist "%PROJECT_DIR%.venv\Scripts\python.exe" (
    set "PYTHON_CMD=%PROJECT_DIR%.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        where py >nul 2>nul
        if errorlevel 1 (
            echo [ERROR] Python no esta disponible.
            echo Ejecuta INSTALAR_TRAFFICWATCH_WINDOWS.ps1 o instala Python 3.
            pause
            exit /b 1
        )
        set "PYTHON_CMD=py -3"
    )
)

echo Verificando dependencias Python...
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    echo Ejecuta manualmente: %PYTHON_CMD% -m pip install -r requirements.txt
    pause
    exit /b 1
)

start "TrafficWatch Dashboard" /D "%PROJECT_DIR%" cmd /k %PYTHON_CMD% run_dashboard.py

if exist "%SURICATA_EXE%" (
    if not exist "%SURICATA_LOGS%" mkdir "%SURICATA_LOGS%"
    for /f "delims=" %%I in ('%PYTHON_CMD% -c "from src.network_utils import detect_network_info; print(detect_network_info().ip_address)" 2^>nul') do set "SURICATA_INTERFACE=%%I"
    if defined SURICATA_INTERFACE (
        echo Iniciando Suricata IDS en %SURICATA_INTERFACE%...
        start "TrafficWatch Suricata" /D "%PROJECT_DIR%" cmd /k ""%SURICATA_EXE%" -c "%SURICATA_CONFIG%" -S "%SURICATA_RULES%" -l "%SURICATA_LOGS%" -i %SURICATA_INTERFACE% -k none"
    ) else (
        echo [AVISO] No se pudo detectar la IP local para Suricata automaticamente.
    )
) else (
    echo [AVISO] Suricata no esta instalado en C:\Program Files\Suricata.
)

echo Abriendo navegador...
timeout /t 3 /nobreak >nul
start "" "%DASHBOARD_URL%"

echo.
echo Listo. Dashboard: %DASHBOARD_URL%
echo Laboratorio remoto: revisa la ventana del dashboard para ver la URL /attack-lab
echo Puedes cerrar esta ventana.
timeout /t 5 /nobreak >nul
