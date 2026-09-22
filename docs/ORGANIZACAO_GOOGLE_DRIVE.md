# 📁 Guia Mestre de Organização do Google Drive: Scoreboard App

> **Pasta de Origem no Google Drive:** [Acessar Pasta do Projeto (ID: `1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z`)](https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z)  
> **Última Atualização:** Setembro de 2026  
> **Finalidade:** Padronizar a nomenclatura, categorizar em subpastas lógicas e eliminar duplicações e títulos truncados de todos os arquivos brutos do projeto no Google Drive.

---

## 1. Diagnóstico da Pasta Atual no Google Drive

Atualmente, a pasta raiz do Google Drive contém 20 arquivos dispersos com os seguintes problemas identificados:
1. **Nomes Truncados e Mal Formatados:** Arquivos exportados com títulos acidentais, como `--- ### 16. EDSS (_Expanded Disability Status Scale_ - Esclerose Múltipla) #### 1. Identificação.pdf` (que na verdade é o guia completo do Bloco 03 - Neurologia) e `__REVISÃO SISTEMÁTICA E EXHAUSTIVA DE ESCORES PROGNÓSTICOS...` (que é o Bloco 01 - Emergência e Choque).
2. **Duplicações de Sincronização:** Arquivos com sufixo `(1)` gerados por múltiplos uploads (ex.: `frontcraft_master_v2_0_est_dio_reativo_de_design_system (1).html` e `Chats com anexos (1).docx`).
3. **Snippets de Código Sem Contexto:** Arquivos nomeados com prefixos de automação (`gemini-code-1789963111869.md`, `gemini-code-1790054955496.ts`, etc.) sem identificação de finalidade.
4. **Ausência de Subpastas:** Documentos de arquitetura, medicina clínica, design system e protocolos de prescrição misturados em um único diretório plano.

---

## 2. Nova Arquitetura de Pastas Recomendada para o Google Drive

Para transformar o Google Drive em um repositório corporativo e médico de alto padrão, organize os arquivos nas seguintes **5 subpastas estruturadas**:

```
📂 Scoreboard App — CDSS Mobile-First (Raiz do Drive)
│
├── 📁 00_Plano_Diretor_e_Arquitetura/
│   ├── PLANO_TECNICO_E_ARQUITETURAL_CDSS.md
│   └── Proposta_Original_Calculadoras_Medicas.pdf
│
├── 📁 01_Especificacoes_Clinicas_98_Dossies/
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
├── 📁 02_Design_System_FrontCraft_UI/
│   ├── frontcraft_master_v2_0_estudio_reativo.html
│   ├── guia_e_laboratorio_front_end_master.html
│   ├── guia_visual_de_frontend_gerador_de_prompts.tsx
│   ├── componente_tokens_frontcraft.ts
│   ├── wcag_contrast_engine.ts
│   └── especificacao_design_system_tokens.md
│
├── 📁 03_Protocolos_Prescricao_e_BIC/
│   ├── protocolo_mestre_prescricao_e_bic.md
│   └── diretriz_geral_prescricao_e_infusao.md
│
└── 📁 04_Inventario_e_Indices/
    ├── INDICE_GERAL_DOCUMENTACAO.md
    └── GUIA_ORGANIZACAO_GOOGLE_DRIVE.md
```

---

## 3. Matriz De/Para: Mapeamento dos 20 Arquivos do Google Drive

Utilize esta tabela para renomear e mover cada arquivo do Google Drive para o seu destino correto:

