# RedSec Dashboard - Start Script
Write-Host "🚀 Starting RedSec Dashboard..." -ForegroundColor Cyan

# Check if we're in the correct directory
if (-not (Test-Path ".\backend") -or -not (Test-Path ".\frontend")) {
    Write-Host "❌ Error: Please run this script from the redlab directory" -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Starting Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\activate; python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 3

Write-Host "🎨 Starting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Write-Host "`n✅ RedSec Dashboard is starting!" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n⚠️  Two new PowerShell windows will open for backend and frontend" -ForegroundColor Yellow
Write-Host "   Close those windows to stop the servers`n" -ForegroundColor Yellow
