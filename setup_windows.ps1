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

function Get-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        try {
            & py -3 --version *> $null
            return @("py", "-3")
        }
        catch {
            # Continue with python.exe lookup.
        }
    }

    if (Get-Command python -ErrorAction SilentlyContinue) {
        try {
            & python --version *> $null
            return @("python")
        }
        catch {
            # No usable python command found.
        }
    }

    return $null
}

function Invoke-Python {
    param(
        [string[]]$PythonCommand,
        [string[]]$Arguments
    )

    $executable = $PythonCommand[0]
    $pythonArgs = @()

    if ($PythonCommand.Count -gt 1) {
        $pythonArgs += $PythonCommand[1..($PythonCommand.Count - 1)]
    }

    & $executable @pythonArgs @Arguments
}

function Test-NmapInstalled {
    if (-not (Get-Command nmap -ErrorAction SilentlyContinue)) {
        return $false
    }

    try {
        & nmap --version *> $null
        return $true
    }
    catch {
        return $false
    }
}

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host ""
Write-Host "IDS PRO - Setup automatico para Windows" -ForegroundColor Magenta
Write-Host "Proyecto: $ProjectRoot"
Write-Host ""

if (-not (Test-Path "requirements.txt")) {
    Write-Fail "No se encontro requirements.txt. Ejecuta este script desde la carpeta del proyecto."
    exit 1
}

Write-Info "Verificando Python..."
$PythonCommand = Get-PythonCommand

if (-not $PythonCommand) {
    Write-Fail "No se encontro Python 3 instalado o disponible en PATH."
    Write-Warn "Instala Python 3.9 o superior y vuelve a ejecutar este script."
    Write-Warn "Pagina oficial: https://www.python.org/downloads/windows/"
    exit 1
}

$PythonVersion = Invoke-Python -PythonCommand $PythonCommand -Arguments @("--version")
Write-Ok "Python detectado: $PythonVersion"

Write-Info "Verificando pip..."
try {
    Invoke-Python -PythonCommand $PythonCommand -Arguments @("-m", "pip", "--version")
    Write-Ok "pip disponible."
}
catch {
    Write-Fail "pip no esta disponible para el Python detectado."
    Write-Warn "Prueba reparar Python marcando la opcion 'pip' en el instalador."
    exit 1
}

Write-Info "Instalando dependencias desde requirements.txt..."
Invoke-Python -PythonCommand $PythonCommand -Arguments @("-m", "pip", "install", "-r", "requirements.txt")
Write-Ok "Dependencias del proyecto instaladas."

Write-Info "Verificando Nmap..."
if (Test-NmapInstalled) {
    $NmapVersion = (& nmap --version | Select-Object -First 1)
    Write-Ok "Nmap detectado: $NmapVersion"
}
else {
    Write-Warn "Nmap no esta instalado o no esta disponible en PATH."

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Fail "WinGet no esta disponible en este Windows."
        Write-Warn "Instala Nmap manualmente desde: https://nmap.org/download.html#windows"
        exit 1
    }

    Write-Info "Instalando Nmap con WinGet..."
    winget install --id Insecure.Nmap --exact --accept-package-agreements --accept-source-agreements

    if (Test-NmapInstalled) {
        $NmapVersion = (& nmap --version | Select-Object -First 1)
        Write-Ok "Nmap instalado correctamente: $NmapVersion"
    }
    else {
        Write-Warn "Nmap se instalo, pero todavia no aparece en PATH en esta terminal."
        Write-Warn "Cierra y vuelve a abrir PowerShell/CMD, luego ejecuta: nmap --version"
    }
}

Write-Host ""
Write-Ok "Setup finalizado."
Write-Host ""
Write-Host "Siguientes comandos sugeridos:" -ForegroundColor Cyan
Write-Host "  python run_dashboard.py"
Write-Host "  python main.py"
Write-Host "  nmap -p 1-100 <gateway>"
Write-Host ""
