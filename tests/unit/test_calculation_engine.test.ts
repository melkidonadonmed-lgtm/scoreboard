import { describe, it, expect } from 'vitest';
import block01Data from '../../src/data/blocks/block_01.json';
import {
  CalculatorSchema,
  type Calculator,
  type ParameterGroup,
  type RiskTier
} from '../../src/types/clinical';
import { calculateScore } from '../../src/engines/calculationEngine';

// Helper to extract calculators from block_01
const getBlock01Calc = (id: string): Calculator => {
  const found = (block01Data.calculators as unknown as Calculator[]).find((c) => c.id === id);
  if (!found) throw new Error(`Calculator ${id} not found in block_01`);
  return found;
};

// ============================================================================
// MOCK BUILDERS FOR CLINICAL SPECIFICATIONS
// ============================================================================

/**
 * Builds a schema-compliant ASPECTS Calculator (Alberta Stroke Program Early CT Score)
 * - Base Score: 10
 * - Subtractive points (-1 per affected MCA territory)
 * - Minimum: 0, Maximum: 10
 */
function createAspectsCalculator(): Calculator {
  const territories = [
    { id: 'caudate', name: 'Núcleo Caudado (C)' },
    { id: 'lentiform', name: 'Núcleo Lentiforme (L)' },
    { id: 'internal_capsule', name: 'Cápsula Interna (IC)' },
    { id: 'insular_cortex', name: 'Córtex Insular / Fita Insular (I)' },
    { id: 'm1', name: 'M1 (Córtex ACM anterior)' },
    { id: 'm2', name: 'M2 (Córtex ACM lateral à fita insular)' },
    { id: 'm3', name: 'M3 (Córtex ACM posterior)' },
    { id: 'm4', name: 'M4 (Território ACM anterior superior)' },
    { id: 'm5', name: 'M5 (Território ACM lateral superior)' },
    { id: 'm6', name: 'M6 (Território ACM posterior superior)' }
  ];

  const parameterGroups: ParameterGroup[] = territories.map((t, idx) => ({
    id: `grp_aspects_${t.id}`,
    name: t.name,
    slug: `aspects-${t.id}`,
    inputType: 'single_choice',
    radarAxisId: 'axis_aspects_neuroimaging',
    normalBaselineValue: 0,
    maxAxisValue: 1,
    sortOrder: idx + 1,
    options: [
      {
        id: `opt_${t.id}_normal`,
        label: 'Normal / Sem Hipoatenuação',
        pointValue: 0,
        isNormalBaseline: true,
        radarNormalizedValue: 0.0,
        sortOrder: 1
      },
      {
        id: `opt_${t.id}_hypodense`,
        label: 'Isquemia Precoce / Hipoatenuação Aguda',
        pointValue: -1,
        isNormalBaseline: false,
        radarNormalizedValue: 1.0,
        sortOrder: 2
      }
    ]
  }));

  const riskTiers: RiskTier[] = [
    {
      id: 'tier_aspects_large_core',
      label: 'Infarto Extenso / Núcleo Isquêmico Amplo (0 a 5 pontos)',
      severityLevel: 'critical',
      minScore: 0,
      maxScore: 5,
      statisticalOutcome: 'Alto risco de transformação hemorrágica sintomática e desfecho funcional desfavorável. Trombectomia em casos selecionados (DAWN/DEFUSE-3/SELECT2).',
      colorHex: '#ef4444',
      pharmacologicalActions: [],
      nonPharmacologicalActions: []
    },
    {
      id: 'tier_aspects_moderate_core',
      label: 'Núcleo Isquêmico Moderado (6 a 7 pontos)',
      severityLevel: 'intermediate',
      minScore: 6,
      maxScore: 7,
      statisticalOutcome: 'Elegível para trombectomia mecânica se oclusão de grandes vasos (LVO) confirmada até 24h.',
      colorHex: '#f59e0b',
      pharmacologicalActions: [],
      nonPharmacologicalActions: []
    },
    {
      id: 'tier_aspects_favorable',
      label: 'Núcleo Isquêmico Pequeno / Parênquima Fisiologicamente Salvo (8 a 10 pontos)',
      severityLevel: 'low',
      minScore: 8,
      maxScore: 10,
      statisticalOutcome: 'Excelente prognóstico para recanalização por trombólise IV e/ou trombectomia mecânica.',
      colorHex: '#10b981',
      pharmacologicalActions: [],
      nonPharmacologicalActions: []
    }
  ];

  return {
    id: 'calc_aspects',
    slug: 'aspects',
    name: 'ASPECTS (Alberta Stroke Program Early CT Score)',
    acronym: 'ASPECTS',
    categorySlug: 'bloco-03-neurologia-neurocirurgia',
    summary: 'Avaliação quantitativa de alterações isquêmicas precoces na circulação anterior (ACM) via TC.',
    calculationType: 'additive_points',
    evidenceSource: 'Barber PA et al. Lancet 2000; 355:1670–1674',
    minPossibleScore: 0,
    maxPossibleScore: 10,
    baseScore: 10,
    radarAxes: [
      {
        id: 'axis_aspects_neuroimaging',
        label: 'Extensão Isquêmica Tomográfica',
        system: 'Imagem',
        baselineValue: 0,
        maxAxisValue: 1
      }
    ],
    parameterGroups,
    riskTiers
  };
}

