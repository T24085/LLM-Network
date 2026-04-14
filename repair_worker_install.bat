@echo off
setlocal

cd /d "%~dp0"

set "APP_VERSION=0.1.1"
set "RELEASE_ZIP_URL=https://github.com/T24085/LLM-Network/archive/refs/tags/v%APP_VERSION%.zip"
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

call "%~dp0uninstall_worker.bat"
if errorlevel 1 exit /b 1

echo.
echo Reinstalling LLM Network v%APP_VERSION% from GitHub.
echo.

%PYTHON_CMD% -m pip install --upgrade --force-reinstall %RELEASE_ZIP_URL%
if errorlevel 1 exit /b 1

for /f "usebackq delims=" %%V in (`%PYTHON_CMD% -c "import importlib.metadata as m; print(m.version('ollama-network'))"`) do set "INSTALLED_VERSION=%%V"
echo Installed package version: %INSTALLED_VERSION%
if /I not "%INSTALLED_VERSION%"=="%APP_VERSION%" (
  echo Warning: installed version does not match expected v%APP_VERSION%.
)

echo.
echo Reinstall complete. Start the worker with start_worker_daemon.bat.
exit /b 0
