# Arquitetura do Sistema: Scoreboard App

## 1. Princípios Arquiteturais Centrais

### 1.1 Zero Monolito (Arquitetura de Dados Modular)
- Em vez de um único arquivo de dados volumoso que prejudica o carregamento inicial, os 98 escores são particionados em **9 blocos modulares independentes**: `src/data/blocks/block_01.json` até `block_09.json`.
- A inicialização do aplicativo consome apenas um **Manifesto Leve** (`manifest.json`, ~30KB), contendo metadados essenciais de busca, categorização, slugs e sinônimos clínicos, garantindo TTI (*Time to Interactive*) < 100ms mesmo em dispositivos móveis modestos.
- Os blocos detalhados (perguntas, opções, faixas de risco, condutas farmacológicas, diluições e eixos de radar) são carregados sob demanda (*lazy-loading*) via importação dinâmica assíncrona.

### 1.2 Motores Clínicos Puros (`src/engines/`)
Todas as rotinas de cálculo, parametrização e formatação operam como funções puras TypeScript em `src/engines/`:
- **Sem efeitos colaterais (side effects):** Determinísticas, sem acoplamento com React, DOM ou estado global.
- **100% testáveis:** Suíte de testes unitários com cobertura total via Vitest.
- Motores fundamentais:
  - `calculationEngine.ts`: Executa modelos aditivos discretos, modelos contínuos (fórmulas) e modelos em árvore de decisão.
  - `infusionEngine.ts`: Executa cálculos de vazão em bomba de infusão contínua (BIC), conversões de unidades ($\mu\text{g/kg/min} \leftrightarrow \text{mL/h}$) e matrizes de titulação.
  - `radarEngine.ts`: Mapeia parâmetros laboratoriais e clínicos em eixos normalizados para geração do polígono SVG.
  - `pepExportEngine.ts`: Gera sumário clínico estruturado em texto plano para colagem em prontuários eletrônicos.

### 1.3 Radar Fisiológico em SVG Nativo Reativo (Zero Bloatware)
- Renderização puramente vetorial em SVG nativo calculando coordenadas cartesianas $(x, y)$ a partir de coordenadas polares $(\theta, r)$.
- Renderiza dois polígonos sobrepostos:
  - **Polígono Central de Higidez (Verde):** Parâmetros basais de normalidade (desvio = 0).
  - **Polígono Dinâmico do Paciente (Laranja/Vermelho):** Expande-se em tempo real conforme os inputs são fornecidos.
- Taxa de quadros constante de 60fps sem dependência de bibliotecas pesadas de terceiros (ex.: D3, Chart.js, Recharts).

### 1.4 Design Premium Minimalista, Sombras em Camadas e Modo Claro / Escuro
- **Minimalismo Refinado (Estilo Apple Health / Linear):**
  - **Modo Claro:** Fundos brancos e off-white refinados (`#FFFFFF`, `#F8FAFC`), bordas sutis de 1px (`#E2E8F0`), sombras difusas suaves em multicamada (`0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02)`).
  - **Modo Escuro:** Fundo escuro profundo e neutro (`#090D16`), cartões com chanfro sutil superior de 1px translúcido (`border-white/[0.08]`) e sombras de oclusão de contato sem estresse visual.
  - **Alternância Fluida:** Respeita o tema do sistema operacional por padrão (`prefers-color-scheme`) e oferece botão de alternância imediata (Sol/Lua) no cabeçalho.
- **Mobile-First e Ergonomia Móvel:**
  - Alvos de toque mínimos de 48×48px respeitando a `safe-area-inset-bottom`.
  - Cores Semânticas WCAG AAA: Verde `#10B981` (Estabilidade), Âmbar `#F59E0B` (Alerta), Vermelho `#EF4444` (Crítico), Azul Safira `#2563EB` (Ações primárias).

### 1.5 Navegação em 4 Pilares (Bottom Navigation) & Lista A-Z
- **Bottom Navigation com Vidro Fosco (`backdrop-blur-md`):**
  1. 📋 **Todos (A-Z):** Lista contínua rolável de todos os scores com régua vertical lateral de salto rápido (Jump Rail estilo iOS), Sticky Headers por letra e barra de busca instantânea no topo. Se houver favoritos, exibe um carrossel de chips rápidos no topo.
  2. 🗂️ **Especialidades:** Navegação pelos 9 blocos e 20 módulos clínicos.
  3. ⭐ **Favoritos:** Aba dedicada aos scores fixados com estrelinha pelo médico para acesso de 1 toque no plantão.
  4. 🛏️ **Meus Leitos:** Painel de acompanhamento de pacientes com identificadores anônimos locais ("Leito 04 - UTI").

### 1.6 Persistência Local e Zero LGPD Risk
- Os favoritos e os leitos do plantão persistem exclusivamente no cliente via **IndexedDB** local (`idb` encapsulado em `storageService.ts`).
- Nenhum dado nominal de paciente trafega ou é gravado em servidores externos.

---

## 2. Stack Tecnológica
- **Linguagem:** TypeScript 5.x
- **Build & Dev Server:** Vite
- **Framework UI:** React 18+
- **Estilização:** Tailwind CSS 3.4+ com tema dual (Light/Dark) e tokens táteis de sombra
- **Ícones:** Lucide React
- **Validação de Schemas:** Zod
- **Persistência:** IndexedDB nativo tipado (`idb`)
- **Testes:** Vitest + React Testing Library
- **PWA & Offline:** `vite-plugin-pwa` + Service Worker
