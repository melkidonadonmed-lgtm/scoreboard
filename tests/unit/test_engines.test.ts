import { describe, it, expect } from 'vitest';
import block01Data from '../../src/data/blocks/block_01.json';
import { type Calculator } from '../../src/types/clinical';
import {
  // 1. Calculation Engine
  calculateScore,
  calculateQsofa,
  calculateFullSofa,
  calculateWellsPe,
  calculateAgeAdjustedDdimerCutoff,
  calculateGlasgowP,
  calculateFourScore,
  calculateRanson,
  calculateBisap,
  convertUreiaToBun,
  convertBunToUreia,
  SSC_2021_QSOFA_WARNING,

  // 2. Infusion Engine
  calculateInfusionRate,
  calculateDoseFromRate,
  generateTitrationMatrix,
  NOREPINEPHRINE_PROTOCOL,
  VASOPRESSIN_PROTOCOL,
  DOBUTAMINE_PROTOCOL,
  NITROGLYCERIN_PROTOCOL,

  // 3. Radar Engine
  normalizeAxisValue,
  normalizeRadarValues,
  polarToCartesian,
  calculateAxisAngle,
  calculatePolygonPoints,
  generateBaselinePolygon,
  generatePatientPolygon,
  generateGridRings,
  generateAxisSpokes,
  getAxisLabelPositions,

  // 4. PEP Export Engine
  generatePepNote,
  generateSbarNote,
  sanitizeBedIdentifier,
  formatDateBrazilian,
  summarizeRadarDeviations
} from '../../src/engines';

const calculators = block01Data.calculators as unknown as Calculator[];
const getCalc = (id: string) => {
  const found = calculators.find((c) => c.id === id);
  if (!found) throw new Error(`Calculator ${id} not found in block_01.json`);
  return found;
};

// ============================================================================
// 1. CALCULATION ENGINE TESTS
// ============================================================================

