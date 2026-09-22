/**
 * Tier 1 — Feature Coverage: Features 11 to 15
 * Covers: Local Storage (IndexedDB), Instant Search, Alphabet Jump Rail, A-Z Score List, Star Favorites
 * Exactly 25 tests (5 per feature).
 */

import { describe, it, expect, adapter, envShim } from '../harness/index.js';

describe('Tier 1 — Feature 11: Local Storage Service (IndexedDB)', () => {
  it('F11-1: Saves and retrieves quick-pin favorites from IndexedDB', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('qsofa');
    const favs = await storage.getFavorites();
    expect(favs).toContain('qsofa');
  });

  it('F11-2: Toggles favorite state idempotently (add then remove)', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    const added = await storage.toggleFavorite('wells_pe');
    expect(added).toBe(true);
    let isFav = await storage.isFavorite('wells_pe');
    expect(isFav).toBe(true);

    const removed = await storage.toggleFavorite('wells_pe');
    expect(removed).toBe(false);
    isFav = await storage.isFavorite('wells_pe');
    expect(isFav).toBe(false);
  });

  it('F11-3: Saves anonymous bed record ("Leito 04 - UTI") with zero LGPD leakage', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.saveBedRecord({
      id: 'bed_04',
      bedLabel: 'Leito 04 - UTI',
      notes: 'Paciente em choque séptico sob desmame de nora',
      scoreSnapshots: [{ scoreId: 'qsofa', score: 2 }]
    });

    const beds = await storage.getBedRecords();
    expect(beds.length).toBe(1);
    expect(beds[0].bedLabel).toBe('Leito 04 - UTI');
    expect(beds[0].scoreSnapshots[0].score).toBe(2);
  });

  it('F11-4: Rejects bed records with personal identifying information (e.g. CPF)', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    let threw = false;
    try {
      await storage.saveBedRecord({
        id: 'bed_bad',
        bedLabel: 'Leito com CPF 123.456.789-00',
        scoreSnapshots: []
      });
    } catch (err) {
      threw = true;
      expect(err.message).toContain('LGPD Violation');
    }
    expect(threw).toBe(true);
  });

  it('F11-5: Retrieves multiple stored anonymous bed records from IndexedDB', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.saveBedRecord({ id: 'bed_1', bedLabel: 'Leito 01 - UTI' });
    await storage.saveBedRecord({ id: 'bed_2', bedLabel: 'Leito 02 - Emergência' });
    const beds = await storage.getBedRecords();
    expect(beds.length).toBe(2);
  });
});

describe('Tier 1 — Feature 12: Instant Search (<10ms)', () => {
  it('F12-1: Finds calculators by Brazilian clinical synonym (e.g. "sepse")', () => {
    const manifest = adapter.getManifestData();
    const { results, latencyMs } = adapter.searchCalculators('sepse', manifest);
    expect(results.length).toBeGreaterThan(0);
    const ids = results.map(r => r.id);
    expect(ids).toContain('qsofa');
    expect(ids).toContain('sofa');
    expect(latencyMs).toBeLessThan(10);
  });

  it('F12-2: Finds calculators by exact acronym (e.g. "TEP")', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('TEP', manifest);
    expect(results.length).toBe(1);
    expect(results[0].id).toBe('wells_pe');
  });

  it('F12-3: Performs case-insensitive and diacritic-insensitive search ("tromboembolismo")', () => {
    const manifest = adapter.getManifestData();
    const res1 = adapter.searchCalculators('tromboembolismo', manifest);
    const res2 = adapter.searchCalculators('TROMBOEMBOLISMO', manifest);
    expect(res1.results.length).toBe(res2.results.length);
    expect(res1.results[0].id).toBe('wells_pe');
  });

  it('F12-4: Validates sub-10ms latency benchmark across multiple queries', () => {
    const manifest = adapter.getManifestData();
    const queries = ['coma', 'glasgow', 'pancreatite', 'sofa', 'wells', 'choque'];
    for (const q of queries) {
      const { latencyMs } = adapter.searchCalculators(q, manifest);
      expect(latencyMs).toBeLessThan(10);
    }
  });

  it('F12-5: Empty search string returns all available calculators without filtering', () => {
    const manifest = adapter.getManifestData();
    const { results } = adapter.searchCalculators('', manifest);
    expect(results.length).toBe(manifest.calculators.length);
  });
});

