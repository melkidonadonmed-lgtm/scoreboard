# GEMINI.md — Scoreboard App (Escores Clínicos e Dossiês Médicos)

Diretrizes e contexto operacional para o **Google Antigravity (AGY)** e **Gemini CLI** atuando no repositório `scoreboard`.

> **Fonte Primária**: Consulte o [`AGENTS.md`](./AGENTS.md) para especificações médicas detalhadas e catálogo de escores. Em caso de divergência, prevalece o `AGENTS.md`.

---

## 1. Identificação e Arquitetura
- **Projeto**: `scoreboard` (Scoreboard App).
- **Domínio**: Saúde e Emergência Médica (YMYL) — 98 escores clínicos monográficos estruturados em `docs/01_especificacoes_clinicas/`.
- **Arquitetura Modular**:
  - Catálogo dividido em 9 blocos modulares (`src/data/blocks/block_01.json` a `block_09.json`) com lazy-loading e manifesto de busca ultraleve (~30KB).
  - Motores de cálculo puros (`src/engines/`): `calculationEngine.ts`, `infusionEngine.ts`, `radarEngine.ts`, `pepExportEngine.ts` sem acoplamento com a UI e com 100% de testes no Vitest.
- **Stack**: React 19 + TypeScript, Vite 6, Tailwind CSS v4, Vitest, Python.
- **Deploy**: Cloud Run `scoreboard-app` (`southamerica-east1`).

---

## 2. Invariantes Clínicas e Diretrizes Médicas Vigentes
- **Anti-Truncamento**: É expressamente proibido abreviar ou descartar ferramentas clínicas, parâmetros laboratoriais ou condutas farmacológicas dos 98 dossiês clínicos.
- **Sepse**: qSOFA com aviso mandatório da Surviving Sepsis Campaign (SSC 2021) desaconselhando uso isolado para exclusão de sepse; SOFA completo para confirmação de disfunção multiorgânica.
- **DPOC**: Classificação GOLD ABE moderna (2024/2025).
- **Queimaduras**: Padrão ABA moderno ($2\text{ mL/kg/% SCQ}$ de Ringer Lactato) como recomendado; Parkland tradicional ($4\text{ mL}$) comutável para trauma elétrico.
- **Nefrologia**: Equação CKD-EPI 2021 sem variável de raça.
- **Hepatologia**: MELD-Na (padrão Brasil/SUS) com opção de análise comparativa para MELD 3.0.
- **Drogas Vasoativas**: Noradrenalina diluída preferencialmente em SG 5%; Vasopressina em dose fixa ($0,01\text{ a }0,04\text{ UI/min}$); Nitroglicerina em frasco de vidro ou polietileno/poliolefina.

---

## 3. Privacidade e LGPD (Zero Risk)
- Nenhum dado identificador de paciente (nome, CPF, prontuário) pode ser enviado para servidores externos.
- O modo "Meus Leitos" opera exclusivamente via IndexedDB local com rótulos anônimos transitórios ("Leito 04 - UTI").
