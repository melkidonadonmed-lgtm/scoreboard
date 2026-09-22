/**
 * SURGICAL CUTOFFS, DECISION THRESHOLDS & CLINICAL EDGE CASES UNIT TESTS
 * Target File: tests/unit/test_neurosurgery_cutoffs.test.ts
 *
 * Comprehensive validation across all neurosurgical modules:
 * 1.  TLICS: Thoracolumbar Spine Trauma (cutoffs <= 3, 4, >= 5; ASIA B/C/D 3 pts vs ASIA A 2 pts)
 * 2.  SLICS: Subaxial Cervical Spine Trauma (cutoffs <= 3, 4, >= 5; +1 progressive deficit modifier)
 * 3.  Anderson-D'Alonzo: C2 Odontoid Fractures (Type I vs II vs III; Grauer IIB anterior screw vs Grauer IIC Harms-Goel)
 * 4.  SINS: Spine Instability Neoplastic Score (tiers 0-6 stable, 7-12 potentially unstable, 13-18 unstable)
 * 5.  NOMS Decision Framework: Multidimensional oncologic pathways (Profiles 1, 2, 3, 4)
 * 6.  Spinopelvic Sagittal Balance: PI = PT + SS identity, PI-LL mismatch, PT, SVA, osteotomies (SPO, PSO, VCR)
 * 7.  PHASES Aneurysm Score: Rupture risk tiers <= 3, 4-7, >= 8; 5-year rupture percentages
 * 8.  Lawton-Young Supplementary AVM: Combined score 2-10 (tiers 2-4 low, 5-6 intermediate, 7-10 prohibitive ARUBA)
 * 9.  Zabramski Cavernoma Classification: Types I & II active vs Type III inactive vs Type IV familial
 * 10. Vasograde: Bivariate DCI matrix (Green vs Yellow vs Red)
 * 11. Knosp Pituitary Classification: Grades 0-2 EETS GTR vs Grades 3A/3B/4 intentional subtotal + SRS
 * 12. Samii & Koos Vestibular Schwannoma: Koos I-III vs Koos IV with brainstem compression & DVE
 * 13. Kiefer Scale & Evans/DESH: Active NPH Tap Test response & gravitational VPS vs Alzheimer ex-vacuo
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
import {
  type Calculator,
  type BlockData,
  CalculationResultSchema
} from '@/types/clinical';

const parsedBlock03: BlockData = rawBlock03Data as unknown as BlockData;

function getTool(id: string): Calculator {
  const tool = parsedBlock03.calculators.find((c) => c.id === id);
  if (!tool) throw new Error(`Calculator ${id} not found in Block 03`);
  return tool;
}

describe('Neurosurgical Decision Thresholds & Surgical Cutoffs Suite', () => {

  // ==========================================================================
  // 1. TLICS: THORACOLUMBAR INJURY CLASSIFICATION AND SEVERITY SCORE
  // ==========================================================================
  describe('1. TLICS Surgical Decision Cutoffs (`calc_tlics`)', () => {
    const tlics = getTool('calc_tlics');

    it('verifies tool metadata, formula and three-pillar radar axes', () => {
      expect(tlics.id).toBe('calc_tlics');
      expect(tlics.minPossibleScore).toBe(1);
      expect(tlics.maxPossibleScore).toBe(10);
      expect(tlics.radarAxes.length).toBe(3);
      expect(tlics.parameterGroups.length).toBe(3);
      expect(tlics.riskTiers.length).toBe(3);
    });

    it('validates Cutoff <= 3: Conservative Management Safe (low severity)', () => {
      // Case 1: Simple compression (1 pt) + intact PLC (0 pt) + intact neuro (0 pt) = 1 pt
      const res1 = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_comp',
        grp_tlics_plc: 'opt_tlics_plc_intact',
        grp_tlics_neuro: 'opt_tlics_neuro_intact'
      });
      expect(res1.rawScore).toBe(1);
      expect(res1.activeRiskTier.id).toBe('tier_tlics_cons');
      expect(res1.activeRiskTier.severityLevel).toBe('low');
      expect(res1.activeRiskTier.label).toContain('Tratamento Conservador Seguro');
      expect(res1.activeRiskTier.nonPharmacologicalActions[0].monitoringPlan).toContain('TLSO');

      // Case 2: Burst fracture (2 pts) + intact PLC (0 pt) + intact neuro (0 pt) = 2 pts
      const res2 = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_burst',
        grp_tlics_plc: 'opt_tlics_plc_intact',
        grp_tlics_neuro: 'opt_tlics_neuro_intact'
      });
      expect(res2.rawScore).toBe(2);
      expect(res2.activeRiskTier.id).toBe('tier_tlics_cons');
      expect(res2.activeRiskTier.severityLevel).toBe('low');

      // Case 3: Compression (1 pt) + suspect PLC (2 pts) + intact neuro (0 pt) = 3 pts (upper boundary)
      const res3 = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_comp',
        grp_tlics_plc: 'opt_tlics_plc_suspect',
        grp_tlics_neuro: 'opt_tlics_neuro_intact'
      });
      expect(res3.rawScore).toBe(3);
      expect(res3.activeRiskTier.id).toBe('tier_tlics_cons');
      expect(res3.activeRiskTier.severityLevel).toBe('low');
    });

    it('validates Cutoff 4: Borderline / Surgeon\'s Choice Equipoise (intermediate severity)', () => {
      // Burst (2 pts) + Suspected PLC (2 pts) + Intact neuro (0 pt) = 4 pts
      const res4 = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_burst',
        grp_tlics_plc: 'opt_tlics_plc_suspect',
        grp_tlics_neuro: 'opt_tlics_neuro_intact'
      });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_tlics_lim');
      expect(res4.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res4.activeRiskTier.label).toContain('Zona Limítrofe / Critério do Cirurgião');
      expect(res4.activeRiskTier.nonPharmacologicalActions[0].monitoringPlan).toContain('cifose focal > 20-30°');
    });

    it('validates Cutoff >= 5: Mandatory Surgery (critical severity)', () => {
      // Burst (2 pts) + Disrupted PLC (3 pts) + Intact neuro (0 pt) = 5 pts (surgical boundary)
      const res5 = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_burst',
        grp_tlics_plc: 'opt_tlics_plc_disrupt',
        grp_tlics_neuro: 'opt_tlics_neuro_intact'
      });
      expect(res5.rawScore).toBe(5);
      expect(res5.activeRiskTier.id).toBe('tier_tlics_surg');
      expect(res5.activeRiskTier.severityLevel).toBe('critical');
      expect(res5.activeRiskTier.label).toContain('Indicação Cirúrgica Mandatória');
      expect(res5.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Artrodese Posterior Instrumentada com Parafusos Pediculares'
      );

      // Distraction (4 pts) + Disrupted PLC (3 pts) + Cauda equina (3 pts) = 10 pts (maximum severity)
      const res10 = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_distr',
        grp_tlics_plc: 'opt_tlics_plc_disrupt',
        grp_tlics_neuro: 'opt_tlics_neuro_cauda'
      });
      expect(res10.rawScore).toBe(10);
      expect(res10.activeRiskTier.id).toBe('tier_tlics_surg');
      expect(res10.activeRiskTier.severityLevel).toBe('critical');
    });

    it('demonstrates clinical edge case: incomplete cord injury (3 pts) vs complete (2 pts) flipping decision', () => {
      // Identical spinal lesion: Burst fracture (2 pts) + Intact PLC (0 pt)
      // Comparison A: Complete cord injury (ASIA A = 2 pts) -> Total = 4 pts (Borderline / Surgeon's Choice)
      const resComplete = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_burst',
        grp_tlics_plc: 'opt_tlics_plc_intact',
        grp_tlics_neuro: 'opt_tlics_neuro_complete'
      });
      expect(resComplete.rawScore).toBe(4);
      expect(resComplete.activeRiskTier.id).toBe('tier_tlics_lim');
      expect(resComplete.activeRiskTier.severityLevel).toBe('intermediate');

      // Comparison B: Incomplete cord injury (ASIA B/C/D = 3 pts) -> Total = 5 pts (Mandatory Urgent Surgery)
      const resIncomplete = calculateScore(tlics, {
        grp_tlics_morphology: 'opt_tlics_morph_burst',
        grp_tlics_plc: 'opt_tlics_plc_intact',
        grp_tlics_neuro: 'opt_tlics_neuro_incomplete'
      });
      expect(resIncomplete.rawScore).toBe(5);
      expect(resIncomplete.activeRiskTier.id).toBe('tier_tlics_surg');
      expect(resIncomplete.activeRiskTier.severityLevel).toBe('critical');

      // Biological justification: Incomplete lesion has salvageable neural tissue at risk of irreversible ischemia
      expect(tlics.clinicalWarning).toContain('lesão medular incompleta pontua 3 pontos');
      expect(tlics.clinicalWarning).toContain('mais do que a completa, que pontua 2');
    });
  });

  // ==========================================================================
  // 2. SLICS: SUBAXIAL CERVICAL SPINE INJURY CLASSIFICATION SYSTEM
  // ==========================================================================
  describe('2. SLICS Surgical Decision Cutoffs & Progressive Modifier (`calc_slics`)', () => {
    const slics = getTool('calc_slics');

    it('verifies tool metadata, formula and four-pillar radar axes including modifier', () => {
      expect(slics.id).toBe('calc_slics');
      expect(slics.minPossibleScore).toBe(0);
      expect(slics.maxPossibleScore).toBe(10);
      expect(slics.radarAxes.length).toBe(4);
      expect(slics.parameterGroups.length).toBe(4);
    });

    it('validates Cutoff <= 3: Conservative Management Safe with Rigid Miami-J Collar', () => {
      // Normal alignment (0) + Intact DLC (0) + Intact neuro (0) + No progression (0) = 0 pts
      const res0 = calculateScore(slics, {
        grp_slics_morphology: 'opt_slics_morph_none',
        grp_slics_dlc: 'opt_slics_dlc_intact',
        grp_slics_neuro: 'opt_slics_neuro_intact',
        grp_slics_modifier: 'opt_slics_mod_no'
      });
      expect(res0.rawScore).toBe(0);
      expect(res0.activeRiskTier.id).toBe('tier_slics_cons');
      expect(res0.activeRiskTier.severityLevel).toBe('low');
      expect(res0.activeRiskTier.nonPharmacologicalActions[0].monitoringPlan).toContain('Miami-J');

      // Compression (1 pt) + DLC indeterminate (1 pt) + Radiculopathy (1 pt) + No progression (0) = 3 pts
      const res3 = calculateScore(slics, {
        grp_slics_morphology: 'opt_slics_morph_comp',
        grp_slics_dlc: 'opt_slics_dlc_indet',
        grp_slics_neuro: 'opt_slics_neuro_rad',
        grp_slics_modifier: 'opt_slics_mod_no'
      });
      expect(res3.rawScore).toBe(3);
      expect(res3.activeRiskTier.id).toBe('tier_slics_cons');
      expect(res3.activeRiskTier.severityLevel).toBe('low');
    });

    it('validates Cutoff 4: Borderline / Individualization Tier', () => {
      // Compression (1 pt) + Disrupted DLC (2 pts) + Radiculopathy (1 pt) + No progression (0) = 4 pts
      const res4 = calculateScore(slics, {
        grp_slics_morphology: 'opt_slics_morph_comp',
        grp_slics_dlc: 'opt_slics_dlc_disrupt',
        grp_slics_neuro: 'opt_slics_neuro_rad',
        grp_slics_modifier: 'opt_slics_mod_no'
      });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_slics_lim');
      expect(res4.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res4.activeRiskTier.label).toContain('Conduta Limítrofe / Individualização');
    });

    it('validates Cutoff >= 5: Mandatory Surgery (ACDF / Posterior Arthrodesis)', () => {
      // Translation/facet dislocation (4 pts) + Disrupted DLC (2 pts) = 6 pts
      const res6 = calculateScore(slics, {
        grp_slics_morphology: 'opt_slics_morph_trans',
        grp_slics_dlc: 'opt_slics_dlc_disrupt',
        grp_slics_neuro: 'opt_slics_neuro_intact',
        grp_slics_modifier: 'opt_slics_mod_no'
      });
      expect(res6.rawScore).toBe(6);
      expect(res6.activeRiskTier.id).toBe('tier_slics_surg');
      expect(res6.activeRiskTier.severityLevel).toBe('critical');
      expect(res6.activeRiskTier.label).toContain('Indicação Cirúrgica Mandatória');
      expect(res6.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain('ACDF');
      expect(res6.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Noradrenalina');
      expect(res6.activeRiskTier.pharmacologicalActions[0].dosage).toContain('PAM entre 85 e 90 mmHg');
    });

    it('demonstrates +1 progressive neurologic deterioration modifier converting borderline (4 pts) to surgical (5 pts)', () => {
      // Baseline Borderline scenario: Compression (1 pt) + Disrupted DLC (2 pts) + Radiculopathy (1 pt) = 4 pts
      const baselineBorderline = calculateScore(slics, {
        grp_slics_morphology: 'opt_slics_morph_comp',
        grp_slics_dlc: 'opt_slics_dlc_disrupt',
        grp_slics_neuro: 'opt_slics_neuro_rad',
        grp_slics_modifier: 'opt_slics_mod_no' // 0 pts
      });
      expect(baselineBorderline.rawScore).toBe(4);
      expect(baselineBorderline.activeRiskTier.id).toBe('tier_slics_lim');
      expect(baselineBorderline.activeRiskTier.severityLevel).toBe('intermediate');

      // Clinical deterioration event: +1 progressive modifier added
      const convertedSurgical = calculateScore(slics, {
        grp_slics_morphology: 'opt_slics_morph_comp',
        grp_slics_dlc: 'opt_slics_dlc_disrupt',
        grp_slics_neuro: 'opt_slics_neuro_rad',
        grp_slics_modifier: 'opt_slics_mod_yes' // +1 pt
      });
      expect(convertedSurgical.rawScore).toBe(5);
      expect(convertedSurgical.activeRiskTier.id).toBe('tier_slics_surg');
      expect(convertedSurgical.activeRiskTier.severityLevel).toBe('critical');
      expect(convertedSurgical.radarValues['axis_slics_mod']).toBe(1.0);
    });
  });

  // ==========================================================================
  // 3. ANDERSON-D'ALONZO: ODONTOID C2 FRACTURES & GRAUER SUBTYPES
  // ==========================================================================
  describe('3. Anderson-D\'Alonzo C2 Odontoid Fractures & Grauer Subtypes (`calc_anderson_dalonzo`)', () => {
    const anderson = getTool('calc_anderson_dalonzo');

    it('verifies tool structure, options and Grauer surgical adjudication', () => {
      expect(anderson.id).toBe('calc_anderson_dalonzo');
      expect(anderson.calculationType).toBe('branching_decision');
      expect(anderson.parameterGroups[0].options.length).toBe(4);
      expect(anderson.riskTiers.length).toBe(3);
    });

    it('validates Type I: Odontoid Apex Avulsion (Stable / Conservative Collar)', () => {
      const res = calculateScore(anderson, { grp_anderson_type: 'opt_od_type1' });
      expect(res.rawScore).toBe(1);
      expect(res.activeRiskTier.id).toBe('tier_od_cons');
      expect(res.activeRiskTier.severityLevel).toBe('low');
      expect(res.activeRiskTier.label).toContain('Tipos I e III: Tratamento Conservador Seguro');
      expect(res.activeRiskTier.statisticalOutcome).toContain('superior a 85% a 95%');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain('Colar Cervical Rígido');
    });

    it('validates Grauer IIB: Anterior Odontoid Screw Candidate (Motion-Preserving Bohler/Apfelbaum)', () => {
      const res = calculateScore(anderson, { grp_anderson_type: 'opt_od_type2_b' });
      expect(res.rawScore).toBe(2);
      expect(res.activeRiskTier.id).toBe('tier_od_screw');
      expect(res.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res.activeRiskTier.label).toContain('Tipo IIB: Indicação de Osteossíntese Anterior com Parafuso de Odontoide');
      expect(res.activeRiskTier.statisticalOutcome).toContain('Preservação de 50% da rotação axial');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'parafusos canulados de rosca parcial de 3,5 mm'
      );
    });

    it('verifies clinical rule: Grauer IIC reverse oblique contraindicates anterior screw and mandates Harms-Goel posterior fixation', () => {
      const opt2c = anderson.parameterGroups[0].options.find((o) => o.id === 'opt_od_type2_c')!;
      expect(opt2c.label).toContain('Grauer IIC');
      expect(opt2c.description).toContain('Contraindica parafuso anterior; exige fixação posterior C1-C2 de Harms');

      // Verify clinical warning strictly details biomechanical shear failure of anterior screw
      expect(anderson.clinicalWarning).toContain('CONTRAINDICAÇÃO FORMAL AO PARAFUSO ANTERIOR DE ODONTOIDE');
      expect(anderson.clinicalWarning).toContain('Traço oblíquo reverso (Grauer Tipo IIC: anteroinferior para posterossuperior)');
      expect(anderson.clinicalWarning).toContain('o aperto do parafuso causa cisalhamento e deslocamento anterior do dente');
      expect(anderson.clinicalWarning).toContain('Artrodese Posterior C1-C2 de Harms-Goel');

      // Verify tier_od_harms specifies Harms-Goel technique
      const harmsTier = anderson.riskTiers.find((t) => t.id === 'tier_od_harms')!;
      expect(harmsTier.label).toContain('Tipo IIC / Falha de Parafuso: Indicação de Artrodese Posterior C1-C2 de Harms-Goel');
      expect(harmsTier.nonPharmacologicalActions[0].interventionalProcedure).toContain('massa lateral de C1 e parafusos pediculares/ístmicos de C2');
    });

    it('verifies Type III: C2 Cancellous Body Extension has high spontaneous union rate (>85-95%)', () => {
      const opt3 = anderson.parameterGroups[0].options.find((o) => o.id === 'opt_od_type3')!;
      expect(opt3.label).toContain('Tipo III: Fratura com Extensão para o Corpo Esponjoso de C2');
      expect(opt3.description).toContain('Alta taxa de união consolidada (85-95%)');
      expect(opt3.isNormalBaseline).toBe(true);

      const consTier = anderson.riskTiers.find((t) => t.id === 'tier_od_cons')!;
      expect(consTier.label).toContain('Tipos I e III');
    });
  });

  // ==========================================================================
  // 4. SINS: SPINE INSTABILITY NEOPLASTIC SCORE
  // ==========================================================================
  describe('4. SINS Instability Tiers & Radiation Safety (`calc_sins`)', () => {
    const sins = getTool('calc_sins');

    it('verifies tool metadata, formula and 6 parameters summing to 18 points', () => {
      expect(sins.id).toBe('calc_sins');
      expect(sins.minPossibleScore).toBe(0);
      expect(sins.maxPossibleScore).toBe(18);
      expect(sins.parameterGroups.length).toBe(6);
      expect(sins.riskTiers.length).toBe(3);
    });

    it('validates Tier 1 (0 to 6 points): Stable Spine (RT safe without surgical stabilization)', () => {
      // Baseline stable: Rigid S2-S5 (0) + No pain (0) + Blastic (0) + Normal align (0) + Involve <=50% (0) + No posterior (0) = 0 pts
      const res0 = calculateScore(sins, {});
      expect(res0.rawScore).toBe(0);
      expect(res0.activeRiskTier.id).toBe('tier_sins_stable');
      expect(res0.activeRiskTier.severityLevel).toBe('low');
      expect(res0.activeRiskTier.label).toContain('Coluna Estável (0 a 6 pontos)');
      expect(res0.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Radioterapia Externa Convencional ou SBRT Segura'
      );
      expect(res0.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia profilática contraindicada'
      );

      // Score 6: Mobile (2) + Non-mechanical pain (1) + Mixed (1) + De novo (2) = 6 pts (upper bound of stable)
      const res6 = calculateScore(sins, {
        grp_sins_location: 'opt_sins_loc_mob', // 2
        grp_sins_pain: 'opt_sins_pain_nonmech', // 1
        grp_sins_bone: 'opt_sins_bone_mixed',  // 1
        grp_sins_alignment: 'opt_sins_align_denovo' // 2
      });
      expect(res6.rawScore).toBe(6);
      expect(res6.activeRiskTier.id).toBe('tier_sins_stable');
      expect(res6.activeRiskTier.severityLevel).toBe('low');
    });

    it('validates Tier 2 (7 to 12 points): Potentially Unstable (Kyphoplasty / Percutaneous Stabilization)', () => {
      // Score 7: Junctional (3) + Mechanical pain (3) + Unilateral posterior (1) = 7 pts (lower boundary)
      const res7 = calculateScore(sins, {
        grp_sins_location: 'opt_sins_loc_junc', // 3
        grp_sins_pain: 'opt_sins_pain_mech',    // 3
        grp_sins_posterior: 'opt_sins_post_unilat' // 1
      });
      expect(res7.rawScore).toBe(7);
      expect(res7.activeRiskTier.id).toBe('tier_sins_potential');
      expect(res7.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res7.activeRiskTier.label).toContain('Coluna Potencialmente Instável (7 a 12 pontos)');
      expect(res7.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cifoplastia percutânea ou estabilização cirúrgica'
      );

      // Score 12: Junctional (3) + Mechanical pain (3) + Lytic (2) + De novo (2) + Collapse <= 50% (2) = 12 pts (upper boundary)
      const res12 = calculateScore(sins, {
        grp_sins_location: 'opt_sins_loc_junc',    // 3
        grp_sins_pain: 'opt_sins_pain_mech',       // 3
        grp_sins_bone: 'opt_sins_bone_lytic',      // 2
        grp_sins_alignment: 'opt_sins_align_denovo', // 2
        grp_sins_collapse: 'opt_sins_coll_le50'    // 2
      });
      expect(res12.rawScore).toBe(12);
      expect(res12.activeRiskTier.id).toBe('tier_sins_potential');
      expect(res12.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('validates Tier 3 (13 to 18 points): Unstable Spine (Mandatory Surgical Stabilization before RT)', () => {
      // Score 13: Junctional (3) + Mechanical pain (3) + Lytic (2) + Subluxation (4) + Involvement > 50% (1) = 13 pts (lower boundary)
      const res13 = calculateScore(sins, {
        grp_sins_location: 'opt_sins_loc_junc',     // 3
        grp_sins_pain: 'opt_sins_pain_mech',        // 3
        grp_sins_bone: 'opt_sins_bone_lytic',       // 2
        grp_sins_alignment: 'opt_sins_align_sublux', // 4
        grp_sins_collapse: 'opt_sins_coll_inv_gt50' // 1
      });
      expect(res13.rawScore).toBe(13);
      expect(res13.activeRiskTier.id).toBe('tier_sins_unstable');
      expect(res13.activeRiskTier.severityLevel).toBe('critical');
      expect(res13.activeRiskTier.label).toContain('Coluna Instável (13 a 18 pontos)');
      expect(res13.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Estabilização Cirúrgica Mandatória Prévia à Radioterapia'
      );
      expect(res13.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Dexametasona');

      // Score 18 (Maximum Derangement): 3 + 3 + 2 + 4 + 3 + 3 = 18 pts
      const res18 = calculateScore(sins, {
        grp_sins_location: 'opt_sins_loc_junc',     // 3
        grp_sins_pain: 'opt_sins_pain_mech',        // 3
        grp_sins_bone: 'opt_sins_bone_lytic',       // 2
        grp_sins_alignment: 'opt_sins_align_sublux', // 4
        grp_sins_collapse: 'opt_sins_coll_gt50',    // 3
        grp_sins_posterior: 'opt_sins_post_bilat'   // 3
      });
      expect(res18.rawScore).toBe(18);
      expect(res18.activeRiskTier.id).toBe('tier_sins_unstable');
      expect(res18.activeRiskTier.severityLevel).toBe('critical');

      // Clinical warning must prohibit isolated radiation without stabilization
      expect(sins.clinicalWarning).toContain('FORMALMENTE CONTRAINDICADA de forma isolada');
      expect(sins.clinicalWarning).toContain('A coluna instável exige fixação instrumentada prévia à irradiação');
      expect(res18.activeRiskTier.nonPharmacologicalActions[0].monitoringPlan).toContain('PROIBIDA RADIOTERAPIA ISOLADA SEM FIXAÇÃO');
    });
  });

  // ==========================================================================
  // 5. NOMS DECISION FRAMEWORK & MULTIDIMENSIONAL PROFILES
  // ==========================================================================
  describe('5. NOMS Decision Framework & Bilsky ESCC (`calc_noms_bilsky`)', () => {

    it('validates Profile 1: Separation Surgery + SBRT (High-grade Bilsky 2/3 + Radioresistant + SINS Unstable + Eligible KPS)', () => {
      const res = calculateNomsFramework({
        bilsky: '2', // High-grade cord compression
        radiosensitivity: 'radioresistant', // e.g. Renal cell carcinoma, melanoma, thyroid
        sins: 14, // Unstable spine
        kps: 80 // Eligible (>= 70%)
      });

      expect(CalculationResultSchema.safeParse(res).success).toBe(true);
      expect(res.rawScore).toBe(4);
      expect(res.scoreFormatted).toContain('Separation Surgery + SBRT');
      expect(res.activeRiskTier.severityLevel).toBe('critical');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia de Separação ("Separation Surgery")'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'descompressão circunferencial de 2 a 3 mm'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'SBRT hipofracionada (18 a 24 Gy'
      );
      expect(res.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Dexametasona');
    });

    it('validates Profile 2: cEBRT alone + high-dose Dexamethasone (High-grade Bilsky 3 + Radiosensitive + Stable Spine)', () => {
      const res = calculateNomsFramework({
        bilsky: '3', // Severe circumferential cord compression
        radiosensitivity: 'radiosensitive', // e.g. Multiple myeloma, lymphoma, seminoma
        sins: 4, // Stable spine
        kps: 80 // Eligible
      });

      expect(res.rawScore).toBe(2);
      expect(res.scoreFormatted).toContain('cEBRT alone');
      expect(res.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Radioterapia Externa Convencional de Urgência (cEBRT: 30 Gy em 10 frações)'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Descompressão cirúrgica aberta dispensada'
      );
    });

    it('validates Profile 3: Percutaneous Stabilization (Low-grade Bilsky 1b + Mechanical Instability SINS 10 + Eligible)', () => {
      const res = calculateNomsFramework({
        bilsky: '1b', // Low-grade epidural extension without cord contact
        radiosensitivity: 'radioresistant',
        sins: 10, // Potentially unstable
        kps: 90
      });

      expect(res.rawScore).toBe(3);
      expect(res.scoreFormatted).toContain('Percutaneous Stabilization');
      expect(res.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cifoplastia com Balão / Vertebroplastia'
      );
    });

    it('validates Profile 4: Palliative Hospice (Systemic Ineligibility KPS < 70% / Terminal Status)', () => {
      const res = calculateNomsFramework({
        bilsky: '3',
        radiosensitivity: 'radioresistant',
        sins: 15,
        kps: 40 // Ineligible / terminal patient
      });

      expect(res.rawScore).toBe(1);
      expect(res.scoreFormatted).toContain('Palliative Hospice');
      expect(res.activeRiskTier.severityLevel).toBe('low');
      expect(res.activeRiskTier.label).toContain('Cuidados Paliativos');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia descompressiva e reconstrução instrumentada aberta estão formalmente contraindicadas'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Radioterapia Paliativa em Fração Única (8 Gy)'
      );
    });
  });

  // ==========================================================================
  // 6. SPINOPELVIC SAGITTAL BALANCE & SRS-SCHWAB CLASSIFICATION
  // ==========================================================================
  describe('6. Spinopelvic Sagittal Balance & Osteotomy Selection (`calc_sagittal_balance`)', () => {

    it('validates Geometrical Identity PI = PT + SS (tolerance <= 3° vs warning > 3°)', () => {
      // Consistent: PI = 55°, PT = 18°, SS = 35° -> PT + SS = 53° (|55 - 53| = 2° <= 3°) -> NO warning
      const consistent = calculateSagittalBalance({
        pi: 55,
        pt: 18,
        ss: 35,
        ll: 55,
        sva: 25
      });
      expect(consistent.warnings).toBeUndefined();

      // Inconsistent: PI = 60°, PT = 15°, SS = 30° -> PT + SS = 45° (|60 - 45| = 15° > 3°) -> WARNING triggered
      const inconsistent = calculateSagittalBalance({
        pi: 60,
        pt: 15,
        ss: 30,
        ll: 50,
        sva: 25
      });
      expect(inconsistent.warnings).toBeDefined();
      expect(inconsistent.warnings?.[0]).toContain('Inconsistência geométrica espinopélvica');
      expect(inconsistent.warnings?.[0]).toContain('15.0° > 3°');
      expect(inconsistent.warnings?.[0]).toContain('Duval-Beaupère');
    });

    it('validates Schwab 0 (Aligned): PI - LL < 10°, PT < 20°, SVA < 40 mm -> In situ arthrodesis', () => {
      // PI = 53°, PT = 13°, SS = 40°, LL = 53° (PI - LL = 0°), SVA = 20 mm
      const res = calculateSagittalBalance({
        pi: 53,
        pt: 13,
        ss: 40,
        ll: 53,
        sva: 20
      });

      expect(res.rawScore).toBe(0); // PI - LL = 0°
      expect(res.scoreFormatted).toContain('Schwab 0');
      expect(res.scoreFormatted).toContain('PT: Normal');
      expect(res.scoreFormatted).toContain('SVA: Normal');
      expect(res.activeRiskTier.severityLevel).toBe('low');
      expect(res.activeRiskTier.label).toContain('Balanço Sagital Preservado');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Artrodese in situ sem necessidade de osteotomias'
      );
    });

    it('validates Schwab + (Moderate Mismatch): PI - LL 10-20°, PT 20-30°, SVA 40-95 mm -> Smith-Petersen (SPO) / ALIF', () => {
      // PI = 55°, PT = 25°, SS = 30°, LL = 40° (PI - LL = 15°), SVA = 65 mm
      const res = calculateSagittalBalance({
        pi: 55,
        pt: 25,
        ss: 30,
        ll: 40,
        sva: 65
      });

      expect(res.rawScore).toBe(15); // PI - LL = 15°
      expect(res.scoreFormatted).toContain('Schwab +');
      expect(res.scoreFormatted).toContain('PT: Moderate');
      expect(res.scoreFormatted).toContain('SVA: Moderate');
      expect(res.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res.activeRiskTier.label).toContain('Desbalanço Sagital Moderado');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Smith-Petersen (SPO / Schwab Grau II)'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain('ALIF');
    });

    it('validates Schwab ++ (Severe Mismatch): PI - LL > 20°, PT > 30°, SVA > 95 mm -> Pedicle Subtraction (PSO / Schwab III) & VCR', () => {
      // PI = 65°, PT = 35°, SS = 30°, LL = 35° (PI - LL = 30°), SVA = 110 mm
      const res = calculateSagittalBalance({
        pi: 65,
        pt: 35,
        ss: 30,
        ll: 35,
        sva: 110
      });

      expect(res.rawScore).toBe(30); // PI - LL = 30°
      expect(res.scoreFormatted).toContain('Schwab ++');
      expect(res.scoreFormatted).toContain('PT: Severe retroversion');
      expect(res.scoreFormatted).toContain('SVA: Severe');
      expect(res.activeRiskTier.severityLevel).toBe('critical');
      expect(res.activeRiskTier.label).toContain('Deformidade Sagital Grave');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Osteotomia de Subtração Pedicular (PSO / Schwab Grau III)'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Vertebrectomia / Ressecção de Coluna Vertebral (VCR / Schwab Grau VI)'
      );
    });
  });

  // ==========================================================================
  // 7. PHASES ANEURYSM RUPTURE RISK SCORE
  // ==========================================================================
  describe('7. PHASES Aneurysm Score & 5-Year Rupture Probability (`calc_phases_score`)', () => {

    it('validates Rupture Risk Tier <= 3: Conservative Safe Management (0.4% - 0.7%)', () => {
      // Score 0: Other pop (0), no HTN (0), age <70 (0), size <7mm (0), no SAH (0), ICA (0) = 0 pts -> 0.4%
      const res0 = calculatePhasesScore({
        population: 'other',
        hypertension: false,
        age: 50,
        size: 5.0,
        earlierSah: false,
        site: 'ica'
      });
      expect(res0.rawScore).toBe(0);
      expect(res0.scoreFormatted).toContain('0 pontos (Risco 5 anos: 0.4%)');
      expect(res0.activeRiskTier.severityLevel).toBe('low');
      expect(res0.activeRiskTier.label).toContain('Baixo Risco de Ruptura (0 a 3 pontos)');
      expect(res0.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Tratamento Conservador Seguro de Escolha'
      );
      expect(res0.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cessação mandatória do tabagismo'
      );

      // Score 3: Japan pop (3 pts) + others 0 = 3 pts -> 0.7% (boundary)
      const res3 = calculatePhasesScore({
        population: 'japan',
        hypertension: false,
        age: 55,
        size: 4.0,
        earlierSah: false,
        site: 'ica'
      });
      expect(res3.rawScore).toBe(3);
      expect(res3.scoreFormatted).toContain('3 pontos (Risco 5 anos: 0.7%)');
      expect(res3.activeRiskTier.severityLevel).toBe('low');
    });

    it('validates Rupture Risk Tier 4 to 7: Borderline / Shared Decision Making (0.9% - 4.3%)', () => {
      // Score 4: Other (0) + HTN (1) + Size 8mm (3) = 4 pts -> 0.9% (lower boundary)
      const res4 = calculatePhasesScore({
        population: 'other',
        hypertension: true,
        age: 60,
        size: 8.0,
        earlierSah: false,
        site: 'ica'
      });
      expect(res4.rawScore).toBe(4);
      expect(res4.scoreFormatted).toContain('4 pontos (Risco 5 anos: 0.9%)');
      expect(res4.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res4.activeRiskTier.label).toContain('Risco Intermediário (4 a 7 pontos)');
      expect(res4.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Caso Limítrofe / Tomada de Decisão Compartilhada'
      );

      // Score 7: Finland pop (5) + MCA site (2) = 7 pts -> 2.4% (upper boundary of intermediate)
      const res7 = calculatePhasesScore({
        population: 'finland',
        hypertension: false,
        age: 55,
        size: 5.0,
        earlierSah: false,
        site: 'mca'
      });
      expect(res7.rawScore).toBe(7);
      expect(res7.scoreFormatted).toContain('7 pontos (Risco 5 anos: 2.4%)');
      expect(res7.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('validates Rupture Risk Tier >= 8: Mandatory Surgical / Interventional Indication', () => {
      // Score 8: Finland (5) + MCA (2) + HTN (1) = 8 pts -> 3.2% (surgical cutoff boundary)
      const res8 = calculatePhasesScore({
        population: 'finland',
        hypertension: true,
        age: 55,
        size: 5.0,
        earlierSah: false,
        site: 'mca'
      });
      expect(res8.rawScore).toBe(8);
      expect(res8.scoreFormatted).toContain('8 pontos (Risco 5 anos: 3.2%)');
      expect(res8.activeRiskTier.severityLevel).toBe('critical');
      expect(res8.activeRiskTier.label).toContain('Alto a Muito Alto Risco de Ruptura (8 a 22 pontos)');
      expect(res8.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Indicação Cirúrgica Mandatória / Tratamento Intervencionista Eletivo Ativo'
      );
      expect(res8.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Clipagem Microcirúrgica Aberta'
      );
      expect(res8.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Stent Diversor de Fluxo (Flow Diverter)'
      );

      // Score 22 (Maximum): Finland (5) + HTN (1) + Age >=70 (1) + Size >=20mm (10) + Prior SAH (1) + Posterior (4) = 22 pts -> > 17.8%
      const res22 = calculatePhasesScore({
        population: 'finland',
        hypertension: true,
        age: 75,
        size: 25.0,
        earlierSah: true,
        site: 'posterior'
      });
      expect(res22.rawScore).toBe(22);
      expect(res22.scoreFormatted).toContain('22 pontos (Risco 5 anos: > 17.8%)');
      expect(res22.activeRiskTier.severityLevel).toBe('critical');
    });
  });

  // ==========================================================================
  // 8. LAWTON-YOUNG SUPPLEMENTARY AVM GRADING SYSTEM
  // ==========================================================================
  describe('8. Lawton-Young Combined Spetzler-Martin Score (`calc_lawton_young`)', () => {

    it('validates Combined Score 2-4: Low Surgical Risk (Primary Microsurgical Resection)', () => {
      // SM: Size < 3cm (1) + Non-eloquent (0) + Superficial (0) = 1 pt
      // LY: Age < 20 (1) + Ruptured (0) + Compact (0) = 1 pt -> Combined = 2 pts
      const res2 = calculateLawtonYoung({
        sm_size: '<3',
        sm_eloquence: false,
        sm_drainage: false,
        age: 18,
        ruptured: true,
        compactness: 'compact'
      });
      expect(res2.rawScore).toBe(2);
      expect(res2.scoreFormatted).toBe('2 pontos (SM 1 + LY 1)');
      expect(res2.activeRiskTier.severityLevel).toBe('low');
      expect(res2.activeRiskTier.label).toContain('Baixa Complexidade Cirúrgica / Baixo Risco');
      expect(res2.activeRiskTier.statisticalOutcome).toContain('< 3% a 5%');
      expect(res2.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Indicação Cirúrgica Mandatória / Eletiva de Ressecção Microcirúrgica Primária Completa'
      );

      // Boundary: Combined = 4 pts
      const res4 = calculateLawtonYoung({
        spetzlerMartin: 2,
        age: 25, // +2
        ruptured: true, // +0
        compactness: 'compact' // +0
      });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.severityLevel).toBe('low');
    });

    it('validates Combined Score 5-6: Intermediate Complexity (Multimodal Planning)', () => {
      // Combined = 5 pts (lower boundary)
      const res5 = calculateLawtonYoung({
        spetzlerMartin: 3,
        age: 25, // +2
        ruptured: true, // +0
        compactness: 'compact' // +0
      });
      expect(res5.rawScore).toBe(5);
      expect(res5.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res5.activeRiskTier.label).toContain('Complexidade Cirúrgica Intermediária');
      expect(res5.activeRiskTier.statisticalOutcome).toContain('10% a 25%');
      expect(res5.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Embolização superseletiva pré-operatória'
      );
      expect(res5.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Radiocirurgia Estereotática (SRS: 18 a 22 Gy)'
      );

      // Combined = 6 pts (upper boundary)
      const res6 = calculateLawtonYoung({
        spetzlerMartin: 3,
        age: 45, // +3
        ruptured: true, // +0
        compactness: 'compact' // +0
      });
      expect(res6.rawScore).toBe(6);
      expect(res6.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('validates Combined Score 7-10: High / Prohibitive Risk (ARUBA Trial Conservative Management)', () => {
      // Combined = 7 pts (boundary)
      const res7 = calculateLawtonYoung({
        spetzlerMartin: 4,
        age: 45, // +3
        ruptured: true,
        compactness: 'compact'
      });
      expect(res7.rawScore).toBe(7);
      expect(res7.activeRiskTier.severityLevel).toBe('critical');
      expect(res7.activeRiskTier.label).toContain('Alta Complexidade / Risco Cirúrgico Proibitivo');
      expect(res7.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Tratamento Conservador Seguro / Manejo Clínico Expectante (Diretrizes do Ensaio Clínico ARUBA)'
      );
      expect(res7.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Microcirurgia aberta formalmente contraindicada'
      );

      // Combined = 10 pts (maximum derangement)
      const res10 = calculateLawtonYoung({
        spetzlerMartin: 5,
        age: 65, // +3
        unruptured: true, // +1
        compactness: 'diffuse' // +1
      });
      expect(res10.rawScore).toBe(10);
      expect(res10.activeRiskTier.severityLevel).toBe('critical');
    });
  });

  // ==========================================================================
  // 9. ZABRAMSKI CAVERNOMA CLASSIFICATION
  // ==========================================================================
  describe('9. Zabramski Cavernoma Classification (`calc_zabramski`)', () => {
    const zabramski = getTool('calc_zabramski');

    it('validates Type I & II (Active Bleeding / Popcorn): Resection of Nidus + Hemosiderin Rim', () => {
      // Type I: Subacute recent hemorrhage (methemoglobin)
      const res1 = calculateScore(zabramski, { grp_zabramski_type: 'opt_zab_1' });
      expect(res1.rawScore).toBe(1);
      expect(res1.activeRiskTier.id).toBe('tier_zab_active');
      expect(res1.activeRiskTier.severityLevel).toBe('high');
      expect(res1.activeRiskTier.statisticalOutcome).toContain('4% a 10% ao ano');
      expect(res1.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Indicação Cirúrgica Mandatória / Eletiva de Ressecção Microcirúrgica Completa'
      );
      expect(res1.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'remoção circunferencial do anel gliótico de hemossiderina (hemosiderin rim resection)'
      );

      // Type II: Classic popcorn lesion with thick hemosiderin ring
      const res2 = calculateScore(zabramski, { grp_zabramski_type: 'opt_zab_2' });
      expect(res2.rawScore).toBe(2);
      expect(res2.activeRiskTier.id).toBe('tier_zab_active');
      expect(res2.activeRiskTier.severityLevel).toBe('high');
    });

    it('validates Type III: Inactive Chronic Hemosiderin Deposit (Safe Conservative Follow-up)', () => {
      const res3 = calculateScore(zabramski, { grp_zabramski_type: 'opt_zab_3' });
      expect(res3.rawScore).toBe(3);
      expect(res3.activeRiskTier.id).toBe('tier_zab_inactive');
      expect(res3.activeRiskTier.severityLevel).toBe('low');
      expect(res3.activeRiskTier.label).toContain('Tipo III: Lesão Inativa Estável');
      expect(res3.activeRiskTier.statisticalOutcome).toContain('< 0,5% a 1% ao ano');
      expect(res3.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia não indicada'
      );
    });

    it('validates Type IV: Multiple Familial CCM (Radiosurgery Strictly Contraindicated)', () => {
      const res4 = calculateScore(zabramski, { grp_zabramski_type: 'opt_zab_4' });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_zab_familiar');
      expect(res4.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res4.activeRiskTier.label).toContain('Tipo IV: Cavernomatose Múltipla Familiar');
      expect(res4.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'PROIBIDA RADIOCIRURGIA'
      );
      expect(zabramski.clinicalWarning).toContain('Contraindicação a Radiocirurgia no Tipo IV familiar');
      expect(zabramski.clinicalWarning).toContain('indução acelerada de lesões cavernosas de novo');
    });

    it('enforces mandatory safety alert: strict DVA preservation to prevent venous infarction', () => {
      expect(zabramski.clinicalWarning).toContain('Preservação da Anomalia de Desenvolvimento Venoso (DVA)');
      expect(zabramski.clinicalWarning).toContain('terminantemente proibida a coagulação ou sacrifício da veia');
      expect(zabramski.clinicalWarning).toContain('infarto venoso hemorrágico catastrófico');
    });
  });

  // ==========================================================================
  // 10. VASOGRADE: BIVARIATE DELAYED CEREBRAL ISCHEMIA RISK
  // ==========================================================================
  describe('10. Vasograde DCI Risk Stratification (`calc_vasograde`)', () => {
    const vasograde = getTool('calc_vasograde');

    it('validates Vasograde-Green: WFNS 1-2 + Modified Fisher 0-2 (Low DCI Risk 15-20%)', () => {
      const res = calculateScore(vasograde, { grp_vasograde_category: 'opt_vaso_green' });
      expect(res.rawScore).toBe(1);
      expect(res.activeRiskTier.id).toBe('tier_vaso_green');
      expect(res.activeRiskTier.severityLevel).toBe('low');
      expect(res.activeRiskTier.label).toContain('Vasograde-Green: Baixo Risco de DCI');
      expect(res.activeRiskTier.statisticalOutcome).toContain('15% a 20%');
      expect(res.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Nimodipino Oral / Enteral');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].monitoringPlan).toContain('Doppler Transcraniano');
    });

    it('validates Vasograde-Yellow: WFNS 1-3 + Modified Fisher 3-4 (Intermediate DCI Risk 30-35%)', () => {
      const res = calculateScore(vasograde, { grp_vasograde_category: 'opt_vaso_yellow' });
      expect(res.rawScore).toBe(2);
      expect(res.activeRiskTier.id).toBe('tier_vaso_yellow');
      expect(res.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res.activeRiskTier.label).toContain('Vasograde-Yellow: Risco Intermediário de DCI');
      expect(res.activeRiskTier.statisticalOutcome).toContain('30% a 35%');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].monitoringPlan).toContain('a cada 12-24h');
      expect(res.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Noradrenalina IV (Preparo para Hipertensão Induzida)');
    });

    it('validates Vasograde-Red: WFNS 4-5 Any Fisher (Critical DCI Risk 40-50% & Urgent Bedside EVD)', () => {
      const res = calculateScore(vasograde, { grp_vasograde_category: 'opt_vaso_red' });
      expect(res.rawScore).toBe(3);
      expect(res.activeRiskTier.id).toBe('tier_vaso_red');
      expect(res.activeRiskTier.severityLevel).toBe('critical');
      expect(res.activeRiskTier.label).toContain('Vasograde-Red: Alto Risco de DCI e Mau Prognóstico');
      expect(res.activeRiskTier.statisticalOutcome).toContain('40% a 50%');
      expect(res.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Indicação Cirúrgica Mandatória: DVE Emergencial + Oclusão Mecânica do Aneurisma'
      );
      expect(res.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Implantação emergencial de Derivação Ventricular Externa (DVE) à beira do leito'
      );
    });

    it('enforces mandatory safety black box: IV Nimodipine strictly prohibited', () => {
      expect(vasograde.clinicalWarning).toContain('ALERTA PRETO DE SEGURANÇA MANDATÓRIO');
      expect(vasograde.clinicalWarning).toContain('TERMINANTEMENTE PROIBIDA');
      expect(vasograde.clinicalWarning).toContain('colapso cardiovascular');
      expect(vasograde.clinicalWarning).toContain('hipertensão com Noradrenalina está proscrita antes da oclusão definitiva');
    });
  });

  // ==========================================================================
  // 11. KNOSP CLASSIFICATION: PITUITARY ADENOMA CAVERNOUS SINUS INVASION
  // ==========================================================================
  describe('11. Knosp Pituitary Adenoma Invasion (`calc_knosp`)', () => {
    const knosp = getTool('calc_knosp');

    it('validates Grades 0 to 2: EETS Feasible with High Gross Total Resection (GTR) Rates', () => {
      // Grade 0: Medial to medial tangent (100% GTR feasible)
      const res0 = calculateScore(knosp, { grp_knosp_grade: 'opt_knosp_0' });
      expect(res0.rawScore).toBe(0);
      expect(res0.activeRiskTier.id).toBe('tier_knosp_low');
      expect(res0.activeRiskTier.severityLevel).toBe('low');
      expect(res0.activeRiskTier.statisticalOutcome).toContain('95% a 100%');
      expect(res0.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain('Cirurgia Endoscópica Transesfenoidal (EETS)');

      // Grade 1: Medial to intercarotid line
      const res1 = calculateScore(knosp, { grp_knosp_grade: 'opt_knosp_1' });
      expect(res1.rawScore).toBe(1);
      expect(res1.activeRiskTier.id).toBe('tier_knosp_low');

      // Grade 2: Crosses intercarotid, medial to lateral tangent (GTR 75-85% feasible with microdoppler)
      const res2 = calculateScore(knosp, { grp_knosp_grade: 'opt_knosp_2' });
      expect(res2.rawScore).toBe(2);
      expect(res2.activeRiskTier.id).toBe('tier_knosp_mod');
      expect(res2.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res2.activeRiskTier.statisticalOutcome).toContain('75% a 85%');
      expect(res2.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain('Microdoppler Vascular e Monitorização Selar');
    });

    it('validates Grades 3A/3B & 4: Cavernous Invasion, Intentional Subtotal Resection + SRS', () => {
      // Grade 3A: Crosses lateral tangent superiorly
      const res3a = calculateScore(knosp, { grp_knosp_grade: 'opt_knosp_3a' });
      expect(res3a.rawScore).toBe(3);
      expect(res3a.activeRiskTier.id).toBe('tier_knosp_high');
      expect(res3a.activeRiskTier.severityLevel).toBe('high');
      expect(res3a.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Ressecção Subtotal + Radiocirurgia Estereotáxica (SRS)'
      );
      expect(res3a.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Ressecção subtotal intencional visando descompressão quiasmática ampla e preservação estrita da integridade carotídea'
      );

      // Grade 4: 360° total circumferential encasement of cavernous ICA
      const res4 = calculateScore(knosp, { grp_knosp_grade: 'opt_knosp_4' });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_knosp_encased');
      expect(res4.activeRiskTier.severityLevel).toBe('critical');
      expect(res4.activeRiskTier.statisticalOutcome).toContain('Invasão dural e intracavernosa de 100%');
      expect(res4.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'suspensão de dissecção na carótida, encaminhando para radioterapia'
      );
    });
  });

  // ==========================================================================
  // 12. SAMII & KOOS CLASSIFICATION: VESTIBULAR SCHWANNOMAS
  // ==========================================================================
  describe('12. Samii & Koos Vestibular Schwannoma Staging (`calc_samii_koos`)', () => {
    const samiiKoos = getTool('calc_samii_koos');

    it('validates Koos I-III (Samii T1-T3): Hearing Preservation, Wait-and-Scan or Elective Microsurgery', () => {
      // Koos I (Samii T1): Pure intrameatal (< 10 mm)
      const res1 = calculateScore(samiiKoos, { grp_koos_grade: 'opt_koos_1' });
      expect(res1.rawScore).toBe(1);
      expect(res1.activeRiskTier.id).toBe('tier_koos_1');
      expect(res1.activeRiskTier.severityLevel).toBe('low');
      expect(res1.activeRiskTier.statisticalOutcome).toContain('98% a 100%');
      expect(res1.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain('Wait-and-Scan');

      // Koos II (Samii T2): Small cisternal (<= 20 mm)
      const res2 = calculateScore(samiiKoos, { grp_koos_grade: 'opt_koos_2' });
      expect(res2.rawScore).toBe(2);
      expect(res2.activeRiskTier.id).toBe('tier_koos_2');
      expect(res2.activeRiskTier.severityLevel).toBe('intermediate');
      expect(res2.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain('Radiocirurgia Estereotáxica (SRS)');

      // Koos III (Samii T3a/b): Contact with brainstem without displacement (<= 30 mm)
      const res3 = calculateScore(samiiKoos, { grp_koos_grade: 'opt_koos_3' });
      expect(res3.rawScore).toBe(3);
      expect(res3.activeRiskTier.id).toBe('tier_koos_3');
      expect(res3.activeRiskTier.severityLevel).toBe('high');
      expect(res3.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain('Microcirurgia Retrosigmoidea com MIO Contínua');
    });

    it('validates Koos IV (Samii T4b): Giant Tumor (> 30 mm) with Brainstem Compression & Urgent DVE Requirement', () => {
      const res4 = calculateScore(samiiKoos, { grp_koos_grade: 'opt_koos_4' });
      expect(res4.rawScore).toBe(4);
      expect(res4.activeRiskTier.id).toBe('tier_koos_4');
      expect(res4.activeRiskTier.severityLevel).toBe('critical');
      expect(res4.activeRiskTier.label).toContain('Compressão Grave de Tronco e 4º Ventrículo');
      expect(res4.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Descompressão Microcirúrgica de Fossa Posterior + DVE de Resgate'
      );
      expect(res4.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'instalação de DVE se ventrículos dilatados pré-operatórios'
      );
      expect(samiiKoos.clinicalWarning).toContain('Derivação Ventricular Externa (DVE) de emergência');
    });
  });

  // ==========================================================================
  // 13. KIEFER SCALE & EVANS / DESH: NORMAL PRESSURE HYDROCEPHALUS
  // ==========================================================================
  describe('13. Kiefer Scale & Evans/DESH Hydrocephalus Differential (`calc_kiefer` & `calc_evans_desh`)', () => {
    const kiefer = getTool('calc_kiefer');
    const evansDesh = getTool('calc_evans_desh');

    it('validates Kiefer Scale clinical ranges and Tap Test improvement threshold (delta >= 2 pts)', () => {
      expect(kiefer.id).toBe('calc_kiefer');
      expect(kiefer.minPossibleScore).toBe(0);
      expect(kiefer.maxPossibleScore).toBe(24);
      expect(kiefer.riskTiers.length).toBe(3);

      // Mild (0-4 pts)
      const resMild = calculateScore(kiefer, {
        grp_kiefer_gait: 'opt_kg_2', // 2
        grp_kiefer_cognitive: 'opt_kc_1' // 1 -> total = 3
      });
      expect(resMild.rawScore).toBe(3);
      expect(resMild.activeRiskTier.id).toBe('tier_kiefer_mild');
      expect(resMild.activeRiskTier.severityLevel).toBe('low');

      // Moderate classic Hakim-Adams (5-11 pts)
      const resMod = calculateScore(kiefer, {
        grp_kiefer_gait: 'opt_kg_3',      // 3 (cane)
        grp_kiefer_cognitive: 'opt_kc_3', // 3 (apathy/supervision)
        grp_kiefer_sphincter: 'opt_ks_2'  // 2 (nocturnal/episodic) -> total = 8
      });
      expect(resMod.rawScore).toBe(8);
      expect(resMod.activeRiskTier.id).toBe('tier_kiefer_mod');
      expect(resMod.activeRiskTier.severityLevel).toBe('intermediate');
      expect(resMod.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Derivação Ventriculoperitoneal (DVP) com Válvula Programável'
      );

      // Severe / Advanced (12-24 pts)
      const resSev = calculateScore(kiefer, {
        grp_kiefer_gait: 'opt_kg_5',      // 5
        grp_kiefer_cognitive: 'opt_kc_4', // 4
        grp_kiefer_sphincter: 'opt_ks_3', // 3
        grp_kiefer_headache: 'opt_kh_2'   // 2 -> total = 14
      });
      expect(resSev.rawScore).toBe(14);
      expect(resSev.activeRiskTier.id).toBe('tier_kiefer_sev');
      expect(resSev.activeRiskTier.severityLevel).toBe('high');

      // Clinical warning must mandate delta >= 2 pts improvement and gravitational valve
      expect(kiefer.clinicalWarning).toContain('melhora de pelo menos 2 pontos na Escala de Kiefer');
      expect(kiefer.clinicalWarning).toContain('válvula regulável com mecanismo gravitacional ou anti-sifão');
    });

    it('validates Evans >= 0.30 + DESH Positive + Acute Callosal Angle (<90°) -> VPS with programmable gravitational valve (>85-92% response)', () => {
      // Full typical DESH pattern:
      // Evans >= 0.30 (3 pts) + Classic DESH tight vertex/dilated Sylvian (3 pts) + Acute callosal angle <90° (2 pts) + Edema (2 pts) = 10 pts
      const resDesh = calculateScore(evansDesh, {
        grp_evans_index: 'opt_evans_enlarged',
        grp_desh_pattern: 'opt_desh_classic',
        grp_callosal_angle: 'opt_angle_acute',
        grp_periventricular_edema: 'opt_edema_present'
      });

      expect(resDesh.rawScore).toBe(10);
      expect(resDesh.activeRiskTier.id).toBe('tier_ed_classic');
      expect(resDesh.activeRiskTier.severityLevel).toBe('critical');
      expect(resDesh.activeRiskTier.label).toContain('Padrão DESH Típico / Altíssima Probabilidade de Resposta à DVP');
      expect(resDesh.activeRiskTier.statisticalOutcome).toContain('> 85% a 92%');
      expect(resDesh.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Cirurgia de DVP com Válvula Programável Anti-Sifão'
      );
      expect(resDesh.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'válvula programável gravitacional ajustada para nível pressórico inicial de 100-120 mmH2O'
      );
    });

    it('validates Alzheimer Atrophy Ex-Vacuo differential (wide vertex sulci, obtuse callosal angle > 100°) -> VPS strictly contraindicated', () => {
      // Ex-vacuo pattern:
      // Normal Evans <0.30 (0 pt) + Absent DESH / wide diffuse vertex sulci (0 pt) + Obtuse callosal angle >=100° (0 pt) + Edema absent (0 pt) = 0 pts
      const resAtrophy = calculateScore(evansDesh, {
        grp_evans_index: 'opt_evans_normal',
        grp_desh_pattern: 'opt_desh_none',
        grp_callosal_angle: 'opt_angle_wide',
        grp_periventricular_edema: 'opt_edema_absent'
      });

      expect(resAtrophy.rawScore).toBe(0);
      expect(resAtrophy.activeRiskTier.id).toBe('tier_ed_unlikely');
      expect(resAtrophy.activeRiskTier.severityLevel).toBe('low');
      expect(resAtrophy.activeRiskTier.label).toContain('Baixa Probabilidade de HPN Responsiva (Atrofia ex-vacuo)');
      expect(resAtrophy.activeRiskTier.statisticalOutcome).toContain('Taxa de resposta à DVP < 15-20%');
      expect(resAtrophy.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Cloridrato de Donepezila');
      expect(resAtrophy.activeRiskTier.nonPharmacologicalActions[0].recommendationTitle).toContain(
        'Investigação com Biomarcadores Liquóricos de Alzheimer'
      );
    });
  });

});
