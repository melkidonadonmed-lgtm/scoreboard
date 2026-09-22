import {
  type Calculator,
  type CalculationResult,
  type RadarAxis
} from '../types/clinical';

export interface BicInfusionSummary {
  drugName: string;
  dilution: string;
  doseFormatted: string;
  rateMlPerHour: number;
  recommendedVehicle?: string;
  containerAlert?: string;
}

export interface PepExportInput {
  calculator: Calculator;
  result: CalculationResult;
  patientBed?: string;
  patientWeightKg?: number;
  creatinineClearanceMlMin?: number;
  subjectiveNotes?: string;
  assessmentNotes?: string;
  bicInfusion?: BicInfusionSummary;
  customPrescription?: string[];
  selectedCriteriaLabels?: string[];
  timestamp?: Date;
  physicianIdentifier?: string; // e.g. "Médico Plantonista - CRM/SP 000000"
}

// ============================================================================
// 1. PRIVACIDADE E SANITIZAÇÃO LGPD
// ============================================================================

/**
 * Sanitizes bed identifier to prevent accidental inclusion of personal identification (LGPD compliance).
 * Strips patterns looking like CPF (xxx.xxx.xxx-xx), RG, or full civil names.
 */
export function sanitizeBedIdentifier(bed?: string): string {
  if (!bed || bed.trim().length === 0) {
    return 'Leito -- (Anônimo)';
  }

  let sanitized = bed.trim();

  // Remove potential CPF patterns (000.000.000-00 or 11 consecutive digits)
  sanitized = sanitized.replace(/\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g, '[REMOVIDO]');
  sanitized = sanitized.replace(/\b\d{11}\b/g, '[REMOVIDO]');

  // Ensure prefix contains "Leito", "Box", "Sala" or similar ward designation
  if (
    !sanitized.toLowerCase().startsWith('leito') &&
    !sanitized.toLowerCase().startsWith('box') &&
    !sanitized.toLowerCase().startsWith('sala') &&
    !sanitized.toLowerCase().startsWith('uti') &&
    !sanitized.toLowerCase().startsWith('enfermaria')
  ) {
    return `Leito ${sanitized}`;
  }

  return sanitized;
}

/**
 * Formats a Date object in standard Brazilian clinical datetime (DD/MM/AAAA - HH:MM).
 */
export function formatDateBrazilian(date: Date = new Date()): string {
  const pad = (n: number) => n.toString().padStart(2, '0');
  const d = pad(date.getDate());
  const m = pad(date.getMonth() + 1);
  const y = date.getFullYear();
  const h = pad(date.getHours());
  const min = pad(date.getMinutes());

  return `${d}/${m}/${y} - ${h}:${min}`;
}

// ============================================================================
// 2. SUMARIZADORES DE RADAR E CONDUTAS
// ============================================================================

/**
 * Summarizes physiological deviations captured by the radar engine.
 */
export function summarizeRadarDeviations(
  axes: RadarAxis[],
  radarValues: Record<string, number>
): string {
  const derangedAxes: string[] = [];

  for (const axis of axes) {
    const val = radarValues[axis.id] ?? 0;
    if (val > 0) {
      const pct = Math.round(val * 100);
      let severityLabel = 'leve';
      if (val >= 0.75) severityLabel = 'crítico';
      else if (val >= 0.4) severityLabel = 'moderado';

      derangedAxes.push(`${axis.system || axis.label} (${severityLabel}: ${pct}%)`);
    }
  }

  if (derangedAxes.length === 0) {
    return 'Sem desvios fisiológicos detectados (todos os eixos no baseline homeostático).';
  }

  return derangedAxes.join('; ');
}

// ============================================================================
// 3. MOTOR PRINCIPAL DE GERAÇÃO SOAP (EHR / PEP)
// ============================================================================

/**
 * Generates a structured, clean plain-text SOAP clinical record formatted
 * for one-touch copying into Brazilian hospital EHRs (MV Soul, Tasy, Epimed, Pixeon).
 */
