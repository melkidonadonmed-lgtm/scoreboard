import {
  type Calculator,
  type ClinicalTool,
  type RiskTier,
  type CalculationResult,
  type ParameterGroup,
  type ParameterOption,
  type SagittalBalanceInputs,
  type NomsInputs,
  type LawtonYoungInputs,
  type PhasesInputs
} from '../types/clinical';

export type {
  SagittalBalanceInputs,
  NomsInputs,
  LawtonYoungInputs,
  PhasesInputs
};

export const SSC_2021_QSOFA_WARNING =
  'O Surviving Sepsis Campaign (SSC 2021) desaconselha formalmente o uso isolado do qSOFA como ferramenta única de triagem ou exclusão de sepse, devido à sua sensibilidade insuficiente (< 60%). Pacientes sépticos graves podem apresentar qSOFA de 0 ou 1 ponto. Recomenda-se a triagem multimodal associando critérios de SIRS, NEWS ou MEWS, e o cálculo obrigatório do SOFA completo diante de qualquer suspeita clínica persistente.';

// ============================================================================
// 1. GENERIC CALCULATION ENGINE
// ============================================================================

/**
 * Executes scoring for any Calculator definition with provided user inputs.
 * Inputs can be mapped by group ID, group slug, or option ID.
 */
export function calculateScore(
  calculator: Calculator,
  inputs: Record<string, any>
): CalculationResult {
  const calc = ((calculator as any)?.calculator ?? calculator) as Calculator;
  const rawBaseScore = (calculator as any)?.calculator?.baseScore ?? calc.baseScore ?? 0;
  let rawScore = typeof rawBaseScore === 'number' ? rawBaseScore : (Number(rawBaseScore) || 0);
  const radarValues: Record<string, number> = {};

  // Initialize all defined radar axes with 0 (normal baseline)
  for (const axis of calc.radarAxes) {
    radarValues[axis.id] = 0;
  }

  // Branching decision specific to Glasgow-P: GCS (3-15) - Pupil Score (0-2)
  if (calc.id === 'calc_glasgow_p' || calc.slug === 'glasgow-p') {
    return calculateGlasgowPFromCalculator(calc, inputs);
  }

  // Delegated handlers for specialized neurosurgical and spine engines
  if (
    calc.id === 'calc_sagittal_balance' ||
    calc.slug === 'balanco-sagital' ||
    calc.slug === 'sagittal-balance' ||
    calc.id === 'calc_spinopelvic_balance'
  ) {
    return calculateSagittalBalance(calc, inputs);
  }

  if (
    calc.id === 'calc_noms' ||
    calc.id === 'calc_noms_bilsky' ||
    calc.slug === 'noms' ||
    calc.slug === 'noms-bilsky' ||
    calc.slug === 'noms-framework'
  ) {
    return calculateNomsFramework(calc, inputs);
  }

  if (
    calc.id === 'calc_lawton_young' ||
    calc.slug === 'lawton-young' ||
    calc.slug === 'spetzler-martin-suplementar' ||
    calc.id === 'calc_spetzler_martin_suplementar'
  ) {
    return calculateLawtonYoung(calc, inputs);
  }

  if (
    calc.id === 'calc_phases' ||
    calc.id === 'calc_phases_score' ||
    calc.slug === 'phases' ||
    calc.slug === 'phases-score'
  ) {
    return calculatePhasesScore(calc, inputs);
  }

  if (
    calc.id === 'calc_vasograde' ||
    calc.slug === 'vasograde' ||
    calc.slug === 'vasograde-dci'
  ) {
    return calculateVasograde(calc, inputs);
  }

  // Process parameter groups
  for (const group of calc.parameterGroups) {
    const selectedOption = resolveSelectedOption(group, inputs);

    if (selectedOption) {
      rawScore += selectedOption.pointValue;
      if (group.radarAxisId) {
        // In case multiple groups map to the same radar axis, take the maximal derangement
        radarValues[group.radarAxisId] = Math.max(
          radarValues[group.radarAxisId] ?? 0,
          selectedOption.radarNormalizedValue
        );
      }
    } else {
      // Check for direct numeric input if applicable
      const numericVal = resolveNumericInputValue(group, inputs);
      if (numericVal !== undefined) {
        rawScore += numericVal;
        if (group.radarAxisId && group.maxAxisValue > 0) {
          const norm = Math.min(
            1,
            Math.max(0, (numericVal - group.normalBaselineValue) / (group.maxAxisValue - group.normalBaselineValue))
          );
          radarValues[group.radarAxisId] = Math.max(radarValues[group.radarAxisId] ?? 0, norm);
        }
      }
    }
  }

  // Clamping score if boundaries are defined
  if (calc.minPossibleScore !== undefined && rawScore < calc.minPossibleScore) {
    rawScore = calc.minPossibleScore;
  }
  if (calc.maxPossibleScore !== undefined && rawScore > calc.maxPossibleScore) {
    rawScore = calc.maxPossibleScore;
  }

  const activeRiskTier = matchRiskTier(calc.riskTiers, rawScore);
  const warnings: string[] = [];

  let sscWarning: string | undefined;
  if (calc.ssc2021Warning || calc.id === 'calc_qsofa' || calc.slug === 'qsofa') {
    sscWarning = SSC_2021_QSOFA_WARNING;
    warnings.push(SSC_2021_QSOFA_WARNING);
  }

  const clinicalWarning = calc.clinicalWarning;
  if (clinicalWarning && !warnings.includes(clinicalWarning)) {
    warnings.push(clinicalWarning);
  }

  const scoreFormatted = Number.isInteger(rawScore)
    ? rawScore.toString()
    : rawScore.toFixed(1);

  return {
    score: rawScore,
    rawScore,
    scoreFormatted,
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning,
    sscWarning,
    warnings: warnings.length > 0 ? warnings : undefined
  };
}

/**
 * Resolves the selected ParameterOption for a given ParameterGroup from user inputs.
 */
function resolveSelectedOption(
  group: ParameterGroup,
  inputs: Record<string, any>
): ParameterOption | undefined {
  // 1. Direct input by group ID or group slug
  const inputValue = inputs[group.id] ?? inputs[group.slug];

  if (typeof inputValue === 'string') {
    const match = group.options.find((opt) => opt.id === inputValue);
    if (match) return match;
  }

  if (typeof inputValue === 'boolean') {
    if (inputValue) {
      return (
        group.options.find((opt) => opt.pointValue > 0 || !opt.isNormalBaseline) ??
        group.options[group.options.length - 1]
      );
    } else {
      return (
        group.options.find((opt) => opt.isNormalBaseline || opt.pointValue === 0) ??
        group.options[0]
      );
    }
  }

  if (typeof inputValue === 'number') {
    // Exact point value match
    const pointMatch = group.options.find((opt) => opt.pointValue === inputValue);
    if (pointMatch) return pointMatch;
  }

  // 2. Check if any option ID in this group is passed as a boolean flag in inputs
  for (const opt of group.options) {
    if (inputs[opt.id] === true) {
      return opt;
    }
  }

  // 3. If no input found, fallback to the baseline option
  return group.options.find((opt) => opt.isNormalBaseline) ?? group.options[0];
}

/**
 * Resolves numeric value if input is given as a number.
 */
function resolveNumericInputValue(
  group: ParameterGroup,
  inputs: Record<string, any>
): number | undefined {
  const val = inputs[group.id] ?? inputs[group.slug];
  if (typeof val === 'number' && !isNaN(val)) {
    return val;
  }
  return undefined;
}

/**
 * Matches a raw score against defined risk tiers.
 */
function matchRiskTier(riskTiers: RiskTier[], score: number): RiskTier {
  if (riskTiers.length === 0) {
    throw new Error('Calculator does not have any risk tiers defined.');
  }

  // 1. Find tier where minScore <= score <= maxScore
  const matched = riskTiers.find((tier) => score >= tier.minScore && score <= tier.maxScore);
  if (matched) {
    return matched;
  }

  // 2. Boundary tolerance (for decimal edges like 4.0 vs 4.5 in Wells)
  for (let i = 0; i < riskTiers.length; i++) {
    const tier = riskTiers[i];
    const nextTier = riskTiers[i + 1];
    if (score >= tier.minScore && nextTier && score < nextTier.minScore) {
      return tier;
    }
  }

  // 3. Fallback to closest tier
  if (score < riskTiers[0].minScore) {
    return riskTiers[0];
  }
  return riskTiers[riskTiers.length - 1];
}

/**
 * Dedicated handler for Glasgow-P within the generic calculator structure:
 * Formula: GCS (3-15) - Pupil Score (0-2) = 1 to 15 points.
 */
function calculateGlasgowPFromCalculator(
  calculator: Calculator,
  inputs: Record<string, any>
): CalculationResult {
  const radarValues: Record<string, number> = {};
  for (const axis of calculator.radarAxes) {
    radarValues[axis.id] = 0;
  }

  let eyeScore = 4;
  let verbScore = 5;
  let motScore = 6;
  let pupilSubtract = 0;

  for (const group of calculator.parameterGroups) {
    const option = resolveSelectedOption(group, inputs);
    if (!option) continue;

    if (group.radarAxisId) {
      radarValues[group.radarAxisId] = option.radarNormalizedValue;
    }

    if (group.id.includes('eye') || group.slug.includes('ocular')) {
      eyeScore = option.pointValue;
    } else if (group.id.includes('verb') || group.slug.includes('verbal')) {
      verbScore = option.pointValue;
    } else if (group.id.includes('mot') || group.slug.includes('motora')) {
      motScore = option.pointValue;
    } else if (group.id.includes('pup') || group.slug.includes('pupil')) {
      pupilSubtract = option.pointValue;
    }
  }

  const gcs = eyeScore + verbScore + motScore;
  const rawScore = Math.max(1, Math.min(15, gcs - pupilSubtract));
  const activeRiskTier = matchRiskTier(calculator.riskTiers, rawScore);

  return {
    score: rawScore,
    rawScore,
    scoreFormatted: rawScore.toString(),
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning: calculator.clinicalWarning,
    warnings: calculator.clinicalWarning ? [calculator.clinicalWarning] : undefined
  };
}

// ============================================================================
// 2. DEDICATED CLINICAL CALCULATORS
// ============================================================================

// ----------------------------------------------------------------------------
// A. qSOFA (Quick Sequential Organ Failure Assessment)
// ----------------------------------------------------------------------------

export interface QsofaInputs {
  respiratoryRateGte22?: boolean;
  gcsLessThan15?: boolean;
  sbpLte100?: boolean;
  respiratoryRate?: number;
  gcs?: number;
  sbp?: number;
}

export interface QsofaResult {
  score: number;
  isHighRisk: boolean;
  riskStratification: string;
  mortalityEstimate: string;
  sscWarning: string;
  warnings: string[];
  criteria: {
    respiratoryRateGte22: boolean;
    gcsLessThan15: boolean;
    sbpLte100: boolean;
  };
}

export function calculateQsofa(inputs: QsofaInputs): QsofaResult {
  const respGte22 =
    inputs.respiratoryRateGte22 ??
    (inputs.respiratoryRate !== undefined ? inputs.respiratoryRate >= 22 : false);

  const gcsLt15 =
    inputs.gcsLessThan15 ??
    (inputs.gcs !== undefined ? inputs.gcs < 15 : false);

  const sbpLte100 =
    inputs.sbpLte100 ??
    (inputs.sbp !== undefined ? inputs.sbp <= 100 : false);

  let score = 0;
  if (respGte22) score += 1;
  if (gcsLt15) score += 1;
  if (sbpLte100) score += 1;

  const isHighRisk = score >= 2;
  const riskStratification = isHighRisk
    ? 'Alto Risco de Sepse / Deterioração Aguda (2 a 3 pontos)'
    : 'Baixo Risco pelo qSOFA (0 a 1 ponto)';

  const mortalityEstimate = isHighRisk
    ? 'Mortalidade intra-hospitalar estimada entre 10% e 25% (aumento de 3 a 14 vezes). Acionar Protocolo de Sepse 1h.'
    : 'Mortalidade intra-hospitalar estimada < 3%. Não exclui sepse: manter monitorização clínica seriada.';

  return {
    score,
    isHighRisk,
    riskStratification,
    mortalityEstimate,
    sscWarning: SSC_2021_QSOFA_WARNING,
    warnings: [SSC_2021_QSOFA_WARNING],
    criteria: {
      respiratoryRateGte22: respGte22,
      gcsLessThan15: gcsLt15,
      sbpLte100: sbpLte100
    }
  };
}