describe('calculationEngine', () => {
  describe('Generic calculateScore with block_01 definitions', () => {
    it('calculates qSOFA accurately and attaches mandatory SSC 2021 warning', () => {
      const qsofa = getCalc('calc_qsofa');

      // Baseline normal patient (0 points)
      const normalResult = calculateScore(qsofa, {
        grp_qsofa_resp: 'opt_resp_normal',
        grp_qsofa_gcs: 'opt_gcs_15',
        grp_qsofa_sbp: 'opt_sbp_normal'
      });
      expect(normalResult.rawScore).toBe(0);
      expect(normalResult.activeRiskTier.id).toBe('tier_qsofa_low');
      expect(normalResult.sscWarning).toBe(SSC_2021_QSOFA_WARNING);
      expect(normalResult.warnings).toContain(SSC_2021_QSOFA_WARNING);

      // High-risk patient (2 points: taquipneia + hipotensão)
      const highRiskResult = calculateScore(qsofa, {
        grp_qsofa_resp: 'opt_resp_high',
        grp_qsofa_gcs: 'opt_gcs_15',
        grp_qsofa_sbp: 'opt_sbp_low'
      });
      expect(highRiskResult.rawScore).toBe(2);
      expect(highRiskResult.activeRiskTier.id).toBe('tier_qsofa_high');
      expect(highRiskResult.radarValues['axis_qsofa_resp']).toBe(1.0);
      expect(highRiskResult.radarValues['axis_qsofa_gcs']).toBe(0.0);
      expect(highRiskResult.radarValues['axis_qsofa_sbp']).toBe(1.0);
    });

    it('calculates Full SOFA score and populates multi-axis radar values', () => {
      const sofa = getCalc('calc_sofa');

      // Normal patient
      const baseline = calculateScore(sofa, {
        grp_sofa_resp: 'opt_sofa_resp_0',
        grp_sofa_coag: 'opt_sofa_coag_0',
        grp_sofa_liver: 'opt_sofa_liver_0',
        grp_sofa_cv: 'opt_sofa_cv_0',
        grp_sofa_cns: 'opt_sofa_cns_0',
        grp_sofa_renal: 'opt_sofa_renal_0'
      });
      expect(baseline.rawScore).toBe(0);
      expect(baseline.activeRiskTier.id).toBe('tier_sofa_0');
      expect(Object.values(baseline.radarValues).every((v) => v === 0)).toBe(true);

      // Septic shock with multiorgan failure
      // PaO2/FiO2 < 200 VM (3 pts), Plaq < 50k (3 pts), Bili 2-5.9 (2 pts), Nora > 0.1 (4 pts), GCS 6-9 (3 pts), Cr 3.5-4.9 (3 pts)
      const severe = calculateScore(sofa, {
        grp_sofa_resp: 'opt_sofa_resp_3',
        grp_sofa_coag: 'opt_sofa_coag_3',
        grp_sofa_liver: 'opt_sofa_liver_2',
        grp_sofa_cv: 'opt_sofa_cv_4',
        grp_sofa_cns: 'opt_sofa_cns_3',
        grp_sofa_renal: 'opt_sofa_renal_3'
      });
      expect(severe.rawScore).toBe(3 + 3 + 2 + 4 + 3 + 3); // 18 pts
      expect(severe.activeRiskTier.id).toBe('tier_sofa_3');
      expect(severe.radarValues['axis_sofa_cv']).toBe(1.0); // Nora high is max (4/4)
      expect(severe.radarValues['axis_sofa_resp']).toBe(0.75); // 3/4
    });

    it('calculates Wells TEP with dichotomous risk threshold', () => {
      const wells = getCalc('calc_wells_tep');

      // Unlikely: Heart rate > 100 (1.5) + Hemoptysis (1.0) = 2.5 pts (<= 4.0)
      const resUnlikely = calculateScore(wells, {
        grp_wtep_hr: 'opt_wtep_hr_yes',
        grp_wtep_hemopt: 'opt_wtep_hemopt_yes'
      });
      expect(resUnlikely.rawScore).toBe(2.5);
      expect(resUnlikely.activeRiskTier.id).toBe('tier_wtep_unlikely');

      // Likely: DVT signs (3.0) + PE most likely (3.0) = 6.0 pts (> 4.0)
      const resLikely = calculateScore(wells, {
        grp_wtep_tvp: 'opt_wtep_tvp_yes',
        grp_wtep_alt: 'opt_wtep_alt_yes'
      });
      expect(resLikely.rawScore).toBe(6.0);
      expect(resLikely.activeRiskTier.id).toBe('tier_wtep_likely');
    });

    it('calculates Glasgow-P via branching decision subtracting pupil reactivity', () => {
      const gp = getCalc('calc_glasgow_p');

      // GCS 15 (4+5+6) with unreactive pupils 0 -> 15
      const resNormal = calculateScore(gp, {
        grp_gp_eye: 'opt_gp_eye_4',
        grp_gp_verb: 'opt_gp_v_5',
        grp_gp_mot: 'opt_gp_m_6',
        grp_gp_pup: 'opt_gp_p_0'
      });
      expect(resNormal.rawScore).toBe(15);
      expect(resNormal.activeRiskTier.id).toBe('tier_gp_mild');

      // GCS 10 (3+3+4) with 1 unreactive pupil (anisocoria) -> 10 - 1 = 9 (moderate)
      const resMod = calculateScore(gp, {
        grp_gp_eye: 'opt_gp_eye_3',
        grp_gp_verb: 'opt_gp_v_3',
        grp_gp_mot: 'opt_gp_m_4',
        grp_gp_pup: 'opt_gp_p_1'
      });
      expect(resMod.rawScore).toBe(9);
      expect(resMod.activeRiskTier.id).toBe('tier_gp_mod');

      // GCS 3 (1+1+1) with 2 unreactive pupils -> 3 - 2 = 1 (severe coma)
      const resSevere = calculateScore(gp, {
        grp_gp_eye: 'opt_gp_eye_1',
        grp_gp_verb: 'opt_gp_v_1',
        grp_gp_mot: 'opt_gp_m_1',
        grp_gp_pup: 'opt_gp_p_2'
      });
      expect(resSevere.rawScore).toBe(1);
      expect(resSevere.activeRiskTier.id).toBe('tier_gp_severe');
    });

    it('calculates FOUR Score across all 4 categories (0-16 pts)', () => {
      const four = getCalc('calc_four');

      // Maximum 16 points
      const full = calculateScore(four, {
        grp_four_eye: 'opt_fe_4',
        grp_four_mot: 'opt_fm_4',
        grp_four_stem: 'opt_fs_4',
        grp_four_resp: 'opt_fr_4'
      });
      expect(full.rawScore).toBe(16);
      expect(full.activeRiskTier.id).toBe('tier_four_high_score');

      // Minimum 0 points (deep coma / brain death screening)
      const zero = calculateScore(four, {
        grp_four_eye: 'opt_fe_0',
        grp_four_mot: 'opt_fm_0',
        grp_four_stem: 'opt_fs_0',
        grp_four_resp: 'opt_fr_0'
      });
      expect(zero.rawScore).toBe(0);
      expect(zero.activeRiskTier.id).toBe('tier_four_low_score');
    });

    it('calculates Ranson and BISAP using block_01 calculators', () => {
      const ranson = getCalc('calc_ranson');
      const ransonRes = calculateScore(ranson, {
        grp_ran_age: 'opt_ran_age_yes',
        grp_ran_leuko: 'opt_ran_leu_yes',
        grp_ran_glyc: 'opt_ran_gly_yes'
      });
      expect(ransonRes.rawScore).toBe(3);
      expect(ransonRes.activeRiskTier.id).toBe('tier_ran_mod');

      const bisap = getCalc('calc_bisap');
      const bisapRes = calculateScore(bisap, {
        grp_bisap_bun: 'opt_bisap_bun_yes',
        grp_bisap_mental: 'opt_bisap_gcs_yes',
        grp_bisap_sirs: 'opt_bisap_sirs_yes',
        grp_bisap_age: 'opt_bisap_age_yes'
      });
      expect(bisapRes.rawScore).toBe(4);
      expect(bisapRes.activeRiskTier.id).toBe('tier_bisap_high');

      // Also test boolean inputs directly
      const bisapBoolRes = calculateScore(bisap, {
        grp_bisap_bun: true,
        grp_bisap_mental: true,
        grp_bisap_sirs: true,
        grp_bisap_age: true,
        grp_bisap_pleural: true
      });
      expect(bisapBoolRes.rawScore).toBe(5);
      expect(bisapBoolRes.activeRiskTier.id).toBe('tier_bisap_high');
    });
  });

  describe('Dedicated Score Functions', () => {
    it('calculateQsofa works with boolean and numeric inputs', () => {
      // Boolean inputs
      const resBool = calculateQsofa({
        respiratoryRateGte22: true,
        gcsLessThan15: false,
        sbpLte100: true
      });
      expect(resBool.score).toBe(2);
      expect(resBool.isHighRisk).toBe(true);
      expect(resBool.sscWarning).toBe(SSC_2021_QSOFA_WARNING);

      // Numeric inputs
      const resNum = calculateQsofa({
        respiratoryRate: 24,
        gcs: 14,
        sbp: 95
      });
      expect(resNum.score).toBe(3);
      expect(resNum.isHighRisk).toBe(true);

      const resNormal = calculateQsofa({
        respiratoryRate: 18,
        gcs: 15,
        sbp: 120
      });
      expect(resNormal.score).toBe(0);
      expect(resNormal.isHighRisk).toBe(false);
    });

    it('calculateFullSofa accurately scores each organ failure individually and combined', () => {
      // Test respiratory grading with and without mechanical ventilation
      const noVentScore = calculateFullSofa({
        respiratory: { pao2Fio2Ratio: 180, isMechanicallyVentilated: false }
      });
      expect(noVentScore.organScores.respiratory).toBe(2); // < 300 without vent is 2

      const ventScore = calculateFullSofa({
        respiratory: { pao2Fio2Ratio: 180, isMechanicallyVentilated: true }
      });
      expect(ventScore.organScores.respiratory).toBe(3); // < 200 with vent is 3

      // Test cardiovascular vasopressor thresholds
      const dobutRes = calculateFullSofa({
        cardiovascular: { dobutamineAnyDose: true }
      });
      expect(dobutRes.organScores.cardiovascular).toBe(2);

      const noraLowRes = calculateFullSofa({
        cardiovascular: { norepinephrineDoseMcgKgMin: 0.08 }
      });
      expect(noraLowRes.organScores.cardiovascular).toBe(3);

      const noraHighRes = calculateFullSofa({
        cardiovascular: { norepinephrineDoseMcgKgMin: 0.25 }
      });
      expect(noraHighRes.organScores.cardiovascular).toBe(4);

      // Combined multiorgan calculation
      const full = calculateFullSofa({
        respiratory: { pao2Fio2Ratio: 80, isMechanicallyVentilated: true }, // 4
        coagulation: { plateletsThousandPerMm3: 15 }, // 4
        hepatic: { totalBilirubinMgDl: 13.5 }, // 4
        cardiovascular: { norepinephrineDoseMcgKgMin: 0.3 }, // 4
        neurological: { gcsScore: 4 }, // 4
        renal: { creatinineMgDl: 5.5, urineOutputMlPerDay: 150 } // 4
      });
      expect(full.score).toBe(24);
      expect(full.riskStratification).toContain('Falência Multiorgânica Catastrófica');
    });

    it('calculateWellsPe verifies dichotomous, 3-tier and age-adjusted D-dimer logic', () => {
      // Age-adjusted D-dimer
      expect(calculateAgeAdjustedDdimerCutoff(40)).toBe(500);
      expect(calculateAgeAdjustedDdimerCutoff(50)).toBe(500);
      expect(calculateAgeAdjustedDdimerCutoff(65)).toBe(650);
      expect(calculateAgeAdjustedDdimerCutoff(82)).toBe(820);

      // Unlikely + age 65
      const resUnlikely = calculateWellsPe(
        {
          heartRateGt100: true, // 1.5
          hemoptysis: true // 1.0
        },
        65
      );
      expect(resUnlikely.score).toBe(2.5);
      expect(resUnlikely.dichotomousRisk).toBe('unlikely');
      expect(resUnlikely.threeTierRisk).toBe('intermediate'); // 2.0 to 6.0
      expect(resUnlikely.ageAdjustedDdimerCutoff).toBe(650);
      expect(resUnlikely.recommendation).toContain('D-Dímero');

      // High risk (> 6.0)
      const resHigh = calculateWellsPe(
        {
          dvtSignsOrSymptoms: true, // 3.0
          peMoreLikelyThanAlternative: true, // 3.0
          heartRateGt100: true // 1.5
        },
        70
      );
      expect(resHigh.score).toBe(7.5);
      expect(resHigh.dichotomousRisk).toBe('likely');
      expect(resHigh.threeTierRisk).toBe('high');
      expect(resHigh.recommendation).toContain('Angiotomografia');
    });

    it('calculateGlasgowP and calculateFourScore edge cases', () => {
      // Glasgow-P
      const gp = calculateGlasgowP({ eye: 4, verbal: 5, motor: 6, unreactivePupils: 0 });
      expect(gp.score).toBe(15);
      expect(gp.severity).toBe('mild');

      const gpMin = calculateGlasgowP({ eye: 1, verbal: 1, motor: 1, unreactivePupils: 2 });
      expect(gpMin.score).toBe(1);
      expect(gpMin.severity).toBe('severe');

      // FOUR Score
      const fourFull = calculateFourScore({ eye: 4, motor: 4, brainstem: 4, respiration: 4 });
      expect(fourFull.score).toBe(16);
      expect(fourFull.isBrainDeathAlert).toBe(false);

      const fourZero = calculateFourScore({ eye: 0, motor: 0, brainstem: 0, respiration: 0 });
      expect(fourZero.score).toBe(0);
      expect(fourZero.isBrainDeathAlert).toBe(true);
      expect(fourZero.recommendation).toContain('Morte Encefálica');
    });

    it('calculateRanson handles Biliary vs Non-Biliary etiology', () => {
      // Non-Biliary: Age > 55
      const nonBiliary = calculateRanson({ ageExceeded: true, wbcExceeded: true }, false);
      expect(nonBiliary.isBiliary).toBe(false);
      expect(nonBiliary.score).toBe(2);
      expect(nonBiliary.severity).toBe('mild');

      // Biliary
      const biliary = calculateRanson(
        {
          ageExceeded: true,
          wbcExceeded: true,
          glucoseExceeded: true,
          ldhExceeded: true
        },
        true
      );
      expect(biliary.isBiliary).toBe(true);
      expect(biliary.score).toBe(4);
      expect(biliary.severity).toBe('moderate');
    });

    it('calculateBisap handles Brazilian Ureia and BUN conversions', () => {
      // BUN = Ureia / 2.14
      expect(convertUreiaToBun(53.5)).toBeCloseTo(25.0, 1);
      expect(convertBunToUreia(25.0)).toBeCloseTo(53.5, 1);

      // Evaluated with serum Ureia = 60 mg/dL (> 53.5 -> +1 pt)
      const resWithUreia = calculateBisap({
        ureiaMgDl: 60,
        impairedMentalStatus: true,
        sirsCriteriaGte2: true,
        ageGt60: true
      });
      expect(resWithUreia.score).toBe(4);
      expect(resWithUreia.severity).toBe('high');
      expect(resWithUreia.criteriaMet.bunElevated).toBe(true);

      // Low risk with normal BUN
      const resLow = calculateBisap({
        bunMgDl: 15,
        impairedMentalStatus: false,
        sirsCriteriaGte2: false,
        ageGt60: false,
        pleuralEffusion: false
      });
      expect(resLow.score).toBe(0);
      expect(resLow.severity).toBe('low');
    });
  });
});

