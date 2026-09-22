import {
  type InfusionProtocol,
  type InfusionCalculationParams,
  type InfusionCalculationResult,
  type TitrationStep
} from '../types/infusion';

// ============================================================================
// 1. PROTOCOLOS MESTRES PADRONIZADOS DAS 4 DROGAS VASOATIVAS
// ============================================================================

export const NOREPINEPHRINE_PROTOCOL: InfusionProtocol = {
  drugId: 'norepinephrine',
  drugName: 'Noradrenalina (Hemitartarato de Norepinefrina)',
  standardSolution: {
    ampoules: '4 ampolas (16 mg = 16 mL)',
    diluent: 'Soro Glicosado 5% (SG 5%) 234 mL (Volume total: 250 mL)',
    totalVolumeMl: 250,
    concentrationMcgMl: 64,
    mandatoryVehicleNotice:
      'OBRIGATÓRIO SORO GLICOSADO A 5% (SG 5%). O pH ácido (3,5 a 5,0) estabiliza a catecolamina contra oxidação precoce. Proibido SF contínuo.',
    indication: 'Choque distributivo / séptico, PAM alvo >= 65 mmHg (ou >= 80 mmHg em TCE grave)'
  },
  concentratedSolution: {
    ampoules: '8 ampolas (32 mg = 32 mL)',
    diluent: 'Soro Glicosado 5% (SG 5%) 218 mL (Volume total: 250 mL)',
    totalVolumeMl: 250,
    concentrationMcgMl: 128,
    mandatoryVehicleNotice: 'SG 5% obrigatório. Indicado em restrição hídrica severa, anúria ou SDRA.',
    indication: 'Restrição hídrica / altas doses de vasopressor'
  },
  doseUnit: 'mcg/kg/min',
  initialDose: 0.05,
  maintenanceDoseMin: 0.1,
  maintenanceDoseMax: 0.5,
  maxDose: 2.0,
  defaultDose: 0.1,
  isFixedDose: false,
  administrationRoute: 'Acesso Venoso Central exclusivo (CVC subclávia/jugular)',
  containerCompatibility: 'qualquer',
  nursingPrecautions:
    'Risco extremo de isquemia e necrose tecidual por extravasamento periférico. Monitorizar PAI e perfusão periférica. Em emergência, usar veia antecubital calibrosa por no máximo 2 a 4h até passagem de CVC.',
  titrationAdvice:
    'Titular a cada 2 a 5 minutos até atingir PAM alvo (>= 65 mmHg). Se dose > 0,25 mcg/kg/min, associar precocemente Vasopressina.',
  weaningCriteria: 'Desmame gradual (0,02 a 0,05 mcg/kg/min a cada 15-30 min) após estabilidade de PAM > 65 mmHg e lactato em queda.'
};

export const VASOPRESSIN_PROTOCOL: InfusionProtocol = {
  drugId: 'vasopressin',
  drugName: 'Vasopressina (Arginina Vasopressina)',
  standardSolution: {
    ampoules: '1 ampola (20 UI = 1 mL)',
    diluent: 'Soro Fisiológico 0,9% ou SG 5% 99 mL (Volume total: 100 mL)',
    totalVolumeMl: 100,
    concentrationMcgMl: 0.2, // 0.2 UI/mL
    mandatoryVehicleNotice: 'SF 0,9% ou SG 5% 100 mL (Concentração de 0,2 UI/mL)',
    indication: 'Choque séptico refratário a noradrenalina (> 0,25 mcg/kg/min), poupador de catecolamina'
  },
  doseUnit: 'UI/min',
  initialDose: 0.01,
  maintenanceDoseMin: 0.01,
  maintenanceDoseMax: 0.04,
  maxDose: 0.04,
  defaultDose: 0.03,
  isFixedDose: true, // Independent of weight
  administrationRoute: 'Acesso Venoso Central exclusivo (CVC)',
  containerCompatibility: 'qualquer',
  nursingPrecautions:
    'DOSE FIXA NÃO TITULÁVEL NO CHOQUE SÉPTICO (0,01 a 0,04 UI/min; dose padrão ouro: 0,03 UI/min = 9 mL/h). PROIBIDO titular como noradrenalina ou administrar em bolus: risco gravíssimo de isquemia coronariana e necrose mesentérica.',
  titrationAdvice: 'Manter dose fixa contínua de 0,03 UI/min (9 mL/h). Desmamar a noradrenalina primeiro.',
  weaningCriteria: 'Iniciar desmame da vasopressina somente após desmame completo ou em baixas doses de noradrenalina (< 0,1 mcg/kg/min).'
};

