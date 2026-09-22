import React, { useState, useMemo, useCallback } from 'react';
import type { Calculator } from '@/types/clinical';
import { calculateScore, SSC_2021_QSOFA_WARNING } from '@/engines/calculationEngine';
import { generatePepNote } from '@/engines/pepExportEngine';
import { PhysiologicalRadar } from './PhysiologicalRadar';
import { ParameterGroupInput } from './ParameterGroupInput';
import { PrescriptionCard } from './PrescriptionCard';
import {
  ArrowLeft,
  Star,
  RotateCcw,
  AlertTriangle,
  Copy,
  Check,
  HeartPulse
} from 'lucide-react';

export interface CalculatorViewProps {
  calculator: Calculator;
  onBack: () => void;
  patientWeightKg?: number;
  onWeightChange?: (weight: number) => void;
  bedLabel?: string;
  isFavorite?: boolean;
  onToggleFavorite?: (calculatorId: string) => void;
  className?: string;
}

/**
 * Interactive Clinical Calculator View.
 * Mobile-first architecture with:
 * - Top navigation bar with Back, Title, Favorite, and Reset buttons
 * - Score summary hero card with large score numbers, risk tier badge, and outcome interpretation
 * - 60fps Native SVG Physiological Radar
 * - Mandatory Surviving Sepsis Campaign 2021 (SSC 2021) warning banner for qSOFA
 * - 48px Touch inputs in the One-Thumb zone
 * - Bedside BIC prescription micro-calculator drawer
 * - Structured non-pharmacological clinical management recommendations
 */
