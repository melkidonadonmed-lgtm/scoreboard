import { type RadarAxis } from '../types/clinical';

export interface Point2D {
  x: number;
  y: number;
}

export interface RadarGeometryConfig {
  center: Point2D;
  maxRadius: number;
  baselineRatio?: number; // default: 0.25
}

export interface AxisSpoke {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  angle: number;
}

export interface AxisLabelPosition {
  id: string;
  label: string;
  system: string;
  x: number;
  y: number;
  textAnchor: 'start' | 'middle' | 'end';
  dominantBaseline: 'hanging' | 'middle' | 'baseline' | 'central';
}

export interface GridRing {
  level: number;
  points: string;
}

// ============================================================================
// 1. MULTI-AXIS NORMALIZATION
// ============================================================================

/**
 * Clamps and normalizes a single axis raw value between 0.0 (baseline) and 1.0 (max derangement).
 */
export function normalizeAxisValue(
  raw: number,
  baseline = 0,
  max = 1
): number {
  if (isNaN(raw)) return 0;
  if (max === baseline) return 0;

  const fraction = (raw - baseline) / (max - baseline);
  return Math.min(1.0, Math.max(0.0, fraction));
}

/**
 * Normalizes all axes of a score given raw values dictionary.
 */
export function normalizeRadarValues(
  axes: RadarAxis[],
  rawValues: Record<string, number>
): Record<string, number> {
  const result: Record<string, number> = {};

  for (const axis of axes) {
    const raw = rawValues[axis.id] ?? rawValues[axis.system] ?? axis.baselineValue;
    result[axis.id] = normalizeAxisValue(raw, axis.baselineValue, axis.maxAxisValue);
  }

  return result;
}

// ============================================================================
// 2. POLAR TO CARTESIAN TRIGONOMETRY
// ============================================================================

/**
 * Converts polar coordinates (radius, angle in radians) into 2D Cartesian coordinates (x, y).
 * Formula:
 *   x = center.x + radius * cos(angle)
 *   y = center.y + radius * sin(angle)
 */
export function polarToCartesian(
  center: Point2D,
  radius: number,
  angleRad: number
): Point2D {
  return {
    x: Math.round((center.x + radius * Math.cos(angleRad)) * 100) / 100,
    y: Math.round((center.y + radius * Math.sin(angleRad)) * 100) / 100
  };
}

/**
 * Calculates the angle in radians for axis i in a uniform N-axis circle,
 * starting at 12 o'clock (top: -Math.PI / 2).
 */
export function calculateAxisAngle(
  axisIndex: number,
  totalAxes: number,
  startAngleRad = -Math.PI / 2
): number {
  if (totalAxes <= 0) return startAngleRad;
  return (2 * Math.PI * axisIndex) / totalAxes + startAngleRad;
}

// ============================================================================
// 3. SVG POLYGON GENERATION
// ============================================================================

/**
 * Generates an SVG points string ("x1,y1 x2,y2 ...") from an array of radii (normalized 0 to 1).
 */
export function calculatePolygonPoints(
  radii: number[],
  center: Point2D,
  maxRadius: number,
  startAngleRad = -Math.PI / 2
): string {
  const total = radii.length;
  if (total === 0) return '';

  return radii
    .map((r, i) => {
      const angle = calculateAxisAngle(i, total, startAngleRad);
      const pt = polarToCartesian(center, r * maxRadius, angle);
      return `${pt.x},${pt.y}`;
    })
    .join(' ');
}

/**
 * Generates the SVG points string for the regular baseline homeostatic polygon (e.g. green circle/polygon at r=0.25).
 */
export function generateBaselinePolygon(
  numAxes: number,
  center: Point2D,
  maxRadius: number,
  baselineRatio = 0.25
): string {
  if (numAxes < 3) return '';
  const radii = new Array(numAxes).fill(baselineRatio);
  return calculatePolygonPoints(radii, center, maxRadius);
}

/**
 * Generates the SVG points string for the dynamic patient deviation polygon.
 * Radii are mapped from baselineRatio (when normalized=0) to 1.0 (when normalized=1):
 *   r_i = baselineRatio + (1.0 - baselineRatio) * normalized_i
 */
export function generatePatientPolygon(
  axes: RadarAxis[],
  normalizedValues: Record<string, number>,
  center: Point2D,
  maxRadius: number,
  baselineRatio = 0.25
): string {
  const numAxes = axes.length;
  if (numAxes === 0) return '';

  const radii = axes.map((axis) => {
    const val = normalizedValues[axis.id] ?? 0;
    const clampedVal = Math.min(1.0, Math.max(0.0, val));
    return baselineRatio + (1.0 - baselineRatio) * clampedVal;
  });

  return calculatePolygonPoints(radii, center, maxRadius);
}

/**
 * Generates concentric grid polygons at given levels (default: 0.25, 0.50, 0.75, 1.00).
 */
export function generateGridRings(
  numAxes: number,
  center: Point2D,
  maxRadius: number,
  levels: number[] = [0.25, 0.5, 0.75, 1.0]
): GridRing[] {
  if (numAxes < 3) return [];

  return levels.map((lvl) => {
    const radii = new Array(numAxes).fill(lvl);
    return {
      level: lvl,
      points: calculatePolygonPoints(radii, center, maxRadius)
    };
  });
}

/**
 * Generates axis spokes (lines from center to maximum perimeter).
 */
export function generateAxisSpokes(
  numAxes: number,
  center: Point2D,
  maxRadius: number,
  startAngleRad = -Math.PI / 2
): AxisSpoke[] {
  const spokes: AxisSpoke[] = [];

  for (let i = 0; i < numAxes; i++) {
    const angle = calculateAxisAngle(i, numAxes, startAngleRad);
    const end = polarToCartesian(center, maxRadius, angle);
    spokes.push({
      x1: center.x,
      y1: center.y,
      x2: end.x,
      y2: end.y,
      angle
    });
  }

  return spokes;
}

/**
 * Calculates optimal positions, text anchors, and baselines for axis labels.
 */
export function getAxisLabelPositions(
  axes: RadarAxis[],
  center: Point2D,
  maxRadius: number,
  labelOffset = 20,
  startAngleRad = -Math.PI / 2
): AxisLabelPosition[] {
  const total = axes.length;
  const labelRadius = maxRadius + labelOffset;

  return axes.map((axis, i) => {
    const angle = calculateAxisAngle(i, total, startAngleRad);
    const pt = polarToCartesian(center, labelRadius, angle);

    // Determine text anchor based on angle / x offset
    const cosVal = Math.cos(angle);
    const sinVal = Math.sin(angle);

    let textAnchor: 'start' | 'middle' | 'end' = 'middle';
    if (cosVal > 0.3) {
      textAnchor = 'start';
    } else if (cosVal < -0.3) {
      textAnchor = 'end';
    }

    let dominantBaseline: 'hanging' | 'middle' | 'baseline' | 'central' = 'central';
    if (sinVal > 0.5) {
      dominantBaseline = 'hanging';
    } else if (sinVal < -0.5) {
      dominantBaseline = 'baseline';
    }

    return {
      id: axis.id,
      label: axis.label,
      system: axis.system,
      x: pt.x,
      y: pt.y,
      textAnchor,
      dominantBaseline
    };
  });
}
