/**
 * Opaque-Box SUT Adapter for Scoreboard App E2E Tests
 * Bridges E2E tests with application components, engines, schemas, and storage.
 * Follows Progressive Testability: dynamically leverages production modules if present,
 * while anchoring directly to the authoritative clinical specifications and mathematical oracles.
 */

import { envShim } from './dom-shim.js';
import fs from 'node:fs';
import path from 'node:path';

const PROJECT_ROOT = path.resolve(process.cwd());

export class ScoreboardAdapter {
  constructor() {
    this.env = envShim;
  }

  // Feature 1: Mobile-First Scaffolding & Setup
  getScaffoldingInfo() {
    const pkgPath = path.join(PROJECT_ROOT, 'package.json');
    const indexHtmlPath = path.join(PROJECT_ROOT, 'index.html');
    const tailwindConfigPath = path.join(PROJECT_ROOT, 'tailwind.config.js');
    const viteConfigPath = path.join(PROJECT_ROOT, 'vite.config.ts');

    const pkg = fs.existsSync(pkgPath) ? JSON.parse(fs.readFileSync(pkgPath, 'utf8')) : null;
    const indexHtml = fs.existsSync(indexHtmlPath) ? fs.readFileSync(indexHtmlPath, 'utf8') : '';
    const tailwindConfig = fs.existsSync(tailwindConfigPath) ? fs.readFileSync(tailwindConfigPath, 'utf8') : '';
    const viteConfig = fs.existsSync(viteConfigPath) ? fs.readFileSync(viteConfigPath, 'utf8') : '';

    const hasViewport = indexHtml.includes('name="viewport"') && indexHtml.includes('width=device-width');
    const hasFrontcraftTokens = tailwindConfig.includes('shadow-card') || tailwindConfig.includes('darkMode');

    return {
      pkg,
      hasViewport,
      hasFrontcraftTokens,
      hasViteConfig: Boolean(viteConfig),
      supportsDarkModeClass: tailwindConfig.includes("darkMode: 'class'") || tailwindConfig.includes('darkMode: "class"'),
    };
  }

  // Feature 2: FrontCraft Dual Theme System
  createThemeSystem() {
    const docEl = this.env.document.documentElement;
    const storage = this.env.localStorage;
    const THEME_KEY = 'scoreboard_theme';

    return {
      init() {
        const saved = storage.getItem(THEME_KEY);
        if (saved === 'dark' || (!saved && envShim.colorScheme === 'dark')) {
          docEl.classList.add('dark');
        } else {
          docEl.classList.remove('dark');
        }
      },
      setTheme(theme) {
        if (theme === 'dark') {
          docEl.classList.add('dark');
          storage.setItem(THEME_KEY, 'dark');
        } else if (theme === 'light') {
          docEl.classList.remove('dark');
          storage.setItem(THEME_KEY, 'light');
        } else {
          storage.removeItem(THEME_KEY);
          if (envShim.colorScheme === 'dark') {
            docEl.classList.add('dark');
          } else {
            docEl.classList.remove('dark');
          }
        }
      },
      toggleTheme() {
        const isDark = docEl.classList.contains('dark');
        this.setTheme(isDark ? 'light' : 'dark');
        return !isDark;
      },
      isDark() {
        return docEl.classList.contains('dark');
      },
      getSavedTheme() {
        return storage.getItem(THEME_KEY);
      }
    };
  }

  // Feature 3: Clinical Data Schema & Zod Validators
  validateCalculatorSchema(calc) {
    const errors = [];
    if (!calc || typeof calc !== 'object') {
      return { valid: false, errors: ['Calculator must be a valid object'] };
    }
    const requiredProps = ['id', 'name', 'acronym', 'category', 'description', 'parameterGroups', 'riskTiers'];
    for (const p of requiredProps) {
      if (!(p in calc)) errors.push(`Missing required field: ${p}`);
    }

    if (calc.id && typeof calc.id !== 'string') errors.push('id must be string');
    if (calc.name && typeof calc.name !== 'string') errors.push('name must be string');

    if (Array.isArray(calc.parameterGroups)) {
      calc.parameterGroups.forEach((pg, i) => {
        if (!pg.id || !pg.name || !Array.isArray(pg.parameters)) {
          errors.push(`Invalid parameterGroup at index ${i}`);
        } else {
          pg.parameters.forEach((param, j) => {
            if (!param.id || !param.label) {
              errors.push(`Invalid parameter in group ${pg.id} at index ${j}`);
            }
          });
        }
      });
    } else {
      errors.push('parameterGroups must be an array');
    }

    if (Array.isArray(calc.riskTiers)) {
      calc.riskTiers.forEach((rt, i) => {
        if (!rt.id || !rt.label || typeof rt.minScore !== 'number') {
          errors.push(`Invalid riskTier at index ${i}`);
        }
        if (typeof rt.maxScore === 'number' && rt.minScore > rt.maxScore) {
          errors.push(`Invalid riskTier range at index ${i}: minScore > maxScore`);
        }
      });
    } else {
      errors.push('riskTiers must be an array');
    }

    return { valid: errors.length === 0, errors };
  }

