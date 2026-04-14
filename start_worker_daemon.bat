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

echo.
echo Starting worker daemon on this PC.
echo The daemon will read llm-network-worker.json or .runtime\worker.local.json if present.
echo It will auto-detect this PC's GPU, RAM, and local Ollama models.
echo.

start "LLM Network Worker" cmd /k "cd /d ""%CD%"" && set PYTHONPATH=src && %PYTHON_CMD% -m ollama_network.worker_daemon"
exit /b 0

:help
echo LLM Network worker launcher
echo.
echo Usage:
echo   %~nx0
echo.
echo What it does:
echo   1. Starts a worker daemon on this machine.
echo   2. Reads llm-network-worker.json or .runtime\worker.local.json automatically.
echo   3. Auto-detects local GPU, host RAM, and Ollama models.
echo   4. Registers the worker with the coordinator and starts polling for jobs.
echo.
echo Environment variables:
echo   OLLAMA_NETWORK_WORKER_CONFIG  Optional explicit path to a worker config JSON file.
echo   OLLAMA_NETWORK_SERVER_URL      Optional coordinator URL override.
echo   OLLAMA_NETWORK_WORKER_TOKEN    Optional long-lived worker token override.
echo.
echo If an older worker install is still on this PC, run uninstall_worker.bat first or use repair_worker_install.bat.
echo.
echo If no config file is found, the daemon will tell you to download one from the dashboard.
exit /b 0
