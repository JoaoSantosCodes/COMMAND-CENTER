@echo off
REM --- Finalizar processo na porta 8000, se houver ---
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Finalizando processo na porta 8000 (PID=%%a)...
    taskkill /PID %%a /F >nul 2>&1
)
REM --- Fim da finalização ---
cd /d %~dp0..

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo ERRO: requirements.txt nao encontrado!
    pause
    exit /b 1
)
echo Backend estara disponivel em: http://localhost:8000
echo Documentacao: http://localhost:8000/docs
python -m uvicorn api_backend:app --host 0.0.0.0 --port 8000 --reload
pause 