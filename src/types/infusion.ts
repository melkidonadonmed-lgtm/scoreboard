import { z } from 'zod';

/**
 * Zod schema for solution compounding and dilution recipe.
 */
export const SolutionRecipeSchema = z.object({
  ampoules: z.string(),
  diluent: z.string(),
  totalVolumeMl: z.number().positive(),
  concentrationMcgMl: z.number().positive(),
  mandatoryVehicleNotice: z.string().optional(),
  indication: z.string().optional()
});

export type SolutionRecipe = z.infer<typeof SolutionRecipeSchema>;

/**
 * Zod schema for continuous IV infusion protocol in BIC.
 */
export const InfusionProtocolSchema = z.object({
  drugId: z.string().optional(),
  drugName: z.string(),
  standardSolution: SolutionRecipeSchema,
  concentratedSolution: SolutionRecipeSchema.optional(),
  doseUnit: z.enum(['mcg/kg/min', 'UI/min', 'mcg/min']),
  initialDose: z.number().nonnegative(),
  maintenanceDoseMin: z.number().nonnegative(),
  maintenanceDoseMax: z.number().positive(),
  maxDose: z.number().positive(),
  defaultDose: z.number().positive(),
  isFixedDose: z.boolean().default(false),
  administrationRoute: z.string(),
  containerCompatibility: z.enum(['vidro_polietileno_obrigatorio', 'qualquer']).optional(),
  nursingPrecautions: z.string(),
  titrationAdvice: z.string().optional(),
  weaningCriteria: z.string().optional()
});

export type InfusionProtocol = z.infer<typeof InfusionProtocolSchema>;

/**
 * Parameters required to calculate BIC infusion rate.
 */
export const InfusionCalculationParamsSchema = z.object({
  drugId: z.string(),
  patientWeightKg: z.number().positive(),
  doseValue: z.number().nonnegative(),
  concentrationMcgPerMl: z.number().positive(),
  isFixedDose: z.boolean().optional()
});

export type InfusionCalculationParams = z.infer<typeof InfusionCalculationParamsSchema>;

/**
 * Results of BIC infusion calculation.
 */
export const InfusionCalculationResultSchema = z.object({
  rateMlPerHour: z.number().nonnegative(),
  recommendedVehicle: z.string(),
  containerAlert: z.string().optional(),
  safetyAlerts: z.array(z.string()),
  formattedDose: z.string(),
  concentrationFormatted: z.string().optional()
});

export type InfusionCalculationResult = z.infer<typeof InfusionCalculationResultSchema>;

/**
 * Titration step entry for rapid bedside reference table.
 */
export const TitrationStepSchema = z.object({
  dose: z.number(),
  rateMlPerHour: z.number(),
  label: z.string(),
  isWarning: z.boolean().optional()
});

export type TitrationStep = z.infer<typeof TitrationStepSchema>;
