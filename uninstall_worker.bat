@echo off
setlocal

cd /d "%~dp0"

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
echo Removing the installed ollama-network package and old worker launchers.
echo.

%PYTHON_CMD% -m pip uninstall -y ollama-network

for /f "usebackq delims=" %%S in (`%PYTHON_CMD% -c "import sysconfig; print(sysconfig.get_path('scripts'))"`) do set "SCRIPTS_DIR=%%S"
if defined SCRIPTS_DIR (
  if exist "%SCRIPTS_DIR%\ollama-network-worker-launch.exe" del /f /q "%SCRIPTS_DIR%\ollama-network-worker-launch.exe"
  if exist "%SCRIPTS_DIR%\ollama-network-worker.exe" del /f /q "%SCRIPTS_DIR%\ollama-network-worker.exe"
  if exist "%SCRIPTS_DIR%\ollama-network-worker-launch-script.py" del /f /q "%SCRIPTS_DIR%\ollama-network-worker-launch-script.py"
  if exist "%SCRIPTS_DIR%\ollama-network-worker-script.py" del /f /q "%SCRIPTS_DIR%\ollama-network-worker-script.py"
)

echo.
echo Uninstall complete.
echo If you want to reinstall the current version from GitHub, run repair_worker_install.bat.
exit /b 0