| # | Nome Atual no Google Drive | Nova Pasta no Drive | Novo Nome Padronizado | Função / Conteúdo Clínico ou Técnico |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `App Calculadoras Médicas - Especificação Técnica e Modelagem de Banco de Dados.pdf` | `00_Plano_Diretor_e_Arquitetura/` | `Proposta_Original_Calculadoras_Medicas.pdf` | Especificação técnica e modelagem relacional de banco de dados original. |
| **2** | `__REVISÃO SISTEMÁTICA E EXHAUSTIVA DE ESCORES PROGNÓSTICOS E CALCULADORAS CLÍNICAS NA.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_01_Emergencia_Choque_UTI.pdf` | Bloco 01: Sepse, Choque e Disfunção Orgânica (qSOFA, SOFA, APACHE II, SAPS 3, Ranson). |
| **3** | `Revisão Sistemática de Escores Cardiológicos.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_02_Cardiologia_Hemodinamica.pdf` | Bloco 02: Dor Torácica, SCA e Arritmias (HEART, TIMI, GRACE, CHA2DS2-VASc, HAS-BLED). |
| **4** | `--- ### 16. EDSS (_Expanded Disability Status Scale_ - Esclerose Múltipla) #### 1. Identificação.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_03_Neurologia_Neurocirurgia.pdf` | Bloco 03: AVC, TCE, Neurotrauma e Escalas Funcionais (NIHSS, ASPECTS, ABCD2, EDSS). |
| **5** | `Chats com anexos (1).docx` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_03_Anexo_Dossie_Neurologia.docx` | Dossiê complementar de neurologia com tabelas de pontuação detalhadas. |
| **6** | `Guia Clínico de Escores Pneumológicos.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_04_Pneumologia.pdf` | Bloco 04: Pneumonias, DPOC e Vias Aéreas (CURB-65, PSI/PORT, GOLD ABE 2024/2025). |
| **7** | `Guia Clínico de Escores Cirúrgicos e Trauma.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_05_Cirurgia_Geral_Trauma.pdf` | Bloco 05: Abdome Agudo, Trauma e Queimaduras (Alvarado, Parkland/ABA, RCRI, Caprini). |
| **8** | `Revisão Sistemática de Escores Nefrológicos.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_06_Nefrologia_Meio_Interno.pdf` | Bloco 06: LRA, TFG e Distúrbios Hidroeletrolíticos (KDIGO, CKD-EPI 2021 sem raça, Ânion Gap). |
| **9** | `Chats com anexos.docx` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_06_Anexo_Dossie_Nefrologia.docx` | Dossiê complementar de nefrologia e meio interno com equações detalhadas. |
| **10** | `Revisão Sistemática de Escores em Hepatologia e Gastroenterologia.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_07_Hepatologia_Gastroenterologia.pdf` | Bloco 07: Hepatopatias e Hemorragia Digestiva (Child-Pugh, MELD, MELD-Na SUS, Rockall). |
| **11** | `Guia Clínico de Escores Pediátricos.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_08_Pediatria_Neonatologia.pdf` | Bloco 08: Neonatologia e Emergência Pediátrica (Apgar, Silverman, PEWS, Holliday-Segar). |
| **12** | `Revisão de Escores em Hematologia.pdf` | `01_Especificacoes_Clinicas_98_Dossies/` | `Bloco_09_Hematologia_Reumatologia.pdf` | Bloco 09: Anemias, Coagulopatias e Hemostasia (Mentzer, CIVD ISTH, 4Ts para HIT). |
| **13** | `frontcraft_master_v2_0_est_dio_reativo_de_design_system.html` | `02_Design_System_FrontCraft_UI/` | `frontcraft_master_v2_0_estudio_reativo.html` | Laboratório web reativo para calibração de tokens táteis e sombras volumétricas. |
| **14** | `frontcraft_master_v2_0_est_dio_reativo_de_design_system (1).html` | *Descartar / Lixeira* | *(Duplicata do item 13)* | Arquivo redundante gerado por sincronização duplicada. |
| **15** | `guia_e_laboratorio_front_end_master.html` | `02_Design_System_FrontCraft_UI/` | `guia_e_laboratorio_front_end_master.html` | Protótipo interativo de componentes e micro-interações FrontCraft. |
| **16** | `guia_visual_de_frontend_gerador_de_prompts.tsx` | `02_Design_System_FrontCraft_UI/` | `guia_visual_de_frontend_gerador_de_prompts.tsx` | Componente React gerador de prompts contextuais de interface. |
| **17** | `gemini-code-1790054955496.ts` | `02_Design_System_FrontCraft_UI/` | `wcag_contrast_engine.ts` | Motor determinístico de cálculo de contraste WCAG 2.1 com suporte a Alpha Blending. |
| **18** | `gemini-code-1790054965786.md` | `02_Design_System_FrontCraft_UI/` | `especificacao_design_system_tokens.md` | Especificação técnica completa de arquitetura FrontCraft Master v2.0. |
| **19** | `gemini-code-1790030040094.md` | `03_Protocolos_Prescricao_e_BIC/` | `protocolo_mestre_prescricao_e_bic.md` | Template mestre de prescrição hospitalar e memórias de cálculo de vazão em BIC. |
| **20** | `gemini-code-1789963111869.md` | `04_Inventario_e_Indices/` | `antigravity_core_engine_spec.md` | Especificação do motor central de engenharia Antigravity Core Engine v3.0. |

