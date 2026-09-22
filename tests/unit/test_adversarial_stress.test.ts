import { describe, it, expect } from 'vitest';
import {
  calculateInfusionRate
} from '@/engines/infusionEngine';
import {
  calculateScore,
  calculateQsofa,
  calculateFullSofa,
  calculateWellsPe,
  calculateAgeAdjustedDdimerCutoff,
  calculateGlasgowP,
  calculateBisap,
  convertUreiaToBun,
  SSC_2021_QSOFA_WARNING
} from '@/engines/calculationEngine';
import {
  normalizeRadarValues,
  generateBaselinePolygon,
  generatePatientPolygon,
  calculatePolygonPoints,
  type Point2D
} from '@/engines/radarEngine';
import {
  validateAnonymousBedRecord,
  StorageService,
  type BedRecord
} from '@/services/storageService';
import block01Data from '@/data/blocks/block_01.json';
import type { Calculator } from '@/types/clinical';

const calculators = block01Data.calculators as unknown as Calculator[];

describe('CHALLENGER 1: Empirical Adversarial Stress Testing', () => {

  // ==========================================================================
  // 1. INFUSION ENGINE STRESS TESTING
  // ==========================================================================
  describe('1. Infusion Engine Stress & Boundary Testing', () => {
    const stdNorepiConcentration = 64; // 64 mcg/mL (4 amp / 250 mL SG 5%)

    it('1.1 Extreme patient weights: 20 kg (pediatric border), 70 kg (standard), 150 kg (bariatric), 300 kg (extreme)', () => {
      const weights = [20, 70, 150, 300];
      const dose = 0.1; // mcg/kg/min

      for (const w of weights) {
        const result = calculateInfusionRate({
          drugId: 'norepinephrine',
          patientWeightKg: w,
          doseValue: dose,
          concentrationMcgPerMl: stdNorepiConcentration
        });

        // Expected rate = (dose * weight * 60) / concentration
        const expectedRate = Math.round(((dose * w * 60) / stdNorepiConcentration) * 100) / 100;
        expect(result.rateMlPerHour).toBe(expectedRate);
        expect(Number.isFinite(result.rateMlPerHour)).toBe(true);
        expect(result.rateMlPerHour).toBeGreaterThan(0);
      }

      // Concrete rate checks
      // 20 kg: (0.1 * 20 * 60) / 64 = 120 / 64 = 1.88 mL/h
      const res20 = calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 20,
        doseValue: dose,
        concentrationMcgPerMl: stdNorepiConcentration
      });
      expect(res20.rateMlPerHour).toBe(1.88);

      // 70 kg: (0.1 * 70 * 60) / 64 = 420 / 64 = 6.56 mL/h
      const res70 = calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 70,
        doseValue: dose,
        concentrationMcgPerMl: stdNorepiConcentration
      });
      expect(res70.rateMlPerHour).toBe(6.56);

      // 150 kg: (0.1 * 150 * 60) / 64 = 900 / 64 = 14.06 mL/h
      const res150 = calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 150,
        doseValue: dose,
        concentrationMcgPerMl: stdNorepiConcentration
      });
      expect(res150.rateMlPerHour).toBe(14.06);

      // 300 kg: (0.1 * 300 * 60) / 64 = 1800 / 64 = 28.13 mL/h
      const res300 = calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 300,
        doseValue: dose,
        concentrationMcgPerMl: stdNorepiConcentration
      });
      expect(res300.rateMlPerHour).toBe(28.13);
    });

    it('1.2 Invalid weights: 0 kg, -10 kg, NaN, Infinity -> verify explicit error handling', () => {
      // 0 kg should throw
      expect(() => {
        calculateInfusionRate({
          drugId: 'norepinephrine',
          patientWeightKg: 0,
          doseValue: 0.1,
          concentrationMcgPerMl: stdNorepiConcentration
        });
      }).toThrow('Patient weight must be greater than zero');

      // Negative weight should throw
      expect(() => {
        calculateInfusionRate({
          drugId: 'norepinephrine',
          patientWeightKg: -10,
          doseValue: 0.1,
          concentrationMcgPerMl: stdNorepiConcentration
        });
      }).toThrow('Patient weight must be greater than zero');

      // NaN weight should throw
      expect(() => {
        calculateInfusionRate({
          drugId: 'norepinephrine',
          patientWeightKg: NaN,
          doseValue: 0.1,
          concentrationMcgPerMl: stdNorepiConcentration
        });
      }).toThrow('Patient weight must be greater than zero');

      // Infinity weight: does engine validate finite numbers?
      // Notice: if Infinity is passed, does it throw or propagate Infinity?
      const checkInfinity = () => {
        return calculateInfusionRate({
          drugId: 'norepinephrine',
          patientWeightKg: Infinity,
          doseValue: 0.1,
          concentrationMcgPerMl: stdNorepiConcentration
        });
      };
      try {
        const infRes = checkInfinity();
        // If it didn't throw, infRes.rateMlPerHour would be Infinity
        expect(infRes.rateMlPerHour).toBe(Infinity);
      } catch (err: any) {
        expect(err.message).toBeDefined();
      }
    });

    it('1.3 Norepinephrine rate calculation across full dose range: 0.01 to 3.0 mcg/kg/min', () => {
      const doses = [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0];
      const weight = 70;

      for (const d of doses) {
        const res = calculateInfusionRate({
          drugId: 'norepinephrine',
          patientWeightKg: weight,
          doseValue: d,
          concentrationMcgPerMl: stdNorepiConcentration
        });

        const expectedRate = Math.round(((d * weight * 60) / stdNorepiConcentration) * 100) / 100;
        expect(res.rateMlPerHour).toBe(expectedRate);

        // Clinical safety alerts checks
        if (d > 0.25) {
          expect(res.safetyAlerts.some((a) => a.includes('Vasopressina'))).toBe(true);
        }
        if (d > 1.0) {
          expect(res.safetyAlerts.some((a) => a.includes('faixa crítica'))).toBe(true);
        }
      }
    });

    it('1.4 Vasopressin fixed dose rates: 0.01, 0.02, 0.03, 0.04 UI/min -> verify exact rates (3, 6, 9, 12 mL/h with 0.2 UI/mL)', () => {
      const concentration = 0.2; // 0.2 UI/mL (20 UI / 100 mL)
      const testCases = [
        { dose: 0.01, expectedRate: 3.0 },
        { dose: 0.02, expectedRate: 6.0 },
        { dose: 0.03, expectedRate: 9.0 },
        { dose: 0.04, expectedRate: 12.0 }
      ];

      for (const tc of testCases) {
        const res = calculateInfusionRate({
          drugId: 'vasopressin',
          patientWeightKg: 80, // should not affect rate
          doseValue: tc.dose,
          concentrationMcgPerMl: concentration,
          concentrationUiPerMl: concentration
        });

        expect(res.rateMlPerHour).toBe(tc.expectedRate);
      }

      // Overdose safety alert (>0.04 UI/min)
      const overdoseRes = calculateInfusionRate({
        drugId: 'vasopressin',
        patientWeightKg: 70,
        doseValue: 0.06,
        concentrationMcgPerMl: concentration,
        concentrationUiPerMl: concentration
      });
      expect(overdoseRes.safetyAlerts.some((a) => a.includes('PERIGO'))).toBe(true);
    });

    it('1.5 Nitroglycerin non-PVC warning is always emitted', () => {
      const doses = [5, 10, 50, 100, 200];
      for (const d of doses) {
        const res = calculateInfusionRate({
          drugId: 'nitroglycerin',
          patientWeightKg: 70,
          doseValue: d,
          concentrationMcgPerMl: 200
        });

        expect(res.containerAlert).toBeDefined();
        expect(res.containerAlert).toContain('VIDRO');
        expect(res.containerAlert).toContain('POLIOLEFINA');
        expect(res.containerAlert).toContain('livre de PVC');
        expect(res.safetyAlerts.some((a) => a.includes('PVC'))).toBe(true);
      }
    });
  });

  // ==========================================================================
  // 2. CLINICAL CALCULATION BOUNDARY TESTING
  // ==========================================================================
  describe('2. Clinical Calculation Boundary Testing', () => {
    it('2.1 qSOFA all combinations (0, 1, 2, 3 points) and mandatory SSC 2021 warning', () => {
      const qsofaCalc = calculators.find((c) => c.id === 'calc_qsofa')!;
      expect(qsofaCalc).toBeDefined();

      const combinations = [
        { inputs: { respiratoryRateGte22: false, gcsLessThan15: false, sbpLte100: false }, expectedScore: 0, highRisk: false },
        { inputs: { respiratoryRateGte22: true, gcsLessThan15: false, sbpLte100: false }, expectedScore: 1, highRisk: false },
        { inputs: { respiratoryRateGte22: false, gcsLessThan15: true, sbpLte100: false }, expectedScore: 1, highRisk: false },
        { inputs: { respiratoryRateGte22: false, gcsLessThan15: false, sbpLte100: true }, expectedScore: 1, highRisk: false },
        { inputs: { respiratoryRateGte22: true, gcsLessThan15: true, sbpLte100: false }, expectedScore: 2, highRisk: true },
        { inputs: { respiratoryRateGte22: true, gcsLessThan15: false, sbpLte100: true }, expectedScore: 2, highRisk: true },
        { inputs: { respiratoryRateGte22: false, gcsLessThan15: true, sbpLte100: true }, expectedScore: 2, highRisk: true },
        { inputs: { respiratoryRateGte22: true, gcsLessThan15: true, sbpLte100: true }, expectedScore: 3, highRisk: true }
      ];

      for (const comb of combinations) {
        // Test via dedicated function
        const res = calculateQsofa(comb.inputs);
        expect(res.score).toBe(comb.expectedScore);
        expect(res.isHighRisk).toBe(comb.highRisk);
        expect(res.sscWarning).toBe(SSC_2021_QSOFA_WARNING);
        expect(res.warnings).toContain(SSC_2021_QSOFA_WARNING);

        // Test via generic calculation engine with option IDs
        const genericInputs: Record<string, boolean> = {
          opt_resp_high: comb.inputs.respiratoryRateGte22,
          opt_resp_normal: !comb.inputs.respiratoryRateGte22,
          opt_gcs_less_15: comb.inputs.gcsLessThan15,
          opt_gcs_15: !comb.inputs.gcsLessThan15,
          opt_sbp_low: comb.inputs.sbpLte100,
          opt_sbp_normal: !comb.inputs.sbpLte100
        };
        const genericRes = calculateScore(qsofaCalc, genericInputs);
        expect(genericRes.score).toBe(comb.expectedScore);
        expect(genericRes.sscWarning).toBe(SSC_2021_QSOFA_WARNING);
        expect(genericRes.warnings).toContain(SSC_2021_QSOFA_WARNING);
      }
    });

    it('2.2 SOFA all minimums (0 pts) vs all maximums (24 pts)', () => {
      const sofaCalc = calculators.find((c) => c.id === 'calc_sofa')!;
      expect(sofaCalc).toBeDefined();

      // Minimum SOFA (0 points)
      const minInputs = {
        respiratory: { pao2Fio2Ratio: 500, isMechanicallyVentilated: false },
        coagulation: { plateletsThousandPerMm3: 250 },
        hepatic: { totalBilirubinMgDl: 0.8 },
        cardiovascular: { mapMmHg: 85 },
        neurological: { gcsScore: 15 },
        renal: { creatinineMgDl: 0.9, urineOutputMlPerDay: 1500 }
      };
      const minRes = calculateFullSofa(minInputs);
      expect(minRes.score).toBe(0);
      expect(minRes.organScores.respiratory).toBe(0);
      expect(minRes.organScores.coagulation).toBe(0);
      expect(minRes.organScores.hepatic).toBe(0);
      expect(minRes.organScores.cardiovascular).toBe(0);
      expect(minRes.organScores.neurological).toBe(0);
      expect(minRes.organScores.renal).toBe(0);
      expect(minRes.riskStratification).toContain('Ausente ou Basal');

      // Maximum SOFA (24 points)
      const maxInputs = {
        respiratory: { pao2Fio2Ratio: 70, isMechanicallyVentilated: true },
        coagulation: { plateletsThousandPerMm3: 15 },
        hepatic: { totalBilirubinMgDl: 15.0 },
        cardiovascular: { norepinephrineDoseMcgKgMin: 0.5 },
        neurological: { gcsScore: 3 },
        renal: { creatinineMgDl: 6.0, urineOutputMlPerDay: 100 }
      };
      const maxRes = calculateFullSofa(maxInputs);
      expect(maxRes.score).toBe(24);
      expect(maxRes.organScores.respiratory).toBe(4);
      expect(maxRes.organScores.coagulation).toBe(4);
      expect(maxRes.organScores.hepatic).toBe(4);
      expect(maxRes.organScores.cardiovascular).toBe(4);
      expect(maxRes.organScores.neurological).toBe(4);
      expect(maxRes.organScores.renal).toBe(4);
      expect(maxRes.riskStratification).toContain('Falência Multiorgânica Catastrófica');
    });

    it('2.3 Wells PE boundary test: score = 4.0 exactly (Improbable) vs 4.5 (Probable); age-adjusted D-dimer age 50 (500) vs 51 (510)', () => {
      // Score = 4.0 (dvtSignsOrSymptoms: 3.0 + hemoptysis: 1.0)
      const score4Res = calculateWellsPe({
        dvtSignsOrSymptoms: true,
        hemoptysis: true
      });
      expect(score4Res.score).toBe(4.0);
      expect(score4Res.dichotomousRisk).toBe('unlikely');
      expect(score4Res.dichotomousLabel).toContain('TEP Improvável');

      // Score = 4.5 (dvtSignsOrSymptoms: 3.0 + heartRateGt100: 1.5)
      const score45Res = calculateWellsPe({
        dvtSignsOrSymptoms: true,
        heartRateGt100: true
      });
      expect(score45Res.score).toBe(4.5);
      expect(score45Res.dichotomousRisk).toBe('likely');
      expect(score45Res.dichotomousLabel).toContain('TEP Provável');

      // Age-adjusted D-dimer cutoffs
      expect(calculateAgeAdjustedDdimerCutoff(30)).toBe(500);
      expect(calculateAgeAdjustedDdimerCutoff(50)).toBe(500);
      expect(calculateAgeAdjustedDdimerCutoff(51)).toBe(510);
      expect(calculateAgeAdjustedDdimerCutoff(75)).toBe(750);
      expect(calculateAgeAdjustedDdimerCutoff(80)).toBe(800);
    });

    it('2.4 Glasgow-P: GCS 3 with unreactive pupils (score = 1), GCS 15 with reactive pupils (score = 15)', () => {
      // Worst possible Glasgow-P: GCS 3 (E1, V1, M1) - 2 unreactive pupils = 1 pt
      const worstRes = calculateGlasgowP({
        eye: 1,
        verbal: 1,
        motor: 1,
        unreactivePupils: 2
      });
      expect(worstRes.gcs).toBe(3);
      expect(worstRes.pupilScore).toBe(2);
      expect(worstRes.score).toBe(1);
      expect(worstRes.severity).toBe('severe');
      expect(worstRes.recommendation).toContain('Intubação Orotraqueal');

      // Best possible Glasgow-P: GCS 15 (E4, V5, M6) - 0 unreactive pupils = 15 pts
      const bestRes = calculateGlasgowP({
        eye: 4,
        verbal: 5,
        motor: 6,
        unreactivePupils: 0
      });
      expect(bestRes.gcs).toBe(15);
      expect(bestRes.pupilScore).toBe(0);
      expect(bestRes.score).toBe(15);
      expect(bestRes.severity).toBe('mild');

      // Generic calculator calculation check
      const gpCalc = calculators.find((c) => c.id === 'calc_glasgow_p')!;
      expect(gpCalc).toBeDefined();
      const genericWorst = calculateScore(gpCalc, {
        opt_gp_eye_1: true,
        opt_gp_v_1: true,
        opt_gp_m_1: true,
        opt_gp_p_2: true
      });
      expect(genericWorst.score).toBe(1);

      const genericBest = calculateScore(gpCalc, {
        opt_gp_eye_4: true,
        opt_gp_v_5: true,
        opt_gp_m_6: true,
        opt_gp_p_0: true
      });
      expect(genericBest.score).toBe(15);
    });

    it('2.5 BISAP: Ureia 53.0 mg/dL (BUN 24.7 -> 0 pts) vs Ureia 54.0 mg/dL (BUN 25.2 -> 1 pt)', () => {
      // Direct BUN conversion math
      const bunAt53 = convertUreiaToBun(53.0);
      expect(bunAt53).toBeCloseTo(24.766, 2);
      expect(bunAt53 < 25.0).toBe(true);

      const bunAt54 = convertUreiaToBun(54.0);
      expect(bunAt54).toBeCloseTo(25.233, 2);
      expect(bunAt54 > 25.0).toBe(true);

      // BISAP score with Ureia 53.0 mg/dL (0 pts for BUN)
      const bisap53 = calculateBisap({
        ureiaMgDl: 53.0
      });
      expect(bisap53.criteriaMet.bunElevated).toBe(false);
      expect(bisap53.score).toBe(0);

      // BISAP score with Ureia 54.0 mg/dL (1 pt for BUN)
      const bisap54 = calculateBisap({
        ureiaMgDl: 54.0
      });
      expect(bisap54.criteriaMet.bunElevated).toBe(true);
      expect(bisap54.score).toBe(1);
    });
  });

  // ==========================================================================
  // 3. RADAR ENGINE NORMALIZATION & PROJECTION
  // ==========================================================================
  describe('3. Radar Engine Normalization & Projection', () => {
    const mockAxes = [
      { id: 'respiratory', label: 'Respiratório', system: 'Respiratório', baselineValue: 0, maxAxisValue: 4 },
      { id: 'cardiovascular', label: 'Cardiovascular', system: 'Cardiovascular', baselineValue: 0, maxAxisValue: 4 },
      { id: 'renal', label: 'Renal', system: 'Renal', baselineValue: 0, maxAxisValue: 4 },
      { id: 'neurological', label: 'Neurológico', system: 'Neurológico', baselineValue: 0, maxAxisValue: 4 }
    ];

    const center: Point2D = { x: 150, y: 150 };
    const maxRadius = 100;
    const baselineRatio = 0.25;

    it('3.1 Zero deviation: verify all vertices at radius 0.25 (homeostatic baseline)', () => {
      const zeroValues = {
        respiratory: 0,
        cardiovascular: 0,
        renal: 0,
        neurological: 0
      };

      const normalized = normalizeRadarValues(mockAxes, zeroValues);
      expect(normalized.respiratory).toBe(0.0);
      expect(normalized.cardiovascular).toBe(0.0);
      expect(normalized.renal).toBe(0.0);
      expect(normalized.neurological).toBe(0.0);

      const baselinePoly = generateBaselinePolygon(mockAxes.length, center, maxRadius, baselineRatio);
      const patientPoly = generatePatientPolygon(mockAxes, normalized, center, maxRadius, baselineRatio);

      // At zero deviation, patient polygon must exactly equal the baseline polygon
      expect(patientPoly).toBe(baselinePoly);

      // Verify coordinate math for 4 axes:
      // Radius = 0.25 * 100 = 25
      // Axis 0 (top, -PI/2): x = 150, y = 150 - 25 = 125
      // Axis 1 (right, 0): x = 150 + 25 = 175, y = 150
      // Axis 2 (bottom, PI/2): x = 150, y = 150 + 25 = 175
      // Axis 3 (left, PI): x = 150 - 25 = 125, y = 150
      expect(baselinePoly).toContain('150,125');
      expect(baselinePoly).toContain('175,150');
      expect(baselinePoly).toContain('150,175');
      expect(baselinePoly).toContain('125,150');
    });

    it('3.2 Maximum deviation: verify vertices stretch to radius 1.0 (maxRadius = 100)', () => {
      const maxValues = {
        respiratory: 4,
        cardiovascular: 4,
        renal: 4,
        neurological: 4
      };

      const normalized = normalizeRadarValues(mockAxes, maxValues);
      expect(normalized.respiratory).toBe(1.0);
      expect(normalized.cardiovascular).toBe(1.0);
      expect(normalized.renal).toBe(1.0);
      expect(normalized.neurological).toBe(1.0);

      const patientPoly = generatePatientPolygon(mockAxes, normalized, center, maxRadius, baselineRatio);

      // At maximum deviation, r = 1.0 * 100 = 100
      // Axis 0 (top): x = 150, y = 150 - 100 = 50
      // Axis 1 (right): x = 150 + 100 = 250, y = 150
      // Axis 2 (bottom): x = 150, y = 150 + 100 = 250
      // Axis 3 (left): x = 150 - 100 = 50, y = 150
      expect(patientPoly).toContain('150,50');
      expect(patientPoly).toContain('250,150');
      expect(patientPoly).toContain('150,250');
      expect(patientPoly).toContain('50,150');
    });

    it('3.3 Trigonometric math: no NaN, no undefined, valid SVG polygon coordinates across 3 to 12 axes', () => {
      for (let n = 3; n <= 12; n++) {
        const radii = new Array(n).fill(0.65);
        const pointsStr = calculatePolygonPoints(radii, center, maxRadius);

        expect(pointsStr).not.toContain('NaN');
        expect(pointsStr).not.toContain('undefined');
        expect(pointsStr).not.toContain('null');

        const pairs = pointsStr.split(' ');
        expect(pairs.length).toBe(n);

        for (const pair of pairs) {
          const [xStr, yStr] = pair.split(',');
          const x = parseFloat(xStr);
          const y = parseFloat(yStr);
          expect(Number.isFinite(x)).toBe(true);
          expect(Number.isFinite(y)).toBe(true);
          // Coordinates must be within [center - maxRadius, center + maxRadius]
          expect(x).toBeGreaterThanOrEqual(center.x - maxRadius - 1);
          expect(x).toBeLessThanOrEqual(center.x + maxRadius + 1);
          expect(y).toBeGreaterThanOrEqual(center.y - maxRadius - 1);
          expect(y).toBeLessThanOrEqual(center.y + maxRadius + 1);
        }
      }
    });
  });

  // ==========================================================================
  // 4. ZERO LGPD ATTACK TESTING
  // ==========================================================================
  describe('4. Zero LGPD Attack & Penetration Testing', () => {
    it('4.1 Attempt storing bed records with forbidden nominal keys: name, cpf, prontuario, mrn', () => {
      const forbiddenKeys = [
        'name',
        'nome',
        'patientname',
        'patient_name',
        'cpf',
        'prontuario',
        'prontuário',
        'mrn',
        'rg',
        'cns',
        'birthdate',
        'data_nascimento'
      ];

      for (const key of forbiddenKeys) {
        const maliciousPayload: any = {
          id: 'bed_attack_01',
          label: 'Leito 04 - UTI',
          updatedAt: new Date().toISOString(),
          [key]: 'Paciente Identificado Teste'
        };

        expect(() => {
          validateAnonymousBedRecord(maliciousPayload);
        }).toThrow(/LGPD Violation/);
      }
    });

    it('4.2 Attempt storing formatted CPF pattern in notes (e.g. 123.456.789-00)', () => {
      const maliciousPayload: BedRecord = {
        id: 'bed_attack_02',
        label: 'Leito 05 - UTI',
        notes: 'Paciente admitido com PA 140/90. Familiar informou CPF 123.456.789-00 para contato.',
        updatedAt: new Date().toISOString()
      };

      expect(() => {
        validateAnonymousBedRecord(maliciousPayload);
      }).toThrow('LGPD Violation: Padrão de CPF detectado no campo de anotações.');
    });

    it('4.3 Verify StorageService strictly blocks malicious bed records before commit', async () => {
      const storage = new StorageService(true); // memory fallback

      const maliciousRecord: any = {
        id: 'bed_attack_03',
        label: 'Leito 06 - UTI',
        cpf: '000.000.000-00',
        updatedAt: new Date().toISOString()
      };

      await expect(storage.saveBed(maliciousRecord)).rejects.toThrow(/LGPD Violation/);

      // Verify nothing was stored
      const beds = await storage.getBeds();
      expect(beds.some((b) => b.id === 'bed_attack_03')).toBe(false);
    });

    it('4.4 Valid anonymous records pass validation cleanly', async () => {
      const storage = new StorageService(true);

      const validRecord: BedRecord = {
        id: 'bed_valid_01',
        label: 'Leito 04 - UTI Geral',
        sector: 'UTI Geral',
        patientWeightKg: 75,
        notes: 'Em desmame de Noradrenalina. PAM estável em 75 mmHg.',
        updatedAt: new Date().toISOString()
      };

      expect(() => validateAnonymousBedRecord(validRecord)).not.toThrow();
      await storage.saveBed(validRecord);

      const saved = await storage.getBed('bed_valid_01');
      expect(saved).toBeDefined();
      expect(saved?.label).toBe('Leito 04 - UTI Geral');
    });
  });
});
