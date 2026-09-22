# Project: Scoreboard App — Block 03 (Neurology, Neurosurgery & Neurotrauma)

## Architecture
- **Zero-Monolith Modular Architecture**: Each clinical block is an independent JSON file (`src/data/blocks/block_XX.json`) loaded on demand.
- **Lightweight Manifest**: `src/data/manifest.json` provides an ultra-fast search index (~68KB across blocks 01 and 03) containing IDs, Portuguese titles, synonyms, acronyms, tags, and category mappings. Search latency is <0.05ms P99 (target <10ms).
- **Pure Functional Calculation Engines**: Reside in `src/engines/` (`calculationEngine.ts`, `infusionEngine.ts`, `radarEngine.ts`, `pepExportEngine.ts`), independent of UI, with 100% unit test coverage in Vitest.
- **Strict Clinical Integrity**: Zero truncation of clinical dossiers. Complete pharmacological actions (diluents, doses, routes, precautions), non-pharmacological interventions, emergency alerts, and radar axes.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Calculation Engine baseScore Support | Add `baseScore` property in `CalculatorSchema` and accumulator initialization in `calculateScore` | M1 | explorer_survey_3 |
| 2 | Rotterdam Score (TCE) | Additive CT trauma score (1-6 pts), basal 1 pt, subarachnoid/intraventricular hemorrhage, 6-month mortality tiers | M2 | spec_miner_survey_1 |
| 3 | Marshall CT Classification (TCE) | Categorical diffuse injury grades I-IV, evacuated mass V, non-evacuated mass VI, ICP risk tiers | M2 | spec_miner_survey_1 |
| 4 | Hunt-Hess Scale (HSA) | Clinical grading 1-5 (plus 1a and +1 comorbidity adjustment), surgical mortality rates, DVE reset rules | M2 | spec_miner_survey_1 |
| 5 | WFNS Scale (HSA) | Objective GCS (3-15) + focal deficit matrix, prognosis tiers (good outcome to 85% mortality) | M2 | spec_miner_survey_1 |
| 6 | Fisher Classic Scale (HSA 1980) | 4 grades based on cisternal blood thickness (<1mm vs >=1mm), vasospasm paradox documentation | M2 | spec_miner_survey_1 |
| 7 | Modified Fisher / Claassen (HSA 2001) | 5 progressive ordinal grades (0 to 4) crossing cisternal blood with bilateral intraventricular hemorrhage (HIV) | M2 | spec_miner_survey_1 |
| 8 | Spetzler-Martin Grade (MAV) | Morphological sum (1-5 pts) + Grade VI inoperable, surgical morbidity, ARUBA conservative evidence | M2 | spec_miner_survey_1 |
| 9 | NIHSS (Stroke Scale) | Full 11 domains / 15 operational items (1a to 11), 0-42 points, thrombolysis/thrombectomy criteria, DAPT protocols | M2 | spec_miner_survey_2 |
| 10 | ASPECTS (MCA Stroke) | All 10 MCA cortical/subcortical zones (C, L, IC, I, M1-M6), subtractive scoring (base 10 minus 1 per zone), large core evidence | M2 | spec_miner_survey_2 |
| 11 | ICH Score (Intracerebral Hemorrhage) | 5 parameters (GCS, volume via ABC/2, IVH, infratentorial, age >= 80), 30-day mortality tiers (0-100%), reversal protocols | M2 | spec_miner_survey_2 |
| 12 | ABCD2 Score (AIT Risk) | 5 domains (Age, BP, Clinical, Duration, Diabetes), stroke risk at 2d, 7d, 90d, dual antiplatelet therapy (CHANCE/POINT) | M2 | spec_miner_survey_2 |
| 13 | ASIA / AIS Impairment Scale | ISNCSCI standards (motor 0-100, sensory 0-224, sacral sparing S4-S5, grades A-E), MAP targets 85-90 mmHg, decompression | M2 | spec_miner_survey_2 |
| 14 | Modified Rankin Scale (mRS) | 7 discrete functional grades (0 to 6), mRS-SI discriminants, independence cutoff mRS 2 vs 3 | M2 | spec_miner_survey_2 |
| 15 | Karnofsky Performance Status (KPS) | 11 percentage tiers (100% to 0% in 10% steps), ECOG correlation, 70% therapeutic threshold | M2 | spec_miner_survey_2 |
| 16 | MEEM / MMSE (Mini-Exame Estado Mental) | 7 domains (0-30 pts), Brazilian schooling cutoffs (Brucki/Bertolucci: analfabeto to superior), IAChE/Memantine actions | M2 | spec_miner_survey_2 |
| 17 | MoCA (Montreal Cognitive Assessment) | 8 domains for MCI screening, education correction (+1 pt if <=12 years), cutoff >= 26 | M2 | spec_miner_survey_2 |
| 18 | Hoehn & Yahr (Parkinson) | 8 motor stages (0 to 5 including 1.5, 2.5), pull test threshold, DBS indication, haloperidol contraindication | M2 | spec_miner_survey_2 |
| 19 | EDSS (Kurtzke Disability Scale) | 20 clinical steps (0.0 to 10.0 in 0.5 increments), 7 functional systems, ambulation distance metrics (500m to 5m) | M2 | spec_miner_survey_2 |
| 20 | Neuropharmacological Actions & Protocols | Nimodipine (black-box IV prohibition), Noradrenaline in SG 5% for PPC, 3% Hypertonic Saline vs Mannitol, Levetiracetam vs Phenytoin | M2 | spec_miner_survey_1,2 |
| 21 | Emergency Neuro Alerts & Red Flags | Acute herniation, refractory ICP, midline shift >= 5mm, status epilepticus, anticoagulation reversal alerts | M2 | spec_miner_survey_1,2 |
| 22 | Radar Axes for Block 03 | 12 normalized clinical axes across neurotrauma, vascular, cognitive, and functional domains | M2 | spec_miner_survey_1,2 |
| 23 | Build Pipeline Modularization | Update `scripts/build_all.py` to compile `block_03.json` and future blocks (02, 04, 05) modularly | M3 | explorer_survey_3 |
| 24 | Search Manifest Expansion & Synonyms | Expand `src/data/manifest.json` with Brazilian clinical synonyms, acronyms, and specialty terms | M3 | explorer_survey_3 |
| 25 | Test Decoupling & Manifest Contract Update | Decouple rigid `length === 19` checks in contract tests to dynamically assert multi-block manifest consistency | M3 | explorer_survey_3 |
| 26 | Block 03 Unit Test Suite (Vitest) | Complete unit tests for all 18 tools, Zod validation, radar normalization, and emergency alerts | M4 | explorer_survey_3 |
| 27 | Calculation Engine Golden Tests | Exhaustive golden calculation tests (ASPECTS subtractive, Rotterdam offset, NIHSS, ICH Score, etc.) | M4 | explorer_survey_3 |
| 28 | Search Performance & Zero Regression Tests | P99 latency benchmark (<10ms) and verification of zero regressions on all existing 140 tests | M4 | explorer_survey_3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Core Engine & Schema Adaptation | `src/types/clinical.ts`, `src/engines/calculationEngine.ts` | none | DONE |
| 2 | Block 03 Monographic Data | `src/data/blocks/block_03.json` (all 18 tools losslessly structured) | M1 | DONE |
| 3 | Build Pipeline & Manifest Integration | `scripts/build_all.py`, `src/data/manifest.json`, test contract decoupling | M2 | DONE |
| 4 | Vitest Suite & E2E Testing Track | `tests/unit/test_block_03.test.ts`, `tests/unit/test_neuro_calculations.test.ts`, `tests/integration/test_search_performance.test.ts` | M3 | DONE |
| 5 | Adversarial Coverage Hardening | White-box adversarial testing, edge cases stress tests, forensic audit | M4 | DONE |

