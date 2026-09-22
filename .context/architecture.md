# Arquitetura do Sistema: Scoreboard App

## 1. Princípios Arquiteturais Centrais

### 1.1 Zero Monolito (Arquitetura de Dados Modular)
- Em vez de um único arquivo de dados volumoso que prejudica o carregamento inicial, os 98 escores são particionados em **9 blocos modulares independentes**: `src/data/blocks/block_01.json` até `block_09.json`.
- A inicialização do aplicativo consome apenas um **Manifesto Leve** (`manifest.json`, ~30KB), contendo metadados essenciais de busca, categorização, slugs e sinônimos, garantindo TTI (*Time to Interactive*) < 100ms mesmo em dispositivos móveis modestos.
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

### 1.4 FrontCraft Master v2.0 & Ergonomia Móvel
- **Mobile-First e Operação com Uma Mão (One-Thumb Zone):** Elementos interativos críticos situados na metade inferior da tela, alvos de toque mínimos de 48×48px.
- **Física Tátil e Profundidade:** Chanfros físicos (`shadow-bevel`), sombras volumétricas em multicamada, feedback hápitico suave.
- **Cores Semânticas WCAG AAA:** Verde `#10B981` (Estabilidade), Âmbar `#F59E0B` (Alerta), Vermelho `#EF4444` (Crítico).

### 1.5 Persistência Local e Zero LGPD Risk
- O modo "Meus Leitos" e os "Favoritos" persistem seus dados no navegador do médico via **IndexedDB** local (usando `idb` ou `dexie`).
- Não há backend centralizado coletando prontuários.
- Rótulos de pacientes são anônimos e transitórios ("Leito 04 - UTI").

---

## 2. Stack Tecnológica
- **Linguagem:** TypeScript 5.x
- **Build & Dev Server:** Vite
- **Framework UI:** React 18+
- **Estilização:** Tailwind CSS 3.4+ com tokens táteis FrontCraft Master
- **Ícones:** Lucide React
- **Validação de Schemas:** Zod
- **Testes:** Vitest + React Testing Library
- **PWA & Offline:** `vite-plugin-pwa` + Service Worker com cache-first para assets e dados JSON