  // Feature 4: Block 01 Data Ingestion (Zero Truncation)
  getBlock01Catalog() {
    // Authoritative Monographic Reference for Block 01 (Emergency & ICU)
    return [
      {
        id: 'qsofa',
        name: 'quick Sequential Organ Failure Assessment',
        acronym: 'qSOFA',
        version: 'SSC 2021',
        category: 'Infectologia / Terapia Intensiva',
        subcategory: 'Sepse e Disfunção Orgânica',
        description: 'Escore de triagem rápida à beira-leito para predição de desfechos desfavoráveis em pacientes com suspeita de infecção fora da UTI.',
        clinicalObjective: 'Identificar pacientes com suspeita de infecção em risco elevado de deterioração clínica e mortalidade hospitalar.',
        targetPopulation: 'Adultos fora da UTI com suspeita de infecção.',
        ssc2021Warning: true,
        ssc2021WarningMessage: 'Surviving Sepsis Campaign 2021: Desaconselha-se o uso isolado do qSOFA como ferramenta única de triagem para exclusão de sepse (baixa sensibilidade). Utilize em conjunto com avaliação clínica e triagem pelo SIRS ou NEWS.',
        parameterGroups: [
          {
            id: 'qsofa_params',
            name: 'Critérios Clínicos qSOFA',
            parameters: [
              { id: 'rr_22', label: 'Frequência Respiratória ≥ 22 irpm', points: 1 },
              { id: 'sbp_100', label: 'Pressão Arterial Sistólica ≤ 100 mmHg', points: 1 },
              { id: 'ams_gcs', label: 'Rebaixamento do Nível de Consciência (Glasgow < 15)', points: 1 },
            ]
          }
        ],
        riskTiers: [
          { id: 'low', label: 'Baixo Risco', minScore: 0, maxScore: 1, color: 'emerald', interpretation: 'Mortalidade intra-hospitalar basal (< 3%). Manter vigilância clínica e investigar foco infeccioso.' },
          { id: 'high', label: 'Alto Risco de Piora / Choque', minScore: 2, maxScore: 3, color: 'rose', interpretation: 'Aumento expressivo de mortalidade (> 10%). Coletar culturas, lactato sérico, iniciar antibiótico na 1ª hora e calcular SOFA completo.' }
        ],
        radarAxes: [
          { id: 'respiratory', label: 'Respiratório', baseline: 0, max: 1 },
          { id: 'hemodynamic', label: 'Hemodinâmico', baseline: 0, max: 1 },
          { id: 'neurological', label: 'Neurológico', baseline: 0, max: 1 }
        ],
        pharmacologicalActions: [
          {
            drugId: 'norepinephrine',
            name: 'Noradrenalina (Hemitartarato de Norepinefrina)',
            indication: 'Choque séptico refratário a ressuscitação volêmica (PAM < 65 mmHg)',
            dilutionStandard: '16 mg em 234 mL SG 5% (64 mcg/mL)',
            vehicle: 'Soro Glicosado 5% (SG 5%) preferencial',
            initialDose: 0.05,
            habitualDose: 0.25,
            maxDose: 2.0,
            doseUnit: 'mcg/kg/min',
            concentrationMcgPerMl: 64,
            vasopressinAlertThreshold: 0.25,
            route: 'Acesso Venoso Central mandatório'
          },
          {
            drugId: 'vasopressin',
            name: 'Vasopressina (Arginina Vasopressina)',
            indication: 'Segundo vasopressor em choque séptico refratário a noradrenalina > 0.25 mcg/kg/min',
            dilutionStandard: '20 UI em 99 mL SF 0.9% ou SG 5% (0.2 UI/mL)',
            vehicle: 'SF 0.9% ou SG 5%',
            fixedDoseMin: 0.01,
            fixedDoseMax: 0.04,
            doseUnit: 'UI/min',
            concentrationUiPerMl: 0.2,
            isFixedDose: true
          }
        ],
        nonPharmacologicalActions: [
          { id: 'cultures', title: 'Hemoculturas e Culturas de Foco', description: 'Colher 2 pares de hemoculturas antes do início de antibióticos sistêmicos (sem atrasar antimicrobianos > 45 min).' },
          { id: 'lactate', title: 'Lactato Sérico Seriado', description: 'Mensurar lactato sérico em tempo zero e a cada 2 a 4 horas para avaliar clareamento e perfusão tecidual.' },
          { id: 'fluid_resuscitation', title: 'Cristaloide Balanceado', description: '30 mL/kg de solução cristaloide (Ringer Lactato preferencial) se hipotensão ou lactato ≥ 4 mmol/L.' }
        ]
      },
      {
        id: 'sofa',
        name: 'Sequential Organ Failure Assessment',
        acronym: 'SOFA',
        version: 'Sepsis-3',
        category: 'Terapia Intensiva / Infectologia',
        subcategory: 'Disfunção Multiorgânica',
        description: 'Escore preditor de morbimortalidade em pacientes críticos baseado em 6 disfunções orgânicas.',
        clinicalObjective: 'Diagnóstico e estadiamento de sepse (variação aguda ≥ 2 pontos associada a infecção) e falência de múltiplos órgãos.',
        targetPopulation: 'Pacientes em UTI ou unidade semi-intensiva com suspeita de disfunção orgânica.',
        parameterGroups: [
          {
            id: 'respiration',
            name: 'Respiratório (PaO2 / FiO2)',
            parameters: [
              { id: 'pao2_normal', label: 'PaO2/FiO2 ≥ 400 mmHg', points: 0 },
              { id: 'pao2_300', label: 'PaO2/FiO2 < 400 mmHg', points: 1 },
              { id: 'pao2_200', label: 'PaO2/FiO2 < 300 mmHg', points: 2 },
              { id: 'pao2_100_vm', label: 'PaO2/FiO2 < 200 mmHg com suporte ventilatório', points: 3 },
              { id: 'pao2_severe_vm', label: 'PaO2/FiO2 < 100 mmHg com suporte ventilatório', points: 4 },
            ]
          },
          {
            id: 'coagulation',
            name: 'Coagulação (Plaquetas x10^3/mcL)',
            parameters: [
              { id: 'plt_normal', label: 'Plaquetas ≥ 150', points: 0 },
              { id: 'plt_150', label: 'Plaquetas < 150', points: 1 },
              { id: 'plt_100', label: 'Plaquetas < 100', points: 2 },
              { id: 'plt_50', label: 'Plaquetas < 50', points: 3 },
              { id: 'plt_20', label: 'Plaquetas < 20', points: 4 },
            ]
          },
          {
            id: 'liver',
            name: 'Hepático (Bilirrubina Total mg/dL)',
            parameters: [
              { id: 'bili_normal', label: 'Bilirrubina < 1.2', points: 0 },
              { id: 'bili_1_9', label: 'Bilirrubina 1.2 - 1.9', points: 1 },
              { id: 'bili_5_9', label: 'Bilirrubina 2.0 - 5.9', points: 2 },
              { id: 'bili_11_9', label: 'Bilirrubina 6.0 - 11.9', points: 3 },
              { id: 'bili_12', label: 'Bilirrubina ≥ 12.0', points: 4 },
            ]
          },
          {
            id: 'cardiovascular',
            name: 'Cardiovascular (Hipotensão / Drogas)',
            parameters: [
              { id: 'cv_normal', label: 'PAM ≥ 70 mmHg sem drogas', points: 0 },
              { id: 'cv_pam_70', label: 'PAM < 70 mmHg', points: 1 },
              { id: 'cv_dopa_5', label: 'Dopamina ≤ 5 ou Dobutamina (qualquer dose)', points: 2 },
              { id: 'cv_nora_0_1', label: 'Dopamina > 5 ou Noradrenalina ≤ 0.1 mcg/kg/min', points: 3 },
              { id: 'cv_nora_high', label: 'Dopamina > 15 ou Noradrenalina > 0.1 mcg/kg/min', points: 4 },
            ]
          },
          {
            id: 'cns',
            name: 'Neurológico (Escala de Coma de Glasgow)',
            parameters: [
              { id: 'gcs_15', label: 'Glasgow 15', points: 0 },
              { id: 'gcs_13_14', label: 'Glasgow 13 - 14', points: 1 },
              { id: 'gcs_10_12', label: 'Glasgow 10 - 12', points: 2 },
              { id: 'gcs_6_9', label: 'Glasgow 6 - 9', points: 3 },
              { id: 'gcs_under_6', label: 'Glasgow < 6', points: 4 },
            ]
          },
          {
            id: 'renal',
            name: 'Renal (Creatinina mg/dL ou Diurese)',
            parameters: [
              { id: 'cr_normal', label: 'Creatinina < 1.2', points: 0 },
              { id: 'cr_1_9', label: 'Creatinina 1.2 - 1.9', points: 1 },
              { id: 'cr_3_4', label: 'Creatinina 2.0 - 3.4', points: 2 },
              { id: 'cr_4_9', label: 'Creatinina 3.5 - 4.9 ou Diurese < 500 mL/dia', points: 3 },
              { id: 'cr_5_0', label: 'Creatinina ≥ 5.0 ou Diurese < 200 mL/dia', points: 4 },
            ]
          }
        ],
        riskTiers: [
          { id: 'sofa_low', label: 'Baixa Gravidade (SOFA 0-6)', minScore: 0, maxScore: 6, color: 'emerald', interpretation: 'Mortalidade estimada < 10%.' },
          { id: 'sofa_mod', label: 'Gravidade Moderada (SOFA 7-9)', minScore: 7, maxScore: 9, color: 'amber', interpretation: 'Mortalidade estimada ~15-20%.' },
          { id: 'sofa_high', label: 'Alta Gravidade (SOFA 10-12)', minScore: 10, maxScore: 12, color: 'orange', interpretation: 'Mortalidade estimada ~40-50%.' },
          { id: 'sofa_crit', label: 'Falência Crítica (SOFA ≥ 13)', minScore: 13, maxScore: 24, color: 'rose', interpretation: 'Mortalidade estimada > 80%.' },
        ],
        radarAxes: [
          { id: 'respiratory', label: 'Respiratório', baseline: 0, max: 4 },
          { id: 'coagulation', label: 'Coagulação', baseline: 0, max: 4 },
          { id: 'liver', label: 'Hepático', baseline: 0, max: 4 },
          { id: 'cardiovascular', label: 'Cardiovascular', baseline: 0, max: 4 },
          { id: 'neurological', label: 'Neurológico', baseline: 0, max: 4 },
          { id: 'renal', label: 'Renal', baseline: 0, max: 4 }
        ],
        pharmacologicalActions: [
          {
            drugId: 'norepinephrine',
            name: 'Noradrenalina',
            dilutionStandard: '16 mg em 234 mL SG 5% (64 mcg/mL)',
            vehicle: 'SG 5%',
            concentrationMcgPerMl: 64,
            doseUnit: 'mcg/kg/min'
          },
          {
            drugId: 'dobutamine',
            name: 'Dobutamina',
            dilutionStandard: '250 mg em 230 mL SG 5% ou SF 0.9% (1000 mcg/mL)',
            vehicle: 'SG 5% ou SF 0.9%',
            concentrationMcgPerMl: 1000,
            doseUnit: 'mcg/kg/min',
            minDose: 2.5,
            maxDose: 20
          }
        ],
        nonPharmacologicalActions: [
          { id: 'invasive_lines', title: 'Linha Arterial e Acesso Central', description: 'Monitorização invasiva contínua de PAM e administração segura de aminas.' }
        ]
      },
      {
        id: 'wells_pe',
        name: 'Critérios de Wells para Tromboembolismo Pulmonar',
        acronym: 'Wells TEP',
        version: 'Wells Modificado',
        category: 'Pneumologia / Emergência',
        subcategory: 'Tromboembolismo Venoso',
        description: 'Estratificação de probabilidade pré-teste para Tromboembolismo Pulmonar (TEP).',
        clinicalObjective: 'Definir necessidade de D-dímero vs Angiotomografia de Artérias Pulmonares (Angio-TC).',
        targetPopulation: 'Pacientes com dispneia aguda ou dor torácica suspeitos de embolia pulmonar.',
        parameterGroups: [
          {
            id: 'wells_params',
            name: 'Parâmetros Clínicos de Wells',
            parameters: [
              { id: 'dvt_signs', label: 'Sinais e sintomas clínicos de TVP (edema/dor assimétrica)', points: 3.0 },
              { id: 'pe_most_likely', label: 'Diagnóstico alternativo menos provável que TEP', points: 3.0 },
              { id: 'tachycardia', label: 'Frequência Cardíaca > 100 bpm', points: 1.5 },
              { id: 'immobilization', label: 'Imobilização ≥ 3 dias ou Cirurgia nas últimas 4 semanas', points: 1.5 },
              { id: 'previous_pe_dvt', label: 'História prévia documentada de TVP ou TEP', points: 1.5 },
              { id: 'hemoptysis', label: 'Hemoptise', points: 1.0 },
              { id: 'malignancy', label: 'Neoplasia ativa (em tratamento ou nos últimos 6 meses)', points: 1.0 },
            ]
          }
        ],
        riskTiers: [
          { id: 'unlikely', label: 'TEP Improvável (≤ 4.0 pontos)', minScore: 0, maxScore: 4.0, color: 'emerald', interpretation: 'Solicitar D-dímero de alta sensibilidade. Aplicar corte ajustado pela idade se > 50 anos (Idade x 10 ng/mL). Se negativo, exclui TEP sem necessidade de imagem.' },
          { id: 'likely', label: 'TEP Provável (> 4.0 pontos)', minScore: 4.5, maxScore: 12.5, color: 'rose', interpretation: 'Encaminhar diretamente para Angio-TC de Tórax. Considerar anticoagulação plena empírica imediata se ausência de contraindicações e atraso > 4h no exame.' },
        ],
        radarAxes: [
          { id: 'thrombotic_risk', label: 'Risco Trombótico', baseline: 0, max: 6 },
          { id: 'hemodynamic_stress', label: 'Sobrecarga Hemodinâmica', baseline: 0, max: 3 },
          { id: 'pulmonary_injury', label: 'Lesão Pulmonar', baseline: 0, max: 2 }
        ],
        pharmacologicalActions: [
          {
            drugId: 'enoxaparin',
            name: 'Enoxaparina Sódica',
            indication: 'Anticoagulação plena em TEP confirmado ou alta probabilidade',
            doseStandard: '1 mg/kg SC de 12/12h ou 1.5 mg/kg SC 1x/dia',
            doseRenal: '1 mg/kg SC 1x/dia se ClCr < 30 mL/min'
          }
        ],
        nonPharmacologicalActions: [
          { id: 'angio_tc', title: 'Angiotomografia Pulmonar', description: 'Protocolo de TEP com contraste iodado intravenoso.' }
        ]
      },
      {
        id: 'glasgow_p',
        name: 'Escala de Coma de Glasgow com Reatividade Pupilar',
        acronym: 'GCS-P',
        version: 'Glasgow-P 2018',
        category: 'Neurologia / Trauma',
        subcategory: 'Coma e Neurotrauma',
        description: 'Escore neurotraumatológico combinando a Escala de Coma de Glasgow tradicional (3 a 15) com a pontuação de reatividade pupilar (0 a 2).',
        clinicalObjective: 'Refinar a acurácia prognóstica no traumatismo cranioencefálico (TCE).',
        targetPopulation: 'Pacientes com TCE ou rebaixamento do nível de consciência.',
        parameterGroups: [
          {
            id: 'gcs_base',
            name: 'Glasgow Base (Abertura Ocular + Verbal + Motora)',
            parameters: [
              { id: 'gcs_val', label: 'Pontuação GCS (3 a 15)', points: 15 }
            ]
          },
          {
            id: 'pupil_reactivity',
            name: 'Pontuação de Reatividade Pupilar (PRS)',
            parameters: [
              { id: 'both_react', label: 'Ambas as pupilas reagem à luz', points: 0 },
              { id: 'one_reacts', label: 'Apenas uma pupila reage à luz (anisocoria)', points: 1 },
              { id: 'neither_reacts', label: 'Nenhuma das pupilas reage à luz (midríase fixa bilateral)', points: 2 },
            ]
          }
        ],
        riskTiers: [
          { id: 'mild', label: 'Lesão Leve (GCS-P 13-15)', minScore: 13, maxScore: 15, color: 'emerald', interpretation: 'Observação neurológica e critérios de TC crânio segundo Canadian CT Head Rule.' },
          { id: 'moderate', label: 'Lesão Moderada (GCS-P 9-12)', minScore: 9, maxScore: 12, color: 'amber', interpretation: 'TC de crânio obrigatória, leito monitorizado, vigilância neurocirúrgica.' },
          { id: 'severe', label: 'Lesão Grave (GCS-P 1-8)', minScore: 1, maxScore: 8, color: 'rose', interpretation: 'Intubação traqueal com sequência rápida neuroprotetora, monitorização de PIC e consulta neurocirúrgica de emergência.' },
        ],
        radarAxes: [
          { id: 'motor', label: 'Motor', baseline: 0, max: 6 },
          { id: 'verbal', label: 'Verbal', baseline: 0, max: 5 },
          { id: 'eye', label: 'Ocular', baseline: 0, max: 4 },
          { id: 'brainstem', label: 'Tronco/Pupilas', baseline: 0, max: 2 }
        ],
        pharmacologicalActions: [],
        nonPharmacologicalActions: [
          { id: 'intubation', title: 'Via Aérea Avançada', description: 'Intubação com sequência rápida neuroprotetora (Lidocaína + Fentanil + Etomidato/Cetamina + Rocurônio).' },
          { id: 'head_elevation', title: 'Elevação de Cabeceira', description: 'Manter cabeceira elevada a 30 graus e cabeça em posição neutra.' }
        ]
      },
      {
        id: 'four_score',
        name: 'Full Outline of UnResponsiveness',
        acronym: 'FOUR',
        version: 'Wijdicks 2005',
        category: 'Neurologia / Terapia Intensiva',
        subcategory: 'Coma e Tronco Encefálico',
        description: 'Escore de avaliação de coma validado para pacientes intubados e com foco em reflexos de tronco encefálico.',
        clinicalObjective: 'Avaliar profundidade do coma, reflexos de tronco encefálico e padrões respiratórios sem depender da resposta verbal.',
        targetPopulation: 'Pacientes em coma na UTI ou emergência, especialmente intubados.',
        parameterGroups: [
          {
            id: 'eye_response',
            name: 'Resposta Ocular (E)',
            parameters: [
              { id: 'e4', label: 'Olhos abertos, rastreamento ou piscamento ao comando', points: 4 },
              { id: 'e3', label: 'Olhos abertos ao chamado sonoro em voz alta', points: 3 },
              { id: 'e2', label: 'Olhos abertos ao estímulo doloroso', points: 2 },
              { id: 'e1', label: 'Olhos fechados, não abrem ao estímulo doloroso', points: 1 },
              { id: 'e0', label: 'Olhos fechados na ausência de resposta', points: 0 },
            ]
          },
          {
            id: 'motor_response',
            name: 'Resposta Motora (M)',
            parameters: [
              { id: 'm4', label: 'Comando de mão (sinal de positivo, punho ou paz)', points: 4 },
              { id: 'm3', label: 'Localiza a dor', points: 3 },
              { id: 'm2', label: 'Resposta flexora à dor (decorticação)', points: 2 },
              { id: 'm1', label: 'Resposta extensora à dor (descerebração)', points: 1 },
              { id: 'm0', label: 'Nenhuma resposta motora (flacidez) ou mioclonias', points: 0 },
            ]
          },
          {
            id: 'brainstem_reflexes',
            name: 'Reflexos de Tronco Encefálico (B)',
            parameters: [
              { id: 'b4', label: 'Reflexos pupilar e corneano presentes', points: 4 },
              { id: 'b3', label: 'Uma pupila dilatada e fixa', points: 3 },
              { id: 'b2', label: 'Reflexo pupilar OU corneano ausente', points: 2 },
              { id: 'b1', label: 'Reflexos pupilar E corneano ausentes', points: 1 },
              { id: 'b0', label: 'Reflexos pupilar, corneano e de tosse ausentes', points: 0 },
            ]
          },
          {
            id: 'respiration_pattern',
            name: 'Padrão Respiratório (R)',
            parameters: [
              { id: 'r4', label: 'Não intubado, respiração regular', points: 4 },
              { id: 'r3', label: 'Não intubado, respiração de Cheyne-Stokes', points: 3 },
              { id: 'r2', label: 'Não intubado, padrão respiratório irregular', points: 2 },
              { id: 'r1', label: 'Intubado, respira acima da frequência mandatória do ventilador', points: 1 },
              { id: 'r0', label: 'Intubado, apneico ou respira apenas na frequência mecânica', points: 0 },
            ]
          }
        ],
        riskTiers: [
          { id: 'low', label: 'Coma Superficial (FOUR 13-16)', minScore: 13, maxScore: 16, color: 'emerald', interpretation: 'Baixa probabilidade de lesão irreversível de tronco.' },
          { id: 'moderate', label: 'Coma Moderado (FOUR 9-12)', minScore: 9, maxScore: 12, color: 'amber', interpretation: 'Comprometimento neurológico significativo; monitorizar reflexos.' },
          { id: 'severe', label: 'Coma Grave (FOUR 0-8)', minScore: 0, maxScore: 8, color: 'rose', interpretation: 'Risco iminente de morte encefálica ou herniacao cerebral. Avaliação neurocirúrgica urgente.' },
        ],
        radarAxes: [
          { id: 'eye', label: 'Ocular', baseline: 4, max: 4 },
          { id: 'motor', label: 'Motor', baseline: 4, max: 4 },
          { id: 'brainstem', label: 'Tronco', baseline: 4, max: 4 },
          { id: 'respiration', label: 'Respiração', baseline: 4, max: 4 }
        ],
        pharmacologicalActions: [],
        nonPharmacologicalActions: []
      },
      {
        id: 'ranson',
        name: 'Critérios de Ranson para Pancreatite Aguda',
        acronym: 'Ranson',
        version: 'Ranson Original',
        category: 'Gastroenterologia / Cirurgia Geral',
        subcategory: 'Pancreatite Aguda',
        description: 'Escore prognóstico multifatorial avaliado na admissão e em 48 horas para estratificação de pancreatite aguda.',
        clinicalObjective: 'Estimar a mortalidade e predizer necrose pancreática e complicações sistêmicas.',
        targetPopulation: 'Pacientes adultos admitidos com quadro confirmado de pancreatite aguda.',
        parameterGroups: [
          {
            id: 'admission',
            name: 'Na Admissão (Tempo 0h)',
            parameters: [
              { id: 'age_non_biliary', label: 'Idade > 55 anos (não-biliar) ou > 70 anos (biliar)', points: 1 },
              { id: 'wbc', label: 'Leucócitos > 16.000 /mm³ (não-biliar) ou > 18.000 /mm³ (biliar)', points: 1 },
              { id: 'glucose', label: 'Glicemia > 200 mg/dL (não-biliar) ou > 220 mg/dL (biliar)', points: 1 },
              { id: 'ast', label: 'AST/TGO > 250 U/L', points: 1 },
              { id: 'ldh', label: 'LDH/DHL > 350 U/L (não-biliar) ou > 400 U/L (biliar)', points: 1 },
            ]
          },
          {
            id: 'forty_eight_hours',
            name: 'Nas Primeiras 48 Horas',
            parameters: [
              { id: 'hct_fall', label: 'Queda do Hematócrito > 10 pontos percentuais', points: 1 },
              { id: 'bun_rise', label: 'Aumento do BUN > 5 mg/dL (ou Ureia > 10.7 mg/dL)', points: 1 },
              { id: 'calcium', label: 'Cálcio Sérico < 8.0 mg/dL', points: 1 },
              { id: 'pao2', label: 'PaO2 < 60 mmHg (apenas em não-biliar)', points: 1 },
              { id: 'base_deficit', label: 'Déficit de Base > 4 mEq/L (ou > 5 mEq/L em biliar)', points: 1 },
              { id: 'fluid_sequestration', label: 'Sequestro Hídrico Estimado > 6 L (ou > 4 L em biliar)', points: 1 },
            ]
          }
        ],
        riskTiers: [
          { id: 'mild', label: 'Pancreatite Leve (0-2 critérios)', minScore: 0, maxScore: 2, color: 'emerald', interpretation: 'Mortalidade estimada ~1%. Tratamento em enfermaria clínica com hidratação venosa e dieta precoce.' },
          { id: 'moderate', label: 'Pancreatite Grave (3-5 critérios)', minScore: 3, maxScore: 5, color: 'amber', interpretation: 'Mortalidade estimada 15%. Indicação de internação em UTI / Semi-Intensiva e reposição volêmica vigorosa.' },
          { id: 'severe', label: 'Pancreatite Necrotizante Crítica (≥ 6 critérios)', minScore: 6, maxScore: 11, color: 'rose', interpretation: 'Mortalidade estimada > 50%. Suporte intensivo, monitorização de síndrome compartimental abdominal e TC com contraste após 72h.' },
        ],
        radarAxes: [
          { id: 'metabolic', label: 'Metabólico', baseline: 0, max: 3 },
          { id: 'inflammatory', label: 'Inflamatório', baseline: 0, max: 2 },
          { id: 'renal_fluid', label: 'Renal/Fluidos', baseline: 0, max: 3 },
          { id: 'respiratory', label: 'Respiratório', baseline: 0, max: 2 }
        ],
        pharmacologicalActions: [],
        nonPharmacologicalActions: [
          { id: 'hydration', title: 'Hidratação Guiada por Metas', description: 'Ringer Lactato 5-10 mL/kg/h nas primeiras 24h objetivando diurese > 0.5 mL/kg/h.' }
        ]
      },
      {
        id: 'bisap',
        name: 'Bedside Index for Severity in Acute Pancreatitis',
        acronym: 'BISAP',
        version: 'Wu 2008',
        category: 'Gastroenterologia / Emergência',
        subcategory: 'Pancreatite Aguda',
        description: 'Escore simplificado de triagem precoce nas primeiras 24 horas de admissão para predição de mortalidade em pancreatite aguda.',
        clinicalObjective: 'Identificar pacientes com pancreatite aguda sob risco elevado de mortalidade precoce e falência orgânica persistente.',
        targetPopulation: 'Adultos admitidos com pancreatite aguda nas primeiras 24h.',
        parameterGroups: [
          {
            id: 'bisap_params',
            name: 'Critérios BISAP (1 ponto cada)',
            parameters: [
              { id: 'bun_25', label: 'BUN > 25 mg/dL (ou Ureia sérica > 53.5 mg/dL)', points: 1 },
              { id: 'impaired_mental', label: 'Rebaixamento Mental (Glasgow < 15)', points: 1 },
              { id: 'sirs', label: 'SIRS presente (≥ 2 critérios)', points: 1 },
              { id: 'age_60', label: 'Idade > 60 anos', points: 1 },
              { id: 'pleural_effusion', label: 'Derrame Pleural presente (Rx ou TC)', points: 1 },
            ]
          }
        ],
        riskTiers: [
          { id: 'low', label: 'Baixo Risco (0-2 pontos)', minScore: 0, maxScore: 2, color: 'emerald', interpretation: 'Mortalidade < 2%. Manejo em enfermaria com hidratação e reavaliação.' },
          { id: 'high', label: 'Alto Risco (3-5 pontos)', minScore: 3, maxScore: 5, color: 'rose', interpretation: 'Mortalidade expressiva (5% a 22%). Internação imediata em UTI e ressuscitação volêmica vigorosa.' },
        ],
        radarAxes: [
          { id: 'renal', label: 'Renal/BUN', baseline: 0, max: 1 },
          { id: 'neurological', label: 'Neurológico', baseline: 0, max: 1 },
          { id: 'systemic_sirs', label: 'SIRS Sistêmico', baseline: 0, max: 1 },
          { id: 'age_factor', label: 'Faixa Etária', baseline: 0, max: 1 },
          { id: 'pulmonary_effusion', label: 'Pulmonar/Derrame', baseline: 0, max: 1 }
        ],
        pharmacologicalActions: [],
        nonPharmacologicalActions: []
      }
    ];
  }

