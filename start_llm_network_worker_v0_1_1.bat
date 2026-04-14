@echo off
setlocal

cd /d "%~dp0"

if /I "%~1"=="help" goto :help
if /I "%~1"=="--help" goto :help
if /I "%~1"=="/?" goto :help

set "WORKER_CONFIG=%CD%\llm-network-worker.json"
if not exist "%WORKER_CONFIG%" if exist "%CD%\.runtime\worker.local.json" set "WORKER_CONFIG=%CD%\.runtime\worker.local.json"
if not exist "%WORKER_CONFIG%" (
  echo Missing llm-network-worker.json next to this launcher.
  echo Download the config from the dashboard and place it in the same folder.
  pause
  exit /b 1
)

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
  pause
  exit /b 1
)

echo LLM Network worker launcher v0.1.1
echo.
echo Starting worker daemon on this PC.
echo This launcher reads llm-network-worker.json or .runtime\worker.local.json next to it.
echo.

start "LLM Network Worker" cmd /k "cd /d ""%CD%"" && set PYTHONPATH=src && %PYTHON_CMD% -m ollama_network.worker_daemon --config ""%WORKER_CONFIG%"""
exit /b 0

:help
echo LLM Network worker launcher
echo.
echo Usage:
echo   %~nx0
echo.
echo What it does:
echo   1. Starts the worker daemon on this machine.
echo   2. Reads llm-network-worker.json or .runtime\worker.local.json automatically.
echo   3. Auto-detects local GPU, host RAM, and Ollama models.
echo   4. Registers the worker with the coordinator and starts polling for jobs.
echo.
echo Place this file next to llm-network-worker.json on the worker PC.
exit /b 0