// ----------------------------------------------------------------------------
// B. Full SOFA (Sequential Organ Failure Assessment)
// ----------------------------------------------------------------------------

export interface SofaParameters {
  respiratory?: {
    pao2Fio2Ratio: number;
    isMechanicallyVentilated?: boolean;
  };
  coagulation?: {
    plateletsThousandPerMm3: number;
  };
  hepatic?: {
    totalBilirubinMgDl: number;
  };
  cardiovascular?: {
    mapMmHg?: number;
    dopamineDoseMcgKgMin?: number;
    dobutamineAnyDose?: boolean;
    norepinephrineDoseMcgKgMin?: number;
    epinephrineDoseMcgKgMin?: number;
  };
  neurological?: {
    gcsScore: number;
  };
  renal?: {
    creatinineMgDl: number;
    urineOutputMlPerDay?: number;
  };
}

export interface SofaResult {
  score: number;
  organScores: {
    respiratory: number;
    coagulation: number;
    hepatic: number;
    cardiovascular: number;
    neurological: number;
    renal: number;
  };
  riskStratification: string;
  mortalityEstimate: string;
}

export function calculateFullSofa(params: SofaParameters): SofaResult {
  // 1. Respiratory
  let respScore = 0;
  if (params.respiratory) {
    const pf = params.respiratory.pao2Fio2Ratio;
    const vent = !!params.respiratory.isMechanicallyVentilated;
    if (pf < 100 && vent) respScore = 4;
    else if (pf < 200 && vent) respScore = 3;
    else if (pf < 300) respScore = 2;
    else if (pf < 400) respScore = 1;
    else respScore = 0;
  }

  // 2. Coagulation
  let coagScore = 0;
  if (params.coagulation) {
    const p = params.coagulation.plateletsThousandPerMm3;
    if (p < 20) coagScore = 4;
    else if (p < 50) coagScore = 3;
    else if (p < 100) coagScore = 2;
    else if (p < 150) coagScore = 1;
    else coagScore = 0;
  }

  // 3. Hepatic
  let liverScore = 0;
  if (params.hepatic) {
    const b = params.hepatic.totalBilirubinMgDl;
    if (b >= 12.0) liverScore = 4;
    else if (b >= 6.0) liverScore = 3;
    else if (b >= 2.0) liverScore = 2;
    else if (b >= 1.2) liverScore = 1;
    else liverScore = 0;
  }

  // 4. Cardiovascular
  let cvScore = 0;
  if (params.cardiovascular) {
    const {
      mapMmHg,
      dopamineDoseMcgKgMin = 0,
      dobutamineAnyDose = false,
      norepinephrineDoseMcgKgMin = 0,
      epinephrineDoseMcgKgMin = 0
    } = params.cardiovascular;

    if (
      dopamineDoseMcgKgMin > 15 ||
      norepinephrineDoseMcgKgMin > 0.1 ||
      epinephrineDoseMcgKgMin > 0.1
    ) {
      cvScore = 4;
    } else if (
      dopamineDoseMcgKgMin > 5 ||
      (norepinephrineDoseMcgKgMin > 0 && norepinephrineDoseMcgKgMin <= 0.1) ||
      (epinephrineDoseMcgKgMin > 0 && epinephrineDoseMcgKgMin <= 0.1)
    ) {
      cvScore = 3;
    } else if (
      (dopamineDoseMcgKgMin > 0 && dopamineDoseMcgKgMin <= 5) ||
      dobutamineAnyDose
    ) {
      cvScore = 2;
    } else if (mapMmHg !== undefined && mapMmHg < 70) {
      cvScore = 1;
    } else {
      cvScore = 0;
    }
  }

  // 5. Neurological
  let cnsScore = 0;
  if (params.neurological) {
    const gcs = params.neurological.gcsScore;
    if (gcs < 6) cnsScore = 4;
    else if (gcs <= 9) cnsScore = 3;
    else if (gcs <= 12) cnsScore = 2;
    else if (gcs <= 14) cnsScore = 1;
    else cnsScore = 0;
  }

  // 6. Renal
  let renalScore = 0;
  if (params.renal) {
    const cr = params.renal.creatinineMgDl;
    const uo = params.renal.urineOutputMlPerDay;

    if (cr >= 5.0 || (uo !== undefined && uo < 200)) renalScore = 4;
    else if ((cr >= 3.5 && cr <= 4.9) || (uo !== undefined && uo < 500)) renalScore = 3;
    else if (cr >= 2.0) renalScore = 2;
    else if (cr >= 1.2) renalScore = 1;
    else renalScore = 0;
  }

  const score = respScore + coagScore + liverScore + cvScore + cnsScore + renalScore;

  let riskStratification = '';
  let mortalityEstimate = '';

  if (score <= 1) {
    riskStratification = 'Disfunção Orgânica Ausente ou Basal (0 a 1 ponto)';
    mortalityEstimate = 'Mortalidade basal de UTI < 5%. Não preenche critério de sepse.';
  } else if (score <= 6) {
    riskStratification = 'Disfunção Orgânica Leve a Moderada / Sepse Inicial (2 a 6 pontos)';
    mortalityEstimate = 'Mortalidade estimada de 10% a 20%. Aplicar pacote de 1h do SSC.';
  } else if (score <= 11) {
    riskStratification = 'Disfunção Orgânica Grave (7 a 11 pontos)';
    mortalityEstimate = 'Mortalidade estimada de 30% a 50%. Suporte intensivo e vasopressores em UTI.';
  } else {
    riskStratification = 'Falência Multiorgânica Catastrófica (12 a 24 pontos)';
    mortalityEstimate = 'Mortalidade superior a 60% a 90%. Suporte avançado multiorgânico nível 3.';
  }

  return {
    score,
    organScores: {
      respiratory: respScore,
      coagulation: coagScore,
      hepatic: liverScore,
      cardiovascular: cvScore,
      neurological: cnsScore,
      renal: renalScore
    },
    riskStratification,
    mortalityEstimate
  };
}

// ----------------------------------------------------------------------------
// C. Wells PE (Tromboembolismo Pulmonar)
// ----------------------------------------------------------------------------

export interface WellsPeCriteria {
  dvtSignsOrSymptoms?: boolean; // +3.0
  peMoreLikelyThanAlternative?: boolean; // +3.0
  heartRateGt100?: boolean; // +1.5
  immobilizationOrSurgery?: boolean; // +1.5
  previousVte?: boolean; // +1.5
  hemoptysis?: boolean; // +1.0
  malignancy?: boolean; // +1.0
}

export interface WellsPeResult {
  score: number;
  dichotomousRisk: 'unlikely' | 'likely';
  threeTierRisk: 'low' | 'intermediate' | 'high';
  dichotomousLabel: string;
  threeTierLabel: string;
  ageAdjustedDdimerCutoff: number;
  recommendation: string;
}

/**
 * Calculates Age-adjusted D-dimer cutoff (ESC guideline).
 * Age > 50 -> Age * 10 mcg/L FEU; Age <= 50 -> 500 mcg/L FEU.
 */
export function calculateAgeAdjustedDdimerCutoff(age: number): number {
  if (age > 50) {
    return Math.round(age * 10);
  }
  return 500;
}

export function calculateWellsPe(
  criteria: WellsPeCriteria,
  patientAge = 50
): WellsPeResult {
  let score = 0;
  if (criteria.dvtSignsOrSymptoms) score += 3.0;
  if (criteria.peMoreLikelyThanAlternative) score += 3.0;
  if (criteria.heartRateGt100) score += 1.5;
  if (criteria.immobilizationOrSurgery) score += 1.5;
  if (criteria.previousVte) score += 1.5;
  if (criteria.hemoptysis) score += 1.0;
  if (criteria.malignancy) score += 1.0;

  const dichotomousRisk = score <= 4.0 ? 'unlikely' : 'likely';
  const dichotomousLabel =
    score <= 4.0
      ? 'TEP Improvável (<= 4,0 pontos)'
      : 'TEP Provável (> 4,0 pontos)';

  let threeTierRisk: 'low' | 'intermediate' | 'high';
  let threeTierLabel = '';
  if (score < 2.0) {
    threeTierRisk = 'low';
    threeTierLabel = 'Baixa Probabilidade Clínica (< 2,0 pontos)';
  } else if (score <= 6.0) {
    threeTierRisk = 'intermediate';
    threeTierLabel = 'Probabilidade Clínica Intermediária (2,0 a 6,0 pontos)';
  } else {
    threeTierRisk = 'high';
    threeTierLabel = 'Alta Probabilidade Clínica (> 6,0 pontos)';
  }

  const ddimerCutoff = calculateAgeAdjustedDdimerCutoff(patientAge);

  const recommendation =
    score <= 4.0
      ? `TEP Improvável (prevalência ~8%). Aplicar critérios PERC. Se PERC positivo, dosar D-Dímero de alta sensibilidade (ponto de corte ajustado pela idade: ${ddimerCutoff} mcg/L). Se D-Dímero normal, descarta-se TEP sem Angio-TC.`
      : `TEP Provável (prevalência > 30-40%). Encaminhar DIRETAMENTE para Angiotomografia de Artérias Pulmonares (Angio-TC). Contraindicada a dosagem de D-Dímero. Se atraso previsto > 4h, iniciar anticoagulação plena empírica.`;

  return {
    score,
    dichotomousRisk,
    threeTierRisk,
    dichotomousLabel,
    threeTierLabel,
    ageAdjustedDdimerCutoff: ddimerCutoff,
    recommendation
  };
}

// ----------------------------------------------------------------------------
// D. Glasgow-P (Glasgow Coma Scale with Pupil Reactivity)
// ----------------------------------------------------------------------------

export interface GlasgowPInputs {
  eye: number; // 1 to 4
  verbal: number; // 1 to 5
  motor: number; // 1 to 6
  unreactivePupils: number; // 0, 1, or 2
}

export interface GlasgowPResult {
  gcs: number;
  pupilScore: number;
  score: number;
  severity: 'mild' | 'moderate' | 'severe';
  severityLabel: string;
  recommendation: string;
}

export function calculateGlasgowP(inputs: GlasgowPInputs): GlasgowPResult {
  const eye = Math.max(1, Math.min(4, Math.round(inputs.eye)));
  const verbal = Math.max(1, Math.min(5, Math.round(inputs.verbal)));
  const motor = Math.max(1, Math.min(6, Math.round(inputs.motor)));
  const unreactive = Math.max(0, Math.min(2, Math.round(inputs.unreactivePupils)));

  const gcs = eye + verbal + motor;
  const score = Math.max(1, Math.min(15, gcs - unreactive));

  let severity: 'mild' | 'moderate' | 'severe';
  let severityLabel = '';
  let recommendation = '';

  if (score >= 13) {
    severity = 'mild';
    severityLabel = 'TCE / Comprometimento Leve (13 a 15 pontos)';
    recommendation = 'Observação clínica seriada. Avaliar TC de crânio conforme critérios de Ottawa/Canadense.';
  } else if (score >= 9) {
    severity = 'moderate';
    severityLabel = 'TCE / Comprometimento Moderado (9 a 12 pontos)';
    recommendation = 'TC de crânio urgente sem contraste. Monitorização neurológica contínua em leito semi-intensivo.';
  } else {
    severity = 'severe';
    severityLabel = 'TCE / Coma Grave (1 a 8 pontos)';
    recommendation = 'Intubação Orotraqueal Imediata com Sequência Rápida (IOT). Metas neuroprotetoras estritas: PAM >= 80 mmHg, PaCO2 35-40 mmHg.';
  }

  return {
    gcs,
    pupilScore: unreactive,
    score,
    severity,
    severityLabel,
    recommendation
  };
}

// ----------------------------------------------------------------------------
// E. FOUR Score (Full Outline of UnResponsiveness)
// ----------------------------------------------------------------------------

export interface FourScoreInputs {
  eye: number; // 0 to 4
  motor: number; // 0 to 4
  brainstem: number; // 0 to 4
  respiration: number; // 0 to 4
  isVentilated?: boolean;
}