## Interface Contracts
### `src/types/clinical.ts` ↔ `src/engines/calculationEngine.ts`
- `CalculatorSchema`: Optional `baseScore?: number` (defaults to 0).
- `calculateScore(tool: ClinicalTool, selections: Record<string, any>): CalculationResult`:
  - Starts initial accumulator with `tool.calculator.baseScore ?? 0`.
  - For each selected item, adds or subtracts item point value according to formula logic.
  - Returns `rawScore`, `percentage`, and matches corresponding `ClassificationTier`.

### `src/data/blocks/block_03.json` ↔ `scripts/build_all.py`
- `block_03.json` must strictly conform to `BlockDataSchema`.
- `build_all.py` discovers all `block_*.json` in `src/data/blocks/` and validates each against `BlockDataSchema`.
- Aggregates tools to generate `src/data/manifest.json` with fields: `id`, `name`, `acronym`, `category`, `tags`, `block_id`, `description`, `synonyms`, `complexity`, `primary_indication`.

## Code Layout
- `src/types/clinical.ts`: Clinical tool schemas and TypeScript types.
- `src/engines/calculationEngine.ts`: Pure scoring calculation engine.
- `src/data/blocks/block_01.json`: Block 01 data (Emergency / Critical Care).
- `src/data/blocks/block_03.json`: Block 03 data (Neurology / Neurosurgery).
- `src/data/manifest.json`: Unified search index manifest.
- `scripts/build_all.py`: Build and validation script for blocks and manifest.
- `tests/unit/`: Unit tests for data blocks, calculation engines, radar, and search.
- `tests/contract/`: Schema and contract validation tests.
- `tests/adversarial/`: Adversarial edge case and stress tests.
