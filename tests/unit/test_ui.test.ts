import { describe, it, expect } from 'vitest';
import React from 'react';
import { renderToString } from 'react-dom/server';

import block01Data from '@/data/blocks/block_01.json';
import block03Data from '@/data/blocks/block_03.json';
import type { Calculator } from '@/types/clinical';

import { PhysiologicalRadar } from '@/components/calculator/PhysiologicalRadar';
import { ParameterGroupInput } from '@/components/calculator/ParameterGroupInput';
import { PrescriptionCard } from '@/components/calculator/PrescriptionCard';
import { CalculatorView } from '@/components/calculator/CalculatorView';
import { BottomNav } from '@/components/common/BottomNav';
import { AzScoreList } from '@/components/catalog/AzScoreList';
import { FavoritesView } from '@/components/catalog/FavoritesView';
import { App } from '@/App';

import {
  NOREPINEPHRINE_PROTOCOL,
  VASOPRESSIN_PROTOCOL,
  NITROGLYCERIN_PROTOCOL,
  calculateInfusionRate
} from '@/engines/infusionEngine';
import { calculateScore } from '@/engines/calculationEngine';
import { generatePepNote } from '@/engines/pepExportEngine';

const h = React.createElement;

const calculators = block01Data.calculators as unknown as Calculator[];
const getCalc = (id: string): Calculator => {
  const found = calculators.find((c) => c.id === id);
  if (!found) throw new Error(`Calculator ${id} not found in block_01.json`);
  return found;
};

const qsofaCalc = getCalc('calc_qsofa');
const sofaCalc = getCalc('calc_sofa');
const wellsCalc = getCalc('calc_wells_tep');

// ============================================================================
// 1. PHYSIOLOGICAL RADAR (SVG 60FPS) TESTS
// ============================================================================

describe('PhysiologicalRadar (SVG 60fps)', () => {
  it('renders native SVG with correct viewBox and accessibility attributes', () => {
    const html = renderToString(
      h(PhysiologicalRadar, { axes: qsofaCalc.radarAxes, values: {} })
    );

    expect(html).toContain('<svg');
    expect(html).toContain('viewBox="0 0 300 300"');
    expect(html).toContain('data-testid="physiological-radar-svg"');
    expect(html).toContain('role="img"');
    expect(html).toContain('aria-label="Gráfico de Radar Fisiológico"');
  });

  it('renders concentric background grid rings at standard levels (0.25, 0.5, 0.75, 1.0)', () => {
    const html = renderToString(
      h(PhysiologicalRadar, { axes: qsofaCalc.radarAxes, values: {} })
    );

    expect(html).toContain('data-testid="radar-grid-rings"');
    // qSOFA has 3 axes -> 4 concentric triangular grid polygons
    const ringMatches = html.match(/<polygon[^>]*class="[^"]*text-slate-200/g);
    expect(ringMatches).not.toBeNull();
    expect(ringMatches!.length).toBe(4);
  });

  it('renders radial spokes for each defined physiological axis', () => {
    const html3 = renderToString(
      h(PhysiologicalRadar, { axes: qsofaCalc.radarAxes, values: {} })
    );
    expect(html3).toContain('data-testid="radar-spokes"');
    // 3 spokes for qSOFA
    const spokes3 = html3.match(/<line[^>]*x1="150"/g);
    expect(spokes3!.length).toBe(3);

    const html6 = renderToString(
      h(PhysiologicalRadar, { axes: sofaCalc.radarAxes, values: {} })
    );
    // 6 spokes for SOFA
    const spokes6 = html6.match(/<line[^>]*x1="150"/g);
    expect(spokes6!.length).toBe(6);
  });

  it('renders green baseline homeostatic polygon (r = 0.25)', () => {
    const html = renderToString(
      h(PhysiologicalRadar, { axes: qsofaCalc.radarAxes, values: {} })
    );

    expect(html).toContain('data-testid="radar-baseline-polygon"');
    expect(html).toContain('stroke="#10b981"');
    expect(html).toContain('fill="rgba(16, 185, 129, 0.12)"');
  });

  it('renders dynamic patient deviation overlay polygon reacting to deranged values', () => {
    // Normal baseline (all 0)
    const htmlNormal = renderToString(
      h(PhysiologicalRadar, {
        axes: qsofaCalc.radarAxes,
        values: { axis_qsofa_resp: 0, axis_qsofa_sbp: 0, axis_qsofa_gcs: 0 }
      })
    );
    expect(htmlNormal).toContain('Homeostase');

    // Deranged patient (critical neuro + cardio + resp)
    const htmlCritical = renderToString(
      h(PhysiologicalRadar, {
        axes: qsofaCalc.radarAxes,
        values: { axis_qsofa_resp: 1.0, axis_qsofa_sbp: 1.0, axis_qsofa_gcs: 1.0 }
      })
    );
    expect(htmlCritical).toContain('data-testid="radar-patient-polygon"');
    expect(htmlCritical).toContain('Desvio Crítico');
    expect(htmlCritical).toContain('#ef4444');
  });

  it('renders spoke labels with dynamic text anchors and percentage indicators', () => {
    const html = renderToString(
      h(PhysiologicalRadar, {
        axes: qsofaCalc.radarAxes,
        values: { axis_qsofa_resp: 0.8, axis_qsofa_sbp: 0.5, axis_qsofa_gcs: 0 }
      })
    );

    expect(html).toContain('data-testid="radar-labels"');
    expect(html).toContain('Respiratório');
    expect(html).toContain('(80%)');
    expect(html).toContain('Cardiovascular');
    expect(html).toContain('(50%)');
    expect(html).toContain('Neurológico');
  });

  it('renders graceful card when fewer than 3 axes are provided', () => {
    const twoAxes = qsofaCalc.radarAxes.slice(0, 2);
    const html = renderToString(
      h(PhysiologicalRadar, { axes: twoAxes, values: {} })
    );

    expect(html).toContain('Radar fisiológico requer no mínimo 3 eixos');
    expect(html).not.toContain('<svg');
  });
});

