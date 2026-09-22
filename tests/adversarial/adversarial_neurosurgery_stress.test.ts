/**
 * EMPIRICAL ADVERSARIAL STRESS TEST SUITE — CHALLENGER NEURO 1
 * Targets:
 *   - src/engines/calculationEngine.ts
 *   - src/data/blocks/block_03.json
 *   - tests/unit/test_neurosurgery_cutoffs.test.ts
 *
 * 10 Empirical Challenge Areas:
 * 1. Spinopelvic Sagittal Balance (PI = PT + SS, PI-LL mismatch, SRS-Schwab cutoffs, negative lordosis, radar key integrity)
 * 2. NOMS Framework (Bilsky 0-3, radiosensitivity, SINS, KPS systemic fitness, pathway naming & radar key integrity)
 * 3. Lawton-Young Supplementary AVM (Spetzler-Martin I-V, age tiers, rupture, compactness, combined 2-10, radar key integrity)
 * 4. PHASES Score (Combinatorial point verification 0-22, Greving 2014 5-year curve, size boundaries, radar key integrity)
 * 5. TLICS (Morphology, PLC, Neuro, cutoffs <=3, 4, >=5, incomplete vs complete cord)
 * 6. SLICS (Morphology, DLC, Neuro, progressive modifier, cutoffs <=3, 4, >=5)
 * 7. SINS (6 dimensions, 0-18 sum, boundaries 6 vs 7, 12 vs 13, stability tiers)
 * 8. Anderson-D'Alonzo (Type I, IIB anterior screw, IIC Harms-Goel posterior, Type III cancellous)
 * 9. Vasograde (WFNS 1-5 x Modified Fisher 0-4, Green / Yellow / Red, input resilience, IV nimodipine prohibition)
 * 10. Kiefer (0-24 pts, Tap Test delta >= 2) & Evans/DESH (Evans >= 0.30, DESH, callosal angle, Alzheimer differential)
 */

import { describe, it, expect } from 'vitest';
import rawBlock03Data from '@/data/blocks/block_03.json';
import {
  calculateScore,
  calculateSagittalBalance,
  calculateNomsFramework,
  calculateLawtonYoung,
  calculatePhasesScore
} from '@/engines/calculationEngine';
import { type Calculator, type BlockData } from '@/types/clinical';

const parsedBlock03: BlockData = rawBlock03Data as unknown as BlockData;

function getTool(id: string): Calculator {
  const tool = parsedBlock03.calculators.find((c) => c.id === id);
  if (!tool) throw new Error(`Calculator ${id} not found in Block 03`);
  return tool;
}