// ============================================================================
// 2. INFUSION BIC ENGINE TESTS
// ============================================================================

describe('infusionEngine', () => {
  it('calculates Norepinephrine infusion rate and flags vehicle and central line requirements', () => {
    // Standard solution (64 mcg/mL) for 70 kg at 0.10 mcg/kg/min
    // Rate = (0.10 * 70 * 60) / 64 = 6.5625 -> 6.56 mL/h
    const standard = calculateInfusionRate({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.1,
      concentrationMcgPerMl: 64
    });
    expect(standard.rateMlPerHour).toBe(6.56);
    expect(standard.recommendedVehicle).toContain('Soro Glicosado 5% (SG 5%) OBRIGATÓRIO');
    expect(standard.safetyAlerts.some((a) => a.includes('SG 5%'))).toBe(true);
    expect(standard.safetyAlerts.some((a) => a.includes('Acesso venoso central'))).toBe(true);

    // Concentrated solution (128 mcg/mL) for 70 kg at 0.10 mcg/kg/min
    // Rate = (0.10 * 70 * 60) / 128 = 3.28 mL/h
    const concentrated = calculateInfusionRate({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.1,
      concentrationMcgPerMl: 128
    });
    expect(concentrated.rateMlPerHour).toBe(3.28);
  });

  it('triggers Vasopressin association alert when Norepinephrine exceeds 0.25 mcg/kg/min', () => {
    const highDose = calculateInfusionRate({
      drugId: 'noradrenalina',
      patientWeightKg: 70,
      doseValue: 0.35,
      concentrationMcgPerMl: 64
    });
    expect(highDose.rateMlPerHour).toBe(22.97);
    const hasVasoAlert = highDose.safetyAlerts.some((a) =>
      a.includes('associar Vasopressina')
    );
    expect(hasVasoAlert).toBe(true);
  });

  it('calculates Vasopressin fixed-dose rate in UI/min independently of patient weight', () => {
    // 0.03 UI/min at 0.2 UI/mL -> (0.03 * 60) / 0.2 = 9.0 mL/h
    const peso70 = calculateInfusionRate({
      drugId: 'vasopressin',
      patientWeightKg: 70,
      doseValue: 0.03,
      concentrationMcgPerMl: 0.2
    });
    const peso100 = calculateInfusionRate({
      drugId: 'vasopressina',
      patientWeightKg: 100,
      doseValue: 0.03,
      concentrationMcgPerMl: 0.2
    });

    expect(peso70.rateMlPerHour).toBe(9.0);
    expect(peso100.rateMlPerHour).toBe(9.0);
    expect(peso70.safetyAlerts.some((a) => a.includes('Dose fixa não titulável'))).toBe(true);

    // Test fixed steps: 0.01 -> 3.0, 0.02 -> 6.0, 0.04 -> 12.0
    expect(
      calculateInfusionRate({
        drugId: 'vasopressin',
        patientWeightKg: 60,
        doseValue: 0.01,
        concentrationMcgPerMl: 0.2
      }).rateMlPerHour
    ).toBe(3.0);

    expect(
      calculateInfusionRate({
        drugId: 'vasopressin',
        patientWeightKg: 60,
        doseValue: 0.04,
        concentrationMcgPerMl: 0.2
      }).rateMlPerHour
    ).toBe(12.0);
  });

  it('calculates Dobutamine flow rate and warns on maximal therapeutic dose', () => {
    // 5.0 mcg/kg/min for 80 kg at 1,000 mcg/mL -> (5 * 80 * 60) / 1000 = 24.0 mL/h
    const dobut = calculateInfusionRate({
      drugId: 'dobutamine',
      patientWeightKg: 80,
      doseValue: 5.0,
      concentrationMcgPerMl: 1000
    });
    expect(dobut.rateMlPerHour).toBe(24.0);

    // Overdose warning
    const dobutHigh = calculateInfusionRate({
      drugId: 'dobutamina',
      patientWeightKg: 70,
      doseValue: 22.0,
      concentrationMcgPerMl: 1000
    });
    expect(dobutHigh.safetyAlerts.some((a) => a.includes('excede o teto recomendado'))).toBe(true);
  });

  it('calculates Nitroglycerin flow rate and enforces non-PVC glass/polyolefin container rules', () => {
    // Rate in mL/h = Dose (mcg/min) * 0.3 for 200 mcg/mL
    // 20 mcg/min -> (20 * 60) / 200 = 6.0 mL/h
    const nitro = calculateInfusionRate({
      drugId: 'nitroglycerin',
      patientWeightKg: 75,
      doseValue: 20,
      concentrationMcgPerMl: 200
    });
    expect(nitro.rateMlPerHour).toBe(6.0);
    expect(nitro.containerAlert).toBeDefined();
    expect(nitro.containerAlert).toContain('VIDRO ou POLIOLEFINA/POLIETILENO');
    expect(nitro.containerAlert).toContain('PROIBIDO frasco/equipo de PVC comum');
    expect(nitro.containerAlert).toContain('80% da droga por adsorção plástica');
  });

  it('performs reverse calculation from BIC rate (mL/h) back to administered dose', () => {
    // 6.56 mL/h at 64 mcg/mL for 70 kg -> 0.0999 ~ 0.1 mcg/kg/min
    const doseNora = calculateDoseFromRate(6.5625, 64, 70, 'mcg/kg/min');
    expect(doseNora).toBeCloseTo(0.1, 3);

    // 9.0 mL/h at 0.2 UI/mL -> 0.03 UI/min
    const doseVaso = calculateDoseFromRate(9.0, 0.2, undefined, 'UI/min');
    expect(doseVaso).toBe(0.03);

    // 6.0 mL/h at 200 mcg/mL -> 20.0 mcg/min
    const doseNitro = calculateDoseFromRate(6.0, 200, undefined, 'mcg/min');
    expect(doseNitro).toBe(20.0);
  });

  it('generates complete bedside titration steps matrix', () => {
    const stepsNora = generateTitrationMatrix(NOREPINEPHRINE_PROTOCOL, 70);
    expect(stepsNora.length).toBeGreaterThan(5);
    expect(stepsNora[0].dose).toBe(0.05);
    expect(stepsNora[0].rateMlPerHour).toBe(3.3);
    expect(stepsNora.find((s) => s.dose === 0.35)?.isWarning).toBe(true);

    const stepsVaso = generateTitrationMatrix(VASOPRESSIN_PROTOCOL, 70);
    expect(stepsVaso.length).toBe(4);
    expect(stepsVaso.map((s) => s.rateMlPerHour)).toEqual([3.0, 6.0, 9.0, 12.0]);

    const stepsDobut = generateTitrationMatrix(DOBUTAMINE_PROTOCOL, 80);
    expect(stepsDobut.find((s) => s.dose === 5.0)?.rateMlPerHour).toBe(24.0);

    const stepsNitro = generateTitrationMatrix(NITROGLYCERIN_PROTOCOL, 70);
    expect(stepsNitro.find((s) => s.dose === 50)?.rateMlPerHour).toBe(15.0);
  });
});

