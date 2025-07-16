# README - Arquitetura Modular ConsultaVD

> **Nota:** Toda a documentação detalhada do projeto está centralizada na pasta [`/docs`](docs/).

## Suporte a Tema Claro/Escuro

- O frontend React/Material-UI possui alternância de tema claro/escuro via ThemeProvider customizado (`src/ThemeProvider.tsx`).
- Todos os componentes devem usar as cores do tema (`theme.palette.background.paper`, `theme.palette.text.primary`, etc) para garantir contraste e acessibilidade.
- Para novos componentes, evite cores fixas e utilize sempre o hook `useTheme()` do Material-UI.

## Estrutura Modular

O projeto ConsultaVD está organizado em módulos separados por domínio de responsabilidade:

- **src/database/**: Conexão e queries SQL.
- **src/editor/**: Lógica de edição, campos editáveis e auditoria.
- **src/ui/**: Componentes visuais, validação, responsividade e buscas guiadas.
  - **src/ui/guided_search/**: Fluxos de busca guiada (ex: Loja > Operadora > Circuito).

## Boas práticas

- Imports absolutos entre módulos (ex: `from src.ui import ...`).
- Cada diretório de módulo possui um `__init__.py`.
- Funções de interface separadas das utilitárias.
- Documentação separada por tema.

## Como rodar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Execute o app modular:
   ```
   python -m streamlit run app_modular.py
   ```

## Fluxos principais

- Dashboard
- Busca unificada
- Busca guiada: Loja > Operadora > Circuito (e outros fluxos futuros)
- Edição e auditoria de dados
- Exportação de resultados
- Interface responsiva

Consulte os arquivos de documentação em [`/docs`](docs/) para detalhes de cada fluxo. 