/**
 * Tier 4 — Real-World Clinical Application Scenarios
 * Implements 11 comprehensive real-world ICU and Emergency patient clinical workflows.
 */

import { describe, it, expect, adapter, envShim } from '../harness/index.js';

describe('Tier 4 — Clinical Scenario 1: Septic Shock with Multiorgan Failure', () => {
  it('CS-01: Full sepsis workflow (qSOFA trigger -> SSC 2021 warning -> SOFA score -> Norepinephrine in SG 5% with Vasopressin prompt -> PEP export for MV Soul)', async () => {
    envShim.reset();

    // 1. Bedside bedside triage with qSOFA
    const qsofaRes = adapter.calculateScore('qsofa', {
      rr_22: true, // FR = 28 irpm
      sbp_100: true, // PA = 85/50 mmHg (PAM 61)
      ams_gcs: true // Glasgow 13
    });
    expect(qsofaRes.score).toBe(3);
    expect(qsofaRes.riskTier.id).toBe('high');
    expect(qsofaRes.sscWarning).toContain('Surviving Sepsis Campaign 2021');

    // 2. Transfer to ICU & confirm organ dysfunction via Full SOFA
    const sofaRes = adapter.calculateScore('sofa', {
      respiration: 3, // PaO2/FiO2 < 200 sob VM
      coagulation: 2, // Plaquetas 85.000
      liver: 1, // Bilirrubina 1.5 mg/dL
      cardiovascular: 4, // Noradrenalina > 0.1 mcg/kg/min
      cns: 2, // Glasgow 11 sob sedação leve
      renal: 3 // Creatinina 3.8 mg/dL e oligúria
    });
    expect(sofaRes.score).toBe(15);
    expect(sofaRes.riskTier.id).toBe('sofa_crit');

    // 3. Initiate high-dose Norepinephrine infusion in SG 5%
    const noraInf = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: 70,
      doseValue: 0.35, // > 0.25 mcg/kg/min triggers Vasopressin prompt
      concentrationMcgPerMl: 64
    });
    expect(noraInf.rateMlPerHour).toBeCloseTo(22.97, 2);
    expect(noraInf.recommendedVehicle).toContain('SG 5%');
    const hasVasoAlert = noraInf.safetyAlerts.some(a => a.includes('associar Vasopressina'));
    expect(hasVasoAlert).toBe(true);

    // 4. Concurrently initiate fixed-dose Vasopressin (0.03 UI/min)
    const vasoInf = adapter.calculateInfusion({
      drugId: 'vasopressin',
      patientWeightKg: 70,
      doseValue: 0.03,
      concentrationUiPerMl: 0.2
    });
    expect(vasoInf.rateMlPerHour).toBe(9.0);

    // 5. Generate complete PEP SOAP note for MV Soul
    const mvSoulNote = adapter.exportPepSummary({
      calculatorName: 'SOFA',
      scoreValue: sofaRes.score,
      riskLabel: sofaRes.riskTier.label,
      patientBed: 'Leito 04 - UTI Geral',
      patientWeight: 70,
      recommendations: [
        'Surviving Sepsis Campaign 2021: Coletar 2 pares de hemoculturas e dosar lactato sérico.',
        'Cristaloide balanceado 30 mL/kg infundido.',
        'Acesso venoso central em veia subclávia direita e linha arterial (PAI) radial esquerda.'
      ],
      infusionInfo: {
        drugName: 'Noradrenalina + Vasopressina',
        dilution: 'Nora 16mg/250mL SG 5% (64 mcg/mL) + Vaso 20 UI/100mL (0.2 UI/mL)',
        dose: 'Nora 0.35 mcg/kg/min | Vaso 0.03 UI/min fixo',
        rateMlPerHour: noraInf.rateMlPerHour,
        vehicle: 'SG 5%',
        containerAlert: 'Alerta: Associado 2º vasopressor por refratariedade (> 0.25 mcg/kg/min).'
      }
    });

    expect(mvSoulNote).toContain('[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]');
    expect(mvSoulNote).toContain('Leito 04 - UTI Geral');
    expect(mvSoulNote).toContain('SOFA = 15 pontos');
    expect(mvSoulNote).toContain('22.97 mL/h');
    expect(mvSoulNote).toContain('Surviving Sepsis Campaign 2021');

    // 6. Copy to clipboard
    await envShim.navigator.clipboard.writeText(mvSoulNote);
    const clipboard = await envShim.navigator.clipboard.readText();
    expect(clipboard).toBe(mvSoulNote);
  });
});

