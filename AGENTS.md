# AGENTS.md — Clinical Scoreboard App (`scoreboard` v2.1)

> **Global Kernel Inheritance:** Universal Golden Rules (1–8), Technical English internals / **Portuguese (`pt-BR`)** user bridge, and the Self-Refine Closing Block inherit from `quality-efficiency-guidelines.md` (`always_on`).

## 0. Project Context & Modular Data Architecture

- **State Triad:** [`.context/context.md`](file:///C:/Users/melki/dev/repos/scoreboard/.context/context.md) | [`.context/spec.md`](file:///C:/Users/melki/dev/repos/scoreboard/.context/spec.md)
- **Zero-Monolith Lazy Blocks:** Organize the **98 clinical scores** across 9 lazy-loaded JSON blocks (`src/data/blocks/block_01.json` through `block_09.json`) backed by a lightweight search manifest (`~30KB`, `<100ms` mobile boot).
- **Pure Calculation Engines:** Keep `calculationEngine.ts`, `infusionEngine.ts`, `radarEngine.ts`, and `pepExportEngine.ts` in `src/engines/` as pure UI-independent TypeScript functions with 100% Vitest unit test coverage.

## 1. Non-Negotiable Clinical & Privacy Invariants

1. **Anti-Truncation of Clinical Dossiers:** Never drop, abbreviate, or suppress clinical tools, lab parameters, point tables, or pharmacological conduct from the 98 monographic dossiers in `docs/01_especificacoes_clinicas/` or `src/types/clinical.ts` (`calculator`, `radar_axes`, `pharmacological_actions`, `non_pharmacological_actions`).
2. **Active Medical Guidelines:**
   - **Sepsis:** Include mandatory Surviving Sepsis Campaign (SSC 2021) warning on qSOFA against standalone sepsis exclusion; use full SOFA for organ dysfunction confirmation.
   - **COPD:** GOLD ABE (2024/2025) classification.
   - **Burns:** Modern ABA standard ($2\text{ mL/kg/\% TBSA}$ Lactated Ringer's) default, with classical Parkland ($4\text{ mL}$) toggleable for electrical trauma.
   - **Nephrology & Hepatology:** Race-free CKD-EPI 2021 equation; MELD-Na (Brazil/SUS default) with MELD 3.0 comparison option.
   - **Vasoactive Infusion Pumps (BIC):** Norepinephrine preferentially diluted in 5% Dextrose (`SG 5%`); fixed-dose Vasopressin ($0.01\text{–}0.04\text{ IU/min}$); Nitroglycerin in glass or polyethylene/polyolefin bottles.
3. **Zero LGPD / PHI Risk:** Never transmit patient identifiers (name, CPF, medical record number) to external servers; operate "Meus Leitos" strictly via local IndexedDB with anonymous labels (`"Leito 04 - UTI"`).
