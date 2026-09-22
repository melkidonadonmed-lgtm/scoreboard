# Estado Atual do Repositório: Scoreboard App

*Data da última atualização: 22 de Setembro de 2026*

---

## 1. O que já foi concluído

### 1.1 Especificações Clínicas Monográficas (`docs/01_especificacoes_clinicas/`)
- **98 Dossiês Clínicos Completos:** Todos os 98 escores das 9 grandes especialidades detalhados em PDFs e DOCX originais.
- **Matriz de Taxonomia MECE:** Estrutura de 20 módulos em `MATRIZ_TAXONOMIA_20_MODULOS.md`.
- **Regra Anti-Truncamento:** Diretriz estrita documentada em `AGENTS.md` impedindo descarte de variáveis clínicas, tabelas de corte ou orientações farmacológicas.

### 1.2 Design System e Tokens UI (`docs/02_design_system_ui/`)
- **Tokens do FrontCraft Master v2.0:** Definidos em `componente_tokens_frontcraft.ts` e `especificacao_design_system_tokens.md`.
- **Estúdio Reativo Interativo:** Laboratório e estúdio tátil em `frontcraft_master_v2_0_estudio_reativo.html`.

### 1.3 Protocolos de Infusão e Prescrição (`docs/03_protocolos_prescricao_bic/`)
- Protocolo Mestre de Drogas Vasoativas em BIC (`protocolo_mestre_prescricao_e_bic.md`).
- Diretriz Geral de Conduta do Preceptor de Terapia Intensiva (`diretriz_geral_preceptor_uti.md`).

### 1.4 Fase 1 (Piloto Vertical do Bloco 01) Concluída e Homologada!
- **Scaffold & Build de Produção:** React 18 + Vite 5 + TypeScript 5 + Tailwind CSS configurado com `darkMode: 'class'`, tokens táteis FrontCraft Master e build 100% limpo em `dist/`.
- **Contratos e Ingestão de Dados:** Schemas Zod rigorosos em `src/types/clinical.ts` e `src/types/infusion.ts`; catálogo completo do Bloco 01 em `src/data/blocks/block_01.json` (223KB, 19 ferramentas monográficas completas) e manifesto de busca rápida em `src/data/manifest.json` (39KB) indexando sinônimos clínicos brasileiros com busca P99 < 0.02ms.
- **Motores Clínicos Puros (`src/engines/`):**
  - `calculationEngine.ts`: Scoring exato para qSOFA (com aviso SSC 2021 obrigatório), SOFA completo, Wells TEP, Glasgow-P, FOUR, Ranson e BISAP.
  - `infusionEngine.ts`: Fórmula exata de vazão em BIC ($mL/h$), conversões de dose e matriz de titulação para Noradrenalina (em SG 5%), Vasopressina, Dobutamina e Nitroglicerina (alerta de frasco de vidro/poliolefina).
  - `radarEngine.ts`: Mapeamento multieixo de homeostase (0) a desvio crítico (1) com projeção polar para SVG nativo.
  - `pepExportEngine.ts`: Gerador de sumário clínico estruturado em texto plano para cópia imediata em prontuários eletrônicos (Tasy, MV Soul, Epimed).
- **Interface Mobile-First & Ergonomia Tátil (`src/components/`):**
  - `AzScoreList.tsx` & `AlphabetJumpRail.tsx`: Lista contínua A-Z com Sticky Headers, régua lateral vertical de salto rápido (estilo iOS) e barra de busca instantânea.
  - `FavoritesView.tsx`: Carrossel de acesso rápido e aba dedicada para scores favoritados com estrelinha (⭐).
  - `storageService.ts`: Persistência assíncrona local no IndexedDB com bloqueio estrito contra violações de LGPD (rejeição de CPF/dados nominais).
  - `PhysiologicalRadar.tsx`: Radar em SVG nativo reativo (60fps) com polígono verde de higidez e sobreposição do paciente.
  - `PrescriptionCard.tsx`: Card de condutas com micro-calculadora de BIC em tempo real (vazão automática em mL/h para peso/dose) e botão "Copiar para PEP".
  - `ThemeToggle.tsx`: Alternador tátil Sol/Lua no cabeçalho com memorização e suporte completo a Modo Claro e Modo Escuro.
  - `BottomNav.tsx` & `App.tsx`: Navegação em 4 abas integrando o fluxo completo.
- **Validação de Testes:**
  - **Vitest Unit & Adversarial Tests:** 140 testes aprovados em 6 suítes (100% de sucesso).
  - **E2E Opaque-Box Test Runner:** 242 testes aprovados em 54 suítes (100% de sucesso).
  - **TypeScript Compilation:** Zero erros (`npx tsc --noEmit` exit 0).

---

## 2. Próximos Passos (Fases Subsequentes)

### 2.1 Expansão dos Blocos 02 a 09
- [ ] Ingestão e estruturação dos dados clínicos dos blocos 02 a 09 (Cardiologia, Neurologia, Pneumologia, Cirurgia/Trauma, Nefrologia, Hepatologia, Pediatria, Hematologia) utilizando a mesma arquitetura modular lazy-loaded validada no Bloco 01.
- [ ] Implementação de novos motores de cálculo especializados (ex.: CKD-EPI 2021 race-free, MELD-Na SUS vs MELD 3.0, ABA 2mL vs Parkland 4mL).

### 2.2 PWA Offline e Instalação Móvel
- [ ] Configuração de Service Worker com `vite-plugin-pwa` para cache offline de todos os blocos e assets em subsolos hospitalares.
- [ ] Geração de ícones e manifesto de aplicativo PWA instalável.
