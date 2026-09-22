# ENGENHARIA DE DESIGN SYSTEM & ESTÚDIO UI: FRONTCRAFT MASTER v2.0

Você é um Arquiteto de Software Frontend Sênior e Especialista em Design Systems, com sólida experiência em micro-interações, ergonomia mobile e acessibilidade web (WCAG 2.1 AA/AAA).

## 1. CONTEXTO
O "FrontCraft Master" é um estúdio web interativo projetado para construir, calibrar e exportar design tokens táteis (sombras em camadas, chanfros de 1px, relevos físicos no estilo Linear/Apple, paletas semânticas e ergonomia móvel via bottom navigation). 
Atualmente, as abas operam como módulos isolados: alterações em sombras ou cores não sincronizam com o gerador de prompts, a visualização limita-se a elementos atômicos isolados e o teste de contraste afere apenas o título contra o plano de fundo primário.

## 2. TAREFA (INSTRUÇÃO PRINCIPAL)
Refatore e implemente o núcleo do FrontCraft Master transformando-o em uma aplicação coesa, reativa e profissional. O sistema deve atender obrigatoriamente a quatro pilares arquiteturais:

1. **Camada de Estado Global e Reativo (Single Source of Truth):**
   - Centralize todos os seletores e sliders (cor primária, superfície, bordas, raio de arredondamento, elevação de sombra de 1px a 3 camadas e chanfro superior).
   - Qualquer mutação em tempo real deve refletir instantaneamente em:
     a) Tokens CSS ativos (`:root`);
     b) Mostruário de componentes;
     c) Cartão de teste composto;
     d) Motor do gerador de prompts contextuais;
     e) Exportador de código de configuração.

2. **Cartão de Teste Composto em Tempo Real ("Live Sandbox Card"):**
   - Substitua o mostruário de peças puramente isoladas por um componente contextual integrado e realista.
   - Forneça um alternador de modelo de dados para o card:
     * *Opção A (Prontuário/Clínico):* Card de triagem com status do paciente, badge de risco, métricas vitais e botão de ação primária.
     * *Opção B (Fintech/Transacional):* Card de fatura/saldo com gráfico sparkline, dados de transação e botão de transferência.
   - O card deve renderizar dinamicamente a paleta escolhida, o chanfro físico de 1px na borda superior, a sombra volumétrica calibrada e o estado ativo/clique do botão.

3. **Auditoria de Acessibilidade Multi-Nível (WCAG 2.1):**
   - Expanda o validador de contraste para além da relação `Texto Primário vs. Fundo`.
   - Implemente cálculo algorítmico exato de luminosidade relativa para quatro camadas simultâneas:
     * Contraste 1: Texto primário (título) sobre superfície (mínimo 4.5:1 - WCAG AA);
     * Contraste 2: Texto secundário/apoio (legendas e metadados cinzas) sobre superfície (mínimo 4.5:1 para AA / 7.0:1 para AAA);
     * Contraste 3: Bordas de inputs e caixas delimitadoras contra superfície (mínimo 3.0:1);
     * Contraste 4: Texto do botão de ação sobre a cor de destaque (accent).
   - Exiba badges visuais claros: "Aprovado AA", "Aprovado AAA" ou "Falha de Legibilidade sob Luz Solar".

4. **Motor Duplo de Exportação (Tokens & Prompt Contextual):**
   - **Aba Prompt:** O botão "Copiar Prompt" deve interpolar os valores exatos configurados nos sliders (ex: valores hexadecimais, box-shadow multicamada em CSS puro, classes de clamp e constraints semânticas). O prompt gerado deve ser pronto para alimentar LLMs na criação de telas completas com essas diretrizes de estilo.
   - **Aba Config:** Botão para download/cópia instantânea do arquivo `tailwind.config.js` completo e do bloco de variáveis CSS nativas (`:root { ... }`).

## 3. RESTRIÇÕES E DIRETRIZES TÉCNICAS
- **Zero Framework Bloat:** Implemente com código limpo, modular e de alto desempenho (Vanilla JS/TypeScript com Web Components OU React/Tailwind CSS conforme conveniência do projeto base).
- **Sem `alert()` ou diálogos bloqueantes:** Use feedback tátil e toasts customizados no canto inferior da viewport.
- **Mobile Ergonomics:** A barra de navegação inferior (Bottom Nav) deve manter alvos de toque mínimos de 48×48px e respeitar a `safe-area-inset-bottom`.
- **Validação Numérica Rígida:** Não arredonde cálculos de contraste WCAG arbitrariamente; aplique a fórmula oficial de luminância $L = 0.2126R + 0.7152G + 0.0722B$ após linearização dos canais sRGB.
- **Responsividade Flexível:** Proibido o uso de larguras fixas em pixels (`width: 420px`) que provoquem rolagem horizontal no celular; utilize `w-full max-w-md` ou unidades relativas (`clamp()`, `rem`).

## 4. FORMATO DE SAÍDA
Entregue a solução estruturada nas seguintes etapas:
1. **Módulo de Estado e Sincronização:** Arquitetura do store reativo que amarra controles, CSS e saídas de texto.
2. **Módulo do Validador de Acessibilidade:** Função matemática pura e determinística em TypeScript/JavaScript para cálculo de contraste e classificação WCAG multi-nível.
3. **Módulo do Card Vivo & Interface:** Estrutura HTML semântica com classes utilitárias e estilos das variáveis táteis (relevo, chanfro de 1px e sombra composta).
4. **Gerador Dinâmico de `tailwind.config.js` e Prompt:** Template literal que compila os valores do estado em código exportável.

## 5. ANTI-PADRÕES PROIBIDOS
- NUNCA isolar o formulário do preview (a experiência precisa ser de manipulação direta, sem botão de "Salvar" ou "Atualizar").
- NUNCA assumir que o texto cinza secundário tem contraste suficiente sem calcular o canal relativo.
- NUNCA gerar código com magic numbers de espaçamento; use a escala rem / escala 4 do Tailwind.
- NUNCA usar sombras duras e sem física; o relevo deve combinar sombra difusa ambiente + sombra de oclusão de contato + chanfro claro de 1px no topo.