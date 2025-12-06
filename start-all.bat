@echo off
echo ========================================
echo Physical AI Textbook - Complete Startup
echo ========================================
echo.
echo This will start BOTH frontend and backend
echo.
echo Starting frontend in new window...
start "Frontend - Docusaurus" cmd /k "cd frontend && npm start"

echo.
echo Waiting 5 seconds...
timeout /t 5 /nobreak > nul

echo.
echo Starting backend in new window...
start "Backend - FastAPI" cmd /k "cd backend && start.bat"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Check the new windows for server status.
echo.
pause
