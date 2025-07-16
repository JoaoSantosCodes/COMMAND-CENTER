# 📦 Pasta /data - ConsultaVD

Esta pasta armazena os arquivos de dados essenciais para o funcionamento do sistema ConsultaVD, incluindo o banco de dados principal e planilhas de referência/importação.

## 📁 Conteúdo

### `consulta_vd.db`
- **Tipo:** Banco de dados SQLite
- **Propósito:** Armazena todas as informações do sistema (lojas, inventário, auditoria, etc.)
- **Uso:** Utilizado por toda a aplicação backend e scripts de integração
- **Backup:** Recomenda-se backup periódico deste arquivo. Para ambientes de produção, utilize dumps SQL ou cópias versionadas.
- **Restauração:** Para restaurar, basta substituir por um backup válido ou importar um dump SQL.

### `Inventario.xlsx`
- **Tipo:** Planilha Excel
- **Propósito:** Fonte de dados para importação inicial ou atualização em lote do inventário
- **Uso:** Utilizada por scripts de integração (ex: `scripts/excel_to_sqlite.py`)
- **Observação:** Mantenha a estrutura das colunas conforme esperado pelo sistema para evitar erros de importação.

### `Relação de Lojas.xlsx`
- **Tipo:** Planilha Excel
- **Propósito:** Fonte de dados para importação ou atualização da relação de lojas
- **Uso:** Utilizada para integração de dados, conferência e auditoria
- **Observação:** Atualize apenas com dados confiáveis e mantenha backups das versões anteriores.

## 🔄 Boas Práticas
- **Backup:** Realize backups regulares do banco de dados e das planilhas antes de qualquer importação ou atualização.
- **Versionamento:** Não versionar arquivos de dados sensíveis em repositórios públicos. Para ambientes de desenvolvimento, utilize dados fictícios ou anonimizados.
- **Importação:** Utilize sempre scripts validados para importar dados das planilhas para o banco de dados.
- **Auditoria:** Após grandes importações, verifique logs e relatórios para garantir a integridade dos dados.

## 🛠️ Scripts Relacionados
- `scripts/excel_to_sqlite.py` — Importa dados das planilhas para o banco SQLite
- `scripts/query_database.py` — Consulta dados do banco
- Outros scripts utilitários na pasta `scripts/`

## 📝 Notas
- **Privacidade:** Os arquivos podem conter dados sensíveis. Restrinja o acesso conforme a política da organização.
- **Integridade:** Não edite manualmente o banco de dados ou as planilhas sem conhecimento técnico.
- **Restauração:** Em caso de corrupção, utilize o backup mais recente ou solicite suporte ao administrador do sistema.

---
*Última atualização: Janeiro 2025* 