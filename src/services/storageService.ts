import { openDB, type IDBPDatabase } from 'idb';

/**
 * BedRecord: Anonymous bedside tracking record.
 * LGPD Rule: Strictly anonymous; no nominal patient data (CPF, name, MRN).
 */
export interface BedRecord {
  id: string;
  label: string; // e.g. "Leito 04 - UTI", "Box 02 - Sala Vermelha"
  sector?: string; // e.g. "UTI Geral", "Emergência", "UCO"
  patientWeightKg?: number;
  notes?: string;
  updatedAt: string; // ISO string
}

export interface FavoriteRecord {
  id: string;
  addedAt: string;
}

const DB_NAME = 'scoreboard_cdss_db';
const DB_VERSION = 1;

// Storage keys for localStorage / fallback
const LS_FAVORITES_KEY = 'scoreboard_cdss_favorites';
const LS_BEDS_KEY = 'scoreboard_cdss_beds';

// Fields that violate LGPD patient privacy guidelines
const FORBIDDEN_LGPD_KEYS = [
  'name',
  'nome',
  'patientname',
  'patient_name',
  'cpf',
  'prontuario',
  'prontuário',
  'mrn',
  'rg',
  'cns',
  'birthdate',
  'birth_date',
  'data_nascimento',
];

/**
 * Validates that no nominal patient identifiers are present in the record.
 */
export function validateAnonymousBedRecord(bed: BedRecord): void {
  if (!bed) {
    throw new Error('Registro de leito inválido: objeto nulo ou indefinido.');
  }

  if (!bed.id || typeof bed.id !== 'string') {
    throw new Error('Registro de leito inválido: identificador (id) obrigatório.');
  }

  if (!bed.label || typeof bed.label !== 'string') {
    throw new Error('Registro de leito inválido: rótulo anônimo (label) obrigatório (ex: "Leito 04 - UTI").');
  }

  const keys = Object.keys(bed);
  for (const k of keys) {
    if (FORBIDDEN_LGPD_KEYS.includes(k.toLowerCase())) {
      throw new Error(
        `LGPD Violation: O campo nominal '${k}' é estritamente proibido. Utilize apenas identificadores de leito anônimos.`
      );
    }
  }

  // Prevent CPF patterns in free-text notes
  if (bed.notes && /\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/.test(bed.notes)) {
    throw new Error('LGPD Violation: Padrão de CPF detectado no campo de anotações.');
  }
}

/**
 * In-Memory & LocalStorage Fallback Store
 */
class MemoryFallbackStore {
  private favorites = new Set<string>();
  private beds = new Map<string, BedRecord>();

  constructor() {
    this.hydrateFromLocalStorage();
  }

  private hydrateFromLocalStorage(): void {
    if (typeof localStorage === 'undefined') return;
    try {
      const rawFavs = localStorage.getItem(LS_FAVORITES_KEY);
      if (rawFavs) {
        const parsed = JSON.parse(rawFavs);
        if (Array.isArray(parsed)) {
          this.favorites = new Set(parsed);
        }
      }
      const rawBeds = localStorage.getItem(LS_BEDS_KEY);
      if (rawBeds) {
        const parsed = JSON.parse(rawBeds);
        if (Array.isArray(parsed)) {
          this.beds.clear();
          parsed.forEach((b: BedRecord) => {
            if (b && b.id) this.beds.set(b.id, b);
          });
        }
      }
    } catch {
      // Ignore localStorage parse errors
    }
  }

  private persistToLocalStorage(): void {
    if (typeof localStorage === 'undefined') return;
    try {
      localStorage.setItem(LS_FAVORITES_KEY, JSON.stringify(Array.from(this.favorites)));
      localStorage.setItem(LS_BEDS_KEY, JSON.stringify(Array.from(this.beds.values())));
    } catch {
      // Ignore storage quota or disabled errors
    }
  }

  async getFavorites(): Promise<string[]> {
    return Array.from(this.favorites);
  }

  async isFavorite(id: string): Promise<boolean> {
    return this.favorites.has(id);
  }

  async addFavorite(id: string): Promise<void> {
    this.favorites.add(id);
    this.persistToLocalStorage();
  }

  async removeFavorite(id: string): Promise<void> {
    this.favorites.delete(id);
    this.persistToLocalStorage();
  }

