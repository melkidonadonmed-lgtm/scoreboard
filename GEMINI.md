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

---

## Diretrizes Globais de Qualidade, Eficiência, Orquestração de Agentes e Execução Adaptativa
Este repositório segue as diretrizes globais do workspace:
- **Regras do Workspace (`dev`)**: [AGENTS.md](file:///C:/Users/melki/dev/AGENTS.md), [GEMINI.md](file:///C:/Users/melki/dev/GEMINI.md) e Hub Interativo [`tools\agent-hub.ps1`](file:///C:/Users/melki/dev/tools/agent-hub.ps1)
- **Preferências e Memória Canônica**: [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)
- **Regra Global (`always_on`)**: [diretrizes-qualidade-eficiencia.md](file:///C:/Users/melki/.gemini/config/rules/diretrizes-qualidade-eficiencia.md) (1. Qualidade e Tipagem Estrita <= 300 linhas; 2. Eficiência, Zero Preâmbulo e Portões HITL; 3. Flexibilidade Anti-Engessamento; 4. Self-Refine Silencioso; 5. Proatividade com 1 Próximo Passo Concreto; 6. Minimalist Impact `DESIGN.md v4.5-soft` — Luz 135°, `Cerulean Sapphire #0284C7`, Zero Cobalto/Glassmorphism).
- **Orquestração Interativa de Agentes (5 Camadas)**:
  1. **Bússola & Heartbeat (`0 tokens`)**: `franklin_smart_compass(intent_or_path)` | `pwsh C:\Users\melki\dev\tools\agent-hub.ps1` | `POST /rpc` (`mesh/heartbeat`).
  2. **Execução Direta vs. Loop Fechado**: Precedência `<user_rules>` **>** `franklin-skills` **>** `superpowers` (entrega direta sem entrevista em baixo risco; `LoopPlanner` Fase 0 + `gap-analyzer-auditor` em missões críticas).
  3. **Esquadrão Frontend (`FrontCraftMaster` + Topologia `3+1`)**: `invoke_subagent` (`ui-shell-navigator` -> `ui-controls-data` + `ui-motion-interaction` -> `ui-deterministic-observer`) ou `franklin_execute_dag("ui")`.
  4. **Gatekeepers Determinísticos**: `code-acceptability-auditor` (AST Python >= 75), `test-quality-auditor`, `franklin_execute_dag("physics")` (`Snorm >= 80`) e `dispatch_skill_deterministic_tests` (Go Pass@k).
  5. **Malha Multiagente Cloud/Web & Clínica**: `adk-tests` (Watchdog SRE + A2A `:8080`), `epic-volta` (DAG Kahn + `MCPBridgeAgent`), `mcp-web-agents` (Gateway 4+1) e `PCM`/`scoreboard` (`prescmed-clinical-reviewer`).