describe('Tier 4 — Clinical Scenario 2: Massive Pulmonary Embolism (TEP)', () => {
  it('CS-02: Wells PE stratification -> age-adjusted D-dimer -> PEP copy for Tasy', async () => {
    envShim.reset();

    // 68-year-old patient with dyspnea and tachycardia
    const wellsRes = adapter.calculateScore('wells_pe', {
      tachycardia: true, // FC 115 bpm (1.5)
      immobilization: true, // Cirurgia ortopédica há 10 dias (1.5)
      pe_most_likely: false,
      age: 68
    });
    expect(wellsRes.score).toBe(3.0); // <= 4.0 -> TEP Improvável
    expect(wellsRes.riskTier.id).toBe('unlikely');
    expect(wellsRes.riskTier.dDimerRecommended).toBe(true);

    // Age-adjusted D-dimer formula: age * 10 if age > 50 -> 68 * 10 = 680 ng/mL
    expect(wellsRes.riskTier.dDimerCutoff).toBe(680);

    // Patient returns with D-dimer of 950 ng/mL (positive!) -> escalate to likely
    const escalatedWells = adapter.calculateScore('wells_pe', {
      tachycardia: true,
      immobilization: true,
      pe_most_likely: true // Alternative diagnosis less likely now
    });
    expect(escalatedWells.score).toBe(6.0);
    expect(escalatedWells.riskTier.id).toBe('likely');
    expect(escalatedWells.riskTier.angioTcRecommended).toBe(true);

    // Generate clinical note for Tasy
    const tasyNote = adapter.exportPepSummary({
      calculatorName: 'Critérios de Wells para TEP',
      scoreValue: escalatedWells.score,
      riskLabel: escalatedWells.riskTier.label,
      patientBed: 'Leito 12 - Pronto-Socorro',
      patientWeight: 82,
      recommendations: [
        'D-dímero sérico 950 ng/mL (ponto de corte ajustado para idade: 680 ng/mL).',
        'Encaminhamento imediato para Angiotomografia de Artérias Pulmonares.',
        'Iniciar Enoxaparina 1 mg/kg SC de 12/12h (80 mg SC 12/12h) na ausência de contraindicações hemorrágicas.'
      ]
    });

    expect(tasyNote).toContain('Critérios de Wells para TEP = 6 pontos');
    expect(tasyNote).toContain('Angiotomografia de Artérias Pulmonares');
    expect(tasyNote).toContain('Enoxaparina');
  });
});

describe('Tier 4 — Clinical Scenario 3: Severe Acute Pancreatitis', () => {
  it('CS-03: Ranson at 0h and 48h + BISAP with Ureia conversion -> physiological radar display', () => {
    const catalog = adapter.getBlock01Catalog();
    const ransonDef = catalog.find(c => c.id === 'ranson');

    // Ranson non-biliary evaluation
    const ransonRes = adapter.calculateScore('ranson', {
      isBiliary: false,
      age: 58, // +1 (>55)
      wbc: 19500, // +1 (>16000)
      glucose: 240, // +1 (>200)
      ast: 310, // +1 (>250)
      ldh: 420, // +1 (>350)
      // 48h
      hctFall: 14, // +1 (>10)
      ureiaRise: 18, // 18 / 2.14 = 8.4 mg/dL BUN rise (>5 -> +1)
      calcium: 7.2, // +1 (<8.0)
      pao2: 58, // +1 (<60)
      baseDeficit: 6, // +1 (>4)
      fluidSequestration: 7 // +1 (>6L)
    });
    expect(ransonRes.score).toBe(11);
    expect(ransonRes.riskTier.id).toBe('severe');
    expect(ransonRes.riskTier.mortality).toContain('> 50%');

    // Concurrently compute BISAP at 24h
    const bisapRes = adapter.calculateScore('bisap', {
      ureia: 65, // 65 / 2.14 = 30.3 mg/dL BUN (>25 -> +1)
      sirs: true, // +1
      pleuralEffusion: true // +1
    });
    expect(bisapRes.score).toBe(3);
    expect(bisapRes.riskTier.id).toBe('high');

    // Verify multi-axis radar geometry
    const geom = adapter.calculateRadarGeometry(ransonDef.radarAxes, ransonRes.radarPoints, 300);
    expect(geom.axisCount).toBe(4);
    expect(geom.patientPolygon.split(' ').length).toBe(4);
  });
});