// ============================================================================
// 2. PRESCRIPTION CARD (BEDSIDE BIC MICRO-CALCULATOR) TESTS
// ============================================================================

describe('PrescriptionCard (Bedside BIC Micro-Calculator)', () => {
  it('renders Norepinephrine protocol with standard solution (64 mcg/mL)', () => {
    const html = renderToString(
      h(PrescriptionCard, {
        protocol: NOREPINEPHRINE_PROTOCOL,
        patientWeightKg: 70
      })
    );

    expect(html).toContain('Noradrenalina');
    expect(html).toContain('64 mcg/mL');
    expect(html).toContain('data-testid="prescription-card"');
    expect(html).toContain('data-testid="bic-flow-rate"');
  });

  it('computes exact live flow rate for Noradrenalina at 70kg and 0.1 mcg/kg/min (6.6 mL/h)', () => {
    // Math: (0.1 * 70 * 60) / 64 = 420 / 64 = 6.5625 mL/h -> 6.56 mL/h (formatted: 6.6 mL/h)
    const rateCalc = calculateInfusionRate({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.1,
      concentrationMcgPerMl: 64
    });
    expect(rateCalc.rateMlPerHour).toBe(6.56);

    const html = renderToString(
      h(PrescriptionCard, {
        protocol: NOREPINEPHRINE_PROTOCOL,
        patientWeightKg: 70
      })
    );
    expect(html).toContain('6.6');
    expect(html).toContain('mL/hora');
  });

  it('instant recalculation when patient weight changes from 70kg to 85kg (8.0 mL/h)', () => {
    // Math: (0.1 * 85 * 60) / 64 = 510 / 64 = 7.96875 mL/h -> 7.97 mL/h (formatted: 8.0 mL/h)
    const rateCalc = calculateInfusionRate({
      drugId: 'norepinephrine',
      patientWeightKg: 85,
      doseValue: 0.1,
      concentrationMcgPerMl: 64
    });
    expect(rateCalc.rateMlPerHour).toBe(7.97);

    const html70 = renderToString(
      h(PrescriptionCard, {
        protocol: NOREPINEPHRINE_PROTOCOL,
        patientWeightKg: 70
      })
    );
    expect(html70).toContain('6.6');

    const html85 = renderToString(
      h(PrescriptionCard, {
        protocol: NOREPINEPHRINE_PROTOCOL,
        patientWeightKg: 85
      })
    );
    expect(html85).toContain('8.0');
    expect(html85).toContain('85 kg');
  });

  it('recalculates flow rate for concentrated solution (128 mcg/mL -> 3.28 mL/h)', () => {
    // Math: (0.1 * 70 * 60) / 128 = 420 / 128 = 3.28125 mL/h -> 3.28 mL/h
    const rateCalc = calculateInfusionRate({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.1,
      concentrationMcgPerMl: 128
    });
    expect(rateCalc.rateMlPerHour).toBe(3.28);
  });

  it('renders mandatory vehicle badge for Norepinephrine (SG 5% Obrigatório)', () => {
    const html = renderToString(
      h(PrescriptionCard, {
        protocol: NOREPINEPHRINE_PROTOCOL,
        patientWeightKg: 70
      })
    );

    expect(html).toContain('data-testid="vehicle-notice-badge"');
    expect(html).toContain('SORO GLICOSADO A 5% (SG 5%)');
  });

  it('renders Vasopressin fixed dose protocol (0.03 UI/min -> 9.0 mL/h independent of weight)', () => {
    // Math: (0.03 * 60) / 0.2 = 1.8 / 0.2 = 9.0 mL/h at 50kg, 70kg, 100kg
    const rate70 = calculateInfusionRate({
      drugId: 'vasopressin',
      patientWeightKg: 70,
      doseValue: 0.03,
      concentrationMcgPerMl: 0.2,
      isFixedDose: true
    });
    const rate100 = calculateInfusionRate({
      drugId: 'vasopressin',
      patientWeightKg: 100,
      doseValue: 0.03,
      concentrationMcgPerMl: 0.2,
      isFixedDose: true
    });
    expect(rate70.rateMlPerHour).toBe(9);
    expect(rate100.rateMlPerHour).toBe(9);

    const html = renderToString(
      h(PrescriptionCard, {
        protocol: VASOPRESSIN_PROTOCOL,
        patientWeightKg: 70
      })
    );
    expect(html).toContain('Vasopressina');
    expect(html).toContain('9.0');
    expect(html).toContain('UI/min');
  });

  it('renders Nitroglycerin container alert banner (Glass or Polyolefin mandatory, PVC prohibited)', () => {
    const html = renderToString(
      h(PrescriptionCard, {
        protocol: NITROGLYCERIN_PROTOCOL,
        patientWeightKg: 70
      })
    );

    expect(html).toContain('data-testid="container-alert-banner"');
    expect(html).toContain('VIDRO');
    expect(html).toContain('POLIOLEFINA');
    expect(html).toContain('PROIBIDO frasco/equipo de PVC');
  });

  it('renders Vasopressin association prompt when Norepinephrine dose > 0.25 mcg/kg/min', () => {
    const customNorProtocol = {
      ...NOREPINEPHRINE_PROTOCOL,
      defaultDose: 0.35 // Higher than 0.25 threshold
    };

    const html = renderToString(
      h(PrescriptionCard, {
        protocol: customNorProtocol,
        patientWeightKg: 70
      })
    );

    expect(html).toContain('data-testid="vasopressin-alert-prompt"');
    expect(html).toContain('Vasoplegia Refratária');
    expect(html).toContain('Vasopressina em dose fixa contínua de 0,01 a 0,04 UI/min');
  });

  it('formats plain-text PEP copy adhering to Brazilian SOAP structure', () => {
    // Resolve valid group ids for qsofa
    const result = calculateScore(qsofaCalc, {
      grp_qsofa_resp: 'opt_resp_high',
      grp_qsofa_sbp: 'opt_sbp_low'
    });

    const note = generatePepNote({
      calculator: qsofaCalc,
      result,
      patientBed: 'Leito 04 - UTI',
      patientWeightKg: 70,
      bicInfusion: {
        drugName: 'Noradrenalina',
        dilution: '4 ampolas em SG 5% 234 mL',
        doseFormatted: '0.1 mcg/kg/min',
        rateMlPerHour: 6.6,
        recommendedVehicle: 'Soro Glicosado 5% (SG 5%)'
      }
    });

    expect(note).toContain('[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]');
    expect(note).toContain('PACIENTE: Leito 04 - UTI | Peso: 70 kg');
    expect(note).toContain('S (Subjetivo):');
    expect(note).toContain('O (Objetivo):');
    expect(note).toContain('quick SOFA (Quick Sequential Organ Failure Assessment) (qSOFA) = 2 pontos');
    expect(note).toContain('A (Avaliação):');
    expect(note).toContain('P (Plano / Condutas Imediatas):');
    expect(note).toContain('Noradrenalina em 4 ampolas em SG 5% 234 mL a 0.1 mcg/kg/min (Vazão em BIC: 6.6 mL/h)');
    expect(note).toContain('ALERTA SSC 2021:');
  });
});

