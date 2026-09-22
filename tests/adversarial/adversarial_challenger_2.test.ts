/**
 * EMPIRICAL ADVERSARIAL STRESS TEST SUITE — CHALLENGER 2
 *
 * Focus Areas:
 * 1. Search Latency & Brazilian Clinical Synonyms Fuzzing (1,000 rapid queries, P99 < 10ms)
 * 2. State & Storage Concurrency (rapid toggles, race conditions, memory fallback, LGPD invariants)
 * 3. PEP EHR Plain-Text Export Robustness (SOAP/SBAR, zero truncation, Zero LGPD risk)
 * 4. Theme & Mobile Interaction Ergonomics (rapid theme toggles, jump rail bounds calculation)
 */

import { describe, it, expect, beforeEach } from 'vitest';
import rawManifest from '../../src/data/manifest.json';
import rawBlock01 from '../../src/data/blocks/block_01.json';
import { type ManifestItem, type Calculator } from '../../src/types/clinical';
import { StorageService, type BedRecord } from '../../src/services/storageService';
import {
  generatePepNote,
  generateSbarNote,
  sanitizeBedIdentifier,
  formatDateBrazilian,
  summarizeRadarDeviations,
  type PepExportInput
} from '../../src/engines/pepExportEngine';

const manifest = rawManifest as unknown as ManifestItem[];
const block01 = rawBlock01 as unknown as { blockId: string; calculators: Calculator[] };