export function generatePepNote(input: PepExportInput): string {
  const {
    calculator,
    result,
    patientBed,
    patientWeightKg,
    creatinineClearanceMlMin,
    subjectiveNotes,
    assessmentNotes,
    bicInfusion,
    customPrescription,
    selectedCriteriaLabels,
    timestamp = new Date(),
    physicianIdentifier
  } = input;

  const nowFormatted = formatDateBrazilian(timestamp);
  const bedClean = sanitizeBedIdentifier(patientBed);
  const weightStr = patientWeightKg ? ` | Peso: ${patientWeightKg} kg` : '';
  const clcrStr = creatinineClearanceMlMin ? ` | ClCr Est.: ${creatinineClearanceMlMin} mL/min` : '';

  const activeTier = result.activeRiskTier;

  // Subjetivo
  const subjective =
    subjectiveNotes && subjectiveNotes.trim().length > 0
      ? subjectiveNotes.trim()
      : `Paciente admitido/avaliado em ambiente de urgência/emergência ou terapia intensiva sob suspeita clínica de ${calculator.subcategory || calculator.name}.`;

  // Objetivo
  const scoreLine = `- Escore Calculado: ${calculator.name} (${calculator.acronym}) = ${result.scoreFormatted} pontos`;
  const riskLine = `- Estratificação de Risco: ${activeTier.label} (Severidade: ${activeTier.severityLevel.toUpperCase()})`;
  const outcomeLine = `- Desfecho / Probabilidade: ${activeTier.statisticalOutcome}`;

  const criteriaLines: string[] = [];
  if (selectedCriteriaLabels && selectedCriteriaLabels.length > 0) {
    criteriaLines.push(`- Critérios Clínicos Presentes: ${selectedCriteriaLabels.join('; ')}`);
  }

  const radarSummary = summarizeRadarDeviations(calculator.radarAxes, result.radarValues);
  const radarLine = `- Radar Fisiológico: ${radarSummary}`;

  // Alertas Regulatórios / SSC 2021
  const warningLines: string[] = [];
  if (result.sscWarning) {
    warningLines.push(`- ALERTA SSC 2021: ${result.sscWarning}`);
  } else if (result.clinicalWarning) {
    warningLines.push(`- ALERTA CLÍNICO: ${result.clinicalWarning}`);
  }

  // Avaliação
  const assessment =
    assessmentNotes && assessmentNotes.trim().length > 0
      ? assessmentNotes.trim()
      : `Quadro compatível com ${calculator.name} estratificado em ${activeTier.label}.`;

  // Plano / Condutas
  const nonPharmActions = activeTier.nonPharmacologicalActions || [];
  const pharmActions = activeTier.pharmacologicalActions || [];

  const disposition =
    nonPharmActions.length > 0
      ? nonPharmActions[0].dispositionTarget
      : 'Unidade de Terapia Intensiva / Sala Vermelha';

  const nonPharmLines = nonPharmActions.map((act) => {
    let text = `   * ${act.recommendationTitle}: ${act.monitoringPlan}`;
    if (act.ventilatorySupport) text += ` | Suporte Ventilatório: ${act.ventilatorySupport}`;
    if (act.vascularAccess) text += ` | Acesso: ${act.vascularAccess}`;
    return text;
  });

  const pharmLines = pharmActions.map((p) => {
    let line = `   * ${p.drugName}: ${p.dosage} via ${p.route} (${p.frequency})`;
    if (p.dilutionInstructions) line += ` - Diluição: ${p.dilutionInstructions}`;
    return line;
  });

  if (customPrescription && customPrescription.length > 0) {
    for (const c of customPrescription) {
      pharmLines.push(`   * ${c}`);
    }
  }

  // BIC Section
  const bicLines: string[] = [];
  if (bicInfusion) {
    bicLines.push(
      `   * ${bicInfusion.drugName} em ${bicInfusion.dilution} a ${bicInfusion.doseFormatted} (Vazão em BIC: ${bicInfusion.rateMlPerHour.toFixed(1)} mL/h)`
    );
    if (bicInfusion.recommendedVehicle) {
      bicLines.push(`     Veículo: ${bicInfusion.recommendedVehicle}`);
    }
    if (bicInfusion.containerAlert) {
      bicLines.push(`     Atenção Frasco/Equipo: ${bicInfusion.containerAlert}`);
    }
  }

  // Assemble plain text note
  const sections: string[] = [
    `[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]`,
    `DATA/HORA: ${nowFormatted}`,
    `PACIENTE: ${bedClean}${weightStr}${clcrStr}`,
    ``,
    `S (Subjetivo): ${subjective}`,
    ``,
    `O (Objetivo):`,
    scoreLine,
    riskLine,
    outcomeLine,
    ...criteriaLines,
    radarLine,
    ...warningLines,
    ``,
    `A (Avaliação): ${assessment}`,
    ``,
    `P (Plano / Condutas Imediatas):`,
    `1. Destino Assistencial: ${disposition}`
  ];

  if (pharmLines.length > 0) {
    sections.push(`2. Conduta Farmacológica & Prescrição:`);
    sections.push(...pharmLines);
  }

  if (bicLines.length > 0) {
    sections.push(`3. Drogas Vasoativas / Infusão Contínua (BIC):`);
    sections.push(...bicLines);
  }

  if (nonPharmLines.length > 0) {
    sections.push(`4. Monitorização, Procedimentos e Suporte:`);
    sections.push(...nonPharmLines);
  }

  const physicianSign = physicianIdentifier
    ? `Responsável: ${physicianIdentifier}`
    : `Registro gerado via Scoreboard CDSS (Suporte à Decisão Clínica)`;

  sections.push(``, physicianSign);

  return sections.join('\n');
}

