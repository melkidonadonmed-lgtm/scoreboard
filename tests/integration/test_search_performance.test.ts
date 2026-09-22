import { describe, it, expect } from 'vitest';
import rawManifest from '@/data/manifest.json';
import { type ManifestItem, ManifestSchema } from '@/types/clinical';

const manifest = ManifestSchema.parse(rawManifest);

function normalizeSearchText(text: string): string {
  if (!text) return '';
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

interface IndexedItem {
  item: ManifestItem;
  indexedTokens: string;
}

function indexManifestItems(items: ManifestItem[]): IndexedItem[] {
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
      ...(item.searchSynonyms || [])
    ]
      .map(normalizeSearchText)
      .join(' ');

    return {
      item,
      indexedTokens: tokens
    };
  });
}

const indexedManifest = indexManifestItems(manifest);

function executeSearch(query: string, index: IndexedItem[] = indexedManifest): {
  results: ManifestItem[];
  durationMs: number;
} {
  const t0 = performance.now();
  const clean = normalizeSearchText(query);
  let results = index;

  if (clean) {
    const terms = clean.split(/\s+/).filter(Boolean);
    results = index.filter(({ indexedTokens }) =>
      terms.every((term) => indexedTokens.includes(term))
    );
  }

  const durationMs = performance.now() - t0;
  return { results: results.map((r) => r.item), durationMs };
}

