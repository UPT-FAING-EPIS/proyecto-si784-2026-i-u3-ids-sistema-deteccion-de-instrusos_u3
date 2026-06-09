$ErrorActionPreference = "Continue"

Set-Location -LiteralPath $PSScriptRoot

Write-Host ""
Write-Host "PowerShell listo para pruebas IDS PRO" -ForegroundColor Green
Write-Host "Escribe salir para cerrar esta ventana." -ForegroundColor Yellow

while ($true) {
    Write-Host ""
    python -m src.network_utils --examples-only --shell powershell
    Write-Host ""

    $command = Read-Host "Escribe o pega un comando para ejecutar [Enter para actualizar / salir para cerrar]"

    if ($command -eq "salir") {
        break
    }

    if ([string]::IsNullOrWhiteSpace($command)) {
        continue
    }

    Write-Host ""
    Invoke-Expression $command
}
