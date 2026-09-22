import { describe, it, expect } from 'vitest';
import rawBlock03Data from '@/data/blocks/block_03.json';
import { calculateScore } from '@/engines/calculationEngine';
import { type Calculator, type BlockData } from '@/types/clinical';

const parsedBlock03: BlockData = rawBlock03Data as unknown as BlockData;

function getTool(id: string): Calculator {
  const tool = parsedBlock03.calculators.find((c) => c.id === id);
  if (!tool) throw new Error(`Calculator ${id} not found in Block 03`);
  return tool;
}

describe('Block 03 Neuro Calculation Engine Golden Tests', () => {
  // ==========================================================================
  // 1. ROTTERDAM CT SCORE (TCE)
  // ==========================================================================
  describe('1. Rotterdam CT Score (`calc_rotterdam`)', () => {
    const rotterdam = getTool('calc_rotterdam');

    it('calculates minimum score (1 point) with baseScore=1 and baseline options', () => {
      const result = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_normal', // 0
        grp_rotterdam_shift: 'opt_shift_le5',          // 0
        grp_rotterdam_hed: 'opt_hed_present',          // 0 (protective)
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_absent'    // 0
      });

      expect(result.rawScore).toBe(1);
      expect(result.scoreFormatted).toBe('1');
      expect(result.activeRiskTier.id).toBe('tier_rotterdam_low');
      expect(result.activeRiskTier.statisticalOutcome).toContain('0%');
    });

    it('calculates intermediate score (4 points) correctly adding parameters', () => {
      const result = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_compressed', // +1
        grp_rotterdam_shift: 'opt_shift_le5',              // 0
        grp_rotterdam_hed: 'opt_hed_absent',              // +1 (absence adds risk)
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_present'       // +1
      });

      // base 1 + 1 + 0 + 1 + 1 = 4 points
      expect(result.rawScore).toBe(4);
      expect(result.scoreFormatted).toBe('4');
      expect(result.activeRiskTier.id).toBe('tier_rotterdam_mod');
      expect(result.activeRiskTier.statisticalOutcome).toContain('26%');
    });

    it('calculates maximum score (6 points) with critical derangements', () => {
      const result = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_absent', // +2
        grp_rotterdam_shift: 'opt_shift_gt5',          // +1
        grp_rotterdam_hed: 'opt_hed_absent',          // +1
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_present'   // +1
      });

      // base 1 + 2 + 1 + 1 + 1 = 6 points
      expect(result.rawScore).toBe(6);
      expect(result.scoreFormatted).toBe('6');
      expect(result.activeRiskTier.id).toBe('tier_rotterdam_crit');
      expect(result.activeRiskTier.statisticalOutcome).toContain('61%');
    });
  });

  // ==========================================================================
  // 2. MARSHALL CT CLASSIFICATION (TCE)
  // ==========================================================================
  describe('2. Marshall CT Classification (`calc_marshall`)', () => {
    const marshall = getTool('calc_marshall');

    it('correctly maps diffuse injury categories I to IV and mass lesions V and VI', () => {
      // Marshall I: Sem patologia visível
      const m1 = calculateScore(marshall, { grp_marshall_cat: 'opt_marshall_1' });
      expect(m1.rawScore).toBe(1);
      expect(m1.activeRiskTier.id).toBe('tier_marshall_low');

      // Marshall II: Cisternas presentes, desvio <= 5mm
      const m2 = calculateScore(marshall, { grp_marshall_cat: 'opt_marshall_2' });
      expect(m2.rawScore).toBe(2);
      expect(m2.activeRiskTier.id).toBe('tier_marshall_low');

      // Marshall III: Cisternas comprimidas/ausentes (Swelling)
      const m3 = calculateScore(marshall, { grp_marshall_cat: 'opt_marshall_3' });
      expect(m3.rawScore).toBe(3);
      expect(m3.activeRiskTier.id).toBe('tier_marshall_mod');

      // Marshall IV: Desvio de linha média > 5mm (Shift) -> matches tier 3-5
      const m4 = calculateScore(marshall, { grp_marshall_cat: 'opt_marshall_4' });
      expect(m4.rawScore).toBe(4);
      expect(m4.activeRiskTier.id).toBe('tier_marshall_mod');

      // Marshall V: Massa cirurgicamente evacuada -> matches tier 3-5
      const m5 = calculateScore(marshall, { grp_marshall_cat: 'opt_marshall_5' });
      expect(m5.rawScore).toBe(5);
      expect(m5.activeRiskTier.id).toBe('tier_marshall_mod');

      // Marshall VI: Massa focal de alta/mista densidade > 25 mL não evacuada -> tier 4-6
      const m6 = calculateScore(marshall, { grp_marshall_cat: 'opt_marshall_6' });
      expect(m6.rawScore).toBe(6);
      expect(m6.activeRiskTier.id).toBe('tier_marshall_crit');
    });
  });

  // ==========================================================================
  // 3. HUNT-HESS SCALE (HSA)
  // ==========================================================================
  describe('3. Hunt-Hess Scale (`calc_hunt_hess`)', () => {
    const huntHess = getTool('calc_hunt_hess');

    it('calculates classical grade 1 without modifier', () => {
      const result = calculateScore(huntHess, {
        grp_hh_grade: 'opt_hh_1',
        grp_hh_modifier: 'opt_hh_mod_none'
      });
      expect(result.rawScore).toBe(1);
      expect(result.activeRiskTier.id).toBe('tier_hh_good');
      expect(result.activeRiskTier.statisticalOutcome).toContain('1%');
    });

    it('calculates grade 1a with fixed deficit and no acute meningismus', () => {
      const result = calculateScore(huntHess, {
        grp_hh_grade: 'opt_hh_1a',
        grp_hh_modifier: 'opt_hh_mod_none'
      });
      expect(result.rawScore).toBe(1);
      expect(result.activeRiskTier.id).toBe('tier_hh_good');
    });

    it('applies +1 comorbidity adjustment (grade 1 -> 2, grade 2 -> 3)', () => {
      // Grade 1 with comorbidity = 2
      const res1 = calculateScore(huntHess, {
        grp_hh_grade: 'opt_hh_1',
        grp_hh_modifier: 'opt_hh_mod_present'
      });
      expect(res1.rawScore).toBe(2);
      expect(res1.activeRiskTier.id).toBe('tier_hh_good');

      // Grade 2 with comorbidity = 3 (advances to intermediate tier)
      const res2 = calculateScore(huntHess, {
        grp_hh_grade: 'opt_hh_2',
        grp_hh_modifier: 'opt_hh_mod_present'
      });
      expect(res2.rawScore).toBe(3);
      expect(res2.activeRiskTier.id).toBe('tier_hh_mod');
    });

    it('calculates poor clinical grades 4 and 5', () => {
      const res4 = calculateScore(huntHess, {
        grp_hh_grade: 'opt_hh_4',
        grp_hh_modifier: 'opt_hh_mod_none'
      });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_hh_poor');

      const res5 = calculateScore(huntHess, {
        grp_hh_grade: 'opt_hh_5',
        grp_hh_modifier: 'opt_hh_mod_none'
      });
      expect(res5.rawScore).toBe(5);
      expect(res5.activeRiskTier.id).toBe('tier_hh_poor');
      expect(res5.activeRiskTier.statisticalOutcome).toContain('70% a 100%');
    });
  });

  // ==========================================================================
  // 4. WFNS SCALE (HSA)
  // ==========================================================================
  describe('4. WFNS Scale (`calc_wfns`)', () => {
    const wfns = getTool('calc_wfns');

    it('correctly discriminates grades based on GCS and focal deficit matrix', () => {
      // Grade I: GCS 15 sem déficit
      const g1 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_1' });
      expect(g1.rawScore).toBe(1);
      expect(g1.activeRiskTier.id).toBe('tier_wfns_low');

      // Grade II: GCS 13-14 sem déficit
      const g2 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_2' });
      expect(g2.rawScore).toBe(2);
      expect(g2.activeRiskTier.id).toBe('tier_wfns_low');

      // Grade III: GCS 13-14 COM déficit motor focal
      const g3 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_3' });
      expect(g3.rawScore).toBe(3);
      expect(g3.activeRiskTier.id).toBe('tier_wfns_mod');

      // Grade IV: GCS 7-12 com ou sem déficit
      const g4 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_4' });
      expect(g4.rawScore).toBe(4);
      expect(g4.activeRiskTier.id).toBe('tier_wfns_high');

      // Grade V: GCS 3-6 com ou sem déficit
      const g5 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_5' });
      expect(g5.rawScore).toBe(5);
      expect(g5.activeRiskTier.id).toBe('tier_wfns_high');
    });
  });

  // ==========================================================================
  // 5. FISHER CLASSIC SCALE (HSA)
  // ==========================================================================
  describe('5. Fisher Classic Scale (`calc_fisher_classic`)', () => {
    const fisherCl = getTool('calc_fisher_classic');

    it('evaluates grades 1 through 4 with blood thickness and non-linear vasospasm risk', () => {
      // Grade 1: Sem sangue visível
      const f1 = calculateScore(fisherCl, { grp_fisher_classic: 'opt_fc_1' });
      expect(f1.rawScore).toBe(1);
      expect(f1.activeRiskTier.id).toBe('tier_fc_low');

      // Grade 2: Sangue difuso fino < 1 mm
      const f2 = calculateScore(fisherCl, { grp_fisher_classic: 'opt_fc_2' });
      expect(f2.rawScore).toBe(2);
      expect(f2.activeRiskTier.id).toBe('tier_fc_low');

      // Grade 3: Coágulo espesso >= 1 mm (Risco CRÍTICO de vasoespasmo)
      const f3 = calculateScore(fisherCl, { grp_fisher_classic: 'opt_fc_3' });
      expect(f3.rawScore).toBe(3);
      expect(f3.activeRiskTier.id).toBe('tier_fc_crit');
      expect(f3.activeRiskTier.statisticalOutcome).toContain('60% a 80%');

      // Grade 4: Hematoma intraparenquimatoso ou hemoventrículo (paradoxo do menor risco)
      const f4 = calculateScore(fisherCl, { grp_fisher_classic: 'opt_fc_4' });
      expect(f4.rawScore).toBe(4);
      expect(f4.activeRiskTier.id).toBe('tier_fc_hydro');
    });
  });

  // ==========================================================================
  // 6. MODIFIED FISHER / CLAASSEN SCALE (HSA)
  // ==========================================================================
  describe('6. Modified Fisher / Claassen Scale (`calc_fisher_modified`)', () => {
    const fisherMod = getTool('calc_fisher_modified');

    it('evaluates 5 progressive ordinal grades (0 to 4) crossing cisternal blood with bilateral IVH', () => {
      // Grade 0: Sem sangue ou traço mínimo
      const fm0 = calculateScore(fisherMod, { grp_fisher_mod: 'opt_fm_0' });
      expect(fm0.rawScore).toBe(0);
      expect(fm0.activeRiskTier.id).toBe('tier_fm_low');

      // Grade 1: HSA fina sem HIV bilateral
      const fm1 = calculateScore(fisherMod, { grp_fisher_mod: 'opt_fm_1' });
      expect(fm1.rawScore).toBe(1);
      expect(fm1.activeRiskTier.id).toBe('tier_fm_low');

      // Grade 2: HSA fina com HIV bilateral
      const fm2 = calculateScore(fisherMod, { grp_fisher_mod: 'opt_fm_2' });
      expect(fm2.rawScore).toBe(2);
      expect(fm2.activeRiskTier.id).toBe('tier_fm_mod');

      // Grade 3: HSA espessa sem HIV bilateral
      const fm3 = calculateScore(fisherMod, { grp_fisher_mod: 'opt_fm_3' });
      expect(fm3.rawScore).toBe(3);
      expect(fm3.activeRiskTier.id).toBe('tier_fm_mod');

      // Grade 4: HSA espessa com HIV bilateral (Risco máximo de DCI)
      const fm4 = calculateScore(fisherMod, { grp_fisher_mod: 'opt_fm_4' });
      expect(fm4.rawScore).toBe(4);
      expect(fm4.activeRiskTier.id).toBe('tier_fm_crit');
      expect(fm4.activeRiskTier.statisticalOutcome).toContain('40% a 50%');
    });
  });

  // ==========================================================================
  // 7. SPETZLER-MARTIN GRADE (MAV)
  // ==========================================================================
  describe('7. Spetzler-Martin Grade (`calc_spetzler_martin`)', () => {
    const spetzler = getTool('calc_spetzler_martin');

    it('calculates Grade I (small, non-eloquent, superficial) -> 1 point', () => {
      const result = calculateScore(spetzler, {
        grp_sm_size: 'opt_sm_size_small',            // 1
        grp_sm_eloquence: 'opt_sm_eloq_no',          // 0
        grp_sm_drainage: 'opt_sm_drain_superficial'  // 0
      });
      expect(result.rawScore).toBe(1);
      expect(result.activeRiskTier.id).toBe('tier_sm_low');
      expect(result.activeRiskTier.label).toContain('Classe A');
    });

    it('calculates Grade III (small, eloquent, deep drainage) -> 3 points', () => {
      const result = calculateScore(spetzler, {
        grp_sm_size: 'opt_sm_size_small',            // 1
        grp_sm_eloquence: 'opt_sm_eloq_yes',         // 1
        grp_sm_drainage: 'opt_sm_drain_deep'         // 1
      });
      expect(result.rawScore).toBe(3);
      expect(result.activeRiskTier.id).toBe('tier_sm_mod');
      expect(result.activeRiskTier.label).toContain('Classe B');
    });

    it('calculates Grade V (large, eloquent, deep drainage) -> 5 points', () => {
      const result = calculateScore(spetzler, {
        grp_sm_size: 'opt_sm_size_large',            // 3
        grp_sm_eloquence: 'opt_sm_eloq_yes',         // 1
        grp_sm_drainage: 'opt_sm_drain_deep'         // 1
      });
      expect(result.rawScore).toBe(5);
      expect(result.activeRiskTier.id).toBe('tier_sm_high');
      expect(result.activeRiskTier.label).toContain('Classe C');
    });
  });

  // ==========================================================================
  // 8. NIHSS (STROKE SCALE)
  // ==========================================================================
  describe('8. NIHSS Stroke Scale (`calc_nihss`)', () => {
    const nihss = getTool('calc_nihss');

    it('calculates score 0 for completely intact neurological examination', () => {
      const result = calculateScore(nihss, {
        grp_nihss_1a: 'opt_nihss_1a_0',
        grp_nihss_1b: 'opt_nihss_1b_0',
        grp_nihss_1c: 'opt_nihss_1c_0',
        grp_nihss_2: 'opt_nihss_2_0',
        grp_nihss_3: 'opt_nihss_3_0',
        grp_nihss_4: 'opt_nihss_4_0',
        grp_nihss_5a: 'opt_nihss_5a_0',
        grp_nihss_5b: 'opt_nihss_5b_0',
        grp_nihss_6a: 'opt_nihss_6a_0',
        grp_nihss_6b: 'opt_nihss_6b_0',
        grp_nihss_7: 'opt_nihss_7_0',
        grp_nihss_8: 'opt_nihss_8_0',
        grp_nihss_9: 'opt_nihss_9_0',
        grp_nihss_10: 'opt_nihss_10_0',
        grp_nihss_11: 'opt_nihss_11_0'
      });

      expect(result.rawScore).toBe(0);
      expect(result.activeRiskTier.id).toBe('tier_nihss_zero');
    });

    it('calculates moderate stroke (5 to 15 points) and triggers thrombolysis/thrombectomy tier', () => {
      const result = calculateScore(nihss, {
        grp_nihss_1a: 'opt_nihss_1a_1', // 1 (sonolento)
        grp_nihss_1b: 'opt_nihss_1b_1', // 1 (erra 1 pergunta)
        grp_nihss_1c: 'opt_nihss_1c_0', // 0
        grp_nihss_2: 'opt_nihss_2_0',  // 0
        grp_nihss_3: 'opt_nihss_3_0',  // 0
        grp_nihss_4: 'opt_nihss_4_2',  // 2 (paresia facial moderada)
        grp_nihss_5a: 'opt_nihss_5a_3', // 3 (queda imediata MSE)
        grp_nihss_5b: 'opt_nihss_5b_0', // 0
        grp_nihss_6a: 'opt_nihss_6a_2', // 2 (esforço contra gravidade MIE)
        grp_nihss_6b: 'opt_nihss_6b_0', // 0
        grp_nihss_7: 'opt_nihss_7_0',  // 0
        grp_nihss_8: 'opt_nihss_8_1',  // 1 (hipoestesia leve)
        grp_nihss_9: 'opt_nihss_9_1',  // 1 (afasia leve)
        grp_nihss_10: 'opt_nihss_10_1', // 1 (disartria leve)
        grp_nihss_11: 'opt_nihss_11_0'  // 0
      });

      // 1+1+0+0+0+2+3+0+2+0+0+1+1+1+0 = 12 points
      expect(result.rawScore).toBe(12);
      expect(result.activeRiskTier.id).toBe('tier_nihss_mod');
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('handles untestable (UN) items properly without adding spurious score', () => {
      const result = calculateScore(nihss, {
        grp_nihss_1a: 'opt_nihss_1a_0',
        grp_nihss_1b: 'opt_nihss_1b_0',
        grp_nihss_1c: 'opt_nihss_1c_0',
        grp_nihss_2: 'opt_nihss_2_0',
        grp_nihss_3: 'opt_nihss_3_0',
        grp_nihss_4: 'opt_nihss_4_0',
        grp_nihss_5a: 'opt_nihss_5a_un', // UN (0 pts)
        grp_nihss_5b: 'opt_nihss_5b_un', // UN (0 pts)
        grp_nihss_6a: 'opt_nihss_6a_un', // UN (0 pts)
        grp_nihss_6b: 'opt_nihss_6b_un', // UN (0 pts)
        grp_nihss_7: 'opt_nihss_7_0',
        grp_nihss_8: 'opt_nihss_8_0',
        grp_nihss_9: 'opt_nihss_9_0',
        grp_nihss_10: 'opt_nihss_10_un', // UN (0 pts)
        grp_nihss_11: 'opt_nihss_11_0'
      });

      expect(result.rawScore).toBe(0);
      expect(result.activeRiskTier.id).toBe('tier_nihss_zero');
    });

    it('calculates severe stroke (42 points maximum derangement)', () => {
      const result = calculateScore(nihss, {
        grp_nihss_1a: 'opt_nihss_1a_3', // 3
        grp_nihss_1b: 'opt_nihss_1b_2', // 2
        grp_nihss_1c: 'opt_nihss_1c_2', // 2
        grp_nihss_2: 'opt_nihss_2_2',  // 2
        grp_nihss_3: 'opt_nihss_3_3',  // 3
        grp_nihss_4: 'opt_nihss_4_3',  // 3
        grp_nihss_5a: 'opt_nihss_5a_4', // 4
        grp_nihss_5b: 'opt_nihss_5b_4', // 4
        grp_nihss_6a: 'opt_nihss_6a_4', // 4
        grp_nihss_6b: 'opt_nihss_6b_4', // 4
        grp_nihss_7: 'opt_nihss_7_2',  // 2
        grp_nihss_8: 'opt_nihss_8_2',  // 2
        grp_nihss_9: 'opt_nihss_9_3',  // 3
        grp_nihss_10: 'opt_nihss_10_2', // 2
        grp_nihss_11: 'opt_nihss_11_2'  // 2
      });

      // Sum: 3+2+2+2+3+3+4+4+4+4+2+2+3+2+2 = 42 points
      expect(result.rawScore).toBe(42);
      expect(result.activeRiskTier.id).toBe('tier_nihss_severe');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
    });
  });

  // ==========================================================================
  // 9. ASPECTS (MCA STROKE)
  // ==========================================================================
  describe('9. ASPECTS Subtractive Logic (`calc_aspects`)', () => {
    const aspects = getTool('calc_aspects');

    it('starts at baseScore=10 and retains 10 points when all regions are normal', () => {
      const result = calculateScore(aspects, {
        grp_aspects_c: 'opt_aspects_c_normal',
        grp_aspects_l: 'opt_aspects_l_normal',
        grp_aspects_ic: 'opt_aspects_ic_normal',
        grp_aspects_i: 'opt_aspects_i_normal',
        grp_aspects_m1: 'opt_aspects_m1_normal',
        grp_aspects_m2: 'opt_aspects_m2_normal',
        grp_aspects_m3: 'opt_aspects_m3_normal',
        grp_aspects_m4: 'opt_aspects_m4_normal',
        grp_aspects_m5: 'opt_aspects_m5_normal',
        grp_aspects_m6: 'opt_aspects_m6_normal'
      });

      expect(result.rawScore).toBe(10);
      expect(result.activeRiskTier.id).toBe('tier_aspects_small_core');
      expect(result.activeRiskTier.statisticalOutcome).toContain('Independência funcional');
    });

    it('deducts 3 points for 3 affected MCA zones (10 - 3 = 7 points)', () => {
      const result = calculateScore(aspects, {
        grp_aspects_c: 'opt_aspects_c_affected',   // -1
        grp_aspects_l: 'opt_aspects_l_affected',   // -1
        grp_aspects_ic: 'opt_aspects_ic_affected', // -1
        grp_aspects_i: 'opt_aspects_i_normal',
        grp_aspects_m1: 'opt_aspects_m1_normal',
        grp_aspects_m2: 'opt_aspects_m2_normal',
        grp_aspects_m3: 'opt_aspects_m3_normal',
        grp_aspects_m4: 'opt_aspects_m4_normal',
        grp_aspects_m5: 'opt_aspects_m5_normal',
        grp_aspects_m6: 'opt_aspects_m6_normal'
      });

      expect(result.rawScore).toBe(7);
      expect(result.activeRiskTier.id).toBe('tier_aspects_moderate');
      expect(result.activeRiskTier.statisticalOutcome).toContain('recanalização mecânica');
    });

    it('deducts all 10 points when all regions are infarcted down to 0 points', () => {
      const result = calculateScore(aspects, {
        grp_aspects_c: 'opt_aspects_c_affected',
        grp_aspects_l: 'opt_aspects_l_affected',
        grp_aspects_ic: 'opt_aspects_ic_affected',
        grp_aspects_i: 'opt_aspects_i_affected',
        grp_aspects_m1: 'opt_aspects_m1_affected',
        grp_aspects_m2: 'opt_aspects_m2_affected',
        grp_aspects_m3: 'opt_aspects_m3_affected',
        grp_aspects_m4: 'opt_aspects_m4_affected',
        grp_aspects_m5: 'opt_aspects_m5_affected',
        grp_aspects_m6: 'opt_aspects_m6_affected'
      });

      expect(result.rawScore).toBe(0);
      expect(result.activeRiskTier.id).toBe('tier_aspects_large_core');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
    });
  });

  // ==========================================================================
  // 10. ICH SCORE (INTRACEREBRAL HEMORRHAGE)
  // ==========================================================================
  describe('10. ICH Score (`calc_ich_score`)', () => {
    const ich = getTool('calc_ich_score');

    it('calculates score 0 with 0% 30-day mortality', () => {
      const result = calculateScore(ich, {
        grp_ich_gcs: 'opt_ich_gcs_13_15',
        grp_ich_volume: 'opt_ich_vol_lt30',
        grp_ich_ivh: 'opt_ich_ivh_no',
        grp_ich_infratentorial: 'opt_ich_infra_no',
        grp_ich_age: 'opt_ich_age_lt80'
      });

      expect(result.rawScore).toBe(0);
      expect(result.activeRiskTier.id).toBe('tier_ich_0');
      expect(result.activeRiskTier.statisticalOutcome).toContain('0%');
    });

    it('calculates score 2 with 26% mortality', () => {
      const result = calculateScore(ich, {
        grp_ich_gcs: 'opt_ich_gcs_5_12',  // 1
        grp_ich_volume: 'opt_ich_vol_ge30', // 1
        grp_ich_ivh: 'opt_ich_ivh_no',     // 0
        grp_ich_infratentorial: 'opt_ich_infra_no', // 0
        grp_ich_age: 'opt_ich_age_lt80'    // 0
      });

      expect(result.rawScore).toBe(2);
      expect(result.activeRiskTier.id).toBe('tier_ich_2');
      expect(result.activeRiskTier.statisticalOutcome).toContain('26%');
    });

    it('calculates score 4 with 97% mortality', () => {
      const result = calculateScore(ich, {
        grp_ich_gcs: 'opt_ich_gcs_3_4',   // 2
        grp_ich_volume: 'opt_ich_vol_ge30', // 1
        grp_ich_ivh: 'opt_ich_ivh_yes',    // 1
        grp_ich_infratentorial: 'opt_ich_infra_no',
        grp_ich_age: 'opt_ich_age_lt80'
      });

      expect(result.rawScore).toBe(4);
      expect(result.activeRiskTier.id).toBe('tier_ich_4');
      expect(result.activeRiskTier.statisticalOutcome).toContain('97%');
    });

    it('calculates score 6 with 100% mortality', () => {
      const result = calculateScore(ich, {
        grp_ich_gcs: 'opt_ich_gcs_3_4',      // 2
        grp_ich_volume: 'opt_ich_vol_ge30',    // 1
        grp_ich_ivh: 'opt_ich_ivh_yes',       // 1
        grp_ich_infratentorial: 'opt_ich_infra_yes', // 1
        grp_ich_age: 'opt_ich_age_ge80'       // 1
      });

      expect(result.rawScore).toBe(6);
      expect(result.activeRiskTier.id).toBe('tier_ich_5_6');
      expect(result.activeRiskTier.statisticalOutcome).toContain('100%');
    });
  });

  // ==========================================================================
  // 11. ABCD2 SCORE (TIA RISK)
  // ==========================================================================
  describe('11. ABCD2 Score (`calc_abcd2`)', () => {
    const abcd2 = getTool('calc_abcd2');

    it('calculates low risk (0-3 points)', () => {
      const result = calculateScore(abcd2, {
        grp_abcd2_age: 'opt_abcd2_age_lt60',     // 0
        grp_abcd2_bp: 'opt_abcd2_bp_norm',       // 0
        grp_abcd2_clinical: 'opt_abcd2_clin_other', // 0
        grp_abcd2_duration: 'opt_abcd2_dur_lt10', // 0
        grp_abcd2_diabetes: 'opt_abcd2_dm_no'     // 0
      });

      expect(result.rawScore).toBe(0);
      expect(result.activeRiskTier.id).toBe('tier_abcd2_low');
      expect(result.activeRiskTier.statisticalOutcome).toContain('1,0%');
    });

    it('calculates moderate risk (4-5 points)', () => {
      const result = calculateScore(abcd2, {
        grp_abcd2_age: 'opt_abcd2_age_ge60',        // 1
        grp_abcd2_bp: 'opt_abcd2_bp_high',          // 1
        grp_abcd2_clinical: 'opt_abcd2_clin_speech', // 1
        grp_abcd2_duration: 'opt_abcd2_dur_10_59',  // 1
        grp_abcd2_diabetes: 'opt_abcd2_dm_no'       // 0
      });

      expect(result.rawScore).toBe(4);
      expect(result.activeRiskTier.id).toBe('tier_abcd2_mod');
      expect(result.activeRiskTier.statisticalOutcome).toContain('4,1%');
    });

    it('calculates high risk (6-7 points)', () => {
      const result = calculateScore(abcd2, {
        grp_abcd2_age: 'opt_abcd2_age_ge60',          // 1
        grp_abcd2_bp: 'opt_abcd2_bp_high',            // 1
        grp_abcd2_clinical: 'opt_abcd2_clin_weakness', // 2
        grp_abcd2_duration: 'opt_abcd2_dur_ge60',     // 2
        grp_abcd2_diabetes: 'opt_abcd2_dm_yes'        // 1
      });

      expect(result.rawScore).toBe(7);
      expect(result.activeRiskTier.id).toBe('tier_abcd2_high');
      expect(result.activeRiskTier.statisticalOutcome).toContain('8,1%');
    });
  });

  // ==========================================================================
  // 12. ASIA / AIS IMPAIRMENT SCALE
  // ==========================================================================
  describe('12. ASIA / AIS Impairment Scale (`calc_asia_ais`)', () => {
    const asia = getTool('calc_asia_ais');

    it('correctly maps completeness classification grades A to E', () => {
      const aisA = calculateScore(asia, { grp_asia_grade: 'opt_ais_a' });
      expect(aisA.rawScore).toBe(1);
      expect(aisA.activeRiskTier.id).toBe('tier_ais_a');

      const aisB = calculateScore(asia, { grp_asia_grade: 'opt_ais_b' });
      expect(aisB.rawScore).toBe(2);
      expect(aisB.activeRiskTier.id).toBe('tier_ais_b');

      const aisC = calculateScore(asia, { grp_asia_grade: 'opt_ais_c' });
      expect(aisC.rawScore).toBe(3);
      expect(aisC.activeRiskTier.id).toBe('tier_ais_c');

      const aisD = calculateScore(asia, { grp_asia_grade: 'opt_ais_d' });
      expect(aisD.rawScore).toBe(4);
      expect(aisD.activeRiskTier.id).toBe('tier_ais_d');

      const aisE = calculateScore(asia, { grp_asia_grade: 'opt_ais_e' });
      expect(aisE.rawScore).toBe(5);
      expect(aisE.activeRiskTier.id).toBe('tier_ais_e');
    });
  });

  // ==========================================================================
  // 13. MODIFIED RANKIN SCALE (mRS)
  // ==========================================================================
  describe('13. Modified Rankin Scale (`calc_mrs`)', () => {
    const mrs = getTool('calc_mrs');

    it('discriminates functional independence (mRS 0-2) from moderate dependence (mRS 3)', () => {
      const mrs0 = calculateScore(mrs, { grp_mrs_grade: 'opt_mrs_0' });
      expect(mrs0.rawScore).toBe(0);
      expect(mrs0.activeRiskTier.id).toBe('tier_mrs_good');

      const mrs2 = calculateScore(mrs, { grp_mrs_grade: 'opt_mrs_2' });
      expect(mrs2.rawScore).toBe(2);
      expect(mrs2.activeRiskTier.id).toBe('tier_mrs_good');

      // Crucial independence boundary: mRS 3 requires assistance with daily activities
      const mrs3 = calculateScore(mrs, { grp_mrs_grade: 'opt_mrs_3' });
      expect(mrs3.rawScore).toBe(3);
      expect(mrs3.activeRiskTier.id).toBe('tier_mrs_mod');

      const mrs6 = calculateScore(mrs, { grp_mrs_grade: 'opt_mrs_6' });
      expect(mrs6.rawScore).toBe(6);
      expect(mrs6.activeRiskTier.id).toBe('tier_mrs_death');
    });
  });

  // ==========================================================================
  // 14. KARNOFSKY PERFORMANCE STATUS (KPS)
  // ==========================================================================
  describe('14. Karnofsky Performance Status (`calc_kps`)', () => {
    const kps = getTool('calc_kps');

    it('correctly maps 10% steps and validates the 70% therapeutic threshold', () => {
      const kps100 = calculateScore(kps, { grp_kps_level: 'opt_kps_100' });
      expect(kps100.rawScore).toBe(100);
      expect(kps100.activeRiskTier.id).toBe('tier_kps_high');

      // Critical 70% threshold: independent self-care cut-off
      const kps70 = calculateScore(kps, { grp_kps_level: 'opt_kps_70' });
      expect(kps70.rawScore).toBe(70);
      expect(kps70.activeRiskTier.id).toBe('tier_kps_int');

      const kps50 = calculateScore(kps, { grp_kps_level: 'opt_kps_50' });
      expect(kps50.rawScore).toBe(50);
      expect(kps50.activeRiskTier.id).toBe('tier_kps_low');

      const kps0 = calculateScore(kps, { grp_kps_level: 'opt_kps_0' });
      expect(kps0.rawScore).toBe(0);
      expect(kps0.activeRiskTier.id).toBe('tier_kps_death');
    });
  });

  // ==========================================================================
  // 15. MEEM / MMSE
  // ==========================================================================
  describe('15. MEEM / MMSE Cognitive Screening (`calc_meem_mmse`)', () => {
    const meem = getTool('calc_meem_mmse');

    it('calculates full 30-point examination for cognitive intactness', () => {
      const result = calculateScore(meem, {
        grp_meem_time: 'opt_meem_time_5',     // 5
        grp_meem_space: 'opt_meem_space_5',   // 5
        grp_meem_reg: 'opt_meem_reg_3',       // 3
        grp_meem_calc: 'opt_meem_calc_5',     // 5
        grp_meem_recall: 'opt_meem_recall_3', // 3
        grp_meem_naming: 'opt_meem_naming_2', // 2
        grp_meem_repeat: 'opt_meem_rep_1',    // 1
        grp_meem_command: 'opt_meem_cmd_3',   // 3
        grp_meem_read: 'opt_meem_read_1',     // 1
        grp_meem_write: 'opt_meem_write_1',   // 1
        grp_meem_praxia: 'opt_meem_praxia_1'  // 1
      });

      // Sum: 5+5+3+5+3+2+1+3+1+1+1 = 30 points
      expect(result.rawScore).toBe(30);
      expect(result.activeRiskTier.id).toBe('tier_meem_normal');
    });

    it('matches Brazilian schooling cutoffs (e.g. 22 points in low-schooling decline tier)', () => {
      const result = calculateScore(meem, {
        grp_meem_time: 'opt_meem_time_3',     // 3
        grp_meem_space: 'opt_meem_space_3',   // 3
        grp_meem_reg: 'opt_meem_reg_3',       // 3
        grp_meem_calc: 'opt_meem_calc_3',     // 3
        grp_meem_recall: 'opt_meem_recall_1', // 1
        grp_meem_naming: 'opt_meem_naming_2', // 2
        grp_meem_repeat: 'opt_meem_rep_1',    // 1
        grp_meem_command: 'opt_meem_cmd_3',   // 3
        grp_meem_read: 'opt_meem_read_1',     // 1
        grp_meem_write: 'opt_meem_write_1',   // 1
        grp_meem_praxia: 'opt_meem_praxia_1'  // 1
      });

      // Sum: 3+3+3+3+1+2+1+3+1+1+1 = 22 points
      expect(result.rawScore).toBe(22);
      expect(result.activeRiskTier.id).toBe('tier_meem_mild_decline');
    });
  });

  // ==========================================================================
  // 16. MoCA (MONTREAL COGNITIVE ASSESSMENT)
  // ==========================================================================
  describe('16. MoCA with Education Adjustment (`calc_moca`)', () => {
    const moca = getTool('calc_moca');

    it('crosses >= 26 threshold with +1 point education correction for <= 12 years study', () => {
      // Base score 25 points + 1 education bonus = 26 points (Normal tier)
      const withCorrection = calculateScore(moca, {
        grp_moca_visuo: 'opt_moca_visuo_4',       // 4
        grp_moca_naming: 'opt_moca_name_3',      // 3
        grp_moca_attention: 'opt_moca_att_5',   // 5
        grp_moca_lang: 'opt_moca_lang_3',        // 3
        grp_moca_abstract: 'opt_moca_abs_2',     // 2
        grp_moca_delayed_recall: 'opt_moca_rec_3', // 3
        grp_moca_orient: 'opt_moca_ori_5',       // 5
        grp_moca_edu_adj: 'opt_moca_edu_le12'    // +1 bonus
      });

      // 4+3+5+3+2+3+5 + 1 = 26 points
      expect(withCorrection.rawScore).toBe(26);
      expect(withCorrection.activeRiskTier.id).toBe('tier_moca_normal');

      // Same performance without education bonus (>12 years study) = 25 points (MCI tier)
      const withoutCorrection = calculateScore(moca, {
        grp_moca_visuo: 'opt_moca_visuo_4',       // 4
        grp_moca_naming: 'opt_moca_name_3',      // 3
        grp_moca_attention: 'opt_moca_att_5',   // 5
        grp_moca_lang: 'opt_moca_lang_3',        // 3
        grp_moca_abstract: 'opt_moca_abs_2',     // 2
        grp_moca_delayed_recall: 'opt_moca_rec_3', // 3
        grp_moca_orient: 'opt_moca_ori_5',       // 5
        grp_moca_edu_adj: 'opt_moca_edu_gt12'    // 0 bonus
      });

      expect(withoutCorrection.rawScore).toBe(25);
      expect(withoutCorrection.activeRiskTier.id).toBe('tier_moca_mci');
    });
  });

  // ==========================================================================
  // 17. HOEHN & YAHR (PARKINSON)
  // ==========================================================================
  describe('17. Hoehn & Yahr Staging (`calc_hoehn_yahr`)', () => {
    const hy = getTool('calc_hoehn_yahr');

    it('evaluates stages 0 through 5 and isolates the pull test discriminator at Stage 3', () => {
      // Stage 2.5: Bilateral disease with recovery on pull test
      const s25 = calculateScore(hy, { grp_hy_stage: 'opt_hy_2_5' });
      expect(s25.rawScore).toBe(2.5);
      expect(s25.activeRiskTier.id).toBe('tier_hy_early');

      // Stage 3: Postural instability / falls on pull test (Watershed for advanced therapy)
      const s3 = calculateScore(hy, { grp_hy_stage: 'opt_hy_3' });
      expect(s3.rawScore).toBe(3);
      expect(s3.activeRiskTier.id).toBe('tier_hy_mod');

      // Stage 5: Wheelchair/bedbound
      const s5 = calculateScore(hy, { grp_hy_stage: 'opt_hy_5' });
      expect(s5.rawScore).toBe(5);
      expect(s5.activeRiskTier.id).toBe('tier_hy_advanced');
    });
  });

  // ==========================================================================
  // 18. EDSS (KURTZKE EXPANDED DISABILITY STATUS SCALE)
  // ==========================================================================
  describe('18. EDSS Kurtzke Disability Scale (`calc_edss`)', () => {
    const edss = getTool('calc_edss');

    it('evaluates steps 0.0 to 10.0 and ambulation distance cutoffs', () => {
      // EDSS 0.0: Normal examination
      const e0 = calculateScore(edss, { grp_edss_level: 'opt_edss_0_0' });
      expect(e0.rawScore).toBe(0.0);
      expect(e0.activeRiskTier.id).toBe('tier_edss_ambulatory');

      // EDSS 4.0: Fully ambulatory without aid >= 500m
      const e4 = calculateScore(edss, { grp_edss_level: 'opt_edss_4_0' });
      expect(e4.rawScore).toBe(4.0);
      expect(e4.activeRiskTier.id).toBe('tier_edss_ambulatory');

      // EDSS 5.0: Ambulatory without aid ~200m (Gait aid transition threshold)
      const e5 = calculateScore(edss, { grp_edss_level: 'opt_edss_5_0' });
      expect(e5.rawScore).toBe(5.0);
      expect(e5.activeRiskTier.id).toBe('tier_edss_gait_aid');

      // EDSS 6.0: Unilateral assistance required
      const e6 = calculateScore(edss, { grp_edss_level: 'opt_edss_6_0' });
      expect(e6.rawScore).toBe(6.0);
      expect(e6.activeRiskTier.id).toBe('tier_edss_gait_aid');

      // EDSS 7.0: Restricted to wheelchair / walking <= 5m
      const e7 = calculateScore(edss, { grp_edss_level: 'opt_edss_7_0' });
      expect(e7.rawScore).toBe(7.0);
      expect(e7.activeRiskTier.id).toBe('tier_edss_wheelchair_bed');

      // EDSS 10.0: Death due to MS complications
      const e10 = calculateScore(edss, { grp_edss_level: 'opt_edss_10_0' });
      expect(e10.rawScore).toBe(10.0);
      expect(e10.activeRiskTier.id).toBe('tier_edss_death');
    });
  });
});
