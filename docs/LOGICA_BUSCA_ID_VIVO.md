# Lógica e Processo de Busca por ID Vivo (Unificada)

## Visão Geral
A busca por ID Vivo no sistema ConsultaVD permite localizar circuitos e exibir a(s) loja(s) associada(s) ao ID Vivo informado, integrando dados do inventário e cadastro de lojas.

---

## 1. Relacionamento entre Tabelas
- **inventario_planilha1**: contém os circuitos, campo `People` referencia a loja.
- **lojas_lojas**: cadastro das lojas, campo `PEOP` é a chave de relacionamento.
- O relacionamento é feito por: `inventario_planilha1.People = lojas_lojas.PEOP`.

---

## 2. Problemas Identificados
- Alguns circuitos referenciavam códigos de loja (`People`) inexistentes em `lojas_lojas`.
- O frontend esperava campos com nomes exatos (ex: `LOJAS`, `ENDEREÇO`, `TELEFONE1`), mas o backend retornava nomes diferentes (ex: `nome`, `endereco`).
- Quando o JOIN não encontrava a loja, os campos vinham nulos e a loja não era exibida.

---

## 3. Solução Implementada
- **Fallback no backend**: Se o JOIN não trouxer a loja, o backend faz uma busca manual na tabela de lojas usando o campo `People/PEOP`.
- **Padronização dos campos**: O backend agora retorna os dados das lojas com os nomes de campos exatamente como o frontend espera:
  - `LOJAS`, `CODIGO`, `Status_Loja`, `ENDEREÇO`, `BAIRRO`, `CIDADE`, `UF`, `CEP`, `TELEFONE1`, `TELEFONE2`, `CELULAR`, `E_MAIL`, `VD NOVO`, `People/PEOP`, `STATUS`, `NOME_GGL`, `NOME_GR`
- **Diagnóstico de dados**: Caso a loja não exista, o sistema não exibe dados e recomenda ajuste no cadastro.

---

## 4. Fluxo da Busca por ID Vivo
1. O usuário informa o ID Vivo no frontend.
2. O frontend chama o endpoint `/api/search/id-vivo?id_vivo=...`.
3. O backend executa a query:
   - Busca circuitos por ID Vivo (`ID_VIVO` ou `Novo_ID_Vivo`).
   - Faz LEFT JOIN com lojas pelo campo `People/PEOP`.
   - Se a loja não for encontrada, faz busca manual pelo código.
   - Monta o dicionário da loja padronizando os campos.
4. O frontend exibe os dados completos da loja e do circuito.

---

## 5. Resultados
- Busca por ID Vivo agora exibe corretamente os dados completos da loja associada ao circuito/ID Vivo.
- Integração frontend-backend robusta e padronizada.
- Documentação e lógica registradas para futuras manutenções.

---

**Processo registrado em junho/2024.** 