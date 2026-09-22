# Índice Geral de Documentação Técnica: Scoreboard App

Este repositório documental centraliza todas as especificações técnicas, médicas, regulatórias, de design e de engenharia do **Scoreboard App** (CDSS Mobile-First PWA).

> [!NOTE]
> Para instruções de organização e mapeamento dos arquivos originais do Google Drive, consulte o [Guia Mestre de Organização do Google Drive](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/ORGANIZACAO_GOOGLE_DRIVE.md).

---

## 🏛️ Estrutura de Pastas Padronizada

```
docs/
├── 00_plano_e_arquitetura/            # Plano Diretor, Arquitetura SaMD e DDL
│   ├── PLANO_TECNICO_E_ARQUITETURAL_ATUALIZADO.md
│   └── Proposta_Original_Calculadoras_Medicas.pdf
├── 01_especificacoes_clinicas/        # 9 Guias em PDF, 2 DOCX e Matriz de 20 Módulos
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
├── 02_design_system_ui/               # Laboratório FrontCraft Master v2.0 e Tokens Táteis
│   ├── frontcraft_master_v2_0_estudio_reativo.html
│   ├── guia_e_laboratorio_front_end_master.html
│   ├── guia_visual_de_frontend_gerador_de_prompts.tsx
│   ├── especificacao_design_system_tokens.md
│   └── componente_tokens_frontcraft.ts
├── 03_protocolos_prescricao_bic/      # Diretrizes de Prescrição Hospitalar e Guia de BIC
│   ├── protocolo_mestre_prescricao_e_bic.md
│   └── diretriz_geral_preceptor_uti.md
├── _bruto_original/                   # Arquivos originais exportados do Google Drive
│   └── README.md                      # Inventário e rastreabilidade dos 20 arquivos brutos
├── ORGANIZACAO_GOOGLE_DRIVE.md        # Mapeamento De/Para e organização da pasta do Drive
└── INDEX.md                           # Este índice geral
```

---

## 📚 Sumário dos Documentos

### 1. Plano Diretor e Arquitetura (`00_plano_e_arquitetura/`)
- [`PLANO_TECNICO_E_ARQUITETURAL_ATUALIZADO.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/00_plano_e_arquitetura/PLANO_TECNICO_E_ARQUITETURAL_ATUALIZADO.md): Especificação mestre com enquadramento regulatório SaMD (RDC ANVISA 657/2022, CFM e LGPD), arquitetura de dados sem monolito, motores puros de cálculo, FrontCraft Master v2.0 e planejamento em 4 fases. Feito para qualquer médico (UPA, enfermaria, ambulatório, cirurgia e UTI) com foco na eliminação do garimpo de tabelas.
- [`Proposta_Original_Calculadoras_Medicas.pdf`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/00_plano_e_arquitetura/Proposta_Original_Calculadoras_Medicas.pdf): Documento PDF original de especificação e modelagem de banco de dados.

### 2. Especificações Clínicas e Dossiês Médicos (`01_especificacoes_clinicas/`)
- [`MATRIZ_TAXONOMIA_20_MODULOS.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/01_especificacoes_clinicas/MATRIZ_TAXONOMIA_20_MODULOS.md): Matriz de referência em Markdown cobrindo os 20 módulos clínicos, pontos de corte críticos e condutas terapêuticas.
- **Bloco 01:** Sepse, Choque e Disfunção Orgânica (`qSOFA`, `SOFA`, `APACHE II`, `SAPS 3`, `Ranson`).
- **Bloco 02:** Dor Torácica, SCA e Arritmias (`HEART`, `TIMI`, `GRACE`, `CHA2DS2-VASc`, `HAS-BLED`).
- **Bloco 03:** AVC, TCE e Neurotrauma (`NIHSS`, `ASPECTS`, `ABCD2`, `ICH`, `Hunt-Hess`, `EDSS`) + [Anexo DOCX](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/01_especificacoes_clinicas/Bloco_03_Anexo_Dossie_Neurologia.docx).
- **Bloco 04:** Pneumologia e Vias Aéreas (`CURB-65`, `CRB-65`, `PSI/PORT`, `GOLD ABE 2024/2025`, `BODE`).
- **Bloco 05:** Cirurgia Geral, Trauma e Queimaduras (`Alvarado`, `Fórmula ABA Moderna/Parkland`, `RCRI de Lee`, `Caprini`).
- **Bloco 06:** Nefrologia e Meio Interno (`KDIGO LRA`, `CKD-EPI 2021 sem raça`, `Cockcroft-Gault`, `Ânion Gap`) + [Anexo DOCX](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/01_especificacoes_clinicas/Bloco_06_Anexo_Dossie_Nefrologia.docx).
- **Bloco 07:** Hepatologia e Gastroenterologia (`Child-Pugh`, `MELD`, `MELD-Na SUS`, `Glasgow-Blatchford`, `Rockall`).
- **Bloco 08:** Pediatria e Neonatologia (`Apgar`, `Silverman-Andersen`, `Novo Ballard`, `PEWS`, `Holliday-Segar`).
- **Bloco 09:** Hematologia e Hemostasia (`Índice de Mentzer`, `Escore 4Ts para HIT`, `CIVD da ISTH`).

### 3. Design System e Engenharia Frontend (`02_design_system_ui/`)
- [`frontcraft_master_v2_0_estudio_reativo.html`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/frontcraft_master_v2_0_estudio_reativo.html): Estúdio interativo para calibração de tokens táteis, chanfro de 1px (`shadow-bevel`) e sombras volumétricas.
- [`especificacao_design_system_tokens.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/especificacao_design_system_tokens.md): Arquitetura do design system, ergonomia One-Thumb e acessibilidade WCAG 2.1 AA/AAA.
- [`componente_tokens_frontcraft.ts`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/componente_tokens_frontcraft.ts): Tokens exportados em TypeScript para consumo pela aplicação.
- [`guia_e_laboratorio_front_end_master.html`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/guia_e_laboratorio_front_end_master.html): Laboratório de componentes e micro-interações.
- [`guia_visual_de_frontend_gerador_de_prompts.tsx`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/02_design_system_ui/guia_visual_de_frontend_gerador_de_prompts.tsx): Gerador dinâmico de prompts de estilo.

### 4. Protocolos de Prescrição e Guia de BIC (`03_protocolos_prescricao_bic/`)
- [`protocolo_mestre_prescricao_e_bic.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/03_protocolos_prescricao_bic/protocolo_mestre_prescricao_e_bic.md): Estrutura mestre de prescrição médica hospitalar e memórias de cálculo de vazão em bomba de infusão.
- [`diretriz_geral_preceptor_uti.md`](file:///home/melki/projects/workspace/projects/scoreboard-app/docs/03_protocolos_prescricao_bic/diretriz_geral_preceptor_uti.md): Protocolos clínicos oficiais AMIB de drogas vasoativas (Noradrenalina, Vasopressina, Dobutamina, Nitroglicerina), diluições em SG 5% e modelos de minuta SOAP/SBAR.

### 5. Rastreabilidade com o Google Drive (`ORGANIZACAO_GOOGLE_DRIVE.md`)
- Mapeamento detalhado dos 20 arquivos brutos exportados do Google Drive ([Pasta `1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z`](https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z)), eliminando duplicações e nomes truncados com correspondência 1:1 na pasta `docs/`.
