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
- **Gerador de Prompts e Especificações Visuais:** Em `guia_visual_de_frontend_gerador_de_prompts.tsx`.

### 1.3 Protocolos de Infusão e Prescrição (`docs/03_protocolos_prescricao_bic/`)
- Protocolo Mestre de Drogas Vasoativas em BIC (`protocolo_mestre_prescricao_e_bic.md`).
- Diretriz Geral de Conduta do Preceptor de Terapia Intensiva (`diretriz_geral_preceptor_uti.md`).

### 1.4 Plano Diretor Atualizado (`docs/00_plano_e_arquitetura/`)
- Especificação arquitetural do CDSS em `PLANO_TECNICO_E_ARQUITETURAL_ATUALIZADO.md`.
- Modelo relacional (DDL SQL) e mapeamento em 4 fases sequenciais.

### 1.5 Organização de Arquivos e Google Drive (`scripts/`)
- Script de automação `organize_google_drive.py` executado com sucesso e estrutura limpa em exatamente 4 pastas oficiais.

---

## 2. O que está pendente (A Fazer)

### 2.1 Fase 1: Fundação do App e Ingestão de Dados
- [ ] Inicialização do scaffold React + Vite + TypeScript + Tailwind CSS na raiz do projeto.
- [ ] Configuração de Tailwind com os tokens táteis FrontCraft Master v2.0.
- [ ] Modelagem de tipos e validação Zod (`src/types/clinical.ts`).
- [ ] Desenvolvimento de script extrator / estruturador (`scripts/ingest_catalog.py` ou geração determinística) para produzir `src/data/manifest.json` e `src/data/blocks/block_01.json` até `block_09.json`.
- [ ] Configuração da suíte de testes Vitest.

### 2.2 Fase 2: Motores Clínicos e Radar SVG
- [ ] Implementação de `src/engines/calculationEngine.ts` com testes unitários (100% cobertura).
- [ ] Implementação de `src/engines/infusionEngine.ts` com testes unitários.
- [ ] Implementação de `src/engines/radarEngine.ts` e componente `PhysiologicalRadar.tsx` em SVG nativo reativo.
- [ ] Implementação de `src/engines/pepExportEngine.ts` e barra de severidade `SeverityGradientBar.tsx`.

### 2.3 Fase 3: Telas Clínicas e Prescrição
- [ ] Tela de Navegação e Busca (`SpecialtyBrowser.tsx`, busca instantânea por sinônimos/siglas).
- [ ] Tela de Execução do Escore (`CalculatorView.tsx`, com modo Score Avulso e Quick-Pins ⭐).
- [ ] Card de Prescrição Hospitalar (`PrescriptionCard.tsx` com BIC e botão "Copiar para PEP").

### 2.4 Fase 4: Modo Meus Leitos e PWA Offline
- [ ] Persistência IndexedDB com `src/services/storageService.ts`.
- [ ] Gerenciador de Leitos do Plantão (`BedsManager.tsx`).
- [ ] Service Worker e manifesto PWA offline (`vite-plugin-pwa`).
- [ ] Homologação e validação ponta a ponta.
