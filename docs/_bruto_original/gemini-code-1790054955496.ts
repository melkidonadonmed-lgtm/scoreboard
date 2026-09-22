/**
 * wcag-contrast-engine.ts
 * Motor matemático de cálculo de contraste WCAG 2.1 com suporte a Alpha Blending.
 * Zero dependências de runtime. Compatível com Node.js, Deno, Bun e navegadores.
 */

// ==========================================
// 1. TIPAGEM E CONTRATOS DE DADOS
// ==========================================

export interface RGBAColor {
  r: number; // 0 - 255
  g: number; // 0 - 255
  b: number; // 0 - 255
  a: number; // 0 - 1
}

export type WCAGLevel = 'AAA' | 'AA' | 'FAIL';

export interface ContrastAuditResult {
  ratio: number;
  formattedRatio: string;
  normalText: WCAGLevel;
  largeText: WCAGLevel;
  uiComponent: WCAGLevel;
  simulatedColor: string;
  notes: string[];
}

export interface GradientAuditResult {
  minRatio: number;
  worstStopColor: string;
  overallCompliance: WCAGLevel;
  stopResults: Array<{
    stopColor: string;
    ratio: number;
    passesAA: boolean;
  }>;
}

// ==========================================
// 2. PARSERS E CONVERSÕES DE COR
// ==========================================

/**
 * Converte strings de cor nos formatos Hexadecimal (#RGB, #RGBA, #RRGGBB, #RRGGBBAA)
 * ou Funcional (rgb(), rgba()) em um objeto estruturado RGBAColor.
 */
export function parseCSSColor(input: string): RGBAColor {
  const clean = input.trim().toLowerCase();

  // Tratamento de Hexadecimal
  if (clean.startsWith('#')) {
    const hex = clean.substring(1);
    
    if (hex.length === 3 || hex.length === 4) {
      // Formato curto: #RGB ou #RGBA
      const r = parseInt(hex[0] + hex[0], 16);
      const g = parseInt(hex[1] + hex[1], 16);
      const b = parseInt(hex[2] + hex[2], 16);
      const a = hex.length === 4 ? parseInt(hex[3] + hex[3], 16) / 255 : 1;
      return { r, g, b, a };
    }

    if (hex.length === 6 || hex.length === 8) {
      // Formato padrão: #RRGGBB ou #RRGGBBAA
      const r = parseInt(hex.substring(0, 2), 16);
      const g = parseInt(hex.substring(2, 4), 16);
      const b = parseInt(hex.substring(4, 6), 16);
      const a = hex.length === 8 ? parseInt(hex.substring(6, 8), 16) / 255 : 1;
      return { r, g, b, a };
    }

    throw new Error(`Formato hexadecimal inválido: "${input}". Use #RGB, #RGBA, #RRGGBB ou #RRGGBBAA.`);
  }

  // Tratamento de rgb() e rgba()
  const rgbRegex = /^rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*([\d.]+))?\s*\)$/;
  const match = clean.match(rgbRegex);

  if (match) {
    const r = Math.min(255, Math.max(0, parseInt(match[1], 10)));
    const g = Math.min(255, Math.max(0, parseInt(match[2], 10)));
    const b = Math.min(255, Math.max(0, parseInt(match[3], 10)));
    const a = match[4] !== undefined ? Math.min(1, Math.max(0, parseFloat(match[4]))) : 1;
    return { r, g, b, a };
  }

  throw new Error(`Sintaxe de cor não suportada ou inválida: "${input}". Use Hex ou RGB/RGBA.`);
}

// ==========================================
// 3. MATEMÁTICA DE COMPOSIÇÃO E LUMINÂNCIA
// ==========================================

/**
 * Aplica o algoritmo Porter-Duff (Source-Over) para mesclar uma cor translúcida de primeiro plano (fg)
 * sobre uma cor de fundo opaca (bg).
 */
export function blendAlpha(fg: RGBAColor, bg: RGBAColor): RGBAColor {
  if (bg.a < 1) {
    throw new Error('A superfície base (background) precisa ser opaca (alpha = 1) para aferição conclusiva.');
  }

  if (fg.a >= 1) {
    return { ...fg };
  }

  const alpha = fg.a;
  const invAlpha = 1 - alpha;

  return {
    r: Math.round(fg.r * alpha + bg.r * invAlpha),
    g: Math.round(fg.g * alpha + bg.g * invAlpha),
    b: Math.round(fg.b * alpha + bg.b * invAlpha),
    a: 1.0,
  };
}

/**
 * Calcula a Luminância Relativa (L) de acordo com o W3C WCAG 2.1.
 * L = 0.2126 * R + 0.7152 * G + 0.0722 * B, onde canais sRGB são deslinearizados.
 */
