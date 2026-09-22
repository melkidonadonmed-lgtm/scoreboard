import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import type { ManifestItem } from '@/types/clinical';
import defaultManifestRaw from '@/data/manifest.json';
import { AlphabetJumpRail, DEFAULT_ALPHABET } from './AlphabetJumpRail';
import { storageService } from '@/services/storageService';
import { Search, Star, X, Droplets, AlertTriangle } from 'lucide-react';

const defaultManifest = defaultManifestRaw as unknown as ManifestItem[];

export interface AzScoreListProps {
  items?: ManifestItem[];
  onSelectCalculator: (calculatorId: string) => void;
  initialFavorites?: string[];
  onToggleFavorite?: (calculatorId: string, isFav: boolean) => void;
  className?: string;
  showJumpRail?: boolean;
}

function normalizeSearchText(text: string): string {
  if (!text) return '';
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

/**
 * Derives the grouping letter from acronym or name.
 */
function getItemLetter(item: ManifestItem): string {
  const candidate = (item.acronym || item.name || '').trim();
  const cleaned = candidate.replace(/^[^a-zA-Z0-9]+/, '');
  if (!cleaned) return '#';
  const firstChar = cleaned[0].toUpperCase();
  return /[A-Z]/.test(firstChar) ? firstChar : '#';
}

export const AzScoreList: React.FC<AzScoreListProps> = ({
  items = defaultManifest,
  onSelectCalculator,
  initialFavorites,
  onToggleFavorite,
  className = '',
  showJumpRail = true,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [favoriteIds, setFavoriteIds] = useState<Set<string>>(new Set(initialFavorites || []));
  const [activeLetter, setActiveLetter] = useState<string>('A');
  const [searchLatencyMs, setSearchLatencyMs] = useState<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Sync favorites from storageService on mount
  useEffect(() => {
    let isMounted = true;
    if (!initialFavorites) {
      storageService
        .getFavorites()
        .then((favs) => {
          if (isMounted) setFavoriteIds(new Set(favs));
        })
        .catch(() => {});
    } else {
      setFavoriteIds(new Set(initialFavorites));
    }
    return () => {
      isMounted = false;
    };
  }, [initialFavorites]);

  // Pre-index search tokens for high-speed (<10ms) matching
  const searchableItems = useMemo(() => {
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
        letter: getItemLetter(item),
        indexedTokens: tokens,
      };
    });
  }, [items]);

  // Filter items in real time (<10ms latency)
  const filteredIndexed = useMemo(() => {
    const t0 = performance.now();
    const query = normalizeSearchText(searchQuery);

    let results = searchableItems;
    if (query) {
      const searchTerms = query.split(/\s+/).filter(Boolean);
      results = searchableItems.filter(({ indexedTokens }) =>
        searchTerms.every((term) => indexedTokens.includes(term))
      );
    }

    const latency = performance.now() - t0;
    setSearchLatencyMs(Number(latency.toFixed(2)));
    return results;
  }, [searchableItems, searchQuery]);

  // Group items by letter
  const groupedSections = useMemo(() => {
    const groups: Record<string, ManifestItem[]> = {};

    // Sort items by acronym/name
    const sorted = [...filteredIndexed].sort((a, b) => {
      const aKey = a.item.acronym || a.item.name;
      const bKey = b.item.acronym || b.item.name;
      return aKey.localeCompare(bKey, 'pt-BR');
    });

    for (const { item, letter } of sorted) {
      if (!groups[letter]) {
        groups[letter] = [];
      }
      groups[letter].push(item);
    }

    // Sort group keys alphabetically, with '#' last
    const sortedKeys = Object.keys(groups).sort((a, b) => {
      if (a === '#') return 1;
      if (b === '#') return -1;
      return a.localeCompare(b);
    });

    return sortedKeys.map((letter) => ({
      letter,
      items: groups[letter],
    }));
  }, [filteredIndexed]);

  const availableLetters = useMemo(() => {
    return groupedSections.map((g) => g.letter);
  }, [groupedSections]);

  // Jump Rail navigation handler
  const handleSelectLetter = useCallback(
    (targetLetter: string) => {
      setActiveLetter(targetLetter);

      // Check if target letter section exists
      let targetEl = document.getElementById(`letter-section-${targetLetter}`);

      // If not directly found, jump to closest next letter
      if (!targetEl && availableLetters.length > 0) {
        const nextLetter = availableLetters.find((l) => l >= targetLetter) || availableLetters[0];
        targetEl = document.getElementById(`letter-section-${nextLetter}`);
      }

      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },
    [availableLetters]
  );

  // Toggle favorite with optimistic UI and storageService
  const handleToggleFavorite = async (calculatorId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const wasFavorite = favoriteIds.has(calculatorId);
    const nextFavorites = new Set(favoriteIds);

    if (wasFavorite) {
      nextFavorites.delete(calculatorId);
    } else {
      nextFavorites.add(calculatorId);
    }
    setFavoriteIds(nextFavorites);

    try {
      await storageService.toggleFavorite(calculatorId);
      onToggleFavorite?.(calculatorId, !wasFavorite);
    } catch (err) {
      // Revert on error
      setFavoriteIds(favoriteIds);
      console.error('Falha ao alternar favorito:', err);
    }
  };

  return (
    <div ref={containerRef} className={`relative flex flex-col w-full ${className}`}>
      {/* Search Bar Header */}
      <div className="sticky top-0 z-20 backdrop-blur-md bg-surface-light/95 dark:bg-surface-dark/95 border-b border-subtle-light dark:border-subtle-dark px-4 py-3 space-y-2 transition-colors">
        <div className="relative flex items-center">
          <div className="absolute left-3.5 text-slate-400 dark:text-slate-500 pointer-events-none">
            <Search className="w-4 h-4" />
          </div>

          <input
            type="text"
            role="searchbox"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Buscar escore, sigla ou sintoma (sepse, choque, TEP)..."
            className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-canvas-light dark:bg-canvas-dark border border-subtle-light dark:border-subtle-dark text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 transition-all"
            aria-label="Buscar escores clínicos"
          />

          {searchQuery && (
            <button
              type="button"
              onClick={() => setSearchQuery('')}
              className="absolute right-3 p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
              aria-label="Limpar busca"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Search status & count */}
        <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 px-1">
          <span>
            {filteredIndexed.length}{' '}
            {filteredIndexed.length === 1 ? 'escore clínico' : 'escores clínicos'}
          </span>
          {searchLatencyMs !== null && (
            <span className="font-mono text-[10px] text-slate-400 dark:text-slate-500">
              {searchLatencyMs < 1 ? '< 1ms' : `${searchLatencyMs}ms`}
            </span>
          )}
        </div>
      </div>

      {/* Main Content Area: Grouped List + Jump Rail */}
      <div className="relative flex-1 flex">
        {/* Scrollable A-Z Grouped Items */}
        <div className="flex-1 min-w-0 px-4 py-3 space-y-5">
          {groupedSections.length === 0 ? (
            <div className="text-center py-12 px-4 space-y-3">
              <div className="w-12 h-12 mx-auto rounded-2xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                <Search className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                Nenhum escore encontrado
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 max-w-xs mx-auto">
                Não encontramos resultados para &ldquo;{searchQuery}&rdquo;. Tente buscar por
                termos como <span className="font-semibold">sepse</span>,{' '}
                <span className="font-semibold">choque</span>,{' '}
                <span className="font-semibold">TEP</span>,{' '}
                <span className="font-semibold">coma</span> ou{' '}
                <span className="font-semibold">glasgow</span>.
              </p>
            </div>
          ) : (
            groupedSections.map(({ letter, items: groupItems }) => (
              <section key={letter} aria-labelledby={`letter-heading-${letter}`} className="space-y-2.5">
                {/* Sticky Alphabet Section Header */}
                <div
                  id={`letter-section-${letter}`}
                  className="sticky top-20 z-10 py-1.5 px-3 rounded-xl backdrop-blur-md bg-canvas-light/90 dark:bg-canvas-dark/90 border border-subtle-light/60 dark:border-subtle-dark/60 flex items-center justify-between shadow-xs transition-colors"
                >
                  <span
                    id={`letter-heading-${letter}`}
                    className="text-xs font-black text-brand-600 dark:text-brand-400 uppercase tracking-wider"
                  >
                    {letter}
                  </span>
                  <span className="text-[10px] font-medium text-slate-400 dark:text-slate-500">
                    {groupItems.length} {groupItems.length === 1 ? 'item' : 'itens'}
                  </span>
                </div>

                {/* Score Cards in Group */}
                <div className="space-y-2.5">
                  {groupItems.map((item) => {
                    const isStarred = favoriteIds.has(item.id);

                    return (
                      <div
                        key={item.id}
                        role="button"
                        tabIndex={0}
                        onClick={() => onSelectCalculator(item.id)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            onSelectCalculator(item.id);
                          }
                        }}
                        className="group relative p-3.5 rounded-2xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark shadow-card active:scale-[0.99] hover:border-brand-500/40 dark:hover:border-brand-400/40 transition-all cursor-pointer min-h-touch flex flex-col justify-between"
                      >
                        {/* Top Row: Acronym, Name, and Star Button */}
                        <div className="flex items-start justify-between gap-2">
                          <div className="min-w-0 flex-1">
                            <div className="flex items-center space-x-2 flex-wrap gap-y-1">
                              <h3 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
                                {item.acronym || item.name}
                              </h3>
                              {item.badge && (
                                <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-brand-500/10 text-brand-600 dark:text-brand-400">
                                  {item.badge}
                                </span>
                              )}
                              {item.hasInfusionProtocol && (
                                <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-clinical-info/10 text-clinical-info">
                                  <Droplets className="w-2.5 h-2.5 mr-1" />
                                  BIC
                                </span>
                              )}
                              {item.id === 'calc_qsofa' && (
                                <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-clinical-warning/15 text-clinical-warning">
                                  <AlertTriangle className="w-2.5 h-2.5 mr-0.5" />
                                  SSC 2021
                                </span>
                              )}
                            </div>

                            <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-1 mt-0.5">
                              {item.name}
                            </p>
                          </div>

                          {/* 48px Accessible Star Button */}
                          <button
                            type="button"
                            aria-label={
                              isStarred
                                ? `Remover ${item.acronym} dos favoritos`
                                : `Adicionar ${item.acronym} aos favoritos`
                            }
                            onClick={(e) => handleToggleFavorite(item.id, e)}
                            className="min-w-touch min-h-touch -mr-2 -mt-2 flex items-center justify-center rounded-xl text-slate-400 hover:text-amber-500 active:scale-90 transition-transform"
                          >
                            <Star
                              className={`w-5 h-5 transition-colors ${
                                isStarred
                                  ? 'fill-amber-400 text-amber-500'
                                  : 'text-slate-400 dark:text-slate-500'
                              }`}
                            />
                          </button>
                        </div>

                        {/* Summary / Indication */}
                        <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-2 mt-2 leading-relaxed">
                          {item.summary || item.description}
                        </p>

                        {/* Bottom Metadata Badges */}
                        <div className="flex items-center space-x-2 mt-2.5 pt-2 border-t border-subtle-light/60 dark:border-subtle-dark/60 text-[10px] text-slate-400 dark:text-slate-500">
                          <span className="truncate max-w-[180px]">
                            {item.moduleName || item.categoryName}
                          </span>
                          <span>•</span>
                          <span className="shrink-0">{item.evidenceSource}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            ))
          )}
        </div>

        {/* Right-Hand Jump Rail (Fixed in viewport or sticky to list) */}
        {showJumpRail && (
          <aside
            aria-label="Atalho alfabético"
            className="sticky top-20 right-0 self-start pr-1 pl-0.5 shrink-0"
          >
            <AlphabetJumpRail
              letters={DEFAULT_ALPHABET}
              activeLetter={activeLetter}
              availableLetters={availableLetters}
              onSelectLetter={handleSelectLetter}
            />
          </aside>
        )}
      </div>
    </div>
  );
};