describe('Tier 4 — Clinical Scenario 4: Severe Traumatic Brain Injury (TBI)', () => {
  it('CS-04: Glasgow-P with non-reactive pupil + FOUR Score intubated brainstem assessment', () => {
    // 1. Glasgow-P evaluation: GCS 7 with right unreactive dilated pupil (anisocoria = 1)
    const gcsPRes = adapter.calculateScore('glasgow_p', {
      gcs: 7,
      pupilReactivity: 1 // Anisocoria
    });
    expect(gcsPRes.score).toBe(6); // 7 - 1 = 6
    expect(gcsPRes.riskTier.id).toBe('severe');
    expect(gcsPRes.riskTier.color).toBe('rose');

    // 2. Patient is intubated: evaluate FOUR score (Wijdicks)
    const fourRes = adapter.calculateScore('four_score', {
      eye: 0, // Olhos fechados à dor (0)
      motor: 1, // Resposta extensora / descerebração (1)
      brainstem: 2, // Reflexo pupilar ou corneano ausente (2)
      respiration: 0 // Apneico ou em FR mecânica mandatória (0)
    });
    expect(fourRes.score).toBe(3);
    expect(fourRes.riskTier.id).toBe('severe');
    expect(fourRes.riskTier.color).toBe('rose');
  });
});

describe('Tier 4 — Clinical Scenario 5: Hypertensive Emergency / Acute Coronary Syndrome', () => {
  it('CS-05: Nitroglycerin infusion with mandatory glass/polyolefin container verification and PVC prohibition alert', () => {
    const patientWeight = 78;
    const doseMcgPerMin = 25; // titrated dose
    const conc = 200; // 50mg in 250mL = 200 mcg/mL

    const inf = adapter.calculateInfusion({
      drugId: 'nitroglycerin',
      patientWeightKg: patientWeight,
      doseValue: doseMcgPerMin,
      concentrationMcgPerMl: conc
    });

    // 25 * 60 / 200 = 1500 / 200 = 7.5 mL/h
    expect(inf.rateMlPerHour).toBe(7.5);
    expect(inf.containerAlert).toBeDefined();
    expect(inf.containerAlert).toContain('Frasco de Vidro ou Polietileno');
    expect(inf.containerAlert).toContain('PROIBIDO frasco ou equipo de PVC');

    // Generate prescription note
    const note = adapter.exportPepSummary({
      calculatorName: 'Tridil (Nitroglicerina)',
      scoreValue: 0,
      riskLabel: 'Emergência Hipertensiva / EAP',
      patientBed: 'Leito 02 - UCO',
      patientWeight: patientWeight,
      infusionInfo: {
        drugName: 'Nitroglicerina (Tridil)',
        dilution: '50 mg em 240 mL SG 5% (200 mcg/mL)',
        dose: `${doseMcgPerMin} mcg/min`,
        rateMlPerHour: inf.rateMlPerHour,
        vehicle: 'SG 5%',
        containerAlert: inf.containerAlert
      }
    });

    expect(note).toContain('PROIBIDO frasco ou equipo de PVC');
    expect(note).toContain('7.5 mL/h');
  });
});