export interface FourScoreResult {
  score: number;
  severity: 'mild' | 'moderate' | 'severe';
  severityLabel: string;
  isBrainDeathAlert: boolean;
  breakdown: {
    eye: number;
    motor: number;
    brainstem: number;
    respiration: number;
  };
  recommendation: string;
}

export function calculateFourScore(inputs: FourScoreInputs): FourScoreResult {
  const eye = Math.max(0, Math.min(4, Math.round(inputs.eye)));
  const motor = Math.max(0, Math.min(4, Math.round(inputs.motor)));
  const brainstem = Math.max(0, Math.min(4, Math.round(inputs.brainstem)));
  const respiration = Math.max(0, Math.min(4, Math.round(inputs.respiration)));

  const score = eye + motor + brainstem + respiration;
  const isBrainDeathAlert = score === 0;

  let severity: 'mild' | 'moderate' | 'severe';
  let severityLabel = '';
  let recommendation = '';

  if (score >= 13) {
    severity = 'mild';
    severityLabel = 'Disfunção Leve a Moderada (13 a 16 pontos)';
    recommendation = 'Baixo risco de deterioração em 48h (< 5%). Manter vigilância neurológica.';
  } else if (score >= 8) {
    severity = 'moderate';
    severityLabel = 'Coma Moderado (8 a 12 pontos)';
    recommendation = 'Risco intermediário de complicações e necessidade de suporte ventilatório avançado.';
  } else {
    severity = 'severe';
    severityLabel = 'Coma Profundo / Alto Risco de Óbito (0 a 7 pontos)';
    recommendation = isBrainDeathAlert
      ? 'FOUR = 0 persistente sem sedação farmacológica e sob normotermia aciona protocolo formal de Morte Encefálica (CFM nº 2.173/2017).'
      : 'Grave comprometimento neurológico com alta mortalidade hospitalar (> 75%). Suporte intensivo neurocrítico imediato.';
  }

  return {
    score,
    severity,
    severityLabel,
    isBrainDeathAlert,
    breakdown: { eye, motor, brainstem, respiration },
    recommendation
  };
}

// ----------------------------------------------------------------------------
// F. Ranson Criteria (Pancreatite Aguda)
// ----------------------------------------------------------------------------

export interface RansonCriteria {
  // Na admissão (0h)
  ageExceeded?: boolean; // >55 não biliar, >70 biliar
  wbcExceeded?: boolean; // >16k não biliar, >18k biliar
  glucoseExceeded?: boolean; // >200 não biliar, >220 biliar
  ldhExceeded?: boolean; // >350 não biliar, >400 biliar
  astExceeded?: boolean; // >250 em ambos

  // Em 48 horas
  hctDropExceeded?: boolean; // Queda Hct > 10%
  bunRiseExceeded?: boolean; // BUN aumento > 5 mg/dL (ou > 2 em biliar)
  calciumLow?: boolean; // Ca < 8,0 mg/dL
  pao2Low?: boolean; // PaO2 < 60 mmHg
  baseDeficitExceeded?: boolean; // BE < -4 mEq/L (ou < -5 em biliar)
  fluidSequestrationExceeded?: boolean; // > 6.000 mL (ou > 4.000 mL em biliar)
}

export interface RansonResult {
  score: number;
  isBiliary: boolean;
  severity: 'mild' | 'moderate' | 'severe';
  severityLabel: string;
  mortalityEstimate: string;
  criteriaMetCount: number;
}

export function calculateRanson(
  criteria: RansonCriteria,
  isBiliary = false
): RansonResult {
  let score = 0;
  if (criteria.ageExceeded) score += 1;
  if (criteria.wbcExceeded) score += 1;
  if (criteria.glucoseExceeded) score += 1;
  if (criteria.ldhExceeded) score += 1;
  if (criteria.astExceeded) score += 1;
  if (criteria.hctDropExceeded) score += 1;
  if (criteria.bunRiseExceeded) score += 1;
  if (criteria.calciumLow) score += 1;
  if (criteria.pao2Low) score += 1;
  if (criteria.baseDeficitExceeded) score += 1;
  if (criteria.fluidSequestrationExceeded) score += 1;

  let severity: 'mild' | 'moderate' | 'severe';
  let severityLabel = '';
  let mortalityEstimate = '';

  if (score <= 2) {
    severity = 'mild';
    severityLabel = 'Pancreatite Aguda Leve (0 a 2 pontos)';
    mortalityEstimate = 'Mortalidade estimada < 1%. Ressuscitação com RL 150-200 mL/h e realimentação precoce.';
  } else if (score <= 5) {
    severity = 'moderate';
    severityLabel = 'Pancreatite Potencialmente Grave (3 a 5 pontos)';
    mortalityEstimate = 'Mortalidade estimada entre 10% e 20%. Ressuscitação volêmica vigorosa em Semi-UTI / UTI.';
  } else {
    severity = 'severe';
    severityLabel = 'Pancreatite Aguda Grave / Fulminante (6 a 11 pontos)';
    mortalityEstimate = 'Mortalidade excede 50% a 90%. Vaga imediata em UTI, suporte vasopressor e TC entre 72-96h.';
  }

  return {
    score,
    isBiliary,
    severity,
    severityLabel,
    mortalityEstimate,
    criteriaMetCount: score
  };
}

// ----------------------------------------------------------------------------
// G. BISAP Score (Bedside Index for Severity in Acute Pancreatitis)
// ----------------------------------------------------------------------------

export interface BisapCriteria {
  bunElevated?: boolean; // BUN > 25 mg/dL (ou Ureia > 53.5 mg/dL)
  bunMgDl?: number;
  ureiaMgDl?: number;
  impairedMentalStatus?: boolean; // Glasgow < 15
  sirsCriteriaGte2?: boolean; // >= 2 critérios de SIRS
  ageGt60?: boolean; // Idade > 60 anos
  pleuralEffusion?: boolean; // Derrame pleural presente
}

export interface BisapResult {
  score: number;
  severity: 'low' | 'high';
  severityLabel: string;
  mortalityEstimate: string;
  criteriaMet: {
    bunElevated: boolean;
    impairedMentalStatus: boolean;
    sirsCriteriaGte2: boolean;
    ageGt60: boolean;
    pleuralEffusion: boolean;
  };
}

/**
 * Converts Brazilian serum Ureia to Blood Urea Nitrogen (BUN):
 * BUN (mg/dL) = Ureia (mg/dL) / 2.14
 */
export function convertUreiaToBun(ureiaMgDl: number): number {
  return ureiaMgDl / 2.14;
}

/**
 * Converts BUN to Brazilian serum Ureia:
 * Ureia (mg/dL) = BUN (mg/dL) * 2.14
 */
export function convertBunToUreia(bunMgDl: number): number {
  return bunMgDl * 2.14;
}

export function calculateBisap(inputs: BisapCriteria): BisapResult {
  let bunElevated = !!inputs.bunElevated;
  if (inputs.bunMgDl !== undefined) {
    bunElevated = inputs.bunMgDl > 25;
  } else if (inputs.ureiaMgDl !== undefined) {
    bunElevated = inputs.ureiaMgDl > 53.5;
  }

  const impairedMental = !!inputs.impairedMentalStatus;
  const sirs = !!inputs.sirsCriteriaGte2;
  const age = !!inputs.ageGt60;
  const pleural = !!inputs.pleuralEffusion;

  let score = 0;
  if (bunElevated) score += 1;
  if (impairedMental) score += 1;
  if (sirs) score += 1;
  if (age) score += 1;
  if (pleural) score += 1;

  const isHigh = score >= 3;
  const severity = isHigh ? 'high' : 'low';
  const severityLabel = isHigh
    ? 'BISAP 3 a 5 pontos (Alto Risco de Gravidade / Falência)'
    : 'BISAP 0 a 2 pontos (Baixo Risco)';

  const mortalityEstimate = isHigh
    ? 'Alto risco de necrose pancreática e falência orgânica (mortalidade estimada de 15% a 30%). Vaga imediata em UTI.'
    : 'Baixo risco de falência orgânica persistente (mortalidade hospitalar estimada < 2%).';

  return {
    score,
    severity,
    severityLabel,
    mortalityEstimate,
    criteriaMet: {
      bunElevated,
      impairedMentalStatus: impairedMental,
      sirsCriteriaGte2: sirs,
      ageGt60: age,
      pleuralEffusion: pleural
    }
  };
}

// ============================================================================
// 3. NEUROSURGERY & SPINE SPECIALIZED CALCULATION ENGINES
// ============================================================================

/**
 * Helper to resolve numeric parameters from inputs supporting multiple synonyms and option names.
 */
function extractNumeric(inputs: Record<string, any>, keys: string[], fallback: number): number {
  for (const k of keys) {
    const val = inputs[k];
    if (val !== undefined && val !== null && val !== '') {
      const num = typeof val === 'number' ? val : parseFloat(val);
      if (!isNaN(num)) return num;
    }
  }
  return fallback;
}

// ----------------------------------------------------------------------------
// H. Sagittal Balance & Spinopelvic Parameters (Balanço Sagital / SRS-Schwab)
// ----------------------------------------------------------------------------

export interface SagittalBalanceDetails {
  pi: number;
  pt: number;
  ss: number;
  ll: number;
  sva: number;
  geometricSum: number;
  geometricDiff: number;
  isGeometricConsistent: boolean;
  mismatchPiLl: number;
  targetLordosisMin: number;
  targetLordosisMax: number;
  targetLordosisIdeal: number;
  schwabMismatchModifier: 'Schwab 0' | 'Schwab +' | 'Schwab ++';
  schwabPtModifier: 'Normal' | 'Moderate' | 'Severe retroversion';
  schwabSvaModifier: 'Normal' | 'Moderate' | 'Severe';
  osteotomyRecommendation: string;
}

