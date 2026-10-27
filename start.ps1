Write-Host "🌸 樱花庄 Sakurasou - 启动脚本" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

# 1. Start Backend Server
Write-Host "[1/2] 启动后端服务器 (Express)..." -ForegroundColor Cyan
$server = Start-Process -WindowStyle Hidden -FilePath "node" -ArgumentList "app.js" -WorkingDirectory "E:\sakurasou\server" -PassThru
Start-Sleep 2

# Check server health
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/api/health" -ErrorAction Stop
    Write-Host "  ✅ 后端服务器运行中 (http://localhost:3001)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 后端服务器启动失败" -ForegroundColor Red
    exit 1
}

# 2. Start Frontend Dev Server
Write-Host "[2/2] 启动前端开发服务器 (Nuxt)..." -ForegroundColor Cyan
Set-Location "E:\sakurasou\client"
$client = Start-Process -WindowStyle Hidden -FilePath "npx" -ArgumentList "nuxt", "dev", "--port", "3000" -WorkingDirectory "E:\sakurasou\client" -PassThru
Start-Sleep 5

Write-Host "  ✅ 前端开发服务器启动中 (http://localhost:3000)" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "🌸 樱花庄 已启动！" -ForegroundColor Magenta
Write-Host "   前端: http://localhost:3000" -ForegroundColor White
Write-Host "   后端: http://localhost:3001" -ForegroundColor White
Write-Host "   健康检查: http://localhost:3001/api/health" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "按任意键停止所有服务..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Cleanup
Write-Host "正在停止服务..." -ForegroundColor Yellow
Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $client.Id -Force -ErrorAction SilentlyContinue
Write-Host "已停止所有服务" -ForegroundColor Green
