/**
 * EMPIRICAL ADVERSARIAL STRESS TEST SUITE — CHALLENGER 1
 * Target: Block 03 (Neurology, Neurosurgery & Neurotrauma)
 *
 * Focus Areas:
 * 1. ASPECTS Subtractive Scoring (base 10 - affected zones, clamping, permutations)
 * 2. Rotterdam CT Trauma Offset Logic (baseScore 1, min 1, max 6, Epidural Hematoma paradox)
 * 3. NIHSS Complete Combinatorial Sweep & Untestable (UN) Parameter Defense
 * 4. ICH Score Extreme Boundary Verification & Exhaustive 48-State Grid
 * 5. Neurotrauma, Vascular & Functional Scales Stress Harness (Marshall, Hunt-Hess, WFNS, Fisher Classic/Mod, ASIA/AIS, EDSS, MEEM, MoCA)
 * 6. Universal Malformed, Negative Offset & Fuzzing Resilience (all 18 Block 03 tools)
 */

import { describe, it, expect } from 'vitest';
import rawBlock03Data from '../../src/data/blocks/block_03.json';
import { calculateScore } from '../../src/engines/calculationEngine';
import { type Calculator, type BlockData } from '../../src/types/clinical';

const parsedBlock03: BlockData = rawBlock03Data as unknown as BlockData;

function getTool(id: string): Calculator {
  const tool = parsedBlock03.calculators.find((c) => c.id === id);
  if (!tool) throw new Error(`Calculator ${id} not found in Block 03`);
  return tool;
}

