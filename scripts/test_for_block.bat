@echo off
REM Teste do bloco FOR para matar processo na porta 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Encontrado PID: %%a
    taskkill /PID %%a /F
)
pause 