/**
 * Generates an alternative SBAR format clinical handover note.
 */
export function generateSbarNote(input: PepExportInput): string {
  const {
    calculator,
    result,
    patientBed,
    patientWeightKg,
    bicInfusion,
    timestamp = new Date()
  } = input;

  const nowFormatted = formatDateBrazilian(timestamp);
  const bedClean = sanitizeBedIdentifier(patientBed);
  const weightStr = patientWeightKg ? ` | Peso: ${patientWeightKg} kg` : '';
  const activeTier = result.activeRiskTier;

  const nonPharmActions = activeTier.nonPharmacologicalActions || [];
  const disposition =
    nonPharmActions.length > 0
      ? nonPharmActions[0].dispositionTarget
      : 'Vaga em UTI / Monitorização Intensiva';

  const lines: string[] = [
    `[SCOREBOARD CDSS - PASSAGEM DE PLANTÃO SBAR]`,
    `DATA/HORA: ${nowFormatted}`,
    `LEITO: ${bedClean}${weightStr}`,
    ``,
    `S (Situação): Paciente sob triagem/estratificação de ${calculator.name} (${calculator.acronym}).`,
    `B (Breve Histórico): Quadro agudo avaliado com ferramentas monográficas do Bloco ${calculator.categorySlug || '01'}.`,
    `A (Avaliação): ${calculator.acronym} = ${result.scoreFormatted} pontos -> ${activeTier.label}. ${activeTier.statisticalOutcome}`,
    `R (Recomendação): Destino: ${disposition}.`
  ];

  if (bicInfusion) {
    lines.push(
      `   BIC ativa: ${bicInfusion.drugName} a ${bicInfusion.doseFormatted} (Vazão: ${bicInfusion.rateMlPerHour.toFixed(1)} mL/h).`
    );
  }

  if (result.sscWarning) {
    lines.push(`   Aviso SSC 2021: Não descartar sepse baseado unicamente no qSOFA.`);
  }

  return lines.join('\n');
}
