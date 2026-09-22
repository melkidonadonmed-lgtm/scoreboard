/**
 * Tier 2 — Boundary & Corner Cases: Features 11 to 15
 * Exactly 25 tests (5 per feature).
 */

import { describe, it, expect, adapter, envShim } from '../harness/index.js';

describe('Tier 2 — Feature 11 Boundaries: Storage & Zero LGPD', () => {
  it('B11-1: Rejects CNPJ patterns in bed label to guarantee Zero LGPD risk', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    let threw = false;
    try {
      await storage.saveBedRecord({
        id: 'bed_cnpj',
        bedLabel: 'Hospital CNPJ 12.345.678/0001-90'
      });
    } catch (e) {
      threw = true;
      expect(e.message).toContain('LGPD Violation');
    }
    expect(threw).toBe(true);
  });

  it('B11-2: Updating an existing bed record mutates in place without creating duplicate IDs', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.saveBedRecord({ id: 'bed_01', bedLabel: 'Leito 01 - UTI', notes: 'Primeira nota' });
    await storage.saveBedRecord({ id: 'bed_01', bedLabel: 'Leito 01 - UTI', notes: 'Segunda nota atualizada' });
    const beds = await storage.getBedRecords();
    expect(beds.length).toBe(1);
    expect(beds[0].notes).toBe('Segunda nota atualizada');
  });

  it('B11-3: Bed record with empty label falls back to anonymous designation', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.saveBedRecord({ id: 'bed_empty', bedLabel: '' });
    const beds = await storage.getBedRecords();
    expect(beds[0].bedLabel).toBe('Leito Sem Identificação');
  });

  it('B11-4: Stores and retrieves large favorites array (up to 98 scores) without truncation', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    const mockIds = Array.from({ length: 98 }, (_, i) => `score_${i}`);
    for (const id of mockIds) {
      await storage.toggleFavorite(id);
    }
    const favs = await storage.getFavorites();
    expect(favs.length).toBe(98);
    expect(favs[0]).toBe('score_0');
    expect(favs[97]).toBe('score_97');
  });

  it('B11-5: Concurrent toggle operations resolve deterministically', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await Promise.all([
      storage.toggleFavorite('score_a'),
      storage.toggleFavorite('score_b'),
      storage.toggleFavorite('score_c')
    ]);
    const favs = await storage.getFavorites();
    expect(favs.length).toBe(3);
  });
});

describe('Tier 2 — Feature 12 Boundaries: Search Extremes', () => {
  it('B12-1: Normalizes and searches queries with multiple internal spaces', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('wells    tep', manifest);
    expect(results.length).toBe(1);
    expect(results[0].id).toBe('wells_pe');
  });

  it('B12-2: Matches substring in Brazilian clinical categories (e.g. "pneumo")', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('pneumo', manifest);
    expect(results.length).toBeGreaterThan(0);
    expect(results.some(r => r.category.toLowerCase().includes('pneumo'))).toBe(true);
  });

  it('B12-3: Single character search matches calculators across multiple fields', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('q', manifest);
    expect(results.length).toBeGreaterThan(0);
    expect(results.some(r => r.id === 'qsofa')).toBe(true);
  });

  it('B12-4: Executes 20 consecutive rapid searches within 25ms total', () => {
    const manifest = adapter.getManifestData();
    const queries = ['sepse', 'tep', 'coma', 'four', 'sofa', 'glasgow', 'ranson', 'bisap', 'choque', 'infecção'];
    const t0 = performance.now();
    for (let i = 0; i < 20; i++) {
      adapter.searchCalculators(queries[i % queries.length], manifest);
    }
    const totalTime = performance.now() - t0;
    expect(totalTime).toBeLessThan(25);
  });

  it('B12-5: Matches identical results regardless of query accentuation ("infecção" vs "infeccao")', () => {
    const manifest = adapter.getManifestData();
    const resWithAccent = adapter.searchCalculators('infecção', manifest);
    const resWithoutAccent = adapter.searchCalculators('infeccao', manifest);
    expect(resWithAccent.results.length).toBe(resWithoutAccent.results.length);
    expect(resWithAccent.results.length).toBeGreaterThan(0);
  });
});

