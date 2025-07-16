# AMS-DB Service Startup Script
# This script starts the necessary services for full AMS-DB functionality

Write-Host "🚀 Starting AMS-DB Services..." -ForegroundColor Green

# Check if Docker Desktop is running
$dockerProcess = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
if (-not $dockerProcess) {
    Write-Host "⚠️  Docker Desktop is not running. Please start Docker Desktop first." -ForegroundColor Yellow
    Write-Host "   You can start it from the Windows Start menu or by running 'Docker Desktop.exe'" -ForegroundColor Yellow
    exit 1
}

# Start Neo4j
Write-Host "📊 Starting Neo4j database..." -ForegroundColor Cyan
docker run -d `
    --name ams-neo4j `
    -p 7474:7474 -p 7687:7687 `
    -e NEO4J_AUTH=neo4j/password `
    -v ams-neo4j-data:/data `
    neo4j:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Neo4j started successfully on http://localhost:7474" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to start Neo4j. Trying to start existing container..." -ForegroundColor Red
    docker start ams-neo4j
}

# Check if Ollama is running
Write-Host "🤖 Checking Ollama status..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Ollama is already running on http://localhost:11434" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Ollama is not running. Please start it manually:" -ForegroundColor Yellow
    Write-Host "   Run: ollama serve" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Service startup complete!" -ForegroundColor Green
Write-Host "📋 Service Status:" -ForegroundColor Cyan
Write-Host "   - Neo4j:  http://localhost:7474 (username: neo4j, password: password)" -ForegroundColor White
Write-Host "   - Ollama: http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "💬 You can now use full AI-powered chat with:" -ForegroundColor Green
Write-Host "   ams-db chat send <alias> 'your message'" -ForegroundColor White
