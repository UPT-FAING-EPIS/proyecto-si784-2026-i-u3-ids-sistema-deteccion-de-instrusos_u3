$ErrorActionPreference = "Stop"

$ProjectRoot = $PSScriptRoot
$EscapedProjectRoot = $ProjectRoot.Replace("'", "''")

$Command = @"
`$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath '$EscapedProjectRoot'
Write-Host ''
Write-Host 'Iniciando IDS PRO como administrador' -ForegroundColor Green
Write-Host 'Ubicacion del proyecto:' -ForegroundColor Cyan
Write-Host '$EscapedProjectRoot'
Write-Host ''
`$PythonCmd = 'python'

if (Test-Path '.venv\Scripts\python.exe') {
    `$PythonCmd = '.venv\Scripts\python.exe'
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    `$PythonCmd = 'py -3'
}

Write-Host "Ejecutando: `$PythonCmd main.py" -ForegroundColor Cyan
Write-Host ''

try {
    Invoke-Expression "`$PythonCmd main.py"

    if (`$LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host "El IDS termino con codigo de salida `$LASTEXITCODE." -ForegroundColor Yellow
    }
}
catch {
    Write-Host ''
    Write-Host 'No se pudo iniciar el IDS.' -ForegroundColor Red
    Write-Host `$_.Exception.Message -ForegroundColor Red
}

Write-Host ''
Write-Host 'La ventana queda abierta para revisar mensajes o ejecutar otro comando.' -ForegroundColor Cyan
"@

Start-Process powershell.exe -Verb RunAs -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    $Command
)
