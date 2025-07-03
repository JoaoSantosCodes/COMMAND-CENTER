# 🖼️ Pasta Assets - ConsultaVD

Esta pasta armazena os recursos visuais (assets) utilizados no sistema ConsultaVD, como logotipos e imagens institucionais.

## 📁 Conteúdo

### `logo.png`
- **Formato:** PNG
- **Tamanho:** 4.3KB
- **Uso:** Logotipo principal do sistema, utilizado em dashboards, cabeçalhos, splash screens e materiais de divulgação.
- **Vantagens:** Compatível com todos os navegadores e sistemas, ideal para fundos claros ou escuros.

### `logo.svg`
- **Formato:** SVG (vetorial)
- **Tamanho:** 1.0KB
- **Uso:** Logotipo vetorial para uso em interfaces responsivas, web, mobile e impressos.
- **Vantagens:** Escalável sem perda de qualidade, ideal para ícones, favicons e aplicações que exigem alta definição.

## 🎨 Boas Práticas de Uso
- Utilize o `logo.svg` sempre que possível para garantir qualidade em diferentes resoluções.
- Use o `logo.png` para compatibilidade máxima ou quando o SVG não for suportado.
- Não altere as proporções ou cores dos logos sem aprovação do design.
- Para novos assets, utilize nomes descritivos e formatos otimizados (preferencialmente SVG ou PNG comprimido).

## 📦 Integração com o Sistema
- Os assets são utilizados tanto no frontend (React) quanto no backend (ex: geração de relatórios).
- Referencie os arquivos via caminhos relativos, ex: `/assets/logo.svg`.
- Para uso em produção, garanta que os assets estejam incluídos no build final.

## 📝 Notas
- **Direitos autorais:** O uso dos logos é restrito ao sistema ConsultaVD e materiais oficiais.
- **Atualização:** Para atualizar um asset, substitua o arquivo mantendo o mesmo nome ou adicione uma nova versão com sufixo de data/versão.
- **Backup:** Mantenha sempre uma cópia dos arquivos originais em alta resolução.

---
*Última atualização: Janeiro 2025* 