export const DOBUTAMINE_PROTOCOL: InfusionProtocol = {
  drugId: 'dobutamine',
  drugName: 'Dobutamina (Cloridrato de Dobutamina)',
  standardSolution: {
    ampoules: '1 ampola (250 mg = 20 mL)',
    diluent: 'SG 5% ou SF 0,9% 230 mL (Volume total: 250 mL)',
    totalVolumeMl: 250,
    concentrationMcgMl: 1000, // 1.000 mcg/mL
    mandatoryVehicleNotice: 'SG 5% ou SF 0,9% (Concentração de 1.000 mcg/mL)',
    indication: 'Choque cardiogênico, disfunção ventricular aguda, disfunção miocárdica na sepse com hipoperfusão persistente'
  },
  concentratedSolution: {
    ampoules: '2 ampolas (500 mg = 40 mL)',
    diluent: 'SG 5% ou SF 0,9% 210 mL (Volume total: 250 mL)',
    totalVolumeMl: 250,
    concentrationMcgMl: 2000,
    mandatoryVehicleNotice: 'SG 5% ou SF 0,9% (Concentração de 2.000 mcg/mL)',
    indication: 'Restrição volêmica no choque cardiogênico'
  },
  doseUnit: 'mcg/kg/min',
  initialDose: 2.5,
  maintenanceDoseMin: 5.0,
  maintenanceDoseMax: 15.0,
  maxDose: 20.0,
  defaultDose: 5.0,
  isFixedDose: false,
  administrationRoute: 'Acesso Venoso Central (ou periférico transitório calibroso)',
  containerCompatibility: 'qualquer',
  nursingPrecautions:
    'Monitorar ritmo cardíaco contínuo e PA. Risco de taquiarritmias ventriculares e hipotensão paradoxal vasodilatadora por estímulo beta-2. Se PAM < 70 mmHg, associar Noradrenalina antes da Dobutamina.',
  titrationAdvice: 'Ajustar a cada 10-15 minutos em passos de 2,5 mcg/kg/min guiado por débito cardíaco, ScvO2 > 70% e clareamento de lactato.',
  weaningCriteria: 'Desmame gradual de 2,5 mcg/kg/min a cada poucas horas sob monitorização hemodinâmica.'
};

export const NITROGLYCERIN_PROTOCOL: InfusionProtocol = {
  drugId: 'nitroglycerin',
  drugName: 'Nitroglicerina (Tridil)',
  standardSolution: {
    ampoules: '1 ampola (50 mg = 10 mL)',
    diluent: 'SG 5% ou SF 0,9% 240 mL (Volume total: 250 mL)',
    totalVolumeMl: 250,
    concentrationMcgMl: 200, // 200 mcg/mL
    mandatoryVehicleNotice: 'SG 5% ou SF 0,9% (Concentração de 200 mcg/mL)',
    indication: 'Edema Agudo de Pulmão (EAP) hipertensivo, Síndrome Coronariana Aguda (SCA) refratária, crise hipertensiva'
  },
  doseUnit: 'mcg/min',
  initialDose: 5.0,
  maintenanceDoseMin: 10.0,
  maintenanceDoseMax: 100.0,
  maxDose: 200.0,
  defaultDose: 10.0,
  isFixedDose: true, // Dose in mcg/min (independent of weight)
  administrationRoute: 'Acesso Venoso Exclusivo com equipo de polietileno livre de PVC',
  containerCompatibility: 'vidro_polietileno_obrigatorio',
  nursingPrecautions:
    'ALERTA CRÍTICO DE FARMACOTÉCNICA: OBRIGATÓRIO frasco de VIDRO ou POLIOLEFINA/POLIETILENO com equipo próprio de POLIETILENO (livre de PVC). O PVC comum adsorve de 40% a 80% do princípio ativo no plástico. Contraindicado se uso de inibidores da PDE-5 (sildenafil em 24h, tadalafil em 48h) ou infarto de VD.',
  titrationAdvice: 'Titular de 5 a 10 mcg/min (1,5 a 3 mL/h) a cada 5 a 10 minutos conforme PAS e alívio sintomático.',
  weaningCriteria: 'Reduzir progressivamente a cada 15-30 min ao atingir estabilização e transição para vasodilatador oral.'
};

