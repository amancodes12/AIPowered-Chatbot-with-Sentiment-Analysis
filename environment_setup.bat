@echo off
REM ============================================================
REM AI Chatbot Environment Setup Script (Windows)
REM Powered by Google Gemini Flash 2.5
REM ============================================================

echo ==============================================
echo   AI Chatbot - Environment Setup (Windows)
echo   Powered by Google Gemini Flash 2.5
echo ==============================================
echo.

REM Configuration
set VENV_NAME=venv

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo X Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo + Found Python: %%i
echo.

REM Navigate to script directory
cd /d "%~dp0"
echo + Working directory: %cd%
echo.

REM Check if virtual environment exists
if exist "%VENV_NAME%" (
    echo Warning: Virtual environment already exists.
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "%RECREATE%"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q %VENV_NAME%
    ) else (
        echo Using existing virtual environment.
    )
)

REM Create virtual environment if it doesn't exist
if not exist "%VENV_NAME%" (
    echo Creating virtual environment...
    python -m venv %VENV_NAME%
    echo + Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate.bat
echo + Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q
echo + pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q
echo + Dependencies installed
echo.

REM Check for API key in config
findstr /c:"<YOUR_GEMINI_API_KEY>" config.py >nul 2>&1
if not errorlevel 1 (
    echo ==============================================
    echo   IMPORTANT: API Key Configuration Required
    echo ==============================================
    echo.
    echo You need to set your Google Gemini API key.
    echo.
    echo Option 1: Edit config.py directly
    echo   Open config.py and replace ^<YOUR_GEMINI_API_KEY^> with your key
    echo.
    echo Option 2: Set environment variable
    echo   set GEMINI_API_KEY=your-api-key-here
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
)

echo ==============================================
echo   + Setup Complete!
echo ==============================================
echo.
echo To start the chatbot:
echo.
echo   1. Activate the virtual environment:
echo      %VENV_NAME%\Scripts\activate
echo.
echo   2. Run the application:
echo      python app.py
echo.
echo ==============================================
echo.

set /p RUN_APP="Would you like to start the chatbot now? (y/n): "
if /i "%RUN_APP%"=="y" (
    echo.
    echo Starting AI Chatbot...
    echo.
    python app.py
)

pause
