@echo off
title Push to GitHub
color 0B
echo.
echo ========================================
echo   PUSH CODE TO GITHUB
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Go to: https://git-scm.com/download/win
    echo 2. Download and install Git
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Git is installed!
echo.

echo Initializing Git repository...
if not exist ".git" (
    git init
)

echo.
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/chingchanghaunji-bit/MONET-PARTY.git
echo.

echo Adding all files...
git add .
echo.

echo Committing changes...
git commit -m "Initial commit: Party Entry System with modern UI"
echo.

echo Pushing to GitHub...
echo.
echo NOTE: You will be prompted for GitHub credentials
echo       Use your username and Personal Access Token (not password)
echo.
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Possible reasons:
    echo 1. Wrong credentials
    echo 2. Repository doesn't exist
    echo 3. No internet connection
    echo.
    echo For Personal Access Token:
    echo GitHub -^> Settings -^> Developer settings -^> Personal access tokens
    echo.
) else (
    echo.
    echo ========================================
    echo   SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Repository: https://github.com/chingchanghaunji-bit/MONET-PARTY
    echo.
    echo Next steps:
    echo 1. Go to a hosting service (Render.com, Railway.app, etc.)
    echo 2. Connect your GitHub repository
    echo 3. Deploy!
    echo.
)

pause