  async toggleFavorite(id: string): Promise<boolean> {
    if (this.favorites.has(id)) {
      this.favorites.delete(id);
      this.persistToLocalStorage();
      return false;
    } else {
      this.favorites.add(id);
      this.persistToLocalStorage();
      return true;
    }
  }

  async getBeds(): Promise<BedRecord[]> {
    return Array.from(this.beds.values());
  }

  async getBed(id: string): Promise<BedRecord | undefined> {
    return this.beds.get(id);
  }

  async saveBed(bed: BedRecord): Promise<void> {
    validateAnonymousBedRecord(bed);
    const sanitized: BedRecord = {
      id: bed.id,
      label: bed.label,
      sector: bed.sector,
      patientWeightKg: bed.patientWeightKg,
      notes: bed.notes,
      updatedAt: bed.updatedAt || new Date().toISOString(),
    };
    this.beds.set(bed.id, sanitized);
    this.persistToLocalStorage();
  }

  async deleteBed(id: string): Promise<void> {
    this.beds.delete(id);
    this.persistToLocalStorage();
  }

  async clear(): Promise<void> {
    this.favorites.clear();
    this.beds.clear();
    if (typeof localStorage !== 'undefined') {
      try {
        localStorage.removeItem(LS_FAVORITES_KEY);
        localStorage.removeItem(LS_BEDS_KEY);
      } catch {
        // ignore
      }
    }
  }
}

/**
 * StorageService: Unified interface with IndexedDB and graceful Fallback.
 */
export class StorageService {
  private dbPromise: Promise<IDBPDatabase> | null = null;
  private fallbackStore = new MemoryFallbackStore();
  private forceFallback = false;
  private fallbackActive = false;

  constructor(forceFallback = false) {
    this.forceFallback = forceFallback;
  }

  /**
   * For testing or environments where IndexedDB should be disabled.
   */
  public setForcedFallback(forced: boolean): void {
    this.forceFallback = forced;
    if (forced) {
      this.fallbackActive = true;
      this.dbPromise = null;
    } else {
      this.fallbackActive = false;
    }
  }

  /**
   * Direct database injector (useful for mocks and custom test harnesses).
   */
  public setCustomDB(db: IDBPDatabase | null): void {
    if (db) {
      this.dbPromise = Promise.resolve(db);
      this.forceFallback = false;
      this.fallbackActive = false;
    } else {
      this.dbPromise = null;
    }
  }

  public isUsingFallback(): boolean {
    return this.forceFallback || this.fallbackActive || (this.dbPromise === null && typeof indexedDB === 'undefined');
  }

  private async getDB(): Promise<IDBPDatabase | null> {
    if (this.forceFallback) {
      this.fallbackActive = true;
      return null;
    }

    if (!this.dbPromise) {
      if (typeof indexedDB === 'undefined') {
        this.fallbackActive = true;
        return null;
      }

      this.dbPromise = openDB(DB_NAME, DB_VERSION, {
        upgrade(db) {
          if (!db.objectStoreNames.contains('favorites')) {
            db.createObjectStore('favorites', { keyPath: 'id' });
          }
          if (!db.objectStoreNames.contains('beds')) {
            const bedStore = db.createObjectStore('beds', { keyPath: 'id' });
            bedStore.createIndex('by-sector', 'sector');
          }
        },
      }).catch((err) => {
        console.warn('IndexedDB unavailable, falling back to local store:', err);
        this.fallbackActive = true;
        return null as any;
      });
    }

    const db = await this.dbPromise;
    if (!db) {
      this.fallbackActive = true;
      return null;
    }
    return db;
  }

  /**
   * Closes database connections.
   */
  public async closeDB(): Promise<void> {
    if (this.dbPromise) {
      try {
        const db = await this.dbPromise;
        if (db) db.close();
      } catch {
        // ignore
      }
      this.dbPromise = null;
    }
  }

  /**
   * Clear all records (useful for test resets).
   */
  public async clearAll(): Promise<void> {
    const db = await this.getDB();
    if (db) {
      try {
        const tx = db.transaction(['favorites', 'beds'], 'readwrite');
        await Promise.all([
          tx.objectStore('favorites').clear(),
          tx.objectStore('beds').clear(),
          tx.done,
        ]);
      } catch {
        // fall back to fallback store
      }
    }
    await this.fallbackStore.clear();
  }

