#!/bin/bash
cd "$(dirname "$0")/.."
# Gera PDF da documentação principal do ConsultaVD
# Requer pandoc instalado (sudo apt install pandoc texlive-xetex)

OUTPUT="ConsultaVD_Documentacao.pdf"
FILES="docs/INDICE_DOCUMENTACAO_ATUALIZADO.md docs/ESTRUTURA_PROJETO_ATUALIZADA.md docs/FLUXOGRAMA_SISTEMA.md docs/ROADMAP_2025.md"

if ! command -v pandoc &> /dev/null; then
    echo "[ERRO] Pandoc não encontrado. Instale com: sudo apt install pandoc texlive-xetex"
    exit 1
fi

pandoc $FILES -o $OUTPUT --toc --pdf-engine=xelatex
if [ $? -eq 0 ]; then
    echo "[OK] PDF gerado: $OUTPUT"
else
    echo "[ERRO] Falha ao gerar PDF."
fi 