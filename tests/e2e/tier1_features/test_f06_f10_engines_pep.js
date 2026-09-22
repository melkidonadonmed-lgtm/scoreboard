/**
 * Tier 1 — Feature Coverage: Features 6 to 10
 * Covers: Score Engine, Infusion BIC Engine, Radar Engine, PEP Export Engine, Engine Unit Tests
 * Exactly 25 tests (5 per feature).
 */

import { describe, it, expect, adapter } from '../harness/index.js';

describe('Tier 1 — Feature 6: Calculation Engine (Scores)', () => {
  it('F06-1: Computes qSOFA score and identifies high-risk threshold', () => {
    const result = adapter.calculateScore('qsofa', {
      rr_22: true,
      sbp_100: true,
      ams_gcs: false
    });
    expect(result.score).toBe(2);
    expect(result.riskTier.id).toBe('high');
    expect(result.riskTier.color).toBe('rose');
    expect(result.sscWarning).toContain('Surviving Sepsis Campaign 2021');
  });

  it('F06-2: Computes Full SOFA score sum across all 6 organ systems', () => {
    const result = adapter.calculateScore('sofa', {
      respiration: 2,
      coagulation: 1,
      liver: 1,
      cardiovascular: 3,
      cns: 2,
      renal: 2
    });
    expect(result.score).toBe(11);
    expect(result.riskTier.id).toBe('sofa_high');
    expect(result.radarPoints.cardiovascular).toBe(0.75);
    expect(result.radarPoints.coagulation).toBe(0.25);
  });

  it('F06-3: Computes Wells PE score and differentiates probability tiers', () => {
    const resultUnlikely = adapter.calculateScore('wells_pe', {
      tachycardia: true,
      hemoptysis: true,
      age: 65
    }); // 1.5 + 1.0 = 2.5 (<= 4.0 -> unlikely)
    expect(resultUnlikely.score).toBe(2.5);
    expect(resultUnlikely.riskTier.id).toBe('unlikely');
    expect(resultUnlikely.riskTier.dDimerRecommended).toBe(true);
    expect(resultUnlikely.riskTier.dDimerCutoff).toBe(650); // Age (65) * 10

    const resultLikely = adapter.calculateScore('wells_pe', {
      dvt_signs: true,
      pe_most_likely: true
    }); // 3.0 + 3.0 = 6.0 (> 4.0 -> likely)
    expect(resultLikely.score).toBe(6.0);
    expect(resultLikely.riskTier.id).toBe('likely');
    expect(resultLikely.riskTier.angioTcRecommended).toBe(true);
  });

  it('F06-4: Computes Glasgow-P by subtracting pupil reactivity from GCS', () => {
    const result = adapter.calculateScore('glasgow_p', {
      gcs: 10,
      pupilReactivity: 1 // 1 pupil non-reactive
    });
    expect(result.score).toBe(9);
    expect(result.riskTier.id).toBe('moderate');
    expect(result.riskTier.color).toBe('amber');
  });

  it('F06-5: Computes Ranson criteria with BUN/Ureia conversion support', () => {
    const result = adapter.calculateScore('ranson', {
      isBiliary: false,
      age: 60, // +1
      wbc: 17000, // +1
      glucose: 210, // +1
      ast: 260, // +1
      ldh: 300, // 0
      hctFall: 12, // +1
      ureiaRise: 15, // 15 / 2.14 = 7.0 mg/dL BUN rise (> 5 -> +1)
      calcium: 7.5, // +1
      pao2: 55, // +1
      baseDeficit: 5, // +1
      fluidSequestration: 7 // +1
    });
    expect(result.score).toBe(10);
    expect(result.riskTier.id).toBe('severe');
    expect(result.riskTier.mortality).toContain('> 50%');
  });
});

