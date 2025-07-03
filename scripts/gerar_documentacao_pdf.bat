@echo off
cd /d %~dp0..
REM Gera PDF da documentação principal do ConsultaVD
REM Requer pandoc instalado (https://pandoc.org/installing.html)

setlocal
set OUTPUT=ConsultaVD_Documentacao.pdf
set FILES=docs/INDICE_DOCUMENTACAO_ATUALIZADO.md docs/ESTRUTURA_PROJETO_ATUALIZADA.md docs/FLUXOGRAMA_SISTEMA.md docs/ROADMAP_2025.md

if not exist %SystemRoot%\System32\pandoc.exe (
    echo [ERRO] Pandoc não encontrado. Instale com: choco install pandoc
    exit /b 1
)

pandoc %FILES% -o %OUTPUT% --toc --pdf-engine=xelatex
if %ERRORLEVEL%==0 (
    echo [OK] PDF gerado: %OUTPUT%
) else (
    echo [ERRO] Falha ao gerar PDF.
)
endlocal 