describe('Tier 2 — Feature 13 Boundaries: Jump Rail Edge Coordinates', () => {
  it('B13-1: Touch Y coordinate exactly on bottom boundary resolves to "Z"', () => {
    // railTop = 100, height = 520 -> bottom = 620
    const res = adapter.calculateJumpRailTouch(620, 100, 520);
    expect(res.letter).toBe('Z');
    expect(res.index).toBe(25);
  });

  it('B13-2: Negative touch Y coordinate clamps safely to "A"', () => {
    const res = adapter.calculateJumpRailTouch(-150, 100, 520);
    expect(res.letter).toBe('A');
    expect(res.index).toBe(0);
  });

  it('B13-3: Operates correctly on compact rail height (e.g. 100px)', () => {
    const res = adapter.calculateJumpRailTouch(150, 100, 100);
    expect(typeof res.letter).toBe('string');
    expect(res.index).toBeGreaterThanOrEqual(0);
    expect(res.index).toBeLessThanOrEqual(25);
  });

  it('B13-4: Scrubbing across all 26 letters records discrete haptic vibration events', () => {
    envShim.reset();
    for (let i = 0; i < 26; i++) {
      const y = 100 + i * 20;
      const touch = adapter.calculateJumpRailTouch(y, 100, 520);
      envShim.navigator.vibrate(touch.vibratePattern);
    }
    expect(envShim.vibrateCalls.length).toBe(26);
    expect(envShim.vibrateCalls[0]).toBe(10);
  });

  it('B13-5: Jump rail mapping produces valid letters even when catalog lacks items for letter', () => {
    const res = adapter.calculateJumpRailTouch(100 + 25 * 20, 100, 520); // 'Z'
    expect(res.letter).toBe('Z');
  });
});

describe('Tier 2 — Feature 14 Boundaries: A-Z Catalog Grouping', () => {
  it('B14-1: Catalog with single calculator generates a single letter section', () => {
    const single = [{ id: 'qsofa', name: 'quick SOFA' }];
    const groups = adapter.groupScoresAlphabetically(single);
    expect(groups.length).toBe(1);
    expect(groups[0].letter).toBe('Q');
    expect(groups[0].items.length).toBe(1);
  });

  it('B14-2: Multiple calculators with identical initial letter are clustered together', () => {
    const items = [
      { id: '1', name: 'Ranson 0h' },
      { id: '2', name: 'Ranson 48h' },
      { id: '3', name: 'Risco de Sangramento' }
    ];
    const groups = adapter.groupScoresAlphabetically(items);
    expect(groups.length).toBe(1);
    expect(groups[0].letter).toBe('R');
    expect(groups[0].items.length).toBe(3);
  });

  it('B14-3: Correctly capitalizes lowercase initials for section header grouping', () => {
    const items = [
      { id: 'q1', name: 'qSOFA' },
      { id: 'q2', name: 'quick Sequential' }
    ];
    const groups = adapter.groupScoresAlphabetically(items);
    expect(groups[0].letter).toBe('Q');
  });

  it('B14-4: Empty input scores array returns an empty section list without error', () => {
    const groups = adapter.groupScoresAlphabetically([]);
    expect(Array.isArray(groups)).toBe(true);
    expect(groups.length).toBe(0);
  });

  it('B14-5: Preserves monographic clinical descriptions regardless of length', () => {
    const longDesc = 'A'.repeat(500);
    const item = [{ id: 'test', name: 'Test Calculator', description: longDesc }];
    const groups = adapter.groupScoresAlphabetically(item);
    expect(groups[0].items[0].description.length).toBe(500);
  });
});

describe('Tier 2 — Feature 15 Boundaries: Favorites Edge Cases', () => {
  it('B15-1: Toggling an already-starred item unstars it immediately', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('qsofa');
    expect(await storage.isFavorite('qsofa')).toBe(true);
    await storage.toggleFavorite('qsofa');
    expect(await storage.isFavorite('qsofa')).toBe(false);
  });

  it('B15-2: Handles carousel state with exactly 1 favorite starred', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('wells_pe');
    const favs = await storage.getFavorites();
    expect(favs.length).toBe(1);
    expect(favs[0]).toBe('wells_pe');
  });

  it('B15-3: Toggling favorite is reflected in subsequent getFavorites calls', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('sofa');
    let favs = await storage.getFavorites();
    expect(favs).toContain('sofa');
    await storage.toggleFavorite('sofa');
    favs = await storage.getFavorites();
    expect(favs).not.toContain('sofa');
  });

  it('B15-4: Checks isFavorite for arbitrary non-starred ID returns false', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    const isFav = await storage.isFavorite('non_existent_id');
    expect(isFav).toBe(false);
  });

  it('B15-5: Preserves insertion timestamp on quick_pins in IndexedDB', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('ranson');
    const db = await envShim.indexedDB.openDB('scoreboard_db', 1);
    const pin = await db.get('quick_pins', 'ranson');
    expect(pin).toBeDefined();
    expect(pin.id).toBe('ranson');
    expect(pin.pinnedAt).toBeDefined();
  });
});
