@echo off
title Meeting Recorder

cd /d "%~dp0"

echo ================================
echo   Meeting Recorder
echo   Close this window to stop.
echo ================================
echo.
echo Starting server, please wait...
echo.

start /b "" cmd /c "ping -n 5 127.0.0.1 >nul && start http://127.0.0.1:8000"

".venv\Scripts\python.exe" main.py

echo.
echo Server stopped.
pause
