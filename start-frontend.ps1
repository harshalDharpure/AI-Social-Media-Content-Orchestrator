# AI Social Media Content Orchestrator - Frontend Start Script

Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Green
Write-Host ""

# Navigate to frontend directory
Set-Location frontend

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Check if .env.local exists
if (-not (Test-Path ".env.local")) {
    Write-Host "⚠️  .env.local file not found. Creating one..." -ForegroundColor Yellow
    @"
VITE_API_URL=http://localhost:8000
"@ | Out-File -FilePath ".env.local" -Encoding UTF8
    Write-Host "✅ Created .env.local file." -ForegroundColor Green
}

# Start the development server
Write-Host ""
Write-Host "✅ Starting React development server on http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Vite
npm run dev