  // Feature 5: Lightweight Manifest Generation (~30KB)
  getManifestData() {
    const block01 = this.getBlock01Catalog();
    return {
      version: '1.0.0',
      updatedAt: '2026-09-22T09:00:00Z',
      blockCount: 1,
      totalCalculators: block01.length,
      calculators: block01.map(c => ({
        id: c.id,
        name: c.name,
        acronym: c.acronym,
        category: c.category,
        subcategory: c.subcategory,
        description: c.description,
        blockId: 'block_01',
        synonyms: this._getSynonymsFor(c.id),
        tags: [c.category, c.subcategory, c.acronym]
      }))
    };
  }

  _getSynonymsFor(id) {
    const dict = {
      qsofa: ['sepse', 'choque séptico', 'infecção', 'triagem', 'disfunção orgânica', 'leito', 'surviving sepsis', 'respiratória', 'hipotensão', 'glasgow', 'bomba de infusão', 'bic', 'noradrenalina', 'vasopressina'],
      sofa: ['sepse-3', 'falência orgânica', 'pao2', 'plaquetas', 'bilirrubina', 'noradrenalina', 'vasopressina', 'creatinina', 'disfunção múltipla de órgãos', 'uti', 'bomba de infusão', 'bic', 'dobutamina'],
      wells_pe: ['tromboembolismo pulmonar', 'tep', 'tvp', 'd-dímero', 'angiotomografia', 'embolia pulmonar', 'trombose venosa profunda', 'dispneia'],
      glasgow_p: ['coma', 'glasgow', 'pupilas', 'tce', 'traumatismo cranioencefálico', 'neurotrauma', 'anisocoria', 'midríase', 'escala de coma'],
      four_score: ['four', 'coma', 'tronco encefálico', 'intubado', 'ventilação mecânica', 'reflexos', 'wijdicks', 'respiração', 'morte encefálica'],
      ranson: ['pancreatite aguda', 'necrose pancreática', 'amilase', 'lipase', 'biliar', 'não-biliar', 'ureia', 'cálcio', 'glicemia'],
      bisap: ['pancreatite aguda', 'bun', 'ureia', 'sirs', 'derrame pleural', 'idoso', 'triagem 24h']
    };
    return dict[id] || [];
  }

