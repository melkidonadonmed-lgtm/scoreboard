# Project: Scoreboard App Phase 1 (Vertical Pilot of Clinical Block 01)

## Architecture
Scoreboard App is a mobile-first Clinical Decision Support System (CDSS) for physicians, engineered for sub-100ms cold start, sub-10ms search, 60fps native SVG visualization, pure clinical calculation engines, and zero patient data leakage (100% local IndexedDB).

### Architectural Stack
- **Framework:** React 18 + Vite 5 + TypeScript 5
- **Styling & Design System:** Tailwind CSS 3 with `darkMode: 'class'`, FrontCraft Master v2.0 design tokens (card shadows, 1px borders, tactile bevels, WCAG 2.1 AA contrast)
- **Data Architecture:** Split data model:
  - `src/data/manifest.json` (~30KB): lightweight index of all calculators with Brazilian clinical synonyms, tags, and categories for instant search.
  - `src/data/blocks/block_01.json`: modular, lazy-loaded monographic JSON of Block 01 (Emergency & ICU) preserving complete dossiers without truncation.
- **Contract & Validation Layer:** TypeScript interfaces and Zod schemas in `src/types/clinical.ts` and `src/types/infusion.ts`.
- **Pure Engine Layer (`src/engines/`):**
  - `calculationEngine.ts`: additive point models, continuous formulas, and decision trees.
  - `infusionEngine.ts`: physical infusion rate formulas ($mL/h$), dilution recipes, and vasoactive titration matrices.
  - `radarEngine.ts`: multi-axis normalization ($0$ baseline to $1$ max deviation) and polar-to-Cartesian trigonometric projection.
  - `pepExportEngine.ts`: structured SOAP/SBAR minute generator for Brazilian hospital EHRs (MV Soul, Tasy, Epimed).
- **Storage Layer (`src/services/storageService.ts`):** IndexedDB (`idb`) for starred favorites and anonymous local bed records ("Leito 04 - UTI") with zero LGPD risk.
- **UI Component Layer (`src/components/`):**
  - `ThemeToggle.tsx`: tactile header Sun/Moon button with smooth transitions and system theme detection.
  - `AlphabetJumpRail.tsx`: iOS-style vertical alphabet rail on right edge with touch/drag listeners, letter balloon, and haptic feedback.
  - `AzScoreList.tsx`: scrollable A-Z directory with sticky alphabetical headers and instant search (<10ms).
  - `FavoritesView.tsx`: top quick-access chip carousel and dedicated "Favoritos" bottom navigation tab.
  - `PhysiologicalRadar.tsx`: pure native reactive SVG radar (60fps) showing green baseline polygon and patient deviation overlay.
  - `PrescriptionCard.tsx`: expandable prescription drawer with embedded BIC micro-calculator (live $mL/h$ recalculation on dose/weight input) and "Copiar para PEP" button.
  - `CalculatorView.tsx`: calculator view with summary score badge, radar, 48px touch inputs in One-Thumb zone, SSC 2021 warning banner, and BIC drawer.
  - `BottomNav.tsx`: 4-tab bottom navigation ("Todos", "Favoritos", "Leitos", "Plantão").
  - `App.tsx`: root view container orchestrating tab routing and theme.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Mobile-First Scaffolding & Setup | React 18, Vite, TypeScript, Tailwind CSS, Lucide icons, Vitest | M1 | ORIGINAL_REQUEST §R1 |