describe('CHALLENGER 1: Adversarial Neuro Calculations Stress Verifier', () => {

  // ==========================================================================
  // DIMENSION 1: ASPECTS SUBTRACTIVE LOGIC & CLAMPING STRESS
  // ==========================================================================
  describe('Dimension 1: ASPECTS Subtractive Logic (`calc_aspects`)', () => {
    const aspects = getTool('calc_aspects');

    it('verifies baseScore property is explicitly defined as 10', () => {
      expect(aspects.baseScore).toBe(10);
      expect(aspects.minPossibleScore).toBe(0);
      expect(aspects.maxPossibleScore).toBe(10);
      expect(aspects.parameterGroups.length).toBe(10);
    });

    it('boundary: 0 zones affected yields exact score of 10 and small core tier', () => {
      // All 10 MCA zones normal (0 points deducted)
      const inputs: Record<string, string> = {};
      for (const group of aspects.parameterGroups) {
        inputs[group.id] = group.options.find((o) => o.pointValue === 0)!.id;
      }

      const res = calculateScore(aspects, inputs);
      expect(res.rawScore).toBe(10);
      expect(res.scoreFormatted).toBe('10');
      expect(res.activeRiskTier.id).toBe('tier_aspects_small_core');
      expect(res.radarValues['axis_aspects_deep']).toBe(0);
      expect(res.radarValues['axis_aspects_cortex_inf']).toBe(0);
      expect(res.radarValues['axis_aspects_cortex_sup']).toBe(0);
    });

    it('boundary: all 10 zones affected yields exact score of 0 and large core tier', () => {
      // All 10 MCA zones affected (-1 point each)
      const inputs: Record<string, string> = {};
      for (const group of aspects.parameterGroups) {
        inputs[group.id] = group.options.find((o) => o.pointValue === -1)!.id;
      }

      const res = calculateScore(aspects, inputs);
      expect(res.rawScore).toBe(0);
      expect(res.scoreFormatted).toBe('0');
      expect(res.activeRiskTier.id).toBe('tier_aspects_large_core');
      expect(res.radarValues['axis_aspects_deep']).toBe(1);
      expect(res.radarValues['axis_aspects_cortex_inf']).toBe(1);
      expect(res.radarValues['axis_aspects_cortex_sup']).toBe(1);
    });

    it('evaluates all intermediate scores from 1 to 9 zones affected monotonically', () => {
      const allGroups = aspects.parameterGroups;

      for (let numAffected = 1; numAffected <= 9; numAffected++) {
        const inputs: Record<string, string> = {};
        for (let i = 0; i < allGroups.length; i++) {
          const group = allGroups[i];
          const shouldAffect = i < numAffected;
          inputs[group.id] = shouldAffect
            ? group.options.find((o) => o.pointValue === -1)!.id
            : group.options.find((o) => o.pointValue === 0)!.id;
        }

        const res = calculateScore(aspects, inputs);
        const expectedScore = 10 - numAffected;
        expect(res.rawScore).toBe(expectedScore);

        if (expectedScore >= 8) {
          expect(res.activeRiskTier.id).toBe('tier_aspects_small_core');
        } else if (expectedScore >= 6) {
          expect(res.activeRiskTier.id).toBe('tier_aspects_moderate');
        } else {
          expect(res.activeRiskTier.id).toBe('tier_aspects_large_core');
        }
      }
    });

    it('boundary: empty input `{}` defaults cleanly to 10 points (0 zones affected)', () => {
      const res = calculateScore(aspects, {});
      expect(res.rawScore).toBe(10);
      expect(res.activeRiskTier.id).toBe('tier_aspects_small_core');
    });

    it('clamping: adversarial negative baseScore cannot reduce score below 0', () => {
      const modifiedAspects = { ...aspects, baseScore: -10 };
      const res = calculateScore(modifiedAspects, {});
      expect(res.rawScore).toBe(0);
      expect(res.score).toBe(0);
      expect(res.activeRiskTier.id).toBe('tier_aspects_large_core');
    });

    it('clamping: adversarial excessive baseScore cannot exceed 10', () => {
      const modifiedAspects = { ...aspects, baseScore: 50 };
      const res = calculateScore(modifiedAspects, {});
      expect(res.rawScore).toBe(10);
      expect(res.score).toBe(10);
      expect(res.activeRiskTier.id).toBe('tier_aspects_small_core');
    });

    it('handles direct numeric -1 selection correctly', () => {
      // In ASPECTS, option pointValue is -1. Passing -1 directly matches the option
      const res = calculateScore(aspects, {
        grp_aspects_c: -1,
        grp_aspects_l: -1,
      });
      // 10 - 2 = 8
      expect(res.rawScore).toBe(8);
      expect(res.activeRiskTier.id).toBe('tier_aspects_small_core');
    });

    it('handles option ID boolean flags correctly (e.g. `{ opt_aspects_m1_affected: true }`)', () => {
      const res = calculateScore(aspects, {
        opt_aspects_m1_affected: true,
        opt_aspects_m2_affected: true,
      });
      // 10 - 2 = 8
      expect(res.rawScore).toBe(8);
      expect(res.activeRiskTier.id).toBe('tier_aspects_small_core');
    });
  });

  // ==========================================================================
  // DIMENSION 2: ROTTERDAM OFFSET LOGIC & EPIDURAL HEMATOMA PARADOX
  // ==========================================================================
  describe('Dimension 2: Rotterdam CT Trauma Offset Logic (`calc_rotterdam`)', () => {
    const rotterdam = getTool('calc_rotterdam');

    it('verifies baseScore property is explicitly defined as 1 with bounds [1, 6]', () => {
      expect(rotterdam.baseScore).toBe(1);
      expect(rotterdam.minPossibleScore).toBe(1);
      expect(rotterdam.maxPossibleScore).toBe(6);
      expect(rotterdam.parameterGroups.length).toBe(4);
    });

    it('boundary: minimum score is strictly 1 point with baseScore=1 and baseline HED present', () => {
      const res = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_normal', // 0
        grp_rotterdam_shift: 'opt_shift_le5',          // 0
        grp_rotterdam_hed: 'opt_hed_present',          // 0 (protective)
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_absent',   // 0
      });

      expect(res.rawScore).toBe(1);
      expect(res.scoreFormatted).toBe('1');
      expect(res.activeRiskTier.id).toBe('tier_rotterdam_low');
      expect(res.activeRiskTier.statisticalOutcome).toContain('0%');
    });

    it('boundary: maximum score is strictly 6 points with critical parameters', () => {
      const res = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_absent', // +2
        grp_rotterdam_shift: 'opt_shift_gt5',          // +1
        grp_rotterdam_hed: 'opt_hed_absent',          // +1
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_present',  // +1
      });

      // base 1 + 2 + 1 + 1 + 1 = 6
      expect(res.rawScore).toBe(6);
      expect(res.scoreFormatted).toBe('6');
      expect(res.activeRiskTier.id).toBe('tier_rotterdam_crit');
      expect(res.activeRiskTier.statisticalOutcome).toContain('61%');
    });

    it('rigorously tests the Epidural Hematoma Paradox across all 12 CT sub-states', () => {
      // In Rotterdam, absence of epidural hematoma (+1) is worse than presence of HED (0).
      // For ANY permutation of (cisterns, shift, sah_ivh), score(HED absent) MUST EQUAL score(HED present) + 1.
      const cisternOptions = ['opt_cisterns_normal', 'opt_cisterns_compressed', 'opt_cisterns_absent'];
      const shiftOptions = ['opt_shift_le5', 'opt_shift_gt5'];
      const sahOptions = ['opt_sah_ivh_absent', 'opt_sah_ivh_present'];

      let comparisonCount = 0;
      for (const cistern of cisternOptions) {
        for (const shift of shiftOptions) {
          for (const sah of sahOptions) {
            const scoreWithHedPresent = calculateScore(rotterdam, {
              grp_rotterdam_cisterns: cistern,
              grp_rotterdam_shift: shift,
              grp_rotterdam_hed: 'opt_hed_present', // 0
              grp_rotterdam_sah_ivh: sah,
            }).rawScore;

            const scoreWithHedAbsent = calculateScore(rotterdam, {
              grp_rotterdam_cisterns: cistern,
              grp_rotterdam_shift: shift,
              grp_rotterdam_hed: 'opt_hed_absent', // +1
              grp_rotterdam_sah_ivh: sah,
            }).rawScore;

            expect(scoreWithHedAbsent).toBe(scoreWithHedPresent + 1);
            expect(scoreWithHedPresent).toBeGreaterThanOrEqual(1);
            expect(scoreWithHedAbsent).toBeLessThanOrEqual(6);
            comparisonCount++;
          }
        }
      }
      expect(comparisonCount).toBe(12);
    });

    it('boundary: empty input `{}` defaults safely to 2 points without error', () => {
      // cisterns=normal (0), shift=<=5 (0), hed=absent (1 baseline), sah=absent (0) -> base 1 + 1 = 2
      const res = calculateScore(rotterdam, {});
      expect(res.rawScore).toBe(2);
      expect(res.activeRiskTier.id).toBe('tier_rotterdam_low');
    });

    it('clamping: negative baseScore injection cannot pull Rotterdam score below 1', () => {
      const modifiedRotterdam = { ...rotterdam, baseScore: -10 };
      const res = calculateScore(modifiedRotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_normal',
        grp_rotterdam_shift: 'opt_shift_le5',
        grp_rotterdam_hed: 'opt_hed_present',
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_absent',
      });
      expect(res.rawScore).toBe(1);
      expect(res.activeRiskTier.id).toBe('tier_rotterdam_low');
    });

    it('clamping: excessive baseScore injection cannot push Rotterdam score above 6', () => {
      const modifiedRotterdam = { ...rotterdam, baseScore: 20 };
      const res = calculateScore(modifiedRotterdam, {});
      expect(res.rawScore).toBe(6);
      expect(res.activeRiskTier.id).toBe('tier_rotterdam_crit');
    });
  });

  // ==========================================================================
  // DIMENSION 3: NIHSS 15-ITEM COMBINATIONS & UNTESTABLE (UN) RESILIENCE
  // ==========================================================================
  describe('Dimension 3: NIHSS Combinations & Untestable (UN) Handling (`calc_nihss`)', () => {
    const nihss = getTool('calc_nihss');

    it('verifies NIHSS has exactly 15 parameter groups summing to maximum 42 points', () => {
      expect(nihss.parameterGroups.length).toBe(15);
      expect(nihss.minPossibleScore).toBe(0);
      expect(nihss.maxPossibleScore).toBe(42);
      expect(nihss.baseScore).toBe(0);
    });

    it('boundary: minimum score is 0 with all items normal', () => {
      const inputs: Record<string, string> = {};
      for (const group of nihss.parameterGroups) {
        inputs[group.id] = group.options.find((o) => o.pointValue === 0 && o.isNormalBaseline)!.id;
      }

      const res = calculateScore(nihss, inputs);
      expect(res.rawScore).toBe(0);
      expect(res.scoreFormatted).toBe('0');
      expect(res.activeRiskTier.id).toBe('tier_nihss_zero');
    });

    it('boundary: maximum score is exactly 42 points with maximum impairment across all items', () => {
      const inputs: Record<string, string> = {
        grp_nihss_1a: 'opt_nihss_1a_3', // 3
        grp_nihss_1b: 'opt_nihss_1b_2', // 2
        grp_nihss_1c: 'opt_nihss_1c_2', // 2
        grp_nihss_2: 'opt_nihss_2_2',   // 2
        grp_nihss_3: 'opt_nihss_3_3',   // 3
        grp_nihss_4: 'opt_nihss_4_3',   // 3
        grp_nihss_5a: 'opt_nihss_5a_4', // 4
        grp_nihss_5b: 'opt_nihss_5b_4', // 4
        grp_nihss_6a: 'opt_nihss_6a_4', // 4
        grp_nihss_6b: 'opt_nihss_6b_4', // 4
        grp_nihss_7: 'opt_nihss_7_2',   // 2
        grp_nihss_8: 'opt_nihss_8_2',   // 2
        grp_nihss_9: 'opt_nihss_9_3',   // 3
        grp_nihss_10: 'opt_nihss_10_2', // 2
        grp_nihss_11: 'opt_nihss_11_2', // 2
      };

      // Sum: 3 + 2 + 2 + 2 + 3 + 3 + 4 + 4 + 4 + 4 + 2 + 2 + 3 + 2 + 2 = 42
      const res = calculateScore(nihss, inputs);
      expect(res.rawScore).toBe(42);
      expect(res.scoreFormatted).toBe('42');
      expect(res.activeRiskTier.id).toBe('tier_nihss_severe');
    });

    it('untestable (UN) items add exactly 0 points and do not derange radar normalization', () => {
      const unItems = [
        { groupId: 'grp_nihss_5a', optionId: 'opt_nihss_5a_un' },
        { groupId: 'grp_nihss_5b', optionId: 'opt_nihss_5b_un' },
        { groupId: 'grp_nihss_6a', optionId: 'opt_nihss_6a_un' },
        { groupId: 'grp_nihss_6b', optionId: 'opt_nihss_6b_un' },
        { groupId: 'grp_nihss_10', optionId: 'opt_nihss_10_un' },
      ];

      for (const item of unItems) {
        const group = nihss.parameterGroups.find((g) => g.id === item.groupId)!;
        const opt = group.options.find((o) => o.id === item.optionId)!;
        expect(opt).toBeDefined();
        expect(opt.pointValue).toBe(0);
        expect(opt.radarNormalizedValue).toBe(0.0);
      }
    });

    it('stress: patient with 4 amputated limbs and severe intubation untestable scores 0 if otherwise normal', () => {
      const inputs: Record<string, string> = {
        grp_nihss_5a: 'opt_nihss_5a_un', // 0
        grp_nihss_5b: 'opt_nihss_5b_un', // 0
        grp_nihss_6a: 'opt_nihss_6a_un', // 0
        grp_nihss_6b: 'opt_nihss_6b_un', // 0
        grp_nihss_10: 'opt_nihss_10_un', // 0
      };

      const res = calculateScore(nihss, inputs);
      expect(res.rawScore).toBe(0);
      expect(res.activeRiskTier.id).toBe('tier_nihss_zero');
    });

    it('stress: patient with all 5 UN items but maximum impairment elsewhere scores exactly 24 points (42 - 18)', () => {
      const inputs: Record<string, string> = {
        grp_nihss_1a: 'opt_nihss_1a_3', // 3
        grp_nihss_1b: 'opt_nihss_1b_2', // 2
        grp_nihss_1c: 'opt_nihss_1c_2', // 2
        grp_nihss_2: 'opt_nihss_2_2',   // 2
        grp_nihss_3: 'opt_nihss_3_3',   // 3
        grp_nihss_4: 'opt_nihss_4_3',   // 3
        grp_nihss_5a: 'opt_nihss_5a_un', // 0 (untestable instead of 4)
        grp_nihss_5b: 'opt_nihss_5b_un', // 0 (untestable instead of 4)
        grp_nihss_6a: 'opt_nihss_6a_un', // 0 (untestable instead of 4)
        grp_nihss_6b: 'opt_nihss_6b_un', // 0 (untestable instead of 4)
        grp_nihss_7: 'opt_nihss_7_2',   // 2
        grp_nihss_8: 'opt_nihss_8_2',   // 2
        grp_nihss_9: 'opt_nihss_9_3',   // 3
        grp_nihss_10: 'opt_nihss_10_un', // 0 (untestable instead of 2)
        grp_nihss_11: 'opt_nihss_11_2', // 2
      };

      // 42 - (4 + 4 + 4 + 4 + 2) = 42 - 18 = 24
      const res = calculateScore(nihss, inputs);
      expect(res.rawScore).toBe(24);
      expect(res.activeRiskTier.id).toBe('tier_nihss_severe');
    });

    it('discriminates clinical thresholds: minor stroke (<=4), LVO trigger (>=6), and severe (>=21)', () => {
      // Score 4: minor stroke
      const minor = calculateScore(nihss, { grp_nihss_5a: 'opt_nihss_5a_4' });
      expect(minor.rawScore).toBe(4);
      expect(minor.activeRiskTier.id).toBe('tier_nihss_minor');

      // Score 6: moderate stroke with LVO suspicion
      const lvo = calculateScore(nihss, {
        grp_nihss_5a: 'opt_nihss_5a_4', // 4
        grp_nihss_2: 'opt_nihss_2_2',   // 2
      });
      expect(lvo.rawScore).toBe(6);
      expect(lvo.activeRiskTier.id).toBe('tier_nihss_mod');

      // Score 21: severe stroke
      const severe = calculateScore(nihss, {
        grp_nihss_1a: 'opt_nihss_1a_3', // 3
        grp_nihss_5a: 'opt_nihss_5a_4', // 4
        grp_nihss_5b: 'opt_nihss_5b_4', // 4
        grp_nihss_6a: 'opt_nihss_6a_4', // 4
        grp_nihss_6b: 'opt_nihss_6b_4', // 4
        grp_nihss_9: 'opt_nihss_9_2',   // 2
      });
      expect(severe.rawScore).toBe(21);
      expect(severe.activeRiskTier.id).toBe('tier_nihss_severe');
    });

    it('asserts mandatory acute stroke blood pressure warning is present', () => {
      const res = calculateScore(nihss, {});
      expect(res.clinicalWarning).toContain('185/110 mmHg');
      expect(res.clinicalWarning).toContain('180/105 mmHg');
      expect(res.clinicalWarning).toContain('Trombectomia Mecânica');
    });
  });

  // ==========================================================================
  // DIMENSION 4: ICH SCORE BOUNDARIES & EXHAUSTIVE 48-STATE COMBINATORIAL GRID
  // ==========================================================================
  describe('Dimension 4: ICH Score Boundaries & Combinatorial Grid (`calc_ich_score`)', () => {
    const ich = getTool('calc_ich_score');

    it('verifies ICH Score configuration bounds [0, 6]', () => {
      expect(ich.baseScore).toBe(0);
      expect(ich.minPossibleScore).toBe(0);
      expect(ich.maxPossibleScore).toBe(6);
      expect(ich.parameterGroups.length).toBe(5);
    });

    it('boundary: extreme case (age>=80, vol>=30, IVH, infratentorial, GCS 3-4) scores 6 and 100% mortality', () => {
      const res = calculateScore(ich, {
        grp_ich_gcs: 'opt_ich_gcs_3_4',         // 2
        grp_ich_volume: 'opt_ich_vol_ge30',      // 1
        grp_ich_ivh: 'opt_ich_ivh_yes',          // 1
        grp_ich_infratentorial: 'opt_ich_infra_yes', // 1
        grp_ich_age: 'opt_ich_age_ge80',         // 1
      });

      // 2 + 1 + 1 + 1 + 1 = 6
      expect(res.rawScore).toBe(6);
      expect(res.scoreFormatted).toBe('6');
      expect(res.activeRiskTier.id).toBe('tier_ich_5_6');
      expect(res.activeRiskTier.statisticalOutcome).toContain('100%');
    });

    it('boundary: minimum case scores 0 and 0% mortality', () => {
      const res = calculateScore(ich, {
        grp_ich_gcs: 'opt_ich_gcs_13_15',
        grp_ich_volume: 'opt_ich_vol_lt30',
        grp_ich_ivh: 'opt_ich_ivh_no',
        grp_ich_infratentorial: 'opt_ich_infra_no',
        grp_ich_age: 'opt_ich_age_lt80',
      });

      expect(res.rawScore).toBe(0);
      expect(res.activeRiskTier.id).toBe('tier_ich_0');
      expect(res.activeRiskTier.statisticalOutcome).toContain('0%');
    });

    it('exhaustive stress: tests all 48 possible input states and verifies monotonic risk mapping', () => {
      const gcsStates = [
        { id: 'opt_ich_gcs_13_15', pts: 0 },
        { id: 'opt_ich_gcs_5_12',  pts: 1 },
        { id: 'opt_ich_gcs_3_4',   pts: 2 },
      ];
      const volStates = [
        { id: 'opt_ich_vol_lt30', pts: 0 },
        { id: 'opt_ich_vol_ge30', pts: 1 },
      ];
      const ivhStates = [
        { id: 'opt_ich_ivh_no',  pts: 0 },
        { id: 'opt_ich_ivh_yes', pts: 1 },
      ];
      const infraStates = [
        { id: 'opt_ich_infra_no',  pts: 0 },
        { id: 'opt_ich_infra_yes', pts: 1 },
      ];
      const ageStates = [
        { id: 'opt_ich_age_lt80', pts: 0 },
        { id: 'opt_ich_age_ge80', pts: 1 },
      ];

      let combinationsTested = 0;
      for (const gcs of gcsStates) {
        for (const vol of volStates) {
          for (const ivh of ivhStates) {
            for (const infra of infraStates) {
              for (const age of ageStates) {
                const expectedScore = gcs.pts + vol.pts + ivh.pts + infra.pts + age.pts;
                const res = calculateScore(ich, {
                  grp_ich_gcs: gcs.id,
                  grp_ich_volume: vol.id,
                  grp_ich_ivh: ivh.id,
                  grp_ich_infratentorial: infra.id,
                  grp_ich_age: age.id,
                });

                expect(res.rawScore).toBe(expectedScore);
                expect(res.rawScore).toBeGreaterThanOrEqual(0);
                expect(res.rawScore).toBeLessThanOrEqual(6);
                expect(res.activeRiskTier).toBeDefined();

                // Check tier mapping fidelity
                if (expectedScore === 0) expect(res.activeRiskTier.id).toBe('tier_ich_0');
                else if (expectedScore === 1) expect(res.activeRiskTier.id).toBe('tier_ich_1');
                else if (expectedScore === 2) expect(res.activeRiskTier.id).toBe('tier_ich_2');
                else if (expectedScore === 3) expect(res.activeRiskTier.id).toBe('tier_ich_3');
                else if (expectedScore === 4) expect(res.activeRiskTier.id).toBe('tier_ich_4');
                else expect(res.activeRiskTier.id).toBe('tier_ich_5_6');

                combinationsTested++;
              }
            }
          }
        }
      }

      // 3 * 2 * 2 * 2 * 2 = 48 states
      expect(combinationsTested).toBe(48);
    });

    it('validates mandatory bioethical warning against self-fulfilling prophecy', () => {
      const res = calculateScore(ich, {});
      expect(res.clinicalWarning).toContain('PROFECIA AUTORREALIZÁVEL');
      expect(res.clinicalWarning).toContain('DNR');
    });
  });

  // ==========================================================================
  // DIMENSION 5: MARSHALL, HUNT-HESS, WFNS, FISHER, ASIA, EDSS, MEEM, MOCA
  // ==========================================================================
  describe('Dimension 5: Neurotrauma, Vascular & Functional Scales Stress Harness', () => {

    // 1. Marshall CT
    describe('Marshall CT Classification (`calc_marshall`)', () => {
      const marshall = getTool('calc_marshall');

      it('evaluates all 6 categories (I to VI) and correctly maps diffuse vs mass lesions', () => {
        for (let i = 1; i <= 6; i++) {
          const res = calculateScore(marshall, { grp_marshall_cat: `opt_marshall_${i}` });
          expect(res.rawScore).toBe(i);
          if (i <= 2) expect(res.activeRiskTier.id).toBe('tier_marshall_low');
          else if (i <= 5) expect(res.activeRiskTier.id).toBe('tier_marshall_mod');
          else expect(res.activeRiskTier.id).toBe('tier_marshall_crit');
        }
      });

      it('defaults to Grade I on empty input', () => {
        const res = calculateScore(marshall, {});
        expect(res.rawScore).toBe(1);
        expect(res.activeRiskTier.id).toBe('tier_marshall_low');
      });
    });

    // 2. Hunt-Hess
    describe('Hunt-Hess Scale (`calc_hunt_hess`)', () => {
      const hh = getTool('calc_hunt_hess');

      it('verifies +1 comorbidity modifier behavior and clamping at Grade 5', () => {
        // Grade 1 + comorbidity = 2
        expect(calculateScore(hh, { grp_hh_grade: 'opt_hh_1', grp_hh_modifier: 'opt_hh_mod_present' }).rawScore).toBe(2);
        // Grade 2 + comorbidity = 3
        expect(calculateScore(hh, { grp_hh_grade: 'opt_hh_2', grp_hh_modifier: 'opt_hh_mod_present' }).rawScore).toBe(3);
        // Grade 3 + comorbidity = 4
        expect(calculateScore(hh, { grp_hh_grade: 'opt_hh_3', grp_hh_modifier: 'opt_hh_mod_present' }).rawScore).toBe(4);
        // Grade 4 + comorbidity = 5
        expect(calculateScore(hh, { grp_hh_grade: 'opt_hh_4', grp_hh_modifier: 'opt_hh_mod_present' }).rawScore).toBe(5);
        // Grade 5 + comorbidity = 5 (clamped by maxPossibleScore: 5!)
        const g5res = calculateScore(hh, { grp_hh_grade: 'opt_hh_5', grp_hh_modifier: 'opt_hh_mod_present' });
        expect(g5res.rawScore).toBe(5);
        expect(g5res.activeRiskTier.id).toBe('tier_hh_poor');
      });

      it('asserts black-box warning prohibiting intravenous Nimodipine', () => {
        const res = calculateScore(hh, {});
        expect(res.clinicalWarning).toContain('PROIBIDA a administração da formulação de Nimodipino');
        expect(res.clinicalWarning).toContain('VIA ORAL ou SONDA ENTERAL');
      });
    });

    // 3. WFNS
    describe('WFNS Scale (`calc_wfns`)', () => {
      const wfns = getTool('calc_wfns');

      it('discriminates Grade II vs Grade III based strictly on major motor deficit', () => {
        // Grade II: GCS 13-14 without motor deficit -> score 2
        const g2 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_2' });
        expect(g2.rawScore).toBe(2);
        expect(g2.activeRiskTier.id).toBe('tier_wfns_low');

        // Grade III: GCS 13-14 WITH motor deficit -> score 3
        const g3 = calculateScore(wfns, { grp_wfns_class: 'opt_wfns_3' });
        expect(g3.rawScore).toBe(3);
        expect(g3.activeRiskTier.id).toBe('tier_wfns_mod');
      });
    });

    // 4. Fisher Classic vs Modified
    describe('Fisher Classic & Modified Scales', () => {
      const fisherCl = getTool('calc_fisher_classic');
      const fisherMod = getTool('calc_fisher_modified');

      it('confirms the non-linear paradox in Fisher Classic: Grade 3 has highest vasospasm risk', () => {
        const g3 = calculateScore(fisherCl, { grp_fisher_classic: 'opt_fc_3' });
        expect(g3.rawScore).toBe(3);
        expect(g3.activeRiskTier.id).toBe('tier_fc_crit');
        expect(g3.activeRiskTier.statisticalOutcome).toContain('60% a 80%');

        const g4 = calculateScore(fisherCl, { grp_fisher_classic: 'opt_fc_4' });
        expect(g4.rawScore).toBe(4);
        expect(g4.activeRiskTier.id).toBe('tier_fc_hydro');
        expect(g4.activeRiskTier.statisticalOutcome).toContain('15% a 20%');
      });

      it('confirms monotonic risk progression in Fisher Modified (Claassen 2001) from 0 to 4', () => {
        for (let i = 0; i <= 4; i++) {
          const res = calculateScore(fisherMod, { grp_fisher_mod: `opt_fm_${i}` });
          expect(res.rawScore).toBe(i);
        }
      });
    });

    // 5. ASIA / AIS
    describe('ASIA / AIS Impairment Scale (`calc_asia_ais`)', () => {
      const asia = getTool('calc_asia_ais');

      it('evaluates all 5 grades A through E and enforces S4-S5 sacral key warning', () => {
        const grades = [
          { id: 'opt_ais_a', score: 1, tier: 'tier_ais_a' },
          { id: 'opt_ais_b', score: 2, tier: 'tier_ais_b' },
          { id: 'opt_ais_c', score: 3, tier: 'tier_ais_c' },
          { id: 'opt_ais_d', score: 4, tier: 'tier_ais_d' },
          { id: 'opt_ais_e', score: 5, tier: 'tier_ais_e' },
        ];

        for (const g of grades) {
          const res = calculateScore(asia, { grp_asia_grade: g.id });
          expect(res.rawScore).toBe(g.score);
          expect(res.activeRiskTier.id).toBe(g.tier);
        }

        const res = calculateScore(asia, {});
        expect(res.clinicalWarning).toContain('CHAVE SACRAL (S4-S5)');
        expect(res.clinicalWarning).toContain('CORTICOSTEROIDES EM MEGADOSES (NASCIS) SÃO FORMALMENTE CONTRAINDICADOS');
      });
    });

    // 6. EDSS
    describe('EDSS Expanded Disability Status Scale (`calc_edss`)', () => {
      const edss = getTool('calc_edss');

      it('verifies 0.0 to 10.0 scale and structural discontinuity at 4.0', () => {
        expect(edss.minPossibleScore).toBe(0.0);
        expect(edss.maxPossibleScore).toBe(10.0);

        const normal = calculateScore(edss, { grp_edss_level: 'opt_edss_0_0' });
        expect(normal.rawScore).toBe(0.0);
        expect(normal.activeRiskTier.id).toBe('tier_edss_ambulatory');

        const step4 = calculateScore(edss, { grp_edss_level: 'opt_edss_4_0' });
        expect(step4.rawScore).toBe(4.0);
        expect(step4.activeRiskTier.id).toBe('tier_edss_ambulatory');

        const step6 = calculateScore(edss, { grp_edss_level: 'opt_edss_6_0' });
        expect(step6.rawScore).toBe(6.0);
        expect(step6.activeRiskTier.id).toBe('tier_edss_gait_aid');

        const death = calculateScore(edss, { grp_edss_level: 'opt_edss_10_0' });
        expect(death.rawScore).toBe(10.0);
        expect(death.activeRiskTier.id).toBe('tier_edss_death');

        expect(edss.clinicalWarning).toContain('DESCONTINUIDADE ESTRUTURAL NO EDSS 4,0');
      });
    });

    // 7. MEEM / MMSE
    describe('MEEM / MMSE (`calc_meem_mmse`)', () => {
      const meem = getTool('calc_meem_mmse');

      it('verifies maximum score 30 and minimum score 0', () => {
        // Zero acertos across all 11 operational subtests
        const zeroRes = calculateScore(meem, {
          grp_meem_time: 'opt_meem_time_0',
          grp_meem_space: 'opt_meem_space_0',
          grp_meem_reg: 'opt_meem_reg_0',
          grp_meem_calc: 'opt_meem_calc_0',
          grp_meem_recall: 'opt_meem_recall_0',
          grp_meem_naming: 'opt_meem_naming_0',
          grp_meem_repeat: 'opt_meem_rep_0',
          grp_meem_command: 'opt_meem_cmd_0',
          grp_meem_read: 'opt_meem_read_0',
          grp_meem_write: 'opt_meem_write_0',
          grp_meem_praxia: 'opt_meem_praxia_0',
        });
        expect(zeroRes.rawScore).toBe(0);
        expect(zeroRes.activeRiskTier.id).toBe('tier_meem_severe_decline');

        // Perfect score
        const maxRes = calculateScore(meem, {});
        expect(maxRes.rawScore).toBe(30);
        expect(maxRes.activeRiskTier.id).toBe('tier_meem_normal');
      });

      it('warns about ceiling effect in patients with >11 years of schooling', () => {
        const res = calculateScore(meem, {});
        expect(res.clinicalWarning).toContain('EFEITO TETO');
        expect(res.clinicalWarning).toContain('MoCA');
      });
    });

    // 8. MoCA
    describe('MoCA Cognitive Assessment (`calc_moca`)', () => {
      const moca = getTool('calc_moca');

      it('applies +1 education adjustment and crosses clinical threshold (25 -> 26)', () => {
        // Subtotal = 25 points without education
        const baseInputs: Record<string, string> = {
          grp_moca_visuo: 'opt_moca_visuo_5',         // 5
          grp_moca_naming: 'opt_moca_naming_3',       // 3
          grp_moca_attention: 'opt_moca_att_6',       // 6
          grp_moca_lang: 'opt_moca_lang_3',           // 3
          grp_moca_abstract: 'opt_moca_abs_2',        // 2
          grp_moca_delayed_recall: 'opt_moca_rec_0',  // 0 (amnestic deficit: 0 instead of 5)
          grp_moca_orient: 'opt_moca_orient_6',       // 6
        };

        // 1. With higher education (>12y): score = 25 (abnormal / MCI screening positive)
        const resHigher = calculateScore(moca, {
          ...baseInputs,
          grp_moca_edu_adj: 'opt_moca_edu_gt12', // +0
        });
        expect(resHigher.rawScore).toBe(25);
        expect(resHigher.activeRiskTier.id).toBe('tier_moca_mci');

        // 2. With <=12y education: score = 26 (adjusted to normal >= 26!)
        const resAdjusted = calculateScore(moca, {
          ...baseInputs,
          grp_moca_edu_adj: 'opt_moca_edu_le12', // +1
        });
        expect(resAdjusted.rawScore).toBe(26);
        expect(resAdjusted.activeRiskTier.id).toBe('tier_moca_normal');
      });

      it('clamping: perfect score (30) with education correction (+1) DOES NOT exceed 30', () => {
        const perfectInputs: Record<string, string> = {
          grp_moca_visuo: 'opt_moca_visuo_5',         // 5
          grp_moca_naming: 'opt_moca_naming_3',       // 3
          grp_moca_attention: 'opt_moca_att_6',       // 6
          grp_moca_lang: 'opt_moca_lang_3',           // 3
          grp_moca_abstract: 'opt_moca_abs_2',        // 2
          grp_moca_delayed_recall: 'opt_moca_rec_5',  // 5
          grp_moca_orient: 'opt_moca_orient_6',       // 6
          grp_moca_edu_adj: 'opt_moca_edu_le12',      // +1 -> sum 31, clamped to 30
        };

        const res = calculateScore(moca, perfectInputs);
        expect(res.rawScore).toBe(30);
        expect(res.score).toBe(30);
        expect(res.activeRiskTier.id).toBe('tier_moca_normal');
      });
    });
  });

  // ==========================================================================
  // DIMENSION 6: UNIVERSAL EXTREME, MALFORMED & FUZZING RESILIENCE
  // ==========================================================================
  describe('Dimension 6: Universal Robustness Across All Block 03 Calculators', () => {
    const allCalculators = parsedBlock03.calculators;

    it('verifies Block 03 contains all 39 clinical tools losslessly', () => {
      expect(allCalculators.length).toBe(39);
    });

    it('adversarial fuzz: empty input `{}` across all calculators never crashes and produces valid result', () => {
      for (const calc of allCalculators) {
        expect(() => calculateScore(calc, {})).not.toThrow();
        const res = calculateScore(calc, {});

        expect(res).toBeDefined();
        expect(typeof res.rawScore).toBe('number');
        expect(isNaN(res.rawScore)).toBe(false);

        if (calc.minPossibleScore !== undefined) {
          expect(res.rawScore).toBeGreaterThanOrEqual(calc.minPossibleScore);
        }
        if (calc.maxPossibleScore !== undefined) {
          expect(res.rawScore).toBeLessThanOrEqual(calc.maxPossibleScore);
        }

        expect(res.activeRiskTier).toBeDefined();
        expect(res.activeRiskTier.id).toBeDefined();
        expect(res.activeRiskTier.statisticalOutcome).toBeDefined();
        expect(typeof res.scoreFormatted).toBe('string');
      }
    });

    it('adversarial fuzz: garbage payload with nonexistent keys and corrupt types never throws', () => {
      const evilPayload = {
        _proto_: 'polluted',
        undefined_key: undefined,
        null_key: null,
        garbage_string: 'totally_random_token_!@#$',
        negative_numeric: -99999,
        huge_numeric: 9999999,
        boolean_chaos: false,
        nested_object: { deep: 'trap' },
        nan_val: NaN,
      };

      for (const calc of allCalculators) {
        expect(() => calculateScore(calc, evilPayload)).not.toThrow();
        const res = calculateScore(calc, evilPayload);

        expect(res).toBeDefined();
        expect(isNaN(res.rawScore)).toBe(false);
      }
    });

    it('adversarial fuzz: partial inputs (only first parameter specified) degrade safely to defaults', () => {
      for (const calc of allCalculators) {
        const firstGroup = calc.parameterGroups[0];
        if (!firstGroup || !firstGroup.options || firstGroup.options.length === 0) continue;

        const partialInput = {
          [firstGroup.id]: firstGroup.options[firstGroup.options.length - 1].id,
        };

        expect(() => calculateScore(calc, partialInput)).not.toThrow();
        const res = calculateScore(calc, partialInput);

        expect(res).toBeDefined();
        expect(isNaN(res.rawScore)).toBe(false);
      }
    });

    it('boundary clamping invariant: score is strictly clamped within [minPossibleScore, maxPossibleScore]', () => {
      const delegatedCalculators = new Set([
        'calc_sagittal_balance',
        'calc_noms_bilsky',
        'calc_lawton_young',
        'calc_phases_score',
        'calc_glasgow_p',
      ]);

      for (const calc of allCalculators) {
        if (calc.minPossibleScore === undefined || calc.maxPossibleScore === undefined) continue;
        if (calc.calculationType !== 'additive_points') continue;
        if (delegatedCalculators.has(calc.id)) continue;

        // Force underflow with negative baseScore
        const underflowCalc = { ...calc, baseScore: -9999 };
        const underflowRes = calculateScore(underflowCalc, {});
        expect(underflowRes.rawScore).toBe(calc.minPossibleScore);

        // Force overflow with excessive baseScore
        const overflowCalc = { ...calc, baseScore: 9999 };
        const overflowRes = calculateScore(overflowCalc, {});
        expect(overflowRes.rawScore).toBe(calc.maxPossibleScore);
      }
    });
  });
});
