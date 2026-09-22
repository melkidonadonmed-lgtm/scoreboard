import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';
import {
  ManifestSchema,
  BlockDataSchema,
  CalculatorSchema,
  type Manifest,
  type BlockData
} from '@/types/clinical';
import {
  InfusionProtocolSchema,
  SolutionRecipeSchema
} from '@/types/infusion';

import rawManifestData from '@/data/manifest.json';
import rawBlock01Data from '@/data/blocks/block_01.json';

describe('Milestone 2 Contract & Schema Verification', () => {
  const parsedManifest: Manifest = ManifestSchema.parse(rawManifestData);
  const parsedBlock01: BlockData = BlockDataSchema.parse(rawBlock01Data);

  describe('Lightweight Manifest Contract (`src/data/manifest.json`)', () => {
    it('should strictly validate the entire manifest against ManifestSchema', () => {
      const parseResult = ManifestSchema.safeParse(rawManifestData);
      expect(parseResult.success).toBe(true);
    });

    it('should contain all 19 clinical tools of Block 01', () => {
      expect(parsedManifest).toHaveLength(19);
    });

    it('should have lightweight manifest size (~30KB)', () => {
      const manifestPath = path.resolve(__dirname, '../../src/data/manifest.json');
      const stats = fs.statSync(manifestPath);
      const sizeKb = stats.size / 1024;
      // Should be around ~30KB (between 20KB and 50KB)
      expect(sizeKb).toBeGreaterThanOrEqual(20);
      expect(sizeKb).toBeLessThanOrEqual(50);
    });

    it('should provide extensive Brazilian clinical search synonyms for all tools', () => {
      for (const item of parsedManifest) {
        expect(item.searchSynonyms.length).toBeGreaterThanOrEqual(10);
        expect(item.blockFile).toBe('block_01.json');
        expect(item.categorySlug).toBe('bloco-01-emergencia-choque-uti');
      }

      // Check specific clinical synonyms
      const qsofa = parsedManifest.find((item) => item.id === 'calc_qsofa');
      expect(qsofa?.searchSynonyms).toContain('sepse');
      expect(qsofa?.searchSynonyms).toContain('choque septico');

      const wells = parsedManifest.find((item) => item.id === 'calc_wells_tep');
      expect(wells?.searchSynonyms).toContain('tromboembolismo pulmonar');
      expect(wells?.searchSynonyms).toContain('tep');

      const glasgow = parsedManifest.find((item) => item.id === 'calc_glasgow_p');
      expect(glasgow?.searchSynonyms).toContain('tce');
      expect(glasgow?.searchSynonyms).toContain('coma');

      const bisap = parsedManifest.find((item) => item.id === 'calc_bisap');
      expect(bisap?.searchSynonyms).toContain('pancreatite');
      expect(bisap?.searchSynonyms).toContain('ureia');
    });

    it('should include starred defaults for primary emergency tools', () => {
      const starred = parsedManifest.filter((i) => i.starredDefault);
      const starredIds = starred.map((i) => i.id);
      expect(starredIds).toContain('calc_qsofa');
      expect(starredIds).toContain('calc_sofa');
      expect(starredIds).toContain('calc_wells_tep');
      expect(starredIds).toContain('calc_glasgow_p');
      expect(starredIds).toContain('calc_bisap');
    });
  });

  describe('Block 01 Ingestion Contract (`src/data/blocks/block_01.json`)', () => {
    it('should strictly validate the entire Block 01 against BlockDataSchema', () => {
      const parseResult = BlockDataSchema.safeParse(rawBlock01Data);
      expect(parseResult.success).toBe(true);
    });

    it('should validate individual calculators with CalculatorSchema', () => {
      for (const calc of parsedBlock01.calculators) {
        const result = CalculatorSchema.safeParse(calc);
        expect(result.success).toBe(true);
      }
    });

    it('should contain all 19 calculators with complete zero-truncation dossiers', () => {
      expect(parsedBlock01.blockId).toBe('block_01');
      expect(parsedBlock01.calculators).toHaveLength(19);

      // Verify bidirectional ID alignment between manifest and block
      const manifestIds = parsedManifest.map((m) => m.id).sort();
      const blockIds = parsedBlock01.calculators.map((c) => c.id).sort();
      expect(manifestIds).toEqual(blockIds);
    });

    it('should enforce qSOFA with mandatory Surviving Sepsis Campaign 2021 warning', () => {
      const qsofa = parsedBlock01.calculators.find((c) => c.id === 'calc_qsofa');
      expect(qsofa).toBeDefined();
      expect(qsofa?.ssc2021Warning).toBe(true);
      expect(qsofa?.clinicalWarning).toBeDefined();
      expect(qsofa?.clinicalWarning).toContain('Surviving Sepsis Campaign (SSC 2021)');
      expect(qsofa?.clinicalWarning).toContain('sensibilidade insuficiente (< 60%)');
      expect(qsofa?.minPossibleScore).toBe(0);
      expect(qsofa?.maxPossibleScore).toBe(3);
      expect(qsofa?.parameterGroups).toHaveLength(3);
      expect(qsofa?.radarAxes).toHaveLength(3);

      // High risk tier must have Norepinephrine protocol
      const highTier = qsofa?.riskTiers.find((t) => t.severityLevel === 'critical');
      expect(highTier).toBeDefined();
      expect(highTier?.infusionProtocol).toBeDefined();
      expect(highTier?.infusionProtocol?.drugName).toContain('Noradrenalina');
      expect(highTier?.infusionProtocol?.standardSolution.diluent).toContain('SG 5%');
    });

    it('should enforce Full SOFA across all 6 organ systems with 0-24 points', () => {
      const sofa = parsedBlock01.calculators.find((c) => c.id === 'calc_sofa');
      expect(sofa).toBeDefined();
      expect(sofa?.minPossibleScore).toBe(0);
      expect(sofa?.maxPossibleScore).toBe(24);
      expect(sofa?.parameterGroups).toHaveLength(6);
      expect(sofa?.radarAxes).toHaveLength(6);

      const groupSlugs = sofa?.parameterGroups.map((g) => g.slug);
      expect(groupSlugs).toContain('sistema-respiratorio');
      expect(groupSlugs).toContain('sistema-coagulacao');
      expect(groupSlugs).toContain('sistema-hepatico');
      expect(groupSlugs).toContain('sistema-cardiovascular');
      expect(groupSlugs).toContain('sistema-nervoso');
      expect(groupSlugs).toContain('sistema-renal');

      // Verify respiratory group has PaO2/FiO2 ventilation criteria
      const respGroup = sofa?.parameterGroups.find((g) => g.slug === 'sistema-respiratorio');
      expect(respGroup?.options).toHaveLength(5);
      const ventilatedOptions = respGroup?.options.filter((o) => o.label.includes('suporte ventilatório'));
      expect(ventilatedOptions?.length).toBeGreaterThanOrEqual(2);

      // Cardiovascular tier must have Norepinephrine & Vasopressin protocols
      const criticalTier = sofa?.riskTiers.find((t) => t.id === 'tier_sofa_2');
      expect(criticalTier?.infusionProtocol?.drugName).toContain('Noradrenalina');
    });

    it('should enforce Wells TEP with 7 criteria and dichotomous/3-tier stratification', () => {
      const wells = parsedBlock01.calculators.find((c) => c.id === 'calc_wells_tep');
      expect(wells).toBeDefined();
      expect(wells?.minPossibleScore).toBe(0);
      expect(wells?.maxPossibleScore).toBe(12.5);
      expect(wells?.parameterGroups).toHaveLength(7);

      // Check criteria point values
      const tvpGroup = wells?.parameterGroups.find((g) => g.slug === 'sinais-tvp');
      expect(tvpGroup?.options.find((o) => o.pointValue === 3.0)).toBeDefined();

      const hrGroup = wells?.parameterGroups.find((g) => g.slug === 'taquicardia');
      expect(hrGroup?.options.find((o) => o.pointValue === 1.5)).toBeDefined();

      const hemoptGroup = wells?.parameterGroups.find((g) => g.slug === 'hemoptise');
      expect(hemoptGroup?.options.find((o) => o.pointValue === 1.0)).toBeDefined();

      // Check risk tiers
      const unlikelyTier = wells?.riskTiers.find((t) => t.id === 'tier_wtep_unlikely');
      expect(unlikelyTier?.maxScore).toBe(4.0);
      expect(unlikelyTier?.nonPharmacologicalActions[0].monitoringPlan).toContain('PERC');
      expect(unlikelyTier?.nonPharmacologicalActions[0].monitoringPlan).toContain('D-Dímero');

      const likelyTier = wells?.riskTiers.find((t) => t.id === 'tier_wtep_likely');
      expect(likelyTier?.minScore).toBe(4.5);
      expect(likelyTier?.pharmacologicalActions[0].drugName).toContain('Enoxaparina');
    });

    it('should enforce Glasgow-P with branching/decision and pupil score subtraction (1-15 pts)', () => {
      const glasgowP = parsedBlock01.calculators.find((c) => c.id === 'calc_glasgow_p');
      expect(glasgowP).toBeDefined();
      expect(glasgowP?.calculationType).toBe('branching_decision');
      expect(glasgowP?.minPossibleScore).toBe(1);
      expect(glasgowP?.maxPossibleScore).toBe(15);
      expect(glasgowP?.parameterGroups).toHaveLength(4);

      // Check pupil reactivity group
      const pupilGroup = glasgowP?.parameterGroups.find((g) => g.slug === 'reatividade-pupilar');
      expect(pupilGroup).toBeDefined();
      expect(pupilGroup?.options).toHaveLength(3);
      const pointValues = pupilGroup?.options.map((o) => o.pointValue);
      expect(pointValues).toEqual([0, 1, 2]);

      // Check severe tier (1 to 8 pts) with IOT and neuroprotection
      const severeTier = glasgowP?.riskTiers.find((t) => t.id === 'tier_gp_severe');
      expect(severeTier?.minScore).toBe(1);
      expect(severeTier?.maxScore).toBe(8);
      expect(severeTier?.pharmacologicalActions[0].drugName).toContain('Sequência Rápida de Intubação');
    });

    it('should enforce FOUR Score across all 4 axes of 0-4 points (0-16 pts)', () => {
      const four = parsedBlock01.calculators.find((c) => c.id === 'calc_four');
      expect(four).toBeDefined();
      expect(four?.minPossibleScore).toBe(0);
      expect(four?.maxPossibleScore).toBe(16);
      expect(four?.parameterGroups).toHaveLength(4);
      expect(four?.radarAxes).toHaveLength(4);

      for (const group of four?.parameterGroups || []) {
        expect(group.options).toHaveLength(5); // 0, 1, 2, 3, 4
      }

      const criticalTier = four?.riskTiers.find((t) => t.id === 'tier_four_low_score');
      expect(criticalTier?.minScore).toBe(0);
      expect(criticalTier?.maxScore).toBe(7);
      expect(criticalTier?.nonPharmacologicalActions[0].monitoringPlan).toContain('Morte Encefálica');
    });

    it('should enforce Ranson (11 criteria) and BISAP with Brazilian BUN/Ureia conversion', () => {
      const ranson = parsedBlock01.calculators.find((c) => c.id === 'calc_ranson');
      expect(ranson).toBeDefined();
      expect(ranson?.minPossibleScore).toBe(0);
      expect(ranson?.maxPossibleScore).toBe(11);
      expect(ranson?.parameterGroups).toHaveLength(11);

      const bisap = parsedBlock01.calculators.find((c) => c.id === 'calc_bisap');
      expect(bisap).toBeDefined();
      expect(bisap?.minPossibleScore).toBe(0);
      expect(bisap?.maxPossibleScore).toBe(5);
      expect(bisap?.parameterGroups).toHaveLength(5);

      // Verify Brazilian Ureia conversion in BUN group
      const bunGroup = bisap?.parameterGroups.find((g) => g.slug === 'bun-ureia');
      expect(bunGroup?.helpText).toContain('Ureia > 53,5 mg/dL');
      expect(bunGroup?.options[1].label).toContain('53,5 mg/dL');
    });
  });

  describe('Infusion Protocols Validation', () => {
    it('should validate Norepinephrine standard and concentrated solutions', () => {
      const qsofa = parsedBlock01.calculators.find((c) => c.id === 'calc_qsofa');
      const highTier = qsofa?.riskTiers.find((t) => t.severityLevel === 'critical');
      const protocol = highTier?.infusionProtocol;

      expect(protocol).toBeDefined();
      const parseResult = InfusionProtocolSchema.safeParse(protocol);
      expect(parseResult.success).toBe(true);

      // Solution recipe schema validation
      if (protocol) {
        expect(SolutionRecipeSchema.safeParse(protocol.standardSolution).success).toBe(true);
        if (protocol.concentratedSolution) {
          expect(SolutionRecipeSchema.safeParse(protocol.concentratedSolution).success).toBe(true);
        }
      }

      // Exact recipe assertions
      expect(protocol?.standardSolution.concentrationMcgMl).toBe(64);
      expect(protocol?.standardSolution.totalVolumeMl).toBe(250);
      expect(protocol?.standardSolution.diluent).toContain('SG 5%');
      expect(protocol?.standardSolution.mandatoryVehicleNotice).toContain('SG 5%');

      expect(protocol?.concentratedSolution?.concentrationMcgMl).toBe(128);
      expect(protocol?.concentratedSolution?.totalVolumeMl).toBe(250);
      expect(protocol?.doseUnit).toBe('mcg/kg/min');
      expect(protocol?.nursingPrecautions).toContain('Vasopressina');
      expect(protocol?.nursingPrecautions).toContain('0,25 mcg/kg/min');
    });

    it('should validate Vasopressin fixed dose protocol', () => {
      const sofa = parsedBlock01.calculators.find((c) => c.id === 'calc_sofa');
      const tier2 = sofa?.riskTiers.find((t) => t.id === 'tier_sofa_2');
      const vasoAction = tier2?.pharmacologicalActions.find((a) => a.drugName.includes('Vasopressina'));

      expect(vasoAction?.infusionProtocol).toBeDefined();
      const protocol = vasoAction?.infusionProtocol;
      expect(protocol?.doseUnit).toBe('UI/min');
      expect(protocol?.isFixedDose).toBe(true);
      expect(protocol?.defaultDose).toBe(0.03);
      expect(protocol?.maintenanceDoseMin).toBe(0.01);
      expect(protocol?.maintenanceDoseMax).toBe(0.04);
      expect(protocol?.standardSolution.totalVolumeMl).toBe(100);
      expect(protocol?.nursingPrecautions).toContain('DOSE FIXA NÃO TITULÁVEL');
    });
  });
});
