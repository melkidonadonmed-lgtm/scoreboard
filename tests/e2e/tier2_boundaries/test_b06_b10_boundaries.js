/**
 * Tier 2 — Boundary & Corner Cases: Features 6 to 10
 * Exactly 25 tests (5 per feature).
 */

import { describe, it, expect, adapter } from '../harness/index.js';

describe('Tier 2 — Feature 6 Boundaries: Clinical Scoring Extreme Values', () => {
  it('B06-1: All maximum organ failure points in SOFA evaluates to max score 24', () => {
    const res = adapter.calculateScore('sofa', {
      respiration: 4,
      coagulation: 4,
      liver: 4,
      cardiovascular: 4,
      cns: 4,
      renal: 4
    });
    expect(res.score).toBe(24);
    expect(res.riskTier.id).toBe('sofa_crit');
    expect(res.riskTier.color).toBe('rose');
    Object.values(res.radarPoints).forEach(val => expect(val).toBe(1.0));
  });

  it('B06-2: Glasgow-P lower boundary: GCS 3 with fixed bilateral pupils evaluates to score 1', () => {
    const res = adapter.calculateScore('glasgow_p', {
      gcs: 3,
      pupilReactivity: 2
    });
    expect(res.score).toBe(1); // GCS 3 - 2 = 1 (lower bound of scale)
    expect(res.riskTier.id).toBe('severe');
  });

  it('B06-3: Ranson criteria correctly switches age threshold between biliary and non-biliary', () => {
    // Non-biliary age threshold > 55
    const nonBiliaryAge56 = adapter.calculateScore('ranson', { isBiliary: false, age: 56 });
    expect(nonBiliaryAge56.score).toBe(1);
    const nonBiliaryAge55 = adapter.calculateScore('ranson', { isBiliary: false, age: 55 });
    expect(nonBiliaryAge55.score).toBe(0);

    // Biliary age threshold > 70
    const biliaryAge60 = adapter.calculateScore('ranson', { isBiliary: true, age: 60 });
    expect(biliaryAge60.score).toBe(0); // 60 is <= 70
    const biliaryAge71 = adapter.calculateScore('ranson', { isBiliary: true, age: 71 });
    expect(biliaryAge71.score).toBe(1);
  });

  it('B06-4: BISAP BUN threshold strictly evaluates > 25 mg/dL boundary', () => {
    const atThreshold = adapter.calculateScore('bisap', { bun: 25.0 });
    expect(atThreshold.score).toBe(0); // must be > 25
    const aboveThreshold = adapter.calculateScore('bisap', { bun: 25.1 });
    expect(aboveThreshold.score).toBe(1);
  });

  it('B06-5: Wells PE threshold boundary strictly splits at 4.0 points', () => {
    // Score exactly 4.0 -> TEP Improvável
    const score4 = adapter.calculateScore('wells_pe', { dvt_signs: true, hemoptysis: true }); // 3.0 + 1.0 = 4.0
    expect(score4.score).toBe(4.0);
    expect(score4.riskTier.id).toBe('unlikely');

    // Score 4.5 -> TEP Provável
    const score4_5 = adapter.calculateScore('wells_pe', { dvt_signs: true, tachycardia: true }); // 3.0 + 1.5 = 4.5
    expect(score4_5.score).toBe(4.5);
    expect(score4_5.riskTier.id).toBe('likely');
  });
});

describe('Tier 2 — Feature 7 Boundaries: BIC Infusion Edge Cases', () => {
  it('B07-1: Computes Norepinephrine infusion for cachectic 30kg patient accurately', () => {
    // 0.1 mcg/kg/min * 30kg * 60 / 64 = 180 / 64 = 2.8125 mL/h
    const calc = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 30,
      doseValue: 0.1,
      concentrationMcgPerMl: 64
    });
    expect(calc.rateMlPerHour).toBeCloseTo(2.81, 2);
  });

  it('B07-2: Computes Norepinephrine infusion for bariatric 300kg patient accurately', () => {
    // 0.1 mcg/kg/min * 300kg * 60 / 64 = 1800 / 64 = 28.125 mL/h
    const calc = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 300,
      doseValue: 0.1,
      concentrationMcgPerMl: 64
    });
    expect(calc.rateMlPerHour).toBeCloseTo(28.13, 2);
  });

  it('B07-3: Vasopressin dose outside standard range (e.g. 0.06 UI/min) triggers safety warning', () => {
    const calc = adapter.calculateInfusion({
      drugId: 'vasopressin',
      patientWeightKg: 70,
      doseValue: 0.06,
      concentrationUiPerMl: 0.2
    });
    expect(calc.rateMlPerHour).toBe(18.0);
    const hasAlert = calc.safetyAlerts.some(a => a.includes('A dose recomendada de Vasopressina'));
    expect(hasAlert).toBe(true);
  });

  it('B07-4: Dobutamine dose at ceiling (20 mcg/kg/min) evaluates correctly', () => {
    // 20 mcg/kg/min * 70kg * 60 / 1000 = 84.0 mL/h
    const calc = adapter.calculateInfusion({
      drugId: 'dobutamine',
      patientWeightKg: 70,
      doseValue: 20.0,
      concentrationMcgPerMl: 1000
    });
    expect(calc.rateMlPerHour).toBe(84.0);
  });

  it('B07-5: Nitroglycerin at maximum recommended titration (200 mcg/min)', () => {
    // 200 mcg/min * 60 / 200 mcg/mL = 60.0 mL/h
    const calc = adapter.calculateInfusion({
      drugId: 'nitroglycerin',
      patientWeightKg: 70,
      doseValue: 200,
      concentrationMcgPerMl: 200
    });
    expect(calc.rateMlPerHour).toBe(60.0);
    expect(calc.containerAlert).toContain('PROIBIDO frasco ou equipo de PVC');
  });
});

describe('Tier 2 — Feature 8 Boundaries: Radar Normalization Corners', () => {
  it('B08-1: All zero values generate homeostatic baseline polygon without null coordinates', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geom = adapter.calculateRadarGeometry(axes, { a: 0, b: 0, c: 0 }, 300);
    expect(geom.patientPolygon).toBeDefined();
    geom.patientPolygon.split(' ').forEach(coord => {
      const [x, y] = coord.split(',').map(Number);
      expect(isNaN(x)).toBe(false);
      expect(isNaN(y)).toBe(false);
    });
  });

  it('B08-2: All max values (1.0) expand polygon to maximum outer radius', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }, { id: 'd' }];
    const geom = adapter.calculateRadarGeometry(axes, { a: 1.0, b: 1.0, c: 1.0, d: 1.0 }, 300);
    expect(geom.patientPolygon).toBeDefined();
    geom.patientPolygon.split(' ').forEach(coord => {
      const [x, y] = coord.split(',').map(Number);
      const distFromCenter = Math.hypot(x - geom.cx, y - geom.cy);
      expect(distFromCenter).toBeCloseTo(geom.radius, 1);
    });
  });

  it('B08-3: Single isolated axis derangement projects asymmetric spike', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geom = adapter.calculateRadarGeometry(axes, { a: 1.0, b: 0.0, c: 0.0 }, 300);
    const [pA, pB, pC] = geom.patientPolygon.split(' ');
    expect(pA).not.toBe(pB);
    expect(pB).not.toBe(pC);
  });

  it('B08-4: Negative input values are clamped to 0.0 without distortion', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geomNeg = adapter.calculateRadarGeometry(axes, { a: -5.0, b: -1.0, c: -0.5 }, 300);
    const geomZero = adapter.calculateRadarGeometry(axes, { a: 0.0, b: 0.0, c: 0.0 }, 300);
    expect(geomNeg.patientPolygon).toBe(geomZero.patientPolygon);
  });

  it('B08-5: Values exceeding 1.0 are clamped to 1.0 outer perimeter', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geomOver = adapter.calculateRadarGeometry(axes, { a: 2.5, b: 99.0, c: 1.1 }, 300);
    const geomMax = adapter.calculateRadarGeometry(axes, { a: 1.0, b: 1.0, c: 1.0 }, 300);
    expect(geomOver.patientPolygon).toBe(geomMax.patientPolygon);
  });
});

describe('Tier 2 — Feature 9 Boundaries: PEP Export Note Formatting', () => {
  it('B09-1: Formats note cleanly when patient bed is unspecified', () => {
    const note = adapter.exportPepSummary({
      calculatorName: 'SOFA',
      scoreValue: 4,
      riskLabel: 'Baixa Gravidade'
    });
    expect(note).toContain('PACIENTE: Não informado');
  });

  it('B09-2: Omits empty bullet points when recommendations array is empty', () => {
    const note = adapter.exportPepSummary({
      calculatorName: 'qSOFA',
      scoreValue: 0,
      riskLabel: 'Baixo Risco',
      recommendations: []
    });
    expect(note).not.toContain('1. undefined');
    expect(note).not.toContain('1. null');
  });

  it('B09-3: Omits BIC section cleanly when no vasoactive infusion is prescribed', () => {
    const note = adapter.exportPepSummary({
      calculatorName: 'Wells TEP',
      scoreValue: 1.0,
      riskLabel: 'TEP Improvável',
      infusionInfo: null
    });
    expect(note).not.toContain('Bomba de Infusão Contínua (BIC)');
  });

  it('B09-4: Preserves special Portuguese symbols and units in UTF-8 output', () => {
    const note = adapter.exportPepSummary({
      calculatorName: 'qSOFA',
      scoreValue: 2,
      riskLabel: 'Alto Risco (≥ 2 pontos)',
      recommendations: ['PAM alvo ≥ 65 mmHg', 'Lactato sérico ≤ 2 mmol/L']
    });
    expect(note).toContain('≥');
    expect(note).toContain('≤');
  });

  it('B09-5: Handles long multiline clinical notes without breaking section delimiters', () => {
    const note = adapter.exportPepSummary({
      calculatorName: 'SOFA',
      scoreValue: 15,
      riskLabel: 'Falência Crítica',
      riskInterpretation: 'Paciente intubado sob sedoanalgesia profunda, hipotenso refratário a noradrenalina em dose elevada, oligúrico nas últimas 6h com elevação aguda de escórias nitrogenadas.'
    });
    expect(note).toContain('S (Subjetivo):');
    expect(note).toContain('O (Objetivo):');
    expect(note).toContain('A (Avaliação):');
    expect(note).toContain('P (Plano / Condutas):');
  });
});

describe('Tier 2 — Feature 10 Boundaries: Pure Engine Robustness', () => {
  it('B10-1: Rejects zero concentration to avoid division-by-zero errors', () => {
    expect(() => {
      adapter.calculateInfusion({
        drugId: 'norepinephrine',
        patientWeightKg: 70,
        doseValue: 0.1,
        concentrationMcgPerMl: 0
      });
    }).toThrow('Concentration must be positive');
  });

  it('B10-2: Non-numeric strings in inputs are sanitized to 0 points', () => {
    const res = adapter.calculateScore('sofa', {
      respiration: 'high',
      cardiovascular: 'unknown'
    });
    expect(res.score).toBe(0);
  });

  it('B10-3: Throws descriptive error on negative patient weight', () => {
    expect(() => {
      adapter.calculateInfusion({
        drugId: 'dobutamine',
        patientWeightKg: -10,
        doseValue: 5.0
      });
    }).toThrow('Patient weight must be greater than zero');
  });

  it('B10-4: Throws descriptive error for unsupported drug IDs', () => {
    expect(() => {
      adapter.calculateInfusion({
        drugId: 'unsupported_drug',
        patientWeightKg: 70,
        doseValue: 1
      });
    }).toThrow('Unsupported drug ID');
  });

  it('B10-5: Throws descriptive error for unknown score IDs', () => {
    expect(() => {
      adapter.calculateScore('non_existent_score', {});
    }).toThrow('Unknown score ID');
  });
});