describe('Multi-Block Search Performance & Brazilian Clinical Synonyms Benchmark', () => {
  describe('1. Manifest Inventory & Structure Verification', () => {
    it('contains all 58 clinical tools across Block 01 and Block 03', () => {
      expect(manifest.length).toBe(58);

      const block01Items = manifest.filter((m) => m.blockFile === 'block_01.json');
      const block03Items = manifest.filter((m) => m.blockFile === 'block_03.json');

      expect(block01Items.length).toBe(19);
      expect(block03Items.length).toBe(39);
    });

    it('ensures every tool has comprehensive search tokens and synonyms', () => {
      for (const item of manifest) {
        expect(item.id).toBeTruthy();
        expect(item.name).toBeTruthy();
        expect(item.acronym).toBeTruthy();
        expect(item.searchSynonyms).toBeDefined();
        expect(item.searchSynonyms.length).toBeGreaterThanOrEqual(5);
      }
    });
  });

  describe('2. Multi-Block Search Latency Benchmark (P99 < 10ms)', () => {
    it('executes 2,000 mixed clinical queries and asserts P99 latency < 10ms', () => {
      const benchmarkQueries = [
        // Acronyms & Short Codes
        'HSA', 'TCE', 'AVC', 'AVCi', 'AVCh', 'TEP', 'ICU', 'UTI', 'GCS', 'PIC',
        'DVE', 'NIHSS', 'mRS', 'KPS', 'MEEM', 'MoCA', 'EDSS', 'ABCD2', 'ASIA',
        'SOFA', 'qSOFA', 'Wells', 'Ranson', 'BISAP', 'FOUR',
        // Brazilian Clinical Terms & Medications
        'Trombólise', 'trombolise', 'Nimodipino', 'nimodipino', 'Rotterdam',
        'Aspects', 'Marshall', 'Parkinson', 'Esclerose Múltipla', 'esclerose multipla',
        'Trauma Raquimedular', 'Hunt-Hess', 'Spetzler-Martin', 'Fisher', 'ICH Score',
        'Rankin', 'Karnofsky', 'Noradrenalina', 'Vasopressina', 'Dobutamina',
        'Salina Hipertônica', 'Manitol', 'Levetiracetam', 'Fenitoína',
        // Compound Multi-word queries
        'avc trombolise tenecteplase', 'hsa nimodipino vasoespasmo', 'tce hematoma epidural',
        'trauma raquimedular chave sacral', 'esclerose multipla edss',
        // Edge cases & fuzzing
        'a', 'b', 'c', 'd', 'e', '', '   ', 'inexistente xyz 99999'
      ];

      const iterations = 2000;
      const latencies: number[] = [];

      for (let i = 0; i < iterations; i++) {
        const query = benchmarkQueries[i % benchmarkQueries.length];
        const { durationMs } = executeSearch(query);
        latencies.push(durationMs);
      }

      latencies.sort((a, b) => a - b);
      const p50 = latencies[Math.floor(latencies.length * 0.5)];
      const p90 = latencies[Math.floor(latencies.length * 0.9)];
      const p95 = latencies[Math.floor(latencies.length * 0.95)];
      const p99 = latencies[Math.floor(latencies.length * 0.99)];
      const max = latencies[latencies.length - 1];

      // Console diagnostic telemetry
      console.log(
        `[Search Performance Benchmark] ${iterations} queries: ` +
        `P50=${p50.toFixed(3)}ms, P90=${p90.toFixed(3)}ms, P95=${p95.toFixed(3)}ms, P99=${p99.toFixed(3)}ms, Max=${max.toFixed(3)}ms`
      );

      // Hard contractual assertion: P99 must be strictly under 10ms
      expect(p99).toBeLessThan(10.0);
      expect(p50).toBeLessThan(1.0);
    });
  });

  describe('3. Brazilian Clinical Synonyms & Terms Resolution', () => {
    const requiredResolutions: Array<{
      query: string;
      expectedAcronymSubstrings: string[];
      description: string;
    }> = [
      {
        query: 'HSA',
        expectedAcronymSubstrings: ['Hunt-Hess', 'WFNS', 'Fisher'],
        description: 'Hemorragia Subaracnóidea'
      },
      {
        query: 'TCE',
        expectedAcronymSubstrings: ['Rotterdam', 'Marshall', 'Glasgow-P'],
        description: 'Traumatismo Cranioencefálico'
      },
      {
        query: 'AVC',
        expectedAcronymSubstrings: ['NIHSS', 'ASPECTS', 'ICH Score', 'ABCD²'],
        description: 'Acidente Vascular Cerebral'
      },
      {
        query: 'AVCi',
        expectedAcronymSubstrings: ['NIHSS'],
        description: 'AVC Isquêmico Agudo'
      },
      {
        query: 'AVCh',
        expectedAcronymSubstrings: ['ICH Score'],
        description: 'AVC Hemorrágico / Hematoma Intraparenquimatoso'
      },
      {
        query: 'Trombólise',
        expectedAcronymSubstrings: ['NIHSS'],
        description: 'Trombólise química / Reperfusão'
      },
      {
        query: 'Nimodipino',
        expectedAcronymSubstrings: ['Hunt-Hess'],
        description: 'Profilaxia de vasoespasmo e isquemia cerebral tardia'
      },
      {
        query: 'Rotterdam',
        expectedAcronymSubstrings: ['Rotterdam'],
        description: 'Escore Tomográfico de Rotterdam'
      },
      {
        query: 'Aspects',
        expectedAcronymSubstrings: ['ASPECTS'],
        description: 'Alberta Stroke Program Early CT Score'
      },
      {
        query: 'Marshall',
        expectedAcronymSubstrings: ['Marshall'],
        description: 'Classificação Tomográfica de Marshall'
      },
      {
        query: 'Parkinson',
        expectedAcronymSubstrings: ['Hoehn & Yahr'],
        description: 'Doença de Parkinson e Estadiamento Motor'
      },
      {
        query: 'Esclerose Múltipla',
        expectedAcronymSubstrings: ['EDSS'],
        description: 'Esclerose Múltipla e Escala Expandida de Incapacidade'
      },
      {
        query: 'Trauma Raquimedular',
        expectedAcronymSubstrings: ['ASIA / AIS'],
        description: 'Lesão Medular Traumática'
      },
      {
        query: 'Hunt-Hess',
        expectedAcronymSubstrings: ['Hunt-Hess'],
        description: 'Escala Clínica de Hunt-Hess'
      },
      {
        query: 'Spetzler-Martin',
        expectedAcronymSubstrings: ['Spetzler-Martin'],
        description: 'Malformações Arteriovenosas Cerebrais (MAV)'
      },
      {
        query: 'Fisher',
        expectedAcronymSubstrings: ['Fisher Clássico', 'Fisher Modificado'],
        description: 'Escalas de Fisher para Risco de Vasoespasmo'
      },
      {
        query: 'ICH Score',
        expectedAcronymSubstrings: ['ICH Score'],
        description: 'Intracerebral Hemorrhage Score'
      },
      {
        query: 'ABCD2',
        expectedAcronymSubstrings: ['ABCD²'],
        description: 'Estratificação de AIT'
      },
      {
        query: 'ASIA',
        expectedAcronymSubstrings: ['ASIA / AIS'],
        description: 'American Spinal Injury Association Impairment Scale'
      },
      {
        query: 'Rankin',
        expectedAcronymSubstrings: ['mRS'],
        description: 'Escala de Rankin Modificada'
      },
      {
        query: 'Karnofsky',
        expectedAcronymSubstrings: ['KPS'],
        description: 'Karnofsky Performance Status'
      },
      {
        query: 'MEEM',
        expectedAcronymSubstrings: ['MEEM / MMSE'],
        description: 'Mini-Exame do Estado Mental'
      },
      {
        query: 'MoCA',
        expectedAcronymSubstrings: ['MoCA'],
        description: 'Montreal Cognitive Assessment'
      },
      {
        query: 'tempo porta agulha',
        expectedAcronymSubstrings: ['NIHSS'],
        description: 'Tempo Porta-Agulha no AVC Isquêmico Agudo'
      },
      {
        query: 'esclerose em placas',
        expectedAcronymSubstrings: ['EDSS'],
        description: 'Sinônimo clássico para Esclerose Múltipla'
      },
      {
        query: 'mielopatia',
        expectedAcronymSubstrings: ['ASIA / AIS'],
        description: 'Lesão Medular e Mielopatia'
      },
      {
        query: 'infarto',
        expectedAcronymSubstrings: ['NIHSS', 'ASPECTS'],
        description: 'Infarto Cerebral / Encefálico'
      },
      {
        query: 'tronco encefalico',
        expectedAcronymSubstrings: ['FOUR'],
        description: 'Reflexos de Tronco Encefálico na Escala FOUR'
      }
    ];

    for (const testCase of requiredResolutions) {
      it(`resolves "${testCase.query}" to ${testCase.expectedAcronymSubstrings.join(', ')} (${testCase.description})`, () => {
        const { results } = executeSearch(testCase.query);
        expect(
          results.length,
          `Query "${testCase.query}" returned 0 results`
        ).toBeGreaterThanOrEqual(1);

        for (const expectedAcronym of testCase.expectedAcronymSubstrings) {
          const found = results.some(
            (r) =>
              r.acronym.toLowerCase().includes(expectedAcronym.toLowerCase()) ||
              r.name.toLowerCase().includes(expectedAcronym.toLowerCase())
          );
          expect(
            found,
            `Query "${testCase.query}" failed to match tool with acronym containing "${expectedAcronym}"`
          ).toBe(true);
        }
      });
    }
  });

  describe('4. Cross-Block Robustness & Invariant Testing', () => {
    it('maintains resolution of Block 01 emergency tools without regression', () => {
      const b1Queries = [
        { q: 'sepse', expected: 'qSOFA' },
        { q: 'choque séptico', expected: 'SOFA' },
        { q: 'tep', expected: 'Wells' },
        { q: 'pancreatite aguda', expected: 'Ranson' },
        { q: 'noradrenalina', expected: 'SOFA' },
        { q: 'glasgow', expected: 'Glasgow-P' }
      ];

      for (const { q, expected } of b1Queries) {
        const { results } = executeSearch(q);
        const match = results.some((r) => r.acronym.includes(expected));
        expect(match, `Block 01 query "${q}" failed to match ${expected}`).toBe(true);
      }
    });

    it('handles diacritics and case insensitivity identically', () => {
      const accented = executeSearch('Trombólise').results.map((r) => r.id);
      const unaccented = executeSearch('trombolise').results.map((r) => r.id);
      expect(accented).toEqual(unaccented);

      const upper = executeSearch('ESCLEROSE MÚLTIPLA').results.map((r) => r.id);
      const lower = executeSearch('esclerose multipla').results.map((r) => r.id);
      expect(upper).toEqual(lower);
    });

    it('returns empty array cleanly for completely mismatched queries without exceptions', () => {
      const { results, durationMs } = executeSearch('inexistente termo clinico xyz 999');
      expect(results).toHaveLength(0);
      expect(durationMs).toBeLessThan(5);
    });
  });

  describe('5. Brazilian Clinical Search Synonyms Non-Zero Resolution Verification', () => {
    const synonymQueries: Array<{
      query: string;
      expectedToolIds: string[];
      description: string;
    }> = [
      {
        query: 'tempo porta agulha',
        expectedToolIds: ['calc_nihss'],
        description: 'Tempo porta-agulha para trombólise no AVC isquêmico agudo'
      },
      {
        query: 'esclerose em placas',
        expectedToolIds: ['calc_edss'],
        description: 'Sinônimo clássico brasileiro para esclerose múltipla'
      },
      {
        query: 'mielopatia',
        expectedToolIds: ['calc_asia_ais'],
        description: 'Mielopatia e lesão medular traumática'
      },
      {
        query: 'infarto',
        expectedToolIds: ['calc_nihss', 'calc_aspects'],
        description: 'Infarto cerebral / encefálico'
      },
      {
        query: 'tronco encefalico',
        expectedToolIds: ['calc_four'],
        description: 'Reflexos de tronco encefálico na escala FOUR'
      }
    ];

    for (const { query, expectedToolIds, description } of synonymQueries) {
      it(`verifies "${query}" resolves with non-zero results to intended tools (${description})`, () => {
        const { results } = executeSearch(query);
        expect(results.length).toBeGreaterThan(0);

        const resultIds = results.map((r) => r.id);
        for (const expectedId of expectedToolIds) {
          expect(
            resultIds,
            `Query "${query}" failed to include expected tool "${expectedId}"`
          ).toContain(expectedId);
        }
      });
    }
  });
});
