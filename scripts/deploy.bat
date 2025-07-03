@echo off
cd /d %~dp0..
echo ========================================
echo    CONSULTAVD v2.0 - DEPLOY PRODUCAO
echo ========================================
echo.

REM Verificar se o Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker nao encontrado! Instale o Docker primeiro.
    pause
    exit /b 1
)

REM Verificar se o Docker Compose está instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker Compose nao encontrado! Instale o Docker Compose primeiro.
    pause
    exit /b 1
)

echo Verificando arquivos necessarios...
if not exist "Dockerfile" (
    echo ERRO: Dockerfile nao encontrado!
    pause
    exit /b 1
)

if not exist "docker-compose.yml" (
    echo ERRO: docker-compose.yml nao encontrado!
    pause
    exit /b 1
)

if not exist "consultavd-frontend\Dockerfile" (
    echo ERRO: Dockerfile do frontend nao encontrado!
    pause
    exit /b 1
)

echo.
echo Criando diretorios necessarios...
if not exist "logs" mkdir logs
if not exist "data\backup" mkdir data\backup
if not exist "nginx" mkdir nginx

echo.
echo Parando containers existentes...
docker-compose down

echo.
echo Removendo imagens antigas...
docker-compose down --rmi all

echo.
echo Construindo imagens Docker...
docker-compose build --no-cache

if errorlevel 1 (
    echo ERRO: Falha ao construir imagens Docker!
    pause
    exit /b 1
)

echo.
echo Iniciando containers em modo de producao...
docker-compose up -d

if errorlevel 1 (
    echo ERRO: Falha ao iniciar containers!
    pause
    exit /b 1
)

echo.
echo Aguardando containers inicializarem...
timeout /t 10 /nobreak >nul

echo.
echo Verificando status dos containers...
docker-compose ps

echo.
echo ========================================
echo DEPLOY CONCLUIDO COM SUCESSO!
echo ========================================
echo - Frontend: http://localhost
echo - Backend: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo - Health Check: http://localhost:8000/api/health
echo.
echo Para verificar logs:
echo - docker-compose logs -f
echo.
echo Para parar o sistema:
echo - docker-compose down
echo.
echo Pressione qualquer tecla para fechar...
pause >nul 