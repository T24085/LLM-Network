@echo off
setlocal

cd /d "%~dp0"

set "HOST=127.0.0.1"
set "PORT=8000"
set "SERVER_URL=http://%HOST%:%PORT%"
set "DASHBOARD_URL=%SERVER_URL%/dashboard"

set "DEMO_USER_ID=usr_demo_local_01"
set "DEMO_USER_CREDITS=10"

set "WORKER_ID=worker-local-01"
set "WORKER_OWNER_ID=bob"
set "WORKER_GPU_NAME=Local GPU"
set "WORKER_VRAM_GB=24"
set "WORKER_MODEL=qwen3:4b"
set "WORKER_TPS=qwen3:4b=60"

if /I "%~1"=="help" goto :help
if /I "%~1"=="--help" goto :help
if /I "%~1"=="/?" goto :help

set "PYTHON_BIN="
if exist ".venv\Scripts\python.exe" set "PYTHON_BIN=%CD%\.venv\Scripts\python.exe"
if not defined PYTHON_BIN (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_BIN=python"
)
if not defined PYTHON_BIN (
  echo Could not find Python. Create .venv or install Python 3.11+ first.
  exit /b 1
)

echo Starting Ollama Network API at %SERVER_URL%
start "Ollama Network API" cmd /k "cd /d ""%CD%"" && set PYTHONPATH=src && ""%PYTHON_BIN%"" -m ollama_network.server --host %HOST% --port %PORT%"

timeout /t 2 /nobreak >nul

echo Seeding demo user %DEMO_USER_ID% with %DEMO_USER_CREDITS% credits
set PYTHONPATH=src
"%PYTHON_BIN%" -m ollama_network.cli --server-url %SERVER_URL% register-user --user-id %DEMO_USER_ID% --starting-credits %DEMO_USER_CREDITS% >nul 2>nul

if /I "%~1"=="worker" (
  echo Starting sample worker %WORKER_ID%
  start "Ollama Network Worker" cmd /k "cd /d ""%CD%"" && set PYTHONPATH=src && ""%PYTHON_BIN%"" -m ollama_network.worker_daemon --server-url %SERVER_URL% --worker-id %WORKER_ID% --owner-user-id %WORKER_OWNER_ID% --gpu-name ""%WORKER_GPU_NAME%"" --vram-gb %WORKER_VRAM_GB% --model %WORKER_MODEL% --tps %WORKER_TPS%"
)

echo Opening dashboard: %DASHBOARD_URL%
start "" "%DASHBOARD_URL%"

echo.
echo Quick test is ready.
echo Dashboard: %DASHBOARD_URL%
echo Demo requester: %DEMO_USER_ID%
echo.
echo Optional:
echo   Run "%~nx0 worker" to also start a sample worker.
echo   Edit the variables at the top of this file if your GPU or model differ.
echo.
exit /b 0

:help
echo Ollama Network quickstart launcher
echo.
echo Usage:
echo   %~nx0
echo   %~nx0 worker
echo.
echo What it does:
echo   1. Starts the API server in a new terminal window.
echo   2. Seeds a demo user named "%DEMO_USER_ID%".
echo   3. Opens the dashboard in your browser.
echo   4. If you pass "worker", starts a sample worker window too.
echo.
echo Edit the variables at the top of this file to change the host, port, model, or worker defaults.
exit /b 0
