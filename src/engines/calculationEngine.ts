import {
  type Calculator,
  type RiskTier,
  type CalculationResult,
  type ParameterGroup,
  type ParameterOption
} from '../types/clinical';

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
  let rawScore = 0;
  const radarValues: Record<string, number> = {};

  // Initialize all defined radar axes with 0 (normal baseline)
  for (const axis of calculator.radarAxes) {
    radarValues[axis.id] = 0;
  }

  // Branching decision specific to Glasgow-P: GCS (3-15) - Pupil Score (0-2)
  if (calculator.id === 'calc_glasgow_p' || calculator.slug === 'glasgow-p') {
    return calculateGlasgowPFromCalculator(calculator, inputs);
  }

  // Process parameter groups
  for (const group of calculator.parameterGroups) {
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
  if (calculator.minPossibleScore !== undefined && rawScore < calculator.minPossibleScore) {
    rawScore = calculator.minPossibleScore;
  }
  if (calculator.maxPossibleScore !== undefined && rawScore > calculator.maxPossibleScore) {
    rawScore = calculator.maxPossibleScore;
  }

  const activeRiskTier = matchRiskTier(calculator.riskTiers, rawScore);
  const warnings: string[] = [];

  let sscWarning: string | undefined;
  if (calculator.ssc2021Warning || calculator.id === 'calc_qsofa' || calculator.slug === 'qsofa') {
    sscWarning = SSC_2021_QSOFA_WARNING;
    warnings.push(SSC_2021_QSOFA_WARNING);
  }

  const clinicalWarning = calculator.clinicalWarning;
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
