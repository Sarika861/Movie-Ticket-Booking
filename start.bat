@echo off
REM CineMax Theater - Movie Ticket Booking System Startup Script

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   🎬 CINEMAX THEATER - BOOKING SYSTEM 🎬  ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7 or later
    pause
    exit /b 1
)

REM Run setup if needed
if not exist "data\" (
    echo 📦 First time setup...
    python setup.py
    if errorlevel 1 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Starting the application...
echo.
echo 🎫 Opening http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
pause