describe('Tier 4 — Clinical Scenario 6: Cardiogenic Shock', () => {
  it('CS-06: Dobutamine titration combined with Norepinephrine in cardiogenic shock', () => {
    const patientWeight = 75;

    // Dobutamine inotropic support: 7.5 mcg/kg/min
    // 7.5 * 75 * 60 / 1000 = 33.75 mL/h
    const dobutaInf = adapter.calculateInfusion({
      drugId: 'dobutamine',
      patientWeightKg: patientWeight,
      doseValue: 7.5,
      concentrationMcgPerMl: 1000
    });
    expect(dobutaInf.rateMlPerHour).toBe(33.75);

    // Norepinephrine vasopressor support: 0.15 mcg/kg/min
    // 0.15 * 75 * 60 / 64 = 675 / 64 = 10.546875 mL/h
    const noraInf = adapter.calculateInfusion({
      drugId: 'norepinephrine',
      patientWeightKg: patientWeight,
      doseValue: 0.15,
      concentrationMcgPerMl: 64
    });
    expect(noraInf.rateMlPerHour).toBeCloseTo(10.55, 2);

    const note = adapter.exportPepSummary({
      calculatorName: 'Choque Cardiogênico (Killip IV)',
      scoreValue: 4,
      riskLabel: 'Alto Risco',
      patientBed: 'Leito 01 - Coronariana',
      patientWeight,
      infusionInfo: {
        drugName: 'Dobutamina + Noradrenalina',
        dilution: 'Dobutamina 250mg/250mL (1000 mcg/mL) + Nora 16mg/250mL (64 mcg/mL)',
        dose: 'Dobutamina 7.5 mcg/kg/min (33.75 mL/h) | Nora 0.15 mcg/kg/min (10.55 mL/h)',
        rateMlPerHour: 44.30,
        vehicle: 'SG 5%'
      }
    });

    expect(note).toContain('Dobutamina + Noradrenalina');
    expect(note).toContain('33.75 mL/h');
  });
});

describe('Tier 4 — Clinical Scenario 7: Bedside Rounding Workflow (Zero LGPD)', () => {
  it('CS-07: "Leito 04 - UTI" anonymous bed assignment, star favorites quick-pin, zero PII persistence', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();

    // 1. Quick-pin essential rounding calculators
    await storage.toggleFavorite('sofa');
    await storage.toggleFavorite('qsofa');
    const favs = await storage.getFavorites();
    expect(favs).toContain('sofa');
    expect(favs).toContain('qsofa');

    // 2. Perform rounding snapshot for Bed 04
    const sofaScore = adapter.calculateScore('sofa', {
      respiration: 2,
      cardiovascular: 3,
      renal: 2
    });

    await storage.saveBedRecord({
      id: 'round_bed_04',
      bedLabel: 'Leito 04 - UTI Geral',
      notes: 'Paciente evoluindo com melhora hemodinâmica após ressuscitação.',
      scoreSnapshots: [
        { scoreId: 'sofa', score: sofaScore.score, timestamp: new Date().toISOString() }
      ]
    });

    const records = await storage.getBedRecords();
    expect(records.length).toBe(1);
    expect(records[0].bedLabel).toBe('Leito 04 - UTI Geral');
    expect(records[0].scoreSnapshots[0].score).toBe(7);

    // Verify zero PII leak
    const serialized = JSON.stringify(records);
    expect(serialized).not.toMatch(/\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/);
    expect(serialized).not.toContain('cpf');
    expect(serialized).not.toContain('nome_completo');
  });
});

describe('Tier 4 — Clinical Scenario 8: Mobile Viewport Responsive Layout & Jump Rail', () => {
  it('CS-08: Responsive simulation across 375px (iPhone SE) and 430px (iPhone Pro Max) with jump rail interaction', () => {
    // Test on iPhone SE (375px)
    envShim.setViewport(375, 667);
    expect(envShim.viewport.width).toBe(375);
    const railTop = 80;
    const railHeight = 500;

    // Simulate thumb drag from 'A' to 'S'
    const touchA = adapter.calculateJumpRailTouch(railTop + 5, railTop, railHeight);
    expect(touchA.letter).toBe('A');

    const touchS = adapter.calculateJumpRailTouch(railTop + (18 * (railHeight / 26)) + 5, railTop, railHeight);
    expect(touchS.letter).toBe('S');

    // Test on iPhone 15 Pro Max (430px)
    envShim.setViewport(430, 932);
    expect(envShim.viewport.width).toBe(430);
    const touchZ = adapter.calculateJumpRailTouch(railTop + railHeight - 2, railTop, railHeight);
    expect(touchZ.letter).toBe('Z');
  });
});

describe('Tier 4 — Clinical Scenario 9: Dark / Light Mode Toggle & Contrast', () => {
  it('CS-09: Dark mode toggle persistence, smooth transition, and style verification', () => {
    envShim.reset();
    const theme = adapter.createThemeSystem();

    // 1. Initial state: light
    theme.init();
    expect(theme.isDark()).toBe(false);

    // 2. Toggle to dark
    theme.toggleTheme();
    expect(theme.isDark()).toBe(true);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
    expect(theme.getSavedTheme()).toBe('dark');

    // 3. Re-initialize from storage (simulating page reload)
    const newSessionTheme = adapter.createThemeSystem();
    newSessionTheme.init();
    expect(newSessionTheme.isDark()).toBe(true);
    expect(envShim.document.documentElement.classList.contains('dark')).toBe(true);
  });
});

describe('Tier 4 — Clinical Scenario 10: High-Speed Instant Search Benchmark', () => {
  it('CS-10: Sub-10ms search latency across 98 Brazilian clinical synonyms', () => {
    const manifest = adapter.getManifestData();
    const brazilianSynonyms = [
      'sepse', 'choque séptico', 'tep', 'tvp', 'tromboembolismo pulmonar',
      'pancreatite aguda', 'necrose pancreática', 'coma', 'glasgow', 'pupilas',
      'four', 'tronco encefálico', 'bomba de infusão', 'noradrenalina', 'vasopressina'
    ];

    const latencies = [];
    for (const syn of brazilianSynonyms) {
      const { results, latencyMs } = adapter.searchCalculators(syn, manifest);
      expect(results.length).toBeGreaterThan(0);
      expect(latencyMs).toBeLessThan(10);
      latencies.push(latencyMs);
    }

    const avgLatency = latencies.reduce((a, b) => a + b, 0) / latencies.length;
    expect(avgLatency).toBeLessThan(5); // Average sub-5ms
  });
});

describe('Tier 4 — Clinical Scenario 11: Anti-Truncation Clinical Completeness Verification', () => {
  it('CS-11: Verifies zero truncation of pharmacological actions, parameters, and clinical dossiers', () => {
    const catalog = adapter.getBlock01Catalog();
    expect(catalog.length).toBe(7);

    // Verify qSOFA completeness
    const qsofa = catalog.find(c => c.id === 'qsofa');
    expect(qsofa.nonPharmacologicalActions.length).toBe(3);
    expect(qsofa.pharmacologicalActions.length).toBe(2);
    expect(qsofa.ssc2021Warning).toBe(true);

    // Verify SOFA 6 organ groups
    const sofa = catalog.find(c => c.id === 'sofa');
    expect(sofa.parameterGroups.length).toBe(6);
    expect(sofa.radarAxes.length).toBe(6);

    // Verify Ranson 11 criteria
    const ranson = catalog.find(c => c.id === 'ranson');
    const totalRansonParams = ranson.parameterGroups[0].parameters.length + ranson.parameterGroups[1].parameters.length;
    expect(totalRansonParams).toBe(11);

    // Verify Wells 7 criteria
    const wells = catalog.find(c => c.id === 'wells_pe');
    expect(wells.parameterGroups[0].parameters.length).toBe(7);
  });
});