export function calculateSagittalBalance(inputs: Record<string, any>): CalculationResult;
export function calculateSagittalBalance(calc: ClinicalTool, inputs: Record<string, any>): CalculationResult;
export function calculateSagittalBalance(
  calcOrInputs: ClinicalTool | Record<string, any>,
  maybeInputs?: Record<string, any>
): CalculationResult {
  let calc: ClinicalTool | undefined;
  let inputs: Record<string, any>;

  if (maybeInputs !== undefined) {
    calc = calcOrInputs as ClinicalTool;
    inputs = maybeInputs;
  } else if (
    calcOrInputs &&
    typeof calcOrInputs === 'object' &&
    'parameterGroups' in calcOrInputs
  ) {
    calc = calcOrInputs as ClinicalTool;
    inputs = {};
  } else {
    calc = undefined;
    inputs = (calcOrInputs as Record<string, any>) || {};
  }

  // Extract continuous spinopelvic parameters
  const pi = extractNumeric(inputs, ['pi', 'PI', 'pelvic_incidence', 'pelvicIncidence', 'input_pi', 'grp_sagittal_pi'], 53);
  const pt = extractNumeric(inputs, ['pt', 'PT', 'pelvic_tilt', 'pelvicTilt', 'input_pt', 'grp_sagittal_pt'], 13);
  const ss = extractNumeric(inputs, ['ss', 'SS', 'sacral_slope', 'sacralSlope', 'input_ss', 'grp_sagittal_ss'], 40);
  const ll = extractNumeric(inputs, ['ll', 'LL', 'lumbar_lordosis', 'lumbarLordosis', 'input_ll', 'grp_sagittal_ll'], 53);
  const sva = extractNumeric(inputs, ['sva', 'SVA', 'sagittal_vertical_axis', 'sagittalVerticalAxis', 'input_sva', 'grp_sagittal_sva'], 20);

  // Geometric identity: PI = PT + SS (Warn if |PI - (PT + SS)| > 3°)
  const geometricSum = pt + ss;
  const geometricDiff = Math.abs(pi - geometricSum);
  const isGeometricConsistent = Math.round(geometricDiff * 10) / 10 <= 3.0;

  const warnings: string[] = [];
  if (!isGeometricConsistent) {
    warnings.push(
      `Inconsistência geométrica espinopélvica: |PI - (PT + SS)| = ${geometricDiff.toFixed(1)}° > 3°. Pela identidade de Duval-Beaupère (PI = PT + SS), a incidência pélvica deve equivaler à soma da versão pélvica com a inclinação sacral. Recomenda-se recalibração da demarcação radiográfica do platô de S1 ou do centro das cabeças femorais.`
    );
  }

  // Spinopelvic mismatch: PI - LL
  const mismatchPiLl = Math.round((pi - ll) * 10) / 10;

  // Target Lumbar Lordosis: LL_target = PI ± 9°
  const targetLordosisMin = Math.round((pi - 9) * 10) / 10;
  const targetLordosisMax = Math.round((pi + 9) * 10) / 10;
  const targetLordosisIdeal = Math.round((pi + 5) * 10) / 10;

  // SRS-Schwab Deformity Modifiers
  // PI - LL modifier: < 10° (Schwab 0), 10-20° (Schwab +), > 20° (Schwab ++)
  let schwabMismatchModifier: 'Schwab 0' | 'Schwab +' | 'Schwab ++';
  if (mismatchPiLl < 10) {
    schwabMismatchModifier = 'Schwab 0';
  } else if (mismatchPiLl <= 20) {
    schwabMismatchModifier = 'Schwab +';
  } else {
    schwabMismatchModifier = 'Schwab ++';
  }

  // PT modifier: < 20° (Normal), 20-30° (Moderate), > 30° (Severe retroversion)
  let schwabPtModifier: 'Normal' | 'Moderate' | 'Severe retroversion';
  if (pt < 20) {
    schwabPtModifier = 'Normal';
  } else if (pt <= 30) {
    schwabPtModifier = 'Moderate';
  } else {
    schwabPtModifier = 'Severe retroversion';
  }

  // SVA modifier: < 40mm (Normal), 40-95mm (Moderate), > 95mm (Severe)
  let schwabSvaModifier: 'Normal' | 'Moderate' | 'Severe';
  if (sva < 40) {
    schwabSvaModifier = 'Normal';
  } else if (sva <= 95) {
    schwabSvaModifier = 'Moderate';
  } else {
    schwabSvaModifier = 'Severe';
  }

  // Surgical Osteotomy Recommendations (SPO / Schwab II, PSO / Schwab III, VCR)
  let osteotomyRecommendation = '';
  let activeSeverity: 'low' | 'intermediate' | 'high' | 'critical';
  let tierId: string;
  let tierLabel: string;
  let tierColor: string;
  let statisticalOutcome: string;

  const isSevere = mismatchPiLl > 20 || pt > 30 || sva > 95;
  const isModerate = !isSevere && (mismatchPiLl >= 10 || pt >= 20 || sva >= 40);

  if (isSevere) {
    activeSeverity = 'critical';
    tierId = 'tier_sagittal_severe';
    tierLabel = 'Deformidade Sagital Grave (SRS-Schwab ++) - Indicação de Osteotomia de Três Colunas';
    tierColor = '#dc2626';
    osteotomyRecommendation =
      'Deformidade sagital rígida grave (SRS-Schwab ++). Indicação de Osteotomia de Subtração Pedicular (PSO / Schwab Grau III) em L3 ou L4 (ganho de 30° a 35° de lordose focal angular) associada a cages lordóticos anteriores/oblíquos (ALIF/OLIF de 15°-20°) ou Vertebrectomia / Ressecção de Coluna Vertebral (VCR / Schwab Grau VI) para cifose angular rígida severa multiapical.';
    statisticalOutcome =
      'Desalinhamento sagital severo associado a incapacidade funcional grave (ODI > 40-50), dor lombar incapacitante, fadiga postural e elevado risco de pseudoartrose/falha mecânica de material caso realizada artrodese sem restauração da lordose.';
  } else if (isModerate) {
    activeSeverity = 'intermediate';
    tierId = 'tier_sagittal_moderate';
    tierLabel = 'Desbalanço Sagital Moderado (SRS-Schwab +) - Indicação de Osteotomias de Smith-Petersen';
    tierColor = '#f59e0b';
    osteotomyRecommendation =
      'Desbalanço sagital moderado (SRS-Schwab +). Correção moderada necessária (~10° a 15° de lordose adicional). Indicação de Osteotomias de Smith-Petersen (SPO / Schwab Grau II) em múltiplos níveis (~5° a 10° por nível) associadas a cages intersomáticos anteriores com hiperlordose (ALIF ou OLIF de 15° a 20°).';
    statisticalOutcome =
      'Desbalanço compensado por retroversão pélvica e flexão de joelhos. Alto risco de progressão de deformidade e sobrecarga degenerativa em níveis adjacentes sem correção cirúrgica equilibrada.';
  } else {
    activeSeverity = 'low';
    tierId = 'tier_sagittal_normal';
    tierLabel = 'Balanço Sagital Preservado (SRS-Schwab 0) - Artrodese In Situ sem Osteotomia Maior';
    tierColor = '#10b981';
    osteotomyRecommendation =
      'Balanço sagital preservado (SRS-Schwab 0). Artrodese in situ sem necessidade de osteotomias desrotacionais ou angulares maiores. Manter alinhamento fisiológico com lordose anatômica.';
    statisticalOutcome =
      'Alinhamento espinopélvico e sagital fisiológico. Risco biomecânico mínimo de falha de ancoragem ou doença de nível adjacente.';
  }

  // Active Risk Tier resolution
  let activeRiskTier: RiskTier;
  if (calc?.riskTiers && calc.riskTiers.length > 0) {
    const matched = calc.riskTiers.find((t) => t.severityLevel === activeSeverity) ??
      calc.riskTiers.find((t) => mismatchPiLl >= t.minScore && mismatchPiLl <= t.maxScore) ??
      calc.riskTiers[0];
    activeRiskTier = {
      ...matched,
      statisticalOutcome: `${matched.statisticalOutcome} ${statisticalOutcome}`,
      nonPharmacologicalActions: [
        {
          id: 'action_sagittal_osteotomy',
          recommendationTitle: 'Recomendação de Osteotomia e Correção Sagital',
          dispositionTarget: isSevere ? 'Centro Cirúrgico / UTI de Coluna' : 'Centro Cirúrgico / Enfermaria Especializada',
          monitoringPlan: 'Radiografia panorâmica total da coluna (espinografia perfil) pré e pós-operatória com mensuração dos ângulos de Cobb, SVA e parâmetros pélvicos.',
          interventionalProcedure: osteotomyRecommendation
        },
        ...matched.nonPharmacologicalActions
      ]
    };
  } else {
    activeRiskTier = {
      id: tierId,
      label: tierLabel,
      severityLevel: activeSeverity,
      minScore: isSevere ? 21 : isModerate ? 10 : -50,
      maxScore: isSevere ? 100 : isModerate ? 20 : 9.9,
      statisticalOutcome,
      colorHex: tierColor,
      pharmacologicalActions: [
        {
          id: 'rx_sagittal_analgesia',
          drugName: 'Cefazolina Sódica (Profilaxia Cirúrgica de Coluna)',
          dosage: '2 g IV na indução (3 g se peso > 120 kg), repique de 1 g a cada 4 horas intraoperatórias',
          route: 'Intravenosa',
          frequency: 'Dose única pré-incisão com repiques'
        }
      ],
      nonPharmacologicalActions: [
        {
          id: 'action_sagittal_osteotomy',
          recommendationTitle: 'Recomendação de Osteotomia e Correção Sagital',
          dispositionTarget: isSevere ? 'Centro Cirúrgico / UTI de Coluna' : 'Centro Cirúrgico / Enfermaria Especializada',
          monitoringPlan: 'Espinografia perfil pós-operatória imediata para cálculo de SVA e lordose residual.',
          interventionalProcedure: osteotomyRecommendation
        }
      ]
    };
  }

  // Radar values mapping
  const radarValues: Record<string, number> = {};
  if (calc?.radarAxes) {
    for (const axis of calc.radarAxes) {
      radarValues[axis.id] = 0;
    }
  }
  const normPiLl = Math.min(1, Math.max(0, mismatchPiLl / 30));
  const normPt = Math.min(1, Math.max(0, (pt - 10) / 30));
  const normSva = Math.min(1, Math.max(0, sva / 120));

  radarValues['axis_pi_ll'] = normPiLl;
  radarValues['axis_sb_pi_ll'] = normPiLl;
  radarValues['axis_pt'] = normPt;
  radarValues['axis_sb_pt'] = normPt;
  radarValues['axis_sva'] = normSva;
  radarValues['axis_sb_sva'] = normSva;
  radarValues['axis_sagittal_deformity'] = isSevere ? 1.0 : isModerate ? 0.6 : 0.1;

  const rawScore = mismatchPiLl;
  const scoreFormatted = `${mismatchPiLl >= 0 ? '+' : ''}${mismatchPiLl.toFixed(1)}° (${schwabMismatchModifier}, PT: ${schwabPtModifier}, SVA: ${schwabSvaModifier}; Alvo: ${targetLordosisMin}° a ${targetLordosisMax}°, ideal: ${targetLordosisIdeal}°)`;

  if (calc?.clinicalWarning && !warnings.includes(calc.clinicalWarning)) {
    warnings.push(calc.clinicalWarning);
  }

  return {
    score: rawScore,
    rawScore,
    scoreFormatted,
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning: calc?.clinicalWarning,
    warnings: warnings.length > 0 ? warnings : undefined
  };
}

// ----------------------------------------------------------------------------
// I. NOMS Decision Framework & Bilsky Scale for Spine Metastases
// ----------------------------------------------------------------------------

