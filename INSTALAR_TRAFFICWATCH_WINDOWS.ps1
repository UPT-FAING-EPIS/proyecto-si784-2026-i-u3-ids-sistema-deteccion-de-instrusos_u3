$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[AVISO] $Message" -ForegroundColor Yellow
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Get-PythonLauncher {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        try {
            & py -3 --version *> $null
            return @("py", "-3")
        }
        catch {
        }
    }

    if (Get-Command python -ErrorAction SilentlyContinue) {
        try {
            & python --version *> $null
            return @("python")
        }
        catch {
        }
    }

    return $null
}

function Invoke-Python {
    param(
        [string[]]$PythonCommand,
        [string[]]$Arguments
    )

    $exe = $PythonCommand[0]
    $pythonArgs = @()

    if ($PythonCommand.Count -gt 1) {
        $pythonArgs += $PythonCommand[1..($PythonCommand.Count - 1)]
    }

    & $exe @pythonArgs @Arguments
}

$ProjectRoot = $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$LauncherBat = Join-Path $ProjectRoot "INICIAR_TRAFFICWATCH.bat"
$CaptureBat = Join-Path $ProjectRoot "abrir_powershell_admin.bat"
$ShortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "TrafficWatch IDS.lnk"
$CaptureShortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "TrafficWatch IDS Captura.lnk"

Set-Location $ProjectRoot

Write-Host ""
Write-Host "TrafficWatch IDS - Instalador Windows" -ForegroundColor Magenta
Write-Host "Proyecto: $ProjectRoot"
Write-Host ""

if (-not (Test-Path "requirements.txt")) {
    Write-Fail "No se encontro requirements.txt. Ejecuta el instalador desde la carpeta del proyecto."
    exit 1
}

$PythonCommand = Get-PythonLauncher

if (-not $PythonCommand) {
    Write-Fail "No se encontro Python 3."
    Write-Warn "Instala Python desde https://www.python.org/downloads/windows/"
    Write-Warn "Marca la opcion 'Add Python to PATH' y vuelve a ejecutar este instalador."
    exit 1
}

$PythonVersion = Invoke-Python -PythonCommand $PythonCommand -Arguments @("--version")
Write-Ok "Python detectado: $PythonVersion"

if (-not (Test-Path $VenvPython)) {
    Write-Info "Creando entorno virtual .venv..."
    Invoke-Python -PythonCommand $PythonCommand -Arguments @("-m", "venv", ".venv")
}
else {
    Write-Ok "Entorno virtual .venv ya existe."
}

Write-Info "Actualizando pip..."
& $VenvPython -m pip install --upgrade pip

Write-Info "Instalando dependencias del proyecto..."
& $VenvPython -m pip install -r requirements.txt
Write-Ok "Dependencias instaladas."

Write-Info "Preparando carpetas de ejecucion..."
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "logs\suricata" | Out-Null

Write-Info "Creando regla de firewall para el dashboard en puerto 5000..."
try {
    $existingRule = Get-NetFirewallRule -DisplayName "TrafficWatch IDS Dashboard" -ErrorAction SilentlyContinue

    if (-not $existingRule) {
        New-NetFirewallRule `
            -DisplayName "TrafficWatch IDS Dashboard" `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort 5000 `
            -Action Allow `
            -Profile Private | Out-Null
        Write-Ok "Firewall configurado para red privada."
    }
    else {
        Write-Ok "La regla de firewall ya existe."
    }
}
catch {
    Write-Warn "No se pudo crear la regla de firewall. Ejecuta PowerShell como administrador si otra PC no puede entrar."
}

Write-Info "Creando acceso directo en el escritorio..."
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $LauncherBat
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "Iniciar TrafficWatch IDS"
$Shortcut.Save()
Write-Ok "Acceso directo creado: $ShortcutPath"

$CaptureShortcut = $Shell.CreateShortcut($CaptureShortcutPath)
$CaptureShortcut.TargetPath = $CaptureBat
$CaptureShortcut.WorkingDirectory = $ProjectRoot
$CaptureShortcut.Description = "Iniciar captura IDS como administrador"
$CaptureShortcut.Save()
Write-Ok "Acceso directo de captura creado: $CaptureShortcutPath"

Write-Info "Verificando herramientas opcionales..."

if (Get-Command nmap -ErrorAction SilentlyContinue) {
    Write-Ok "Nmap disponible."
}
else {
    Write-Warn "Nmap no esta disponible. El escaneo real con Nmap no funcionara hasta instalarlo."

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        $InstallNmap = Read-Host "Quieres instalar Nmap automaticamente con winget? (S/N)"

        if ($InstallNmap -match "^[sS]") {
            Write-Info "Instalando Nmap con winget..."
            winget install --id Insecure.Nmap --exact --accept-package-agreements --accept-source-agreements

            if (Get-Command nmap -ErrorAction SilentlyContinue) {
                Write-Ok "Nmap instalado correctamente."
            }
            else {
                Write-Warn "Nmap se instalo, pero esta terminal todavia no lo detecta en PATH."
                Write-Warn "Cierra y vuelve a abrir PowerShell/CMD, luego prueba: nmap --version"
            }
        }
        else {
            Write-Warn "Instalacion de Nmap omitida por el usuario."
            Write-Warn "Descarga manual: https://nmap.org/download.html#windows"
        }
    }
    else {
        Write-Warn "WinGet no esta disponible en esta computadora."
        Write-Warn "Descarga manual: https://nmap.org/download.html#windows"
    }
}

if (Test-Path "C:\Program Files\Suricata\suricata.exe") {
    Write-Ok "Suricata detectado."
}
else {
    Write-Warn "Suricata no esta instalado. El panel Suricata funcionara solo como integracion/demo."
}

$NpcapInstalled = (Test-Path "C:\Windows\System32\Npcap") -or [bool](Get-Service npcap -ErrorAction SilentlyContinue)

if ($NpcapInstalled) {
    Write-Ok "Npcap detectado. La captura real con Scapy puede funcionar con permisos de administrador."
}
else {
    Write-Warn "Npcap no esta instalado. La captura IDS real puede no funcionar."
    $OpenNpcap = Read-Host "Quieres abrir la pagina oficial para instalar Npcap? (S/N)"

    if ($OpenNpcap -match "^[sS]") {
        Start-Process "https://npcap.com/#download"
        Write-Warn "Instala Npcap y luego vuelve a ejecutar este instalador o inicia la captura como administrador."
    }
    else {
        Write-Warn "Instalacion de Npcap omitida. Descarga manual: https://npcap.com/#download"
    }
}

Write-Host ""
Write-Ok "Instalacion finalizada."
Write-Host ""
Write-Host "Para iniciar:" -ForegroundColor Cyan
Write-Host "  1. Doble clic en el acceso directo 'TrafficWatch IDS' del escritorio"
Write-Host "  2. O ejecuta: INICIAR_TRAFFICWATCH.bat"
Write-Host "  3. Para captura real: doble clic en 'TrafficWatch IDS Captura' y acepta permisos de administrador"
Write-Host ""
Write-Host "URLs locales:" -ForegroundColor Cyan
Write-Host "  Dashboard: http://127.0.0.1:5000/"
Write-Host "  Laboratorio: http://127.0.0.1:5000/attack-lab"
Write-Host ""