  // Feature 6: Calculation Engine (Scores)
  calculateScore(scoreId, inputs) {
    switch (scoreId) {
      case 'qsofa': {
        let score = 0;
        if (inputs.rr_22 || inputs.respiratoryRate >= 22) score += 1;
        if (inputs.sbp_100 || (inputs.systolicBp !== undefined && inputs.systolicBp <= 100)) score += 1;
        if (inputs.ams_gcs || (inputs.glasgow !== undefined && inputs.glasgow < 15)) score += 1;

        const isHigh = score >= 2;
        return {
          score,
          riskTier: isHigh
            ? { id: 'high', label: 'Alto Risco de Piora / Choque', color: 'rose', interpretation: 'Aumento expressivo de mortalidade (> 10%).' }
            : { id: 'low', label: 'Baixo Risco', color: 'emerald', interpretation: 'Mortalidade intra-hospitalar basal (< 3%).' },
          radarPoints: {
            respiratory: (inputs.rr_22 || inputs.respiratoryRate >= 22) ? 1.0 : 0.0,
            hemodynamic: (inputs.sbp_100 || (inputs.systolicBp <= 100)) ? 1.0 : 0.0,
            neurological: (inputs.ams_gcs || (inputs.glasgow < 15)) ? 1.0 : 0.0,
          },
          sscWarning: 'Surviving Sepsis Campaign 2021: Desaconselha-se o uso isolado do qSOFA como ferramenta única de triagem para exclusão de sepse.'
        };
      }

      case 'sofa': {
        const toScore = (v) => { const n = Number(v); return isNaN(n) ? 0 : n; };
        const resp = toScore(inputs.respiration);
        const coag = toScore(inputs.coagulation);
        const liv = toScore(inputs.liver);
        const card = toScore(inputs.cardiovascular);
        const cns = toScore(inputs.cns);
        const ren = toScore(inputs.renal);

        const score = resp + coag + liv + card + cns + ren;
        let tier;
        if (score <= 6) tier = { id: 'sofa_low', label: 'Baixa Gravidade (SOFA 0-6)', color: 'emerald' };
        else if (score <= 9) tier = { id: 'sofa_mod', label: 'Gravidade Moderada (SOFA 7-9)', color: 'amber' };
        else if (score <= 12) tier = { id: 'sofa_high', label: 'Alta Gravidade (SOFA 10-12)', color: 'orange' };
        else tier = { id: 'sofa_crit', label: 'Falência Crítica (SOFA ≥ 13)', color: 'rose' };

        return {
          score,
          riskTier: tier,
          radarPoints: {
            respiratory: Math.min(1.0, resp / 4),
            coagulation: Math.min(1.0, coag / 4),
            liver: Math.min(1.0, liv / 4),
            cardiovascular: Math.min(1.0, card / 4),
            neurological: Math.min(1.0, cns / 4),
            renal: Math.min(1.0, ren / 4),
          }
        };
      }

      case 'wells_pe': {
        let score = 0;
        if (inputs.dvt_signs) score += 3.0;
        if (inputs.pe_most_likely) score += 3.0;
        if (inputs.tachycardia || inputs.heartRate > 100) score += 1.5;
        if (inputs.immobilization) score += 1.5;
        if (inputs.previous_pe_dvt) score += 1.5;
        if (inputs.hemoptysis) score += 1.0;
        if (inputs.malignancy) score += 1.0;

        const isLikely = score > 4.0;
        const patientAge = inputs.age ?? 50;
        const dDimerCutoff = patientAge > 50 ? patientAge * 10 : 500;

        return {
          score,
          riskTier: isLikely
            ? { id: 'likely', label: 'TEP Provável (> 4.0 pontos)', color: 'rose', dDimerRecommended: false, angioTcRecommended: true }
            : { id: 'unlikely', label: 'TEP Improvável (≤ 4.0 pontos)', color: 'emerald', dDimerRecommended: true, dDimerCutoff, angioTcRecommended: false },
          radarPoints: {
            thrombotic_risk: Math.min(1.0, ((inputs.dvt_signs ? 3 : 0) + (inputs.previous_pe_dvt ? 1.5 : 0) + (inputs.malignancy ? 1 : 0)) / 6.0),
            hemodynamic_stress: Math.min(1.0, (inputs.tachycardia || inputs.heartRate > 100 ? 1.5 : 0) / 3.0),
            pulmonary_injury: Math.min(1.0, (inputs.hemoptysis ? 1 : 0) / 2.0),
          }
        };
      }

      case 'glasgow_p': {
        const gcs = Number(inputs.gcs ?? 15);
        const pupil = Number(inputs.pupilReactivity ?? 0); // 0 = both react, 1 = one reacts, 2 = neither reacts
        const score = Math.max(1, gcs - pupil);

        let tier;
        if (score >= 13) tier = { id: 'mild', label: 'Lesão Leve (GCS-P 13-15)', color: 'emerald' };
        else if (score >= 9) tier = { id: 'moderate', label: 'Lesão Moderada (GCS-P 9-12)', color: 'amber' };
        else tier = { id: 'severe', label: 'Lesão Grave (GCS-P 1-8)', color: 'rose' };

        return {
          score,
          gcs,
          pupilScore: pupil,
          riskTier: tier,
          radarPoints: {
            motor: Math.min(1.0, (6 - (inputs.gcsMotor ?? 6)) / 6),
            verbal: Math.min(1.0, (5 - (inputs.gcsVerbal ?? 5)) / 5),
            eye: Math.min(1.0, (4 - (inputs.gcsEye ?? 4)) / 4),
            brainstem: Math.min(1.0, pupil / 2),
          }
        };
      }

      case 'four_score': {
        const e = Number(inputs.eye ?? 4);
        const m = Number(inputs.motor ?? 4);
        const b = Number(inputs.brainstem ?? 4);
        const r = Number(inputs.respiration ?? 4);
        const score = e + m + b + r;

        let tier;
        if (score >= 13) tier = { id: 'low', label: 'Coma Superficial (FOUR 13-16)', color: 'emerald' };
        else if (score >= 9) tier = { id: 'moderate', label: 'Coma Moderado (FOUR 9-12)', color: 'amber' };
        else tier = { id: 'severe', label: 'Coma Grave (FOUR 0-8)', color: 'rose' };

        return {
          score,
          riskTier: tier,
          radarPoints: {
            eye: 1.0 - (e / 4),
            motor: 1.0 - (m / 4),
            brainstem: 1.0 - (b / 4),
            respiration: 1.0 - (r / 4),
          }
        };
      }

      case 'ranson': {
        let score = 0;
        const isBiliary = Boolean(inputs.isBiliary);

        // Admission criteria
        if (isBiliary ? (inputs.age > 70) : (inputs.age > 55)) score += 1;
        if (isBiliary ? (inputs.wbc > 18000) : (inputs.wbc > 16000)) score += 1;
        if (isBiliary ? (inputs.glucose > 220) : (inputs.glucose > 200)) score += 1;
        if (inputs.ast > 250) score += 1;
        if (isBiliary ? (inputs.ldh > 400) : (inputs.ldh > 350)) score += 1;

        // 48h criteria
        if (inputs.hctFall > 10) score += 1;
        const bunIncrease = inputs.bunRise ?? (inputs.ureiaRise ? inputs.ureiaRise / 2.14 : 0);
        if (bunIncrease > 5) score += 1;
        if (inputs.calcium < 8.0) score += 1;
        if (!isBiliary && inputs.pao2 && inputs.pao2 < 60) score += 1;
        if (inputs.baseDeficit > (isBiliary ? 5 : 4)) score += 1;
        if (inputs.fluidSequestration > (isBiliary ? 4 : 6)) score += 1;

        let tier;
        if (score <= 2) tier = { id: 'mild', label: 'Pancreatite Leve (0-2)', color: 'emerald', mortality: '~1%' };
        else if (score <= 5) tier = { id: 'moderate', label: 'Pancreatite Grave (3-5)', color: 'amber', mortality: '15%' };
        else tier = { id: 'severe', label: 'Pancreatite Necrotizante Crítica (≥ 6)', color: 'rose', mortality: '> 50%' };

        return {
          score,
          isBiliary,
          riskTier: tier,
          radarPoints: {
            metabolic: Math.min(1.0, ((inputs.glucose > 200 ? 1 : 0) + (inputs.calcium < 8.0 ? 1 : 0) + (inputs.baseDeficit > 4 ? 1 : 0)) / 3),
            inflammatory: Math.min(1.0, ((inputs.wbc > 16000 ? 1 : 0) + (inputs.ldh > 350 ? 1 : 0)) / 2),
            renal_fluid: Math.min(1.0, ((bunIncrease > 5 ? 1 : 0) + (inputs.fluidSequestration > 6 ? 1 : 0) + (inputs.hctFall > 10 ? 1 : 0)) / 3),
            respiratory: Math.min(1.0, (inputs.pao2 && inputs.pao2 < 60 ? 1 : 0)),
          }
        };
      }

      case 'bisap': {
        let score = 0;
        const bunVal = inputs.bun ?? (inputs.ureia ? inputs.ureia / 2.14 : 0);
        if (bunVal > 25) score += 1;
        if (inputs.impairedMental || inputs.gcs < 15) score += 1;
        if (inputs.sirsCriteria >= 2 || inputs.sirs) score += 1;
        if (inputs.age > 60) score += 1;
        if (inputs.pleuralEffusion) score += 1;

        const tier = score <= 2
          ? { id: 'low', label: 'Baixo Risco (0-2 pontos)', color: 'emerald', mortality: '< 2%' }
          : { id: 'high', label: 'Alto Risco (3-5 pontos)', color: 'rose', mortality: '5-22%' };

        return {
          score,
          riskTier: tier,
          radarPoints: {
            renal: bunVal > 25 ? 1.0 : 0.0,
            neurological: (inputs.impairedMental || inputs.gcs < 15) ? 1.0 : 0.0,
            systemic_sirs: (inputs.sirsCriteria >= 2 || inputs.sirs) ? 1.0 : 0.0,
            age_factor: inputs.age > 60 ? 1.0 : 0.0,
            pulmonary_effusion: inputs.pleuralEffusion ? 1.0 : 0.0,
          }
        };
      }

      default:
        throw new Error(`Unknown score ID: ${scoreId}`);
    }
  }

  // Feature 7: Infusion BIC Engine
  calculateInfusion(params) {
    const { drugId, patientWeightKg, doseValue, concentrationMcgPerMl, concentrationUiPerMl } = params;

    if (patientWeightKg !== undefined && patientWeightKg <= 0) {
      throw new Error('Patient weight must be greater than zero');
    }

    const alerts = [];
    let rateMlPerHour = 0;
    let recommendedVehicle = 'SG 5%';
    let containerAlert = null;
    let formattedDose = '';

    switch (drugId) {
      case 'norepinephrine': {
        if (concentrationMcgPerMl !== undefined && concentrationMcgPerMl <= 0) {
          throw new Error('Concentration must be positive');
        }
        const conc = concentrationMcgPerMl || 64; // default 16mg in 250mL = 64 mcg/mL
        const weight = patientWeightKg || 70;
        rateMlPerHour = (doseValue * weight * 60) / conc;
        recommendedVehicle = 'Soro Glicosado 5% (SG 5%)';
        formattedDose = `${doseValue} mcg/kg/min`;

        if (doseValue > 0.25) {
          alerts.push('Alerta Refratariedade: Dose > 0.25 mcg/kg/min. Indicação formal de associar Vasopressina como 2º vasopressor.');
        }
        alerts.push('Veículo Mandatório: Diluir preferencialmente em SG 5% (previne oxidação da catecolamina). Acesso Venoso Central mandatório.');
        break;
      }

      case 'vasopressin': {
        if (concentrationUiPerMl !== undefined && concentrationUiPerMl <= 0) {
          throw new Error('Concentration must be positive');
        }
        const conc = concentrationUiPerMl || 0.2; // default 20 UI in 100mL = 0.2 UI/mL
        rateMlPerHour = (doseValue * 60) / conc;
        recommendedVehicle = 'SF 0.9% ou SG 5%';
        formattedDose = `${doseValue} UI/min`;

        if (doseValue < 0.01 || doseValue > 0.04) {
          alerts.push('Atenção: A dose recomendada de Vasopressina no choque séptico é fixa entre 0.01 e 0.04 UI/min. Não titular indiscriminadamente.');
        }
        break;
      }

      case 'dobutamine': {
        if (concentrationMcgPerMl !== undefined && concentrationMcgPerMl <= 0) {
          throw new Error('Concentration must be positive');
        }
        const conc = concentrationMcgPerMl || 1000; // default 250mg in 250mL = 1000 mcg/mL
        const weight = patientWeightKg || 70;
        rateMlPerHour = (doseValue * weight * 60) / conc;
        recommendedVehicle = 'SG 5% ou SF 0.9%';
        formattedDose = `${doseValue} mcg/kg/min`;

        if (doseValue > 20) {
          alerts.push('Dose Máxima Ultrapassada: Doses > 20 mcg/kg/min aumentam risco grave de taquiarritmias e vasodilatação reflexa.');
        }
        break;
      }

      case 'nitroglycerin': {
        if (concentrationMcgPerMl !== undefined && concentrationMcgPerMl <= 0) {
          throw new Error('Concentration must be positive');
        }
        const conc = concentrationMcgPerMl || 200; // default 50mg in 250mL = 200 mcg/mL
        if (conc <= 0) throw new Error('Concentration must be positive');
        rateMlPerHour = (doseValue * 60) / conc;
        recommendedVehicle = 'SG 5% ou SF 0.9%';
        containerAlert = 'Recipiente Mandatório: Frasco de Vidro ou Polietileno/Poliolefina com equipo próprio de polietileno. PROIBIDO frasco ou equipo de PVC comum (adsorção de até 80% no plástico).';
        alerts.push(containerAlert);
        formattedDose = `${doseValue} mcg/min`;
        break;
      }

      default:
        throw new Error(`Unsupported drug ID: ${drugId}`);
    }

    return {
      drugId,
      rateMlPerHour: Number(rateMlPerHour.toFixed(2)),
      recommendedVehicle,
      containerAlert,
      safetyAlerts: alerts,
      formattedDose
    };
  }