// ============================================================================
// 3. PHYSIOLOGICAL RADAR ENGINE TESTS
// ============================================================================

describe('radarEngine', () => {
  it('normalizes axis values strictly between 0.0 and 1.0', () => {
    expect(normalizeAxisValue(0, 0, 4)).toBe(0.0);
    expect(normalizeAxisValue(2, 0, 4)).toBe(0.5);
    expect(normalizeAxisValue(4, 0, 4)).toBe(1.0);
    expect(normalizeAxisValue(6, 0, 4)).toBe(1.0); // clamped
    expect(normalizeAxisValue(-2, 0, 4)).toBe(0.0); // clamped
    expect(normalizeAxisValue(NaN, 0, 4)).toBe(0.0);
  });

  it('normalizes dictionary of multiple radar axes simultaneously', () => {
    const sofa = getCalc('calc_sofa');
    const rawMap: Record<string, number> = {
      axis_sofa_resp: 3, // max is 4 -> 0.75
      axis_sofa_coag: 2, // max is 4 -> 0.50
      axis_sofa_liver: 1, // max is 4 -> 0.25
      axis_sofa_cv: 4, // max is 4 -> 1.00
      axis_sofa_cns: 0, // max is 4 -> 0.00
      axis_sofa_renal: 2 // max is 4 -> 0.50
    };
    const normalized = normalizeRadarValues(sofa.radarAxes, rawMap);
    expect(normalized.axis_sofa_resp).toBe(0.75);
    expect(normalized.axis_sofa_cv).toBe(1.0);
    expect(normalized.axis_sofa_cns).toBe(0.0);
  });

  it('projects polar coordinates accurately into Cartesian space', () => {
    const center = { x: 100, y: 100 };
    // Top (angle = -PI/2)
    const top = polarToCartesian(center, 50, -Math.PI / 2);
    expect(top.x).toBeCloseTo(100, 1);
    expect(top.y).toBeCloseTo(50, 1);

    // Right (angle = 0)
    const right = polarToCartesian(center, 50, 0);
    expect(right.x).toBeCloseTo(150, 1);
    expect(right.y).toBeCloseTo(100, 1);

    // Bottom (angle = PI/2)
    const bottom = polarToCartesian(center, 50, Math.PI / 2);
    expect(bottom.x).toBeCloseTo(100, 1);
    expect(bottom.y).toBeCloseTo(150, 1);
  });

  it('calculates axis angles starting at 12 o clock (-PI/2)', () => {
    expect(calculateAxisAngle(0, 4)).toBeCloseTo(-Math.PI / 2, 4);
    expect(calculateAxisAngle(1, 4)).toBeCloseTo(0, 4);
    expect(calculateAxisAngle(2, 4)).toBeCloseTo(Math.PI / 2, 4);
    expect(calculateAxisAngle(3, 4)).toBeCloseTo(Math.PI, 4);
  });

  it('generates baseline and patient SVG polygon points strings', () => {
    const qsofa = getCalc('calc_qsofa');
    const center = { x: 100, y: 100 };
    const maxRadius = 80;

    const baseline = generateBaselinePolygon(qsofa.radarAxes.length, center, maxRadius, 0.25);
    expect(typeof baseline).toBe('string');
    const baselinePts = baseline.split(' ');
    expect(baselinePts.length).toBe(3); // 3 axes in qSOFA

    // Normal patient -> patient polygon matches baseline ratio
    const patientNorm = generatePatientPolygon(
      qsofa.radarAxes,
      { axis_qsofa_resp: 0, axis_qsofa_gcs: 0, axis_qsofa_sbp: 0 },
      center,
      maxRadius,
      0.25
    );
    expect(patientNorm).toBe(baseline);

    // Severe patient -> patient polygon expands outward
    const patientSevere = generatePatientPolygon(
      qsofa.radarAxes,
      { axis_qsofa_resp: 1.0, axis_qsofa_gcs: 1.0, axis_qsofa_sbp: 1.0 },
      center,
      maxRadius,
      0.25
    );
    expect(patientSevere).not.toBe(baseline);
    const severePts = patientSevere.split(' ');
    expect(severePts.length).toBe(3);
  });

  it('generates concentric grid rings and axis spokes', () => {
    const center = { x: 100, y: 100 };
    const rings = generateGridRings(6, center, 80);
    expect(rings.length).toBe(4); // 0.25, 0.5, 0.75, 1.0
    expect(rings[0].points.split(' ').length).toBe(6);

    const spokes = generateAxisSpokes(6, center, 80);
    expect(spokes.length).toBe(6);
    expect(spokes[0].x1).toBe(100);
    expect(spokes[0].y1).toBe(100);
  });

  it('computes axis label positions with correct alignment attributes', () => {
    const sofa = getCalc('calc_sofa');
    const center = { x: 100, y: 100 };
    const labelPositions = getAxisLabelPositions(sofa.radarAxes, center, 80, 20);

    expect(labelPositions.length).toBe(6);
    expect(labelPositions[0].id).toBe('axis_sofa_resp');
    // Top axis should have textAnchor middle
    expect(labelPositions[0].textAnchor).toBe('middle');
  });
});

