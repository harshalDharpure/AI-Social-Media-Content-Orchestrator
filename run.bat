@echo off
REM AI Social Media Content Orchestrator - Run Script (Windows)

echo 🚀 Starting AI Social Media Content Orchestrator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    exit /b 1
)

REM Start backend
echo 📦 Starting Backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\.installed" (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    type nul > venv\.installed
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Created .env file. Please update it with your API keys.
    )
)

REM Start backend in background
echo Starting FastAPI server on http://localhost:8000
start "Backend Server" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo.
echo 🎨 Starting Frontend...
cd frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo ⚠️  Warning: .env.local file not found. Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env.local
        echo ✅ Created .env.local file.
    )
)

REM Start frontend
echo Starting React development server on http://localhost:3000
start "Frontend Server" cmd /k "npm run dev"
cd ..

echo.
echo ✅ Application started!
echo.
echo 📍 Backend API: http://localhost:8000
echo 📍 Frontend: http://localhost:3000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo Close the command windows to stop the servers.

pause

