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

set "SERVER_URL=%OLLAMA_NETWORK_SERVER_URL%"
if not defined SERVER_URL set "SERVER_URL=https://llm-network.websitesolutions.shop"

set "WORKER_ID=%OLLAMA_NETWORK_WORKER_ID%"
if not defined WORKER_ID set "WORKER_ID=worker-%COMPUTERNAME%"

echo.
echo Starting worker launcher on this PC.
echo Worker ID: %WORKER_ID%
echo Server URL: %SERVER_URL%
echo The launcher will auto-detect this PC's GPU, RAM, and local Ollama models.
echo On first run it will save the worker settings to .runtime\worker.local.json.
echo.

start "LLM Network Worker" cmd /k "cd /d ""%CD%"" && set PYTHONPATH=src && %PYTHON_CMD% -m ollama_network.worker_bootstrap --server-url ""%SERVER_URL%"" --worker-id ""%WORKER_ID%"""
exit /b 0

:help
echo LLM Network worker launcher
echo.
echo Usage:
echo   %~nx0
echo.
echo What it does:
echo   1. Starts a worker launcher on this machine.
echo   2. Auto-detects local GPU, host RAM, and Ollama models.
echo   3. Saves the worker profile locally after the first run.
echo   4. Registers the worker with the coordinator and starts polling for jobs.
echo.
echo Environment variables:
echo   OLLAMA_NETWORK_SERVER_URL    Coordinator URL. Defaults to https://llm-network.websitesolutions.shop
echo   OLLAMA_NETWORK_WORKER_ID     Worker identifier. Defaults to worker-%%COMPUTERNAME%%
echo   OLLAMA_NETWORK_OWNER_USER_ID Owner network user id. Saved in .runtime\worker.local.json after setup.
echo   OLLAMA_NETWORK_WORKER_TOKEN  Long-lived worker token. Saved in .runtime\worker.local.json after setup.
echo.
echo The launcher prompts only on first run when the local worker profile has not been saved yet.
exit /b 0