// ============================================================================
// 3. PARAMETER GROUP INPUT (48PX ONE-THUMB ZONE) TESTS
// ============================================================================

describe('ParameterGroupInput (48px Touch Targets)', () => {
  it('renders single_choice cards with min-h-touch (48px) and point badges', () => {
    const group = qsofaCalc.parameterGroups[0]; // Frequência Respiratória
    const html = renderToString(
      h(ParameterGroupInput, {
        group,
        value: group.options[0].id,
        onChange: () => {}
      })
    );

    expect(html).toContain(`data-testid="parameter-group-${group.id}"`);
    expect(html).toContain('min-h-touch');
    expect(html).toContain('Frequência Respiratória');
    expect(html).toContain('0 pts');
    expect(html).toContain('+1 pt');
  });

  it('renders boolean options with Sim / Não 48px buttons', () => {
    const booleanGroup = {
      id: 'group_test_bool',
      name: 'Uso de Vasopressor',
      slug: 'vasopressor',
      inputType: 'boolean' as const,
      radarAxisId: 'axis_cardio',
      normalBaselineValue: 0,
      maxAxisValue: 1,
      sortOrder: 1,
      options: [
        { id: 'opt_yes', label: 'Sim', pointValue: 1, isNormalBaseline: false, radarNormalizedValue: 1, sortOrder: 1 },
        { id: 'opt_no', label: 'Não', pointValue: 0, isNormalBaseline: true, radarNormalizedValue: 0, sortOrder: 2 }
      ]
    };

    const html = renderToString(
      h(ParameterGroupInput, {
        group: booleanGroup,
        value: false,
        onChange: () => {}
      })
    );

    expect(html).toContain('Não');
    expect(html).toContain('Sim');
    expect(html).toContain('min-h-touch');
  });

  it('renders numeric_input with plus/minus step buttons', () => {
    const numericGroup = {
      id: 'group_test_num',
      name: 'PaO2/FiO2',
      slug: 'pao2-fio2',
      inputType: 'numeric_input' as const,
      unit: 'mmHg',
      radarAxisId: 'axis_resp',
      normalBaselineValue: 400,
      maxAxisValue: 500,
      minValue: 50,
      maxValue: 600,
      sortOrder: 1,
      options: []
    };

    const html = renderToString(
      h(ParameterGroupInput, {
        group: numericGroup,
        value: 300,
        onChange: () => {}
      })
    );

    expect(html).toContain('PaO2/FiO2');
    expect(html).toContain('mmHg');
    expect(html).toContain('value="300"');
    expect(html).toContain('aria-label="Diminuir PaO2/FiO2"');
    expect(html).toContain('aria-label="Aumentar PaO2/FiO2"');
  });

  it('renders pupil_reactivity cards with visual pupil indicators', () => {
    const pupilGroup = {
      id: 'group_pupils',
      name: 'Reatividade Pupilar',
      slug: 'pupil-reactivity',
      inputType: 'pupil_reactivity' as const,
      radarAxisId: 'axis_neuro',
      normalBaselineValue: 0,
      maxAxisValue: 2,
      sortOrder: 1,
      options: [
        { id: 'p0', label: 'Ambas as pupilas reativas', pointValue: 0, isNormalBaseline: true, radarNormalizedValue: 0, sortOrder: 1 },
        { id: 'p1', label: 'Apenas uma pupila reativa', pointValue: -1, isNormalBaseline: false, radarNormalizedValue: 0.5, sortOrder: 2 },
        { id: 'p2', label: 'Nenhuma pupila reativa', pointValue: -2, isNormalBaseline: false, radarNormalizedValue: 1.0, sortOrder: 3 }
      ]
    };

    const html = renderToString(
      h(ParameterGroupInput, {
        group: pupilGroup,
        value: 'p0',
        onChange: () => {}
      })
    );

    expect(html).toContain('Ambas as pupilas reativas');
    expect(html).toContain('Apenas uma pupila reativa');
    expect(html).toContain('Nenhuma pupila reativa');
    expect(html).toContain('0 pts');
    expect(html).toContain('-1 pt');
    expect(html).toContain('-2 pts');
  });
});

