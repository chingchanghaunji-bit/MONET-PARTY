@echo off
title Party Entry System Server
color 0A
echo.
echo ========================================
echo   PARTY ENTRY SYSTEM - STARTING SERVER
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment!
    echo Make sure venv folder exists.
    pause
    exit /b 1
)

echo [2/3] Checking Python...
python --version
echo.

echo [3/3] Starting Flask server...
echo.
echo ========================================
echo   SERVER STARTING...
echo ========================================
echo.
echo   Open your browser and go to:
echo   http://localhost:5000
echo.
echo   Admin Login:
echo   http://localhost:5000/admin/login
echo   Username: admin
echo   Password: admin123
echo.
echo ========================================
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause


