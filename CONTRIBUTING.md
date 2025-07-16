# Guia de Contribuição - ConsultaVD

Obrigado por contribuir com o ConsultaVD!

## Como contribuir

1. **Fork o repositório** e crie uma branch para sua feature/correção.
2. **Instale as dependências**:
   ```
   pip install -r requirements.txt
   ```
3. **Siga a estrutura de módulos**:
   - Coloque novas funcionalidades no módulo apropriado (`src/database`, `src/editor`, `src/ui`).
   - Use imports absolutos (ex: `from src.ui import ...`).
4. **Documente seu código** com docstrings e comentários claros.
5. **Adicione testes** para novas funcionalidades (use `test_modular.py` como referência).
6. **Atualize a documentação** se necessário.
7. **Abra um Pull Request** detalhando sua contribuição.

## Boas práticas
- Siga o padrão PEP8 para Python.
- Prefira funções pequenas e modulares.
- Não deixe código comentado ou "debug prints".
- Atualize o README.md e outros arquivos de documentação se necessário.

## Testes
- Execute `python test_modular.py` para garantir que tudo está funcionando.
- Se possível, adicione novos testes para cobrir sua feature/correção.

## Dúvidas ou problemas?
Abra uma issue ou entre em contato com o responsável pelo projeto.

---

Obrigado por ajudar a melhorar o ConsultaVD! 