describe('Tier 1 — Feature 7: Infusion BIC Engine', () => {
  it('F07-1: Computes Norepinephrine infusion flow rate for patient weight and concentration', () => {
    // 0.1 mcg/kg/min * 70kg * 60 / 64 mcg/mL = 420 / 64 = 6.5625 mL/h
    const result = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.1,
      concentrationMcgPerMl: 64
    });
    expect(result.rateMlPerHour).toBeCloseTo(6.56, 2);
    expect(result.recommendedVehicle).toContain('SG 5%');
    expect(result.formattedDose).toBe('0.1 mcg/kg/min');
  });

  it('F07-2: Generates refractory vasoplegia alert when Norepinephrine exceeds 0.25 mcg/kg/min', () => {
    const result = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.35,
      concentrationMcgPerMl: 64
    });
    expect(result.rateMlPerHour).toBeCloseTo(22.97, 2);
    const hasVasopressinPrompt = result.safetyAlerts.some(a => a.includes('associar Vasopressina'));
    expect(hasVasopressinPrompt).toBe(true);
  });

  it('F07-3: Computes Vasopressin fixed-dose rate in UI/min without weight multiplier', () => {
    // 0.03 UI/min * 60 / 0.2 UI/mL = 1.8 / 0.2 = 9.0 mL/h
    const result = adapter.calculateInfusion({
      drugId: 'vasopressin',
      patientWeightKg: 85, // Weight should not alter fixed dose
      doseValue: 0.03,
      concentrationUiPerMl: 0.2
    });
    expect(result.rateMlPerHour).toBe(9.0);
    expect(result.formattedDose).toBe('0.03 UI/min');
  });

  it('F07-4: Computes Dobutamine inotropic rate and checks therapeutic range', () => {
    // 5.0 mcg/kg/min * 80kg * 60 / 1000 mcg/mL = 24.0 mL/h
    const result = adapter.calculateInfusion({
      drugId: 'dobutamine',
      patientWeightKg: 80,
      doseValue: 5.0,
      concentrationMcgPerMl: 1000
    });
    expect(result.rateMlPerHour).toBe(24.0);
    expect(result.formattedDose).toBe('5 mcg/kg/min');
  });

  it('F07-5: Flags mandatory non-PVC glass/polyolefin container requirement for Nitroglycerin', () => {
    // 20 mcg/min * 60 / 200 mcg/mL = 6.0 mL/h
    const result = adapter.calculateInfusion({
      drugId: 'nitroglycerin',
      patientWeightKg: 75,
      doseValue: 20,
      concentrationMcgPerMl: 200
    });
    expect(result.rateMlPerHour).toBe(6.0);
    expect(result.containerAlert).toBeDefined();
    expect(result.containerAlert).toContain('Frasco de Vidro ou Polietileno');
    expect(result.containerAlert).toContain('PROIBIDO frasco ou equipo de PVC');
  });
});

describe('Tier 1 — Feature 8: Physiological Radar Engine', () => {
  it('F08-1: Normalizes values to homeostatic range [0.0, 1.0]', () => {
    const axes = [
      { id: 'respiratory', label: 'Respiratório', baseline: 0, max: 4 },
      { id: 'coagulation', label: 'Coagulação', baseline: 0, max: 4 },
      { id: 'renal', label: 'Renal', baseline: 0, max: 4 }
    ];
    const geom = adapter.calculateRadarGeometry(axes, {
      respiratory: 2,
      coagulation: 4,
      renal: 0
    });
    expect(geom.axisCount).toBe(3);
    expect(geom.patientPolygon).toBeDefined();
  });

  it('F08-2: Distributes axes symmetrically across polar coordinates with top offset', () => {
    const axes = [
      { id: 'a', label: 'A' },
      { id: 'b', label: 'B' },
      { id: 'c', label: 'C' },
      { id: 'd', label: 'D' }
    ];
    const geom = adapter.calculateRadarGeometry(axes, {}, 200);
    expect(geom.axisPoints.length).toBe(4);
    // First axis should be pointing straight up at -PI/2
    expect(geom.axisPoints[0].angle).toBeCloseTo(-Math.PI / 2, 4);
  });

  it('F08-3: Generates Cartesian coordinates for SVG polygon points string', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geom = adapter.calculateRadarGeometry(axes, { a: 0.5, b: 0.5, c: 0.5 }, 300);
    expect(typeof geom.patientPolygon).toBe('string');
    const pairs = geom.patientPolygon.split(' ');
    expect(pairs.length).toBe(3);
    pairs.forEach(pair => {
      const [x, y] = pair.split(',').map(Number);
      expect(isNaN(x)).toBe(false);
      expect(isNaN(y)).toBe(false);
    });
  });

  it('F08-4: Generates distinct homeostatic baseline polygon points string', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geom = adapter.calculateRadarGeometry(axes, { a: 1.0, b: 1.0, c: 1.0 }, 300);
    expect(geom.baselinePolygon).toBeDefined();
    expect(geom.baselinePolygon).not.toBe(geom.patientPolygon);
  });

  it('F08-5: Scales patient polygon proportionately to physiological derangement', () => {
    const axes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
    const geomMild = adapter.calculateRadarGeometry(axes, { a: 0.2, b: 0.2, c: 0.2 }, 300);
    const geomSevere = adapter.calculateRadarGeometry(axes, { a: 1.0, b: 1.0, c: 1.0 }, 300);
    expect(geomMild.patientPolygon).not.toBe(geomSevere.patientPolygon);
  });
});

