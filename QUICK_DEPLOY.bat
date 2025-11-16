@echo off
title Quick Deploy Guide
color 0E
echo.
echo ========================================
echo   QUICK DEPLOYMENT CHECKLIST
echo ========================================
echo.

cd /d "%~dp0"

echo [1] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Git is NOT installed!
    echo.
    echo Please install Git first:
    echo 1. Go to: https://git-scm.com/download/win
    echo 2. Download and install
    echo 3. Restart computer
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Git is installed
    git --version
)

echo.
echo [2] Checking if code is on GitHub...
echo.
echo Opening GitHub repository in browser...
start https://github.com/chingchanghaunji-bit/MONET-PARTY

echo.
echo Please check:
echo - Do you see your files (app.py, templates/, etc.)?
echo - Or is the repository empty?
echo.
set /p github_status="Is your code on GitHub? (y/n): "

if /i "%github_status%"=="n" (
    echo.
    echo ========================================
    echo   PUSH CODE TO GITHUB FIRST
    echo ========================================
    echo.
    echo Run: PUSH_TO_GITHUB.bat
    echo OR follow manual steps in DEPLOY_INSTRUCTIONS.md
    echo.
    pause
    exit /b 1
)

echo.
echo [3] Deployment Options:
echo.
echo Option 1: Render.com (Recommended - Free)
echo   URL: https://render.com
echo.
echo Option 2: Railway.app (Free Tier)
echo   URL: https://railway.app
echo.
echo Opening deployment guides...
start https://render.com
timeout /t 2 >nul
start https://railway.app

echo.
echo ========================================
echo   NEXT STEPS
echo ========================================
echo.
echo 1. Sign up on Render.com or Railway.app
echo 2. Connect your GitHub account
echo 3. Select MONET-PARTY repository
echo 4. Add environment variables:
echo    - SECRET_KEY = (any random string)
echo    - ADMIN_USER = admin
echo    - ADMIN_PASS = (your password)
echo    - PORT = 5000
echo    - HOST = 0.0.0.0
echo 5. Deploy!
echo.
echo For detailed instructions, see: DEPLOY_INSTRUCTIONS.md
echo.
pause

