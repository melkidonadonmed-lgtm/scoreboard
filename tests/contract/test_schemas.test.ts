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
import rawBlock03Data from '@/data/blocks/block_03.json';

describe('Milestone 2 Contract & Schema Verification', () => {
  const parsedManifest: Manifest = ManifestSchema.parse(rawManifestData);
  const parsedBlock01: BlockData = BlockDataSchema.parse(rawBlock01Data);
  const parsedBlock03: BlockData = BlockDataSchema.parse(rawBlock03Data);

  describe('Lightweight Manifest Contract (`src/data/manifest.json`)', () => {
    it('should strictly validate the entire manifest against ManifestSchema', () => {
      const parseResult = ManifestSchema.safeParse(rawManifestData);
      expect(parseResult.success).toBe(true);
    });

    it('should contain all clinical tools from available blocks (>= 19 tools)', () => {
      expect(parsedManifest.length).toBeGreaterThanOrEqual(19);
    });

    it('should have lightweight manifest size (~30KB-140KB)', () => {
      const manifestPath = path.resolve(__dirname, '../../src/data/manifest.json');
      const stats = fs.statSync(manifestPath);
      const sizeKb = stats.size / 1024;
      // Should be lightweight (between 20KB and 140KB for multi-block manifest)
      expect(sizeKb).toBeGreaterThanOrEqual(20);
      expect(sizeKb).toBeLessThanOrEqual(140);
    });

    it('should provide extensive Brazilian clinical search synonyms for all tools', () => {
      for (const item of parsedManifest) {
        expect(item.searchSynonyms.length).toBeGreaterThanOrEqual(10);
        expect(['block_01.json', 'block_03.json']).toContain(item.blockFile);
        expect(['bloco-01-emergencia-choque-uti', 'bloco-03-neurologia-neurocirurgia']).toContain(item.categorySlug);
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

      // Verify all Block 01 calculator IDs are present in manifest
      const manifestIds = new Set(parsedManifest.map((m) => m.id));
      const blockIds = parsedBlock01.calculators.map((c) => c.id);
      for (const id of blockIds) {
        expect(manifestIds.has(id)).toBe(true);
      }
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

  describe('Block 03 Ingestion Contract (`src/data/blocks/block_03.json`)', () => {
    it('should strictly validate the entire Block 03 against BlockDataSchema', () => {
      const parseResult = BlockDataSchema.safeParse(rawBlock03Data);
      expect(parseResult.success).toBe(true);
    });

    it('should validate all individual Block 03 calculators with CalculatorSchema (>= 18 tools, currently 39)', () => {
      for (const calc of parsedBlock03.calculators) {
        const result = CalculatorSchema.safeParse(calc);
        expect(result.success).toBe(true);
      }
    });

    it('should contain all neuro calculators with complete zero-truncation dossiers (>= 18 tools, currently 39)', () => {
      expect(parsedBlock03.blockId).toBe('block_03');
      expect(parsedBlock03.calculators.length).toBeGreaterThanOrEqual(18);
      expect(parsedBlock03.calculators).toHaveLength(39);

      const manifestIds = new Set(parsedManifest.map((m) => m.id));
      const blockIds = parsedBlock03.calculators.map((c) => c.id);
      for (const id of blockIds) {
        expect(manifestIds.has(id)).toBe(true);
      }
    });

    it('should validate NIHSS with full 11 domains / 15 items and 0-42 points', () => {
      const nihss = parsedBlock03.calculators.find((c) => c.id === 'calc_nihss');
      expect(nihss).toBeDefined();
      expect(nihss?.minPossibleScore).toBe(0);
      expect(nihss?.maxPossibleScore).toBe(42);
      expect(nihss?.parameterGroups).toHaveLength(15);
      expect(nihss?.radarAxes.length).toBeGreaterThanOrEqual(1);
    });

    it('should validate ASPECTS with 10 MCA regions and baseScore=10', () => {
      const aspects = parsedBlock03.calculators.find((c) => c.id === 'calc_aspects');
      expect(aspects).toBeDefined();
      expect(aspects?.baseScore).toBe(10);
      expect(aspects?.minPossibleScore).toBe(0);
      expect(aspects?.maxPossibleScore).toBe(10);
      expect(aspects?.parameterGroups).toHaveLength(10);
    });

    it('should validate ICH Score with 5 criteria and 30-day mortality statistics', () => {
      const ich = parsedBlock03.calculators.find((c) => c.id === 'calc_ich_score');
      expect(ich).toBeDefined();
      expect(ich?.minPossibleScore).toBe(0);
      expect(ich?.maxPossibleScore).toBe(6);
      expect(ich?.parameterGroups).toHaveLength(5);
      expect(ich?.riskTiers.length).toBeGreaterThanOrEqual(4);
    });

    it('should validate Hunt-Hess with 5 classical grades and Nimodipine warning', () => {
      const hh = parsedBlock03.calculators.find((c) => c.id === 'calc_hunt_hess');
      expect(hh).toBeDefined();
      expect(hh?.minPossibleScore).toBe(1);
      expect(hh?.maxPossibleScore).toBe(5);
      expect(hh?.clinicalWarning).toContain('Nimodipino');
      expect(hh?.clinicalWarning).toContain('TERMINANTEMENTE PROIBIDA');
      expect(hh?.clinicalWarning).toContain('intravenosa');
    });

    it('should validate Rotterdam CT Score with baseScore=1 and 1-6 points', () => {
      const rotterdam = parsedBlock03.calculators.find((c) => c.id === 'calc_rotterdam');
      expect(rotterdam).toBeDefined();
      expect(rotterdam?.baseScore).toBe(1);
      expect(rotterdam?.minPossibleScore).toBe(1);
      expect(rotterdam?.maxPossibleScore).toBe(6);
      expect(rotterdam?.parameterGroups).toHaveLength(4);
    });

    it('should validate ASIA/AIS impairment scale with 5 AIS grades and rectal examination notice', () => {
      const asia = parsedBlock03.calculators.find((c) => c.id === 'calc_asia_ais');
      expect(asia).toBeDefined();
      expect(asia?.clinicalWarning).toContain('CHAVE SACRAL');
      expect(asia?.clinicalWarning).toContain('exame anal digital');
      expect(asia?.riskTiers).toHaveLength(5);
    });

    it('should validate mRS (0-6) and KPS (0-100%) functional scales', () => {
      const mrs = parsedBlock03.calculators.find((c) => c.id === 'calc_mrs');
      expect(mrs).toBeDefined();
      expect(mrs?.minPossibleScore).toBe(0);
      expect(mrs?.maxPossibleScore).toBe(6);

      const kps = parsedBlock03.calculators.find((c) => c.id === 'calc_kps');
      expect(kps).toBeDefined();
      expect(kps?.minPossibleScore).toBe(0);
      expect(kps?.maxPossibleScore).toBe(100);
    });

    it('should validate MEEM (0-30) and MoCA (0-30) cognitive tools with Brazilian education standards', () => {
      const meem = parsedBlock03.calculators.find((c) => c.id === 'calc_meem_mmse');
      expect(meem).toBeDefined();
      expect(meem?.minPossibleScore).toBe(0);
      expect(meem?.maxPossibleScore).toBe(30);
      expect(meem?.parameterGroups).toHaveLength(11);

      const moca = parsedBlock03.calculators.find((c) => c.id === 'calc_moca');
      expect(moca).toBeDefined();
      expect(moca?.minPossibleScore).toBe(0);
      expect(moca?.maxPossibleScore).toBe(30);
      expect(moca?.parameterGroups).toHaveLength(8);
      expect(moca?.clinicalWarning).toContain('12 ANOS OU MENOS');
    });

    it('should validate Hoehn & Yahr (0-5 with 1.5, 2.5) and EDSS (0.0-10.0 in 0.5 steps)', () => {
      const hy = parsedBlock03.calculators.find((c) => c.id === 'calc_hoehn_yahr');
      expect(hy).toBeDefined();
      expect(hy?.minPossibleScore).toBe(0);
      expect(hy?.maxPossibleScore).toBe(5);
      expect(hy?.parameterGroups[0].options).toHaveLength(8);

      const edss = parsedBlock03.calculators.find((c) => c.id === 'calc_edss');
      expect(edss).toBeDefined();
      expect(edss?.minPossibleScore).toBe(0.0);
      expect(edss?.maxPossibleScore).toBe(10.0);
      expect(edss?.parameterGroups[0].options).toHaveLength(20);
    });
  });
});