// ============================================================================
// 4. PEP EXPORT ENGINE TESTS
// ============================================================================

describe('pepExportEngine', () => {
  const sofa = getCalc('calc_sofa');

  it('generates structured plain-text SOAP note for hospital EHR copy', () => {
    const calcResult = calculateScore(sofa, {
      grp_sofa_resp: 'opt_sofa_resp_2',
      grp_sofa_cv: 'opt_sofa_cv_3'
    });

    const note = generatePepNote({
      calculator: sofa,
      result: calcResult,
      patientBed: 'Leito 04 - UTI',
      patientWeightKg: 70,
      creatinineClearanceMlMin: 65,
      bicInfusion: {
        drugName: 'Noradrenalina',
        dilution: '16 mg em 234 mL SG 5% (64 mcg/mL)',
        doseFormatted: '0.15 mcg/kg/min',
        rateMlPerHour: 9.84,
        recommendedVehicle: 'Soro Glicosado 5% (SG 5%)',
        containerAlert: 'Acesso venoso central exclusivo'
      },
      physicianIdentifier: 'Dr. Lucas Silveira - CRM/SP 123456'
    });

    expect(note).toContain('[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]');
    expect(note).toContain('PACIENTE: Leito 04 - UTI | Peso: 70 kg | ClCr Est.: 65 mL/min');
    expect(note).toContain('S (Subjetivo):');
    expect(note).toContain('O (Objetivo):');
    expect(note).toContain('Sequential Organ Failure Assessment (SOFA)');
    expect(note).toContain('Radar Fisiológico:');
    expect(note).toContain('A (Avaliação):');
    expect(note).toContain('P (Plano / Condutas Imediatas):');
    expect(note).toContain('Noradrenalina em 16 mg em 234 mL SG 5% (64 mcg/mL) a 0.15 mcg/kg/min');
    expect(note).toContain('Vazão em BIC: 9.8 mL/h');
    expect(note).toContain('Dr. Lucas Silveira - CRM/SP 123456');
  });

  it('guarantees zero LGPD leakage by sanitizing bed identifier and stripping CPFs', () => {
    // Sanitizes raw number
    expect(sanitizeBedIdentifier('12')).toBe('Leito 12');
    // Keeps valid ward identifier
    expect(sanitizeBedIdentifier('Box 03 - Sala Vermelha')).toBe('Box 03 - Sala Vermelha');
    // Default when empty
    expect(sanitizeBedIdentifier('')).toBe('Leito -- (Anônimo)');

    // Strips CPF numbers accidentally passed
    const strippedCpf = sanitizeBedIdentifier('Paciente 123.456.789-00 Leito 05');
    expect(strippedCpf).not.toContain('123.456.789-00');
    expect(strippedCpf).toContain('[REMOVIDO]');
  });

  it('generates alternative SBAR clinical handover format', () => {
    const qsofa = getCalc('calc_qsofa');
    const calcResult = calculateScore(qsofa, {
      grp_qsofa_resp: 'opt_resp_high',
      grp_qsofa_sbp: 'opt_sbp_low'
    });

    const sbar = generateSbarNote({
      calculator: qsofa,
      result: calcResult,
      patientBed: 'Box 02 - Emergência'
    });

    expect(sbar).toContain('[SCOREBOARD CDSS - PASSAGEM DE PLANTÃO SBAR]');
    expect(sbar).toContain('S (Situação):');
    expect(sbar).toContain('B (Breve Histórico):');
    expect(sbar).toContain('A (Avaliação):');
    expect(sbar).toContain('R (Recomendação):');
    expect(sbar).toContain('qSOFA = 2 pontos');
  });

  it('formats dates consistently in Brazilian DD/MM/AAAA - HH:MM format', () => {
    const date = new Date(2026, 8, 22, 14, 30); // 22 Sept 2026 14:30
    const formatted = formatDateBrazilian(date);
    expect(formatted).toBe('22/09/2026 - 14:30');
  });

  it('summarizes radar physiological deviations accurately', () => {
    const summary = summarizeRadarDeviations(sofa.radarAxes, {
      axis_sofa_cv: 1.0,
      axis_sofa_resp: 0.5,
      axis_sofa_coag: 0.0
    });
    expect(summary).toContain('Cardiovascular (crítico: 100%)');
    expect(summary).toContain('Respiratório (moderado: 50%)');
    expect(summary).not.toContain('Coagulação');
  });

  it('handles empty / edge inputs gracefully in PEP note generation without crashing', () => {
    const qsofa = getCalc('calc_qsofa');
    const calcResult = calculateScore(qsofa, {});

    const minimalNote = generatePepNote({
      calculator: qsofa,
      result: calcResult
    });

    expect(minimalNote).toContain('[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]');
    expect(minimalNote).toContain('Leito -- (Anônimo)');
    expect(minimalNote).toContain('O (Objetivo):');
    expect(minimalNote).toContain('A (Avaliação):');
    expect(minimalNote).toContain('P (Plano / Condutas Imediatas):');
  });
});

