import { z } from 'zod';
import {
  InfusionProtocolSchema,
  type InfusionProtocol
} from './infusion';
export { InfusionProtocolSchema, type InfusionProtocol };

// ==========================================
// 1. RADAR FISIOLÓGICO
// ==========================================

export const RadarAxisSchema = z.object({
  id: z.string(),
  label: z.string(),
  system: z.string(), // e.g. "Respiratório", "Cardiovascular", "Renal", "Neurológico"
  unit: z.string().optional(),
  baselineValue: z.number().default(0), // Normal homeostatic baseline = 0
  maxAxisValue: z.number().default(1)   // Maximum deviation = 1
});

export type RadarAxis = z.infer<typeof RadarAxisSchema>;
export const RadarAxisDefinitionSchema = RadarAxisSchema;
export type RadarAxisDefinition = RadarAxis;

// ==========================================
// 2. PARÂMETROS E OPÇÕES DO ESCORE
// ==========================================

export const ParameterOptionSchema = z.object({
  id: z.string(),
  label: z.string(),
  pointValue: z.number(),
  isNormalBaseline: z.boolean().default(false),
  radarNormalizedValue: z.number().min(0).max(1), // Mapped to radar (0 = normal, 1 = critical deviation)
  sortOrder: z.number().int(),
  description: z.string().optional()
});

export type ParameterOption = z.infer<typeof ParameterOptionSchema>;

export const ParameterGroupSchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
  inputType: z.enum(['single_choice', 'boolean', 'numeric_input', 'pupil_reactivity']),
  unit: z.string().optional(),
  radarAxisId: z.string(),
  normalBaselineValue: z.number().default(0),
  maxAxisValue: z.number().default(1),
  sortOrder: z.number().int(),
  options: z.array(ParameterOptionSchema),
  helpText: z.string().optional(),
  placeholder: z.string().optional(),
  minValue: z.number().optional(),
  maxValue: z.number().optional()
});

export type ParameterGroup = z.infer<typeof ParameterGroupSchema>;

// ==========================================
// 3. CONDUTAS CLÍNICAS E FAIXAS DE RISCO
// ==========================================

export const PharmacologicalActionSchema = z.object({
  id: z.string(),
  drugName: z.string(),
  dosage: z.string(),
  route: z.string(),
  frequency: z.string(),
  dilutionInstructions: z.string().optional(),
  renalAdjustment: z.string().optional(),
  contraindications: z.string().optional(),
  infusionProtocol: InfusionProtocolSchema.optional()
});

export type PharmacologicalAction = z.infer<typeof PharmacologicalActionSchema>;

export const NonPharmacologicalActionSchema = z.object({
  id: z.string(),
  recommendationTitle: z.string(),
  dispositionTarget: z.string(), // 'Alta Orientada' | 'Observação' | 'Enfermaria' | 'UTI' | etc.
  monitoringPlan: z.string(),
  interventionalProcedure: z.string().optional(),
  ventilatorySupport: z.string().optional(),
  vascularAccess: z.string().optional(),
  laboratoryPanel: z.string().optional()
});

export type NonPharmacologicalAction = z.infer<typeof NonPharmacologicalActionSchema>;

export const RiskTierSchema = z.object({
  id: z.string(),
  label: z.string(),
  severityLevel: z.enum(['low', 'intermediate', 'high', 'critical']),
  minScore: z.number(),
  maxScore: z.number(),
  statisticalOutcome: z.string(),
  colorHex: z.string(),
  pharmacologicalActions: z.array(PharmacologicalActionSchema),
  nonPharmacologicalActions: z.array(NonPharmacologicalActionSchema),
  infusionProtocol: InfusionProtocolSchema.optional()
});

export type RiskTier = z.infer<typeof RiskTierSchema>;

// ==========================================
// 4. CALCULADORA COMPLETA (MODELO SEED MONOGRÁFICO)
// ==========================================

export const CalculatorSchema = z.object({
  id: z.string(),
  slug: z.string(),
  name: z.string(),
  acronym: z.string(),
  version: z.string().optional(),
  category: z.string().optional(),
  subcategory: z.string().optional(),
  categorySlug: z.string(),
  categoryName: z.string().optional(),
  moduleName: z.string().optional(),
  description: z.string().optional(),
  summary: z.string(),
  clinicalObjective: z.string().optional(),
  targetPopulation: z.string().optional(),
  calculationType: z.enum(['additive_points', 'continuous_formula', 'branching_decision']),
  formulaExpression: z.string().optional(),
  evidenceSource: z.string(),
  minPossibleScore: z.number(),
  maxPossibleScore: z.number(),
  baseScore: z.number().default(0),
  ssc2021Warning: z.boolean().optional(),
  clinicalWarning: z.string().optional(),
  badge: z.string().optional(),
  radarAxes: z.array(RadarAxisSchema),
  parameterGroups: z.array(ParameterGroupSchema),
  riskTiers: z.array(RiskTierSchema),
  pharmacologicalActions: z.array(PharmacologicalActionSchema).optional(),
  nonPharmacologicalActions: z.array(NonPharmacologicalActionSchema).optional()
});

export type Calculator = z.infer<typeof CalculatorSchema>;
export type CalculatorDefinition = Calculator;
export const ClinicalToolSchema = CalculatorSchema;
export type ClinicalTool = Calculator;

export const BlockDataSchema = z.object({
  blockId: z.string(),
  blockName: z.string(),
  version: z.string(),
  categorySlug: z.string().optional(),
  description: z.string().optional(),
  calculators: z.array(CalculatorSchema)
});

export type BlockData = z.infer<typeof BlockDataSchema>;

// ==========================================
// 5. MANIFESTO LEVE DE BUSCA (~30KB)
// ==========================================

export const ManifestItemSchema = z.object({
  id: z.string(),
  slug: z.string(),
  name: z.string(),
  acronym: z.string(),
  category: z.string().optional(),
  subcategory: z.string().optional(),
  categorySlug: z.string(),
  categoryName: z.string(),
  moduleName: z.string(),
  description: z.string().optional(),
  summary: z.string(),
  synonyms: z.array(z.string()).optional(),
  searchSynonyms: z.array(z.string()),
  calculationType: z.enum(['additive_points', 'continuous_formula', 'branching_decision']),
  blockId: z.string().optional(),
  blockFile: z.string(),
  evidenceSource: z.string(),
  badge: z.string().optional(),
  hasInfusionProtocol: z.boolean().default(false),
  starredDefault: z.boolean().optional()
});

export const ManifestSchema = z.array(ManifestItemSchema);
export type ManifestItem = z.infer<typeof ManifestItemSchema>;
export type Manifest = z.infer<typeof ManifestSchema>;

// ==========================================
// 6. RESULTADO DO MOTOR DE CÁLCULO
// ==========================================

export const CalculationResultSchema = z.object({
  score: z.number().optional(),
  rawScore: z.number(),
  scoreFormatted: z.string(),
  activeRiskTier: RiskTierSchema,
  radarValues: z.record(z.string(), z.number()),
  radarPoints: z.record(z.string(), z.number()).optional(),
  clinicalWarning: z.string().optional(),
  sscWarning: z.string().optional(),
  warnings: z.array(z.string()).optional()
});

export type CalculationResult = z.infer<typeof CalculationResultSchema>;
