@echo off
setlocal

cd /d "%~dp0"

echo Starting Nova Studio development server...
if exist node_modules (
  start "Nova Studio Dev Server" cmd /k "npm run dev -- --host 127.0.0.1 --port 5173 --strictPort"
  timeout /t 3 /nobreak >nul
  start "" "http://127.0.0.1:5173/Nova.Studio/"
) else (
  echo.
  echo Dependencies are missing. Run npm install first.
  pause
)

endlocal
