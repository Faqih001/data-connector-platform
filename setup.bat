@echo off
REM Data Connector Platform - Automated Setup Script (Windows)
REM Runs all necessary setup steps for the project

setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   Data Connector Platform - Complete Setup Script              ║
echo ║   This will install dependencies and set up demo data          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check for Node.js
echo [Step 1] Checking Prerequisites...
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo OK: Node.js %NODE_VERSION% found

REM Check for Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo OK: %PYTHON_VERSION% found
echo.

REM Get project directory
set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"

echo Project directory: %PROJECT_ROOT%
echo.

REM Step 2: Install Node dependencies
echo [Step 2] Installing Node.js Dependencies...
if not exist "%PROJECT_ROOT%node_modules" (
    cd /d "%PROJECT_ROOT%"
    call npm install
    echo OK: Node dependencies installed
) else (
    echo OK: Node dependencies already installed
)
echo.

REM Step 3: Setup Python virtual environment
echo [Step 3] Setting up Python Virtual Environment...
cd /d "%BACKEND_DIR%"

if not exist ".venv" (
    call python -m venv .venv
    echo OK: Virtual environment created
) else (
    echo OK: Virtual environment already exists
)
echo.

REM Step 4: Activate virtual environment and install dependencies
echo [Step 4] Installing Python Dependencies...
call .venv\Scripts\activate.bat
call pip install -q -r requirements.txt
echo OK: Python dependencies installed
echo.

REM Step 5: Run Django migrations
echo [Step 5] Running Database Migrations...
call python manage.py migrate --noinput
echo OK: Database migrations completed
echo.

REM Step 6: Create admin user
echo [Step 6] Setting up Admin User...
call python reset_admin.py
echo OK: Admin user configured
echo.

REM Step 7: Setup demo users
echo [Step 7] Creating Demo Users...
call python setup_demo_users.py
echo OK: Demo users created
echo.

REM Step 8: Populate demo data
echo [Step 8] Populating Demo Data...
if exist "populate_demo_data.py" (
    call python populate_demo_data.py
    echo OK: Demo data populated
) else (
    echo WARNING: Demo data script not found, skipping
)
echo.

REM Summary
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   ✓ Setup Complete!                                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Next Steps:
echo.
echo 1. Start the backend:
echo    - Open Command Prompt or PowerShell
echo    - Navigate to: %BACKEND_DIR%
echo    - Run: .venv\Scripts\activate.bat
echo    - Run: python manage.py runserver 0.0.0.0:8001
echo.
echo 2. Start the frontend (in a new Command Prompt/PowerShell):
echo    - Navigate to: %PROJECT_ROOT%
echo    - Run: npm run dev
echo.
echo 3. Open your browser:
echo    - http://localhost:3000
echo.
echo Demo Credentials:
echo   User: admin          Password: admin123       (Admin)
echo   User: john_sales     Password: john123
echo   User: sarah_analytics Password: sarah456
echo   User: mike_reporting Password: mike789
echo.
echo Happy coding! 🚀
echo.
pause