export const STANDARD_PROTOCOLS: Record<string, InfusionProtocol> = {
  norepinephrine: NOREPINEPHRINE_PROTOCOL,
  noradrenalina: NOREPINEPHRINE_PROTOCOL,
  vasopressin: VASOPRESSIN_PROTOCOL,
  vasopressina: VASOPRESSIN_PROTOCOL,
  dobutamine: DOBUTAMINE_PROTOCOL,
  dobutamina: DOBUTAMINE_PROTOCOL,
  nitroglycerin: NITROGLYCERIN_PROTOCOL,
  nitroglicerina: NITROGLYCERIN_PROTOCOL,
  tridil: NITROGLYCERIN_PROTOCOL
};

// ============================================================================
// 2. MOTORES DE CÁLCULO FÍSICO DE INFUSÃO (BIC)
// ============================================================================

/**
 * Calculates continuous IV infusion flow rate in mL/h for BIC.
 *
 * Weight-dependent formula (mcg/kg/min):
 *   Rate (mL/h) = [Dose (mcg/kg/min) * Weight (kg) * 60 min/h] / Concentration (mcg/mL)
 *
 * Absolute rate formula (mcg/min or UI/min):
 *   Rate (mL/h) = [Dose (unit/min) * 60 min/h] / Concentration (unit/mL)
 */