export const CalculatorView: React.FC<CalculatorViewProps> = ({
  calculator,
  onBack,
  patientWeightKg = 70,
  onWeightChange,
  bedLabel = 'Leito 04 - UTI',
  isFavorite = false,
  onToggleFavorite,
  className = ''
}) => {
  // Initialize parameter inputs
  const initialInputs = useMemo(() => {
    const defaults: Record<string, any> = {};
    for (const group of calculator.parameterGroups) {
      if (group.inputType === 'single_choice' || group.inputType === 'pupil_reactivity') {
        const normalOpt = group.options.find((o) => o.isNormalBaseline || o.pointValue === 0) || group.options[0];
        if (normalOpt) defaults[group.id] = normalOpt.id;
      } else if (group.inputType === 'boolean') {
        defaults[group.id] = false;
      } else if (group.inputType === 'numeric_input') {
        defaults[group.id] = group.normalBaselineValue ?? 0;
      }
    }
    return defaults;
  }, [calculator]);

  const [inputs, setInputs] = useState<Record<string, any>>(initialInputs);
  const [copiedPep, setCopiedPep] = useState(false);

  // Compute clinical score, active risk tier, and radar values
  const result = useMemo(() => {
    return calculateScore(calculator, inputs);
  }, [calculator, inputs]);

  // Handle single parameter change
  const handleInputChange = useCallback((groupId: string, value: any) => {
    setInputs((prev) => ({
      ...prev,
      [groupId]: value
    }));
  }, []);

  // Reset all parameters to baseline
  const handleReset = useCallback(() => {
    setInputs(initialInputs);
  }, [initialInputs]);

  // Copy clinical note to clipboard (PEP format)
  const handleCopySummary = useCallback(async () => {
    const text = generatePepNote({
      calculator,
      result,
      patientBed: bedLabel,
      patientWeightKg
    });

    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      }
      setCopiedPep(true);
      setTimeout(() => setCopiedPep(false), 2000);
    } catch {
      setCopiedPep(true);
      setTimeout(() => setCopiedPep(false), 2000);
    }
  }, [calculator, result, bedLabel, patientWeightKg]);

  // Check whether calculator or result warrants SSC 2021 warning
  const isQsofa =
    calculator.id === 'calc_qsofa' ||
    calculator.slug === 'qsofa' ||
    Boolean(calculator.ssc2021Warning);

  // Find relevant pharmacological actions from risk tier or calculator
  const activeTier = result.activeRiskTier;
  const pharmActions = activeTier.pharmacologicalActions?.length
    ? activeTier.pharmacologicalActions
    : calculator.pharmacologicalActions || [];

  const nonPharmActions = activeTier.nonPharmacologicalActions?.length
    ? activeTier.nonPharmacologicalActions
    : calculator.nonPharmacologicalActions || [];

  // Vasoactive infusion action (e.g. Norepinephrine, Vasopressin)
  const infusionAction = pharmActions.find(
    (a) =>
      Boolean(a.infusionProtocol) ||
      a.drugName.toLowerCase().includes('nor') ||
      a.drugName.toLowerCase().includes('vaso') ||
      a.drugName.toLowerCase().includes('dobut') ||
      a.drugName.toLowerCase().includes('nitrog')
  );

  return (
    <div
      className={`min-h-full flex flex-col bg-canvas-light dark:bg-canvas-dark text-slate-900 dark:text-slate-100 pb-28 transition-colors duration-200 ${className}`}
      data-testid="calculator-view"
    >
      {/* 1. Sticky Navigation Header */}
      <header className="sticky top-0 z-20 backdrop-blur-md bg-surface-light/90 dark:bg-surface-dark/90 border-b border-subtle-light dark:border-subtle-dark px-3 py-2.5 transition-colors">
        <div className="max-w-md mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-1.5">
            <button
              type="button"
              onClick={onBack}
              className="w-10 h-10 rounded-xl flex items-center justify-center text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors min-h-touch min-w-touch"
              aria-label="Voltar para o catálogo"
              data-testid="calc-back-button"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="truncate max-w-[190px] sm:max-w-[220px]">
              <h1 className="text-sm font-bold text-slate-900 dark:text-white truncate">
                {calculator.name}
              </h1>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate">
                {calculator.acronym ? `${calculator.acronym} • ` : ''}{calculator.subcategory || calculator.categoryName || 'Calculadora Clínica'}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-1">
            {/* Reset Button */}
            <button
              type="button"
              onClick={handleReset}
              className="w-10 h-10 rounded-xl flex items-center justify-center text-slate-500 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors min-h-touch min-w-touch"
              title="Redefinir parâmetros"
              aria-label="Redefinir parâmetros"
              data-testid="calc-reset-button"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            {/* Favorite Star Button */}
            {onToggleFavorite && (
              <button
                type="button"
                onClick={() => onToggleFavorite(calculator.id)}
                className="w-10 h-10 rounded-xl flex items-center justify-center text-slate-400 hover:text-amber-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors min-h-touch min-w-touch"
                title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                aria-label={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                data-testid="calc-favorite-button"
              >
                <Star
                  className={`w-5 h-5 transition-colors ${
                    isFavorite ? 'text-amber-500 fill-amber-500' : 'text-slate-400'
                  }`}
                />
              </button>
            )}

            {/* Quick PEP Copy */}
            <button
              type="button"
              onClick={handleCopySummary}
              className={`min-h-touch px-2.5 py-1.5 rounded-xl flex items-center space-x-1 text-xs font-semibold transition-all ${
                copiedPep
                  ? 'bg-emerald-500 text-white'
                  : 'bg-brand-500/10 text-brand-600 dark:text-brand-400 hover:bg-brand-500/20'
              }`}
              title="Copiar resumo para PEP"
              aria-label="Copiar resumo para PEP"
              data-testid="calc-copy-pep"
            >
              {copiedPep ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span className="hidden sm:inline">{copiedPep ? 'Copiado!' : 'PEP'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Scroll Area */}
      <main className="flex-1 max-w-md mx-auto w-full px-4 py-4 space-y-4">
        {/* 2. Score Summary Hero Card */}
        <section
          className="p-4 rounded-2xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-card space-y-3"
          data-testid="score-summary-card"
        >
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Resultado do Escore
              </span>
              <div className="flex items-baseline space-x-2 mt-0.5">
                <span
                  className="text-4xl font-black tabular-nums tracking-tight text-slate-900 dark:text-white"
                  data-testid="score-value-display"
                >
                  {result.scoreFormatted}
                </span>
                <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">
                  {Math.abs(Number(result.scoreFormatted)) === 1 ? 'ponto' : 'pontos'}
                </span>
              </div>
            </div>

            {/* Risk Tier Severity Badge */}
            <div className="text-right">
              <span
                className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold shadow-sm"
                style={{
                  backgroundColor: `${activeTier.colorHex}22`,
                  color: activeTier.colorHex,
                  border: `1px solid ${activeTier.colorHex}44`
                }}
                data-testid="risk-tier-badge"
              >
                {activeTier.label}
              </span>
              <span className="block text-[10px] text-slate-400 uppercase tracking-wider mt-1">
                Severidade: {activeTier.severityLevel}
              </span>
            </div>
          </div>

          {/* Statistical Outcome / Prognosis */}
          {activeTier.statisticalOutcome && (
            <div className="p-2.5 rounded-xl bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light/60 dark:border-subtle-dark/60 text-xs text-slate-700 dark:text-slate-300">
              <strong className="font-semibold block text-slate-900 dark:text-white">
                Desfecho Clínico Estimado:
              </strong>
              <span>{activeTier.statisticalOutcome}</span>
            </div>
          )}
        </section>

        {/* 3. Mandatory Surviving Sepsis Campaign (SSC 2021) Warning Banner */}
        {isQsofa && (
          <div
            className="p-4 rounded-2xl bg-amber-500/10 border-2 border-amber-500/40 text-slate-900 dark:text-white space-y-2 shadow-sm"
            role="alert"
            data-testid="ssc-2021-warning-banner"
          >
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
              <h2 className="font-bold text-xs sm:text-sm text-amber-600 dark:text-amber-400 uppercase tracking-wide">
                Aviso Mandatório SSC 2021 (Surviving Sepsis Campaign)
              </h2>
            </div>
            <p className="text-xs leading-relaxed text-slate-700 dark:text-slate-300">
              {result.sscWarning || SSC_2021_QSOFA_WARNING}
            </p>
          </div>
        )}

        {/* 4. Native SVG 60fps Physiological Radar */}
        {calculator.radarAxes && calculator.radarAxes.length >= 3 && (
          <PhysiologicalRadar
            axes={calculator.radarAxes}
            values={result.radarValues}
            data-testid="calculator-physiological-radar"
          />
        )}

        {/* 5. Parameter Input Cards in One-Thumb Zone */}
        <section className="space-y-3" aria-label="Parâmetros Clínicos">
          <div className="flex items-center justify-between px-1">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Parâmetros Avaliados ({calculator.parameterGroups.length})
            </h2>
            <span className="text-[11px] text-slate-400">Zona de Polegar (48px)</span>
          </div>

          <div className="space-y-3">
            {calculator.parameterGroups.map((group) => (
              <ParameterGroupInput
                key={group.id}
                group={group}
                value={inputs[group.id]}
                onChange={handleInputChange}
              />
            ))}
          </div>
        </section>

        {/* 6. Bedside BIC Prescription Drawer */}
        {(infusionAction || calculator.id === 'calc_qsofa' || calculator.id === 'calc_sofa') && (
          <section className="space-y-2 pt-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 px-1">
              Drogas Vasoativas em BIC
            </h2>
            <PrescriptionCard
              pharmacologicalAction={infusionAction}
              calculator={calculator}
              calculationResult={result}
              patientWeightKg={patientWeightKg}
              onWeightChange={onWeightChange}
              bedLabel={bedLabel}
              defaultExpanded={false}
            />
          </section>
        )}

        {/* 7. Non-Pharmacological Management Plan */}
        {nonPharmActions.length > 0 && (
          <section
            className="p-4 rounded-2xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-card space-y-3"
            data-testid="non-pharm-actions-card"
          >
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                <HeartPulse className="w-4 h-4" />
              </div>
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white">
                Condutas Clínicas Recomendadas
              </h2>
            </div>

            <div className="space-y-2.5">
              {nonPharmActions.map((action, idx) => (
                <div
                  key={action.id || `action-${idx}`}
                  className="p-3 rounded-xl bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light/60 dark:border-subtle-dark/60 text-xs space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900 dark:text-white">
                      {action.recommendationTitle}
                    </span>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-brand-500/15 text-brand-600 dark:text-brand-400">
                      {action.dispositionTarget}
                    </span>
                  </div>

                  <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
                    {action.monitoringPlan}
                  </p>

                  {action.ventilatorySupport && (
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">
                      <strong>Suporte Ventilatório:</strong> {action.ventilatorySupport}
                    </div>
                  )}

                  {action.vascularAccess && (
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">
                      <strong>Acesso Vascular:</strong> {action.vascularAccess}
                    </div>
                  )}

                  {action.laboratoryPanel && (
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">
                      <strong>Painel Laboratorial:</strong> {action.laboratoryPanel}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 8. Evidence Source Footer */}
        {calculator.evidenceSource && (
          <footer className="p-3 rounded-xl bg-surface-raised-light/50 dark:bg-surface-raised-dark/50 border border-subtle-light/40 dark:border-subtle-dark/40 text-[11px] text-slate-400 leading-relaxed">
            <strong className="block font-semibold text-slate-500 dark:text-slate-400 mb-0.5">
              Evidência & Referência:
            </strong>
            {calculator.evidenceSource}
          </footer>
        )}
      </main>
    </div>
  );
};

export default CalculatorView;
