import React, { useState, useEffect, useMemo, useCallback } from 'react';
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
 * Clean, uncluttered mobile-first hierarchy:
 * 1. Compact Sticky Header (Back, Title, Reset, Favorite, Copy PEP)
 * 2. Compact Score & Risk Summary Bar
 * 3. Mandatory SSC 2021 Warning (when applicable)
 * 4. Primary Bedside Parameter Inputs (First fold on mobile)
 * 5. Actionable Clinical Management & BIC Infusion Drawer
 * 6. Physiological Deviation Radar Chart (Bottom analytical section)
 * 7. Evidence Reference Footer
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

  useEffect(() => {
    if (typeof window !== 'undefined' && typeof window.scrollTo === 'function') {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    }
  }, [calculator.id]);

  useEffect(() => {
    setInputs(initialInputs);
  }, [initialInputs]);

  const result = useMemo(() => {
    return calculateScore(calculator, inputs);
  }, [calculator, inputs]);

  const handleInputChange = useCallback((groupId: string, value: any) => {
    setInputs((prev) => ({
      ...prev,
      [groupId]: value
    }));
  }, []);

  const handleReset = useCallback(() => {
    setInputs(initialInputs);
  }, [initialInputs]);

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

  const isQsofa =
    calculator.id === 'calc_qsofa' ||
    calculator.slug === 'qsofa' ||
    Boolean(calculator.ssc2021Warning);

  const activeTier = result.activeRiskTier;
  const pharmActions = activeTier.pharmacologicalActions?.length
    ? activeTier.pharmacologicalActions
    : calculator.pharmacologicalActions || [];

  const nonPharmActions = activeTier.nonPharmacologicalActions?.length
    ? activeTier.nonPharmacologicalActions
    : calculator.nonPharmacologicalActions || [];

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
      className={`min-h-full flex flex-col bg-canvas-light dark:bg-canvas-dark text-slate-900 dark:text-slate-100 pb-24 transition-colors duration-200 ${className}`}
      data-testid="calculator-view"
    >
      {/* 1. Compact Sticky Navigation Header */}
      <header className="sticky top-0 z-20 backdrop-blur-xl bg-surface-light/95 dark:bg-surface-dark/95 border-b border-subtle-light dark:border-subtle-dark px-3 py-2 transition-colors shadow-xs">
        <div className="max-w-md mx-auto flex items-center justify-between gap-2">
          <div className="flex items-center space-x-1.5 min-w-0 flex-1">
            <button
              type="button"
              onClick={onBack}
              className="w-9 h-9 rounded-xl flex items-center justify-center text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shrink-0"
              aria-label="Voltar para o catálogo"
              data-testid="calc-back-button"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="min-w-0 flex-1">
              <h1 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-white truncate">
                {calculator.acronym ? `${calculator.acronym} — ${calculator.name}` : calculator.name}
              </h1>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate">
                {calculator.summary}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-1 shrink-0">
            <button
              type="button"
              onClick={handleReset}
              className="w-9 h-9 rounded-xl flex items-center justify-center text-slate-500 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title="Redefinir parâmetros"
              aria-label="Redefinir parâmetros"
              data-testid="calc-reset-button"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            {onToggleFavorite && (
              <button
                type="button"
                onClick={() => onToggleFavorite(calculator.id)}
                className="w-9 h-9 rounded-xl flex items-center justify-center text-slate-400 hover:text-amber-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                aria-label={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                data-testid="calc-favorite-button"
              >
                <Star
                  className={`w-4 h-4 transition-colors ${
                    isFavorite ? 'text-amber-500 fill-amber-500' : 'text-slate-400'
                  }`}
                />
              </button>
            )}

            <button
              type="button"
              onClick={handleCopySummary}
              className={`h-9 px-2.5 rounded-xl flex items-center space-x-1 text-xs font-semibold transition-all ${
                copiedPep
                  ? 'bg-emerald-500 text-white'
                  : 'bg-brand-500/10 text-brand-600 dark:text-brand-400 hover:bg-brand-500/20'
              }`}
              title="Copiar resumo para PEP"
              aria-label="Copiar resumo para PEP"
              data-testid="calc-copy-pep"
            >
              {copiedPep ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedPep ? 'Copiado!' : 'PEP'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Scroll Area */}
      <main className="flex-1 max-w-md mx-auto w-full px-3.5 py-3 space-y-3.5">
        {/* 2. Compact Score & Risk Summary Bar */}
        <section
          className="p-3 rounded-xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-xs space-y-2"
          data-testid="score-summary-card"
          aria-live="polite"
        >
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-baseline space-x-1.5">
              <span
                className="text-2xl sm:text-3xl font-black tabular-nums tracking-tight text-slate-900 dark:text-white"
                data-testid="score-value-display"
              >
                {result.scoreFormatted}
              </span>
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 clinical-unit">
                {Math.abs(Number(result.scoreFormatted)) === 1 ? 'ponto' : 'pontos'}
              </span>
            </div>

            <span
              className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold"
              style={{
                backgroundColor: `${activeTier.colorHex}20`,
                color: activeTier.colorHex,
                border: `1px solid ${activeTier.colorHex}45`
              }}
              data-testid="risk-tier-badge"
            >
              {activeTier.label}
            </span>
          </div>

          {activeTier.statisticalOutcome && (
            <p className="text-xs text-slate-600 dark:text-slate-300 leading-snug pt-1.5 border-t border-subtle-light/60 dark:border-subtle-dark/60">
              <strong className="font-semibold text-slate-900 dark:text-white">Desfecho: </strong>
              {activeTier.statisticalOutcome}
            </p>
          )}
        </section>

        {/* 3. Mandatory Surviving Sepsis Campaign (SSC 2021) Warning Banner */}
        {isQsofa && (
          <div
            className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/40 text-slate-900 dark:text-white space-y-1"
            role="alert"
            data-testid="ssc-2021-warning-banner"
          >
            <div className="flex items-center space-x-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
              <h2 className="font-bold text-xs text-amber-600 dark:text-amber-400 uppercase tracking-wide">
                Aviso Mandatório SSC 2021 (Surviving Sepsis Campaign)
              </h2>
            </div>
            <p className="text-[11px] leading-relaxed text-slate-700 dark:text-slate-300">
              {result.sscWarning || SSC_2021_QSOFA_WARNING}
            </p>
          </div>
        )}

        {/* 4. Parameter Input Cards (Primary Bedside Interaction at Top) */}
        <section className="space-y-2" aria-label="Parâmetros Clínicos">
          <div className="flex items-center justify-between px-0.5">
            <h2 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Parâmetros do Escore ({calculator.parameterGroups.length})
            </h2>
          </div>

          <div className="space-y-2">
            {calculator.parameterGroups.map((group, idx) => (
              <ParameterGroupInput
                key={group.id}
                index={idx}
                group={group}
                value={inputs[group.id]}
                onChange={handleInputChange}
              />
            ))}
          </div>
        </section>

        {/* 5. Non-Pharmacological Management Plan */}
        {nonPharmActions.length > 0 && (
          <section
            className="p-3 rounded-xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-xs space-y-2.5"
            data-testid="non-pharm-actions-card"
          >
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-md bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                <HeartPulse className="w-3.5 h-3.5" />
              </div>
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white">
                Condutas Clínicas Recomendadas
              </h2>
            </div>

            <div className="space-y-2">
              {nonPharmActions.map((action, idx) => (
                <div
                  key={action.id || `action-${idx}`}
                  className="p-2.5 rounded-lg bg-surface-raised-light/80 dark:bg-surface-raised-dark/80 border border-subtle-light/60 dark:border-subtle-dark/60 text-xs space-y-1"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-slate-900 dark:text-white">
                      {action.recommendationTitle}
                    </span>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-brand-500/15 text-brand-600 dark:text-brand-400 shrink-0">
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

        {/* 6. Bedside BIC Prescription Drawer */}
        {(infusionAction || calculator.id === 'calc_qsofa' || calculator.id === 'calc_sofa') && (
          <section className="space-y-1.5">
            <h2 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 px-0.5">
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

        {/* 7. Native SVG 60fps Physiological Radar (Positioned at the bottom) */}
        {calculator.radarAxes && calculator.radarAxes.length >= 3 && (
          <section className="space-y-1.5 pt-1" aria-label="Gráfico de Desvio Fisiológico">
            <h2 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 px-0.5">
              Análise Gráfica de Desvio Fisiológico
            </h2>
            <PhysiologicalRadar
              axes={calculator.radarAxes}
              values={result.radarValues}
              data-testid="calculator-physiological-radar"
            />
          </section>
        )}

        {/* 8. Evidence Source Footer */}
        {calculator.evidenceSource && (
          <footer className="p-2.5 rounded-xl bg-surface-raised-light/50 dark:bg-surface-raised-dark/50 border border-subtle-light/40 dark:border-subtle-dark/40 text-[11px] text-slate-400 leading-relaxed">
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