describe('CHALLENGER NEURO 1: Empirical Adversarial Stress Suite', () => {

  // ==========================================================================
  // 1. SPINOPELVIC SAGITTAL BALANCE
  // ==========================================================================
  describe('Challenge 1: Spinopelvic Sagittal Balance & SRS-Schwab', () => {
    const tool = getTool('calc_sagittal_balance');

    it('empirically verifies Duval-Beaupère identity PI = PT + SS boundary at exactly 3.0° vs 3.01°', () => {
      // Exactly 3.0° difference: PI = 56, PT = 13, SS = 40 (PT + SS = 53, diff = 3.0) -> NO warning
      const res30 = calculateSagittalBalance({ pi: 56, pt: 13, ss: 40, ll: 56, sva: 20 });
      expect(res30.warnings).toBeUndefined();

      // Slightly above 3.0°: PI = 56.1, PT = 13, SS = 40 (PT + SS = 53, diff = 3.1) -> WARNING triggered
      const res31 = calculateSagittalBalance({ pi: 56.1, pt: 13, ss: 40, ll: 56, sva: 20 });
      expect(res31.warnings).toBeDefined();
      expect(res31.warnings?.[0]).toContain('Inconsistência geométrica espinopélvica');
      expect(res31.warnings?.[0]).toContain('3.1° > 3°');
    });

    it('verifies floating point precision resilience in geometric diff calculation', () => {
      // 53.05 - (13.00 + 40.05) = 0.00 (IEEE-754 precision)
      const resFloat = calculateSagittalBalance({ pi: 53.05, pt: 13.0, ss: 40.05, ll: 53.05, sva: 20.0 });
      expect(resFloat.warnings).toBeUndefined();
    });

    it('verifies SRS-Schwab PI - LL mismatch boundaries (9.9° vs 10.0° vs 20.0° vs 20.1°)', () => {
      // 9.9° -> Schwab 0 (Aligned)
      const res99 = calculateSagittalBalance({ pi: 59.9, pt: 13, ss: 46.9, ll: 50.0, sva: 20 });
      expect(res99.rawScore).toBe(9.9);
      expect(res99.scoreFormatted).toContain('Schwab 0');
      expect(res99.activeRiskTier.severityLevel).toBe('low');

      // 10.0° -> Schwab + (Moderate mismatch)
      const res100 = calculateSagittalBalance({ pi: 60.0, pt: 13, ss: 47.0, ll: 50.0, sva: 20 });
      expect(res100.rawScore).toBe(10.0);
      expect(res100.scoreFormatted).toContain('Schwab +');
      expect(res100.activeRiskTier.severityLevel).toBe('intermediate');

      // 20.0° -> Schwab + (Moderate mismatch boundary)
      const res200 = calculateSagittalBalance({ pi: 70.0, pt: 15, ss: 55.0, ll: 50.0, sva: 20 });
      expect(res200.rawScore).toBe(20.0);
      expect(res200.scoreFormatted).toContain('Schwab +');
      expect(res200.activeRiskTier.severityLevel).toBe('intermediate');

      // 20.1° -> Schwab ++ (Severe mismatch)
      const res201 = calculateSagittalBalance({ pi: 70.1, pt: 15, ss: 55.1, ll: 50.0, sva: 20 });
      expect(res201.rawScore).toBe(20.1);
      expect(res201.scoreFormatted).toContain('Schwab ++');
      expect(res201.activeRiskTier.severityLevel).toBe('critical');
    });

    it('verifies PT and SVA boundary cutoffs (PT 19.9 vs 20.0 vs 30.0 vs 30.1; SVA 39.9 vs 40.0 vs 95.0 vs 95.1)', () => {
      // PT: 19.9 Normal, 20.0 Moderate, 30.0 Moderate, 30.1 Severe
      const ptNormal = calculateSagittalBalance({ pt: 19.9 });
      expect(ptNormal.scoreFormatted).toContain('PT: Normal');

      const ptMod = calculateSagittalBalance({ pt: 20.0 });
      expect(ptMod.scoreFormatted).toContain('PT: Moderate');

      const ptModHigh = calculateSagittalBalance({ pt: 30.0 });
      expect(ptModHigh.scoreFormatted).toContain('PT: Moderate');

      const ptSevere = calculateSagittalBalance({ pt: 30.1 });
      expect(ptSevere.scoreFormatted).toContain('PT: Severe retroversion');

      // SVA: 39.9 Normal, 40.0 Moderate, 95.0 Moderate, 95.1 Severe
      const svaNormal = calculateSagittalBalance({ sva: 39.9 });
      expect(svaNormal.scoreFormatted).toContain('SVA: Normal');

      const svaMod = calculateSagittalBalance({ sva: 40.0 });
      expect(svaMod.scoreFormatted).toContain('SVA: Moderate');

      const svaModHigh = calculateSagittalBalance({ sva: 95.0 });
      expect(svaModHigh.scoreFormatted).toContain('SVA: Moderate');

      const svaSevere = calculateSagittalBalance({ sva: 95.1 });
      expect(svaSevere.scoreFormatted).toContain('SVA: Severe');
    });

    it('stress-tests extreme negative lordosis (lumbar kyphosis: LL = -15°)', () => {
      // Severe flatback / lumbar kyphosis: PI = 53°, LL = -15° -> PI - LL = 53 - (-15) = 68°!
      const resKyphosis = calculateSagittalBalance({ pi: 53, pt: 32, ss: 21, ll: -15, sva: 130 });
      expect(resKyphosis.rawScore).toBe(68.0);
      expect(resKyphosis.scoreFormatted).toContain('+68.0°');
      expect(resKyphosis.scoreFormatted).toContain('Schwab ++');
      expect(resKyphosis.activeRiskTier.severityLevel).toBe('critical');
      expect(resKyphosis.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Osteotomia de Subtração Pedicular (PSO / Schwab Grau III)'
      );
    });

    it('stress-tests extreme multiapical deformity values (PI 95, PT 45, SS 50, LL 10, SVA 220)', () => {
      const resExtreme = calculateSagittalBalance({ pi: 95, pt: 45, ss: 50, ll: 10, sva: 220 });
      expect(resExtreme.rawScore).toBe(85.0);
      expect(resExtreme.activeRiskTier.severityLevel).toBe('critical');
      expect(resExtreme.radarValues['axis_sagittal_deformity']).toBe(1.0);
    });

    it('verifies radarAxis ID synchronization for sagittal balance (both axis_sb_* and legacy axis_*)', () => {
      // In block_03.json, radarAxes are: axis_sb_pi_ll, axis_sb_pt, axis_sb_sva
      // In calculationEngine.ts, both axis_sb_* and legacy axis_* are populated
      const res = calculateScore(tool, { pi: 65, pt: 35, ss: 30, ll: 35, sva: 110 });

      const block03AxisIds = tool.radarAxes.map((a) => a.id);
      expect(block03AxisIds).toEqual(['axis_sb_pi_ll', 'axis_sb_pt', 'axis_sb_sva']);

      // Synchronized radar axes:
      expect(res.radarValues['axis_sb_pi_ll']).toBeGreaterThan(0);
      expect(res.radarValues['axis_pi_ll']).toBeGreaterThan(0);
      expect(res.radarValues['axis_sb_pt']).toBeGreaterThan(0);
      expect(res.radarValues['axis_pt']).toBeGreaterThan(0);
      expect(res.radarValues['axis_sb_sva']).toBeGreaterThan(0);
      expect(res.radarValues['axis_sva']).toBeGreaterThan(0);
    });
  });

  // ==========================================================================
  // 2. NOMS DECISION FRAMEWORK
  // ==========================================================================
  describe('Challenge 2: NOMS Framework & Bilsky ESCC Decision Matrix', () => {
    const tool = getTool('calc_noms_bilsky');

    it('empirically tests all 6 Bilsky grades (0, 1a, 1b, 1c, 2, 3) across radiosensitive and radioresistant tumors', () => {
      // High grade: 2 and 3
      const g2Res = calculateNomsFramework({ bilsky: '2', radiosensitivity: 'radioresistant', sins: 5, kps: 80 });
      expect(g2Res.scoreFormatted).toContain('Separation Surgery + SBRT');

      const g3Res = calculateNomsFramework({ bilsky: '3', radiosensitivity: 'radioresistant', sins: 5, kps: 80 });
      expect(g3Res.scoreFormatted).toContain('Separation Surgery + SBRT');

      // Low grade (0, 1a, 1b, 1c) with stable spine and radioresistant tumor -> Primary SBRT
      for (const grade of ['0', '1a', '1b', '1c']) {
        const res = calculateNomsFramework({ bilsky: grade, radiosensitivity: 'radioresistant', sins: 4, kps: 80 });
        // Verifies correct clinical indication: scoreFormatted contains 'Primary SBRT'
        expect(res.scoreFormatted).toContain('Primary SBRT');
        // While the activeRiskTier.label correctly states Primary SBRT:
        expect(res.activeRiskTier.label).toContain('SBRT Primária Isolada');
      }

      // Radiosensitive high grade: Bilsky 3 + radiosensitive -> cEBRT alone (rapid cellular lysis)
      const radioSens = calculateNomsFramework({ bilsky: '3', radiosensitivity: 'mieloma', sins: 4, kps: 80 });
      expect(radioSens.scoreFormatted).toContain('cEBRT alone');
      expect(radioSens.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('verifies mechanical instability cutoff in NOMS: SINS >= 13 converts radiosensitive cEBRT into cEBRT + Stabilization', () => {
      // SINS 12 (potentially unstable) + Bilsky 3 + radiosensitive -> cEBRT alone
      const res12 = calculateNomsFramework({ bilsky: '3', radiosensitivity: 'radiosensitive', sins: 12, kps: 80 });
      expect(res12.scoreFormatted).toContain('cEBRT alone');
      expect(res12.activeRiskTier.severityLevel).toBe('intermediate');

      // SINS 13 (unstable boundary) + Bilsky 3 + radiosensitive -> cEBRT + Stabilization
      const res13 = calculateNomsFramework({ bilsky: '3', radiosensitivity: 'radiosensitive', sins: 13, kps: 80 });
      expect(res13.scoreFormatted).toContain('cEBRT alone'); // title in scoreFormatted
      expect(res13.activeRiskTier.id).toBe('tier_noms_cebrt_stabilization');
      expect(res13.activeRiskTier.severityLevel).toBe('high');
      expect(res13.activeRiskTier.label).toContain('Radioterapia Convencional de Urgência + Estabilização Cirúrgica');
    });

    it('verifies systemic ineligibility override (KPS < 70% or terminal status): Palliative Hospice dominates even for Bilsky 3', () => {
      const resPalliative = calculateNomsFramework({
        bilsky: '3',
        radiosensitivity: 'radioresistant',
        sins: 16,
        kps: 50 // KPS < 70
      });
      expect(resPalliative.scoreFormatted).toContain('Palliative Hospice');
      expect(resPalliative.activeRiskTier.id).toBe('tier_noms_palliative');
      expect(resPalliative.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia descompressiva e reconstrução instrumentada aberta estão formalmente contraindicadas'
      );
    });

    it('verifies radar key axis_noms_syst synchronization in NOMS', () => {
      const res = calculateScore(tool, {
        grp_noms_neuro: 'opt_bilsky_2',
        grp_noms_oncologic: 'opt_onco_radioresistant',
        grp_noms_mechanical: 'opt_sins_stable',
        grp_noms_systemic: 'opt_kps_ge70'
      });

      const block03AxisIds = tool.radarAxes.map((a) => a.id);
      expect(block03AxisIds).toContain('axis_noms_syst');

      // Both axis_noms_syst and axis_noms_sys are populated
      expect(res.radarValues['axis_noms_sys']).toBeDefined();
      expect(res.radarValues['axis_noms_sys']).toBeGreaterThan(0);
      expect(res.radarValues['axis_noms_syst']).toBeDefined();
      expect(res.radarValues['axis_noms_syst']).toBeGreaterThan(0);
    });
  });

  // ==========================================================================
  // 3. LAWTON-YOUNG SUPPLEMENTARY AVM GRADING SYSTEM
  // ==========================================================================
  describe('Challenge 3: Lawton-Young Supplementary AVM Score', () => {
    const tool = getTool('calc_lawton_young');

    it('empirically verifies age tiers (<20: 1 pt, 20-40: 2 pts, >40: 3 pts) at exact boundaries', () => {
      // Age 19 -> 1 pt
      const res19 = calculateLawtonYoung({ spetzlerMartin: 1, age: 19, ruptured: true, compactness: 'compact' });
      expect(res19.rawScore).toBe(2); // SM 1 + LY (1 + 0 + 0) = 2

      // Age 20 -> 2 pts
      const res20 = calculateLawtonYoung({ spetzlerMartin: 1, age: 20, ruptured: true, compactness: 'compact' });
      expect(res20.rawScore).toBe(3); // SM 1 + LY (2 + 0 + 0) = 3

      // Age 40 -> 2 pts
      const res40 = calculateLawtonYoung({ spetzlerMartin: 1, age: 40, ruptured: true, compactness: 'compact' });
      expect(res40.rawScore).toBe(3); // SM 1 + LY (2 + 0 + 0) = 3

      // Age 41 -> 3 pts
      const res41 = calculateLawtonYoung({ spetzlerMartin: 1, age: 41, ruptured: true, compactness: 'compact' });
      expect(res41.rawScore).toBe(4); // SM 1 + LY (3 + 0 + 0) = 4
    });

    it('verifies unruptured (+1) vs ruptured (0) and diffuse (+1) vs compact (0) point contributions', () => {
      // Ruptured (0) + Compact (0)
      const resRC = calculateLawtonYoung({ spetzlerMartin: 2, age: 25, ruptured: true, compactness: 'compact' });
      expect(resRC.rawScore).toBe(4); // SM 2 + LY (2 + 0 + 0) = 4

      // Unruptured (+1) + Compact (0)
      const resUC = calculateLawtonYoung({ spetzlerMartin: 2, age: 25, unruptured: true, compactness: 'compact' });
      expect(resUC.rawScore).toBe(5); // SM 2 + LY (2 + 1 + 0) = 5

      // Unruptured (+1) + Diffuse (+1)
      const resUD = calculateLawtonYoung({ spetzlerMartin: 2, age: 25, unruptured: true, compactness: 'diffuse' });
      expect(resUD.rawScore).toBe(6); // SM 2 + LY (2 + 1 + 1) = 6
    });

    it('empirically verifies the full combined score spectrum from 2 to 10 points and ARUBA cutoff (>= 7)', () => {
      // Score 2: SM 1, Age 18 (1), Ruptured (0), Compact (0) -> 2 pts (Low risk)
      const res2 = calculateLawtonYoung({ spetzlerMartin: 1, age: 18, ruptured: true, compactness: 'compact' });
      expect(res2.rawScore).toBe(2);
      expect(res2.activeRiskTier.severityLevel).toBe('low');

      // Score 4: SM 2, Age 25 (2), Ruptured (0), Compact (0) -> 4 pts (Upper bound of low risk)
      const res4 = calculateLawtonYoung({ spetzlerMartin: 2, age: 25, ruptured: true, compactness: 'compact' });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.severityLevel).toBe('low');

      // Score 5: SM 3, Age 25 (2), Ruptured (0), Compact (0) -> 5 pts (Lower bound of intermediate)
      const res5 = calculateLawtonYoung({ spetzlerMartin: 3, age: 25, ruptured: true, compactness: 'compact' });
      expect(res5.rawScore).toBe(5);
      expect(res5.activeRiskTier.severityLevel).toBe('intermediate');

      // Score 6: SM 3, Age 45 (3), Ruptured (0), Compact (0) -> 6 pts (Upper bound of intermediate)
      const res6 = calculateLawtonYoung({ spetzlerMartin: 3, age: 45, ruptured: true, compactness: 'compact' });
      expect(res6.rawScore).toBe(6);
      expect(res6.activeRiskTier.severityLevel).toBe('intermediate');

      // Score 7: SM 4, Age 45 (3), Ruptured (0), Compact (0) -> 7 pts (ARUBA prohibitive boundary)
      const res7 = calculateLawtonYoung({ spetzlerMartin: 4, age: 45, ruptured: true, compactness: 'compact' });
      expect(res7.rawScore).toBe(7);
      expect(res7.activeRiskTier.severityLevel).toBe('critical');
      expect(res7.activeRiskTier.label).toContain('Risco Cirúrgico Proibitivo');

      // Score 10: SM 5, Age 50 (3), Unruptured (1), Diffuse (1) -> 10 pts (Maximum)
      const res10 = calculateLawtonYoung({ spetzlerMartin: 5, age: 50, unruptured: true, compactness: 'diffuse' });
      expect(res10.rawScore).toBe(10);
      expect(res10.activeRiskTier.severityLevel).toBe('critical');
    });

    it('verifies radarAxis synchronization in Lawton-Young (both axis_ly_* and axis_mav_*)', () => {
      const res = calculateScore(tool, {
        grp_ly_sm: 'opt_ly_sm_3',
        grp_ly_age: 'opt_ly_age_20_40',
        grp_ly_rupture: 'opt_ly_rup_yes',
        grp_ly_compact: 'opt_ly_comp_compact'
      });

      const block03AxisIds = tool.radarAxes.map((a) => a.id);
      expect(block03AxisIds).toEqual(['axis_ly_sm', 'axis_ly_age', 'axis_ly_rupture', 'axis_ly_compact']);

      // Both axis_ly_* and axis_mav_* are populated
      expect(res.radarValues['axis_mav_size']).toBeDefined();
      expect(res.radarValues['axis_mav_eloquence']).toBeDefined();
      expect(res.radarValues['axis_mav_surgical_risk']).toBeDefined();

      expect(res.radarValues['axis_ly_sm']).toBeGreaterThan(0);
      expect(res.radarValues['axis_ly_age']).toBeGreaterThan(0);
      expect(res.radarValues['axis_ly_rupture']).toBeDefined();
      expect(res.radarValues['axis_ly_compact']).toBeDefined();
    });
  });

  // ==========================================================================
  // 4. PHASES SCORE
  // ==========================================================================
  describe('Challenge 4: PHASES Rupture Risk Engine & Greving 2014 Table', () => {
    const tool = getTool('calc_phases_score');

    it('empirically verifies the Greving 2014 5-year rupture probability curve across all scores 0-22', () => {
      const expectedCurve: Record<number, string> = {
        0: '0.4%',
        1: '0.4%',
        2: '0.7%',
        3: '0.7%',
        4: '0.9%',
        5: '1.3%',
        6: '1.7%',
        7: '2.4%',
        8: '3.2%',
        9: '4.3%',
        10: '5.3%',
        11: '7.2%',
        12: '9.8%',
        13: '13.0%',
        14: '15.3%',
        15: '> 17.8%',
        16: '> 17.8%',
        17: '> 17.8%',
        18: '> 17.8%',
        19: '> 17.8%',
        20: '> 17.8%',
        21: '> 17.8%',
        22: '> 17.8%'
      };

      for (let s = 0; s <= 22; s++) {
        const inputs = constructPhasesInputsForScore(s);
        const res = calculatePhasesScore(inputs);
        expect(res.rawScore).toBe(s);
        expect(res.scoreFormatted).toContain(expectedCurve[s]);
      }
    });

    it('verifies size threshold cutoffs (<7.0: 0, 7.0-9.9: 3, 10.0-19.9: 6, >=20.0: 10)', () => {
      expect(calculatePhasesScore({ size: 6.9 }).rawScore).toBe(0);
      expect(calculatePhasesScore({ size: 7.0 }).rawScore).toBe(3);
      expect(calculatePhasesScore({ size: 9.9 }).rawScore).toBe(3);
      expect(calculatePhasesScore({ size: 10.0 }).rawScore).toBe(6);
      expect(calculatePhasesScore({ size: 19.9 }).rawScore).toBe(6);
      expect(calculatePhasesScore({ size: 20.0 }).rawScore).toBe(10);
    });

    it('verifies surgical decision cutoffs: <=3 (Conservative), 4-7 (Borderline), >=8 (Mandatory Surgery)', () => {
      // Score 3: Low
      const res3 = calculatePhasesScore({ population: 'japan' }); // 3
      expect(res3.rawScore).toBe(3);
      expect(res3.activeRiskTier.severityLevel).toBe('low');

      // Score 4: Intermediate
      const res4 = calculatePhasesScore({ site: 'posterior' }); // 4
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.severityLevel).toBe('intermediate');

      // Score 7: Intermediate boundary
      const res7 = calculatePhasesScore({ population: 'finland', site: 'mca' }); // 5 + 2 = 7
      expect(res7.rawScore).toBe(7);
      expect(res7.activeRiskTier.severityLevel).toBe('intermediate');

      // Score 8: Critical / Surgical
      const res8 = calculatePhasesScore({ population: 'finland', site: 'mca', hypertension: true }); // 5 + 2 + 1 = 8
      expect(res8.rawScore).toBe(8);
      expect(res8.activeRiskTier.severityLevel).toBe('critical');
      expect(res8.activeRiskTier.label).toContain('Alto a Muito Alto Risco de Ruptura');
    });

    it('verifies radarAxis synchronization in PHASES (both axis_ph_* and axis_aneurysm_*)', () => {
      const res = calculateScore(tool, {
        grp_phases_pop: 'opt_ph_pop_japan',
        grp_phases_htn: 'opt_ph_htn_yes',
        grp_phases_age: 'opt_ph_age_gte70',
        grp_phases_size: 'opt_ph_size_10_19',
        grp_phases_earlier_sah: 'opt_ph_sah_no',
        grp_phases_site: 'opt_ph_site_mca'
      });

      const block03AxisIds = tool.radarAxes.map((a) => a.id);
      expect(block03AxisIds).toEqual(['axis_ph_morphology', 'axis_ph_site', 'axis_ph_demographic', 'axis_ph_clinical']);

      // Both axis_ph_* and axis_aneurysm_* are populated
      expect(res.radarValues['axis_aneurysm_size']).toBeGreaterThan(0);
      expect(res.radarValues['axis_aneurysm_site']).toBeGreaterThan(0);
      expect(res.radarValues['axis_rupture_risk']).toBeGreaterThan(0);

      expect(res.radarValues['axis_ph_morphology']).toBeGreaterThan(0);
      expect(res.radarValues['axis_ph_site']).toBeGreaterThan(0);
      expect(res.radarValues['axis_ph_demographic']).toBeGreaterThan(0);
      expect(res.radarValues['axis_ph_clinical']).toBeGreaterThan(0);
    });
  });

  // ==========================================================================
  // 5. TLICS: THORACOLUMBAR SPINE TRAUMA
  // ==========================================================================
  describe('Challenge 5: TLICS Cutoffs & Biological Incomplete Deficit Logic', () => {
    const tool = getTool('calc_tlics');

    it('validates the complete spectrum of scores from 1 to 10 points', () => {
      // Min score is 1 (compression 1 + intact PLC 0 + intact neuro 0)
      const resMin = calculateScore(tool, {
        grp_tlics_morphology: 'opt_tlics_morph_comp',
        grp_tlics_plc: 'opt_tlics_plc_intact',
        grp_tlics_neuro: 'opt_tlics_neuro_intact'
      });
      expect(resMin.rawScore).toBe(1);
      expect(resMin.activeRiskTier.severityLevel).toBe('low');

      // Max score is 10 (distraction 4 + disrupted PLC 3 + incomplete neuro 3)
      const resMax = calculateScore(tool, {
        grp_tlics_morphology: 'opt_tlics_morph_distr',
        grp_tlics_plc: 'opt_tlics_plc_disrupt',
        grp_tlics_neuro: 'opt_tlics_neuro_incomplete'
      });
      expect(resMax.rawScore).toBe(10);
      expect(resMax.activeRiskTier.severityLevel).toBe('critical');
    });

    it('verifies clinical triage cutoffs: <=3 (Conservative), 4 (Borderline), >=5 (Mandatory Surgery)', () => {
      // Score 3
      const res3 = calculateScore(tool, {
        grp_tlics_morphology: 'opt_tlics_morph_comp', // 1
        grp_tlics_plc: 'opt_tlics_plc_suspect',       // 2
        grp_tlics_neuro: 'opt_tlics_neuro_intact'     // 0
      });
      expect(res3.rawScore).toBe(3);
      expect(res3.activeRiskTier.id).toBe('tier_tlics_cons');

      // Score 4
      const res4 = calculateScore(tool, {
        grp_tlics_morphology: 'opt_tlics_morph_burst', // 2
        grp_tlics_plc: 'opt_tlics_plc_suspect',        // 2
        grp_tlics_neuro: 'opt_tlics_neuro_intact'      // 0
      });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_tlics_lim');

      // Score 5
      const res5 = calculateScore(tool, {
        grp_tlics_morphology: 'opt_tlics_morph_burst',  // 2
        grp_tlics_plc: 'opt_tlics_plc_disrupt',        // 3
        grp_tlics_neuro: 'opt_tlics_neuro_intact'      // 0
      });
      expect(res5.rawScore).toBe(5);
      expect(res5.activeRiskTier.id).toBe('tier_tlics_surg');
    });
  });

  // ==========================================================================
  // 6. SLICS: SUBAXIAL CERVICAL SPINE TRAUMA
  // ==========================================================================
  describe('Challenge 6: SLICS Subaxial Cervical Trauma & Progressive Modifier', () => {
    const tool = getTool('calc_slics');

    it('verifies score spectrum from 0 to 10 points and radar axis alignment', () => {
      const res0 = calculateScore(tool, {
        grp_slics_morphology: 'opt_slics_morph_none',
        grp_slics_dlc: 'opt_slics_dlc_intact',
        grp_slics_neuro: 'opt_slics_neuro_intact',
        grp_slics_modifier: 'opt_slics_mod_no'
      });
      expect(res0.rawScore).toBe(0);
      expect(res0.activeRiskTier.severityLevel).toBe('low');

      const res10 = calculateScore(tool, {
        grp_slics_morphology: 'opt_slics_morph_trans', // 4
        grp_slics_dlc: 'opt_slics_dlc_disrupt',        // 2
        grp_slics_neuro: 'opt_slics_neuro_incomp',     // 3
        grp_slics_modifier: 'opt_slics_mod_yes'        // 1 -> total = 10
      });
      expect(res10.rawScore).toBe(10);
      expect(res10.activeRiskTier.severityLevel).toBe('critical');
    });

    it('verifies that SLICS radar axes correctly match block_03 definitions', () => {
      const res = calculateScore(tool, {
        grp_slics_morphology: 'opt_slics_morph_trans',
        grp_slics_dlc: 'opt_slics_dlc_disrupt',
        grp_slics_neuro: 'opt_slics_neuro_incomp',
        grp_slics_modifier: 'opt_slics_mod_yes'
      });

      // SLICS uses the generic engine, so its radar keys directly match block_03:
      expect(res.radarValues['axis_slics_morph']).toBe(1.0);
      expect(res.radarValues['axis_slics_dlc']).toBe(1.0);
      expect(res.radarValues['axis_slics_neuro']).toBe(1.0);
      expect(res.radarValues['axis_slics_mod']).toBe(1.0);
    });
  });

  // ==========================================================================
  // 7. SINS: SPINE INSTABILITY NEOPLASTIC SCORE
  // ==========================================================================
  describe('Challenge 7: SINS Metastatic Instability & Boundary Integrity', () => {
    const tool = getTool('calc_sins');

    it('verifies all 6 criteria summing strictly from 0 to 18 points', () => {
      expect(tool.parameterGroups.length).toBe(6);
      expect(tool.minPossibleScore).toBe(0);
      expect(tool.maxPossibleScore).toBe(18);

      const res0 = calculateScore(tool, {});
      expect(res0.rawScore).toBe(0);
      expect(res0.activeRiskTier.id).toBe('tier_sins_stable');
    });

    it('validates critical boundaries: 6 vs 7 (stable to potentially unstable) and 12 vs 13 (potentially unstable to unstable)', () => {
      // 6 pts -> Stable
      const res6 = calculateScore(tool, {
        grp_sins_location: 'opt_sins_loc_mob',     // 2
        grp_sins_pain: 'opt_sins_pain_nonmech',    // 1
        grp_sins_bone: 'opt_sins_bone_mixed',      // 1
        grp_sins_alignment: 'opt_sins_align_denovo' // 2
      });
      expect(res6.rawScore).toBe(6);
      expect(res6.activeRiskTier.id).toBe('tier_sins_stable');
      expect(res6.activeRiskTier.severityLevel).toBe('low');

      // 7 pts -> Potentially Unstable
      const res7 = calculateScore(tool, {
        grp_sins_location: 'opt_sins_loc_junc', // 3
        grp_sins_pain: 'opt_sins_pain_mech',    // 3
        grp_sins_posterior: 'opt_sins_post_unilat' // 1
      });
      expect(res7.rawScore).toBe(7);
      expect(res7.activeRiskTier.id).toBe('tier_sins_potential');
      expect(res7.activeRiskTier.severityLevel).toBe('intermediate');

      // 12 pts -> Potentially Unstable
      const res12 = calculateScore(tool, {
        grp_sins_location: 'opt_sins_loc_junc',     // 3
        grp_sins_pain: 'opt_sins_pain_mech',        // 3
        grp_sins_bone: 'opt_sins_bone_lytic',       // 2
        grp_sins_alignment: 'opt_sins_align_denovo', // 2
        grp_sins_collapse: 'opt_sins_coll_le50'     // 2
      });
      expect(res12.rawScore).toBe(12);
      expect(res12.activeRiskTier.id).toBe('tier_sins_potential');

      // 13 pts -> Unstable (Mandatory surgical fixation before RT)
      const res13 = calculateScore(tool, {
        grp_sins_location: 'opt_sins_loc_junc',      // 3
        grp_sins_pain: 'opt_sins_pain_mech',         // 3
        grp_sins_bone: 'opt_sins_bone_lytic',        // 2
        grp_sins_alignment: 'opt_sins_align_sublux',  // 4
        grp_sins_collapse: 'opt_sins_coll_inv_gt50'  // 1
      });
      expect(res13.rawScore).toBe(13);
      expect(res13.activeRiskTier.id).toBe('tier_sins_unstable');
      expect(res13.activeRiskTier.severityLevel).toBe('critical');
    });
  });

  // ==========================================================================
  // 8. ANDERSON-D'ALONZO & GRAUER SUBTYPES
  // ==========================================================================
  describe('Challenge 8: Anderson-D\'Alonzo C2 Fractures & Grauer Biomechanics', () => {
    const tool = getTool('calc_anderson_dalonzo');

    it('verifies Grauer IIB enables motion-preserving anterior screw', () => {
      const resIIB = calculateScore(tool, { grp_anderson_type: 'opt_od_type2_b' });
      expect(resIIB.activeRiskTier.id).toBe('tier_od_screw');
      expect(resIIB.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'parafusos canulados de rosca parcial de 3,5 mm'
      );
    });

    it('verifies clinical alignment for Grauer IIC (Harms-Goel) and Type III (Conservative)', () => {
      // 1. Grauer IIC (reverse oblique, cominutive) -> tier_od_harms (3 pts)
      const resIIC = calculateScore(tool, { grp_anderson_type: 'opt_od_type2_c' });
      expect(resIIC.rawScore).toBe(3);
      expect(resIIC.activeRiskTier.id).toBe('tier_od_harms');
      expect(resIIC.activeRiskTier.severityLevel).toBe('critical');
      expect(resIIC.activeRiskTier.label).toContain('Tipo IIC / Falha de Parafuso');

      // 2. Type III (cancellous body C2, high union rate) -> tier_od_cons (1 pt)
      const resType3 = calculateScore(tool, { grp_anderson_type: 'opt_od_type3' });
      expect(resType3.rawScore).toBe(1);
      expect(resType3.activeRiskTier.id).toBe('tier_od_cons');
      expect(resType3.activeRiskTier.severityLevel).toBe('low');
      expect(resType3.activeRiskTier.label).toContain('Tipos I e III: Tratamento Conservador');
    });
  });

  // ==========================================================================
  // 9. VASOGRADE DCI STRATIFICATION
  // ==========================================================================
  describe('Challenge 9: Vasograde DCI Risk & Safety Black-Box', () => {
    const tool = getTool('calc_vasograde');

    it('validates Green (WFNS 1-2 + Fisher 0-2), Yellow (WFNS 1-3 + Fisher 3-4), and Red (WFNS 4-5)', () => {
      const green = calculateScore(tool, { grp_vasograde_category: 'opt_vaso_green' });
      expect(green.rawScore).toBe(1);
      expect(green.activeRiskTier.id).toBe('tier_vaso_green');

      const yellow = calculateScore(tool, { grp_vasograde_category: 'opt_vaso_yellow' });
      expect(yellow.rawScore).toBe(2);
      expect(yellow.activeRiskTier.id).toBe('tier_vaso_yellow');

      const red = calculateScore(tool, { grp_vasograde_category: 'opt_vaso_red' });
      expect(red.rawScore).toBe(3);
      expect(red.activeRiskTier.id).toBe('tier_vaso_red');
      expect(red.activeRiskTier.severityLevel).toBe('critical');
    });

    it('verifies dedicated bivariate resolver maps { wfns, modified_fisher } to correct risk tiers', () => {
      // 1. Critical risk: WFNS 5 + Modified Fisher 4 -> Vasograde-Red (3 pts)
      const redRes = calculateScore(tool, { wfns: 5, modified_fisher: 4 });
      expect(redRes.rawScore).toBe(3);
      expect(redRes.activeRiskTier.id).toBe('tier_vaso_red');
      expect(redRes.activeRiskTier.severityLevel).toBe('critical');

      // 2. Intermediate risk (Amber/Yellow): WFNS 2 + Modified Fisher 4
      const yellowRes1 = calculateScore(tool, { wfns: 2, modified_fisher: 4 });
      expect(yellowRes1.rawScore).toBe(2);
      expect(yellowRes1.activeRiskTier.id).toBe('tier_vaso_yellow');
      expect(yellowRes1.activeRiskTier.severityLevel).toBe('intermediate');

      // 3. Intermediate risk (Amber/Yellow): WFNS 3 + Modified Fisher 1
      const yellowRes2 = calculateScore(tool, { wfns: 3, modified_fisher: 1 });
      expect(yellowRes2.rawScore).toBe(2);
      expect(yellowRes2.activeRiskTier.id).toBe('tier_vaso_yellow');
      expect(yellowRes2.activeRiskTier.severityLevel).toBe('intermediate');

      // 4. Low risk: WFNS 1 + Modified Fisher 2 -> Vasograde-Green (1 pt)
      const greenRes = calculateScore(tool, { wfns: 1, modified_fisher: 2 });
      expect(greenRes.rawScore).toBe(1);
      expect(greenRes.activeRiskTier.id).toBe('tier_vaso_green');
      expect(greenRes.activeRiskTier.severityLevel).toBe('low');
    });
  });

  // ==========================================================================
  // 10. KIEFER SCALE & EVANS / DESH
  // ==========================================================================
  describe('Challenge 10: Kiefer HPN Scale & Evans / DESH Morphometrics', () => {
    const kiefer = getTool('calc_kiefer');
    const evans = getTool('calc_evans_desh');

    it('verifies Kiefer 0-24 points and Tap Test delta >= 2 criterion', () => {
      expect(kiefer.minPossibleScore).toBe(0);
      expect(kiefer.maxPossibleScore).toBe(24);

      const res0 = calculateScore(kiefer, {});
      expect(res0.rawScore).toBe(0);

      expect(kiefer.clinicalWarning).toContain('melhora de pelo menos 2 pontos na Escala de Kiefer');
      expect(kiefer.clinicalWarning).toContain('válvula regulável com mecanismo gravitacional ou anti-sifão');
    });

    it('verifies Evans >= 0.30 + DESH + acute angle yields >85-92% response vs Alzheimer ex-vacuo', () => {
      // Full typical DESH
      const resDesh = calculateScore(evans, {
        grp_evans_index: 'opt_evans_enlarged',
        grp_desh_pattern: 'opt_desh_classic',
        grp_callosal_angle: 'opt_angle_acute',
        grp_periventricular_edema: 'opt_edema_present'
      });
      expect(resDesh.rawScore).toBe(10);
      expect(resDesh.activeRiskTier.id).toBe('tier_ed_classic');
      expect(resDesh.activeRiskTier.statisticalOutcome).toContain('> 85% a 92%');

      // Ex-vacuo Alzheimer atrophy
      const resAtrophy = calculateScore(evans, {
        grp_evans_index: 'opt_evans_normal',
        grp_desh_pattern: 'opt_desh_none',
        grp_callosal_angle: 'opt_angle_wide',
        grp_periventricular_edema: 'opt_edema_absent'
      });
      expect(resAtrophy.rawScore).toBe(0);
      expect(resAtrophy.activeRiskTier.id).toBe('tier_ed_unlikely');
      expect(resAtrophy.activeRiskTier.statisticalOutcome).toContain('Taxa de resposta à DVP < 15-20%');
    });
  });
});

/**
 * Helper to construct PHASES inputs matching a target score s (0 to 22).
 */
function constructPhasesInputsForScore(target: number): Record<string, any> {
  const popOptions = [{ val: 5, p: 'finland' }, { val: 3, p: 'japan' }, { val: 0, p: 'other' }];
  const sizeOptions = [{ val: 10, s: 25.0 }, { val: 6, s: 15.0 }, { val: 3, s: 8.0 }, { val: 0, s: 5.0 }];
  const siteOptions = [{ val: 4, site: 'posterior' }, { val: 2, site: 'mca' }, { val: 0, site: 'ica' }];
  const htnOptions = [{ val: 1, htn: true }, { val: 0, htn: false }];
  const ageOptions = [{ val: 1, age: 75 }, { val: 0, age: 50 }];
  const sahOptions = [{ val: 1, sah: true }, { val: 0, sah: false }];

  for (const pop of popOptions) {
    for (const size of sizeOptions) {
      for (const site of siteOptions) {
        for (const htn of htnOptions) {
          for (const age of ageOptions) {
            for (const sah of sahOptions) {
              if (pop.val + size.val + site.val + htn.val + age.val + sah.val === target) {
                return {
                  population: pop.p,
                  size: size.s,
                  site: site.site,
                  hypertension: htn.htn,
                  age: age.age,
                  earlierSah: sah.sah
                };
              }
            }
          }
        }
      }
    }
  }
  throw new Error(`Unable to construct PHASES inputs for score ${target}`);
}