export function calculateNomsFramework(inputs: Record<string, any>): CalculationResult;
export function calculateNomsFramework(calc: ClinicalTool, inputs: Record<string, any>): CalculationResult;
export function calculateNomsFramework(
  calcOrInputs: ClinicalTool | Record<string, any>,
  maybeInputs?: Record<string, any>
): CalculationResult {
  let calc: ClinicalTool | undefined;
  let inputs: Record<string, any>;

  if (maybeInputs !== undefined) {
    calc = calcOrInputs as ClinicalTool;
    inputs = maybeInputs;
  } else if (
    calcOrInputs &&
    typeof calcOrInputs === 'object' &&
    'parameterGroups' in calcOrInputs
  ) {
    calc = calcOrInputs as ClinicalTool;
    inputs = {};
  } else {
    calc = undefined;
    inputs = (calcOrInputs as Record<string, any>) || {};
  }

  // 1. Neurologic: Bilsky ESCC (0, 1a, 1b, 1c, 2, 3)
  let bilskyStr = '0';
  const neuroVal = inputs.neurologic ?? inputs.bilsky ?? inputs.escc ?? inputs.grp_noms_neurologic ?? inputs.bilskyGrade;
  if (typeof neuroVal === 'string') {
    const match = neuroVal.match(/(0|1a|1b|1c|2|3)/i);
    if (match) bilskyStr = match[1].toLowerCase();
  } else if (typeof neuroVal === 'number') {
    bilskyStr = neuroVal.toString();
  } else {
    for (const b of ['3', '2', '1c', '1b', '1a', '0']) {
      if (inputs[`opt_bilsky_${b}`] || inputs[`bilsky_${b}`]) {
        bilskyStr = b;
        break;
      }
    }
  }

  const isHighGradeBilsky = bilskyStr === '2' || bilskyStr === '3';

  // 2. Oncologic: Histological Radiosensitivity (Radiosensitive vs Radioresistant)
  let isRadiosensitive = false;
  const oncoVal = inputs.oncologic ?? inputs.radiosensitivity ?? inputs.histology ?? inputs.grp_noms_oncologic;
  if (typeof oncoVal === 'string') {
    const lower = oncoVal.toLowerCase();
    if (
      lower.includes('sens') ||
      lower.includes('mieloma') ||
      lower.includes('myeloma') ||
      lower.includes('linfoma') ||
      lower.includes('lymphoma') ||
      lower.includes('pequenas') ||
      lower.includes('small') ||
      lower.includes('seminoma')
    ) {
      isRadiosensitive = true;
    }
  } else if (typeof oncoVal === 'boolean') {
    isRadiosensitive = oncoVal;
  } else {
    if (inputs.opt_radiosensitive || inputs.radiosensitive === true) {
      isRadiosensitive = true;
    }
  }

  // 3. Mechanical: SINS (0-6 Stable, 7-12 Potentially Unstable, 13-18 Unstable)
  let mechanicalCategory: 'stable' | 'potentially_unstable' | 'unstable' = 'stable';
  const mechVal = inputs.mechanical ?? inputs.sins ?? inputs.sins_score ?? inputs.grp_noms_mechanical;
  if (typeof mechVal === 'number') {
    if (mechVal >= 13) mechanicalCategory = 'unstable';
    else if (mechVal >= 7) mechanicalCategory = 'potentially_unstable';
    else mechanicalCategory = 'stable';
  } else if (typeof mechVal === 'string') {
    const lower = mechVal.toLowerCase();
    if (lower.includes('unstable') || lower.includes('instab')) mechanicalCategory = 'unstable';
    else if (lower.includes('poten')) mechanicalCategory = 'potentially_unstable';
    else mechanicalCategory = 'stable';
  } else {
    if (inputs.opt_sins_unstable || inputs.unstable === true) mechanicalCategory = 'unstable';
    else if (inputs.opt_sins_potentially_unstable) mechanicalCategory = 'potentially_unstable';
  }

  // 4. Systemic: KPS (>= 70% vs < 70% or terminal)
  let isSystemicEligible = true;
  const sysVal = inputs.systemic ?? inputs.kps ?? inputs.kps_score ?? inputs.grp_noms_systemic ?? inputs.eligibility;
  if (typeof sysVal === 'number') {
    isSystemicEligible = sysVal >= 70;
  } else if (typeof sysVal === 'boolean') {
    isSystemicEligible = sysVal;
  } else if (typeof sysVal === 'string') {
    const lower = sysVal.toLowerCase();
    if (lower.includes('ineligible') || lower.includes('terminal') || lower.includes('hospice') || lower.includes('desfavoravel')) {
      isSystemicEligible = false;
    }
  } else {
    if (inputs.opt_kps_lt70 || inputs.ineligible === true || inputs.terminal === true) {
      isSystemicEligible = false;
    }
  }

  // Multidimensional Decision Matrix Adjudication
  let pathwayName: 'Separation Surgery + SBRT' | 'cEBRT alone' | 'Percutaneous Stabilization' | 'Palliative Hospice' | 'Primary SBRT';
  let pathwayTitle: string;
  let severityLevel: 'low' | 'intermediate' | 'high' | 'critical';
  let tierId: string;
  let tierColor: string;
  let recommendation: string;
  let statisticalOutcome: string;
  let rawScore: number;

  if (!isSystemicEligible) {
    pathwayName = 'Palliative Hospice';
    pathwayTitle = 'Cuidados Paliativos / Radioterapia de Curso Curto (Palliative Hospice)';
    severityLevel = 'low';
    tierId = 'tier_noms_palliative';
    tierColor = '#6b7280';
    rawScore = 1;
    recommendation =
      'Paciente com status de performance fragilizado (KPS < 70% ou doença terminal). Cirurgia descompressiva e reconstrução instrumentada aberta estão formalmente contraindicadas pela elevada taxa de mortalidade perioperatória e sobrevida restrita (< 2-3 meses). Indicação de Radioterapia Paliativa em Fração Única (8 Gy) ou hipofracionada (20 Gy em 5 frações) para alívio álgico, associada a Dexametasona oral/SC e plano de hospice humanizado.';
    statisticalOutcome =
      'Sobrevida estimada inferior a 3 meses. Prioridade absoluta para conforto, alívio de dor e prevenção de sofrimento, evitando futilidade cirúrgica.';
  } else if (isHighGradeBilsky && !isRadiosensitive) {
    pathwayName = 'Separation Surgery + SBRT';
    pathwayTitle = 'Cirurgia de Separação + SBRT Pós-Operatória (Separation Surgery + SBRT)';
    severityLevel = 'critical';
    tierId = 'tier_noms_separation_sbrt';
    tierColor = '#dc2626';
    rawScore = 4;
    recommendation =
      'Indicação Cirúrgica Mandatória de Cirurgia de Separação ("Separation Surgery") com laminectomia e descompressão circunferencial de 2 a 3 mm ao redor do saco dural e medula espinhal, associada à Artrodese Posterior Instrumentada com Parafusos Pediculares. Após cicatrização da ferida operatória (2 a 4 semanas), realizar SBRT hipofracionada (18 a 24 Gy em 1 a 3 frações). A radioterapia convencional exclusiva é contraindicada por taxa de falha tumoral > 80% em tumores radiorresistentes.';
    statisticalOutcome =
      'A Cirurgia de Separação seguida de SBRT atinge taxa de controle local superior a 85-90% em 1 ano com preservação e recuperação neurológica sustentada.';
  } else if (isHighGradeBilsky && isRadiosensitive) {
    if (mechanicalCategory === 'unstable') {
      pathwayName = 'cEBRT alone';
      pathwayTitle = 'Radioterapia Convencional de Urgência + Estabilização Cirúrgica (cEBRT + Stabilization)';
      severityLevel = 'high';
      tierId = 'tier_noms_cebrt_stabilization';
      tierColor = '#ef4444';
      rawScore = 3;
      recommendation =
        'Indicação de Radioterapia Externa Convencional de Urgência (cEBRT: 30 Gy em 10 frações) associada a Dexametasona em altas doses (10 a 16 mg IV bolus seguido de 4 mg 6/6h) para descompressão tumoral rápida. Pela instabilidade mecânica presente (SINS >= 13), é mandatória a Estabilização Cirúrgica Instrumentada (aberta ou percutânea) concomitante para prevenção de colapso estrutural catastrófico.';
      statisticalOutcome =
        'Excelente descompressão celular pela alta radiossensibilidade tumoral, porém a irradiação não repara o suporte mecânico destruído.';
    } else {
      pathwayName = 'cEBRT alone';
      pathwayTitle = 'Radioterapia Externa Convencional Exclusiva (cEBRT alone)';
      severityLevel = 'intermediate';
      tierId = 'tier_noms_cebrt_alone';
      tierColor = '#f59e0b';
      rawScore = 2;
      recommendation =
        'Tumor de alta radiossensibilidade celular (Mieloma Múltiplo, Linfoma, Seminoma) com coluna estável. Indicação de Radioterapia Externa Convencional de Urgência (cEBRT: 30 Gy em 10 frações) combinada com corticoterapia em altas doses. Descompressão cirúrgica aberta dispensada em virtude da rápida resposta tumoral.';
      statisticalOutcome =
        'Taxa de resposta de descompressão medular superior a 80-90% sem a morbidade de cirurgia aberta de grande porte.';
    }
  } else if (mechanicalCategory === 'unstable' || mechanicalCategory === 'potentially_unstable') {
    pathwayName = 'Percutaneous Stabilization';
    pathwayTitle = 'Estabilização Percutânea / Cifoplastia ± SBRT (Percutaneous Stabilization)';
    severityLevel = mechanicalCategory === 'unstable' ? 'high' : 'intermediate';
    tierId = 'tier_noms_percutaneous';
    tierColor = '#f97316';
    rawScore = 3;
    recommendation =
      'Presença de instabilidade mecânica tumoral (SINS 7-12 com dor mecânica ou SINS >= 13) sem compressão medular crítica (Bilsky baixo grau 0 a 1c). Indicação de Estabilização Percutânea com Parafusos Pediculares ou Cifoplastia com Balão / Vertebroplastia associada à irradiação conformacional (SBRT para tumores radiorresistentes ou cEBRT para radiossensíveis).';
    statisticalOutcome =
      'Alívio álgico imediato (> 85% de resposta para dor ao suporte de carga) e prevenção de colapso vertebral induzido por radiação.';
  } else {
    // Low grade Bilsky, stable mechanical
    if (!isRadiosensitive) {
      pathwayName = 'Primary SBRT';
      pathwayTitle = 'SBRT Primária Isolada (Primary SBRT)';
      severityLevel = 'intermediate';
      tierId = 'tier_noms_primary_sbrt';
      tierColor = '#3b82f6';
      rawScore = 2;
      recommendation =
        'Ausência de compressão medular de alto grau e coluna mecanicamente estável em tumor radiorresistente. Indicação de SBRT Primária Isolada (24 a 30 Gy em 3 a 5 frações) com excelente controle local (> 90%) sem necessidade de abordagem cirúrgica.';
      statisticalOutcome =
        'Controle local de 90-95% em 1 a 2 anos com mínima toxicidade tecidual.';
    } else {
      pathwayName = 'cEBRT alone';
      pathwayTitle = 'Radioterapia Convencional Eletiva (cEBRT alone)';
      severityLevel = 'low';
      tierId = 'tier_noms_cebrt_elective';
      tierColor = '#10b981';
      rawScore = 2;
      recommendation =
        'Tumor radiossensível estável sem compressão medular. Indicação de Radioterapia Convencional Eletiva (20 a 30 Gy) e continuidade do tratamento sistêmico quimioterápico / imunoterápico.';
      statisticalOutcome =
        'Excelente prognóstico funcional com controle oncológico pleno.';
    }
  }

  // Active risk tier
  let activeRiskTier: RiskTier;
  if (calc?.riskTiers && calc.riskTiers.length > 0) {
    const matched = calc.riskTiers.find((t) => t.severityLevel === severityLevel) ?? calc.riskTiers[0];
    activeRiskTier = {
      ...matched,
      label: `${matched.label}: ${pathwayTitle}`,
      statisticalOutcome: `${matched.statisticalOutcome} ${statisticalOutcome}`,
      nonPharmacologicalActions: [
        {
          id: 'action_noms_pathway',
          recommendationTitle: pathwayTitle,
          dispositionTarget: severityLevel === 'critical' || severityLevel === 'high' ? 'Centro Cirúrgico / UTI Neuro-Oncológica' : 'Radioterapia / Ambulatório de Oncologia',
          monitoringPlan: 'RM de neuroeixo seriada e vigilância motora rigorosa.',
          interventionalProcedure: recommendation
        },
        ...matched.nonPharmacologicalActions
      ]
    };
  } else {
    activeRiskTier = {
      id: tierId,
      label: pathwayTitle,
      severityLevel,
      minScore: 1,
      maxScore: 4,
      statisticalOutcome,
      colorHex: tierColor,
      pharmacologicalActions: [
        {
          id: 'rx_noms_dexamethasone',
          drugName: 'Dexametasona (Controle de Edema Medular)',
          dosage: isHighGradeBilsky ? '10 a 16 mg IV em bolus, seguido de 4 mg IV/VO a cada 6 horas' : '4 mg VO 12/12h com desmame em 7-14 dias',
          route: 'Intravenosa / Oral',
          frequency: '4/4h a 12/12h conforme gravidade'
        }
      ],
      nonPharmacologicalActions: [
        {
          id: 'action_noms_pathway',
          recommendationTitle: pathwayTitle,
          dispositionTarget: severityLevel === 'critical' ? 'Centro Cirúrgico / UTI Neurocrítica' : 'Radioterapia / Oncologia',
          monitoringPlan: 'Avaliação motora seriada dos dermátomos e miótomos.',
          interventionalProcedure: recommendation
        }
      ]
    };
  }

  const radarValues: Record<string, number> = {};
  if (calc?.radarAxes) {
    for (const axis of calc.radarAxes) {
      radarValues[axis.id] = 0;
    }
  }
  radarValues['axis_noms_neuro'] = bilskyStr === '3' ? 1.0 : bilskyStr === '2' ? 0.8 : bilskyStr === '1c' ? 0.6 : bilskyStr === '1b' ? 0.4 : bilskyStr === '1a' ? 0.2 : 0;
  radarValues['axis_noms_onco'] = isRadiosensitive ? 0.2 : 0.9;
  radarValues['axis_noms_mech'] = mechanicalCategory === 'unstable' ? 1.0 : mechanicalCategory === 'potentially_unstable' ? 0.6 : 0.1;
  radarValues['axis_noms_sys'] = isSystemicEligible ? 0.1 : 0.9;
  radarValues['axis_noms_syst'] = isSystemicEligible ? 0.1 : 0.9;

  const scoreFormatted = `${pathwayName} (Bilsky ${bilskyStr} / ${isRadiosensitive ? 'Sensível' : 'Resistente'} / SINS ${mechanicalCategory})`;

  return {
    score: rawScore,
    rawScore,
    scoreFormatted,
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning: calc?.clinicalWarning,
    warnings: calc?.clinicalWarning ? [calc.clinicalWarning] : undefined
  };
}

// ----------------------------------------------------------------------------
// J. Lawton-Young Supplementary AVM Grading System
// ----------------------------------------------------------------------------