---

## 4. Instruções Práticas Passo a Passo para o Usuário no Google Drive

Siga este procedimento direto na interface web do Google Drive:

1. **Acessar a Pasta:** Abra [https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z](https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z).
2. **Criar as 5 Subpastas:**
   - Botão `Novo` $\rightarrow$ `Nova pasta`:
     - `00_Plano_Diretor_e_Arquitetura`
     - `01_Especificacoes_Clinicas_98_Dossies`
     - `02_Design_System_FrontCraft_UI`
     - `03_Protocolos_Prescricao_e_BIC`
     - `04_Inventario_e_Indices`
3. **Renomear os Arquivos Críticos:**
   - Clique com o botão direito no arquivo `--- ### 16. EDSS...` $\rightarrow$ `Renomear` $\rightarrow$ Digite: `Bloco_03_Neurologia_Neurocirurgia.pdf`.
   - Clique com o botão direito no arquivo `__REVISÃO SISTEMÁTICA E EXHAUSTIVA...` $\rightarrow$ `Renomear` $\rightarrow$ Digite: `Bloco_01_Emergencia_Choque_UTI.pdf`.
   - Renomeie os scripts `gemini-code-*.ts` e `gemini-code-*.md` conforme a tabela De/Para da Seção 3.
4. **Mover os Arquivos para Suas Respectivas Pastas:**
   - Arraste os 9 PDFs e os 2 DOCX para dentro de `01_Especificacoes_Clinicas_98_Dossies/`.
   - Arraste os arquivos de tela e tokens para `02_Design_System_FrontCraft_UI/`.
   - Arraste os protocolos médicos para `03_Protocolos_Prescricao_e_BIC/`.
5. **Remover Arquivos Duplicados:**
   - Exclua para a lixeira o arquivo `frontcraft_master_v2_0_est_dio_reativo_de_design_system (1).html` para evitar confusão de versão.

---

## 5. Correspondência 1:1 com o Repositório de Código

Toda a organização acima já está refletida de forma determinística na pasta `docs/` do repositório Git, servindo de base de dados para a ingestão automatizada em `src/data/blocks/`:

- `docs/00_plano_e_arquitetura/` $\leftrightarrow$ `00_Plano_Diretor_e_Arquitetura/`
- `docs/01_especificacoes_clinicas/` $\leftrightarrow$ `01_Especificacoes_Clinicas_98_Dossies/`
- `docs/02_design_system_ui/` $\leftrightarrow$ `02_Design_System_FrontCraft_UI/`
- `docs/03_protocolos_prescricao_bic/` $\leftrightarrow$ `03_Protocolos_Prescricao_e_BIC/`
- `docs/INDEX.md` $\leftrightarrow$ Índice central e rastreabilidade documental.
