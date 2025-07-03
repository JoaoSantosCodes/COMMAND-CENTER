# Testes Automatizados - ConsultaVD

Esta pasta contém os testes automatizados do sistema ConsultaVD.

## Estrutura

- `test_cache.py`         - Testes para o sistema de cache/memória
- `test_database.py`      - Testes para operações e queries no banco de dados
- `test_editor.py`        - Testes para funcionalidades de edição de dados
- `test_imports.py`       - Testa se todos os módulos principais podem ser importados sem erro
- `test_integration.py`   - Testes de integração entre diferentes partes do sistema
- `test_ui.py`            - Testes para componentes de interface

## Como rodar os testes

### Usando pytest (recomendado)
```bash
pytest tests/
```

### Usando unittest
```bash
python -m unittest discover -s tests
```

## Boas práticas
- Sempre nomeie os arquivos como `test_*.py`.
- Separe testes por domínio (cache, database, editor, etc).
- Adicione novos testes para cada nova funcionalidade implementada.
- Mantenha os testes atualizados conforme o sistema evolui.

---

Dúvidas? Consulte o arquivo `CONTRIBUTING.md` na raiz do projeto. 