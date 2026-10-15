# ESPECIFICAÇÃO TÉCNICA (`SPEC.md`) — `scoreboard`

## 1. Visão Geral
Sistema de Apoio à Decisão Clínica (CDSS) em **TypeScript + React + Vite + Vitest**, arquitetado sob separação estrita entre dados clínicos modulares (`src/data/blocks/`), contratos tipados (`src/types/clinical.ts`) e motores numéricos puros (`src/engines/`).

---

## 2. Arquitetura de Módulos e Invariantes

| Camada | Caminho | Especificação Técnica |
| :--- | :--- | :--- |
| **Especificações Fonte** | `docs/01_especificacoes_clinicas/` | 98 dossiês clínicos monográficos completos (proibida condensação ou truncamento de tabelas/condutas). |
| **Contratos Tipados** | `src/types/clinical.ts` | Schemas TypeScript/Zod (`calculator`, `radar_axes`, `pharmacological_actions`, `non_pharmacological_actions`). |
| **Blocos de Dados** | `src/data/blocks/block_01..09.json` | Particionamento em 9 blocos JSON carregados sob demanda (*lazy-loading*). |
| **Motores Puros** | `src/engines/*.ts` | `calculationEngine.ts`, `infusionEngine.ts`, `radarEngine.ts`, `pepExportEngine.ts` (zero dependência de DOM/React). |

---

## 3. Regras Clínicas e de Segurança
1. **Zero Truncamento Clínico**: Todas as faixas de dose, diluições em BIC (Noradrenalina em SG 5%, Vasopressina 0,01–0,04 UI/min, Nitroglicerina em vidro/polietileno) e alertas (SSC 2021 no qSOFA) são obrigatórios.
2. **Zero PII/PHI em Rede**: Nenhum dado identificável de paciente é transmitido para fora do dispositivo; armazenamento local restrito a IndexedDB.
