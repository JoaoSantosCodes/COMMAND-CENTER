# Código Fonte - Pasta `src/`

Esta pasta contém todo o código-fonte modularizado do sistema ConsultaVD.

## Estrutura dos Módulos

- `src/database/`  - Conexão, queries e lógica de acesso ao banco de dados
- `src/editor/`    - Lógica de edição de dados, operações CRUD, auditoria
- `src/ui/`        - Componentes de interface, validação, responsividade, buscas guiadas
- `src/cache/`     - Implementação de cache/memória para otimizar consultas

## Boas práticas
- Use imports absolutos entre módulos, por exemplo:
  ```python
  from src.database.queries import minha_funcao
  from src.ui.components import meu_componente
  ```
- Cada subpasta possui um `__init__.py` para ser tratada como módulo Python.
- Separe funcionalidades por domínio para facilitar manutenção e testes.

## Expansão
Se o projeto crescer, adicione novos submódulos (ex: `src/api/`, `src/services/`) mantendo a organização.

---

Dúvidas? Consulte a documentação em `/docs` ou o arquivo `CONTRIBUTING.md` na raiz do projeto. 