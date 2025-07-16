# Estrutura do Projeto ConsultaVD

Este documento descreve a estrutura de diretórios e arquivos do projeto ConsultaVD, explicando o propósito de cada parte para facilitar a navegação, manutenção e colaboração.

---

## Raiz do Projeto

```
ConsultaVD/
│
├── app_modular.py                # Entrada principal do sistema modularizado (Streamlit)
├── app_streamlit.py              # Versão anterior do app
├── app_streamlit_fixed.py        # Versão intermediária
├── config.py                     # Configurações globais do projeto
├── requirements.txt              # Dependências do projeto
├── README.md                     # Visão geral e instruções principais
├── CONTRIBUTING.md               # Guia para colaboradores
│
├── consulta_vd.db                # Banco de dados SQLite
├── Inventario.xlsx               # Planilha de inventário
├── Relação de Lojas.xlsx         # Planilha de lojas
├── test_modular.py               # Testes do sistema modular
│
├── docs/                         # Documentação detalhada do projeto
│   ├── README_MODULAR.md
│   ├── DOCUMENTACAO_BUSCA_GUIADA.md
│   ├── RESUMO_MODULARIZACAO.md
│   ├── DOCUMENTACAO_INFORMATIVOS.md
│   ├── REVISAO_CODIGO_2025.md
│   ├── RESUMO_MELHORIAS_2025.md
│   ├── GUIA_USO_EDICAO.md
│   ├── DOCUMENTACAO_DADOS.md
│   ├── RELATORIO_ESTRUTURA_DADOS.md
│   └── ESTRUTURA_PROJETO.md      # (este arquivo)
│
├── src/                          # Código-fonte principal
│   ├── __init__.py
│   ├── database/                  # Módulo de acesso e queries ao banco de dados
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── queries.py
│   ├── editor/                    # Lógica de edição, campos editáveis e auditoria
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── fields.py
│   │   ├── operations.py
│   ├── ui/                        # Componentes visuais, validação, responsividade
│   │   ├── __init__.py
│   │   ├── components.py
│   │   ├── stamps.py
│   │   ├── validation.py
│   │   ├── responsive.py
│   │   ├── guided_search/         # Fluxos de busca guiada
│   │   │   ├── __init__.py
│   │   │   ├── loja_operadora_circuito.py
│
├── tests/                        # Testes automatizados (pytest)
│   ├── test_imports.py
```

---

## Descrição dos principais diretórios e arquivos

- **app_modular.py**: Ponto de entrada principal do sistema modularizado com Streamlit.
- **src/database/**: Funções de conexão e queries SQL.
- **src/editor/**: Lógica de edição, campos editáveis e auditoria de alterações.
- **src/ui/**: Componentes de interface, validação, responsividade e fluxos de busca guiada.
  - **src/ui/guided_search/**: Cada fluxo guiado (ex: Loja > Operadora > Circuito) fica em seu próprio arquivo.
- **docs/**: Toda a documentação detalhada do projeto.
- **tests/**: Testes automatizados para garantir integridade dos módulos.
- **requirements.txt**: Lista de dependências do projeto.
- **README.md**: Visão geral, instruções de uso e links para documentação.
- **CONTRIBUTING.md**: Guia para colaboradores.

---

## Observações

- A estrutura modular facilita a manutenção, testes e expansão do sistema.
- Novos fluxos ou módulos podem ser adicionados facilmente seguindo o padrão existente.
- Toda a documentação está centralizada em `/docs` para fácil acesso.

---

Para dúvidas, consulte o README.md ou os arquivos em `/docs`. 