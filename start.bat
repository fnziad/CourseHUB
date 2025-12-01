@echo off
REM CourseHUB Startup Script for Windows

echo.
echo Starting CourseHUB...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env file with your database credentials before running again.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt

REM Start the application
echo.
echo All checks passed!
echo Starting Flask application...
echo Access at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
