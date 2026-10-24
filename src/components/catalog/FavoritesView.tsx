import React, { useState, useEffect, useMemo } from 'react';
import type { ManifestItem } from '@/types/clinical';
import defaultManifestRaw from '@/data/manifest.json';
import { storageService } from '@/services/storageService';
import { Star, Search, X, Droplets, AlertTriangle, BookmarkPlus, ChevronRight } from 'lucide-react';

const defaultManifest = defaultManifestRaw as unknown as ManifestItem[];

/**
 * 1. QuickFavoritesCarousel
 * Compact horizontal scrollable chip bar for immediate 1-tap bedside access.
 */
export interface QuickFavoritesCarouselProps {
  favorites?: string[];
  items?: ManifestItem[];
  onSelectCalculator: (calculatorId: string) => void;
  onRemoveFavorite?: (calculatorId: string) => void;
  className?: string;
}

export const QuickFavoritesCarousel: React.FC<QuickFavoritesCarouselProps> = ({
  favorites,
  items = defaultManifest,
  onSelectCalculator,
  className = '',
}) => {
  const [favoriteIds, setFavoriteIds] = useState<string[]>(favorites || []);

  useEffect(() => {
    if (favorites !== undefined) {
      setFavoriteIds(favorites);
    } else {
      let isMounted = true;
      storageService
        .getFavorites()
        .then((favs) => {
          if (isMounted) setFavoriteIds(favs);
        })
        .catch(() => {});
      return () => {
        isMounted = false;
      };
    }
  }, [favorites]);

  const favoritedItems = useMemo(() => {
    const itemMap = new Map(items.map((it) => [it.id, it]));
    return favoriteIds
      .map((id) => itemMap.get(id))
      .filter((it): it is ManifestItem => Boolean(it));
  }, [items, favoriteIds]);

  if (favoritedItems.length === 0) {
    return (
      <div
        className={`w-full overflow-x-auto no-scrollbar py-1.5 px-3 rounded-lg border border-subtle-light/60 dark:border-subtle-dark/60 bg-surface-raised-light/50 dark:bg-surface-raised-dark/50 ${className}`}
      >
        <div className="flex items-center space-x-2 text-[11px] text-slate-400 dark:text-slate-500">
          <BookmarkPlus className="w-3.5 h-3.5 text-amber-500/80 shrink-0" />
          <span className="truncate">
            Acesso Rápido: marque a estrela nos escores mais usados no plantão.
          </span>
        </div>
      </div>
    );
  }

  return (
    <div
      role="region"
      aria-label="Carrossel de Favoritos Rápidos"
      className={`w-full overflow-x-auto no-scrollbar py-1 px-1 ${className}`}
    >
      <div className="flex items-center space-x-1.5 min-w-max">
        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mr-1 flex items-center">
          <Star className="w-3 h-3 text-amber-500 fill-amber-400 mr-1" />
          Fixados:
        </span>

        {favoritedItems.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => onSelectCalculator(item.id)}
            className="group inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark hover:border-amber-500/50 dark:hover:border-amber-400/50 shadow-xs active:scale-95 transition-all text-left"
          >
            <span className="text-[11px] font-bold text-slate-900 dark:text-white group-hover:text-amber-600 dark:group-hover:text-amber-400">
              {item.acronym || item.name}
            </span>

            {item.hasInfusionProtocol && (
              <span className="w-1.5 h-1.5 rounded-full bg-clinical-info" title="Protocolo BIC disponível" />
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

/**
 * 2. FavoritesView
 * Compact full-page tab displaying all favorited calculators.
 */
export interface FavoritesViewProps {
  items?: ManifestItem[];
  onSelectCalculator: (calculatorId: string) => void;
  onNavigateToCatalog?: () => void;
  className?: string;
}

export const FavoritesView: React.FC<FavoritesViewProps> = ({
  items = defaultManifest,
  onSelectCalculator,
  onNavigateToCatalog,
  className = '',
}) => {
  const [favoriteIds, setFavoriteIds] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setIsLoading(true);
    storageService
      .getFavorites()
      .then((favs) => {
        if (isMounted) {
          setFavoriteIds(new Set(favs));
          setIsLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const favoritedItems = useMemo(() => {
    const itemMap = new Map(items.map((it) => [it.id, it]));
    const result: ManifestItem[] = [];
    favoriteIds.forEach((id) => {
      const item = itemMap.get(id);
      if (item) result.push(item);
    });

    return result.sort((a, b) => (a.acronym || a.name).localeCompare(b.acronym || b.name, 'pt-BR'));
  }, [items, favoriteIds]);

  const filteredFavorites = useMemo(() => {
    if (!searchQuery.trim()) return favoritedItems;
    const query = searchQuery
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();

    return favoritedItems.filter((item) => {
      const combined = [
        item.name,
        item.acronym,
        item.category || '',
        item.summary || '',
        ...(item.synonyms || []),
      ]
        .join(' ')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase();

      return combined.includes(query);
    });
  }, [favoritedItems, searchQuery]);

  const handleRemoveFavorite = async (calculatorId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const nextSet = new Set(favoriteIds);
    nextSet.delete(calculatorId);
    setFavoriteIds(nextSet);

    try {
      await storageService.removeFavorite(calculatorId);
    } catch (err) {
      setFavoriteIds(favoriteIds);
      console.error('Falha ao remover favorito:', err);
    }
  };

  if (isLoading) {
    return (
      <div className={`flex items-center justify-center py-12 text-slate-400 max-w-md mx-auto ${className}`}>
        <span className="text-xs">Carregando favoritos...</span>
      </div>
    );
  }

  if (favoriteIds.size === 0) {
    return (
      <div className={`p-6 text-center space-y-3.5 max-w-md mx-auto ${className}`}>
        <div className="w-12 h-12 mx-auto rounded-2xl bg-amber-500/10 text-amber-500 flex items-center justify-center">
          <Star className="w-6 h-6 fill-amber-400 text-amber-500" />
        </div>

        <div className="space-y-1.5">
          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Nenhum escore favoritado
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-xs mx-auto">
            Toque no ícone de estrela ao lado de qualquer escore clínico no Catálogo A-Z para fixá-lo
            nesta aba durante os plantões.
          </p>
        </div>

        {onNavigateToCatalog && (
          <button
            type="button"
            onClick={onNavigateToCatalog}
            className="inline-flex items-center justify-center min-h-touch px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold shadow-card transition-colors active:scale-98"
          >
            Explorar Catálogo A-Z
          </button>
        )}
      </div>
    );
  }

  return (
    <div className={`flex flex-col w-full max-w-md mx-auto px-3.5 py-3 space-y-3 ${className}`}>
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Star className="w-4 h-4 text-amber-500 fill-amber-400" />
            <h2 className="text-sm font-bold text-slate-900 dark:text-white">
              Escores Favoritos
            </h2>
          </div>
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-600 dark:text-amber-400 tabular-nums">
            {favoriteIds.size} {favoriteIds.size === 1 ? 'escore' : 'escores'}
          </span>
        </div>

        {favoriteIds.size >= 2 && (
          <div className="relative flex items-center">
            <div className="absolute left-3 text-slate-400 dark:text-slate-500 pointer-events-none">
              <Search className="w-3.5 h-3.5" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filtrar favoritos..."
              className="w-full pl-8 pr-8 py-1.5 rounded-xl bg-surface-light dark:bg-surface-dark border border-subtle-light dark:border-subtle-dark text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
              aria-label="Filtrar escores favoritos"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 p-1 text-slate-400 hover:text-slate-600"
                aria-label="Limpar filtro"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        )}
      </div>

      {/* Compact Favorited Rows */}
      <div className="space-y-1.5">
        {filteredFavorites.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-400">
            Nenhum favorito encontrado para &ldquo;{searchQuery}&rdquo;.
          </div>
        ) : (
          filteredFavorites.map((item) => {
            const primaryTitle = item.acronym || item.name;
            const secondaryTitle =
              item.acronym && item.name && item.name !== item.acronym ? item.name : null;

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
                className="group relative px-3 py-2 rounded-xl bg-surface-light dark:bg-surface-dark border border-subtle-light/90 dark:border-subtle-dark/90 shadow-xs hover:shadow-card hover:border-amber-500/40 dark:hover:border-amber-400/40 hover:translate-x-0.5 active:scale-[0.99] transition-spring cursor-pointer flex items-center justify-between gap-2 min-w-0 overflow-hidden"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <h3 className="text-sm font-bold text-slate-900 dark:text-white tracking-tight shrink-0">
                      {primaryTitle}
                    </h3>

                    {secondaryTitle && (
                      <span className="text-[11px] text-slate-400 dark:text-slate-500 truncate flex-1 min-w-0">
                        — {secondaryTitle}
                      </span>
                    )}

                    {item.hasInfusionProtocol && (
                      <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[9px] font-bold bg-clinical-info/10 text-clinical-info border border-clinical-info/20 shrink-0">
                        <Droplets className="w-2.5 h-2.5 mr-0.5" />
                        BIC
                      </span>
                    )}

                    {item.id === 'calc_qsofa' && (
                      <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[9px] font-bold bg-clinical-warning/15 text-clinical-warning border border-clinical-warning/25 shrink-0">
                        <AlertTriangle className="w-2.5 h-2.5 mr-0.5" />
                        SSC
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-1 mt-0.5 leading-snug">
                    {item.summary || item.description}
                  </p>
                </div>

                <div className="flex items-center shrink-0 -mr-1">
                  <button
                    type="button"
                    aria-label={`Remover ${item.acronym} dos favoritos`}
                    onClick={(e) => handleRemoveFavorite(item.id, e)}
                    className="w-9 h-9 flex items-center justify-center rounded-lg text-amber-500 hover:text-slate-400 active:scale-90 transition-transform"
                  >
                    <Star className="w-4 h-4 fill-amber-400 text-amber-500" />
                  </button>
                  <ChevronRight className="w-4 h-4 text-slate-300 dark:text-slate-600 group-hover:text-amber-500 group-hover:translate-x-0.5 transition-all" />
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
