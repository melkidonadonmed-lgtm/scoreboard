# Índice Geral de Documentação Técnica: Scoreboard App

Este repositório documental centraliza todas as especificações técnicas, médicas, regulatórias, de design e planejamento do **Scoreboard App** (CDSS Mobile-First PWA).

---

## Estrutura de Pastas Padronizada

```
docs/
├── 00_proposta_e_arquitetura/
│   ├── PROPOSTA_TECNICA_E_ARQUITETURAL_ATUALIZADA.md
│   └── Proposta_Original_Calculadoras_Medicas.pdf
├── 01_especificacoes_clinicas/
│   ├── MATRIZ_TAXONOMIA_20_MODULOS.md
│   ├── Bloco_01_Emergencia_Choque_UTI.pdf
│   ├── Bloco_02_Cardiologia_Hemodinamica.pdf
│   ├── Bloco_03_Neurologia_Neurocirurgia.pdf
│   ├── Bloco_03_Anexo_Dossie_Neurologia.docx
│   ├── Bloco_04_Pneumologia.pdf
│   ├── Bloco_05_Cirurgia_Geral_Trauma.pdf
│   ├── Bloco_06_Nefrologia_Meio_Interno.pdf
│   ├── Bloco_06_Anexo_Dossie_Nefrologia.docx
│   ├── Bloco_07_Hepatologia_Gastroenterologia.pdf
│   ├── Bloco_08_Pediatria_Neonatologia.pdf
│   └── Bloco_09_Hematologia_Reumatologia.pdf
├── 02_design_system_ui/
│   ├── frontcraft_master_v2_0_estudio_reativo.html
│   ├── guia_e_laboratorio_front_end_master.html
│   ├── guia_visual_de_frontend_gerador_de_prompts.tsx
│   ├── especificacao_design_system_tokens.md
│   └── componente_tokens_frontcraft.ts
├── 03_protocolos_prescricao_bic/
│   ├── protocolo_mestre_prescricao_e_bic.md
│   └── diretriz_geral_preceptor_uti.md
├── _bruto_original/
│   └── (Arquivos brutos originais preservados como backup)
└── INDEX.md
```

---

## Sumário dos Documentos

### 1. Proposta Técnica, Arquitetura e Planejamento (`00_proposta_e_arquitetura/`)
- [`PROPOSTA_TECNICA_E_ARQUITETURAL_ATUALIZADA.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/00_proposta_e_arquitetura/PROPOSTA_TECNICA_E_ARQUITETURAL_ATUALIZADA.md): Documento mestre de referência técnica contendo a visão do CDSS, enquadramento regulatório SaMD (RDC ANVISA 657/2022, CFM e LGPD), DDL PostgreSQL/Supabase, os 3 motores de cálculo, regras físicas de bomba de infusão contínua (BIC), FrontCraft Master v2.0 e o plano de implementação detalhado em 4 fases.
- [`Proposta_Original_Calculadoras_Medicas.pdf`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/00_proposta_e_arquitetura/Proposta_Original_Calculadoras_Medicas.pdf): Arquivo PDF original com a especificação técnica e modelagem de banco de dados.

### 2. Especificações Clínicas e Dossiês Médicos (`01_especificacoes_clinicas/`)
- [`MATRIZ_TAXONOMIA_20_MODULOS.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/01_especificacoes_clinicas/MATRIZ_TAXONOMIA_20_MODULOS.md): Síntese sistemática em Markdown de todos os 20 módulos dos 9 blocos com pontos de corte críticos, condutas farmacológicas/não farmacológicas e equações.
- **Bloco 01:** Sepse, Choque e Disfunção Orgânica (qSOFA, SOFA, APACHE, Ranson, Wells TEP).
- **Bloco 02:** Dor Torácica e Risco Coronariano (HEART, TIMI, GRACE, CHA2DS2-VASc, HAS-BLED).
- **Bloco 03:** AVC, Hemorragias e Neurotrauma (NIHSS, ASPECTS, ABCD2, ICH, Hunt-Hess, EDSS).
- **Bloco 04:** Pneumologia e Vias Aéreas (CURB-65, CRB-65, PSI/PORT, GOLD, BODE).
- **Bloco 05:** Cirurgia Geral e Trauma (Alvarado, Parkland para queimados, RCRI de Lee, Caprini).
- **Bloco 06:** Nefrologia e Meio Interno (KDIGO para LRA, Cockcroft-Gault, CKD-EPI, Ânion Gap).
- **Bloco 07:** Hepatologia e Gastroenterologia (Child-Pugh, MELD, MELD-Na, Glasgow-Blatchford).
- **Bloco 08:** Pediatria e Neonatologia (Apgar, Silverman-Andersen, PEWS, Holliday-Segar).
- **Bloco 09:** Hematologia e Coagulação (Índice de Mentzer, Escore 4Ts para HIT, CIVD da ISTH).

### 3. Design System e Engenharia Frontend (`02_design_system_ui/`)
- [`frontcraft_master_v2_0_estudio_reativo.html`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/frontcraft_master_v2_0_estudio_reativo.html): Estúdio interativo completo para calibração de tokens táteis, chanfros de 1px e sombras volumétricas.
- [`especificacao_design_system_tokens.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/especificacao_design_system_tokens.md): Diretrizes de engenharia de design system, cálculo de contraste WCAG 2.1 AA/AAA e micro-interações mobile.
- [`guia_visual_de_frontend_gerador_de_prompts.tsx`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/guia_visual_de_frontend_gerador_de_prompts.tsx): Gerador de componentes e prompts de design tokens.

### 4. Protocolos de Prescrição e Guia de BIC (`03_protocolos_prescricao_bic/`)
- [`protocolo_mestre_prescricao_e_bic.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/03_protocolos_prescricao_bic/protocolo_mestre_prescricao_e_bic.md): Protocolos de diluição e velocidade de infusão para Noradrenalina, Vasopressina, Dobutamina, Nitroglicerina e formato de prescrição médica hospitalar.
- [`diretriz_geral_preceptor_uti.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/03_protocolos_prescricao_bic/diretriz_geral_preceptor_uti.md): Guia de preceptoria e medicina intensiva baseada em evidências.
