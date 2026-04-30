@echo off
setlocal

cd /d "%~dp0"

if not exist ".env" (
  echo Creating .env from .env.example...
  copy ".env.example" ".env" >nul
  echo.
  echo Add your GEMINI_API_KEY to .env before using chat.
  echo The app will still start, but chat needs that key.
  echo.
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating local Python virtual environment...
  py -3 -m venv .venv 2>nul
  if errorlevel 1 python -m venv .venv
)

call ".venv\Scripts\activate.bat"

echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Dependency install failed. Check the error above.
  pause
  exit /b 1
)

set "SERVER_MODE="
set "PORT="
for /f "tokens=1,2" %%A in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "$ports=8081..8090; foreach($p in $ports){ try { $r=Invoke-WebRequest -UseBasicParsing -Uri ('http://127.0.0.1:' + $p + '/') -TimeoutSec 1; if($r.Content -like '*ElectionIQ*'){ Write-Output ('EXISTING ' + $p); exit 0 } } catch {} }; foreach($p in $ports){ $busy=Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort $p -State Listen -ErrorAction SilentlyContinue; if(-not $busy){ Write-Output ('NEW ' + $p); exit 0 } }; Write-Output 'NONE 0'; exit 1"') do (
  set "SERVER_MODE=%%A"
  set "PORT=%%B"
)

if "%PORT%"=="" (
  echo.
  echo Could not find an available local port.
  pause
  exit /b 1
)

if /i "%SERVER_MODE%"=="EXISTING" (
  echo.
  echo ElectionIQ is already running on http://127.0.0.1:%PORT%/
  echo Opening the existing app instead of starting another copy.
  start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Process 'http://127.0.0.1:%PORT%/'"
  exit /b 0
)

if /i "%SERVER_MODE%"=="NONE" (
  echo.
  echo Ports 8081 through 8090 are already in use.
  pause
  exit /b 1
)

echo.
echo Starting ElectionIQ on http://127.0.0.1:%PORT%/
echo Press Ctrl+C in this window to stop the server.
echo.

start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:%PORT%/'"
python -m uvicorn main:app --host 127.0.0.1 --port %PORT%

echo.
echo Server stopped.
pause
