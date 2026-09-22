import React, { useState, useMemo } from 'react';
import type { PharmacologicalAction, Calculator, CalculationResult } from '@/types/clinical';
import type { InfusionProtocol, SolutionRecipe } from '@/types/infusion';
import {
  calculateInfusionRate,
  NOREPINEPHRINE_PROTOCOL,
  VASOPRESSIN_PROTOCOL,
  DOBUTAMINE_PROTOCOL,
  NITROGLYCERIN_PROTOCOL
} from '@/engines/infusionEngine';
import { generatePepNote } from '@/engines/pepExportEngine';
import {
  Droplets,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  ShieldAlert,
  Flame,
  Scale,
  Minus,
  Plus,
  Info
} from 'lucide-react';

export interface PrescriptionCardProps {
  protocol?: InfusionProtocol;
  pharmacologicalAction?: PharmacologicalAction;
  calculator?: Calculator;
  calculationResult?: CalculationResult;
  patientWeightKg?: number;
  onWeightChange?: (weight: number) => void;
  bedLabel?: string;
  defaultExpanded?: boolean;
  className?: string;
}

/**
 * Resolves standard infusion protocol from action name or drugId.
 */
function resolveProtocol(
  protocol?: InfusionProtocol,
  action?: PharmacologicalAction
): InfusionProtocol {
  if (protocol) return protocol;
  if (action?.infusionProtocol) return action.infusionProtocol;

  const targetName = (action?.drugName || '').toLowerCase();
  if (targetName.includes('nor') || targetName.includes('norepi')) return NOREPINEPHRINE_PROTOCOL;
  if (targetName.includes('vaso')) return VASOPRESSIN_PROTOCOL;
  if (targetName.includes('dobut')) return DOBUTAMINE_PROTOCOL;
  if (targetName.includes('nitrog') || targetName.includes('tridil')) return NITROGLYCERIN_PROTOCOL;

  return NOREPINEPHRINE_PROTOCOL;
}

/**
 * Bedside BIC Prescription Drawer & Micro-Calculator.
 * Features:
 * - Real-time mL/h recalculation upon dose or patient weight change
 * - Dilution recipe selection (standard vs concentrated)
 * - Vehicle notice (e.g. SG 5% mandatory for Noradrenaline)
 * - Container alert banner (e.g. Glass / polyolefin mandatory for Nitroglycerin)
 * - Vasopressin clinical prompt when Noradrenaline > 0.25 mcg/kg/min
 * - 1-Touch "Copiar para PEP" button with temporary visual confirmation badge
 */
