# AI Social Media Content Orchestrator - Backend Start Script

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
Write-Host ""

# Navigate to backend directory
Set-Location backend

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated. Activating..." -ForegroundColor Yellow
    if (Test-Path "venv\Scripts\Activate.ps1") {
        .\venv\Scripts\Activate.ps1
    } else {
        Write-Host "❌ Virtual environment not found. Please create one first:" -ForegroundColor Red
        Write-Host "   python -m venv venv" -ForegroundColor Cyan
        Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
        exit 1
    }
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating a basic one..." -ForegroundColor Yellow
    @"
# Server
PORT=8000
ENVIRONMENT=development

# LLM APIs (at least one is required)
# Add your API key here:
OPENAI_API_KEY=
# ANTHROPIC_API_KEY=
# GOOGLE_API_KEY=

# Vector Database (optional)
USE_PINECONE=false
QDRANT_URL=http://localhost:6333

# Security
SECRET_KEY=development-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file. Please add your API keys!" -ForegroundColor Green
}

# Check if uvicorn is installed
try {
    python -c "import uvicorn" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Installing uvicorn..." -ForegroundColor Yellow
        pip install uvicorn[standard]
    }
} catch {
    Write-Host "📦 Installing uvicorn..." -ForegroundColor Yellow
    pip install uvicorn[standard]
}

# Start the server
Write-Host ""
Write-Host "✅ Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "📍 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "📍 Health Check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn (correct spelling!)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