| 2 | FrontCraft Dual Theme System | Light & Dark mode (`class` strategy), `ThemeToggle.tsx`, layered shadows, system preference sync | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Clinical Data Schema & Zod Validators | Zod schemas and TypeScript types for manifest, calculators, parameters, risk tiers, and actions | M2 | ORIGINAL_REQUEST §R3, AGENTS.md |
| 4 | Block 01 Data Ingestion (Zero Truncation) | Complete monographic data for Block 01 (Emergency/ICU) in `block_01.json` with preserved Seed JSON schema | M2 | ORIGINAL_REQUEST §R3, AGENTS.md |
| 5 | Lightweight Manifest Generation | Search-optimized `manifest.json` (~30KB) indexing Brazilian clinical synonyms | M2 | ORIGINAL_REQUEST §R3, AGENTS.md |
| 6 | Calculation Engine (Scores) | Pure scoring logic for qSOFA (with SSC 2021 warning), SOFA, Wells PE, Glasgow-P / FOUR, Ranson / BISAP | M3 | ORIGINAL_REQUEST §R4 |
| 7 | Infusion BIC Engine | Vasoactive BIC rate formulas ($mL/h$), Norepinephrine in SG 5%, Vasopressin fixed dose, Nitroglycerin container rules | M3 | ORIGINAL_REQUEST §R4, AGENTS.md |
| 8 | Physiological Radar Engine | Multi-axis normalization (0 to 1) and polar-to-Cartesian projection algorithms | M3 | ORIGINAL_REQUEST §R4 |
| 9 | PEP/EHR Plain-Text Export Engine | Formatted SOAP/SBAR clinical note generator for MV Soul, Tasy, and Epimed | M3 | ORIGINAL_REQUEST §R4 |
| 10 | 100% Vitest Engine Unit Tests | Comprehensive automated unit test suite in `tests/unit/test_engines.test.ts` | M3 | ORIGINAL_REQUEST §R4 |
| 11 | Local Storage Service (IndexedDB) | Local persistence of favorites (Quick-Pins) and anonymous bed records with zero LGPD risk | M4 | ORIGINAL_REQUEST §R2, AGENTS.md |
| 12 | Instant Search (<10ms) | Client-side search indexing Brazilian clinical synonyms across names, abbreviations, and keywords | M4 | ORIGINAL_REQUEST §R2 |
| 13 | iOS-Style Alphabet Jump Rail | Vertical right-edge jump rail with touch/drag tracking, visual balloon indicator, and haptic feedback | M4 | ORIGINAL_REQUEST §R2 |
| 14 | A-Z Score List & Sticky Headers | Scrollable directory with sticky alphabetical headers and quick-filter cards | M4 | ORIGINAL_REQUEST §R2 |
| 15 | Star Favorites Carousel & Tab | Quick-access chip carousel on top and dedicated "Favoritos" bottom tab | M4 | ORIGINAL_REQUEST §R2 |
| 16 | Native Reactive SVG Physiological Radar | Pure SVG 60fps radar with baseline homeostatic polygon and dynamic patient deviation overlay | M5 | ORIGINAL_REQUEST §R5 |
| 17 | Bedside BIC Prescription Drawer | Expandable drawer with live $mL/h$ recalculation on dose/weight input and "Copiar para PEP" button | M5 | ORIGINAL_REQUEST §R5 |
| 18 | Interactive Calculator View | Full calculator screen with summary score, 48px touch inputs in One-Thumb zone, SSC 2021 warning banner | M5 | ORIGINAL_REQUEST §R5 |
| 19 | Bottom Navigation & App Assembly | 4-tab bottom navigation (`BottomNav.tsx`) integrated in `App.tsx` with responsive layout (375px-430px) | M5 | ORIGINAL_REQUEST §R5 |
| 20 | E2E Testing Suite (Tiers 1-4) | Opaque-box automated requirement-driven test suite with >=11*N test cases | E2E Track | ORIGINAL_REQUEST Acceptance Criteria |
| 21 | Final Verification & Adversarial Coverage (Tier 5) | Pass 100% E2E tests + white-box adversarial stress testing with zero regressions | M6 | ORIGINAL_REQUEST Acceptance Criteria |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Test harness, runner, and test suites (Tiers 1-4) covering all features -> publishes `TEST_READY.md` | none | IN_PROGRESS |
| M1 | Scaffolding & Theme Foundation | Setup React 18, Vite, TS, Tailwind CSS (`class` strategy), FrontCraft tokens, Vitest setup, `ThemeToggle.tsx` | none | IN_PROGRESS |
| M2 | Data Contracts & Block 01 Ingestion | `src/types/clinical.ts`, `src/types/infusion.ts`, `manifest.json`, `block_01.json` with zero truncation, Zod validation | M1 | PLANNED |
| M3 | Pure Clinical Engines & Unit Tests | Pure functions in `src/engines/` (`calculationEngine`, `infusionEngine`, `radarEngine`, `pepExportEngine`) + 100% Vitest coverage | M2 | PLANNED |
| M4 | Storage & A-Z Catalog with Jump Rail | `storageService.ts` (IndexedDB), `AlphabetJumpRail.tsx`, `AzScoreList.tsx` (<10ms search), `FavoritesView.tsx` | M2, M3 | PLANNED |
| M5 | Interactive UI, Radar SVG & BIC Drawer | `PhysiologicalRadar.tsx` (SVG 60fps), `PrescriptionCard.tsx` (live BIC + PEP copy), `CalculatorView.tsx`, `BottomNav.tsx`, `App.tsx` | M3, M4 | PLANNED |
| M6 | Final Milestone: E2E Test Pass & Hardening | Run 100% of E2E tests (Tiers 1-4) until passing, then Phase 2 adversarial coverage hardening (Tier 5) | M5, E2E | PLANNED |

---

## Interface Contracts

### M1 ↔ M2: Build Tooling & Environment
- Module bundler: Vite with ESM support.
- TypeScript config: Strict mode (`"strict": true`), path aliases `@/*` mapping to `src/*`.
- Tailwind CSS: configured with `darkMode: 'class'` and FrontCraft theme tokens (`shadow-card`, `shadow-bevel`, custom colors).

### M2 ↔ M3: Data Contracts & Pure Engines
- `CalculatorDefinition`:
  ```typescript
  interface CalculatorDefinition {
    id: string;
    name: string;
    acronym: string;
    version: string;
    category: string;
    subcategory: string;
    description: string;
    clinicalObjective: string;
    targetPopulation: string;
    ssc2021Warning?: boolean; // Required for qSOFA
    parameterGroups: ParameterGroup[];
    riskTiers: RiskTier[];
    radarAxes: RadarAxisDefinition[];
    pharmacologicalActions: PharmacologicalAction[];
    nonPharmacologicalActions: NonPharmacologicalAction[];
  }
  ```
