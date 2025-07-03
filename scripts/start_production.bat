@echo off
cd /d %~dp0..
echo ========================================
echo    CONSULTAVD v2.0 - PRODUCAO
echo ========================================
echo.

echo Verificando dependencias...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo Iniciando Backend FastAPI em modo producao...
start "Backend FastAPI - Producao" cmd /k "cd /d %cd% && python -m uvicorn api_backend:app --host 0.0.0.0 --port 8000"
echo Backend iniciado em: http://localhost:8000
echo.

echo Aguardando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo Iniciando Frontend em modo producao...
start "Frontend React - Producao" cmd /k "cd consultavd-frontend && npm start"
echo Frontend sera iniciado em: http://localhost:3000
echo.

echo ========================================
echo SISTEMA EM PRODUCAO INICIADO!
echo ========================================
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo - API Docs: http://localhost:8000/docs
echo - Health Check: http://localhost:8000/api/health
echo.
echo Para parar o sistema, feche as janelas dos servidores.
echo.
pause
