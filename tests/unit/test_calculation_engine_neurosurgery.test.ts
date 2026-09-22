import { describe, it, expect } from 'vitest';
import {
  calculateScore,
  calculateSagittalBalance,
  calculateNomsFramework,
  calculateLawtonYoung,
  calculatePhasesScore
} from '@/engines/calculationEngine';
import {
  CalculationResultSchema,
  type ClinicalTool
} from '@/types/clinical';

describe('Neurosurgery & Spine Specialized Engines Unit Tests', () => {
  // ==========================================================================
  // 1. SAGITTAL BALANCE & SPINOPELVIC PARAMETERS (SRS-SCHWAB)
  // ==========================================================================
  describe('1. Sagittal Balance & Spinopelvic Parameters', () => {
    it('calculates normal physiological alignment (Schwab 0) with zero deformity', () => {
      const result = calculateSagittalBalance({
        pi: 53,
        pt: 13,
        ss: 40,
        ll: 53,
        sva: 20
      });

      expect(CalculationResultSchema.safeParse(result).success).toBe(true);
      expect(result.rawScore).toBe(0); // PI - LL = 53 - 53 = 0°
      expect(result.scoreFormatted).toContain('Schwab 0');
      expect(result.scoreFormatted).toContain('PT: Normal');
      expect(result.scoreFormatted).toContain('SVA: Normal');
      expect(result.scoreFormatted).toContain('Alvo: 44° a 62°');
      expect(result.activeRiskTier.severityLevel).toBe('low');
      expect(result.activeRiskTier.label).toContain('Balanço Sagital Preservado');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Artrodese in situ sem necessidade de osteotomias'
      );
      expect(result.warnings).toBeUndefined(); // |53 - (13 + 40)| = 0 <= 3
    });

    it('detects and warns on geometrical inconsistency when |PI - (PT + SS)| > 3°', () => {
      // Inconsistent: PI = 60, PT = 15, SS = 30 -> PT + SS = 45 != 60 (diff = 15° > 3°)
      const result = calculateSagittalBalance({
        pi: 60,
        pt: 15,
        ss: 30,
        ll: 50,
        sva: 25
      });

      expect(CalculationResultSchema.safeParse(result).success).toBe(true);
      expect(result.warnings).toBeDefined();
      expect(result.warnings?.[0]).toContain('Inconsistência geométrica espinopélvica');
      expect(result.warnings?.[0]).toContain('15.0° > 3°');
      expect(result.warnings?.[0]).toContain('Duval-Beaupère');
    });

    it('does not warn when geometric difference is within 3° tolerance', () => {
      // Consistent: PI = 55, PT = 18, SS = 35 -> PT + SS = 53 (diff = 2° <= 3°)
      const result = calculateSagittalBalance({
        pi: 55,
        pt: 18,
        ss: 35,
        ll: 55,
        sva: 30
      });

      expect(result.warnings).toBeUndefined();
    });

    it('correctly classifies moderate deformity (Schwab +) and recommends Smith-Petersen osteotomy (SPO)', () => {
      // PI-LL = 55 - 40 = 15° (Schwab +: 10-20°)
      // PT = 25° (Moderate: 20-30°)
      // SVA = 65mm (Moderate: 40-95mm)
      const result = calculateSagittalBalance({
        pi: 55,
        pt: 25,
        ss: 30,
        ll: 40,
        sva: 65
      });

      expect(result.rawScore).toBe(15);
      expect(result.scoreFormatted).toContain('Schwab +');
      expect(result.scoreFormatted).toContain('PT: Moderate');
      expect(result.scoreFormatted).toContain('SVA: Moderate');
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
      expect(result.activeRiskTier.label).toContain('Desbalanço Sagital Moderado');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Smith-Petersen (SPO / Schwab Grau II)'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain('ALIF');
    });

    it('correctly classifies severe rigid deformity (Schwab ++) and recommends Pedicle Subtraction Osteotomy (PSO / Schwab III) and VCR', () => {
      // PI-LL = 65 - 35 = 30° (Schwab ++: > 20°)
      // PT = 35° (Severe: > 30°)
      // SVA = 110mm (Severe: > 95mm)
      const result = calculateSagittalBalance({
        pi: 65,
        pt: 35,
        ss: 30,
        ll: 35,
        sva: 110
      });

      expect(result.rawScore).toBe(30);
      expect(result.scoreFormatted).toContain('Schwab ++');
      expect(result.scoreFormatted).toContain('PT: Severe retroversion');
      expect(result.scoreFormatted).toContain('SVA: Severe');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
      expect(result.activeRiskTier.label).toContain('Deformidade Sagital Grave');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Osteotomia de Subtração Pedicular (PSO / Schwab Grau III)'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Vertebrectomia / Ressecção de Coluna Vertebral (VCR / Schwab Grau VI)'
      );
    });

    it('works via generic calculateScore when tool id is calc_sagittal_balance', () => {
      const mockTool: ClinicalTool = {
        id: 'calc_sagittal_balance',
        slug: 'balanco-sagital',
        name: 'Balanço Sagital e Parâmetros Espinopélvicos',
        acronym: 'Balanço Sagital',
        categorySlug: 'coluna',
        summary: 'Calculadora morfométrica de alinhamento sagital',
        evidenceSource: 'SRS-Schwab Adult Spinal Deformity Classification',
        calculationType: 'continuous_formula',
        minPossibleScore: -50,
        maxPossibleScore: 100,
        baseScore: 0,
        radarAxes: [
          { id: 'axis_pi_ll', label: 'Descompasso PI-LL', system: 'Alinhamento', baselineValue: 0, maxAxisValue: 1 },
          { id: 'axis_pt', label: 'Versão Pélvica', system: 'Alinhamento', baselineValue: 0, maxAxisValue: 1 },
          { id: 'axis_sva', label: 'Eixo Vertical Sagital', system: 'Alinhamento', baselineValue: 0, maxAxisValue: 1 }
        ],
        parameterGroups: [],
        riskTiers: []
      };

      const result = calculateScore(mockTool, {
        pi: 50,
        pt: 15,
        ss: 35,
        ll: 48,
        sva: 25
      });

      expect(result.rawScore).toBe(2);
      expect(result.activeRiskTier.severityLevel).toBe('low');
      expect(result.radarValues.axis_pi_ll).toBeCloseTo(2 / 30, 2);
    });
  });

  // ==========================================================================
  // 2. NOMS DECISION FRAMEWORK & BILSKY SCALE
  // ==========================================================================
  describe('2. NOMS Decision Framework & Bilsky Scale', () => {
    it('adjudicates Pathway A: Separation Surgery + SBRT for high-grade Bilsky, radioresistant tumor, and eligible patient', () => {
      const result = calculateNomsFramework({
        bilsky: '2', // High-grade cord compression
        radiosensitivity: 'radioresistant', // e.g. Renal cell, melanoma
        sins: 14, // Unstable
        kps: 80 // Eligible (>= 70%)
      });

      expect(CalculationResultSchema.safeParse(result).success).toBe(true);
      expect(result.rawScore).toBe(4);
      expect(result.scoreFormatted).toContain('Separation Surgery + SBRT');
      expect(result.scoreFormatted).toContain('Bilsky 2');
      expect(result.scoreFormatted).toContain('Resistente');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
      expect(result.activeRiskTier.label).toContain('Separation Surgery + SBRT');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia de Separação ("Separation Surgery")'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'descompressão circunferencial de 2 a 3 mm'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'SBRT hipofracionada (18 a 24 Gy'
      );
      expect(result.activeRiskTier.pharmacologicalActions[0].drugName).toContain('Dexametasona');
    });

    it('adjudicates Pathway B: cEBRT alone for high-grade Bilsky, radiosensitive tumor, and stable spine', () => {
      const result = calculateNomsFramework({
        bilsky: '3', // High-grade cord compression
        radiosensitivity: 'radiosensitive', // e.g. Multiple myeloma, lymphoma
        sins: 4, // Stable
        kps: 80 // Eligible
      });

      expect(result.rawScore).toBe(2);
      expect(result.scoreFormatted).toContain('cEBRT alone');
      expect(result.scoreFormatted).toContain('Sensível');
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Radioterapia Externa Convencional de Urgência (cEBRT: 30 Gy em 10 frações)'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Descompressão cirúrgica aberta dispensada'
      );
    });

    it('adjudicates Pathway B2: cEBRT + Stabilization for high-grade Bilsky, radiosensitive tumor, with unstable spine', () => {
      const result = calculateNomsFramework({
        bilsky: '3',
        radiosensitivity: 'radiosensitive',
        sins: 15, // Unstable
        kps: 80
      });

      expect(result.rawScore).toBe(3);
      expect(result.activeRiskTier.severityLevel).toBe('high');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Estabilização Cirúrgica Instrumentada'
      );
    });

    it('adjudicates Pathway C: Percutaneous Stabilization for low-grade Bilsky with mechanical instability', () => {
      const result = calculateNomsFramework({
        bilsky: '1b', // Low-grade
        radiosensitivity: 'radioresistant',
        sins: 10, // Potentially unstable
        kps: 80
      });

      expect(result.rawScore).toBe(3);
      expect(result.scoreFormatted).toContain('Percutaneous Stabilization');
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cifoplastia com Balão / Vertebroplastia'
      );
    });

    it('adjudicates Pathway D: Palliative Hospice when systemic status is ineligible (KPS < 70%)', () => {
      const result = calculateNomsFramework({
        bilsky: '3',
        radiosensitivity: 'radioresistant',
        sins: 16,
        kps: 40 // Ineligible / terminal
      });

      expect(result.rawScore).toBe(1);
      expect(result.scoreFormatted).toContain('Palliative Hospice');
      expect(result.activeRiskTier.severityLevel).toBe('low');
      expect(result.activeRiskTier.label).toContain('Cuidados Paliativos');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cirurgia descompressiva e reconstrução instrumentada aberta estão formalmente contraindicadas'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Radioterapia Paliativa em Fração Única (8 Gy)'
      );
    });

    it('works via generic calculateScore when tool id is calc_noms', () => {
      const mockTool: ClinicalTool = {
        id: 'calc_noms',
        slug: 'noms-framework',
        name: 'NOMS Framework',
        acronym: 'NOMS',
        categorySlug: 'coluna',
        summary: 'Matriz multidimensional para metástases espinhais',
        evidenceSource: 'Bilsky et al. 2013',
        calculationType: 'branching_decision',
        minPossibleScore: 1,
        maxPossibleScore: 4,
        baseScore: 0,
        radarAxes: [],
        parameterGroups: [],
        riskTiers: []
      };

      const result = calculateScore(mockTool, {
        neurologic: '2',
        oncologic: 'radioresistant',
        mechanical: 14,
        systemic: 90
      });

      expect(result.rawScore).toBe(4);
      expect(result.scoreFormatted).toContain('Separation Surgery + SBRT');
    });
  });

  // ==========================================================================
  // 3. LAWTON-YOUNG SUPPLEMENTARY AVM GRADING SYSTEM
  // ==========================================================================
  describe('3. Lawton-Young Supplementary AVM Grading System', () => {
    it('calculates low surgical risk (2-4 points) with primary resection indication', () => {
      // SM: Size < 3cm (1) + Non-eloquent (0) + Superficial (0) = 1 point
      // LY: Age < 20 (1) + Ruptured (0) + Compact (0) = 1 point
      // Total = 2 points
      const result = calculateLawtonYoung({
        sm_size: '<3',
        sm_eloquence: false,
        sm_drainage: false,
        age: 18,
        ruptured: true,
        compactness: 'compact'
      });

      expect(CalculationResultSchema.safeParse(result).success).toBe(true);
      expect(result.rawScore).toBe(2);
      expect(result.scoreFormatted).toBe('2 pontos (SM 1 + LY 1)');
      expect(result.activeRiskTier.severityLevel).toBe('low');
      expect(result.activeRiskTier.label).toContain('Baixa Complexidade Cirúrgica / Baixo Risco');
      expect(result.activeRiskTier.statisticalOutcome).toContain('< 3% a 5%');
      expect(result.activeRiskTier.statisticalOutcome).toContain('> 95% a 98%');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Indicação Cirúrgica Mandatória / Eletiva de Ressecção Microcirúrgica Primária Completa'
      );
    });

    it('calculates intermediate risk (5-6 points) with multimodal management', () => {
      // SM: Size 3-6cm (2) + Eloquent (1) + Superficial (0) = 3 points
      // LY: Age 30 (2) + Ruptured (0) + Compact (0) = 2 points
      // Total = 5 points
      const result = calculateLawtonYoung({
        sm_size: '3-6',
        sm_eloquence: true,
        sm_drainage: false,
        age: 30,
        ruptured: true,
        compactness: 'compact'
      });

      expect(result.rawScore).toBe(5);
      expect(result.scoreFormatted).toBe('5 pontos (SM 3 + LY 2)');
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
      expect(result.activeRiskTier.label).toContain('Complexidade Cirúrgica Intermediária');
      expect(result.activeRiskTier.statisticalOutcome).toContain('10% a 25%');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Embolização superseletiva pré-operatória estagiada com agentes líquidos não absorvíveis (Onyx ou Squid)'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Radiocirurgia Estereotática (SRS: 18 a 22 Gy)'
      );
    });

    it('calculates prohibitive risk (7-10 points) mandating ARUBA conservative treatment', () => {
      // SM: Size > 6cm (3) + Eloquent (1) + Deep drainage (1) = 5 points
      // LY: Age > 40 (3) + Unruptured (1) + Diffuse (1) = 5 points
      // Total = 10 points
      const result = calculateLawtonYoung({
        sm_size: '>6',
        sm_eloquence: true,
        sm_drainage: true,
        age: 55,
        unruptured: true,
        compactness: 'diffuse'
      });

      expect(result.rawScore).toBe(10);
      expect(result.scoreFormatted).toBe('10 pontos (SM 5 + LY 5)');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
      expect(result.activeRiskTier.label).toContain('Alta Complexidade / Risco Cirúrgico Proibitivo');
      expect(result.activeRiskTier.statisticalOutcome).toContain('> 35% a 50%');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Tratamento Conservador Seguro / Manejo Clínico Expectante (Diretrizes do Ensaio Clínico ARUBA)'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Microcirurgia aberta formalmente contraindicada'
      );
    });

    it('tests risk tier boundary cutoffs: score 4 (low) vs score 5 (intermediate)', () => {
      const score4 = calculateLawtonYoung({ spetzlerMartin: 2, age: 25, ruptured: true, compactness: 'compact' }); // 2 + 2 = 4
      const score5 = calculateLawtonYoung({ spetzlerMartin: 3, age: 25, ruptured: true, compactness: 'compact' }); // 3 + 2 = 5

      expect(score4.rawScore).toBe(4);
      expect(score4.activeRiskTier.severityLevel).toBe('low');

      expect(score5.rawScore).toBe(5);
      expect(score5.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('tests risk tier boundary cutoffs: score 6 (intermediate) vs score 7 (critical)', () => {
      const score6 = calculateLawtonYoung({ spetzlerMartin: 3, age: 45, ruptured: true, compactness: 'compact' }); // 3 + 3 = 6
      const score7 = calculateLawtonYoung({ spetzlerMartin: 4, age: 45, ruptured: true, compactness: 'compact' }); // 4 + 3 = 7

      expect(score6.rawScore).toBe(6);
      expect(score6.activeRiskTier.severityLevel).toBe('intermediate');

      expect(score7.rawScore).toBe(7);
      expect(score7.activeRiskTier.severityLevel).toBe('critical');
    });

    it('works via generic calculateScore when tool id is calc_lawton_young', () => {
      const mockTool: ClinicalTool = {
        id: 'calc_lawton_young',
        slug: 'lawton-young',
        name: 'Spetzler-Martin Suplementar (Lawton-Young)',
        acronym: 'Lawton-Young',
        categorySlug: 'vascular',
        summary: 'Escore de risco de ressecção microcirúrgica de MAVs',
        evidenceSource: 'Lawton et al. 2010',
        calculationType: 'additive_points',
        minPossibleScore: 2,
        maxPossibleScore: 10,
        baseScore: 0,
        radarAxes: [],
        parameterGroups: [],
        riskTiers: []
      };

      const result = calculateScore(mockTool, {
        spetzlerMartin: 3,
        age: 35, // +2
        ruptured: true, // +0
        compactness: 'compact' // +0
      });

      expect(result.rawScore).toBe(5);
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
    });
  });

  // ==========================================================================
  // 4. PHASES SCORE FOR UNRUPTURED INTRACRANIAL ANEURYSMS
  // ==========================================================================
  describe('4. PHASES Aneurysm Rupture Risk Score', () => {
    it('calculates low rupture risk (<= 3 points) with conservative management', () => {
      // P: Other (0) + H: No (0) + A: Age 50 (0) + S: Size 5mm (0) + E: SAH no (0) + S: Site ICA (0) = 0 points
      const result = calculatePhasesScore({
        population: 'other',
        hypertension: false,
        age: 50,
        size: 5.0,
        earlierSah: false,
        site: 'ica'
      });

      expect(CalculationResultSchema.safeParse(result).success).toBe(true);
      expect(result.rawScore).toBe(0);
      expect(result.scoreFormatted).toContain('0 pontos (Risco 5 anos: 0.4%)');
      expect(result.activeRiskTier.severityLevel).toBe('low');
      expect(result.activeRiskTier.label).toContain('Baixo Risco de Ruptura (0 a 3 pontos)');
      expect(result.activeRiskTier.statisticalOutcome).toContain('0.4%');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Tratamento Conservador Seguro de Escolha'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Cessação mandatória do tabagismo'
      );
    });

    it('calculates score 3 (boundary of low risk) with 0.7% risk in 5 years', () => {
      // P: Japan (3) + others 0 = 3 points
      const result = calculatePhasesScore({
        population: 'japan',
        hypertension: false,
        age: 55,
        size: 4.5,
        earlierSah: false,
        site: 'ica'
      });

      expect(result.rawScore).toBe(3);
      expect(result.scoreFormatted).toContain('3 pontos (Risco 5 anos: 0.7%)');
      expect(result.activeRiskTier.severityLevel).toBe('low');
    });

    it('calculates intermediate risk (4 to 7 points) with shared decision making', () => {
      // P: Other (0) + H: Yes (1) + A: <70 (0) + S: Size 8.5mm (3) + E: No (0) + S: ICA (0) = 4 points
      const result = calculatePhasesScore({
        population: 'other',
        hypertension: true,
        age: 60,
        size: 8.5,
        earlierSah: false,
        site: 'ica'
      });

      expect(result.rawScore).toBe(4);
      expect(result.scoreFormatted).toContain('4 pontos (Risco 5 anos: 0.9%)');
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
      expect(result.activeRiskTier.label).toContain('Risco Intermediário (4 a 7 pontos)');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Caso Limítrofe / Tomada de Decisão Compartilhada'
      );
    });

    it('calculates high risk (>= 8 points) with mandatory surgical / interventional indication', () => {
      // P: Other (0) + H: Yes (1) + A: <70 (0) + S: Size 12mm (6) + E: No (0) + S: Site MCA (2) = 9 points
      const result = calculatePhasesScore({
        population: 'other',
        hypertension: true,
        age: 55,
        size: 12.0,
        earlierSah: false,
        site: 'mca'
      });

      expect(result.rawScore).toBe(9);
      expect(result.scoreFormatted).toContain('9 pontos (Risco 5 anos: 4.3%)');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
      expect(result.activeRiskTier.label).toContain('Alto a Muito Alto Risco de Ruptura (8 a 22 pontos)');
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Indicação Cirúrgica Mandatória / Tratamento Intervencionista Eletivo Ativo'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Clipagem Microcirúrgica Aberta'
      );
      expect(result.activeRiskTier.nonPharmacologicalActions[0].interventionalProcedure).toContain(
        'Stent Diversor de Fluxo (Flow Diverter)'
      );
    });

    it('calculates maximum score (22 points) with > 17.8% 5-year rupture risk', () => {
      // P: Finland (5) + H: Yes (1) + A: >=70 (1) + S: >=20mm (10) + E: Yes (1) + S: Posterior (4) = 22 points
      const result = calculatePhasesScore({
        population: 'finland',
        hypertension: true,
        age: 75,
        size: 25.0, // Giant aneurysm
        earlierSah: true,
        site: 'posterior'
      });

      expect(result.rawScore).toBe(22);
      expect(result.scoreFormatted).toContain('22 pontos (Risco 5 anos: > 17.8%)');
      expect(result.activeRiskTier.severityLevel).toBe('critical');
      expect(result.activeRiskTier.statisticalOutcome).toContain('> 17.8%');
    });

    it('tests risk tier boundary cutoffs: score 3 (low) vs score 4 (intermediate)', () => {
      const score3 = calculatePhasesScore({ population: 'japan' }); // 3 pts
      const score4 = calculatePhasesScore({ population: 'japan', hypertension: true }); // 3 + 1 = 4 pts

      expect(score3.rawScore).toBe(3);
      expect(score3.activeRiskTier.severityLevel).toBe('low');

      expect(score4.rawScore).toBe(4);
      expect(score4.activeRiskTier.severityLevel).toBe('intermediate');
    });

    it('tests risk tier boundary cutoffs: score 7 (intermediate) vs score 8 (critical)', () => {
      // Finland (5) + MCA (2) = 7 pts
      const score7 = calculatePhasesScore({ population: 'finland', site: 'mca' });
      // Finland (5) + MCA (2) + HTN (1) = 8 pts
      const score8 = calculatePhasesScore({ population: 'finland', site: 'mca', hypertension: true });

      expect(score7.rawScore).toBe(7);
      expect(score7.activeRiskTier.severityLevel).toBe('intermediate');

      expect(score8.rawScore).toBe(8);
      expect(score8.activeRiskTier.severityLevel).toBe('critical');
    });

    it('works via generic calculateScore when tool id is calc_phases_score', () => {
      const mockTool: ClinicalTool = {
        id: 'calc_phases_score',
        slug: 'phases-score',
        name: 'PHASES Aneurysm Rupture Risk Score',
        acronym: 'PHASES',
        categorySlug: 'vascular',
        summary: 'Predição de risco de ruptura em 5 anos para aneurismas não rotos',
        evidenceSource: 'Greving et al. Lancet Neurol 2014',
        calculationType: 'additive_points',
        minPossibleScore: 0,
        maxPossibleScore: 22,
        baseScore: 0,
        radarAxes: [],
        parameterGroups: [],
        riskTiers: []
      };

      const result = calculateScore(mockTool, {
        size: 8.0, // 3 pts
        hypertension: true // 1 pt -> 4 pts
      });

      expect(result.rawScore).toBe(4);
      expect(result.activeRiskTier.severityLevel).toBe('intermediate');
      expect(result.scoreFormatted).toContain('4 pontos');
    });
  });
});
