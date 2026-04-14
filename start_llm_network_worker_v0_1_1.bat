@echo off
setlocal

cd /d "%~dp0"

echo LLM Network worker launcher v0.1.1
echo.
echo This versioned launcher starts the current config-first worker daemon.
echo If this PC still has an older worker install, run repair_worker_install_v0_1_1.bat first.
echo.

call "%~dp0start_worker_daemon.bat"
exit /b %errorlevel%
