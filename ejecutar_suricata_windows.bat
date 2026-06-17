@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "SURICATA_EXE=C:\Program Files\Suricata\suricata.exe"
set "SURICATA_CONFIG=C:\Program Files\Suricata\suricata.yaml"
set "LOCAL_RULES=%PROJECT_DIR%suricata\local.rules"
set "LOG_DIR=%PROJECT_DIR%logs\suricata"
set "PYTHON_CMD=python"

if not exist "%SURICATA_EXE%" (
    echo [ERROR] No se encontro Suricata en "%SURICATA_EXE%".
    pause
    exit /b 1
)

if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

if exist "%PROJECT_DIR%.venv\Scripts\python.exe" (
    set "PYTHON_CMD=%PROJECT_DIR%.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        where py >nul 2>nul
        if errorlevel 1 (
            echo [ERROR] Python no esta disponible para detectar la IP local.
            pause
            exit /b 1
        )
        set "PYTHON_CMD=py -3"
    )
)

for /f "delims=" %%I in ('%PYTHON_CMD% -c "from src.network_utils import detect_network_info; print(detect_network_info().ip_address)" 2^>nul') do set "LOCAL_IP=%%I"

if not defined LOCAL_IP (
    echo [ERROR] No se pudo detectar la IP local automaticamente.
    pause
    exit /b 1
)

echo [INFO] Iniciando Suricata IDS en Windows...
echo [INFO] Interfaz/IP: %LOCAL_IP%
echo [INFO] Logs: %LOG_DIR%
echo [INFO] Reglas: %LOCAL_RULES%
echo.

"%SURICATA_EXE%" -c "%SURICATA_CONFIG%" -S "%LOCAL_RULES%" -l "%LOG_DIR%" -i %LOCAL_IP% -k none

pause