// ============================================================================
// 4. CALCULATOR VIEW & SSC 2021 MANDATORY WARNING TESTS
// ============================================================================

describe('CalculatorView', () => {
  it('renders qSOFA with score display, risk tier badge, radar, and parameters', () => {
    const html = renderToString(
      h(CalculatorView, {
        calculator: qsofaCalc,
        onBack: () => {}
      })
    );

    expect(html).toContain('data-testid="calculator-view"');
    expect(html).toContain('data-testid="score-summary-card"');
    expect(html).toContain('data-testid="score-value-display"');
    expect(html).toContain('data-testid="risk-tier-badge"');
    expect(html).toContain('quick SOFA');
  });

  it('renders mandatory Surviving Sepsis Campaign (SSC 2021) warning banner for qSOFA', () => {
    const html = renderToString(
      h(CalculatorView, {
        calculator: qsofaCalc,
        onBack: () => {}
      })
    );

    expect(html).toContain('data-testid="ssc-2021-warning-banner"');
    expect(html).toContain('Aviso Mandatório SSC 2021 (Surviving Sepsis Campaign)');
    expect(html).toContain('O Surviving Sepsis Campaign (SSC 2021) desaconselha formalmente o uso isolado do qSOFA');
    expect(html).toContain('sensibilidade insuficiente (&lt; 60%)');
  });

  it('does NOT render SSC 2021 warning banner for non-sepsis calculators (Wells PE)', () => {
    const html = renderToString(
      h(CalculatorView, {
        calculator: wellsCalc,
        onBack: () => {}
      })
    );

    expect(html).not.toContain('data-testid="ssc-2021-warning-banner"');
    expect(html).not.toContain('Surviving Sepsis Campaign');
  });

  it('renders non-pharmacological recommendations and disposition target', () => {
    const html = renderToString(
      h(CalculatorView, {
        calculator: qsofaCalc,
        onBack: () => {}
      })
    );

    expect(html).toContain('data-testid="non-pharm-actions-card"');
    expect(html).toContain('Condutas Clínicas Recomendadas');
  });
});

