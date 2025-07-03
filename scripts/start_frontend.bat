@echo off
cd /d %~dp0..
cd /d %~dp0..\consultavd-frontend

node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado!
    pause
    exit /b 1
)
if not exist "node_modules" (
    echo Instalando dependencias...
    call npm install
)
echo Iniciando servidor de desenvolvimento...
call npm start
pause 