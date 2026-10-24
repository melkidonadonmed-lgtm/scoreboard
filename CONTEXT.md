# CONTEXTO OPERACIONAL — `scoreboard` (CDSS — Sistema de Apoio à Decisão Clínica e Escores)

Este documento resume a arquitetura modular, o catálogo de 114 dossiês clínicos e o estado operacional do **`scoreboard`**.

---

## 1. Papel e Arquitetura
O `scoreboard` é um Progressive Web App (PWA) de apoio à decisão clínica (**CDSS**) focado em medicina de emergência, terapia intensiva, neurocirurgia e clínica médica, estruturado sem monólitos:
- **Catálogo de 114 Escores Clínicos em 9 Blocos Modulares (`src/data/blocks/block_01.json` .. `block_09.json`)**: Carregamento via manifesto leve (`src/data/manifest.json`) e code-splitting por bloco no Vite (`clinical-block-01` .. `09`, todos `< 500 kB`).
- **4 Motores Puros em TypeScript (`src/engines/`)**:
  1. `calculationEngine.ts`: Cálculo determinístico de escores, estratificação de risco e projeção reativa dos desvios normalizados (`[0.0, 1.0]`) para todos os eixos do radar (`>= 3` eixos por ferramenta).
  2. `infusionEngine.ts`: Diluição e vazão de drogas vasoativas e sedoanalgesia em bomba de infusão contínua (`BIC`).
  3. `radarEngine.ts`: Geometria polar-cartesiana em SVG puro a 60fps para o `PhysiologicalRadar.tsx`.
  4. `pepExportEngine.ts`: Formatação estruturada SOAP em texto puro para cópia direta ao Prontuário Eletrônico do Paciente (`PEP`).
- **Privacidade Zero-LGPD Risk**: Modo "Meus Leitos" persistido exclusivamente em IndexedDB/localStorage local com identificadores anônimos transitórios e bloqueio determinístico de PII (CPF/RG/CNS).

---

## 2. Estado Operacional e Portões de Qualidade (Outubro/2026)
- Diretrizes médicas atualizadas (SSC 2021 para Sepse/qSOFA/SOFA, GOLD ABE 2024/2025 para DPOC, ABA 2 mL/kg/% SCQ para queimaduras, CKD-EPI 2021 sem raça, MELD-Na / MELD 3.0 e 39 ferramentas neurocirúrgicas/neurocríticas no Bloco 03).
- **Vitest**: `14/14` suítes aprovadas (`421/421` testes `PASS`).
- **E2E Harness (Tiers 1 a 4)**: `54/54` suítes aprovadas (`242/242` testes `PASS`).
- **Frontend UI/A11y/FSM/Security (`audit_tactile_ui.py`)**: `100.0/100` (`PASS`).
- **Qualidade de Testes (`test_quality_auditor.py`)**: `100.0/100` (`PASS`, Nível 4 em `632` casos de teste).
- **Aceitabilidade de Código Python (`code_acceptability_auditor.py`)**: `24/24` arquivos `APPROVED` (`90.5/100`, `0` violações críticas).