  // Feature 8: Physiological Radar Engine
  calculateRadarGeometry(axes, values, size = 300) {
    const cx = size / 2;
    const cy = size / 2;
    const radius = (size / 2) * 0.8;
    const n = axes.length;

    const angleStep = (2 * Math.PI) / n;
    const axisPoints = [];
    const baselinePoints = [];
    const patientPoints = [];

    axes.forEach((axis, i) => {
      const angle = i * angleStep - Math.PI / 2;
      const xMax = cx + radius * Math.cos(angle);
      const yMax = cy + radius * Math.sin(angle);
      axisPoints.push({ id: axis.id, label: axis.label, angle, x: xMax, y: yMax });

      // Baseline is normal homeostasis (0)
      const baseVal = 0.15; // small aesthetic offset for visibility
      const xBase = cx + radius * baseVal * Math.cos(angle);
      const yBase = cy + radius * baseVal * Math.sin(angle);
      baselinePoints.push(`${xBase.toFixed(1)},${yBase.toFixed(1)}`);

      // Patient deviation: clamp to [0, 1]
      const rawVal = values[axis.id] ?? 0;
      const normalized = Math.max(0, Math.min(1.0, isNaN(rawVal) ? 0 : rawVal));
      const effectiveRadius = radius * (0.15 + 0.85 * normalized);
      const xPat = cx + effectiveRadius * Math.cos(angle);
      const yPat = cy + effectiveRadius * Math.sin(angle);
      patientPoints.push(`${xPat.toFixed(1)},${yPat.toFixed(1)}`);
    });

    return {
      size,
      cx,
      cy,
      radius,
      axisCount: n,
      axisPoints,
      baselinePolygon: baselinePoints.join(' '),
      patientPolygon: patientPoints.join(' ')
    };
  }