- `CalculationResult`:
  ```typescript
  interface CalculationResult {
    score: number;
    rawValues: Record<string, any>;
    riskTier: RiskTier;
    radarPoints: Record<string, number>; // normalized [0, 1]
    warnings?: string[];
    sscWarning?: string;
  }
  ```
- `InfusionCalculation`:
  ```typescript
  interface InfusionCalculationParams {
    drugId: string;
    patientWeightKg: number;
    doseValue: number; // in mcg/kg/min, UI/min, or mcg/min
    concentrationMcgPerMl: number;
  }
  interface InfusionCalculationResult {
    rateMlPerHour: number;
    recommendedVehicle: string;
    containerAlert?: string;
    safetyAlerts: string[];
    formattedDose: string;
  }
  ```

### M3 ↔ M4 & M5: Engines ↔ UI & Storage
- `storageService`:
  ```typescript
  interface StorageService {
    getFavorites(): Promise<string[]>;
    toggleFavorite(scoreId: string): Promise<boolean>;
    isFavorite(scoreId: string): Promise<boolean>;
    getBedRecords(): Promise<BedRecord[]>;
    saveBedRecord(record: BedRecord): Promise<void>;
  }
  ```
- `PhysiologicalRadar`:
  - Input: `axes: RadarAxisDefinition[]`, `values: Record<string, number>` (normalized $0$ to $1$).
  - Output: Native reactive SVG polygon with homeostatic baseline (green) and deviation overlay (red/amber) at 60fps.
- `PrescriptionCard`:
  - Input: `drugProtocol: PharmacologicalAction`, `patientWeightKg: number`.
  - Output: Instant $mL/h$ recalculation on dose/weight input and formatted plain-text clipboard copy for EHR.

---

## Code Layout
```
/home/melki/projects/workspace/projects/scoreboard-app/
├── docs/                                  # Monographic clinical dossiers, UI tokens, protocols
├── index.html                             # HTML entry point with viewport meta
├── package.json                           # Dependencies and scripts
├── postcss.config.js                      # Tailwind PostCSS configuration
├── tailwind.config.js                     # Tailwind CSS theme configuration (FrontCraft tokens)
├── tsconfig.json                          # TypeScript configuration
├── tsconfig.node.json                     # Node/Vite TS configuration
├── vite.config.ts                         # Vite configuration with Vitest setup
├── src/
│   ├── main.tsx                           # React DOM mount point
│   ├── App.tsx                            # Root application component & routing
│   ├── index.css                          # Global styles, Tailwind imports, CSS custom properties
│   ├── types/
│   │   ├── clinical.ts                    # Zod schemas & TS types for calculators and manifest
│   │   └── infusion.ts                    # TS types for BIC infusion protocols and calculations
│   ├── data/
│   │   ├── manifest.json                  # Lightweight search index (~30KB)
│   │   └── blocks/
│   │       └── block_01.json              # Monographic clinical data for Block 01
│   ├── engines/
│   │   ├── calculationEngine.ts           # Pure clinical scoring algorithms
│   │   ├── infusionEngine.ts              # Pure BIC infusion flow rate formulas
│   │   ├── radarEngine.ts                 # Multi-axis normalization & polar math
│   │   └── pepExportEngine.ts             # Formatted SOAP/SBAR EHR copy engine
│   ├── services/
│   │   └── storageService.ts              # IndexedDB local storage for favorites & beds
│   └── components/
│       ├── common/
│       │   ├── ThemeToggle.tsx            # Header Sun/Moon theme switch
│       │   └── BottomNav.tsx              # 4-tab bottom navigation bar
│       ├── catalog/
│       │   ├── AlphabetJumpRail.tsx       # iOS-style vertical jump rail
│       │   ├── AzScoreList.tsx            # A-Z list with sticky headers & search
│       │   └── FavoritesView.tsx          # Favorites carousel & tab view
│       └── calculator/
│           ├── CalculatorView.tsx         # Main calculator screen (One-Thumb zone)
│           ├── PhysiologicalRadar.tsx     # Native reactive SVG radar (60fps)
│           ├── ParameterGroupInput.tsx    # 48px touch-friendly option cards
│           └── PrescriptionCard.tsx       # BIC micro-calculator drawer & PEP copy
└── tests/
    ├── unit/
    │   ├── test_engines.test.ts           # Pure engine unit test suite (100% coverage)
    │   └── test_storage.test.ts           # Storage service unit tests
    ├── contract/
    │   └── test_schemas.test.ts           # Zod schema validation tests
    └── e2e/
        ├── harness/                       # Test runner and fixtures
        ├── tier1_features/                # Tier 1 tests (>=5 per feature)
        ├── tier2_boundaries/              # Tier 2 tests (>=5 per feature)
        ├── tier3_combinations/            # Tier 3 tests (cross-feature)
        └── tier4_scenarios/               # Tier 4 tests (real-world clinical scenarios)
```
