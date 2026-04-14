@echo off
setlocal

cd /d "%~dp0"

if /I "%~1"=="help" goto :help
if /I "%~1"=="--help" goto :help
if /I "%~1"=="/?" goto :help

set "PYTHON_CMD="
if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=""%CD%\.venv\Scripts\python.exe"""
if not defined PYTHON_CMD (
  where py >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=py -3"
)
if not defined PYTHON_CMD (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=python"
)
if not defined PYTHON_CMD (
  echo Could not find Python. Create .venv or install Python 3.8+ first.
  exit /b 1
)

set "WORKER_CONFIG="
if exist ".runtime\worker.local.json" set "WORKER_CONFIG=%CD%\.runtime\worker.local.json"
if not defined WORKER_CONFIG if exist "llm-network-worker.json" set "WORKER_CONFIG=%CD%\llm-network-worker.json"

echo.
echo Starting one-click LLM Network quickstart.
echo.

call "%~dp0start_network_server.bat"
if errorlevel 1 exit /b 1

echo Waiting for the local coordinator at http://localhost:8000/health
powershell -NoProfile -ExecutionPolicy Bypass -Command "$deadline=(Get-Date).AddSeconds(60); $url='http://localhost:8000/health'; while((Get-Date) -lt $deadline){ try { $response=Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5; if($response.StatusCode -eq 200){ exit 0 } } catch { Start-Sleep -Seconds 2 } }; exit 1"
if errorlevel 1 (
  echo The coordinator did not become healthy in time.
  echo Start the dashboard manually with start_dashboard.bat after the server window finishes initializing.
  exit /b 1
)

if not defined WORKER_CONFIG (
  echo.
  echo No worker config found.
  echo Download llm-network-worker.json from the dashboard and place it next to this file, or create .runtime\worker.local.json.
  exit /b 1
)

echo.
echo Starting worker using %WORKER_CONFIG%
start "LLM Network Worker" cmd /k "cd /d ""%CD%"" && set PYTHONPATH=src && %PYTHON_CMD% -m ollama_network.worker_daemon --config ""%WORKER_CONFIG%"""

start "" "http://localhost:8000/dashboard"
echo.
echo One-click launch requested. The server is starting in one window and the worker in another.
exit /b 0

:help
echo LLM Network worker launcher
echo.
echo Usage:
echo   %~nx0
echo.
echo What it does:
echo   1. Starts the local coordinator server.
echo   2. Waits for the coordinator health check to pass.
echo   3. Starts the worker daemon using llm-network-worker.json or .runtime\worker.local.json.
echo   4. Opens the local dashboard in your browser.
echo.
echo Environment variables:
echo   OLLAMA_NETWORK_WORKER_CONFIG  Optional explicit path to a worker config JSON file.
echo   OLLAMA_NETWORK_SERVER_URL      Optional coordinator URL override.
echo   OLLAMA_NETWORK_WORKER_TOKEN    Optional long-lived worker token override.
echo.
echo If you only want the worker daemon on a remote PC, use start_llm_network_worker_v0_1_1.bat instead.
echo.
echo If no config file is found, the daemon will tell you to download one from the dashboard.
exit /b 0