describe('Tier 1 — Feature 9: PEP/EHR Plain-Text Export Engine', () => {
  it('F09-1: Generates structured SOAP format with standard header and timestamp', () => {
    const text = adapter.exportPepSummary({
      calculatorName: 'quick SOFA (qSOFA)',
      scoreValue: 2,
      riskLabel: 'Alto Risco de Piora / Choque'
    });
    expect(text).toContain('[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]');
    expect(text).toContain('DATA/HORA:');
    expect(text).toContain('S (Subjetivo):');
    expect(text).toContain('O (Objetivo):');
    expect(text).toContain('A (Avaliação):');
    expect(text).toContain('P (Plano / Condutas):');
  });

  it('F09-2: Includes patient bed identification and calculated score details', () => {
    const text = adapter.exportPepSummary({
      calculatorName: 'SOFA',
      scoreValue: 12,
      riskLabel: 'Alta Gravidade (SOFA 10-12)',
      riskInterpretation: 'Mortalidade estimada ~40-50%.',
      patientBed: 'Leito 04 - UTI',
      patientWeight: 80
    });
    expect(text).toContain('PACIENTE: Leito 04 - UTI | Peso: 80 kg');
    expect(text).toContain('Escore Calculado: SOFA = 12 pontos');
    expect(text).toContain('Estratificação de Risco: Alta Gravidade');
    expect(text).toContain('Mortalidade estimada ~40-50%.');
  });

  it('F09-3: Includes non-pharmacological clinical recommendations in plan', () => {
    const text = adapter.exportPepSummary({
      calculatorName: 'qSOFA',
      scoreValue: 2,
      riskLabel: 'Alto Risco',
      recommendations: [
        'Hemoculturas (2 pares) antes do antibiótico.',
        'Lactato sérico na admissão e a cada 2-4h.',
        'Cristaloide 30 mL/kg se hipotensão persistente.'
      ]
    });
    expect(text).toContain('1. Hemoculturas (2 pares) antes do antibiótico.');
    expect(text).toContain('2. Lactato sérico na admissão e a cada 2-4h.');
    expect(text).toContain('3. Cristaloide 30 mL/kg se hipotensão persistente.');
  });

  it('F09-4: Formats continuous vasoactive BIC infusion details and flow rate', () => {
    const text = adapter.exportPepSummary({
      calculatorName: 'qSOFA',
      scoreValue: 3,
      riskLabel: 'Alto Risco',
      infusionInfo: {
        drugName: 'Noradrenalina',
        dilution: '16 mg em 234 mL SG 5% (64 mcg/mL)',
        dose: '0.2 mcg/kg/min',
        rateMlPerHour: 13.12,
        vehicle: 'Soro Glicosado 5% (SG 5%)',
        containerAlert: 'Acesso venoso central mandatório.'
      }
    });
    expect(text).toContain('Bomba de Infusão Contínua (BIC):');
    expect(text).toContain('Droga: Noradrenalina');
    expect(text).toContain('Vazão em BIC: 13.12 mL/h');
    expect(text).toContain('Veículo: Soro Glicosado 5% (SG 5%)');
  });

  it('F09-5: Appends regulatory CDSS safety disclaimer to export output', () => {
    const text = adapter.exportPepSummary({
      calculatorName: 'Wells TEP',
      scoreValue: 1.5,
      riskLabel: 'TEP Improvável'
    });
    expect(text).toContain('Aviso de Segurança: Suporte à decisão clínica informada.');
    expect(text).toContain('Não substitui o julgamento médico presencial.');
  });
});

describe('Tier 1 — Feature 10: 100% Vitest Engine Unit Tests', () => {
  it('F10-1: Verifies engine module interfaces export deterministic pure functions', () => {
    const out1 = adapter.calculateScore('qsofa', { rr_22: true, sbp_100: false, ams_gcs: false });
    const out2 = adapter.calculateScore('qsofa', { rr_22: true, sbp_100: false, ams_gcs: false });
    expect(out1.score).toBe(out2.score);
    expect(out1.riskTier.id).toBe(out2.riskTier.id);
  });

  it('F10-2: Verifies score calculations produce predictable outputs for zero inputs', () => {
    const result = adapter.calculateScore('qsofa', {});
    expect(result.score).toBe(0);
    expect(result.riskTier.id).toBe('low');
  });

  it('F10-3: Verifies infusion engine throws on non-positive patient weight', () => {
    expect(() => {
      adapter.calculateInfusion({
        drugId: 'norepinephrine',
        patientWeightKg: 0,
        doseValue: 0.1
      });
    }).toThrow('Patient weight must be greater than zero');
  });

  it('F10-4: Verifies radar engine handles arbitrary physiological axes counts cleanly', () => {
    const axes6 = [{ id: '1' }, { id: '2' }, { id: '3' }, { id: '4' }, { id: '5' }, { id: '6' }];
    const geom6 = adapter.calculateRadarGeometry(axes6, {});
    expect(geom6.axisCount).toBe(6);
    expect(geom6.axisPoints.length).toBe(6);
  });

  it('F10-5: Verifies PEP export handles optional parameters gracefully without crashing', () => {
    const text = adapter.exportPepSummary({
      calculatorName: 'Glasgow-P',
      scoreValue: 15,
      riskLabel: 'Leve'
    });
    expect(typeof text).toBe('string');
    expect(text.length).toBeGreaterThan(50);
  });
});