  // =========================================================================
  // FAVORITES
  // =========================================================================

  async getFavorites(): Promise<string[]> {
    const db = await this.getDB();
    if (db) {
      try {
        const items = await db.getAll('favorites');
        return items.map((item) => (typeof item === 'string' ? item : item.id));
      } catch {
        // Fallback to memory
      }
    }
    return this.fallbackStore.getFavorites();
  }

  async isFavorite(id: string): Promise<boolean> {
    const db = await this.getDB();
    if (db) {
      try {
        const item = await db.get('favorites', id);
        return Boolean(item);
      } catch {
        // Fallback
      }
    }
    return this.fallbackStore.isFavorite(id);
  }

  async addFavorite(id: string): Promise<void> {
    const db = await this.getDB();
    if (db) {
      try {
        await db.put('favorites', {
          id,
          addedAt: new Date().toISOString(),
        });
        return;
      } catch {
        // Fallback
      }
    }
    await this.fallbackStore.addFavorite(id);
  }

  async removeFavorite(id: string): Promise<void> {
    const db = await this.getDB();
    if (db) {
      try {
        await db.delete('favorites', id);
        return;
      } catch {
        // Fallback
      }
    }
    await this.fallbackStore.removeFavorite(id);
  }

  async toggleFavorite(id: string): Promise<boolean> {
    const currentlyFav = await this.isFavorite(id);
    if (currentlyFav) {
      await this.removeFavorite(id);
      return false;
    } else {
      await this.addFavorite(id);
      return true;
    }
  }

  // =========================================================================
  // BEDS (Zero LGPD Risk)
  // =========================================================================

  async getBeds(): Promise<BedRecord[]> {
    const db = await this.getDB();
    if (db) {
      try {
        return await db.getAll('beds');
      } catch {
        // Fallback
      }
    }
    return this.fallbackStore.getBeds();
  }

  async getBedRecords(): Promise<BedRecord[]> {
    return this.getBeds();
  }

  async getBed(id: string): Promise<BedRecord | undefined> {
    const db = await this.getDB();
    if (db) {
      try {
        return await db.get('beds', id);
      } catch {
        // Fallback
      }
    }
    return this.fallbackStore.getBed(id);
  }

  async saveBed(bed: BedRecord): Promise<void> {
    validateAnonymousBedRecord(bed);
    const sanitized: BedRecord = {
      id: bed.id,
      label: bed.label,
      sector: bed.sector,
      patientWeightKg: bed.patientWeightKg,
      notes: bed.notes,
      updatedAt: bed.updatedAt || new Date().toISOString(),
    };

    const db = await this.getDB();
    if (db) {
      try {
        await db.put('beds', sanitized);
        return;
      } catch {
        // Fallback
      }
    }
    await this.fallbackStore.saveBed(sanitized);
  }

  async saveBedRecord(record: BedRecord): Promise<void> {
    return this.saveBed(record);
  }

  async deleteBed(id: string): Promise<void> {
    const db = await this.getDB();
    if (db) {
      try {
        await db.delete('beds', id);
        return;
      } catch {
        // Fallback
      }
    }
    await this.fallbackStore.deleteBed(id);
  }

  async deleteBedRecord(id: string): Promise<void> {
    return this.deleteBed(id);
  }
}

// Singleton export
export const storageService = new StorageService();

// Standalone function exports for convenience
export const getFavorites = () => storageService.getFavorites();
export const isFavorite = (id: string) => storageService.isFavorite(id);
export const addFavorite = (id: string) => storageService.addFavorite(id);
export const removeFavorite = (id: string) => storageService.removeFavorite(id);
export const toggleFavorite = (id: string) => storageService.toggleFavorite(id);

export const getBeds = () => storageService.getBeds();
export const getBedRecords = () => storageService.getBedRecords();
export const getBed = (id: string) => storageService.getBed(id);
export const saveBed = (bed: BedRecord) => storageService.saveBed(bed);
export const saveBedRecord = (record: BedRecord) => storageService.saveBedRecord(record);
export const deleteBed = (id: string) => storageService.deleteBed(id);
export const deleteBedRecord = (id: string) => storageService.deleteBedRecord(id);
