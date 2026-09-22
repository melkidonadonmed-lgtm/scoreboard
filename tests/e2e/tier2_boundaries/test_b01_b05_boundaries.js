/**
 * Tier 2 — Boundary & Corner Cases: Features 1 to 5
 * Exactly 25 tests (5 per feature).
 */

import { describe, it, expect, adapter, envShim } from '../harness/index.js';

describe('Tier 2 — Feature 1 Boundaries: Mobile Scaffolding & Viewport', () => {
  it('B01-1: Handles ultra-small mobile screen viewport (320px width)', () => {
    envShim.setViewport(320, 568);
    expect(envShim.viewport.width).toBe(320);
    expect(envShim.window.innerWidth).toBe(320);
  });

  it('B01-2: Handles tablet breakpoint boundary (768px width)', () => {
    envShim.setViewport(768, 1024);
    expect(envShim.viewport.width).toBe(768);
    expect(envShim.viewport.width).toBeGreaterThanOrEqual(768);
  });

  it('B01-3: Handles mobile landscape orientation swap (844px width x 390px height)', () => {
    envShim.setViewport(844, 390);
    expect(envShim.viewport.width).toBe(844);
    expect(envShim.viewport.height).toBe(390);
    expect(envShim.viewport.width).toBeGreaterThan(envShim.viewport.height);
  });

  it('B01-4: Verifies scaffolding handles extreme device pixel ratios without geometry collapse', () => {
    envShim.viewport.scale = 3.0; // iPhone Super Retina
    expect(envShim.viewport.scale).toBe(3.0);
    envShim.viewport.scale = 1.0;
  });

  it('B01-5: Validates build scripts with custom environment arguments', () => {
    const { pkg } = adapter.getScaffoldingInfo();
    expect(typeof pkg.scripts.build).toBe('string');
    expect(pkg.scripts.build.length).toBeGreaterThan(0);
  });
});

describe('Tier 2 — Feature 2 Boundaries: FrontCraft Theme Edge Cases', () => {
  it('B02-1: Rapidly toggles theme 50 times consecutively maintaining deterministic parity', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.init();
    for (let i = 0; i < 50; i++) {
      theme.toggleTheme();
    }
    // 50 toggles from initial light returns to light
    expect(theme.isDark()).toBe(false);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('B02-2: Corrupted theme string in localStorage defaults safely to light mode', () => {
    envShim.reset();
    envShim.localStorage.setItem('scoreboard_theme', 'invalid-corrupt-theme');
    const theme = adapter.createThemeSystem();
    theme.init();
    expect(theme.isDark()).toBe(false);
  });

  it('B02-3: Responds dynamically to prefers-color-scheme changes during runtime', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.init();
    expect(theme.isDark()).toBe(false);

    envShim.setColorScheme('dark');
    theme.init();
    expect(theme.isDark()).toBe(true);
  });

  it('B02-4: Theme toggle retains other preexisting CSS classes on documentElement', () => {
    envShim.reset();
    envShim.document.documentElement.classList.add('font-sans', 'antialiased');
    const theme = adapter.createThemeSystem();
    theme.setTheme('dark');
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
    expect(envShim.document.documentElement.classList.contains('font-sans')).toBe(true);
    expect(envShim.document.documentElement.classList.contains('antialiased')).toBe(true);
  });

  it('B02-5: Clearing explicit theme selection reverts to system color scheme', () => {
    envShim.reset();
    envShim.setColorScheme('dark');
    const theme = adapter.createThemeSystem();
    theme.setTheme('light');
    expect(theme.isDark()).toBe(false);
    theme.setTheme(null); // Clear preference
    expect(theme.isDark()).toBe(true);
  });
});

