param([switch]$Install,[switch]$CreateAdmin)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
$backendRoot=Join-Path $projectRoot 'backend'
$frontendRoot=Join-Path $projectRoot 'frontend'
$pythonPath=Join-Path $backendRoot '.venv\Scripts\python.exe'
if($Install){
    Push-Location $backendRoot
    try {
        py -3.12 -m venv .venv
        if($LASTEXITCODE -ne 0){throw 'No se pudo crear el entorno Python 3.12'}
        & $pythonPath -m pip install -r requirements-lock.txt
        if($LASTEXITCODE -ne 0){throw 'No se pudieron instalar las dependencias Python'}
    } finally {Pop-Location}
    Push-Location $frontendRoot
    try {npm.cmd ci; if($LASTEXITCODE -ne 0){throw 'No se pudieron instalar las dependencias de la interfaz'}} finally {Pop-Location}
}
if(!(Test-Path -LiteralPath $pythonPath)){throw 'Crea backend/.venv siguiendo README.md o ejecuta primero con -Install'}
if($CreateAdmin){
    Push-Location $backendRoot
    try {& $pythonPath -m app.manage create-admin; if($LASTEXITCODE -ne 0){throw 'No se creó la cuenta administrativa'}} finally {Pop-Location}
}
$apiProcess=Start-Process -FilePath $pythonPath -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000' -WorkingDirectory $backendRoot -WindowStyle Hidden -PassThru
try {
    Write-Host 'SII-MB: http://127.0.0.1:3000 . Para detenerlo pulsa Ctrl+C en esta terminal.'
    Push-Location $frontendRoot
    try {npm.cmd run dev} finally {Pop-Location}
} finally {if(!$apiProcess.HasExited){Stop-Process -Id $apiProcess.Id}}
