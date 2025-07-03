@echo off
cd /d %~dp0..
echo ========================================
echo    CONSULTAVD v2.0 - React/TypeScript
echo ========================================
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

REM Verificar se o Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado! Instale o Node.js primeiro.
    pause
    exit /b 1
)

echo Verificando dependencias do backend...
if not exist "requirements.txt" (
    echo ERRO: requirements.txt nao encontrado!
    pause
    exit /b 1
)
REM Instalar dependencias do backend se necessario
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias do backend...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias do backend!
        pause
        exit /b 1
    )
)

echo Verificando dependencias do frontend...
if not exist "consultavd-frontend\package.json" (
    echo ERRO: package.json nao encontrado no frontend!
    pause
    exit /b 1
)
REM Instalar dependencias do frontend se necessario
if not exist "consultavd-frontend\node_modules" (
    echo Instalando dependencias do frontend...
    cd consultavd-frontend
    npm install
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias do frontend!
        echo Tente executar manualmente: cd consultavd-frontend ^&^& npm install
        pause
        exit /b 1
    )
    cd ..
)

echo.
echo Iniciando Backend FastAPI...
start "Backend FastAPI" cmd /k "cd /d %cd% && python -m uvicorn api_backend:app --host 0.0.0.0 --port 8000 --reload"
echo Backend iniciado em: http://localhost:8000
echo.

echo Aguardando 5 segundos para o backend inicializar...
timeout /t 5 /nobreak >nul
echo.

echo Iniciando Frontend React...
start "Frontend React" cmd /k "cd consultavd-frontend && npm start"
echo Frontend sera iniciado em: http://localhost:3000
echo.

echo ========================================
echo Sistema iniciado com sucesso!
echo ========================================
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo - Documentacao API: http://localhost:8000/docs
echo - Health Check: http://localhost:8000/api/health
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul 