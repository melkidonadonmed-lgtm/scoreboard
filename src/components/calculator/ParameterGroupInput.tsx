import React from 'react';
import type { ParameterGroup, ParameterOption } from '@/types/clinical';
import { Minus, Plus, HelpCircle, Eye, EyeOff } from 'lucide-react';

export interface ParameterGroupInputProps {
  group: ParameterGroup;
  value: any;
  onChange: (groupId: string, value: any) => void;
  index?: number;
  className?: string;
}

/**
 * Compact touch-target parameter group input optimized for mobile bedside entry.
 * Supports:
 * - single_choice (compact radio rows)
 * - boolean (Sim / Não segmented toggle)
 * - numeric_input (direct input with step buttons)
 * - pupil_reactivity (visual pupil reactivity selector)
 */
export const ParameterGroupInput: React.FC<ParameterGroupInputProps> = ({
  group,
  value,
  onChange,
  index,
  className = ''
}) => {
  const { id, name, inputType, unit, helpText, options = [], minValue, maxValue } = group;

  const renderPointBadge = (points: number) => {
    const isZero = points === 0;
    const isPositive = points > 0;
    const label = isPositive ? `+${points}` : `${points}`;
    const unitText = Math.abs(points) === 1 ? 'pt' : 'pts';
    return (
      <span
        className={`px-1.5 py-0.5 rounded-md text-[10px] font-bold tabular-nums clinical-unit shrink-0 ${
          isZero
            ? 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400'
            : isPositive
              ? 'bg-brand-500/15 text-brand-600 dark:text-brand-400'
              : 'bg-clinical-warning/15 text-clinical-warning'
        }`}
      >
        {`${label} ${unitText}`}
      </span>
    );
  };

  // 1. Single Choice Input Type
  const renderSingleChoice = () => {
    return (
      <div className="grid grid-cols-1 gap-1.5" role="radiogroup" aria-label={name}>
        {options.map((option: ParameterOption) => {
          const isSelected = value === option.id || value === option.pointValue;

          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => onChange(id, option.id)}
              className={`w-full min-h-touch px-2.5 py-2 rounded-lg flex items-center justify-between text-left transition-spring select-none ${
                isSelected
                  ? 'bg-brand-50/90 dark:bg-brand-950/45 border border-brand-500 text-slate-900 dark:text-white shadow-xs ring-1 ring-brand-500/20'
                  : 'bg-surface-raised-light/80 dark:bg-surface-raised-dark/80 border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 active:scale-[0.99]'
              }`}
            >
              <div className="flex items-center space-x-2.5 pr-2 min-w-0 flex-1">
                <div
                  className={`w-4 h-4 rounded-full border-2 flex items-center justify-center shrink-0 transition-colors ${
                    isSelected
                      ? 'border-brand-500 bg-brand-500 text-white'
                      : 'border-slate-300 dark:border-slate-600'
                  }`}
                >
                  {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-white" />}
                </div>
                <div className="min-w-0 flex-1">
                  <span className="text-xs font-medium leading-snug block break-words">
                    {option.label}
                  </span>
                  {option.description && (
                    <span className="text-[11px] text-slate-500 dark:text-slate-400 leading-tight block break-words mt-0.5">
                      {option.description}
                    </span>
                  )}
                </div>
              </div>

              {renderPointBadge(option.pointValue)}
            </button>
          );
        })}
      </div>
    );
  };

  // 2. Boolean Input Type
  const renderBoolean = () => {
    const trueOption = options.find((o) => o.pointValue > 0) || options[0];
    const falseOption = options.find((o) => o.pointValue === 0) || options[1];

    const isTrue =
      value === true ||
      value === 1 ||
      (trueOption && value === trueOption.id) ||
      (trueOption && value === trueOption.pointValue);

    const isFalse =
      value === false ||
      value === 0 ||
      (falseOption && value === falseOption.id) ||
      (falseOption && value === falseOption.pointValue);

    return (
      <div className="grid grid-cols-2 gap-2">
        <button
          type="button"
          aria-pressed={isFalse}
          onClick={() => onChange(id, falseOption ? falseOption.id : false)}
          className={`min-h-touch px-3 py-2 rounded-lg flex items-center justify-center space-x-2 font-medium text-xs transition-spring select-none ${
            isFalse
              ? 'bg-slate-200 dark:bg-slate-700 border border-slate-400 dark:border-slate-500 text-slate-900 dark:text-white font-semibold'
              : 'bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <span>Não</span>
          {falseOption && renderPointBadge(falseOption.pointValue)}
        </button>

        <button
          type="button"
          aria-pressed={isTrue}
          onClick={() => onChange(id, trueOption ? trueOption.id : true)}
          className={`min-h-touch px-3 py-2 rounded-lg flex items-center justify-center space-x-2 font-medium text-xs transition-spring select-none ${
            isTrue
              ? 'bg-brand-500 text-white font-semibold shadow-xs ring-2 ring-brand-500/25'
              : 'bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <span>Sim</span>
          {trueOption && renderPointBadge(trueOption.pointValue)}
        </button>
      </div>
    );
  };

  // 3. Numeric Input Type with Step Buttons
  const renderNumericInput = () => {
    const numericValue = typeof value === 'number' ? value : group.normalBaselineValue || 0;
    const min = minValue !== undefined ? minValue : 0;
    const max = maxValue !== undefined ? maxValue : 999;
    const step = 1;

    const handleStep = (delta: number) => {
      const next = Math.min(max, Math.max(min, numericValue + delta));
      onChange(id, next);
    };

    const handleDirectChange = (rawVal: string) => {
      const parsed = parseFloat(rawVal);
      if (!isNaN(parsed)) {
        onChange(id, Math.min(max, Math.max(min, parsed)));
      } else if (rawVal === '') {
        onChange(id, min);
      }
    };

    return (
      <div className="flex items-center space-x-2">
        <button
          type="button"
          onClick={() => handleStep(-step)}
          disabled={numericValue <= min}
          className="w-11 h-11 rounded-lg flex items-center justify-center bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-200 disabled:opacity-40 disabled:pointer-events-none active:scale-95 transition-all min-h-touch min-w-touch"
          aria-label={`Diminuir ${name}`}
        >
          <Minus className="w-4 h-4" />
        </button>

        <div className="flex-1 min-h-touch px-3 py-1.5 rounded-lg bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark flex items-center justify-center space-x-1.5 focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-500/20">
          <input
            type="number"
            value={numericValue}
            onChange={(e) => handleDirectChange(e.target.value)}
            min={min}
            max={max}
            step={step}
            className="w-20 text-center font-bold text-sm sm:text-base tabular-nums bg-transparent text-slate-900 dark:text-white outline-none"
            aria-label={`${name} ${unit || ''}`}
          />
          {unit && (
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 clinical-unit">
              {unit}
            </span>
          )}
        </div>

        <button
          type="button"
          onClick={() => handleStep(step)}
          disabled={numericValue >= max}
          className="w-11 h-11 rounded-lg flex items-center justify-center bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-200 disabled:opacity-40 disabled:pointer-events-none active:scale-95 transition-all min-h-touch min-w-touch"
          aria-label={`Aumentar ${name}`}
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>
    );
  };

  // 4. Pupil Reactivity Input Type (Glasgow-P)
  const renderPupilReactivity = () => {
    return (
      <div className="grid grid-cols-1 gap-1.5" role="radiogroup" aria-label={name}>
        {options.map((option: ParameterOption) => {
          const isSelected = value === option.id || value === option.pointValue;
          const isNormal = option.pointValue === 0;

          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => onChange(id, option.id)}
              className={`w-full min-h-touch px-2.5 py-2 rounded-lg flex items-center justify-between text-left transition-spring select-none ${
                isSelected
                  ? 'bg-brand-50/90 dark:bg-brand-950/45 border border-brand-500 text-slate-900 dark:text-white shadow-xs ring-1 ring-brand-500/20'
                  : 'bg-surface-raised-light/80 dark:bg-surface-raised-dark/80 border border-subtle-light dark:border-subtle-dark text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 active:scale-[0.99]'
              }`}
            >
              <div className="flex items-center space-x-2.5 pr-2 min-w-0 flex-1">
                <div className="w-7 h-7 rounded-md bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark flex items-center justify-center shrink-0">
                  {isNormal ? (
                    <Eye className="w-3.5 h-3.5 text-emerald-500" />
                  ) : (
                    <EyeOff className="w-3.5 h-3.5 text-clinical-critical" />
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <span className="text-xs font-medium leading-snug block break-words">
                    {option.label}
                  </span>
                  {option.description && (
                    <span className="text-[11px] text-slate-500 dark:text-slate-400 block break-words mt-0.5">
                      {option.description}
                    </span>
                  )}
                </div>
              </div>

              {renderPointBadge(option.pointValue)}
            </button>
          );
        })}
      </div>
    );
  };

  return (
    <div
      className={`p-3 rounded-xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-xs space-y-2 transition-colors duration-200 ${className}`}
      data-testid={`parameter-group-${id}`}
    >
      {/* Compact Parameter Header */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center space-x-1.5 min-w-0">
          {index !== undefined && (
            <span className="w-5 h-5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 text-[10px] font-bold tabular-nums flex items-center justify-center shrink-0">
              {index + 1}
            </span>
          )}
          <label className="text-xs font-bold text-slate-900 dark:text-white tracking-tight truncate">
            {name}
          </label>
          {unit && (
            <span className="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 clinical-unit">
              {unit}
            </span>
          )}
        </div>

        {helpText && (
          <div className="group relative cursor-pointer shrink-0" title={helpText}>
            <HelpCircle className="w-3.5 h-3.5 text-slate-400 hover:text-brand-500 transition-colors" />
          </div>
        )}
      </div>

      {helpText && (
        <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
          {helpText}
        </p>
      )}

      {/* Input Selector */}
      {inputType === 'single_choice' && renderSingleChoice()}
      {inputType === 'boolean' && renderBoolean()}
      {inputType === 'numeric_input' && renderNumericInput()}
      {inputType === 'pupil_reactivity' && renderPupilReactivity()}
    </div>
  );
};

export default ParameterGroupInput;
