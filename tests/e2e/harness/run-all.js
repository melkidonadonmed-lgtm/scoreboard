#!/usr/bin/env node
/**
 * Master E2E Test Suite Runner for Scoreboard App Phase 1
 * Executes all 4 test tiers (Tiers 1-4) across 21 features.
 * Usage: node tests/e2e/harness/run-all.js
 */

import { runner } from './index.js';

// Tier 1 — Isolated Feature Coverage (Features 1 to 21: 105 tests)
import '../tier1_features/test_f01_f05_scaffolding_data.js';
import '../tier1_features/test_f06_f10_engines_pep.js';
import '../tier1_features/test_f11_f15_storage_catalog.js';
import '../tier1_features/test_f16_f21_ui_verification.js';

// Tier 2 — Boundary & Corner Cases (Features 1 to 21: 105 tests)
import '../tier2_boundaries/test_b01_b05_boundaries.js';
import '../tier2_boundaries/test_b06_b10_boundaries.js';
import '../tier2_boundaries/test_b11_b15_boundaries.js';
import '../tier2_boundaries/test_b16_b21_boundaries.js';

// Tier 3 — Cross-Feature Combinations (Pairwise: 21 tests)
import '../tier3_combinations/test_pairwise_combinations.js';

// Tier 4 — Real-World Clinical Application Scenarios (11 scenarios)
import '../tier4_scenarios/test_clinical_scenarios.js';

async function main() {
  const results = await runner.run();
  if (results.failed > 0) {
    process.exitCode = 1;
  }
}

main().catch(err => {
  console.error('Fatal test runner error:', err);
  process.exit(1);
});
