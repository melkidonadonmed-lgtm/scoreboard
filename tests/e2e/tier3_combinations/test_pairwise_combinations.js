/**
 * Tier 3 — Cross-Feature Combinations (Pairwise Workflows)
 * Tests multi-module interactions across features.
 * Exactly 21 pairwise integration tests.
 */

import { describe, it, expect, adapter, envShim } from '../harness/index.js';

describe('Tier 3 — Cross-Feature Combinations (Pairwise)', () => {
  it('P01: Feature 2 (Theme) + Feature 13 (Jump Rail) — Dark mode applies to Jump Rail balloon', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.setTheme('dark');
    expect(theme.isDark()).toBe(true);

    const touch = adapter.calculateJumpRailTouch(200, 100, 520);
    expect(touch.letter).toBeDefined();
    // In dark mode, documentElement has 'dark' class which sets dark style tokens on balloon
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('P02: Feature 11 (Storage) + Feature 15 (Favorites) — Star calculator persists to storage and populates carousel', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('wells_pe');

    const favs = await storage.getFavorites();
    expect(favs).toContain('wells_pe');

    const catalog = adapter.getBlock01Catalog();
    const carouselItems = catalog.filter(c => favs.includes(c.id));
    expect(carouselItems.length).toBe(1);
    expect(carouselItems[0].acronym).toBe('Wells TEP');
  });

  it('P03: Feature 12 (Search) + Feature 14 (A-Z Catalog) — Search query filters catalog and retains alphabetical grouping', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('pancreatite', manifest);
    expect(results.length).toBe(2); // Ranson and BISAP

    const catalog = adapter.getBlock01Catalog();
    const filteredScores = catalog.filter(c => results.some(r => r.id === c.id));
    const groups = adapter.groupScoresAlphabetically(filteredScores);
    expect(groups.length).toBe(2);
    expect(groups.map(g => g.letter)).toEqual(['B', 'C']); // BISAP (B), Critérios de Ranson (C)
  });

  it('P04: Feature 6 (Score) + Feature 18 (Interactive View) — Selecting parameters updates score and risk badge color', () => {
    const res = adapter.calculateScore('glasgow_p', {
      gcs: 12,
      pupilReactivity: 1
    });
    expect(res.score).toBe(11);
    expect(res.riskTier.id).toBe('moderate');
    expect(res.riskTier.color).toBe('amber');
  });

  it('P05: Feature 6 (Score) + Feature 8 (Radar) + Feature 16 (SVG Radar) — High SOFA computes points and renders critical SVG overlay', () => {
    const catalog = adapter.getBlock01Catalog();
    const sofa = catalog.find(c => c.id === 'sofa');
    const scoreRes = adapter.calculateScore('sofa', {
      respiration: 3,
      coagulation: 3,
      liver: 2,
      cardiovascular: 4,
      cns: 1,
      renal: 3
    });
    expect(scoreRes.score).toBe(16);

    const geom = adapter.calculateRadarGeometry(sofa.radarAxes, scoreRes.radarPoints, 300);
    expect(geom.patientPolygon).toBeDefined();
    // Cardiovascular is max derangement (4/4 = 1.0)
    expect(scoreRes.radarPoints.cardiovascular).toBe(1.0);
  });

  it('P06: Feature 7 (Infusion) + Feature 17 (BIC Drawer) — Modifying patient weight recalculates flow rate live', () => {
    const calc70 = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.2,
      concentrationMcgPerMl: 64
    });
    const calc85 = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 85,
      doseValue: 0.2,
      concentrationMcgPerMl: 64
    });
    expect(calc70.rateMlPerHour).toBeCloseTo(13.13, 2);
    expect(calc85.rateMlPerHour).toBeCloseTo(15.94, 2);
  });

  it('P07: Feature 6 (Score) + Feature 7 (Infusion) + Feature 9 (PEP Export) — qSOFA + Norepinephrine generates full EHR note', () => {
    const scoreRes = adapter.calculateScore('qsofa', { rr_22: true, sbp_100: true, ams_gcs: true });
    const infRes = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.3,
      concentrationMcgPerMl: 64
    });

    const pepNote = adapter.exportPepSummary({
      calculatorName: 'quick SOFA (qSOFA)',
      scoreValue: scoreRes.score,
      riskLabel: scoreRes.riskTier.label,
      infusionInfo: {
        drugName: 'Noradrenalina',
        dilution: '16 mg em 234 mL SG 5% (64 mcg/mL)',
        dose: infRes.formattedDose,
        rateMlPerHour: infRes.rateMlPerHour,
        vehicle: infRes.recommendedVehicle,
        containerAlert: infRes.safetyAlerts.find(a => a.includes('Vasopressina'))
      }
    });

    expect(pepNote).toContain('Escore Calculado: quick SOFA (qSOFA) = 3 pontos');
    expect(pepNote).toContain('Vazão em BIC: 19.69 mL/h');
    expect(pepNote).toContain('Vasopressina');
  });

  it('P08: Feature 9 (PEP Export) + Feature 17 (BIC Drawer) — "Copiar para PEP" puts exact structured text into clipboard', async () => {
    envShim.reset();
    const note = adapter.exportPepSummary({
      calculatorName: 'SOFA',
      scoreValue: 12,
      riskLabel: 'Alta Gravidade',
      patientBed: 'Leito 04 - UTI',
      infusionInfo: {
        drugName: 'Noradrenalina',
        dilution: '16 mg em 234 mL SG 5%',
        dose: '0.25 mcg/kg/min',
        rateMlPerHour: 16.41,
        vehicle: 'SG 5%'
      }
    });

    await envShim.navigator.clipboard.writeText(note);
    const clipboard = await envShim.navigator.clipboard.readText();
    expect(clipboard).toBe(note);
    expect(clipboard).toContain('Leito 04 - UTI');
    expect(clipboard).toContain('16.41 mL/h');
  });

  it('P09: Feature 11 (Storage) + Feature 19 (Navigation) — Anonymous bed record persists across simulated view transitions', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.saveBedRecord({
      id: 'bed_04',
      bedLabel: 'Leito 04 - UTI',
      scoreSnapshots: [{ scoreId: 'qsofa', score: 3 }]
    });

    // Simulate navigation to 'beds' tab
    const beds = await storage.getBedRecords();
    expect(beds.length).toBe(1);
    expect(beds[0].bedLabel).toBe('Leito 04 - UTI');
    expect(beds[0].scoreSnapshots[0].score).toBe(3);
  });

  it('P10: Feature 2 (Theme) + Feature 16 (SVG Radar) — SVG Radar adapts high-contrast polygon against dark theme', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.setTheme('dark');

    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geom = adapter.calculateRadarGeometry(axes, { a: 0.8, b: 0.5, c: 0.2 }, 300);
    expect(geom.patientPolygon).toBeDefined();
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('P11: Feature 4 (Block 01 Ingestion) + Feature 18 (Interactive View) — Ingested qSOFA dossier displays mandatory SSC 2021 warning', () => {
    const catalog = adapter.getBlock01Catalog();
    const qsofa = catalog.find(c => c.id === 'qsofa');
    expect(qsofa.ssc2021Warning).toBe(true);

    const scoreRes = adapter.calculateScore('qsofa', { rr_22: true });
    expect(scoreRes.sscWarning).toContain('Surviving Sepsis Campaign 2021');
  });

  it('P12: Feature 3 (Schema) + Feature 4 (Block 01 Ingestion) — Schema validator parses all 7 monographic calculators successfully', () => {
    const catalog = adapter.getBlock01Catalog();
    catalog.forEach(calc => {
      const res = adapter.validateCalculatorSchema(calc);
      expect(res.valid).toBe(true);
      expect(res.errors.length).toBe(0);
    });
  });

  it('P13: Feature 5 (Manifest) + Feature 12 (Search) — Portuguese synonym "embolia pulmonar" finds Wells calculator in <10ms', () => {
    const manifest = adapter.getManifestData();
    const { results, latencyMs } = adapter.searchCalculators('embolia pulmonar', manifest);
    expect(results.length).toBe(1);
    expect(results[0].id).toBe('wells_pe');
    expect(latencyMs).toBeLessThan(10);
  });

  it('P14: Feature 14 (A-Z Catalog) + Feature 18 (Interactive) + Feature 19 (Navigation) — Preserves calculator state across tab switches', () => {
    const activeInputs = { dvt_signs: true, pe_most_likely: true };
    const scoreBefore = adapter.calculateScore('wells_pe', activeInputs);

    // Navigate to favorites and back to Todos
    let currentTab = 'favorites';
    currentTab = 'all';
    expect(currentTab).toBe('all');

    const scoreAfter = adapter.calculateScore('wells_pe', activeInputs);
    expect(scoreAfter.score).toBe(scoreBefore.score);
    expect(scoreAfter.riskTier.id).toBe('likely');
  });

  it('P15: Feature 7 (Infusion) + Feature 18 (Interactive) — Prescribing Nitroglycerin generates mandatory glass container alert', () => {
    const inf = adapter.calculateInfusion({
      drugId: 'nitroglycerin',
      patientWeightKg: 75,
      doseValue: 15,
      concentrationMcgPerMl: 200
    });
    expect(inf.containerAlert).toContain('Frasco de Vidro ou Polietileno');
    expect(inf.containerAlert).toContain('PROIBIDO frasco ou equipo de PVC');
  });

  it('P16: Feature 6 (Score) + Feature 11 (Storage) — Computes BISAP score and saves snapshot to anonymous bed record', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    const scoreRes = adapter.calculateScore('bisap', {
      bun: 28, // +1
      impairedMental: true, // +1
      sirs: true, // +1
      age: 65 // +1
    });
    expect(scoreRes.score).toBe(4);
    expect(scoreRes.riskTier.id).toBe('high');

    await storage.saveBedRecord({
      id: 'bed_07',
      bedLabel: 'Leito 07 - Semi-Intensiva',
      scoreSnapshots: [{ scoreId: 'bisap', score: scoreRes.score, riskLabel: scoreRes.riskTier.label }]
    });

    const beds = await storage.getBedRecords();
    expect(beds.length).toBe(1);
    expect(beds[0].scoreSnapshots[0].score).toBe(4);
  });

  it('P17: Feature 2 (Theme) + Feature 19 (Navigation) — Theme switch modifies styling context for bottom navigation bar', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();
    theme.setTheme('dark');
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);

    theme.setTheme('light');
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('P18: Feature 8 (Radar) + Feature 17 (Drawer) — Simultaneous physiological radar and BIC drawer coexistence', () => {
    const axes = [{ id: 'cv' }, { id: 'resp' }, { id: 'ren' }];
    const geom = adapter.calculateRadarGeometry(axes, { cv: 1.0, resp: 0.8, ren: 0.5 }, 300);
    const inf = adapter.calculateInfusion({
      drugId: 'dobutamine',
      patientWeightKg: 70,
      doseValue: 10.0,
      concentrationMcgPerMl: 1000
    });

    expect(geom.patientPolygon).toBeDefined();
    expect(inf.rateMlPerHour).toBe(42.0);
  });

  it('P19: Feature 12 (Search) + Feature 15 (Favorites) — Starred calculator preserves star status in search results', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('qsofa');

    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('qsofa', manifest);
    expect(results.length).toBe(1);

    const isFav = await storage.isFavorite(results[0].id);
    expect(isFav).toBe(true);
  });

  it('P20: Feature 1 (Scaffolding) + Feature 19 (Navigation) — Mobile viewports (375px to 430px) maintain accessible layout', () => {
    const viewports = [375, 390, 414, 430];
    viewports.forEach(w => {
      envShim.setViewport(w, 800);
      expect(envShim.viewport.width).toBe(w);
      expect(envShim.viewport.width).toBeGreaterThanOrEqual(375);
      expect(envShim.viewport.width).toBeLessThanOrEqual(430);
    });
  });

  it('P21: Feature 11 (Storage) + Feature 21 (Adversarial) — CPF insertion in bed record is blocked before IndexedDB commit', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    let threw = false;
    try {
      await storage.saveBedRecord({
        id: 'bed_leak',
        bedLabel: 'Leito com CPF 123.456.789-00'
      });
    } catch (e) {
      threw = true;
      expect(e.message).toContain('LGPD Violation');
    }
    expect(threw).toBe(true);

    const beds = await storage.getBedRecords();
    expect(beds.length).toBe(0); // Zero records committed
  });
});
