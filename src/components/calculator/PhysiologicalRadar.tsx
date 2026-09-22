import React, { useMemo } from 'react';
import type { RadarAxis } from '@/types/clinical';
import {
  generateBaselinePolygon,
  generatePatientPolygon,
  generateGridRings,
  generateAxisSpokes,
  getAxisLabelPositions,
  normalizeRadarValues,
  polarToCartesian,
  calculateAxisAngle
} from '@/engines/radarEngine';

export interface PhysiologicalRadarProps {
  axes: RadarAxis[];
  values?: Record<string, number>;
  size?: number;
  center?: { x: number; y: number };
  maxRadius?: number;
  baselineRatio?: number;
  showLegend?: boolean;
  showValues?: boolean;
  className?: string;
  title?: string;
}

/**
 * Pure native reactive SVG Physiological Radar rendering at 60fps.
 * No external charting libraries used.
 *
 * Displays:
 * - Concentric background grid rings (0.25, 0.50, 0.75, 1.00)
 * - Radial spoke lines connecting center to axes
 * - Homeostatic green baseline polygon (r = 0.25)
 * - Dynamic patient deviation overlay polygon (r = 0.25 to 1.0)
 * - Colored vertex dots and dynamic text labels
 */
export const PhysiologicalRadar: React.FC<PhysiologicalRadarProps> = ({
  axes,
  values = {},
  size = 300,
  center = { x: 150, y: 150 },
  maxRadius = 88,
  baselineRatio = 0.25,
  showLegend = true,
  showValues = true,
  className = '',
  title = 'Radar de Desvio Fisiológico'
}) => {
  const numAxes = axes.length;

  // Normalized patient deviations between 0 (homeostasis) and 1 (critical derangement)
  const normalizedValues = useMemo(() => {
    return normalizeRadarValues(axes, values);
  }, [axes, values]);

  // Determine peak deviation to set dynamic styling
  const maxDeviation = useMemo(() => {
    const vals = Object.values(normalizedValues);
    return vals.length > 0 ? Math.max(...vals) : 0;
  }, [normalizedValues]);

  // Geometry computation
  const gridRings = useMemo(() => {
    if (numAxes < 3) return [];
    return generateGridRings(numAxes, center, maxRadius, [0.25, 0.5, 0.75, 1.0]);
  }, [numAxes, center, maxRadius]);

  const spokes = useMemo(() => {
    if (numAxes < 3) return [];
    return generateAxisSpokes(numAxes, center, maxRadius);
  }, [numAxes, center, maxRadius]);

  const baselinePoints = useMemo(() => {
    if (numAxes < 3) return '';
    return generateBaselinePolygon(numAxes, center, maxRadius, baselineRatio);
  }, [numAxes, center, maxRadius, baselineRatio]);

  const patientPoints = useMemo(() => {
    if (numAxes < 3) return '';
    return generatePatientPolygon(axes, normalizedValues, center, maxRadius, baselineRatio);
  }, [axes, normalizedValues, center, maxRadius, baselineRatio]);

  const labelPositions = useMemo(() => {
    if (numAxes < 3) return [];
    return getAxisLabelPositions(axes, center, maxRadius, 22);
  }, [axes, center, maxRadius]);

  // Vertex points for the patient deviation polygon
  const patientVertices = useMemo(() => {
    if (numAxes < 3) return [];
    return axes.map((axis, i) => {
      const normVal = Math.min(1.0, Math.max(0.0, normalizedValues[axis.id] ?? 0));
      const r = baselineRatio + (1.0 - baselineRatio) * normVal;
      const angle = calculateAxisAngle(i, numAxes);
      const pt = polarToCartesian(center, r * maxRadius, angle);
      return {
        ...pt,
        axisId: axis.id,
        label: axis.label,
        normVal
      };
    });
  }, [axes, normalizedValues, center, maxRadius, baselineRatio, numAxes]);

  // Dynamic color theme based on deviation severity
  const deviationTheme = useMemo(() => {
    if (maxDeviation >= 0.75) {
      return {
        polygonFill: 'rgba(239, 68, 68, 0.35)',
        polygonStroke: '#ef4444',
        dotFill: '#ef4444',
        badgeBg: 'bg-clinical-critical/15 text-clinical-critical',
        label: 'Desvio Crítico'
      };
    }
    if (maxDeviation >= 0.35) {
      return {
        polygonFill: 'rgba(245, 158, 11, 0.30)',
        polygonStroke: '#f59e0b',
        dotFill: '#f59e0b',
        badgeBg: 'bg-clinical-warning/15 text-clinical-warning',
        label: 'Desvio Moderado'
      };
    }
    if (maxDeviation > 0.05) {
      return {
        polygonFill: 'rgba(59, 130, 246, 0.25)',
        polygonStroke: '#3b82f6',
        dotFill: '#3b82f6',
        badgeBg: 'bg-brand-500/15 text-brand-600 dark:text-brand-400',
        label: 'Desvio Leve'
      };
    }
    return {
      polygonFill: 'rgba(16, 185, 129, 0.20)',
      polygonStroke: '#10b981',
      dotFill: '#10b981',
      badgeBg: 'bg-clinical-stable/15 text-clinical-stable',
      label: 'Homeostase'
    };
  }, [maxDeviation]);

  if (numAxes < 3) {
    return (
      <div className={`p-4 rounded-2xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark text-center text-xs text-slate-500 ${className}`}>
        Radar fisiológico requer no mínimo 3 eixos monitorizados ({numAxes} disponíveis).
      </div>
    );
  }

  return (
    <div
      className={`relative flex flex-col items-center justify-center p-3 rounded-2xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-card transition-colors duration-200 ${className}`}
      data-testid="physiological-radar-card"
    >
      {/* Header with Title and Severity Badge */}
      <div className="w-full flex items-center justify-between mb-1 px-1">
        <span className="text-xs font-semibold tracking-tight text-slate-700 dark:text-slate-300">
          {title}
        </span>
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${deviationTheme.badgeBg}`}>
          {deviationTheme.label}
        </span>
      </div>

      {/* SVG Radar Surface */}
      <div className="relative w-full max-w-[280px] sm:max-w-[320px] aspect-square flex items-center justify-center">
        <svg
          viewBox={`0 0 ${size} ${size}`}
          className="w-full h-full select-none overflow-visible transition-all duration-300"
          aria-label="Gráfico de Radar Fisiológico"
          role="img"
          data-testid="physiological-radar-svg"
        >
          <defs>
            {/* Subtle glow filter for the dynamic deviation polygon */}
            <filter id="radarGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* 1. Background Grid Rings */}
          <g className="radar-grid" data-testid="radar-grid-rings">
            {gridRings.map((ring, idx) => (
              <polygon
                key={`grid-ring-${idx}`}
                points={ring.points}
                fill="none"
                stroke="currentColor"
                strokeWidth={ring.level === 1.0 ? '1.2' : '0.8'}
                strokeDasharray={ring.level === 1.0 ? undefined : '2 3'}
                className="text-slate-200 dark:text-slate-800"
                opacity={0.8}
              />
            ))}
          </g>

          {/* 2. Radial Spokes */}
          <g className="radar-spokes" data-testid="radar-spokes">
            {spokes.map((spoke, idx) => (
              <line
                key={`spoke-${idx}`}
                x1={spoke.x1}
                y1={spoke.y1}
                x2={spoke.x2}
                y2={spoke.y2}
                stroke="currentColor"
                strokeWidth="0.8"
                strokeDasharray="2 2"
                className="text-slate-200 dark:text-slate-800"
                opacity={0.9}
              />
            ))}
          </g>

          {/* 3. Green Baseline Polygon (Homeostasis, r = 0.25) */}
          <polygon
            points={baselinePoints}
            fill="rgba(16, 185, 129, 0.12)"
            stroke="#10b981"
            strokeWidth="1.5"
            strokeDasharray="3 3"
            data-testid="radar-baseline-polygon"
            className="transition-all duration-300"
          />

          {/* 4. Dynamic Patient Deviation Overlay Polygon */}
          <polygon
            points={patientPoints}
            fill={deviationTheme.polygonFill}
            stroke={deviationTheme.polygonStroke}
            strokeWidth="2"
            filter="url(#radarGlow)"
            data-testid="radar-patient-polygon"
            className="transition-all duration-300 ease-out"
          />

          {/* 5. Patient Deviation Vertices (Dots) */}
          <g className="radar-dots" data-testid="radar-vertices">
            {patientVertices.map((vertex) => (
              <circle
                key={`dot-${vertex.axisId}`}
                cx={vertex.x}
                cy={vertex.y}
                r={vertex.normVal > 0 ? 3.5 : 2.5}
                fill={vertex.normVal > 0 ? deviationTheme.dotFill : '#10b981'}
                stroke="#ffffff"
                strokeWidth="1"
                className="transition-all duration-300 ease-out"
              />
            ))}
          </g>

          {/* 6. Spoke Labels */}
          <g className="radar-labels" data-testid="radar-labels">
            {labelPositions.map((pos) => {
              const normVal = normalizedValues[pos.id] ?? 0;
              const isDeranged = normVal > 0.05;

              return (
                <text
                  key={`label-${pos.id}`}
                  x={pos.x}
                  y={pos.y}
                  textAnchor={pos.textAnchor}
                  dominantBaseline={
                    pos.dominantBaseline === 'baseline'
                      ? 'alphabetic'
                      : (pos.dominantBaseline as React.SVGAttributes<SVGTextElement>['dominantBaseline'])
                  }
                  fontSize="9.5"
                  fontWeight={isDeranged ? '600' : '500'}
                  className={`select-none transition-colors duration-200 ${
                    isDeranged
                      ? 'fill-slate-900 dark:fill-white'
                      : 'fill-slate-500 dark:fill-slate-400'
                  }`}
                >
                  {pos.system || pos.label}
                  {showValues && isDeranged ? ` (${Math.round(normVal * 100)}%)` : ''}
                </text>
              );
            })}
          </g>
        </svg>
      </div>

      {/* 7. Bottom Legend */}
      {showLegend && (
        <div className="w-full flex items-center justify-center space-x-4 pt-2 border-t border-subtle-light/60 dark:border-subtle-dark/60 text-[11px] text-slate-500 dark:text-slate-400">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80 border border-emerald-600 inline-block" />
            <span>Homeostase (0%)</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span
              className="w-2.5 h-2.5 rounded-full inline-block border"
              style={{
                backgroundColor: deviationTheme.polygonStroke,
                borderColor: deviationTheme.polygonStroke
              }}
            />
            <span>Desvio do Paciente</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default PhysiologicalRadar;