// ============================================================================
// 5. ADDITIONAL BOUNDARY & ERROR HANDLING TESTS
// ============================================================================

describe('Engine Boundary & Error Handling', () => {
  it('infusionEngine enforces strict physical parameter validation', () => {
    // Non-positive weight for weight-dependent drug
    expect(() => {
      calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 0,
        doseValue: 0.1,
        concentrationMcgPerMl: 64
      });
    }).toThrow('Patient weight must be greater than zero');

    expect(() => {
      calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: -10,
        doseValue: 0.1,
        concentrationMcgPerMl: 64
      });
    }).toThrow('Patient weight must be greater than zero');

    // Non-positive concentration
    expect(() => {
      calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 70,
        doseValue: 0.1,
        concentrationMcgPerMl: 0
      });
    }).toThrow('Solution concentration must be greater than zero');

    // Negative dose
    expect(() => {
      calculateInfusionRate({
        drugId: 'norepinephrine',
        patientWeightKg: 70,
        doseValue: -0.1,
        concentrationMcgPerMl: 64
      });
    }).toThrow('Dose value must be non-negative');
  });

  it('radarEngine handles extreme / boundary values safely', () => {
    // Clamping values outside [0, 1]
    expect(normalizeAxisValue(100, 0, 10)).toBe(1.0);
    expect(normalizeAxisValue(-50, 0, 10)).toBe(0.0);
    expect(normalizeAxisValue(5, 5, 5)).toBe(0.0); // baseline == max edge case

    // Polygon generation with < 3 axes
    expect(generateBaselinePolygon(2, { x: 0, y: 0 }, 50)).toBe('');
    expect(generateGridRings(2, { x: 0, y: 0 }, 50)).toEqual([]);
    expect(calculatePolygonPoints([], { x: 0, y: 0 }, 50)).toBe('');
    expect(calculateAxisAngle(0, 0)).toBe(-Math.PI / 2);
  });

  it('calculationEngine falls back to normal baseline when option is not recognized', () => {
    const qsofa = getCalc('calc_qsofa');
    // Non-existent option ID -> falls back to baseline (0 pts)
    const result = calculateScore(qsofa, {
      grp_qsofa_resp: 'non_existent_option_id'
    });
    expect(result.rawScore).toBe(0);
    expect(result.activeRiskTier.id).toBe('tier_qsofa_low');
  });

  it('verifies round-trip fidelity of Ureia and BUN conversions across various levels', () => {
    const testLevels = [10, 20, 25, 30, 50, 100, 150];
    for (const bun of testLevels) {
      const ureia = convertBunToUreia(bun);
      const roundTripBun = convertUreiaToBun(ureia);
      expect(roundTripBun).toBeCloseTo(bun, 5);
    }
  });
});
