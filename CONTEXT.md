# CONTEXTO OPERACIONAL — `scoreboard` (CDSS — Sistema de Apoio à Decisão Clínica e Escores)

Este documento resume a arquitetura modular, o catálogo de 98 dossiês clínicos e o estado operacional do **`scoreboard`**.

---

## 1. Papel e Arquitetura
O `scoreboard` é um Progressive Web App (PWA) de apoio à decisão clínica (**CDSS**) focado em medicina de emergência, terapia intensiva e clínica médica, estruturado sem monólitos:
- **Catálogo de 98 Escores Clínicos em 9 Blocos Lazy (`src/data/blocks/block_01.json` .. `block_09.json`)**: Carregamento inicial via manifesto leve (`~30KB`, `<100ms` em dispositivos móveis).
- **4 Motores Puros em TypeScript (`src/engines/`)**:
  1. `calculationEngine.ts`: Cálculo determinístico de escores e estratificação de risco.
  2. `infusionEngine.ts`: Diluição e vazão de drogas vasoativas e sedoanalgesia em bomba de infusão contínua (`BIC`).
  3. `radarEngine.ts`: Geração de eixos fisiológicos para visualização multidimensional.
  4. `pepExportEngine.ts`: Formatação estruturada de condutas e escores para cópia direta ao Prontuário Eletrônico do Paciente (`PEP`).
- **Privacidade Zero-LGPD Risk**: Modo "Meus Leitos" persistido exclusivamente em IndexedDB local com identificadores anônimos transitórios.

---

## 2. Estado Operacional (Outubro/2026)
- Diretrizes médicas atualizadas (SSC 2021 para Sepse/qSOFA/SOFA, GOLD ABE 2024/2025 para DPOC, ABA 2 mL/kg/% SCQ para queimaduras, CKD-EPI 2021 sem raça e MELD-Na / MELD 3.0).
- Motores validados por testes unitários no Vitest.