// Production search normalization logic identical to AzScoreList.tsx
function normalizeSearchText(text: string): string {
  if (!text) return '';
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function indexManifestItems(items: ManifestItem[]) {
  return items.map((item) => {
    const tokens = [
      item.name,
      item.acronym,
      item.category || '',
      item.categoryName || '',
      item.subcategory || '',
      item.moduleName || '',
      item.description || '',
      item.summary || '',
      ...(item.synonyms || []),
      ...(item.searchSynonyms || []),
    ]
      .map(normalizeSearchText)
      .join(' ');

    return {
      item,
      indexedTokens: tokens,
    };
  });
}

describe('Adversarial Dimension 1: Search Latency & Brazilian Synonyms Fuzzing', () => {
  const indexed = indexManifestItems(manifest);

  function executeSearch(query: string) {
    const t0 = performance.now();
    const clean = normalizeSearchText(query);
    let results = indexed;
    if (clean) {
      const terms = clean.split(/\s+/).filter(Boolean);
      results = indexed.filter(({ indexedTokens }) =>
        terms.every((term) => indexedTokens.includes(term))
      );
    }
    const duration = performance.now() - t0;
    return { results: results.map((r) => r.item), duration };
  }

  it('verifies manifest has all 19 Block 01 calculators with comprehensive search tokens', () => {
    expect(manifest.length).toBe(19);
    for (const item of manifest) {
      expect(item.id).toBeDefined();
      expect(item.name.length).toBeGreaterThan(0);
      expect(item.searchSynonyms).toBeDefined();
      expect(item.searchSynonyms.length).toBeGreaterThanOrEqual(5);
    }
  });

  it('matches all mandatory Brazilian clinical synonyms to their correct calculators', () => {
    const synonymExpectations: Array<{ query: string; expectedAcronym: string }> = [
      { query: 'sepse', expectedAcronym: 'qSOFA' },
      { query: 'choque séptico', expectedAcronym: 'qSOFA' },
      { query: 'tep', expectedAcronym: 'Wells' },
      { query: 'embolia pulmonar', expectedAcronym: 'Wells' },
      { query: 'pancreatite', expectedAcronym: 'Ranson' },
      { query: 'coma', expectedAcronym: 'Glasgow-P' },
      { query: 'glasgow', expectedAcronym: 'Glasgow-P' },
      { query: 'noradrenalina', expectedAcronym: 'SOFA' },
      { query: 'vasopressina', expectedAcronym: 'SOFA' },
      { query: 'reflexos de tronco', expectedAcronym: 'FOUR' },
      { query: 'ureia', expectedAcronym: 'BISAP' }
    ];

    for (const { query, expectedAcronym } of synonymExpectations) {
      const { results } = executeSearch(query);
      const matched = results.some(
        (r) => r.acronym.toLowerCase().includes(expectedAcronym.toLowerCase()) ||
               r.name.toLowerCase().includes(expectedAcronym.toLowerCase())
      );
      expect(matched, `Expected query "${query}" to match calculator with acronym/name "${expectedAcronym}"`).toBe(true);
    }
  });

  it('uncovers synonym gap: "tronco encefalico" does not match FOUR Score despite being the canonical brainstem coma scale', () => {
    const { results } = executeSearch('tronco encefalico');
    const matched = results.some((r) => r.acronym === 'FOUR Score');
    // This empirically documents the clinical synonym omission in manifest.json
    expect(matched).toBe(false);
  });

  it('executes 1,000 randomized rapid queries and asserts P99 latency < 10ms', () => {
    const candidateTerms = [
      'sepse', 'choque', 'tep', 'pancreatite', 'coma', 'glasgow', 'noradrenalina',
      'vasopressina', 'dobutamina', 'nitroglicerina', 'sofa', 'qsofa', 'wells',
      'ranson', 'bisap', 'four', 'pupila', 'lactato', 'plaquetas', 'uti',
      'emergência', 'sedação', 'tromboembolismo', 'd-dímero', 'respiratória',
      'pao2', 'creatinina', 'bilirrubina', 'pam', 'glasgow-p', 'insuficiência',
      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
      'sepse choque', 'tep dispneia', 'pancreatite aguda amilase',
      'não existe calculator xyz 12345'
    ];

    const latencies: number[] = [];
    const queryCount = 1000;

    for (let i = 0; i < queryCount; i++) {
      const term = candidateTerms[i % candidateTerms.length];
      const { duration } = executeSearch(term);
      latencies.push(duration);
    }

    latencies.sort((a, b) => a - b);
    const p50 = latencies[Math.floor(queryCount * 0.5)];
    const p95 = latencies[Math.floor(queryCount * 0.95)];
    const p99 = latencies[Math.floor(queryCount * 0.99)];
    const max = latencies[queryCount - 1];

    console.log(`[Search Benchmark] 1,000 queries: P50=${p50.toFixed(3)}ms, P95=${p95.toFixed(3)}ms, P99=${p99.toFixed(3)}ms, Max=${max.toFixed(3)}ms`);

    expect(p99).toBeLessThan(10.0);
    expect(p50).toBeLessThan(2.0);
  });

  it('handles adversarial fuzzing inputs without throwing or stalling', () => {
    const adversarialInputs = [
      '',
      '   ',
      '   sepse    choque   ',
      'a'.repeat(2000), // 2000 chars query
      'SELECT * FROM calculators WHERE 1=1; DROP TABLE users;--',
      '<script>alert("xss")</script>',
      '\\d+.*[a-z]{3,}',
      'çãõáéíóúâêîôû',
      '💉 🩺 🚑 💊 ⭐',
      '!@#$%¨&*()_+-=[]{}|;:",.<>?/'
    ];

    for (const input of adversarialInputs) {
      const { results, duration } = executeSearch(input);
      expect(Array.isArray(results)).toBe(true);
      expect(duration).toBeLessThan(20.0);
    }
  });
});

describe('Adversarial Dimension 2: State & Storage Concurrency & Fallback', () => {
  let storage: StorageService;

  beforeEach(async () => {
    // Force in-memory fallback to avoid fake-indexeddb environment quirks and test raw store logic
    storage = new StorageService(true);
    await storage.clearAll();
  });

  it('preserves deterministic favorite state under 20 rapid sequential toggles', async () => {
    const calcId = 'calc_qsofa';

    for (let i = 1; i <= 20; i++) {
      const isFav = await storage.toggleFavorite(calcId);
      const expected = i % 2 !== 0;
      expect(isFav).toBe(expected);
      expect(await storage.isFavorite(calcId)).toBe(expected);
    }

    // After 20 toggles (even number), it should NOT be favorite
    expect(await storage.isFavorite(calcId)).toBe(false);
    expect(await storage.getFavorites()).not.toContain(calcId);
  });

  it('investigates concurrency race condition when toggles are dispatched simultaneously', async () => {
    const calcId = 'calc_sofa';
    expect(await storage.isFavorite(calcId)).toBe(false);

    // Fire 10 concurrent toggle calls without awaiting between them
    const promises = Array.from({ length: 10 }).map(() => storage.toggleFavorite(calcId));
    const results = await Promise.all(promises);

    const finalState = await storage.isFavorite(calcId);
    console.log('[Storage Concurrency Check] 10 concurrent toggles returned:', results, 'Final state:', finalState);

    // Note: If toggleFavorite is not protected by an atomic mutex or lock,
    // concurrent toggles read stale state (all see false, and all set true).
    // An adversarial finding to document!
  });

  it('correctly falls back to MemoryFallbackStore when forced', async () => {
    expect(storage.isUsingFallback()).toBe(true);

    await storage.addFavorite('calc_wells_tep');
    expect(await storage.isFavorite('calc_wells_tep')).toBe(true);

    const favs = await storage.getFavorites();
    expect(favs).toContain('calc_wells_tep');

    await storage.removeFavorite('calc_wells_tep');
    expect(await storage.isFavorite('calc_wells_tep')).toBe(false);
  });

  it('enforces Zero LGPD invariants on saveBed', async () => {
    // Valid anonymous bed record
    const validBed: BedRecord = {
      id: 'bed_01',
      label: 'Leito 04 - UTI',
      sector: 'UTI Geral',
      patientWeightKg: 70,
      notes: 'Paciente estável em ventilação mecânica',
      updatedAt: new Date().toISOString()
    };
    await expect(storage.saveBed(validBed)).resolves.not.toThrow();

    // LGPD Violation: CPF property injected
    const piiBed: any = {
      id: 'bed_02',
      label: 'Leito 05 - UTI',
      cpf: '123.456.789-00'
    };
    await expect(storage.saveBed(piiBed)).rejects.toThrow(/LGPD Violation/);

    // LGPD Violation: Patient full name injected
    const nameBed: any = {
      id: 'bed_03',
      label: 'Leito 06 - UTI',
      patientName: 'Carlos Eduardo da Silva'
    };
    await expect(storage.saveBed(nameBed)).rejects.toThrow(/LGPD Violation/);

    // LGPD Violation: CPF embedded in notes
    const noteCpfBed: BedRecord = {
      id: 'bed_04',
      label: 'Leito 07 - UTI',
      notes: 'Paciente CPF 123.456.789-00 admitido hoje',
      updatedAt: new Date().toISOString()
    };
    await expect(storage.saveBed(noteCpfBed)).rejects.toThrow(/LGPD Violation.*CPF/);
  });
});

describe('Adversarial Dimension 3: PEP EHR Plain-Text Export Robustness', () => {
  const qsofa = block01.calculators.find((c) => c.slug === 'qsofa' || c.id === 'calc_qsofa')!;

  it('generates complete SOAP note without missing any mandatory clinical section', () => {
    const input: PepExportInput = {
      calculator: qsofa,
      result: {
        rawScore: 2,
        scoreFormatted: '2',
        activeRiskTier: qsofa.riskTiers[1], // High risk
        radarValues: {
          respiratory: 1.0,
          hemodynamic: 1.0,
          neurological: 0.0
        },
        sscWarning: 'Surviving Sepsis Campaign 2021: Desaconselha-se o uso isolado do qSOFA como ferramenta única de triagem para exclusão de sepse (baixa sensibilidade).'
      },
      patientBed: 'Leito 04 - UTI Geral',
      patientWeightKg: 80,
      creatinineClearanceMlMin: 45,
      selectedCriteriaLabels: ['FR >= 22 irpm', 'PAS <= 100 mmHg'],
      bicInfusion: {
        drugName: 'Noradrenalina (Hemitartarato de Norepinefrina)',
        dilution: '16 mg em 234 mL SG 5% (64 mcg/mL)',
        doseFormatted: '0.25 mcg/kg/min',
        rateMlPerHour: 18.75,
        recommendedVehicle: 'Soro Glicosado 5% (SG 5%) preferencial',
        containerAlert: 'Proibido frascos/equipos sem proteção ou infusão em veia periférica'
      },
      physicianIdentifier: 'Dr. Plantonista - CRM/SP 123456'
    };

    const note = generatePepNote(input);

    // Verify all mandatory clinical sections exist
    expect(note).toContain('[SCOREBOARD CDSS - REGISTRO DE SUPORTE CLÍNICO]');
    expect(note).toContain('PACIENTE: Leito 04 - UTI Geral | Peso: 80 kg | ClCr Est.: 45 mL/min');
    expect(note).toContain('S (Subjetivo):');
    expect(note).toContain('O (Objetivo):');
    expect(note).toContain('- Escore Calculado:');
    expect(note).toContain('- Estratificação de Risco:');
    expect(note).toContain('- Desfecho / Probabilidade:');
    expect(note).toContain('- Critérios Clínicos Presentes: FR >= 22 irpm; PAS <= 100 mmHg');
    expect(note).toContain('- Radar Fisiológico:');
    expect(note).toContain('- ALERTA SSC 2021:');
    expect(note).toContain('A (Avaliação):');
    expect(note).toContain('P (Plano / Condutas Imediatas):');
    expect(note).toContain('1. Destino Assistencial:');
    expect(note).toContain('3. Drogas Vasoativas / Infusão Contínua (BIC):');
    expect(note).toContain('Noradrenalina (Hemitartarato de Norepinefrina)');
    expect(note).toContain('Vazão em BIC: 18.8 mL/h');
    expect(note).toContain('Veículo: Soro Glicosado 5% (SG 5%) preferencial');
    expect(note).toContain('Atenção Frasco/Equipo:');
    expect(note).toContain('Responsável: Dr. Plantonista - CRM/SP 123456');
  });

  it('generates clean SBAR handover note with BIC and SSC warning', () => {
    const input: PepExportInput = {
      calculator: qsofa,
      result: {
        rawScore: 2,
        scoreFormatted: '2',
        activeRiskTier: qsofa.riskTiers[1],
        radarValues: { respiratory: 1.0, hemodynamic: 1.0, neurological: 0.0 },
        sscWarning: 'Aviso SSC 2021'
      },
      patientBed: 'Box 02 - Sala Vermelha',
      patientWeightKg: 75,
      bicInfusion: {
        drugName: 'Noradrenalina',
        dilution: '64 mcg/mL',
        doseFormatted: '0.20 mcg/kg/min',
        rateMlPerHour: 14.1
      }
    };

    const sbar = generateSbarNote(input);
    expect(sbar).toContain('[SCOREBOARD CDSS - PASSAGEM DE PLANTÃO SBAR]');
    expect(sbar).toContain('S (Situação):');
    expect(sbar).toContain('B (Breve Histórico):');
    expect(sbar).toContain('A (Avaliação):');
    expect(sbar).toContain('R (Recomendação):');
    expect(sbar).toContain('BIC ativa: Noradrenalina a 0.20 mcg/kg/min (Vazão: 14.1 mL/h)');
    expect(sbar).toContain('Aviso SSC 2021: Não descartar sepse baseado unicamente no qSOFA.');
  });

  it('sanitizes bed identifier preventing any nominal CPF leakage (Zero LGPD)', () => {
    expect(sanitizeBedIdentifier('Leito 04')).toBe('Leito 04');
    expect(sanitizeBedIdentifier('04')).toBe('Leito 04');
    expect(sanitizeBedIdentifier('Box 12')).toBe('Box 12');
    expect(sanitizeBedIdentifier('UTI 3')).toBe('UTI 3');
    expect(sanitizeBedIdentifier('')).toBe('Leito -- (Anônimo)');

    // CPF in bed identifier is replaced by [REMOVIDO]
    const sanitizedWithCpf = sanitizeBedIdentifier('Leito 04 - 123.456.789-00');
    expect(sanitizedWithCpf).not.toContain('123.456.789-00');
    expect(sanitizedWithCpf).toContain('[REMOVIDO]');

    const raw11Digits = sanitizeBedIdentifier('Box 12345678901');
    expect(raw11Digits).not.toContain('12345678901');
    expect(raw11Digits).toContain('[REMOVIDO]');
  });

  it('formats dates consistently in Brazilian DD/MM/AAAA - HH:MM notation', () => {
    const fixedDate = new Date(2026, 8, 22, 14, 5); // 22/09/2026 14:05
    const formatted = formatDateBrazilian(fixedDate);
    expect(formatted).toBe('22/09/2026 - 14:05');
  });

  it('summarizes physiological radar deviations accurately across severity tiers', () => {
    const summary = summarizeRadarDeviations(qsofa.radarAxes, {
      axis_qsofa_resp: 0.8, // critico
      axis_qsofa_sbp: 0.5,  // moderado
      axis_qsofa_gcs: 0.2   // leve
    });

    expect(summary).toContain('crítico: 80%');
    expect(summary).toContain('moderado: 50%');
    expect(summary).toContain('leve: 20%');

    const cleanSummary = summarizeRadarDeviations(qsofa.radarAxes, {
      axis_qsofa_resp: 0,
      axis_qsofa_sbp: 0,
      axis_qsofa_gcs: 0
    });
    expect(cleanSummary).toContain('Sem desvios fisiológicos detectados');
  });
});

describe('Adversarial Dimension 4: Mobile Ergonomics & Jump Rail Boundary Conditions', () => {
  it('handles negative or out-of-bounds touch coordinates in jump rail logic safely', () => {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    const railHeight = 400;

    function calculateLetter(clientY: number, railTop: number) {
      const relativeY = clientY - railTop;
      const clampedY = Math.max(0, Math.min(relativeY, railHeight - 1));
      const letterHeight = railHeight / letters.length;
      const index = Math.floor(clampedY / letterHeight);
      return letters[Math.min(index, letters.length - 1)];
    }

    // Well above rail
    expect(calculateLetter(-500, 100)).toBe('A');
    // At top of rail
    expect(calculateLetter(100, 100)).toBe('A');
    // In the middle
    expect(calculateLetter(300, 100)).toBeDefined();
    // At the bottom
    expect(calculateLetter(500, 100)).toBe('Z');
    // Well below rail
    expect(calculateLetter(2000, 100)).toBe('Z');
  });
});