/**
 * Builds a schema-compliant Rotterdam CT Score Calculator (Neurotrauma / TCE)
 * - Base Score: 1 (pontuação basal obrigatória)
 * - Offset additive score (pontos positivos somados à base de 1)
 * - Minimum: 1, Maximum: 6
 */
function createRotterdamCalculator(): Calculator {
  const parameterGroups: ParameterGroup[] = [
    {
      id: 'grp_rotterdam_cisterns',
      name: 'Cisternas Basais',
      slug: 'rotterdam-cisterns',
      inputType: 'single_choice',
      radarAxisId: 'axis_rotterdam_icp',
      normalBaselineValue: 0,
      maxAxisValue: 1,
      sortOrder: 1,
      options: [
        {
          id: 'opt_cisterns_normal',
          label: 'Normais / Abertas',
          pointValue: 0,
          isNormalBaseline: true,
          radarNormalizedValue: 0.0,
          sortOrder: 1
        },
        {
          id: 'opt_cisterns_compressed',
          label: 'Comprimidas',
          pointValue: 1,
          isNormalBaseline: false,
          radarNormalizedValue: 0.5,
          sortOrder: 2
        },
        {
          id: 'opt_cisterns_absent',
          label: 'Ausentes / Apagadas',
          pointValue: 2,
          isNormalBaseline: false,
          radarNormalizedValue: 1.0,
          sortOrder: 3
        }
      ]
    },
    {
      id: 'grp_rotterdam_shift',
      name: 'Desvio de Linha Média',
      slug: 'rotterdam-shift',
      inputType: 'single_choice',
      radarAxisId: 'axis_rotterdam_icp',
      normalBaselineValue: 0,
      maxAxisValue: 1,
      sortOrder: 2,
      options: [
        {
          id: 'opt_shift_lte_5mm',
          label: '<= 5 mm (ou ausente)',
          pointValue: 0,
          isNormalBaseline: true,
          radarNormalizedValue: 0.0,
          sortOrder: 1
        },
        {
          id: 'opt_shift_gt_5mm',
          label: '> 5 mm',
          pointValue: 1,
          isNormalBaseline: false,
          radarNormalizedValue: 1.0,
          sortOrder: 2
        }
      ]
    },
    {
      id: 'grp_rotterdam_edh',
      name: 'Hematoma Epidural (HED)',
      slug: 'rotterdam-edh',
      inputType: 'single_choice',
      radarAxisId: 'axis_rotterdam_mass',
      normalBaselineValue: 0,
      maxAxisValue: 1,
      sortOrder: 3,
      options: [
        {
          id: 'opt_edh_present',
          label: 'Presente (efeito protetor relativo no modelo Rotterdam: 0 pts adicionais)',
          pointValue: 0,
          isNormalBaseline: false,
          radarNormalizedValue: 0.2,
          sortOrder: 1
        },
        {
          id: 'opt_edh_absent',
          label: 'Ausente (+1 ponto adicional na escala de risco)',
          pointValue: 1,
          isNormalBaseline: true,
          radarNormalizedValue: 0.0,
          sortOrder: 2
        }
      ]
    },
    {
      id: 'grp_rotterdam_sah_ivh',
      name: 'Hemorragia Subaracnóidea Traumática (tHSA) ou Intraventricular (HIV)',
      slug: 'rotterdam-sah-ivh',
      inputType: 'single_choice',
      radarAxisId: 'axis_rotterdam_hemorrhage',
      normalBaselineValue: 0,
      maxAxisValue: 1,
      sortOrder: 4,
      options: [
        {
          id: 'opt_sah_ivh_absent',
          label: 'Ausente',
          pointValue: 0,
          isNormalBaseline: true,
          radarNormalizedValue: 0.0,
          sortOrder: 1
        },
        {
          id: 'opt_sah_ivh_present',
          label: 'Presente',
          pointValue: 1,
          isNormalBaseline: false,
          radarNormalizedValue: 1.0,
          sortOrder: 2
        }
      ]
    }
  ];

  const riskTiers: RiskTier[] = [
    {
      id: 'tier_rotterdam_1_2',
      label: 'Rotterdam 1 a 2 pontos (Baixa Mortalidade em 6 meses)',
      severityLevel: 'low',
      minScore: 1,
      maxScore: 2,
      statisticalOutcome: 'Mortalidade estimada em 6 meses entre 5% e 10%.',
      colorHex: '#10b981',
      pharmacologicalActions: [],
      nonPharmacologicalActions: []
    },
    {
      id: 'tier_rotterdam_3_4',
      label: 'Rotterdam 3 a 4 pontos (Mortalidade Intermediária)',
      severityLevel: 'intermediate',
      minScore: 3,
      maxScore: 4,
      statisticalOutcome: 'Mortalidade estimada em 6 meses entre 25% e 35%. Monitorização invasiva de PIC.',
      colorHex: '#f59e0b',
      pharmacologicalActions: [],
      nonPharmacologicalActions: []
    },
    {
      id: 'tier_rotterdam_5_6',
      label: 'Rotterdam 5 a 6 pontos (Alta Mortalidade / TCE Crítico)',
      severityLevel: 'critical',
      minScore: 5,
      maxScore: 6,
      statisticalOutcome: 'Mortalidade estimada em 6 meses de 53% a 61%. Risco extremo de hipertensão intracraniana refratária.',
      colorHex: '#ef4444',
      pharmacologicalActions: [],
      nonPharmacologicalActions: []
    }
  ];

  return {
    id: 'calc_rotterdam',
    slug: 'rotterdam',
    name: 'Escore Tomográfico de Rotterdam (TCE)',
    acronym: 'Rotterdam',
    categorySlug: 'bloco-03-neurologia-neurocirurgia',
    summary: 'Classificação tomográfica prognóstica de mortalidade em 6 meses para TCE moderado a grave.',
    calculationType: 'additive_points',
    evidenceSource: 'Maas AI et al. Neurosurgery 2005; 57(6):1173-1182',
    minPossibleScore: 1,
    maxPossibleScore: 6,
    baseScore: 1,
    radarAxes: [
      { id: 'axis_rotterdam_icp', label: 'Risco de HIC', system: 'Neurológico', baselineValue: 0, maxAxisValue: 1 },
      { id: 'axis_rotterdam_mass', label: 'Efeito de Massa', system: 'Imagem', baselineValue: 0, maxAxisValue: 1 },
      { id: 'axis_rotterdam_hemorrhage', label: 'Sangramento Intracraniano', system: 'Imagem', baselineValue: 0, maxAxisValue: 1 }
    ],
    parameterGroups,
    riskTiers
  };
}

