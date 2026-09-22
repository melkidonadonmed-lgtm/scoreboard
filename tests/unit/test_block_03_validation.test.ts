import { describe, it, expect } from 'vitest';
import rawBlock03Data from '@/data/blocks/block_03.json';
import {
  BlockDataSchema,
  ClinicalToolSchema,
  CalculatorSchema,
  type BlockData,
  type Calculator,
  type PharmacologicalAction,
  type NonPharmacologicalAction
} from '@/types/clinical';

describe('Block 03 Clinical Tools Schema & Data Integrity Validation', () => {
  const parsedBlock03: BlockData = BlockDataSchema.parse(rawBlock03Data);
  const calculators: Calculator[] = parsedBlock03.calculators;

  describe('1. Block & Tool Schema Conformance', () => {
    it('should strictly validate the entire Block 03 payload against BlockDataSchema', () => {
      const result = BlockDataSchema.safeParse(rawBlock03Data);
      expect(result.success).toBe(true);
      expect(parsedBlock03.blockId).toBe('block_03');
      expect(parsedBlock03.blockName).toContain('Neurologia');
      expect(parsedBlock03.version).toBeDefined();
    });

    it('should contain all clinical tools matching the monographic inventory (>= 18 tools, currently 39)', () => {
      expect(calculators.length).toBeGreaterThanOrEqual(18);
      expect(calculators).toHaveLength(39);

      const expectedLegacyToolIds = [
        'calc_rotterdam',
        'calc_marshall',
        'calc_asia_ais',
        'calc_hunt_hess',
        'calc_wfns',
        'calc_fisher_classic',
        'calc_fisher_modified',
        'calc_spetzler_martin',
        'calc_nihss',
        'calc_aspects',
        'calc_ich_score',
        'calc_abcd2',
        'calc_mrs',
        'calc_kps',
        'calc_meem_mmse',
        'calc_moca',
        'calc_hoehn_yahr',
        'calc_edss'
      ];

      const actualIds = calculators.map((c) => c.id);
      for (const id of expectedLegacyToolIds) {
        expect(actualIds).toContain(id);
      }
    });

    it('should validate every individual clinical tool with ClinicalToolSchema / CalculatorSchema', () => {
      for (const tool of calculators) {
        const result = ClinicalToolSchema.safeParse(tool);
        expect(result.success, `Tool ${tool.id} failed ClinicalToolSchema validation`).toBe(true);

        const calcResult = CalculatorSchema.safeParse(tool);
        expect(calcResult.success, `Tool ${tool.id} failed CalculatorSchema validation`).toBe(true);

        // Core identity attributes
        expect(tool.id).toBeTruthy();
        expect(tool.name).toBeTruthy();
        expect(tool.acronym).toBeTruthy();
        expect(tool.slug).toBeTruthy();
        expect(tool.categorySlug).toBe('bloco-03-neurologia-neurocirurgia');
        expect(tool.summary.length).toBeGreaterThanOrEqual(20);
        expect(tool.evidenceSource.length).toBeGreaterThanOrEqual(20);
        expect(tool.parameterGroups.length).toBeGreaterThanOrEqual(1);
        expect(tool.riskTiers.length).toBeGreaterThanOrEqual(3);
        expect(tool.minPossibleScore).toBeLessThanOrEqual(tool.maxPossibleScore);
      }
    });

    it('should enforce proper baseScore configurations for subtractive and offset models', () => {
      const rotterdam = calculators.find((c) => c.id === 'calc_rotterdam');
      expect(rotterdam?.baseScore).toBe(1);

      const aspects = calculators.find((c) => c.id === 'calc_aspects');
      expect(aspects?.baseScore).toBe(10);

      // Other 16 tools should default to baseScore 0
      const standardTools = calculators.filter(
        (c) => c.id !== 'calc_rotterdam' && c.id !== 'calc_aspects'
      );
      for (const tool of standardTools) {
        expect(tool.baseScore ?? 0).toBe(0);
      }
    });
  });

  describe('2. Radar Axes & Value Normalization [0, 100%]', () => {
    it('should ensure all 18 tools have non-empty radar_axes definitions', () => {
      for (const tool of calculators) {
        expect(
          tool.radarAxes.length,
          `Tool ${tool.id} must define at least one radar axis`
        ).toBeGreaterThanOrEqual(1);

        for (const axis of tool.radarAxes) {
          expect(axis.id).toBeTruthy();
          expect(axis.label).toBeTruthy();
          expect(axis.system).toBeTruthy();
          expect(axis.baselineValue).toBeGreaterThanOrEqual(0);
          expect(axis.maxAxisValue).toBeGreaterThan(0);
          expect(axis.maxAxisValue).toBeGreaterThanOrEqual(axis.baselineValue);
        }
      }
    });

    it('should verify that all option radarNormalizedValues map strictly to [0, 1] (0% to 100%)', () => {
      for (const tool of calculators) {
        for (const group of tool.parameterGroups) {
          for (const option of group.options) {
            const normVal = option.radarNormalizedValue;
            expect(
              normVal,
              `Tool ${tool.id}, group ${group.id}, option ${option.id} has invalid radar value ${normVal}`
            ).toBeGreaterThanOrEqual(0);
            expect(
              normVal,
              `Tool ${tool.id}, group ${group.id}, option ${option.id} has radar value > 1: ${normVal}`
            ).toBeLessThanOrEqual(1);

            // In scaled percentage space (0 to 100)
            const percentage = normVal * 100;
            expect(percentage).toBeGreaterThanOrEqual(0);
            expect(percentage).toBeLessThanOrEqual(100);
          }
        }
      }
    });

    it('should verify that normal baseline options have valid normalized values in [0, 1]', () => {
      for (const tool of calculators) {
        for (const group of tool.parameterGroups) {
          const baselineOptions = group.options.filter((opt) => opt.isNormalBaseline);
          for (const opt of baselineOptions) {
            expect(opt.radarNormalizedValue).toBeGreaterThanOrEqual(0);
            expect(opt.radarNormalizedValue).toBeLessThanOrEqual(1);

            // For non-inverted parameters where pointValue is 0, radar derangement is 0
            if (opt.pointValue === 0) {
              expect(
                opt.radarNormalizedValue,
                `Tool ${tool.id} option ${opt.id} with pointValue 0 should have 0 radar derangement`
              ).toBe(0);
            }
          }
        }
      }
    });
  });

  describe('3. Emergency Alerts & Critical Neuro Warnings', () => {
    it('should ensure every tool has an emergency alert or clinical warning configured', () => {
      for (const tool of calculators) {
        const warning = tool.clinicalWarning;
        expect(
          warning,
          `Tool ${tool.id} must have a non-empty clinicalWarning/alert`
        ).toBeDefined();
        expect(
          warning?.length,
          `Tool ${tool.id} clinical warning must be comprehensive (>= 40 chars)`
        ).toBeGreaterThanOrEqual(40);
      }
    });

    it('should verify high-priority black-box warnings and clinical red flags', () => {
      // Hunt-Hess: Nimodipine IV prohibition black-box warning
      const huntHess = calculators.find((c) => c.id === 'calc_hunt_hess');
      expect(huntHess?.clinicalWarning).toMatch(/Nimodipino/i);
      expect(huntHess?.clinicalWarning).toMatch(/TERMINANTEMENTE PROIBIDA/i);
      expect(huntHess?.clinicalWarning).toMatch(/intravenosa/i);

      // WFNS: Pre-sedation GCS mandatory assessment
      const wfns = calculators.find((c) => c.id === 'calc_wfns');
      expect(wfns?.clinicalWarning).toMatch(/PRÉ-SEDAÇÃO OBRIGATÓRIA/i);
      expect(wfns?.clinicalWarning).toMatch(/sedativos/i);

      // Fisher Classic: Non-linearity paradox warning
      const fisherCl = calculators.find((c) => c.id === 'calc_fisher_classic');
      expect(fisherCl?.clinicalWarning).toMatch(/NÃO-LINEARIDADE/i);
      expect(fisherCl?.clinicalWarning).toMatch(/Grau 3/i);

      // Spetzler-Martin: ARUBA trial evidence
      const spetzler = calculators.find((c) => c.id === 'calc_spetzler_martin');
      expect(spetzler?.clinicalWarning).toMatch(/ARUBA/i);
      expect(spetzler?.clinicalWarning).toMatch(/conservador/i);

      // ASPECTS: Stroke window HU settings
      const aspects = calculators.find((c) => c.id === 'calc_aspects');
      expect(aspects?.clinicalWarning).toMatch(/STROKE WINDOW/i);
      expect(aspects?.clinicalWarning).toMatch(/40 HU/i);

      // ICH Score: Bioethical AHA 2022 warning against self-fulfilling prophecy
      const ich = calculators.find((c) => c.id === 'calc_ich_score');
      expect(ich?.clinicalWarning).toMatch(/PROFECIA AUTORREALIZÁVEL/i);
      expect(ich?.clinicalWarning).toMatch(/AHA\/ASA 2022/i);

      // ASIA/AIS: Mandatory sacral key examination (S4-S5)
      const asia = calculators.find((c) => c.id === 'calc_asia_ais');
      expect(asia?.clinicalWarning).toMatch(/CHAVE SACRAL/i);
      expect(asia?.clinicalWarning).toMatch(/exame anal digital/i);

      // NIHSS: Blood pressure goals for acute reperfusion
      const nihss = calculators.find((c) => c.id === 'calc_nihss');
      expect(nihss?.clinicalWarning).toMatch(/METAS PRESSÓRICAS/i);
      expect(nihss?.clinicalWarning).toMatch(/185\/110/i);

      // ABCD2: Isolated score pitfall in carotid stenosis
      const abcd2 = calculators.find((c) => c.id === 'calc_abcd2');
      expect(abcd2?.clinicalWarning).toMatch(/ARMADILHA DO ABCD/i);
      expect(abcd2?.clinicalWarning).toMatch(/carotídea/i);

      // Hoehn & Yahr: Pull test postural instability discriminator
      const hy = calculators.find((c) => c.id === 'calc_hoehn_yahr');
      expect(hy?.clinicalWarning).toMatch(/DIVISOR DE ÁGUAS/i);
      expect(hy?.clinicalWarning).toMatch(/pull test/i);
    });
  });

  describe('4. Pharmacological Actions & Neurocritical Protocols', () => {
    it('should ensure all tools have pharmacological actions defined (top-level or in risk tiers)', () => {
      for (const tool of calculators) {
        const topLevelPharm = tool.pharmacologicalActions || [];
        const tierPharm = tool.riskTiers.flatMap((t) => t.pharmacologicalActions || []);
        const totalPharm = [...topLevelPharm, ...tierPharm];

        expect(
          totalPharm.length,
          `Tool ${tool.id} must define pharmacological actions across tiers`
        ).toBeGreaterThanOrEqual(1);
      }
    });

    it('should verify that all pharmacological actions contain non-empty drug name, dose, and route', () => {
      let inspectedActionCount = 0;

      for (const tool of calculators) {
        const allPharm: PharmacologicalAction[] = [
          ...(tool.pharmacologicalActions || []),
          ...tool.riskTiers.flatMap((t) => t.pharmacologicalActions || [])
        ];

        for (const action of allPharm) {
          inspectedActionCount++;
          expect(action.id, `Empty action ID in ${tool.id}`).toBeTruthy();
          expect(action.drugName, `Empty drugName in ${tool.id}`).toBeTruthy();
          expect(action.dosage, `Empty dosage for ${action.drugName} in ${tool.id}`).toBeTruthy();
          expect(action.route, `Empty route for ${action.drugName} in ${tool.id}`).toBeTruthy();
          expect(action.frequency, `Empty frequency for ${action.drugName} in ${tool.id}`).toBeTruthy();
        }
      }

      expect(inspectedActionCount).toBeGreaterThanOrEqual(50);
    });

    it('should verify that every clinical tool specifies diluent, administration, or clinical precautions in its actions', () => {
      for (const tool of calculators) {
        const allPharm: PharmacologicalAction[] = [
          ...(tool.pharmacologicalActions || []),
          ...tool.riskTiers.flatMap((t) => t.pharmacologicalActions || [])
        ];

        const hasPrecInTool = allPharm.some((action) => {
          return (
            Boolean(action.dilutionInstructions?.trim()) ||
            Boolean(action.contraindications?.trim()) ||
            Boolean(action.renalAdjustment?.trim()) ||
            Boolean(action.infusionProtocol) ||
            /proibido|dilui|ajust|precau|meta|npo|sg|sf|cuidad/i.test(
              `${action.dosage} ${action.route} ${action.drugName}`
            )
          );
        });

        expect(
          hasPrecInTool,
          `Tool ${tool.id} must specify clinical precautions/diluents across its pharmacological actions`
        ).toBe(true);
      }
    });

    it('should verify essential neurocritical drugs and safety guidelines', () => {
      const allPharm: PharmacologicalAction[] = calculators.flatMap((tool) => [
        ...(tool.pharmacologicalActions || []),
        ...tool.riskTiers.flatMap((t) => t.pharmacologicalActions || [])
      ]);

      const drugNames = allPharm.map((p) => p.drugName.toLowerCase());

      // Nimodipine in HSA
      const hasNimodipine = drugNames.some((d) => d.includes('nimodipino'));
      expect(hasNimodipine).toBe(true);

      // Osmotherapy (Salina Hipertônica 3% or Manitol)
      const hasOsmotherapy = drugNames.some(
        (d) => d.includes('salina') || d.includes('manitol')
      );
      expect(hasOsmotherapy).toBe(true);

      // Anticonvulsants (Levetiracetam or Fenitoína)
      const hasAnticonvulsant = drugNames.some(
        (d) => d.includes('levetiracetam') || d.includes('fenitoína')
      );
      expect(hasAnticonvulsant).toBe(true);

      // Thrombolysis (Alteplase or Tenecteplase)
      const hasThrombolysis = drugNames.some(
        (d) => d.includes('alteplase') || d.includes('tenecteplase')
      );
      expect(hasThrombolysis).toBe(true);

      // Vasoactive support (Noradrenalina)
      const hasNoradrenalina = drugNames.some((d) => d.includes('noradrenalina'));
      expect(hasNoradrenalina).toBe(true);
    });
  });

  describe('5. Non-Pharmacological Actions & Interventional Pathways', () => {
    it('should ensure all tools have non-pharmacological actions defined', () => {
      for (const tool of calculators) {
        const topLevelNonPharm = tool.nonPharmacologicalActions || [];
        const tierNonPharm = tool.riskTiers.flatMap((t) => t.nonPharmacologicalActions || []);
        const totalNonPharm = [...topLevelNonPharm, ...tierNonPharm];

        expect(
          totalNonPharm.length,
          `Tool ${tool.id} must define non-pharmacological actions`
        ).toBeGreaterThanOrEqual(1);
      }
    });

    it('should verify that all non-pharmacological actions have complete structural fields', () => {
      let inspectedActionCount = 0;

      for (const tool of calculators) {
        const allNonPharm: NonPharmacologicalAction[] = [
          ...(tool.nonPharmacologicalActions || []),
          ...tool.riskTiers.flatMap((t) => t.nonPharmacologicalActions || [])
        ];

        for (const action of allNonPharm) {
          inspectedActionCount++;
          expect(action.id, `Empty non-pharm ID in ${tool.id}`).toBeTruthy();
          expect(
            action.recommendationTitle,
            `Empty recommendationTitle in ${tool.id}`
          ).toBeTruthy();
          expect(
            action.dispositionTarget,
            `Empty dispositionTarget in ${tool.id}`
          ).toBeTruthy();
          expect(
            action.monitoringPlan,
            `Empty monitoringPlan in ${tool.id}`
          ).toBeTruthy();
        }
      }

      expect(inspectedActionCount).toBeGreaterThanOrEqual(50);
    });

    it('should verify surgical and neuro-interventional procedures are specified where required', () => {
      const allNonPharm = calculators.flatMap((tool) => [
        ...(tool.nonPharmacologicalActions || []),
        ...tool.riskTiers.flatMap((t) => t.nonPharmacologicalActions || [])
      ]);

      const procedures = allNonPharm
        .map((np) => (np.interventionalProcedure || '').toLowerCase())
        .filter(Boolean);

      // External Ventricular Drainage (DVE)
      const hasDVE = procedures.some((p) => p.includes('dve') || p.includes('derivação ventricular'));
      expect(hasDVE).toBe(true);

      // Decompressive Craniectomy
      const hasCraniectomy = procedures.some((p) => p.includes('craniectomia'));
      expect(hasCraniectomy).toBe(true);

      // Mechanical Thrombectomy
      const hasThrombectomy = procedures.some((p) => p.includes('trombectomia'));
      expect(hasThrombectomy).toBe(true);

      // Surgical clipping or endovascular coiling
      const hasAneurysmRepair = procedures.some(
        (p) => p.includes('clipagem') || p.includes('embolização')
      );
      expect(hasAneurysmRepair).toBe(true);
    });
  });

  describe('6. Citations & References Validation', () => {
    it('should ensure all 18 tools provide valid academic references', () => {
      for (const tool of calculators) {
        const citation = tool.evidenceSource;
        expect(citation, `Tool ${tool.id} has no evidenceSource`).toBeTruthy();
        expect(citation.length, `Citation too short in ${tool.id}`).toBeGreaterThanOrEqual(30);

        // Must contain a 4-digit publication year (19xx or 20xx)
        const hasYear = /\b(19\d{2}|20\d{2})\b/.test(citation);
        expect(hasYear, `Evidence source for ${tool.id} must include publication year: "${citation}"`).toBe(true);

        // Must contain journal or author pattern
        const hasAuthorOrJournal = /[a-zA-Z]{3,}/.test(citation);
        expect(hasAuthorOrJournal).toBe(true);
      }
    });
  });
});