export function calculateInfusionRate(
  params: InfusionCalculationParams & { concentrationUiPerMl?: number }
): InfusionCalculationResult {
  const {
    drugId,
    patientWeightKg,
    doseValue,
    isFixedDose
  } = params;

  const concentration = params.concentrationUiPerMl ?? params.concentrationMcgPerMl;

  const normalizedDrugId = drugId.toLowerCase();
  const protocol = STANDARD_PROTOCOLS[normalizedDrugId];

  // Check whether dose is fixed (weight-independent) or weight-dependent
  const isWeightIndependent =
    isFixedDose ||
    (protocol && (protocol.isFixedDose || protocol.doseUnit === 'UI/min' || protocol.doseUnit === 'mcg/min'));

  if (!isWeightIndependent && (!patientWeightKg || patientWeightKg <= 0)) {
    throw new Error('Patient weight must be greater than zero');
  }

  if (!concentration || concentration <= 0) {
    throw new Error('Solution concentration must be greater than zero');
  }

  if (doseValue < 0) {
    throw new Error('Dose value must be non-negative');
  }

  const safetyAlerts: string[] = [];
  let containerAlert: string | undefined;
  let recommendedVehicle = 'Soro Glicosado 5% (SG 5%) ou SF 0,9%';

  let rawRate = 0;
  if (isWeightIndependent) {
    // Rate = (dose * 60) / concentration
    rawRate = (doseValue * 60) / concentration;
  } else {
    // Rate = (dose * weight * 60) / concentration
    rawRate = (doseValue * patientWeightKg * 60) / concentration;
  }

  // Round rate to 2 decimal places for medical precision
  const rateMlPerHour = Math.round(rawRate * 100) / 100;

  // Drug-specific safety validations and clinical warnings
  if (normalizedDrugId.includes('nor') || normalizedDrugId.includes('norepinephrine')) {
    recommendedVehicle = 'Soro Glicosado 5% (SG 5%) OBRIGATÓRIO (pH 3,5-5,0 estabiliza contra oxidação)';
    safetyAlerts.push('Veículo: Soro Glicosado 5% (SG 5%) obrigatório. Contraindicada a diluição em SF para infusão prolongada.');
    safetyAlerts.push('Acesso venoso central exclusivo obrigatório para prevenir necrose por extravasamento.');

    if (doseValue > 0.25) {
      safetyAlerts.push(
        'ALERTA CLÍNICO: Dose de Noradrenalina > 0,25 mcg/kg/min indica vasoplegia acentuada. Recomenda-se associar Vasopressina em dose fixa (0,01 a 0,04 UI/min) como segundo vasopressor poupador de catecolaminas.'
      );
    }
    if (doseValue > 1.0) {
      safetyAlerts.push('ALERTA DE SEGURANÇA: Dose em faixa crítica (> 1,0 mcg/kg/min). Alto risco de isquemia periférica e visceral.');
    }
  } else if (normalizedDrugId.includes('vaso')) {
    recommendedVehicle = 'Soro Fisiológico 0,9% ou SG 5% (100 mL)';
    safetyAlerts.push('Dose fixa não titulável no choque séptico (0,01 a 0,04 UI/min). Vazão independe do peso do paciente.');
    safetyAlerts.push('Atenção: NÃO administrar em bolus e NÃO titular agressivamente acima de 0,04 UI/min (risco de isquemia miocárdica e mesentérica).');
    if (doseValue > 0.04) {
      safetyAlerts.push('PERIGO: Dose acima de 0,04 UI/min contraindicada formalmente em diretrizes devido a vasoespasmo coronariano grave.');
    }
  } else if (normalizedDrugId.includes('dobut')) {
    recommendedVehicle = 'SG 5% ou SF 0,9%';
    safetyAlerts.push('Monitorização contínua de ECG e PA. Risco de arritmias ventriculares e vasodilatação beta-2.');
    if (doseValue > 20.0) {
      safetyAlerts.push('ALERTA: Dose acima de 20 mcg/kg/min excede o teto recomendado com ganho inotrópico mínimo e toxicidade arrítmica.');
    }
  } else if (normalizedDrugId.includes('nitrog') || normalizedDrugId.includes('tridil')) {
    recommendedVehicle = 'SG 5% ou SF 0,9% em frasco de vidro ou poliolefina';
    containerAlert =
      'OBRIGATÓRIO Frasco de VIDRO ou POLIOLEFINA/POLIETILENO com equipo próprio de POLIETILENO livre de PVC. PROIBIDO frasco/equipo de PVC comum: perda de até 80% da droga por adsorção plástica no plástico.';
    safetyAlerts.push(containerAlert);
    safetyAlerts.push('Contraindicado formalmente se uso recente de inibidores da fosfodiesterase-5 (sildenafil < 24h, tadalafil < 48h).');
  }

  const formattedDose = protocol
    ? `${doseValue} ${protocol.doseUnit}`
    : `${doseValue} (unidade/min)`;

  const concentrationFormatted = `${concentration} ${protocol?.doseUnit === 'UI/min' ? 'UI/mL' : 'mcg/mL'}`;

  return {
    rateMlPerHour,
    recommendedVehicle,
    containerAlert,
    safetyAlerts,
    formattedDose,
    concentrationFormatted
  };
}

/**
 * Reverse calculation: computes the administered dose from an observed BIC rate in mL/h.
 *
 * Weight-dependent:
 *   Dose (mcg/kg/min) = [Rate (mL/h) * Concentration (mcg/mL)] / [Weight (kg) * 60]
 *
 * Weight-independent:
 *   Dose (unit/min) = [Rate (mL/h) * Concentration (unit/mL)] / 60
 */
