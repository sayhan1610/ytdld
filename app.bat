@echo off
title YouTube MP3 Downloader
echo ===========================
echo  YouTube MP3 Downloader
echo ===========================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+ first.
    pause
    exit /b
)

:: Check dependencies
echo Installing dependencies (if not already installed)...
pip install -r requirements.txt >nul

:: Run script
echo.
echo Starting downloads...
echo.
python dl.py --list list.txt --out downloads --workers 4

echo.
echo ===========================
echo  All tasks completed!
echo ===========================
pause