export function calculateLawtonYoung(inputs: Record<string, any>): CalculationResult;
export function calculateLawtonYoung(calc: ClinicalTool, inputs: Record<string, any>): CalculationResult;
export function calculateLawtonYoung(
  calcOrInputs: ClinicalTool | Record<string, any>,
  maybeInputs?: Record<string, any>
): CalculationResult {
  let calc: ClinicalTool | undefined;
  let inputs: Record<string, any>;

  if (maybeInputs !== undefined) {
    calc = calcOrInputs as ClinicalTool;
    inputs = maybeInputs;
  } else if (
    calcOrInputs &&
    typeof calcOrInputs === 'object' &&
    'parameterGroups' in calcOrInputs
  ) {
    calc = calcOrInputs as ClinicalTool;
    inputs = {};
  } else {
    calc = undefined;
    inputs = (calcOrInputs as Record<string, any>) || {};
  }

  // 1. Spetzler-Martin Base Score (1 to 5)
  let smScore = 1;
  const directSm = inputs.spetzlerMartin ?? inputs.smScore ?? inputs.spetzler_martin ?? inputs.sm ?? inputs.grp_ly_sm;
  if (typeof directSm === 'number' && directSm >= 1 && directSm <= 5) {
    smScore = Math.round(directSm);
  } else if (typeof directSm === 'string') {
    const match = directSm.match(/[1-5]/);
    if (match) smScore = parseInt(match[0], 10);
  } else {
    let sizePts = 1;
    const sizeVal = inputs.sm_size ?? inputs.size ?? inputs.grp_sm_size;
    if (typeof sizeVal === 'number') {
      if (sizeVal > 6) sizePts = 3;
      else if (sizeVal >= 3) sizePts = 2;
      else sizePts = 1;
    } else if (typeof sizeVal === 'string') {
      if (sizeVal.includes('>6') || sizeVal.includes('large') || sizeVal.includes('grande')) sizePts = 3;
      else if (sizeVal.includes('3-6') || sizeVal.includes('medium') || sizeVal.includes('medio')) sizePts = 2;
      else sizePts = 1;
    } else {
      if (inputs.opt_sm_size_large) sizePts = 3;
      else if (inputs.opt_sm_size_medium) sizePts = 2;
      else if (inputs.opt_sm_size_small) sizePts = 1;
    }

    let eloqPts = 0;
    const eloqVal = inputs.sm_eloquence ?? inputs.eloquence ?? inputs.grp_sm_eloquence;
    if (typeof eloqVal === 'boolean') {
      eloqPts = eloqVal ? 1 : 0;
    } else if (typeof eloqVal === 'number') {
      eloqPts = eloqVal > 0 ? 1 : 0;
    } else if (typeof eloqVal === 'string') {
      eloqPts = eloqVal.toLowerCase().includes('eloq') && !eloqVal.toLowerCase().includes('nao') ? 1 : 0;
    } else {
      if (inputs.opt_sm_eloq_yes) eloqPts = 1;
    }

    let drainPts = 0;
    const drainVal = inputs.sm_drainage ?? inputs.drainage ?? inputs.deep_drainage ?? inputs.grp_sm_drainage;
    if (typeof drainVal === 'boolean') {
      drainPts = drainVal ? 1 : 0;
    } else if (typeof drainVal === 'number') {
      drainPts = drainVal > 0 ? 1 : 0;
    } else if (typeof drainVal === 'string') {
      drainPts = drainVal.toLowerCase().includes('profund') || drainVal.toLowerCase().includes('deep') ? 1 : 0;
    } else {
      if (inputs.opt_sm_drain_deep) drainPts = 1;
    }

    smScore = Math.max(1, Math.min(5, sizePts + eloqPts + drainPts));
  }

  // 2. Supplementary Lawton-Young Score (1 to 5)
  // Age: < 20 (1 pt), 20-40 (2 pts), > 40 (3 pts)
  let agePts = 2;
  const ageVal = inputs.age ?? inputs.lawton_age ?? inputs.grp_lawton_age ?? inputs.grp_ly_age;
  if (typeof ageVal === 'number') {
    if (ageVal > 40) agePts = 3;
    else if (ageVal >= 20) agePts = 2;
    else agePts = 1;
  } else if (typeof ageVal === 'string') {
    if (ageVal.includes('>40') || ageVal.includes('gt40')) agePts = 3;
    else if (ageVal.includes('20-40') || ageVal.includes('20_40')) agePts = 2;
    else if (ageVal.includes('<20') || ageVal.includes('lt20')) agePts = 1;
  } else {
    if (inputs.opt_lawton_age_gt40 || inputs.opt_ly_age_gt40) agePts = 3;
    else if (inputs.opt_lawton_age_20_40 || inputs.opt_ly_age_20_40) agePts = 2;
    else if (inputs.opt_lawton_age_lt20 || inputs.opt_ly_age_lt20) agePts = 1;
  }

  // Bleeding status: Ruptured / previous bleed (0 pts), Unruptured (1 pt)
  let bleedPts = 0;
  const bleedVal = inputs.unruptured ?? inputs.ruptured ?? inputs.bleed ?? inputs.bleeding ?? inputs.lawton_bleed ?? inputs.grp_lawton_bleed ?? inputs.grp_ly_bleed ?? inputs.grp_ly_rupture;
  if (typeof bleedVal === 'boolean') {
    if (inputs.unruptured !== undefined) {
      bleedPts = inputs.unruptured ? 1 : 0;
    } else {
      bleedPts = bleedVal ? 0 : 1;
    }
  } else if (typeof bleedVal === 'string') {
    const lower = bleedVal.toLowerCase();
    if (lower.includes('unruptured') || lower.includes('nao_roto') || lower.includes('sem_sangramento') || lower.includes('bleed_no') || lower.includes('rup_no')) {
      bleedPts = 1;
    } else {
      bleedPts = 0;
    }
  } else {
    if (inputs.opt_lawton_bleed_no || inputs.opt_lawton_unruptured || inputs.opt_ly_bleed_no) bleedPts = 1;
    else if (inputs.opt_lawton_bleed_yes || inputs.opt_lawton_ruptured || inputs.opt_ly_bleed_yes) bleedPts = 0;
  }

  // Nidus compactness: Compact (0 pts), Diffuse (1 pt)
  let compactPts = 0;
  const compactVal = inputs.compactness ?? inputs.nidus ?? inputs.diffuse ?? inputs.lawton_compactness ?? inputs.grp_lawton_compactness ?? inputs.grp_ly_compact ?? inputs.grp_ly_compactness;
  if (typeof compactVal === 'boolean') {
    compactPts = compactVal ? 1 : 0;
  } else if (typeof compactVal === 'string') {
    const lower = compactVal.toLowerCase();
    if (lower.includes('diffuse') || lower.includes('difuso') || lower.includes('compact_no') || lower.includes('comp_diffuse')) compactPts = 1;
    else compactPts = 0;
  } else {
    if (inputs.opt_lawton_diffuse || inputs.opt_ly_compact_no) compactPts = 1;
    else if (inputs.opt_lawton_compact || inputs.opt_ly_compact_yes) compactPts = 0;
  }

  const lyScore = agePts + bleedPts + compactPts; // 1 to 5
  const rawScore = smScore + lyScore; // 2 to 10

  // Risk Tiers:
  // 2 to 4: Low surgical risk
  // 5 to 6: Intermediate / multimodal
  // 7 to 10: Prohibitive / ARUBA conservative
  let severityLevel: 'low' | 'intermediate' | 'high' | 'critical';
  let tierId: string;
  let tierLabel: string;
  let tierColor: string;
  let statisticalOutcome: string;
  let recommendation: string;

  if (rawScore <= 4) {
    severityLevel = 'low';
    tierId = 'tier_lawton_low';
    tierLabel = 'Baixa Complexidade Cirúrgica / Baixo Risco (2 a 4 pontos)';
    tierColor = '#10b981';
    statisticalOutcome =
      'Taxa de déficit neurológico permanente pós-operatório < 3% a 5%. Taxa de cura e obliteração microcirúrgica completa imediata > 95% a 98%.';
    recommendation =
      'Indicação Cirúrgica Mandatória / Eletiva de Ressecção Microcirúrgica Primária Completa. A cirurgia precoce elimina o risco vital de sangramento futuro com excelente segurança anatômica.';
  } else if (rawScore <= 6) {
    severityLevel = 'intermediate';
    tierId = 'tier_lawton_intermediate';
    tierLabel = 'Complexidade Cirúrgica Intermediária / Caso Limítrofe (5 a 6 pontos)';
    tierColor = '#f59e0b';
    statisticalOutcome =
      'Taxa de novos déficits permanentes pós-operatórios de 10% a 25%. Risco moderado de complicações isquêmicas ou hemorrágicas.';
    recommendation =
      'Caso Limítrofe / Manejo Multimodal Individualizado: Embolização superseletiva pré-operatória estagiada com agentes líquidos não absorvíveis (Onyx ou Squid) para oclusão de pedículos profundos seguida de microcirurgia OU Radiocirurgia Estereotática (SRS: 18 a 22 Gy) se nidus < 3 cm.';
  } else {
    severityLevel = 'critical';
    tierId = 'tier_lawton_high';
    tierLabel = 'Alta Complexidade / Risco Cirúrgico Proibitivo (7 a 10 pontos)';
    tierColor = '#dc2626';
    statisticalOutcome =
      'Risco de morbidade cirúrgica permanente incapacitante superior a 35% a 50% (> 35% a 50%). A morbimortalidade procedimental excede expressivamente o risco da história natural da malformação.';
    recommendation =
      'Tratamento Conservador Seguro / Manejo Clínico Expectante (Diretrizes do Ensaio Clínico ARUBA). Microcirurgia aberta formalmente contraindicada pela alta taxa de déficits permanentes, exceto para evacuação emergencial de hematoma com risco de morte.';
  }

  // Active risk tier
  let activeRiskTier: RiskTier;
  if (calc?.riskTiers && calc.riskTiers.length > 0) {
    const matched = calc.riskTiers.find((t) => t.severityLevel === severityLevel) ??
      calc.riskTiers.find((t) => rawScore >= t.minScore && rawScore <= t.maxScore) ??
      calc.riskTiers[0];
    activeRiskTier = {
      ...matched,
      statisticalOutcome: `${matched.statisticalOutcome} ${statisticalOutcome}`,
      nonPharmacologicalActions: [
        {
          id: 'action_lawton_plan',
          recommendationTitle: tierLabel,
          dispositionTarget: severityLevel === 'critical' ? 'Ambulatório de Neurovascular / Tratamento Conservador' : 'Centro Cirúrgico Neurovascular / UTI',
          monitoringPlan: 'Angiografia digital de controle pós-operatória precoce (< 24h) e controle rigoroso de PA.',
          interventionalProcedure: recommendation
        },
        ...matched.nonPharmacologicalActions
      ]
    };
  } else {
    activeRiskTier = {
      id: tierId,
      label: tierLabel,
      severityLevel,
      minScore: rawScore <= 4 ? 2 : rawScore <= 6 ? 5 : 7,
      maxScore: rawScore <= 4 ? 4 : rawScore <= 6 ? 6 : 10,
      statisticalOutcome,
      colorHex: tierColor,
      pharmacologicalActions: [
        {
          id: 'rx_lawton_nppb',
          drugName: 'Nitroprussiato de Sódio / Esmolol em BIC (Protocolo Anti-Hiperemia NPPB)',
          dosage: 'Titular para manter PAS estritamente < 120 mmHg no pós-operatório imediato',
          route: 'Intravenosa em BIC contínua',
          frequency: 'Contínua em UTI Neurocrítica',
          contraindications: 'Proibida hipertensão induzida pós-ressecção pelo risco catastrófico de sangramento por perda de autorregulação (NPPB).'
        }
      ],
      nonPharmacologicalActions: [
        {
          id: 'action_lawton_plan',
          recommendationTitle: tierLabel,
          dispositionTarget: severityLevel === 'critical' ? 'Ambulatório Neurovascular (Conduta ARUBA)' : 'Centro Cirúrgico Neurovascular',
          monitoringPlan: 'Angiografia cerebral digital de 6 vasos e controle em UTI.',
          interventionalProcedure: recommendation
        }
      ]
    };
  }

  const radarValues: Record<string, number> = {};
  if (calc?.radarAxes) {
    for (const axis of calc.radarAxes) {
      radarValues[axis.id] = 0;
    }
  }
  radarValues['axis_mav_size'] = Math.min(1, Math.max(0, (smScore - 1) / 4));
  radarValues['axis_mav_eloquence'] = smScore >= 3 ? 0.7 : 0.2;
  radarValues['axis_mav_surgical_risk'] = Math.min(1, Math.max(0, (rawScore - 2) / 8));

  radarValues['axis_ly_sm'] = Math.min(1, Math.max(0, (smScore - 1) / 4));
  radarValues['axis_ly_age'] = Math.min(1, Math.max(0, (agePts - 1) / 2));
  radarValues['axis_ly_rupture'] = bleedPts;
  radarValues['axis_ly_compact'] = compactPts;

  const scoreFormatted = `${rawScore} pontos (SM ${smScore} + LY ${lyScore})`;

  return {
    score: rawScore,
    rawScore,
    scoreFormatted,
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning: calc?.clinicalWarning,
    warnings: calc?.clinicalWarning ? [calc.clinicalWarning] : undefined
  };
}