// ============================================================================
// 5. BOTTOM NAVIGATION & ROUTING TESTS
// ============================================================================

describe('BottomNav', () => {
  it('renders all 4 tabs (Todos, Favoritos, Leitos, Plantão)', () => {
    const html = renderToString(
      h(BottomNav, {
        activeTab: 'catalog',
        onTabChange: () => {},
        favoritesCount: 3,
        bedsCount: 1
      })
    );

    expect(html).toContain('data-testid="bottom-nav"');
    expect(html).toContain('data-testid="tab-catalog"');
    expect(html).toContain('data-testid="tab-favorites"');
    expect(html).toContain('data-testid="tab-beds"');
    expect(html).toContain('data-testid="tab-infusions"');
    expect(html).toContain('Todos');
    expect(html).toContain('Favoritos');
    expect(html).toContain('Leitos');
    expect(html).toContain('Plantão');
  });

  it('displays badge counters for favorites and beds', () => {
    const html = renderToString(
      h(BottomNav, {
        activeTab: 'catalog',
        onTabChange: () => {},
        favoritesCount: 5,
        bedsCount: 2
      })
    );

    expect(html).toContain('5');
    expect(html).toContain('2');
  });

  it('highlights the active tab with active indicator styles', () => {
    const htmlCatalog = renderToString(
      h(BottomNav, { activeTab: 'catalog', onTabChange: () => {} })
    );
    expect(htmlCatalog).toContain('text-brand-600 dark:text-brand-400 font-bold');

    const htmlInfusions = renderToString(
      h(BottomNav, { activeTab: 'infusions', onTabChange: () => {} })
    );
    expect(htmlInfusions).toContain('data-testid="tab-infusions"');
  });
});