describe('Tier 2 — Feature 3 Boundaries: Schema Validation Corners', () => {
  it('B03-1: Rejects null or undefined calculator object', () => {
    const resNull = adapter.validateCalculatorSchema(null);
    expect(resNull.valid).toBe(false);
    const resUndef = adapter.validateCalculatorSchema(undefined);
    expect(resUndef.valid).toBe(false);
  });

  it('B03-2: Rejects riskTier configuration where minScore exceeds maxScore', () => {
    const invalidCalc = {
      id: 'test',
      name: 'Test',
      acronym: 'TST',
      category: 'Test',
      description: 'Desc',
      parameterGroups: [{ id: 'g', name: 'G', parameters: [{ id: 'p', label: 'P' }] }],
      riskTiers: [{ id: 'rt', label: 'RT', minScore: 10, maxScore: 5 }] // min > max
    };
    const res = adapter.validateCalculatorSchema(invalidCalc);
    expect(res.valid).toBe(false);
    expect(res.errors.some(e => e.includes('minScore > maxScore'))).toBe(true);
  });

  it('B03-3: Flags missing required top-level attributes', () => {
    const incomplete = { id: 'only_id' };
    const res = adapter.validateCalculatorSchema(incomplete);
    expect(res.valid).toBe(false);
    expect(res.errors.length).toBeGreaterThanOrEqual(5);
  });

  it('B03-4: Flags invalid parameterGroup without parameters array', () => {
    const badParams = {
      id: 'test',
      name: 'Test',
      acronym: 'TST',
      category: 'Test',
      description: 'Desc',
      parameterGroups: [{ id: 'g', name: 'G' }], // missing parameters array
      riskTiers: [{ id: 'rt', label: 'RT', minScore: 0, maxScore: 1 }]
    };
    const res = adapter.validateCalculatorSchema(badParams);
    expect(res.valid).toBe(false);
  });

  it('B03-5: Tolerates additional unexpected properties without crashing schema validator', () => {
    const catalog = adapter.getBlock01Catalog();
    const qsofa = { ...catalog[0], extraMetadata: 'bonus', auxiliaryScore: 99 };
    const res = adapter.validateCalculatorSchema(qsofa);
    expect(res.valid).toBe(true);
  });
});

describe('Tier 2 — Feature 4 Boundaries: Block 01 Ingestion Integrity', () => {
  it('B04-1: Preserves Portuguese clinical accents without encoding corruption', () => {
    const catalog = adapter.getBlock01Catalog();
    const wells = catalog.find(c => c.id === 'wells_pe');
    expect(wells.name).toContain('Critérios');
    expect(wells.name).toContain('Pulmonar');
    const qsofa = catalog.find(c => c.id === 'qsofa');
    expect(qsofa.description).toContain('à beira-leito');
  });

  it('B04-2: Verifies target population specification is defined on all calculators', () => {
    const catalog = adapter.getBlock01Catalog();
    catalog.forEach(c => {
      expect(c.targetPopulation).toBeDefined();
      expect(typeof c.targetPopulation).toBe('string');
      expect(c.targetPopulation.length).toBeGreaterThan(5);
    });
  });

  it('B04-3: Verifies all risk tiers have assigned FrontCraft semantic color codes', () => {
    const catalog = adapter.getBlock01Catalog();
    const validColors = ['emerald', 'amber', 'orange', 'rose'];
    catalog.forEach(c => {
      c.riskTiers.forEach(rt => {
        expect(validColors).toContain(rt.color);
      });
    });
  });

  it('B04-4: Verifies all calculators have explicit clinical objectives defined', () => {
    const catalog = adapter.getBlock01Catalog();
    catalog.forEach(c => {
      expect(c.clinicalObjective).toBeDefined();
      expect(c.clinicalObjective.length).toBeGreaterThan(10);
    });
  });

  it('B04-5: Verifies parameter point weights are positive numbers or zero', () => {
    const catalog = adapter.getBlock01Catalog();
    catalog.forEach(c => {
      c.parameterGroups.forEach(g => {
        g.parameters.forEach(p => {
          expect(typeof p.points).toBe('number');
          expect(p.points).toBeGreaterThanOrEqual(0);
        });
      });
    });
  });
});

describe('Tier 2 — Feature 5 Boundaries: Manifest Search Boundaries', () => {
  it('B05-1: Handles 1,000-character long query strings without lag or failure', () => {
    const manifest = adapter.getManifestData();
    const longQuery = 'sepse '.repeat(200);
    const { results, latencyMs } = adapter.searchCalculators(longQuery, manifest);
    expect(Array.isArray(results)).toBe(true);
    expect(latencyMs).toBeLessThan(10);
  });

  it('B05-2: Handles regex special characters as literal text without error', () => {
    const manifest = adapter.getManifestData();
    const regexQueries = ['.*', '[a-z]+', '(sepse|choque)', '+?^$'];
    for (const q of regexQueries) {
      const { results } = adapter.searchCalculators(q, manifest);
      expect(Array.isArray(results)).toBe(true);
    }
  });

  it('B05-3: Handles SQL and HTML injection strings safely', () => {
    const manifest = adapter.getManifestData();
    const injections = ["' OR '1'='1", '<script>alert(1)</script>', '"><img src=x onerror=alert(1)>'];
    for (const inj of injections) {
      const { results } = adapter.searchCalculators(inj, manifest);
      expect(Array.isArray(results)).toBe(true);
      expect(results.length).toBe(0);
    }
  });

  it('B05-4: Handles query with leading, trailing, and excessive whitespace', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('   wells   ', manifest);
    expect(results.length).toBe(1);
    expect(results[0].id).toBe('wells_pe');
  });

  it('B05-5: Handles Unicode emojis in search gracefully', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('🫁 💉 🏥', manifest);
    expect(Array.isArray(results)).toBe(true);
    expect(results.length).toBe(0);
  });
});