// ----------------------------------------------------------------------------
// K. PHASES Rupture Risk Score for Unruptured Intracranial Aneurysms
// ----------------------------------------------------------------------------

const PHASES_5_YEAR_RISK_MAP: Record<number, number> = {
  0: 0.4,
  1: 0.4,
  2: 0.7,
  3: 0.7,
  4: 0.9,
  5: 1.3,
  6: 1.7,
  7: 2.4,
  8: 3.2,
  9: 4.3,
  10: 5.3,
  11: 7.2,
  12: 9.8,
  13: 13.0,
  14: 15.3
};

export function calculatePhasesScore(inputs: Record<string, any>): CalculationResult;
export function calculatePhasesScore(calc: ClinicalTool, inputs: Record<string, any>): CalculationResult;
export function calculatePhasesScore(
  calcOrInputs: ClinicalTool | Record<string, any>,
  maybeInputs?: Record<string, any>
): CalculationResult {
  let calc: ClinicalTool | undefined;
  let inputs: Record<string, any>;

  if (maybeInputs !== undefined) {
    calc = calcOrInputs as ClinicalTool;
    inputs = maybeInputs;
  } else if (
    calcOrInputs &&
    typeof calcOrInputs === 'object' &&
    'parameterGroups' in calcOrInputs
  ) {
    calc = calcOrInputs as ClinicalTool;
    inputs = {};
  } else {
    calc = undefined;
    inputs = (calcOrInputs as Record<string, any>) || {};
  }

  // 1. Population (P): Other (0), Japan (3), Finland (5)
  let p = 0;
  const popVal = inputs.population ?? inputs.grp_phases_pop ?? inputs.pop;
  if (typeof popVal === 'string') {
    const lower = popVal.toLowerCase();
    if (lower.includes('finland') || lower.includes('finlandia')) p = 5;
    else if (lower.includes('japan') || lower.includes('japao')) p = 3;
    else p = 0;
  } else {
    if (inputs.opt_phases_pop_finland) p = 5;
    else if (inputs.opt_phases_pop_japan) p = 3;
  }

  // 2. Hypertension (H): No (0), Yes (1)
  let h = 0;
  const htnVal = inputs.hypertension ?? inputs.htn ?? inputs.grp_phases_htn;
  if (typeof htnVal === 'boolean') {
    h = htnVal ? 1 : 0;
  } else if (typeof htnVal === 'string') {
    const lower = htnVal.toLowerCase();
    h = lower.includes('yes') || lower.includes('sim') || lower.includes('present') || lower.includes('htn_yes') ? 1 : 0;
  } else {
    if (inputs.opt_phases_htn_yes) h = 1;
  }

  // 3. Age >= 70 (A): < 70 (0), >= 70 (1)
  let a = 0;
  const ageVal = inputs.age ?? inputs.ageGte70 ?? inputs.grp_phases_age;
  if (typeof ageVal === 'number') {
    a = ageVal >= 70 ? 1 : 0;
  } else if (typeof ageVal === 'boolean') {
    a = ageVal ? 1 : 0;
  } else if (typeof ageVal === 'string') {
    a = ageVal.includes('70') && (ageVal.includes('>=') || ageVal.includes('gte') || ageVal.includes('>')) ? 1 : 0;
  } else {
    if (inputs.opt_phases_age_gte70) a = 1;
  }

  // 4. Size (S): < 7.0mm (0), 7.0-9.9mm (3), 10.0-19.9mm (6), >= 20.0mm (10)
  let s = 0;
  const sizeVal = inputs.size ?? inputs.aneurysmSize ?? inputs.grp_phases_size;
  if (typeof sizeVal === 'number') {
    if (sizeVal >= 20.0) s = 10;
    else if (sizeVal >= 10.0) s = 6;
    else if (sizeVal >= 7.0) s = 3;
    else s = 0;
  } else if (typeof sizeVal === 'string') {
    const lower = sizeVal.toLowerCase();
    if (lower.includes('20') || lower.includes('giant') || lower.includes('gigante')) s = 10;
    else if (lower.includes('10') || lower.includes('10-19') || lower.includes('10_19')) s = 6;
    else if (lower.includes('7') || lower.includes('7-9') || lower.includes('7_9')) s = 3;
    else s = 0;
  } else {
    if (inputs.opt_phases_size_gte20) s = 10;
    else if (inputs.opt_phases_size_10_19) s = 6;
    else if (inputs.opt_phases_size_7_9) s = 3;
  }

  // 5. Earlier SAH (E): No (0), Yes (1)
  let e = 0;
  const sahVal = inputs.earlierSah ?? inputs.earlier_sah ?? inputs.previousSah ?? inputs.grp_phases_earlier_sah;
  if (typeof sahVal === 'boolean') {
    e = sahVal ? 1 : 0;
  } else if (typeof sahVal === 'string') {
    const lower = sahVal.toLowerCase();
    e = (lower.includes('yes') || lower.includes('sim') || lower.includes('present') || lower.includes('sah_yes')) && !lower.includes('no') && !lower.includes('nao') ? 1 : 0;
  } else {
    if (inputs.opt_phases_earlier_sah_yes) e = 1;
  }

  // 6. Site (S): ICA (0), MCA (2), ACoA/PCoA/Posterior (4)
  let sitePts = 0;
  const siteVal = inputs.site ?? inputs.location ?? inputs.grp_phases_site;
  if (typeof siteVal === 'string') {
    const lower = siteVal.toLowerCase();
    if (
      lower.includes('post') ||
      lower.includes('basilar') ||
      lower.includes('vertebral') ||
      lower.includes('pica') ||
      lower.includes('pca') ||
      lower.includes('acoa') ||
      lower.includes('pcoa') ||
      lower.includes('comunicante')
    ) {
      sitePts = 4;
    } else if (lower.includes('mca') || lower.includes('acm') || lower.includes('media')) {
      sitePts = 2;
    } else {
      sitePts = 0; // ICA
    }
  } else {
    if (inputs.opt_phases_site_acoa_pcoa_post) sitePts = 4;
    else if (inputs.opt_phases_site_mca) sitePts = 2;
    else if (inputs.opt_phases_site_ica) sitePts = 0;
  }

  const rawScore = p + h + a + s + e + sitePts; // 0 to 22

  // 5-year aneurysm rupture probability
  let riskFormatted: string;
  let riskPercent: number;
  if (rawScore >= 15) {
    riskPercent = 17.8;
    riskFormatted = '> 17.8%';
  } else if (PHASES_5_YEAR_RISK_MAP[rawScore] !== undefined) {
    riskPercent = PHASES_5_YEAR_RISK_MAP[rawScore];
    riskFormatted = `${riskPercent.toFixed(1)}%`;
  } else {
    riskPercent = 0.4;
    riskFormatted = '0.4%';
  }

  // Risk Cutoffs:
  // <= 3: Conservative Safe (0.4% - 0.7%)
  // 4 - 7: Borderline / Shared decision (0.9% - 4.3%)
  // >= 8: Mandatory Surgical / Interventional (>= 5.3% to > 17.8%)
  let severityLevel: 'low' | 'intermediate' | 'high' | 'critical';
  let tierId: string;
  let tierLabel: string;
  let tierColor: string;
  let statisticalOutcome: string;
  let recommendation: string;

  if (rawScore <= 3) {
    severityLevel = 'low';
    tierId = 'tier_phases_low';
    tierLabel = 'Baixo Risco de Ruptura (0 a 3 pontos) - Tratamento Conservador Seguro';
    tierColor = '#10b981';
    statisticalOutcome = `Probabilidade estimada de ruptura em 5 anos de ${riskFormatted} (risco anualizado < 0,1% a 0,15%/ano). O risco cumulativo de morbimortalidade de qualquer procedimento invasivo supera o risco da história natural do aneurisma.`;
    recommendation =
      'Tratamento Conservador Seguro de Escolha. Cessação mandatória do tabagismo, controle pressórico rigoroso com anti-hipertensivos (meta PAS < 130 mmHg) e vigilância por neuroimagem vascular não invasiva (Angio-TC ou Angio-RM sem contraste) aos 12 meses; se estabilidade dimensional, a cada 2 a 3 anos.';
  } else if (rawScore <= 7) {
    severityLevel = 'intermediate';
    tierId = 'tier_phases_intermediate';
    tierLabel = 'Risco Intermediário (4 a 7 pontos) - Caso Limítrofe / Decisão Compartilhada';
    tierColor = '#f59e0b';
    statisticalOutcome = `Probabilidade estimada de ruptura em 5 anos de ${riskFormatted}.`;
    recommendation =
      'Caso Limítrofe / Tomada de Decisão Compartilhada. Avaliar aspectos morfológicos angiorradiológicos de alto risco: presença de irregularidades de parede (daughter sacs, multilobulação), Aspect Ratio (profundidade/colo > 1,6), idade biológica, história familiar de HSA e expectativa de vida. Considerar intervenção preventiva em pacientes jovens com colo favorável.';
  } else {
    severityLevel = 'critical';
    tierId = 'tier_phases_high';
    tierLabel = 'Alto a Muito Alto Risco de Ruptura (8 a 22 pontos) - Indicação Cirúrgica Mandatória';
    tierColor = '#dc2626';
    statisticalOutcome = `Probabilidade estimada de ruptura em 5 anos de ${riskFormatted} (elevadíssimo risco cumulativo com taxa de mortalidade ou dependência grave superior a 60-70% caso ocorra rotura).`;
    recommendation =
      'Indicação Cirúrgica Mandatória / Tratamento Intervencionista Eletivo Ativo. Avaliação anatômica para Clipagem Microcirúrgica Aberta (de escolha para aneurismas de bifurcação da ACM e colos largos com ramos emergentes) versus Oclusão Endovascular com micromolas destacáveis ou Stent Diversor de Fluxo (Flow Diverter) com dupla antiagregação prévia.';
  }

  // Active risk tier
  let activeRiskTier: RiskTier;
  if (calc?.riskTiers && calc.riskTiers.length > 0) {
    const matched = calc.riskTiers.find((t) => t.severityLevel === severityLevel) ??
      calc.riskTiers.find((t) => rawScore >= t.minScore && rawScore <= t.maxScore) ??
      calc.riskTiers[0];
    activeRiskTier = {
      ...matched,
      statisticalOutcome: `${matched.statisticalOutcome} ${statisticalOutcome}`,
      nonPharmacologicalActions: [
        {
          id: 'action_phases_treatment',
          recommendationTitle: tierLabel,
          dispositionTarget: severityLevel === 'critical' ? 'Centro Cirúrgico / Hemodinâmica Neurointervencionista' : 'Ambulatório de Neurocirurgia Vascular',
          monitoringPlan: 'Angio-TC / Angio-RM vascular cerebral seriada.',
          interventionalProcedure: recommendation
        },
        ...matched.nonPharmacologicalActions
      ]
    };
  } else {
    activeRiskTier = {
      id: tierId,
      label: tierLabel,
      severityLevel,
      minScore: rawScore <= 3 ? 0 : rawScore <= 7 ? 4 : 8,
      maxScore: rawScore <= 3 ? 3 : rawScore <= 7 ? 7 : 22,
      statisticalOutcome,
      colorHex: tierColor,
      pharmacologicalActions: [
        {
          id: 'rx_phases_bp_control',
          drugName: 'Enalapril / Losartana (Controle Pressórico Estrito)',
          dosage: 'Titular para PAS < 130 mmHg e PAD < 80 mmHg',
          route: 'Oral',
          frequency: 'Uso contínuo diário'
        }
      ],
      nonPharmacologicalActions: [
        {
          id: 'action_phases_treatment',
          recommendationTitle: tierLabel,
          dispositionTarget: severityLevel === 'critical' ? 'Centro Cirúrgico / Hemodinâmica Intervencionista' : 'Ambulatório de Neurocirurgia Vascular',
          monitoringPlan: 'Neuroimagem vascular sem contraste periódica.',
          interventionalProcedure: recommendation
        }
      ]
    };
  }

  const radarValues: Record<string, number> = {};
  if (calc?.radarAxes) {
    for (const axis of calc.radarAxes) {
      radarValues[axis.id] = 0;
    }
  }
  radarValues['axis_aneurysm_size'] = Math.min(1, Math.max(0, s / 10));
  radarValues['axis_aneurysm_site'] = sitePts / 4;
  radarValues['axis_rupture_risk'] = Math.min(1, Math.max(0, riskPercent / 20));

  radarValues['axis_ph_morphology'] = Math.min(1, Math.max(0, s / 10));
  radarValues['axis_ph_site'] = sitePts / 4;
  radarValues['axis_ph_demographic'] = Math.min(1, (p + a) / 5);
  radarValues['axis_ph_clinical'] = Math.min(1, (h + e) / 2);

  const scoreFormatted = `${rawScore} pontos (Risco 5 anos: ${riskFormatted})`;

  return {
    score: rawScore,
    rawScore,
    scoreFormatted,
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning: calc?.clinicalWarning,
    warnings: calc?.clinicalWarning ? [calc.clinicalWarning] : undefined
  };
}