export function calculateRelativeLuminance(color: RGBAColor): number {
  const linearize = (channelValue: number): number => {
    const sRGB = channelValue / 255;
    return sRGB <= 0.04045 ? sRGB / 12.92 : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  };

  const rLin = linearize(color.r);
  const gLin = linearize(color.g);
  const bLin = linearize(color.b);

  return 0.2126 * rLin + 0.7152 * gLin + 0.0722 * bLin;
}

/**
 * Calcula a razão de contraste (Contrast Ratio) entre duas cores após linearização.
 * Fórmula: (L1 + 0.05) / (L2 + 0.05), variando de 1:1 a 21:1.
 */
export function calculateContrastRatio(fgColor: RGBAColor, bgColor: RGBAColor): number {
  // Realiza a composição do canal alfa do primeiro plano sobre o fundo antes da luminância
  const renderedFg = blendAlpha(fgColor, bgColor);

  const lumA = calculateRelativeLuminance(renderedFg);
  const lumB = calculateRelativeLuminance(bgColor);

  const lighter = Math.max(lumA, lumB);
  const darker = Math.min(lumA, lumB);

  const ratio = (lighter + 0.05) / (darker + 0.05);
  return Number(ratio.toFixed(2));
}

// ==========================================
// 4. AUDITORIA E MÉTODOS DE ALTO NÍVEL
// ==========================================

/**
 * Executa a auditoria completa de contraste para texto e UI, suportando cores com canal alfa.
 */
export function auditContrast(foregroundCSS: string, backgroundCSS: string): ContrastAuditResult {
  const fg = parseCSSColor(foregroundCSS);
  const bg = parseCSSColor(backgroundCSS);

  const ratio = calculateContrastRatio(fg, bg);
  const rendered = blendAlpha(fg, bg);
  const renderedHex = `#${rendered.r.toString(16).padStart(2, '0')}${rendered.g.toString(16).padStart(2, '0')}${rendered.b.toString(16).padStart(2, '0')}`;

  const notes: string[] = [];

  if (fg.a < 1) {
    notes.push(`Cor frontal possui transparência (${(fg.a * 100).toFixed(0)}%). O cálculo simulou a fusão sobre ${backgroundCSS}, resultando em ${renderedHex}.`);
  }

  // Regras WCAG 2.1:
  // Texto Normal: AA = 4.5:1, AAA = 7.0:1
  // Texto Grande (>=18pt ou >=14pt bold): AA = 3.0:1, AAA = 4.5:1
  // Componentes de UI e Bordas de inputs: AA = 3.0:1
  const normalText: WCAGLevel = ratio >= 7.0 ? 'AAA' : ratio >= 4.5 ? 'AA' : 'FAIL';
  const largeText: WCAGLevel = ratio >= 4.5 ? 'AAA' : ratio >= 3.0 ? 'AA' : 'FAIL';
  const uiComponent: WCAGLevel = ratio >= 3.0 ? 'AA' : 'FAIL';

  if (normalText === 'FAIL') {
    notes.push('Reprovado para texto de corpo (< 4.5:1). Risco severo de ilegibilidade sob luz ambiente.');
  }

  return {
    ratio,
    formattedRatio: `${ratio.toFixed(2)}:1`,
    normalText,
    largeText,
    uiComponent,
    simulatedColor: renderedHex,
    notes,
  };
}

/**
 * Avalia o pior cenário de contraste de um elemento de primeiro plano quando colocado sobre um gradiente linear.
 * Testa o elemento contra todos os pontos de transição (stops) do fundo.
 */
export function auditGradientContrast(foregroundCSS: string, gradientStopsCSS: string[]): GradientAuditResult {
  if (!gradientStopsCSS || gradientStopsCSS.length === 0) {
    throw new Error('Forneça ao menos uma cor de fundo para a avaliação de gradiente.');
  }

  let minRatio = Infinity;
  let worstStopColor = gradientStopsCSS[0];
  const stopResults = [];

  for (const stop of gradientStopsCSS) {
    const audit = auditContrast(foregroundCSS, stop);
    const passesAA = audit.normalText !== 'FAIL';

    stopResults.push({
      stopColor: stop,
      ratio: audit.ratio,
      passesAA,
    });

    if (audit.ratio < minRatio) {
      minRatio = audit.ratio;
      worstStopColor = stop;
    }
  }

  const overallCompliance: WCAGLevel = minRatio >= 7.0 ? 'AAA' : minRatio >= 4.5 ? 'AA' : 'FAIL';

  return {
    minRatio,
    worstStopColor,
    overallCompliance,
    stopResults,
  };
}