# RedSec Dashboard - Docker Compose Start Script
Write-Host "🐳 Starting RedSec Dashboard with Docker..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Building and starting containers..." -ForegroundColor Yellow
docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ RedSec Dashboard is running!" -ForegroundColor Green
    Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Cyan
    Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "`n📋 Useful commands:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs -f     # View logs" -ForegroundColor Gray
    Write-Host "   docker-compose down        # Stop services" -ForegroundColor Gray
    Write-Host "   docker-compose restart     # Restart services`n" -ForegroundColor Gray
} else {
    Write-Host "❌ Failed to start containers" -ForegroundColor Red
}