// ============================================================================
// 6. VASOGRADE BIVARIATE RESOLVER (WFNS x MODIFIED FISHER)
// ============================================================================

export interface VasogradeInputs {
  wfns?: number | string;
  wfnsGrade?: number | string;
  wfns_grade?: number | string;
  modified_fisher?: number | string;
  modifiedFisher?: number | string;
  fisher?: number | string;
  grp_vasograde_category?: string;
  vasograde_category?: string;
  [key: string]: any;
}

/**
 * Calculates Vasograde DCI Risk Stratification (Stroke 2014, de Oliveira Manoel et al.).
 * Accepts bivariate inputs { wfns, modified_fisher } or categorical inputs { grp_vasograde_category }.
 *
 * Matrix logic:
 * - Vasograde-Green (1 pt): WFNS 1-2 + Modified Fisher 0-2 (or 1-2)
 * - Vasograde-Amber/Yellow (2 pts): (WFNS 1-2 + Modified Fisher 3-4) OR (WFNS 3 + Modified Fisher 0-2)
 * - Vasograde-Red (3 pts): (WFNS 3 + Modified Fisher 3-4) OR (WFNS 4-5 with any Modified Fisher)
 */
export function calculateVasograde(inputs: Record<string, any>): CalculationResult;
export function calculateVasograde(calc: ClinicalTool, inputs: Record<string, any>): CalculationResult;
export function calculateVasograde(
  calcOrInputs: ClinicalTool | Record<string, any>,
  maybeInputs?: Record<string, any>
): CalculationResult {
  let calc: ClinicalTool | undefined;
  let inputs: Record<string, any>;

  if (
    calcOrInputs &&
    typeof calcOrInputs === 'object' &&
    'parameterGroups' in calcOrInputs &&
    maybeInputs !== undefined
  ) {
    calc = calcOrInputs as ClinicalTool;
    inputs = maybeInputs;
  } else if (
    calcOrInputs &&
    typeof calcOrInputs === 'object' &&
    'parameterGroups' in calcOrInputs
  ) {
    calc = calcOrInputs as ClinicalTool;
    inputs = {};
  } else {
    calc = undefined;
    inputs = (calcOrInputs as Record<string, any>) || {};
  }

  // 1. Direct Option / Category parsing
  let categoryChoice: 'green' | 'yellow' | 'red' | undefined;

  const directCat = inputs.grp_vasograde_category ?? inputs.vasograde_category ?? inputs.category ?? inputs.vasograde;
  if (typeof directCat === 'string') {
    const lower = directCat.toLowerCase();
    if (lower.includes('green') || lower.includes('verde')) {
      categoryChoice = 'green';
    } else if (lower.includes('yellow') || lower.includes('amarelo') || lower.includes('amber')) {
      categoryChoice = 'yellow';
    } else if (lower.includes('red') || lower.includes('vermelho')) {
      categoryChoice = 'red';
    }
  }

  if (!categoryChoice) {
    if (inputs.opt_vaso_red) categoryChoice = 'red';
    else if (inputs.opt_vaso_yellow || inputs.opt_vaso_amber) categoryChoice = 'yellow';
    else if (inputs.opt_vaso_green) categoryChoice = 'green';
  }

  // 2. Bivariate input parsing: WFNS (1-5) and Modified Fisher (0-4)
  let wfnsVal: number | undefined;
  let fisherVal: number | undefined;

  const rawWfns = inputs.wfns ?? inputs.wfnsGrade ?? inputs.wfns_grade ?? inputs.wfnsScore ?? inputs.wfns_score ?? inputs.grp_wfns ?? inputs.grp_wfns_grade;
  if (typeof rawWfns === 'number') {
    wfnsVal = Math.round(rawWfns);
  } else if (typeof rawWfns === 'string') {
    const match = rawWfns.match(/[1-5]/);
    if (match) wfnsVal = parseInt(match[0], 10);
  }

  const rawFisher = inputs.modified_fisher ?? inputs.modifiedFisher ?? inputs.mod_fisher ?? inputs.modFisher ?? inputs.fisher ?? inputs.modified_fisher_grade ?? inputs.grp_fisher_mod ?? inputs.grp_modified_fisher;
  if (typeof rawFisher === 'number') {
    fisherVal = Math.round(rawFisher);
  } else if (typeof rawFisher === 'string') {
    const match = rawFisher.match(/[0-4]/);
    if (match) fisherVal = parseInt(match[0], 10);
  }

  // If bivariate values provided (and category not explicitly chosen via option ID)
  if (!categoryChoice && (wfnsVal !== undefined || fisherVal !== undefined)) {
    const w = wfnsVal ?? 1;
    const f = fisherVal ?? 0;

    if (w >= 4) {
      categoryChoice = 'red';
    } else if (w === 3) {
      categoryChoice = f >= 3 ? 'red' : 'yellow';
    } else {
      // w is 1 or 2
      categoryChoice = f >= 3 ? 'yellow' : 'green';
    }
  }

  // Default fallback if no valid inputs: green
  if (!categoryChoice) {
    categoryChoice = 'green';
  }

  let rawScore: number;
  let severityLevel: 'low' | 'intermediate' | 'high' | 'critical';
  let tierId: string;
  let tierLabel: string;
  let colorHex: string;
  let statisticalOutcome: string;
  let scoreFormatted: string;

  if (categoryChoice === 'red') {
    rawScore = 3;
    severityLevel = 'critical';
    tierId = 'tier_vaso_red';
    tierLabel = 'Vasograde-Red: Alto Risco de DCI e Mau Prognóstico';
    colorHex = '#ef4444';
    statisticalOutcome = 'Incidência de Isquemia Cerebral Tardia (DCI) de 40% a 50% e elevada mortalidade hospitalar (> 50-70%).';
    scoreFormatted = wfnsVal !== undefined && fisherVal !== undefined
      ? `Vasograde-Red (WFNS ${wfnsVal}, Fisher Mod ${fisherVal})`
      : 'Vasograde-Red: Alto Risco de DCI e Mau Prognóstico';
  } else if (categoryChoice === 'yellow') {
    rawScore = 2;
    severityLevel = 'intermediate';
    tierId = 'tier_vaso_yellow';
    tierLabel = 'Vasograde-Yellow: Risco Intermediário de DCI';
    colorHex = '#f59e0b';
    statisticalOutcome = 'Incidência estimada de Isquemia Cerebral Tardia (DCI) de aproximadamente 30% a 35%. Alta taxa de vasoespasmo angiográfico.';
    scoreFormatted = wfnsVal !== undefined && fisherVal !== undefined
      ? `Vasograde-Yellow (WFNS ${wfnsVal}, Fisher Mod ${fisherVal})`
      : 'Vasograde-Yellow: Risco Intermediário de DCI';
  } else {
    rawScore = 1;
    severityLevel = 'low';
    tierId = 'tier_vaso_green';
    tierLabel = 'Vasograde-Green: Baixo Risco de DCI';
    colorHex = '#10b981';
    statisticalOutcome = 'Incidência estimada de Isquemia Cerebral Tardia (DCI) de aproximadamente 15% a 20%. Mortalidade intra-hospitalar baixa (< 10%).';
    scoreFormatted = wfnsVal !== undefined && fisherVal !== undefined
      ? `Vasograde-Green (WFNS ${wfnsVal}, Fisher Mod ${fisherVal})`
      : 'Vasograde-Green: Baixo Risco de DCI';
  }

  let activeRiskTier: RiskTier;
  if (calc?.riskTiers && calc.riskTiers.length > 0) {
    const matched = calc.riskTiers.find((t) => t.id === tierId) ??
      calc.riskTiers.find((t) => t.severityLevel === severityLevel) ??
      calc.riskTiers[0];
    activeRiskTier = matched;
  } else {
    activeRiskTier = {
      id: tierId,
      label: tierLabel,
      severityLevel,
      minScore: rawScore,
      maxScore: rawScore,
      statisticalOutcome,
      colorHex,
      pharmacologicalActions: [
        {
          id: 'rx_vaso_nimo',
          drugName: 'Nimodipino Oral / Enteral',
          dosage: '60 mg VO ou SNE a cada 4 horas por 21 dias contínuos',
          route: 'Oral / SNE exclusiva',
          frequency: '4/4h',
          dilutionInstructions: 'PROIBIDO USO INTRAVENOSO. Se por sonda, aspirar cápsula com seringa oral e lavar com 20 mL de água.',
          contraindications: 'Choque hipotensivo grave refratário.'
        }
      ],
      nonPharmacologicalActions: [
        {
          id: 'non_vaso_mgmt',
          recommendationTitle: tierLabel,
          dispositionTarget: severityLevel === 'critical' ? 'Centro Cirúrgico / Hemodinâmica' : severityLevel === 'intermediate' ? 'UTI Neurocrítica' : 'UTI Neurocrítica / Semi-Intensiva',
          monitoringPlan: 'Doppler Transcraniano (DTC) seriado e controle de euvolemia.',
          interventionalProcedure: severityLevel === 'critical'
            ? 'Implantação emergencial de Derivação Ventricular Externa (DVE) à beira do leito para alívio de hidrocefalia aguda hipertensiva e lavagem liquórica, seguida de oclusão do aneurisma.'
            : 'Oclusão precoce do aneurisma em < 24h a 72h.'
        }
      ]
    };
  }

  const radarValues: Record<string, number> = {};
  if (calc?.radarAxes) {
    for (const axis of calc.radarAxes) {
      radarValues[axis.id] = 0;
    }
  }

  const normClinical = wfnsVal !== undefined ? (wfnsVal - 1) / 4 : (categoryChoice === 'red' ? 1.0 : categoryChoice === 'yellow' ? 0.4 : 0.0);
  const normImaging = fisherVal !== undefined ? fisherVal / 4 : (categoryChoice === 'red' ? 1.0 : categoryChoice === 'yellow' ? 0.75 : 0.2);
  const normDci = categoryChoice === 'red' ? 1.0 : categoryChoice === 'yellow' ? 0.5 : 0.0;

  radarValues['axis_vaso_clinical'] = Math.min(1, Math.max(0, normClinical));
  radarValues['axis_vaso_imaging'] = Math.min(1, Math.max(0, normImaging));
  radarValues['axis_vaso_dci'] = normDci;

  return {
    score: rawScore,
    rawScore,
    scoreFormatted,
    activeRiskTier,
    radarValues,
    radarPoints: radarValues,
    clinicalWarning: calc?.clinicalWarning,
    warnings: calc?.clinicalWarning ? [calc.clinicalWarning] : undefined
  };
}


