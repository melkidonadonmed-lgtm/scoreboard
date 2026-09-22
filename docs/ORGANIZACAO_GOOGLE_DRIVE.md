# 📁 Guia de Organização do Google Drive: Scoreboard App

> **Pasta do Projeto no Google Drive:** [Acessar Pasta (ID: `1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z`)](https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z)  
> **Finalidade:** Organizar os arquivos brutos do Google Drive nas 4 pastas oficiais do projeto, corrigindo títulos truncados e eliminando duplicatas.

---

## 🏛️ As 4 Pastas Oficiais do Projeto no Google Drive

Toda a documentação clínica, técnica e de interface deve ser distribuída exclusivamente nestas **4 pastas**:

```
📂 Scoreboard App (Raiz do Drive)
│
├── 📁 00_Plano_e_Arquitetura/
│   ├── PLANO_TECNICO_E_ARQUITETURAL_CDSS.md
│   └── Proposta_Original_Calculadoras_Medicas.pdf
│
├── 📁 01_Especificacoes_Clinicas/
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
│
├── 📁 02_Design_System_UI/
│   ├── frontcraft_master_v2_0_estudio_reativo.html
│   ├── guia_e_laboratorio_front_end_master.html
│   ├── guia_visual_de_frontend_gerador_de_prompts.tsx
│   ├── componente_tokens_frontcraft.ts
│   └── especificacao_design_system_tokens.md
│
└── 📁 03_Protocolos_Prescricao_BIC/
    ├── protocolo_mestre_prescricao_e_bic.md
    └── diretriz_geral_prescricao_e_infusao.md
```

---

## 📋 Tabela De/Para dos Arquivos do Google Drive

Mapeamento exato de cada um dos arquivos soltos atualmente na raiz do Google Drive:

| # | Nome Atual no Google Drive | Pasta de Destino | Nome Limpo Padronizado | O Que É / Função |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `App Calculadoras Médicas - Especificação Técnica...pdf` | `00_Plano_e_Arquitetura/` | `Proposta_Original_Calculadoras_Medicas.pdf` | Documento de arquitetura e modelo relacional original. |
| **2** | `__REVISÃO SISTEMÁTICA E EXHAUSTIVA DE ESCORES...pdf` | `01_Especificacoes_Clinicas/` | `Bloco_01_Emergencia_Choque_UTI.pdf` | Sepse, Choque e Disfunção Orgânica (`qSOFA`, `SOFA`, `APACHE`). |
| **3** | `Revisão Sistemática de Escores Cardiológicos.pdf` | `01_Especificacoes_Clinicas/` | `Bloco_02_Cardiologia_Hemodinamica.pdf` | Dor Torácica, SCA e Arritmias (`HEART`, `TIMI`, `CHA2DS2-VASc`). |
| **4** | `--- ### 16. EDSS (_Expanded Disability Status Scale_...pdf` | `01_Especificacoes_Clinicas/` | `Bloco_03_Neurologia_Neurocirurgia.pdf` | AVC, TCE, Neurotrauma e Escalas (`NIHSS`, `ASPECTS`, `EDSS`). |
| **5** | `Chats com anexos (1).docx` | `01_Especificacoes_Clinicas/` | `Bloco_03_Anexo_Dossie_Neurologia.docx` | Dossiê complementar de Neurologia com tabelas de pontos. |
| **6** | `Guia Clínico de Escores Pneumológicos.pdf` | `01_Especificacoes_Clinicas/` | `Bloco_04_Pneumologia.pdf` | Pneumonias, DPOC e Vias Aéreas (`CURB-65`, `GOLD ABE 2024/2025`). |
| **7** | `Guia Clínico de Escores Cirúrgicos e Trauma.pdf` | `01_Especificacoes_Clinicas/` | `Bloco_05_Cirurgia_Geral_Trauma.pdf` | Abdome Agudo, Trauma e Queimaduras (`Alvarado`, `Parkland/ABA`). |
| **8** | `Revisão Sistemática de Escores Nefrológicos.pdf` | `01_Especificacoes_Clinicas/` | `Bloco_06_Nefrologia_Meio_Interno.pdf` | LRA, TFG e Meio Interno (`KDIGO`, `CKD-EPI 2021`, `Ânion Gap`). |
| **9** | `Chats com anexos.docx` | `01_Especificacoes_Clinicas/` | `Bloco_06_Anexo_Dossie_Nefrologia.docx` | Dossiê complementar de Nefrologia com equações de clearance. |
| **10** | `Revisão Sistemática de Escores em Hepatologia...pdf` | `01_Especificacoes_Clinicas/` | `Bloco_07_Hepatologia_Gastroenterologia.pdf` | Cirrose, Fila de Transplante e HDA (`Child-Pugh`, `MELD-Na SUS`). |
| **11** | `Guia Clínico de Escores Pediátricos.pdf` | `01_Especificacoes_Clinicas/` | `Bloco_08_Pediatria_Neonatologia.pdf` | Neonatologia e Emergência Pediátrica (`Apgar`, `PEWS`, `Holliday`). |
| **12** | `Revisão de Escores em Hematologia.pdf` | `01_Especificacoes_Clinicas/` | `Bloco_09_Hematologia_Reumatologia.pdf` | Anemias, CIVD e Hemostasia (`Mentzer`, `CIVD ISTH`, `4Ts para HIT`). |
| **13** | `frontcraft_master_v2_0_est_dio_reativo...html` | `02_Design_System_UI/` | `frontcraft_master_v2_0_estudio_reativo.html` | Laboratório web para calibração de tokens táteis. |
| **14** | `frontcraft_master_v2_0_est_dio_reativo... (1).html` | *Excluir / Lixeira* | *(Duplicata redundante)* | Arquivo duplicado por sincronização. |
| **15** | `guia_e_laboratorio_front_end_master.html` | `02_Design_System_UI/` | `guia_e_laboratorio_front_end_master.html` | Protótipo interativo de componentes móveis One-Thumb. |
| **16** | `guia_visual_de_frontend_gerador_de_prompts.tsx` | `02_Design_System_UI/` | `guia_visual_de_frontend_gerador_de_prompts.tsx` | Componente React gerador de prompts contextuais de UI. |
| **17** | `gemini-code-1790054955496.ts` | `02_Design_System_UI/` | `componente_tokens_frontcraft.ts` | Motor determinístico de cálculo de contraste e tokens. |
| **18** | `gemini-code-1790054965786.md` | `02_Design_System_UI/` | `especificacao_design_system_tokens.md` | Especificação técnica de arquitetura FrontCraft Master v2.0. |
| **19** | `gemini-code-1790030040094.md` | `03_Protocolos_Prescricao_BIC/` | `protocolo_mestre_prescricao_e_bic.md` | Template mestre de prescrição médica e memórias de BIC. |

---

## ⚡ Como Organizar Diretamente no Google Drive

1. Abra a pasta do projeto: [drive.google.com/.../1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z](https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z);
2. Crie as **4 pastas**:
   - `00_Plano_e_Arquitetura`
   - `01_Especificacoes_Clinicas`
   - `02_Design_System_UI`
   - `03_Protocolos_Prescricao_BIC`
3. Arraste os arquivos para suas respectivas pastas e renomeie os títulos truncados conforme a tabela acima;
4. Envie o arquivo duplicado com `(1)` para a lixeira.
