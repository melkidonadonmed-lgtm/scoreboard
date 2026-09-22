/**
 * Tier 1 — Feature Coverage: Features 1 to 5
 * Covers: Scaffolding, Dual Theme, Clinical Schemas, Block 01 Ingestion, Manifest Generation
 * Exactly 25 tests (5 per feature).
 */

import { describe, it, expect, adapter, envShim } from '../harness/index.js';

describe('Tier 1 — Feature 1: Mobile-First Scaffolding & Setup', () => {
  it('F01-1: Verifies viewport meta tag is configured for mobile scaling', () => {
    const info = adapter.getScaffoldingInfo();
    expect(info.hasViewport).toBe(true);
  });

  it('F01-2: Verifies core production dependencies in package.json', () => {
    const { pkg } = adapter.getScaffoldingInfo();
    expect(pkg).toBeDefined();
    expect(pkg.dependencies).toHaveProperty('react');
    expect(pkg.dependencies).toHaveProperty('react-dom');
    expect(pkg.dependencies).toHaveProperty('zod');
    expect(pkg.dependencies).toHaveProperty('idb');
    expect(pkg.dependencies).toHaveProperty('lucide-react');
  });

  it('F01-3: Verifies Tailwind CSS configuration with FrontCraft theme tokens', () => {
    const info = adapter.getScaffoldingInfo();
    expect(info.hasFrontcraftTokens).toBe(true);
  });

  it('F01-4: Verifies dark mode strategy is configured as "class"', () => {
    const info = adapter.getScaffoldingInfo();
    expect(info.supportsDarkModeClass).toBe(true);
  });

  it('F01-5: Verifies build and test scripts are defined in package.json', () => {
    const { pkg } = adapter.getScaffoldingInfo();
    expect(pkg.scripts).toBeDefined();
    expect(pkg.scripts.build).toContain('vite build');
    expect(pkg.scripts.test).toContain('vitest');
  });
});