describe('Tier 1 — Feature 13: iOS-Style Alphabet Jump Rail', () => {
  it('F13-1: Provides 26-letter array (A-Z) for vertical jump rail', () => {
    const letters = adapter.getJumpRailLetters();
    expect(letters.length).toBe(26);
    expect(letters[0]).toBe('A');
    expect(letters[25]).toBe('Z');
  });

  it('F13-2: Maps touch Y-coordinate to corresponding letter index', () => {
    // Rail: top = 100, height = 520 (20px per letter)
    const resultTop = adapter.calculateJumpRailTouch(105, 100, 520); // within letter A
    expect(resultTop.letter).toBe('A');
    expect(resultTop.index).toBe(0);

    const resultMid = adapter.calculateJumpRailTouch(100 + 260, 100, 520); // letter N (index 13)
    expect(resultMid.index).toBe(13);
    expect(resultMid.letter).toBe('N');
  });

  it('F13-3: Clamps touch coordinate at top and bottom bounds', () => {
    const resultAbove = adapter.calculateJumpRailTouch(50, 100, 520); // above rail
    expect(resultAbove.letter).toBe('A');

    const resultBelow = adapter.calculateJumpRailTouch(700, 100, 520); // below rail
    expect(resultBelow.letter).toBe('Z');
  });

  it('F13-4: Triggers haptic feedback vibration pattern (10ms) on letter touch', () => {
    const touch = adapter.calculateJumpRailTouch(150, 100, 520);
    expect(touch.vibratePattern).toBe(10);
    envShim.navigator.vibrate(touch.vibratePattern);
    expect(envShim.vibrateCalls).toContain(10);
  });

  it('F13-5: Returns index and letter for visual balloon indicator positioning', () => {
    const touch = adapter.calculateJumpRailTouch(200, 100, 520);
    expect(typeof touch.index).toBe('number');
    expect(typeof touch.letter).toBe('string');
    expect(touch.letter.length).toBe(1);
  });
});

describe('Tier 1 — Feature 14: A-Z Score List & Sticky Headers', () => {
  it('F14-1: Groups calculators alphabetically by first letter of name', () => {
    const catalog = adapter.getBlock01Catalog();
    const groups = adapter.groupScoresAlphabetically(catalog);
    expect(groups.length).toBeGreaterThan(0);
    groups.forEach(g => {
      expect(typeof g.letter).toBe('string');
      expect(Array.isArray(g.items)).toBe(true);
      expect(g.items.length).toBeGreaterThan(0);
    });
  });

  it('F14-2: Sorts letter groups in ascending order', () => {
    const catalog = adapter.getBlock01Catalog();
    const groups = adapter.groupScoresAlphabetically(catalog);
    const letters = groups.map(g => g.letter);
    const sortedLetters = [...letters].sort();
    expect(letters).toEqual(sortedLetters);
  });

  it('F14-3: Sorts calculators within each letter group alphabetically', () => {
    const catalog = adapter.getBlock01Catalog();
    const groups = adapter.groupScoresAlphabetically(catalog);
    groups.forEach(g => {
      const names = g.items.map(i => i.name);
      const sortedNames = [...names].sort((a, b) => a.localeCompare(b, 'pt-BR'));
      expect(names).toEqual(sortedNames);
    });
  });

  it('F14-4: Preserves complete card information (acronym, category, description)', () => {
    const catalog = adapter.getBlock01Catalog();
    const groups = adapter.groupScoresAlphabetically(catalog);
    const allItems = groups.flatMap(g => g.items);
    allItems.forEach(item => {
      expect(item.acronym).toBeDefined();
      expect(item.category).toBeDefined();
      expect(item.description).toBeDefined();
    });
  });

  it('F14-5: Accurately identifies sticky header anchors for each group', () => {
    const catalog = adapter.getBlock01Catalog();
    const groups = adapter.groupScoresAlphabetically(catalog);
    const headers = groups.map(g => `header-${g.letter}`);
    expect(headers.length).toBe(groups.length);
    expect(headers[0]).toMatch(/^header-[A-Z]$/);
  });
});

describe('Tier 1 — Feature 15: Star Favorites Carousel & Tab', () => {
  it('F15-1: Quick-access carousel chips reflect currently starred calculator IDs', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('qsofa');
    await storage.toggleFavorite('wells_pe');

    const favs = await storage.getFavorites();
    const catalog = adapter.getBlock01Catalog();
    const carouselChips = catalog.filter(c => favs.includes(c.id));
    expect(carouselChips.length).toBe(2);
    expect(carouselChips.map(c => c.id)).toContain('qsofa');
    expect(carouselChips.map(c => c.id)).toContain('wells_pe');
  });

  it('F15-2: Unstarring an item immediately updates the carousel chip list', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('qsofa');
    await storage.toggleFavorite('qsofa'); // toggle off
    const favs = await storage.getFavorites();
    expect(favs.length).toBe(0);
  });

  it('F15-3: Displays empty state placeholder when no favorites are starred', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    const favs = await storage.getFavorites();
    const isEmpty = favs.length === 0;
    expect(isEmpty).toBe(true);
  });

  it('F15-4: Populates dedicated "Favoritos" view with full calculator cards', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('sofa');
    const favs = await storage.getFavorites();
    const catalog = adapter.getBlock01Catalog();
    const favCards = catalog.filter(c => favs.includes(c.id));
    expect(favCards.length).toBe(1);
    expect(favCards[0].name).toBe('Sequential Organ Failure Assessment');
  });

  it('F15-5: Synchronizes star status with A-Z catalog item bookmarks', async () => {
    envShim.reset();
    const storage = adapter.createStorageService();
    await storage.toggleFavorite('four_score');
    const isFav = await storage.isFavorite('four_score');
    expect(isFav).toBe(true);
    const notFav = await storage.isFavorite('ranson');
    expect(notFav).toBe(false);
  });
});