  // Feature 9: PEP/EHR Plain-Text Export Engine
  exportPepSummary(params) {
    const {
      calculatorName,
      scoreValue,
      riskLabel,
      riskInterpretation,
      patientBed = 'Não informado',
      patientWeight = 70,
      infusionInfo = null,
      recommendations = []
    } = params;

    const now = new Date();
    const dateStr = `${String(now.getDate()).padStart(2, '0')}/${String(now.getMonth() + 1).padStart(2, '0')}/${now.getFullYear()}`;
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

    let text = `[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]\n`;
    text += `DATA/HORA: ${dateStr} - ${timeStr}\n`;
    text += `PACIENTE: ${patientBed} | Peso: ${patientWeight} kg\n\n`;

    text += `S (Subjetivo): Paciente sob vigilância intensiva / emergencial.\n`;
    text += `O (Objetivo):\n`;
    text += `- Escore Calculado: ${calculatorName} = ${scoreValue} pontos\n`;
    text += `- Estratificação de Risco: ${riskLabel}\n`;
    if (riskInterpretation) {
      text += `- Interpretação: ${riskInterpretation}\n`;
    }

    text += `\nA (Avaliação): Deterioração fisiológica conforme protocolo CDSS.\n`;
    text += `P (Plano / Condutas):\n`;

    if (recommendations && recommendations.length > 0) {
      recommendations.forEach((rec, idx) => {
        text += `${idx + 1}. ${rec}\n`;
      });
    }

    if (infusionInfo) {
      const nextNum = (recommendations ? recommendations.length : 0) + 1;
      text += `${nextNum}. Bomba de Infusão Contínua (BIC):\n`;
      text += `   - Droga: ${infusionInfo.drugName}\n`;
      text += `   - Diluição: ${infusionInfo.dilution}\n`;
      text += `   - Dose: ${infusionInfo.dose}\n`;
      text += `   - Vazão em BIC: ${infusionInfo.rateMlPerHour} mL/h\n`;
      text += `   - Veículo: ${infusionInfo.vehicle}\n`;
      if (infusionInfo.containerAlert) {
        text += `   - Atenção: ${infusionInfo.containerAlert}\n`;
      }
    }

    text += `\n[Aviso de Segurança: Suporte à decisão clínica informada. Não substitui o julgamento médico presencial.]\n`;

    return text;
  }

