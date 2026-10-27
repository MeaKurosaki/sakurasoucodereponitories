@echo off
chcp 65001 >nul
echo.
echo 🌸 樱花庄 Sakurasou - 启动脚本
echo ========================================

echo [1/2] 启动后端服务器 (Express)...
start "sakurasou-server" /min cmd /c "cd /d E:\sakurasou\server && node app.js"
timeout /t 3 /nobreak >nul
echo   ✅ 后端启动完成 (http://localhost:3001)

echo [2/2] 启动前端开发服务器 (Nuxt)...
echo   ⏳ 首次启动需要编译，请耐心等待...
start "sakurasou-client" /min cmd /c "cd /d E:\sakurasou\client && npx nuxt dev --port 3000"
timeout /t 8 /nobreak >nul

echo.
echo ========================================
echo 🌸 樱花庄 已启动！
echo    前端: http://localhost:3000
echo    后端: http://localhost:3001
echo ========================================
echo.
echo 关闭此窗口不会停止服务，
echo 如需停止请打开任务管理器结束 node.exe
echo.
pause
