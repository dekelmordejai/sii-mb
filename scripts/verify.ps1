$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Push-Location (Join-Path $projectRoot 'backend')
try {
    & .\.venv\Scripts\python.exe -m ruff check app tests alembic; if($LASTEXITCODE -ne 0){throw 'Falló la revisión estática de Python'}
    & .\.venv\Scripts\python.exe -m pytest -q; if($LASTEXITCODE -ne 0){throw 'Fallaron las pruebas de backend'}
} finally {Pop-Location}
Push-Location (Join-Path $projectRoot 'frontend')
try {
    npm.cmd run typecheck; if($LASTEXITCODE -ne 0){throw 'Falló la comprobación de tipos'}
    npm.cmd run format:check; if($LASTEXITCODE -ne 0){throw 'Falló la comprobación de formato'}
    npm.cmd run build; if($LASTEXITCODE -ne 0){throw 'Falló la compilación'}
    npx.cmd playwright test; if($LASTEXITCODE -ne 0){throw 'Fallaron las pruebas en navegador'}
} finally {Pop-Location}