export function calculateDoseFromRate(
  rateMlPerHour: number,
  concentration: number,
  weightKg?: number,
  unit: 'mcg/kg/min' | 'UI/min' | 'mcg/min' = 'mcg/kg/min'
): number {
  if (unit === 'UI/min' || unit === 'mcg/min' || !weightKg) {
    const dose = (rateMlPerHour * concentration) / 60;
    return Math.round(dose * 1000) / 1000;
  }

  const dose = (rateMlPerHour * concentration) / (weightKg * 60);
  return Math.round(dose * 1000) / 1000;
}

/**
 * Generates a complete bedside titration step matrix for quick reference.
 */
export function generateTitrationMatrix(
  protocol: InfusionProtocol,
  patientWeightKg: number,
  useConcentrated = false
): TitrationStep[] {
  const concentration =
    useConcentrated && protocol.concentratedSolution
      ? protocol.concentratedSolution.concentrationMcgMl
      : protocol.standardSolution.concentrationMcgMl;

  const steps: TitrationStep[] = [];
  const drugId = (protocol.drugId ?? protocol.drugName).toLowerCase();

  if (drugId.includes('vaso')) {
    // Vasopressin fixed steps: 0.01, 0.02, 0.03, 0.04 UI/min
    const doses = [0.01, 0.02, 0.03, 0.04];
    for (const d of doses) {
      const rate = Math.round(((d * 60) / concentration) * 10) / 10;
      steps.push({
        dose: d,
        rateMlPerHour: rate,
        label: `${d} UI/min${d === 0.03 ? ' (Dose Padrão Ouro)' : ''}`,
        isWarning: d > 0.04
      });
    }
    return steps;
  }

  if (drugId.includes('nitrog') || drugId.includes('tridil')) {
    // Nitroglycerin absolute steps in mcg/min: 5, 10, 20, 30, 50, 100, 150, 200
    const doses = [5, 10, 20, 30, 50, 100, 150, 200];
    for (const d of doses) {
      const rate = Math.round(((d * 60) / concentration) * 10) / 10;
      steps.push({
        dose: d,
        rateMlPerHour: rate,
        label: `${d} mcg/min`,
        isWarning: d >= 200
      });
    }
    return steps;
  }

  if (drugId.includes('nor')) {
    // Norepinephrine steps in mcg/kg/min
    const doses = [0.05, 0.1, 0.15, 0.2, 0.25, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0];
    for (const d of doses) {
      const rate = Math.round(((d * patientWeightKg * 60) / concentration) * 10) / 10;
      steps.push({
        dose: d,
        rateMlPerHour: rate,
        label: `${d.toFixed(2)} mcg/kg/min${d > 0.25 ? ' (Associar Vasopressina)' : ''}`,
        isWarning: d > 0.25
      });
    }
    return steps;
  }

  if (drugId.includes('dobut')) {
    // Dobutamine steps in mcg/kg/min: 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0
    const doses = [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0];
    for (const d of doses) {
      const rate = Math.round(((d * patientWeightKg * 60) / concentration) * 10) / 10;
      steps.push({
        dose: d,
        rateMlPerHour: rate,
        label: `${d.toFixed(1)} mcg/kg/min`,
        isWarning: d >= 20.0
      });
    }
    return steps;
  }

  // Generic generator for custom protocols
  const min = protocol.maintenanceDoseMin || protocol.initialDose;
  const max = protocol.maxDose;
  const stepCount = 6;
  const increment = (max - min) / (stepCount - 1);

  for (let i = 0; i < stepCount; i++) {
    const d = Math.round((min + i * increment) * 100) / 100;
    const rate = protocol.isFixedDose
      ? Math.round(((d * 60) / concentration) * 10) / 10
      : Math.round(((d * patientWeightKg * 60) / concentration) * 10) / 10;
    steps.push({
      dose: d,
      rateMlPerHour: rate,
      label: `${d} ${protocol.doseUnit}`,
      isWarning: d >= max
    });
  }

  return steps;
}
