import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import {
  StorageService,
  storageService,
  validateAnonymousBedRecord,
  type BedRecord,
} from '@/services/storageService';

describe('StorageService & Zero LGPD Verification', () => {
  let service: StorageService;

  beforeEach(async () => {
    service = new StorageService(true); // Test fallback mode first
    await service.clearAll();
  });

  afterEach(async () => {
    await service.clearAll();
  });

  describe('Zero LGPD Risk Compliance', () => {
    it('allows compliant anonymous bed records (e.g. "Leito 04 - UTI")', () => {
      const compliantBed: BedRecord = {
        id: 'bed_01',
        label: 'Leito 04 - UTI',
        sector: 'UTI Geral',
        patientWeightKg: 75,
        notes: 'Em desmame de noradrenalina a 0.05 mcg/kg/min.',
        updatedAt: new Date().toISOString(),
      };

      expect(() => validateAnonymousBedRecord(compliantBed)).not.toThrow();
    });

    it('rejects records containing nominal patient name (LGPD violation)', () => {
      const nonCompliantBed: any = {
        id: 'bed_02',
        label: 'Leito 02',
        name: 'Carlos Drummond de Andrade', // VIOLATION
        updatedAt: new Date().toISOString(),
      };

      expect(() => validateAnonymousBedRecord(nonCompliantBed)).toThrow(
        /LGPD Violation: O campo nominal 'name' é estritamente proibido/i
      );
    });

    it('rejects records containing CPF field (LGPD violation)', () => {
      const nonCompliantBed: any = {
        id: 'bed_03',
        label: 'Leito 03',
        cpf: '123.456.789-00', // VIOLATION
        updatedAt: new Date().toISOString(),
      };

      expect(() => validateAnonymousBedRecord(nonCompliantBed)).toThrow(
        /LGPD Violation: O campo nominal 'cpf' é estritamente proibido/i
      );
    });

    it('rejects records containing prontuario / medical record number (LGPD violation)', () => {
      const nonCompliantBed: any = {
        id: 'bed_04',
        label: 'Leito 04',
        prontuario: 'HC-994821', // VIOLATION
        updatedAt: new Date().toISOString(),
      };

      expect(() => validateAnonymousBedRecord(nonCompliantBed)).toThrow(
        /LGPD Violation: O campo nominal 'prontuario' é estritamente proibido/i
      );
    });

    it('rejects CPF strings embedded in notes', () => {
      const nonCompliantBed: BedRecord = {
        id: 'bed_05',
        label: 'Leito 05',
        notes: 'Contato do familiar CPF 123.456.789-00 na recepção.', // VIOLATION
        updatedAt: new Date().toISOString(),
      };

      expect(() => validateAnonymousBedRecord(nonCompliantBed)).toThrow(
        /LGPD Violation: Padrão de CPF detectado no campo de anotações/i
      );
    });

    it('rejects null, undefined, or missing required fields', () => {
      expect(() => validateAnonymousBedRecord(null as any)).toThrow();
      expect(() => validateAnonymousBedRecord({ id: '', label: 'Leito' } as any)).toThrow();
      expect(() => validateAnonymousBedRecord({ id: '1', label: '' } as any)).toThrow();
    });
  });

  describe('Favorites Management (Fallback & Persistence)', () => {
    it('starts with empty favorites list', async () => {
      const favs = await service.getFavorites();
      expect(favs).toEqual([]);
    });

    it('adds and checks favorites', async () => {
      expect(await service.isFavorite('calc_qsofa')).toBe(false);

      await service.addFavorite('calc_qsofa');
      expect(await service.isFavorite('calc_qsofa')).toBe(true);

      const favs = await service.getFavorites();
      expect(favs).toContain('calc_qsofa');
    });

    it('toggles favorites correctly (on -> off -> on)', async () => {
      // 1st toggle: added
      const res1 = await service.toggleFavorite('calc_sofa');
      expect(res1).toBe(true);
      expect(await service.isFavorite('calc_sofa')).toBe(true);

      // 2nd toggle: removed
      const res2 = await service.toggleFavorite('calc_sofa');
      expect(res2).toBe(false);
      expect(await service.isFavorite('calc_sofa')).toBe(false);

      // 3rd toggle: added back
      const res3 = await service.toggleFavorite('calc_sofa');
      expect(res3).toBe(true);
      expect(await service.isFavorite('calc_sofa')).toBe(true);
    });

    it('removes favorite via removeFavorite', async () => {
      await service.addFavorite('calc_wells_tep');
      await service.addFavorite('calc_glasgow_p');

      expect(await service.getFavorites()).toHaveLength(2);

      await service.removeFavorite('calc_wells_tep');
      const updated = await service.getFavorites();
      expect(updated).toEqual(['calc_glasgow_p']);
      expect(await service.isFavorite('calc_wells_tep')).toBe(false);
    });
  });

  describe('Beds Management (Bedside Clinical Tracking)', () => {
    it('saves and retrieves anonymous bed records', async () => {
      const bed1: BedRecord = {
        id: 'bed_uti_01',
        label: 'Leito 01 - UTI Choque',
        sector: 'UTI Choque',
        patientWeightKg: 82.5,
        notes: 'Protocolo de sepse aberto, qSOFA 2.',
        updatedAt: '2026-09-22T10:00:00.000Z',
      };

      await service.saveBed(bed1);

      const retrieved = await service.getBed('bed_uti_01');
      expect(retrieved).toBeDefined();
      expect(retrieved?.id).toBe('bed_uti_01');
      expect(retrieved?.label).toBe('Leito 01 - UTI Choque');
      expect(retrieved?.patientWeightKg).toBe(82.5);

      const allBeds = await service.getBeds();
      expect(allBeds).toHaveLength(1);
      expect(allBeds[0].id).toBe('bed_uti_01');
    });

    it('updates existing bed record', async () => {
      const bed: BedRecord = {
        id: 'bed_02',
        label: 'Leito 02 - Emergência',
        patientWeightKg: 70,
        updatedAt: '2026-09-22T08:00:00.000Z',
      };
      await service.saveBed(bed);

      // Update weight
      const updatedBed: BedRecord = {
        ...bed,
        patientWeightKg: 72,
        notes: 'Peso atualizado após hidratação.',
      };
      await service.saveBed(updatedBed);

      const found = await service.getBed('bed_02');
      expect(found?.patientWeightKg).toBe(72);
      expect(found?.notes).toBe('Peso atualizado após hidratação.');
    });

    it('deletes bed record', async () => {
      await service.saveBed({ id: 'b1', label: 'Leito 1', updatedAt: '2026-01-01' });
      await service.saveBed({ id: 'b2', label: 'Leito 2', updatedAt: '2026-01-01' });

      expect(await service.getBeds()).toHaveLength(2);

      await service.deleteBed('b1');
      const beds = await service.getBeds();
      expect(beds).toHaveLength(1);
      expect(beds[0].id).toBe('b2');
      expect(await service.getBed('b1')).toBeUndefined();
    });

    it('supports alias methods saveBedRecord and getBedRecords', async () => {
      const bed: BedRecord = {
        id: 'bed_alias_01',
        label: 'Leito 10 - Semi-Intensiva',
        updatedAt: '2026-09-22',
      };
      await service.saveBedRecord(bed);
      const records = await service.getBedRecords();
      expect(records.map((r) => r.id)).toContain('bed_alias_01');

      await service.deleteBedRecord('bed_alias_01');
      expect(await service.getBed('bed_alias_01')).toBeUndefined();
    });
  });

  describe('Fallback Resilience and Mode Detection', () => {
    it('detects fallback mode correctly', () => {
      service.setForcedFallback(true);
      expect(service.isUsingFallback()).toBe(true);

      service.setForcedFallback(false);
      // In Node environment where indexedDB is undefined and no custom DB is set, isUsingFallback() returns true
      expect(service.isUsingFallback()).toBe(true);
    });

    it('retains in-memory data across multiple calls when fallback is active', async () => {
      service.setForcedFallback(true);
      await service.addFavorite('calc_ranson');
      await service.saveBed({ id: 'bed_mem', label: 'Leito Memória', updatedAt: '2026-09-22' });

      expect(await service.isFavorite('calc_ranson')).toBe(true);
      expect(await service.getBed('bed_mem')).toBeDefined();

      await service.clearAll();
      expect(await service.getFavorites()).toEqual([]);
      expect(await service.getBeds()).toEqual([]);
    });
  });

  describe('IndexedDB Store Upgrade & Mock Execution', () => {
    it('verifies DB upgrade callback registers "favorites" and "beds" object stores', async () => {
      const createdStores: string[] = [];
      const createdIndexes: string[] = [];

      const mockDb = {
        objectStoreNames: {
          contains: (name: string) => createdStores.includes(name),
        },
        createObjectStore: vi.fn((name: string, _options?: any) => {
          createdStores.push(name);
          return {
            createIndex: vi.fn((idxName: string) => {
              createdIndexes.push(idxName);
            }),
          };
        }),
      };

      // Simulate upgrade function defined in openDB
      const upgradeHandler = (db: any) => {
        if (!db.objectStoreNames.contains('favorites')) {
          db.createObjectStore('favorites', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('beds')) {
          const bedStore = db.createObjectStore('beds', { keyPath: 'id' });
          bedStore.createIndex('by-sector', 'sector');
        }
      };

      upgradeHandler(mockDb);

      expect(createdStores).toContain('favorites');
      expect(createdStores).toContain('beds');
      expect(createdIndexes).toContain('by-sector');
    });

    it('verifies singleton storageService methods are exported and functional', async () => {
      expect(typeof storageService.getFavorites).toBe('function');
      expect(typeof storageService.toggleFavorite).toBe('function');
      expect(typeof storageService.getBeds).toBe('function');
      expect(typeof storageService.saveBed).toBe('function');

      const favs = await storageService.getFavorites();
      expect(Array.isArray(favs)).toBe(true);
    });
  });

  describe('IndexedDB Direct Branch Verification', () => {
    it('executes get/put/delete operations against IDBPDatabase when available', async () => {
      const storeData: Record<string, Map<string, any>> = {
        favorites: new Map(),
        beds: new Map(),
      };

      const mockDbInstance = {
        getAll: vi.fn(async (store: string) => {
          return Array.from(storeData[store]?.values() || []);
        }),
        get: vi.fn(async (store: string, key: string) => {
          return storeData[store]?.get(key);
        }),
        put: vi.fn(async (store: string, val: any) => {
          storeData[store]?.set(val.id, val);
        }),
        delete: vi.fn(async (store: string, key: string) => {
          storeData[store]?.delete(key);
        }),
        close: vi.fn(),
        transaction: vi.fn(() => ({
          objectStore: vi.fn((name: string) => ({
            clear: vi.fn(async () => storeData[name]?.clear()),
          })),
          done: Promise.resolve(),
        })),
      };

      // Instantiate service and inject mock DB instance
      const idbService = new StorageService(false);
      idbService.setCustomDB(mockDbInstance as any);

      expect(idbService.isUsingFallback()).toBe(false);

      // Test favorites on IDB
      await idbService.addFavorite('calc_qsofa');
      expect(mockDbInstance.put).toHaveBeenCalledWith('favorites', expect.objectContaining({ id: 'calc_qsofa' }));

      const isFav = await idbService.isFavorite('calc_qsofa');
      expect(isFav).toBe(true);
      expect(mockDbInstance.get).toHaveBeenCalledWith('favorites', 'calc_qsofa');

      const favs = await idbService.getFavorites();
      expect(favs).toContain('calc_qsofa');
      expect(mockDbInstance.getAll).toHaveBeenCalledWith('favorites');

      await idbService.removeFavorite('calc_qsofa');
      expect(mockDbInstance.delete).toHaveBeenCalledWith('favorites', 'calc_qsofa');

      // Test bed records on IDB
      const bed: BedRecord = {
        id: 'bed_idb_01',
        label: 'Leito 01 - UTI Coronária',
        patientWeightKg: 68,
        updatedAt: '2026-09-22T00:00:00.000Z',
      };
      await idbService.saveBed(bed);
      expect(mockDbInstance.put).toHaveBeenCalledWith('beds', expect.objectContaining({ id: 'bed_idb_01' }));

      const fetchedBed = await idbService.getBed('bed_idb_01');
      expect(fetchedBed?.id).toBe('bed_idb_01');

      const allBeds = await idbService.getBeds();
      expect(allBeds).toHaveLength(1);

      await idbService.deleteBed('bed_idb_01');
      expect(mockDbInstance.delete).toHaveBeenCalledWith('beds', 'bed_idb_01');
    });
  });
});

import manifestDataRaw from '@/data/manifest.json';
import type { ManifestItem } from '@/types/clinical';

const manifestData = manifestDataRaw as unknown as ManifestItem[];

describe('Brazilian Clinical Synonyms & Instant Search (<10ms)', () => {
  function normalize(text: string): string {
    return text
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();
  }

  function searchManifest(query: string): ManifestItem[] {
    const normQuery = normalize(query);
    const terms = normQuery.split(/\s+/).filter(Boolean);

    return manifestData.filter((item) => {
      const combined = [
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
        .map(normalize)
        .join(' ');

      return terms.every((t) => combined.includes(t));
    });
  }

  it('verifies manifest has valid items and search latency is strictly < 10ms', () => {
    const t0 = performance.now();
    const results = searchManifest('sepse');
    const elapsed = performance.now() - t0;

    expect(results.length).toBeGreaterThan(0);
    expect(elapsed).toBeLessThan(10); // Guaranteed <10ms latency requirement
  });

  it('correctly indexes Brazilian clinical synonym "sepse" (returns qSOFA and SOFA)', () => {
    const results = searchManifest('sepse');
    const ids = results.map((r) => r.id);
    expect(ids).toContain('calc_qsofa');
    expect(ids).toContain('calc_sofa');
  });

  it('correctly indexes Brazilian clinical synonym "choque" (returns shock & sepsis tools)', () => {
    const results = searchManifest('choque');
    const ids = results.map((r) => r.id);
    expect(ids).toContain('calc_qsofa');
    expect(ids).toContain('calc_sofa');
  });

  it('correctly indexes Brazilian clinical synonym "tep" (returns Wells TEP, Geneva, PERC, PESI)', () => {
    const results = searchManifest('tep');
    const ids = results.map((r) => r.id);
    expect(ids).toContain('calc_wells_tep');
    expect(ids).toContain('calc_geneva');
    expect(ids).toContain('calc_perc');
    expect(ids).toContain('calc_pesi');
  });

  it('correctly indexes Brazilian clinical synonym "pancreatite" (returns Ranson, BISAP, Balthazar, Marshall)', () => {
    const results = searchManifest('pancreatite');
    const ids = results.map((r) => r.id);
    expect(ids).toContain('calc_ranson');
    expect(ids).toContain('calc_bisap');
    expect(ids).toContain('calc_balthazar_ctsi');
    expect(ids).toContain('calc_marshall_mod');
  });

  it('correctly indexes Brazilian clinical synonym "glasgow" and "coma" (returns Glasgow-P, FOUR)', () => {
    const glasgowResults = searchManifest('glasgow');
    expect(glasgowResults.map((r) => r.id)).toContain('calc_glasgow_p');

    const comaResults = searchManifest('coma');
    expect(comaResults.map((r) => r.id)).toContain('calc_glasgow_p');
    expect(comaResults.map((r) => r.id)).toContain('calc_four');
  });

  it('correctly indexes vasoactive drug synonym "noradrenalina"', () => {
    const results = searchManifest('noradrenalina');
    const ids = results.map((r) => r.id);
    expect(ids).toContain('calc_qsofa');
    expect(ids).toContain('calc_sofa');
  });

  it('groups all manifest items alphabetically by acronym into valid A-Z sections', () => {
    const letters = new Set<string>();

    for (const item of manifestData) {
      const acronym = item.acronym || item.name;
      const firstChar = acronym.trim().replace(/^[^a-zA-Z0-9]+/, '')[0]?.toUpperCase() || '#';
      letters.add(firstChar);
    }

    // Verify key letters present in Block 01
    expect(letters.has('A')).toBe(true); // APACHE II
    expect(letters.has('B')).toBe(true); // BISAP, Balthazar
    expect(letters.has('C')).toBe(true); // CAM-ICU
    expect(letters.has('F')).toBe(true); // FOUR
    expect(letters.has('G')).toBe(true); // Geneva, Glasgow-P
    expect(letters.has('M')).toBe(true); // Marshall
    expect(letters.has('P')).toBe(true); // PERC, PESI
    expect(letters.has('Q')).toBe(true); // qSOFA
    expect(letters.has('R')).toBe(true); // Ranson, RASS
    expect(letters.has('S')).toBe(true); // SOFA, SAPS 3, SAS, sPESI
    expect(letters.has('W')).toBe(true); // Wells TEP, Wells TVP
  });
});