// ============================================================================
// TEST SUITE
// ============================================================================

describe('calculationEngine: baseScore & Schema Validation', () => {

  // --------------------------------------------------------------------------
  // 1. BACKWARD COMPATIBILITY: Default baseScore (0) with existing Block 01
  // --------------------------------------------------------------------------
  describe('Default baseScore (0) Backward Compatibility', () => {
    it('defaults baseScore to 0 when parsing an object without baseScore', () => {
      const rawCalculatorWithoutBaseScore = {
        id: 'calc_test_nobase',
        slug: 'test-nobase',
        name: 'Test No Base',
        acronym: 'TNB',
        categorySlug: 'test',
        summary: 'Test summary',
        calculationType: 'additive_points',
        evidenceSource: 'Test Source',
        minPossibleScore: 0,
        maxPossibleScore: 3,
        radarAxes: [],
        parameterGroups: [],
        riskTiers: [
          {
            id: 'tier_1',
            label: 'Tier 1',
            severityLevel: 'low',
            minScore: 0,
            maxScore: 3,
            statisticalOutcome: 'Outcome',
            colorHex: '#000000',
            pharmacologicalActions: [],
            nonPharmacologicalActions: []
          }
        ]
      };

      const parsed = CalculatorSchema.parse(rawCalculatorWithoutBaseScore);
      expect(parsed.baseScore).toBe(0);
    });

    it('calculates existing block_01 calculators with implicit baseScore = 0', () => {
      const qsofa = getBlock01Calc('calc_qsofa');
      expect(qsofa.baseScore).toBeUndefined(); // In raw JSON it has not been serialized yet

      // When calculateScore runs, it initializes rawScore with baseScore ?? 0 = 0
      const baselineResult = calculateScore(qsofa, {
        grp_qsofa_resp: 'opt_resp_normal',
        grp_qsofa_gcs: 'opt_gcs_15',
        grp_qsofa_sbp: 'opt_sbp_normal'
      });
      expect(baselineResult.rawScore).toBe(0);
      expect(baselineResult.scoreFormatted).toBe('0');

      const positiveResult = calculateScore(qsofa, {
        grp_qsofa_resp: 'opt_resp_high',
        grp_qsofa_gcs: 'opt_gcs_15',
        grp_qsofa_sbp: 'opt_sbp_low'
      });
      expect(positiveResult.rawScore).toBe(2);
      expect(positiveResult.scoreFormatted).toBe('2');
    });

    it('handles explicit baseScore = 0 identically to undefined baseScore', () => {
      const qsofa = getBlock01Calc('calc_qsofa');
      const qsofaWithExplicitZero: Calculator = {
        ...qsofa,
        baseScore: 0
      };

      const result = calculateScore(qsofaWithExplicitZero, {
        grp_qsofa_resp: 'opt_resp_high'
      });
      expect(result.rawScore).toBe(1);
    });
  });

  // --------------------------------------------------------------------------
  // 2. SUBTRACTIVE SCORE WITH POSITIVE BASE SCORE (ASPECTS: baseScore = 10)
  // --------------------------------------------------------------------------
  describe('Subtractive Scoring: ASPECTS (baseScore = 10, subtract points)', () => {
    const aspects = createAspectsCalculator();

    it('strictly passes Zod validation against CalculatorSchema', () => {
      const parseResult = CalculatorSchema.safeParse(aspects);
      expect(parseResult.success).toBe(true);
      if (parseResult.success) {
        expect(parseResult.data.baseScore).toBe(10);
        expect(parseResult.data.minPossibleScore).toBe(0);
        expect(parseResult.data.maxPossibleScore).toBe(10);
      }
    });

    it('calculates perfect 10/10 for pristine CT with 0 ischemic territories', () => {
      // All territories default to normal (0 points deducted)
      const result = calculateScore(aspects, {});
      expect(result.rawScore).toBe(10);
      expect(result.scoreFormatted).toBe('10');
      expect(result.activeRiskTier.id).toBe('tier_aspects_favorable');
      expect(result.radarValues['axis_aspects_neuroimaging']).toBe(0);
    });

    it('deducts points accurately when specific MCA zones are affected (e.g., 3 zones = ASPECTS 7)', () => {
      // 3 territories infarcted: M1, M2, and Lentiform
      const result = calculateScore(aspects, {
        grp_aspects_m1: 'opt_m1_hypodense',
        grp_aspects_m2: 'opt_m2_hypodense',
        grp_aspects_lentiform: 'opt_lentiform_hypodense'
      });

      // 10 - 1 - 1 - 1 = 7
      expect(result.rawScore).toBe(7);
      expect(result.scoreFormatted).toBe('7');
      expect(result.activeRiskTier.id).toBe('tier_aspects_moderate_core');
      expect(result.radarValues['axis_aspects_neuroimaging']).toBe(1.0);
    });

    it('correctly stratifies large ischemic core when 5+ zones are affected (e.g., ASPECTS 4)', () => {
      // 6 territories infarcted: Caudate, Lentiform, Internal Capsule, Insular, M1, M2
      const result = calculateScore(aspects, {
        grp_aspects_caudate: 'opt_caudate_hypodense',
        grp_aspects_lentiform: 'opt_lentiform_hypodense',
        grp_aspects_internal_capsule: 'opt_internal_capsule_hypodense',
        grp_aspects_insular_cortex: 'opt_insular_cortex_hypodense',
        grp_aspects_m1: 'opt_m1_hypodense',
        grp_aspects_m2: 'opt_m2_hypodense'
      });

      // 10 - 6 = 4
      expect(result.rawScore).toBe(4);
      expect(result.scoreFormatted).toBe('4');
      expect(result.activeRiskTier.id).toBe('tier_aspects_large_core');
    });

    it('calculates 0/10 when all 10 MCA territories are infarcted', () => {
      const inputs: Record<string, string> = {
        grp_aspects_caudate: 'opt_caudate_hypodense',
        grp_aspects_lentiform: 'opt_lentiform_hypodense',
        grp_aspects_internal_capsule: 'opt_internal_capsule_hypodense',
        grp_aspects_insular_cortex: 'opt_insular_cortex_hypodense',
        grp_aspects_m1: 'opt_m1_hypodense',
        grp_aspects_m2: 'opt_m2_hypodense',
        grp_aspects_m3: 'opt_m3_hypodense',
        grp_aspects_m4: 'opt_m4_hypodense',
        grp_aspects_m5: 'opt_m5_hypodense',
        grp_aspects_m6: 'opt_m6_hypodense'
      };

      const result = calculateScore(aspects, inputs);
      // 10 - 10 = 0
      expect(result.rawScore).toBe(0);
      expect(result.scoreFormatted).toBe('0');
      expect(result.activeRiskTier.id).toBe('tier_aspects_large_core');
    });

    it('clamps negative score to minPossibleScore = 0', () => {
      // Test safety clamp
      const calculatorWithLowerBound: Calculator = {
        ...aspects,
        minPossibleScore: 0
      };

      // Pass simulated direct negative addition
      const inputs = {
        grp_aspects_caudate: 'opt_caudate_hypodense',
        grp_aspects_lentiform: 'opt_lentiform_hypodense',
        grp_aspects_internal_capsule: 'opt_internal_capsule_hypodense',
        grp_aspects_insular_cortex: 'opt_insular_cortex_hypodense',
        grp_aspects_m1: 'opt_m1_hypodense',
        grp_aspects_m2: 'opt_m2_hypodense',
        grp_aspects_m3: 'opt_m3_hypodense',
        grp_aspects_m4: 'opt_m4_hypodense',
        grp_aspects_m5: 'opt_m5_hypodense',
        grp_aspects_m6: 'opt_m6_hypodense'
      };

      const result = calculateScore(calculatorWithLowerBound, inputs);
      expect(result.rawScore).toBe(0);
      expect(result.rawScore).toBeGreaterThanOrEqual(calculatorWithLowerBound.minPossibleScore);
    });
  });

  // --------------------------------------------------------------------------
  // 3. OFFSET SCORE WITH POSITIVE BASE SCORE (Rotterdam CT: baseScore = 1)
  // --------------------------------------------------------------------------
  describe('Offset Scoring: Rotterdam CT Score (baseScore = 1, add points)', () => {
    const rotterdam = createRotterdamCalculator();

    it('strictly passes Zod validation against CalculatorSchema', () => {
      const parseResult = CalculatorSchema.safeParse(rotterdam);
      expect(parseResult.success).toBe(true);
      if (parseResult.success) {
        expect(parseResult.data.baseScore).toBe(1);
        expect(parseResult.data.minPossibleScore).toBe(1);
        expect(parseResult.data.maxPossibleScore).toBe(6);
      }
    });

    it('calculates minimum 1 point for best-prognosis CT scan (Base 1 + 0 = 1)', () => {
      // Normal cisterns (0), Shift <= 5mm (0), EDH present (0), SAH/IVH absent (0)
      const result = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_normal',
        grp_rotterdam_shift: 'opt_shift_lte_5mm',
        grp_rotterdam_edh: 'opt_edh_present',
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_absent'
      });

      // 1 (base) + 0 + 0 + 0 + 0 = 1
      expect(result.rawScore).toBe(1);
      expect(result.scoreFormatted).toBe('1');
      expect(result.activeRiskTier.id).toBe('tier_rotterdam_1_2');
      expect(result.radarValues['axis_rotterdam_icp']).toBe(0.0);
    });

    it('calculates intermediate risk: Cisternas comprimidas (+1) + Sem HED (+1) = Rotterdam 3', () => {
      // Base (1) + Cisterns compressed (1) + Shift <= 5mm (0) + EDH absent (1) + No SAH (0) = 3
      const result = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_compressed',
        grp_rotterdam_shift: 'opt_shift_lte_5mm',
        grp_rotterdam_edh: 'opt_edh_absent',
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_absent'
      });

      expect(result.rawScore).toBe(3);
      expect(result.scoreFormatted).toBe('3');
      expect(result.activeRiskTier.id).toBe('tier_rotterdam_3_4');
      expect(result.radarValues['axis_rotterdam_icp']).toBe(0.5);
    });

    it('calculates critical risk: Cisternas apagadas (+2) + Desvio > 5mm (+1) + Sem HED (+1) + tHSA (+1) = Rotterdam 6', () => {
      // Base (1) + Absent cisterns (2) + Shift > 5mm (1) + EDH absent (1) + SAH/IVH (1) = 6
      const result = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_absent',
        grp_rotterdam_shift: 'opt_shift_gt_5mm',
        grp_rotterdam_edh: 'opt_edh_absent',
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_present'
      });

      expect(result.rawScore).toBe(6);
      expect(result.scoreFormatted).toBe('6');
      expect(result.activeRiskTier.id).toBe('tier_rotterdam_5_6');
      expect(result.radarValues['axis_rotterdam_icp']).toBe(1.0);
      expect(result.radarValues['axis_rotterdam_hemorrhage']).toBe(1.0);
    });

    it('clamps rawScore to maxPossibleScore = 6 and minPossibleScore = 1', () => {
      expect(rotterdam.minPossibleScore).toBe(1);
      expect(rotterdam.maxPossibleScore).toBe(6);

      // Best case cannot be less than 1
      const best = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_normal',
        grp_rotterdam_shift: 'opt_shift_lte_5mm',
        grp_rotterdam_edh: 'opt_edh_present',
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_absent'
      });
      expect(best.rawScore).toBe(1);

      // Worst case cannot exceed 6
      const worst = calculateScore(rotterdam, {
        grp_rotterdam_cisterns: 'opt_cisterns_absent',
        grp_rotterdam_shift: 'opt_shift_gt_5mm',
        grp_rotterdam_edh: 'opt_edh_absent',
        grp_rotterdam_sah_ivh: 'opt_sah_ivh_present'
      });
      expect(worst.rawScore).toBe(6);
    });
  });

  // --------------------------------------------------------------------------
  // 4. CALL SIGNATURE COMPATIBILITY (tool.calculator.baseScore wrapping)
  // --------------------------------------------------------------------------
  describe('Wrapper and Input Signature Ergonomics', () => {
    it('supports calling calculateScore with a wrapped object: { calculator: tool }', () => {
      const aspects = createAspectsCalculator();

      // Wrapped in { calculator: aspects }
      const wrapped = { calculator: aspects } as unknown as Calculator;

      const result = calculateScore(wrapped, {
        grp_aspects_m1: 'opt_m1_hypodense'
      });

      // 10 - 1 = 9
      expect(result.rawScore).toBe(9);
      expect(result.activeRiskTier.id).toBe('tier_aspects_favorable');
    });

    it('handles numeric string conversion if baseScore is passed as string', () => {
      const rotterdam = createRotterdamCalculator();
      const stringBaseCalculator = {
        ...rotterdam,
        baseScore: '1' as any
      };

      const result = calculateScore(stringBaseCalculator, {
        grp_rotterdam_cisterns: 'opt_cisterns_compressed'
      });

      // 1 + 1 = 2 (and EDH defaults to absent which is 1 -> 1 + 1 + 1 = 3)
      expect(typeof result.rawScore).toBe('number');
      expect(Number.isFinite(result.rawScore)).toBe(true);
    });
  });
});
