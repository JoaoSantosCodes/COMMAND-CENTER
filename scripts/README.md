# Scripts Utilitários - ConsultaVD

Esta pasta contém scripts de automação, inicialização, testes e utilitários para o projeto ConsultaVD.

## Principais scripts

- **start_system.bat**  
  Inicia backend (FastAPI) e frontend (React) em janelas separadas.  
  _Uso:_  
  ```
  scripts\start_system.bat
  ```

- **start_backend.bat**  
  Inicia apenas o backend FastAPI.  
  _Uso:_  
  ```
  scripts\start_backend.bat
  ```

- **start_frontend.bat**  
  Inicia apenas o frontend React/TypeScript.  
  _Uso:_  
  ```
  scripts\start_frontend.bat
  ```

- **check_typescript.bat**  
  Verifica erros de digitação no frontend TypeScript.

- **test_system.bat**  
  Testa se backend e frontend estão rodando corretamente.

- **test_modular.py / test_imports.py**  
  Testes automatizados do sistema modular.

- **gerar_documentacao_pdf.sh / gerar_documentacao_pdf.bat**  
  Scripts para gerar documentação em PDF.

- **gerar_relatorio_estrutura.py, query_database.py, excel_to_sqlite.py**  
  Scripts utilitários para manipulação de dados e banco.

- **utils/**  
  Scripts utilitários menos usados diretamente (ex: `check_tables.py`).

## Observações

- Execute os scripts sempre a partir da raiz do projeto ou diretamente da pasta `scripts/`.
- Os scripts `.bat` são para Windows. Para Linux/Mac, use os scripts `.sh` equivalentes (quando disponíveis).
- Para rodar os testes automatizados, use:
  ```
  pytest
  ```

---

Dúvidas? Consulte o README principal do projeto ou a documentação em `/docs`. 