describe('Tier 1 — Feature 2: FrontCraft Dual Theme System', () => {
  it('F02-1: Initializes theme system with light mode default when no preference is saved', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.init();
    expect(theme.isDark()).toBe(false);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('F02-2: Toggling theme adds "dark" class to documentElement', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.init();
    const isNowDark = theme.toggleTheme();
    expect(isNowDark).toBe(true);
    expect(theme.isDark()).toBe(true);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('F02-3: Persists selected theme in localStorage', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.setTheme('dark');
    expect(theme.getSavedTheme()).toBe('dark');
    expect(envShim.localStorage.getItem('scoreboard_theme')).toBe('dark');
  });

  it('F02-4: Honors system preference (prefers-color-scheme: dark) when not explicitly set', () => {
    envShim.reset();
    envShim.setColorScheme('dark');
    const theme = adapter.createThemeSystem();
    theme.init();
    expect(theme.isDark()).toBe(true);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('F02-5: Switching back to light removes "dark" class and updates storage', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.setTheme('dark');
    expect(theme.isDark()).toBe(true);
    theme.setTheme('light');
    expect(theme.isDark()).toBe(false);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(false);
    expect(theme.getSavedTheme()).toBe('light');
  });
});

describe('Tier 1 — Feature 3: Clinical Data Schema & Zod Validators', () => {
  it('F03-1: Validates a complete CalculatorDefinition structure', () => {
    const catalog = adapter.getBlock01Catalog();
    const qsofa = catalog.find(c => c.id === 'qsofa');
    const result = adapter.validateCalculatorSchema(qsofa);
    expect(result.valid).toBe(true);
    expect(result.errors.length).toBe(0);
  });

  it('F03-2: Validates parameter groups and parameter attributes', () => {
    const catalog = adapter.getBlock01Catalog();
    const sofa = catalog.find(c => c.id === 'sofa');
    expect(sofa.parameterGroups.length).toBe(6);
    sofa.parameterGroups.forEach(group => {
      expect(group.id).toBeDefined();
      expect(group.name).toBeDefined();
      expect(Array.isArray(group.parameters)).toBe(true);
      expect(group.parameters.length).toBeGreaterThan(0);
    });
  });

  it('F03-3: Validates risk tiers for non-overlapping logical ranges', () => {
    const catalog = adapter.getBlock01Catalog();
    const wells = catalog.find(c => c.id === 'wells_pe');
    expect(wells.riskTiers.length).toBe(2);
    const [unlikely, likely] = wells.riskTiers;
    expect(unlikely.minScore).toBe(0);
    expect(unlikely.maxScore).toBe(4.0);
    expect(likely.minScore).toBeGreaterThan(unlikely.maxScore);
  });

  it('F03-4: Validates radar axes definition and baselines', () => {
    const catalog = adapter.getBlock01Catalog();
    const sofa = catalog.find(c => c.id === 'sofa');
    expect(Array.isArray(sofa.radarAxes)).toBe(true);
    expect(sofa.radarAxes.length).toBe(6);
    sofa.radarAxes.forEach(axis => {
      expect(axis.baseline).toBe(0);
      expect(axis.max).toBe(4);
    });
  });

  it('F03-5: Validates pharmacological actions and dilution protocols', () => {
    const catalog = adapter.getBlock01Catalog();
    const qsofa = catalog.find(c => c.id === 'qsofa');
    expect(qsofa.pharmacologicalActions.length).toBeGreaterThan(0);
    const nora = qsofa.pharmacologicalActions.find(a => a.drugId === 'norepinephrine');
    expect(nora).toBeDefined();
    expect(nora.concentrationMcgPerMl).toBe(64);
    expect(nora.vehicle).toContain('SG 5%');
  });
});

describe('Tier 1 — Feature 4: Block 01 Data Ingestion (Zero Truncation)', () => {
  it('F04-1: Preserves all 7 monographic calculators in Block 01 without loss', () => {
    const catalog = adapter.getBlock01Catalog();
    expect(catalog.length).toBe(7);
    const ids = catalog.map(c => c.id);
    expect(ids).toContain('qsofa');
    expect(ids).toContain('sofa');
    expect(ids).toContain('wells_pe');
    expect(ids).toContain('glasgow_p');
    expect(ids).toContain('four_score');
    expect(ids).toContain('ranson');
    expect(ids).toContain('bisap');
  });

  it('F04-2: Preserves mandatory Surviving Sepsis Campaign 2021 warning on qSOFA', () => {
    const catalog = adapter.getBlock01Catalog();
    const qsofa = catalog.find(c => c.id === 'qsofa');
    expect(qsofa.ssc2021Warning).toBe(true);
    expect(qsofa.ssc2021WarningMessage).toContain('Surviving Sepsis Campaign 2021');
    expect(qsofa.ssc2021WarningMessage).toContain('baixa sensibilidade');
  });

  it('F04-3: Preserves all 6 organ systems in Full SOFA', () => {
    const catalog = adapter.getBlock01Catalog();
    const sofa = catalog.find(c => c.id === 'sofa');
    const groupIds = sofa.parameterGroups.map(g => g.id);
    expect(groupIds).toContain('respiration');
    expect(groupIds).toContain('coagulation');
    expect(groupIds).toContain('liver');
    expect(groupIds).toContain('cardiovascular');
    expect(groupIds).toContain('cns');
    expect(groupIds).toContain('renal');
  });

  it('F04-4: Preserves complete Wells PE criteria and age-adjusted cut-off guidance', () => {
    const catalog = adapter.getBlock01Catalog();
    const wells = catalog.find(c => c.id === 'wells_pe');
    const params = wells.parameterGroups[0].parameters;
    expect(params.length).toBe(7);
    const dvt = params.find(p => p.id === 'dvt_signs');
    expect(dvt.points).toBe(3.0);
    const tach = params.find(p => p.id === 'tachycardia');
    expect(tach.points).toBe(1.5);
    expect(wells.riskTiers[0].interpretation).toContain('Idade x 10');
  });

  it('F04-5: Preserves both admission and 48-hour criteria for Ranson acute pancreatitis', () => {
    const catalog = adapter.getBlock01Catalog();
    const ranson = catalog.find(c => c.id === 'ranson');
    expect(ranson.parameterGroups.length).toBe(2);
    expect(ranson.parameterGroups[0].id).toBe('admission');
    expect(ranson.parameterGroups[1].id).toBe('forty_eight_hours');
    expect(ranson.parameterGroups[0].parameters.length).toBe(5);
    expect(ranson.parameterGroups[1].parameters.length).toBe(6);
  });
});

describe('Tier 1 — Feature 5: Lightweight Manifest Generation', () => {
  it('F05-1: Manifest structure size conforms to the ~30KB lightweight limit', () => {
    const manifest = adapter.getManifestData();
    const jsonStr = JSON.stringify(manifest);
    const sizeKb = Buffer.byteLength(jsonStr, 'utf8') / 1024;
    expect(sizeKb).toBeLessThan(35); // strictly under 35KB
  });

  it('F05-2: Manifest indexes required search attributes for each calculator', () => {
    const manifest = adapter.getManifestData();
    expect(manifest.calculators.length).toBe(7);
    manifest.calculators.forEach(calc => {
      expect(calc.id).toBeDefined();
      expect(calc.name).toBeDefined();
      expect(calc.acronym).toBeDefined();
      expect(calc.category).toBeDefined();
      expect(calc.blockId).toBe('block_01');
    });
  });

  it('F05-3: Manifest indexes Brazilian clinical synonyms for rapid localized lookup', () => {
    const manifest = adapter.getManifestData();
    const wells = manifest.calculators.find(c => c.id === 'wells_pe');
    expect(wells.synonyms).toContain('tromboembolismo pulmonar');
    expect(wells.synonyms).toContain('tep');
    expect(wells.synonyms).toContain('embolia pulmonar');
  });

  it('F05-4: Manifest indexes emergency and ICU category tags', () => {
    const manifest = adapter.getManifestData();
    const qsofa = manifest.calculators.find(c => c.id === 'qsofa');
    expect(qsofa.tags).toContain('qSOFA');
    expect(qsofa.category).toContain('Terapia Intensiva');
  });

  it('F05-5: Manifest contains build metadata and block count', () => {
    const manifest = adapter.getManifestData();
    expect(manifest.version).toBe('1.0.0');
    expect(manifest.blockCount).toBe(1);
    expect(manifest.totalCalculators).toBe(7);
    expect(manifest.updatedAt).toBeDefined();
  });
});
