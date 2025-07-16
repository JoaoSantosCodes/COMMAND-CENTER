@echo off
cd /d %~dp0..
echo ========================================
echo    CONSULTAVD v2.0 - DEPLOY PRODUCAO
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

echo Instalando dependencias do backend...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias do backend!
    pause
    exit /b 1
)

echo Verificando dependencias do frontend...
if not exist "consultavd-frontend\package.json" (
    echo ERRO: package.json nao encontrado no frontend!
    pause
    exit /b 1
)

echo Instalando dependencias do frontend...
cd consultavd-frontend
npm install
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias do frontend!
    pause
    exit /b 1
)

echo Gerando build de producao do frontend...
npm run build
if errorlevel 1 (
    echo ERRO: Falha ao gerar build do frontend!
    pause
    exit /b 1
)

cd ..

echo.
echo Criando diretorios necessarios...
if not exist "logs" mkdir logs
if not exist "data\backup" mkdir data\backup
if not exist "production" mkdir production

echo.
echo Copiando arquivos para producao...
xcopy "consultavd-frontend\build\*" "production\" /E /I /Y

echo.
echo Configurando servidor de producao...
echo @echo off > production\start_production.bat
echo cd /d %%~dp0 >> production\start_production.bat
echo echo Iniciando ConsultaVD em modo producao... >> production\start_production.bat
echo start "Backend FastAPI" cmd /k "cd /d %cd% && python -m uvicorn api_backend:app --host 0.0.0.0 --port 8000" >> production\start_production.bat
echo timeout /t 3 /nobreak ^>nul >> production\start_production.bat
echo start "Frontend Production" cmd /k "cd /d %cd%\production && python -m http.server 80" >> production\start_production.bat
echo echo Sistema iniciado! >> production\start_production.bat
echo echo - Frontend: http://localhost >> production\start_production.bat
echo echo - Backend: http://localhost:8000 >> production\start_production.bat
echo pause >> production\start_production.bat

echo.
echo ========================================
echo DEPLOY PRODUCAO CONCLUIDO!
echo ========================================
echo.
echo Para iniciar o sistema em producao:
echo 1. cd production
echo 2. start_production.bat
echo.
echo URLs de acesso:
echo - Frontend: http://localhost
echo - Backend: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.
echo Pressione qualquer tecla para fechar...
pause >nul 