  // Feature 11: Local Storage Service (IndexedDB)
  createStorageService() {
    const dbPromise = this.env.indexedDB.openDB('scoreboard_db', 1, {
      upgrade(db) {
        db.createObjectStore('quick_pins', { keyPath: 'id' });
        db.createObjectStore('beds', { keyPath: 'id' });
      }
    });

    const PII_REGEX = /\b(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})\b/g;

    return {
      async getFavorites() {
        const db = await dbPromise;
        const pins = await db.getAll('quick_pins');
        return pins.map(p => p.id);
      },

      async toggleFavorite(scoreId) {
        const db = await dbPromise;
        const exists = await db.get('quick_pins', scoreId);
        if (exists) {
          await db.delete('quick_pins', scoreId);
          return false;
        } else {
          await db.put('quick_pins', { id: scoreId, pinnedAt: new Date().toISOString() });
          return true;
        }
      },

      async isFavorite(scoreId) {
        const db = await dbPromise;
        const item = await db.get('quick_pins', scoreId);
        return Boolean(item);
      },

      async saveBedRecord(record) {
        // Zero LGPD validation
        if (record.bedLabel && PII_REGEX.test(record.bedLabel)) {
          throw new Error('LGPD Violation: CPF or personal identifier detected in bed record');
        }
        if (record.patientName || record.cpf || record.medicalRecordNumber) {
          throw new Error('LGPD Violation: Patient identifying data is prohibited');
        }

        const db = await dbPromise;
        await db.put('beds', {
          id: record.id,
          bedLabel: record.bedLabel || 'Leito Sem Identificação',
          notes: record.notes || '',
          scoreSnapshots: record.scoreSnapshots || [],
          updatedAt: new Date().toISOString()
        });
      },

      async getBedRecords() {
        const db = await dbPromise;
        return await db.getAll('beds');
      }
    };
  }

  // Feature 12: Instant Search (<10ms)
  searchCalculators(query, manifest) {
    const start = performance.now();
    const cleanQuery = query.toLowerCase().trim().replace(/\s+/g, ' ').normalize('NFD').replace(/[\u0300-\u036f]/g, '');

    const target = manifest || this.getManifestData();
    const list = Array.isArray(target) ? target : (target && target.calculators ? target.calculators : []);

    if (!cleanQuery) {
      return {
        results: list,
        latencyMs: performance.now() - start
      };
    }

    const results = list.filter(calc => {
      const name = (calc.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const acronym = (calc.acronym || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const category = (calc.category || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const desc = (calc.description || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

      if (name.includes(cleanQuery) || acronym.includes(cleanQuery) || category.includes(cleanQuery) || desc.includes(cleanQuery)) {
        return true;
      }

      if (Array.isArray(calc.synonyms)) {
        return calc.synonyms.some(syn => {
          const normSyn = syn.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
          return normSyn.includes(cleanQuery);
        });
      }

      return false;
    });

    const latencyMs = performance.now() - start;
    return { results, latencyMs };
  }

  // Feature 13: iOS-Style Alphabet Jump Rail
  getJumpRailLetters() {
    return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  }

  calculateJumpRailTouch(touchY, railTop, railHeight) {
    const letters = this.getJumpRailLetters();
    if (railHeight <= 0) return letters[0];

    const clampedY = Math.max(railTop, Math.min(railTop + railHeight - 1, touchY));
    const relativeY = clampedY - railTop;
    const itemHeight = railHeight / letters.length;
    const index = Math.floor(relativeY / itemHeight);
    const letter = letters[Math.min(letters.length - 1, Math.max(0, index))];

    return {
      index,
      letter,
      vibratePattern: 10 // haptic feedback 10ms
    };
  }

  // Feature 14: A-Z Score List & Sticky Headers
  groupScoresAlphabetically(scores) {
    const groups = {};
    const sorted = [...scores].sort((a, b) => a.name.localeCompare(b.name, 'pt-BR'));

    for (const score of sorted) {
      const letter = score.name.trim()[0].toUpperCase();
      if (!groups[letter]) groups[letter] = [];
      groups[letter].push(score);
    }

    return Object.keys(groups).sort().map(letter => ({
      letter,
      items: groups[letter]
    }));
  }
}

export const adapter = new ScoreboardAdapter();
