# 🎯 Guia de Uso - Sistema de Edição VD

## 🚀 Como Acessar

1. **Execute o aplicativo:**
   ```bash
   python -m streamlit run app_streamlit_fixed.py
   ```

2. **Acesse no navegador:**
   - URL: `http://localhost:8504` (ou porta indicada)
   - Use a versão `app_streamlit_fixed.py` (versão corrigida)

## ✏️ Como Usar a Edição de Dados

### **Passo a Passo:**

1. **Acesse "Edição de Dados"** no sidebar
2. **Selecione a tabela:**
   - `lojas_lojas` - Para editar dados das lojas
   - `inventario_planilha1` - Para editar dados do inventário
3. **Escolha o registro** pelo ID (People/PEOP)
4. **Edite os campos** desejados
5. **Clique em "💾 Salvar Alterações"**
6. **Confirme o sucesso** da operação

### **Campos Editáveis:**

#### **Tabela `lojas_lojas`:**
- LOJAS, ENDEREÇO, BAIRRO, CIDADE, UF, CEP
- TELEFONE1, TELEFONE2, CELULAR, E_MAIL
- 2ª_a_6ª, SAB, DOM, FUNC.
- VD_NOVO, NOME_GGL, NOME_GR

#### **Tabela `inventario_planilha1`:**
- Status_Loja, Operadora
- ID_VIVO, Novo_ID_Vivo
- Circuito_Designação, Novo_Circuito_Designação

## 🔍 Exemplo Prático

### **Cenário:** Corrigir endereço de uma loja

1. **Buscar o People/PEOP** na "Busca Unificada"
2. **Identificar** que o endereço está incorreto
3. **Ir para "Edição de Dados"**
4. **Selecionar tabela:** `lojas_lojas`
5. **Escolher o PEOP** da loja
6. **Editar o campo "ENDEREÇO"**
7. **Salvar alterações**
8. **Verificar** se foi salvo corretamente

## ⚠️ Observações Importantes

### **Segurança:**
- ✅ **Backup recomendado** antes de edições em massa
- ✅ **Validação manual** de dados críticos
- ✅ **Teste em ambiente de desenvolvimento** primeiro

### **Limitações:**
- ⚠️ **Logs de alterações** não implementados
- ⚠️ **Histórico de mudanças** não disponível
- ⚠️ **Validação de tipos** básica

## 🛠️ Troubleshooting

### **Problema:** "Erro ao atualizar"
- **Solução:** Verificar se o campo existe na tabela
- **Solução:** Verificar se o ID (People/PEOP) está correto

### **Problema:** "Campo não editável"
- **Solução:** Verificar se a tabela suporta edição
- **Solução:** Verificar se o campo está na lista de editáveis

### **Problema:** "Streamlit não reconhecido"
- **Solução:** Usar `python -m streamlit run app_streamlit_fixed.py`

## 📊 Verificação de Alterações

### **Antes de editar:**
1. Anote o valor original
2. Faça backup se necessário
3. Teste com um registro não crítico

### **Após editar:**
1. Verifique a mensagem de sucesso
2. Confirme na visualização da tabela
3. Teste a busca unificada para verificar

## 🎯 Dicas de Uso

### **Eficiência:**
- Use a **Busca Unificada** para encontrar registros
- **Copie o People/PEOP** para usar na edição
- **Edite múltiplos campos** de uma vez

### **Segurança:**
- **Faça backup** regular do banco
- **Teste alterações** em dados de exemplo
- **Valide resultados** após edições

## 📞 Suporte

### **Se encontrar problemas:**
1. Verifique os logs do Streamlit
2. Teste com dados de exemplo
3. Verifique a estrutura do banco
4. Consulte a documentação técnica

---

**🎉 Sistema de Edição VD - Funcional e Pronto para Uso!** 