// ============================================================================
// 6. INTEGRATED APP ASSEMBLY TESTS
// ============================================================================

describe('App Integration', () => {
  it('renders mobile-first app shell with header, theme toggle, and bottom navigation', () => {
    const html = renderToString(h(App));

    expect(html).toContain('Scoreboard');
    expect(html).toContain('CDSS');
    expect(html).toContain('aria-label="Navegação Principal"');
    expect(html).toContain('data-testid="bottom-nav"');
  });

  it('renders catalog search and quick favorites carousel on initial load', () => {
    const html = renderToString(h(App));

    expect(html).toContain('data-testid="az-score-list"');
    expect(html).toContain('role="searchbox"');
    expect(html).toContain('Buscar escore, sigla ou sintoma');
  });

  it('renders active interactive calculator view for Block 03 tools instead of Calculadora em Preparação', () => {
    const rotterdam = (block03Data as any).calculators.find((c: any) => c.id === 'calc_rotterdam');
    expect(rotterdam).toBeDefined();

    const html = renderToString(
      h(CalculatorView, {
        calculator: rotterdam,
        onBack: () => {}
      })
    );

    expect(html).not.toContain('Calculadora em Preparação');
    expect(html).toContain('Rotterdam');
    expect(html).toContain('ponto');
  });

  it('AzScoreList enforces mobile centering with max-w-md mx-auto and citation truncation', () => {
    const html = renderToString(
      h(AzScoreList, {
        onSelectCalculator: () => {}
      })
    );

    expect(html).toContain('max-w-md mx-auto');
    expect(html).toContain('min-w-0 overflow-hidden');
    expect(html).toContain('truncate flex-1 min-w-0');
    expect(html).not.toContain('shrink-0 text-slate-400');
  });

  it('FavoritesView enforces mobile centering with max-w-md mx-auto', () => {
    const html = renderToString(
      h(FavoritesView, {
        onSelectCalculator: () => {}
      })
    );

    expect(html).toContain('max-w-md mx-auto');
  });

  it('verifies that all 58 calculators across Block 01 and Block 03 execute calculateScore without throwing', () => {
    const allCalculators = [...block01Data.calculators, ...block03Data.calculators] as unknown as Calculator[];
    expect(allCalculators.length).toBe(58);

    for (const calc of allCalculators) {
      const defaultInputs: Record<string, any> = {};
      for (const group of calc.parameterGroups) {
        if (group.inputType === 'single_choice' || group.inputType === 'pupil_reactivity') {
          const normalOpt = group.options?.find((o: any) => o.isNormalBaseline || o.pointValue === 0) || group.options?.[0];
          if (normalOpt) defaultInputs[group.id] = normalOpt.id;
        } else if (group.inputType === 'boolean') {
          defaultInputs[group.id] = false;
        } else if (group.inputType === 'numeric_input') {
          defaultInputs[group.id] = group.normalBaselineValue ?? 0;
        }
      }

      const res = calculateScore(calc, defaultInputs);
      expect(res).toBeDefined();
      expect(res.scoreFormatted).toBeDefined();
      expect(res.activeRiskTier).toBeDefined();
      expect(res.activeRiskTier.label).toBeTruthy();
    }
  });
});