export const PrescriptionCard: React.FC<PrescriptionCardProps> = ({
  protocol: explicitProtocol,
  pharmacologicalAction,
  calculator,
  calculationResult,
  patientWeightKg = 70,
  onWeightChange,
  bedLabel = 'Leito 04 - UTI',
  defaultExpanded = true,
  className = ''
}) => {
  const protocol = useMemo(
    () => resolveProtocol(explicitProtocol, pharmacologicalAction),
    [explicitProtocol, pharmacologicalAction]
  );

  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [selectedSolutionType, setSelectedSolutionType] = useState<'standard' | 'concentrated'>('standard');
  const [dose, setDose] = useState<number>(protocol.defaultDose);
  const [internalWeight, setInternalWeight] = useState<number>(patientWeightKg);
  const [copied, setCopied] = useState(false);

  // Sync internal weight if prop changes
  const effectiveWeight = onWeightChange ? patientWeightKg : internalWeight;
  const updateWeight = (newWeight: number) => {
    const valid = Math.max(20, Math.min(250, newWeight));
    if (onWeightChange) {
      onWeightChange(valid);
    } else {
      setInternalWeight(valid);
    }
  };

  // Active solution recipe
  const activeRecipe: SolutionRecipe = useMemo(() => {
    if (selectedSolutionType === 'concentrated' && protocol.concentratedSolution) {
      return protocol.concentratedSolution;
    }
    return protocol.standardSolution;
  }, [protocol, selectedSolutionType]);

  // Live calculation of BIC flow rate in mL/h
  const calculation = useMemo(() => {
    try {
      return calculateInfusionRate({
        drugId: protocol.drugId || protocol.drugName,
        patientWeightKg: effectiveWeight,
        doseValue: dose,
        concentrationMcgPerMl: activeRecipe.concentrationMcgMl,
        isFixedDose: protocol.isFixedDose
      });
    } catch (err: any) {
      return {
        rateMlPerHour: 0,
        recommendedVehicle: activeRecipe.mandatoryVehicleNotice || 'Veículo padrão',
        containerAlert: undefined,
        safetyAlerts: [err.message || 'Erro no cálculo de infusão.'],
        formattedDose: `${dose} ${protocol.doseUnit}`,
        concentrationFormatted: `${activeRecipe.concentrationMcgMl} mcg/mL`
      };
    }
  }, [protocol, effectiveWeight, dose, activeRecipe]);

  // Dose step sizing based on drug
  const doseStep = useMemo(() => {
    if (protocol.doseUnit === 'UI/min') return 0.01;
    if (protocol.doseUnit === 'mcg/min') return 5;
    if (protocol.maxDose <= 2.0) return 0.05;
    return 1.0;
  }, [protocol]);

  const handleStepDose = (delta: number) => {
    const next = Math.max(0, Math.min(protocol.maxDose * 1.5, Math.round((dose + delta) * 100) / 100));
    setDose(next);
  };

  // Check for Vasopressin association prompt (Noradrenalina > 0.25 mcg/kg/min)
  const isNoradrenaline =
    (protocol.drugId || protocol.drugName).toLowerCase().includes('nor');
  const showVasopressinPrompt = isNoradrenaline && dose > 0.25;

  // Check for Nitroglycerin glass/polyolefin warning
  const isNitroglycerin =
    (protocol.drugId || protocol.drugName).toLowerCase().includes('nitrog') ||
    (protocol.drugId || protocol.drugName).toLowerCase().includes('tridil');

  // One-touch PEP/EHR clipboard copy
  const handleCopyPep = async () => {
    let textToCopy = '';

    if (calculator && calculationResult) {
      textToCopy = generatePepNote({
        calculator,
        result: calculationResult,
        patientBed: bedLabel,
        patientWeightKg: effectiveWeight,
        bicInfusion: {
          drugName: protocol.drugName,
          dilution: `${activeRecipe.ampoules} + ${activeRecipe.diluent}`,
          doseFormatted: calculation.formattedDose,
          rateMlPerHour: calculation.rateMlPerHour,
          recommendedVehicle: calculation.recommendedVehicle,
          containerAlert: calculation.containerAlert
        }
      });
    } else {
      // Standalone BIC prescription summary
      textToCopy = [
        `[PRESCRIÇÃO BIC - SCOREBOARD CDSS]`,
        `LEITO: ${bedLabel} | PESO: ${effectiveWeight} kg`,
        `DROGA: ${protocol.drugName}`,
        `SOLUÇÃO (${selectedSolutionType === 'concentrated' ? 'CONCENTRADA' : 'PADRÃO'}): ${activeRecipe.ampoules} em ${activeRecipe.diluent}`,
        `CONCENTRAÇÃO: ${activeRecipe.concentrationMcgMl} ${protocol.doseUnit === 'UI/min' ? 'UI/mL' : 'mcg/mL'}`,
        `DOSE: ${calculation.formattedDose}`,
        `VAZÃO EM BIC: ${calculation.rateMlPerHour.toFixed(1)} mL/h`,
        `VEÍCULO: ${calculation.recommendedVehicle}`,
        protocol.administrationRoute ? `ACESSO: ${protocol.administrationRoute}` : '',
        calculation.containerAlert ? `ATENÇÃO FRASCO/EQUIPO: ${calculation.containerAlert}` : '',
        showVasopressinPrompt ? `ALERTA: Dose > 0,25 mcg/kg/min — associar Vasopressina em dose fixa (0,01 a 0,04 UI/min).` : ''
      ]
        .filter(Boolean)
        .join('\n');
    }

    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(textToCopy);
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div
      className={`rounded-2xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-card overflow-hidden transition-all duration-200 ${className}`}
      data-testid="prescription-card"
    >
      {/* Header Drawer Toggle */}
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full min-h-touch px-4 py-3.5 flex items-center justify-between bg-surface-raised-light dark:bg-surface-raised-dark hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors select-none text-left"
        aria-expanded={isExpanded}
        data-testid="toggle-bic-drawer"
      >
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-clinical-info/15 text-clinical-info flex items-center justify-center shrink-0">
            <Droplets className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">
                {protocol.drugName}
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.2 rounded bg-clinical-info/10 text-clinical-info">
                BIC
              </span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">
              Vazão calculada: <strong className="text-clinical-info tabular-nums">{calculation.rateMlPerHour.toFixed(1)} mL/h</strong> à dose de {calculation.formattedDose}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          <div className="text-right hidden sm:block">
            <span className="text-base font-extrabold tabular-nums text-clinical-info">
              {calculation.rateMlPerHour.toFixed(1)}
            </span>
            <span className="text-xs text-slate-500 dark:text-slate-400 ml-1">mL/h</span>
          </div>
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-slate-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-slate-400" />
          )}
        </div>
      </button>

      {/* Expanded Drawer Content */}
      {isExpanded && (
        <div className="p-4 space-y-4 border-t border-subtle-light dark:border-subtle-dark">
          {/* Main BIC Rate Hero Card */}
          <div className="p-4 rounded-xl bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark flex items-center justify-between">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 block">
                Vazão em Bomba de Infusão Contínua (BIC)
              </span>
              <div className="flex items-baseline space-x-2 mt-1">
                <span
                  className="text-3xl sm:text-4xl font-black tabular-nums text-clinical-info tracking-tight"
                  data-testid="bic-flow-rate"
                >
                  {calculation.rateMlPerHour.toFixed(1)}
                </span>
                <span className="text-sm font-bold text-slate-500 dark:text-slate-400">
                  mL/hora
                </span>
              </div>
              <span className="text-xs text-slate-500 dark:text-slate-400 block mt-0.5">
                Solução: {`${activeRecipe.concentrationMcgMl} ${protocol.doseUnit === 'UI/min' ? 'UI/mL' : 'mcg/mL'}`} ({selectedSolutionType === 'concentrated' ? 'Concentrada' : 'Padrão'})
              </span>
            </div>

            {/* Quick Copy Action */}
            <button
              type="button"
              onClick={handleCopyPep}
              className={`min-h-touch min-w-touch px-3 py-2.5 rounded-xl flex items-center space-x-1.5 text-xs font-semibold transition-all select-none ${
                copied
                  ? 'bg-emerald-500 text-white shadow-card scale-95'
                  : 'bg-brand-500 text-white hover:bg-brand-600 active:scale-95 shadow-sm'
              }`}
              data-testid="copy-pep-button"
            >
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              <span>{copied ? 'Copiado!' : 'Copiar PEP'}</span>
            </button>
          </div>

          {/* Solution Recipe Selector (Standard vs Concentrated) */}
          {protocol.concentratedSolution && (
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
                Diluição / Concentração
              </label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={() => setSelectedSolutionType('standard')}
                  className={`min-h-touch p-2.5 rounded-xl border text-left text-xs transition-all ${
                    selectedSolutionType === 'standard'
                      ? 'border-brand-500 bg-brand-50/70 dark:bg-brand-950/40 text-brand-900 dark:text-brand-100 font-semibold ring-1 ring-brand-500/20'
                      : 'border-subtle-light dark:border-subtle-dark bg-surface-raised-light dark:bg-surface-raised-dark text-slate-600 dark:text-slate-400'
                  }`}
                  data-testid="select-standard-dilution"
                >
                  <div className="font-bold">Solução Padrão</div>
                  <div className="text-[11px] opacity-80">{protocol.standardSolution.ampoules}</div>
                  <div className="text-[10px] opacity-70">{protocol.standardSolution.concentrationMcgMl} mcg/mL</div>
                </button>

                <button
                  type="button"
                  onClick={() => setSelectedSolutionType('concentrated')}
                  className={`min-h-touch p-2.5 rounded-xl border text-left text-xs transition-all ${
                    selectedSolutionType === 'concentrated'
                      ? 'border-brand-500 bg-brand-50/70 dark:bg-brand-950/40 text-brand-900 dark:text-brand-100 font-semibold ring-1 ring-brand-500/20'
                      : 'border-subtle-light dark:border-subtle-dark bg-surface-raised-light dark:bg-surface-raised-dark text-slate-600 dark:text-slate-400'
                  }`}
                  data-testid="select-concentrated-dilution"
                >
                  <div className="font-bold">Concentrada (2x)</div>
                  <div className="text-[11px] opacity-80">{protocol.concentratedSolution.ampoules}</div>
                  <div className="text-[10px] opacity-70">{protocol.concentratedSolution.concentrationMcgMl} mcg/mL</div>
                </button>
              </div>
            </div>
          )}

          {/* Dose Adjustment Slider & Step Buttons */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
                Dose Prescrita ({protocol.doseUnit})
              </label>
              <span className="text-xs font-bold text-brand-600 dark:text-brand-400 tabular-nums">
                {calculation.formattedDose}
              </span>
            </div>

            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={() => handleStepDose(-doseStep)}
                disabled={dose <= 0}
                className="w-12 h-12 rounded-xl flex items-center justify-center bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark disabled:opacity-40 active:scale-95 transition-all text-slate-700 dark:text-slate-200"
                aria-label="Diminuir dose"
                data-testid="dose-decrease-btn"
              >
                <Minus className="w-5 h-5" />
              </button>

              <div className="flex-1 min-h-touch px-3 py-2 rounded-xl bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark flex items-center justify-center space-x-1.5">
                <input
                  type="number"
                  step={doseStep}
                  min={0}
                  max={protocol.maxDose * 2}
                  value={dose}
                  onChange={(e) => {
                    const parsed = parseFloat(e.target.value);
                    if (!isNaN(parsed) && parsed >= 0) setDose(parsed);
                  }}
                  className="w-24 text-center font-bold text-lg tabular-nums bg-transparent text-slate-900 dark:text-white outline-none"
                  aria-label={`Dose em ${protocol.doseUnit}`}
                  data-testid="dose-input"
                />
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
                  {protocol.doseUnit}
                </span>
              </div>

              <button
                type="button"
                onClick={() => handleStepDose(doseStep)}
                className="w-12 h-12 rounded-xl flex items-center justify-center bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark active:scale-95 transition-all text-slate-700 dark:text-slate-200"
                aria-label="Aumentar dose"
                data-testid="dose-increase-btn"
              >
                <Plus className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Patient Weight Adjuster (Weight-Dependent Drugs) */}
          {!protocol.isFixedDose && (
            <div className="space-y-2 pt-1 border-t border-subtle-light/60 dark:border-subtle-dark/60">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-1.5 text-xs font-bold text-slate-700 dark:text-slate-300">
                  <Scale className="w-3.5 h-3.5 text-slate-400" />
                  <span>Peso do Paciente (kg)</span>
                </div>
                <span className="text-xs font-bold text-slate-900 dark:text-white tabular-nums">
                  {`${effectiveWeight} kg`}
                </span>
              </div>

              {/* Quick weight selector chips */}
              <div className="flex items-center space-x-1.5 overflow-x-auto no-scrollbar py-1">
                {[50, 60, 70, 80, 85, 90, 100].map((w) => (
                  <button
                    key={`weight-chip-${w}`}
                    type="button"
                    onClick={() => updateWeight(w)}
                    className={`min-h-touch px-3 py-1.5 rounded-xl text-xs font-semibold tabular-nums shrink-0 transition-all ${
                      effectiveWeight === w
                        ? 'bg-brand-500 text-white shadow-card'
                        : 'bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                    }`}
                    data-testid={`weight-btn-${w}`}
                  >
                    {`${w} kg`}
                  </button>
                ))}
              </div>

              {/* Weight Stepper */}
              <div className="flex items-center space-x-2">
                <button
                  type="button"
                  onClick={() => updateWeight(effectiveWeight - 1)}
                  className="w-10 h-10 rounded-lg flex items-center justify-center bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-300"
                  aria-label="Diminuir peso em 1 kg"
                  data-testid="weight-decrease-1kg"
                >
                  <Minus className="w-4 h-4" />
                </button>
                <div className="flex-1 text-center font-bold text-sm text-slate-900 dark:text-white tabular-nums">
                  {`${effectiveWeight} kg`}
                </div>
                <button
                  type="button"
                  onClick={() => updateWeight(effectiveWeight + 1)}
                  className="w-10 h-10 rounded-lg flex items-center justify-center bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-300"
                  aria-label="Aumentar peso em 1 kg"
                  data-testid="weight-increase-1kg"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Clinical Vehicle Requirement Badge */}
          {activeRecipe.mandatoryVehicleNotice && (
            <div
              className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-700 dark:text-amber-300 flex items-start space-x-2.5"
              data-testid="vehicle-notice-badge"
            >
              <Info className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
              <div>
                <strong className="block font-bold">Veículo Obrigatório:</strong>
                <span>{activeRecipe.mandatoryVehicleNotice}</span>
              </div>
            </div>
          )}

          {/* Nitroglycerin Container Alert Banner */}
          {(isNitroglycerin || calculation.containerAlert) && (
            <div
              className="p-3 rounded-xl bg-clinical-critical/10 border border-clinical-critical/30 text-xs text-clinical-critical flex items-start space-x-2.5"
              data-testid="container-alert-banner"
            >
              <ShieldAlert className="w-4 h-4 text-clinical-critical shrink-0 mt-0.5" />
              <div>
                <strong className="block font-bold">Atenção Frasco / Equipo:</strong>
                <span>
                  {calculation.containerAlert ||
                    'OBRIGATÓRIO frasco de VIDRO ou POLIETILENO/POLIOLEFINA com equipo livre de PVC. PROIBIDO PVC comum (perda de até 80% da dose por adsorção plástica).'}
                </span>
              </div>
            </div>
          )}

          {/* Vasopressin Association Alert (Noradrenalina > 0.25 mcg/kg/min) */}
          {showVasopressinPrompt && (
            <div
              className="p-3.5 rounded-xl bg-clinical-warning/15 border-2 border-clinical-warning/30 text-xs text-slate-900 dark:text-white flex items-start space-x-2.5"
              data-testid="vasopressin-alert-prompt"
            >
              <Flame className="w-4 h-4 text-clinical-warning shrink-0 mt-0.5" />
              <div className="space-y-1">
                <strong className="block font-bold text-clinical-warning">
                  Alerta: Noradrenalina &gt; 0,25 mcg/kg/min (Vasoplegia Refratária)
                </strong>
                <p className="text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed">
                  Diretrizes da Surviving Sepsis Campaign recomendam a introdução precoce de <strong>Vasopressina em dose fixa contínua de 0,01 a 0,04 UI/min</strong> (dose padrão ouro: 0,03 UI/min = 9 mL/h na diluição de 20 UI/100 mL) como segundo vasopressor poupador de catecolamina.
                </p>
              </div>
            </div>
          )}

          {/* Nursing & Administration Precautions */}
          {protocol.nursingPrecautions && (
            <div className="p-3 rounded-xl bg-surface-raised-light dark:bg-surface-raised-dark text-slate-600 dark:text-slate-400 text-xs leading-relaxed space-y-1 border border-subtle-light/60 dark:border-subtle-dark/60">
              <span className="font-bold text-slate-700 dark:text-slate-300 block">
                Cuidados de Enfermagem & Administração:
              </span>
              <p className="text-[11px]">{protocol.nursingPrecautions}</p>
              {protocol.administrationRoute && (
                <p className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
                  Via de Acesso: {protocol.administrationRoute}
                </p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PrescriptionCard;
