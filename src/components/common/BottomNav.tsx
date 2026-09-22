import React from 'react';
import { LayoutList, Star, BedDouble, Droplets } from 'lucide-react';

export type TabType = 'catalog' | 'favorites' | 'beds' | 'infusions';

export interface NavItemConfig {
  id: TabType;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  badgeCount?: number;
}

export interface BottomNavProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
  favoritesCount?: number;
  bedsCount?: number;
  className?: string;
}

/**
 * 4-Tab Bottom Navigation Bar for Mobile Viewports.
 * Tabs:
 * 1. "Todos" (Catalog A-Z)
 * 2. "Favoritos" (Quick Pins & Favorites)
 * 3. "Leitos" (Anonymous Local Beds)
 * 4. "Plantão" (Bedside BIC Micro-Calculators)
 *
 * Meets 48px touch targets, safe area inset padding, and tactile active highlights.
 */
export const BottomNav: React.FC<BottomNavProps> = ({
  activeTab,
  onTabChange,
  favoritesCount = 0,
  bedsCount = 0,
  className = ''
}) => {
  const tabs: NavItemConfig[] = [
    {
      id: 'catalog',
      label: 'Todos',
      icon: LayoutList
    },
    {
      id: 'favorites',
      label: 'Favoritos',
      icon: Star,
      badgeCount: favoritesCount > 0 ? favoritesCount : undefined
    },
    {
      id: 'beds',
      label: 'Leitos',
      icon: BedDouble,
      badgeCount: bedsCount > 0 ? bedsCount : undefined
    },
    {
      id: 'infusions',
      label: 'Plantão',
      icon: Droplets
    }
  ];

  return (
    <nav
      className={`fixed bottom-0 left-0 right-0 z-30 bg-surface-light/95 dark:bg-surface-dark/95 backdrop-blur-md border-t border-subtle-light dark:border-subtle-dark pb-safe transition-colors duration-200 ${className}`}
      aria-label="Navegação Principal"
      data-testid="bottom-nav"
    >
      <div className="max-w-md mx-auto grid grid-cols-4 px-2 py-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => onTabChange(tab.id)}
              className={`relative flex flex-col items-center justify-center min-h-touch py-1.5 px-1 rounded-xl transition-all duration-200 select-none ${
                isActive
                  ? 'text-brand-600 dark:text-brand-400 font-bold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
              aria-selected={isActive}
              aria-label={tab.label}
              data-testid={`tab-${tab.id}`}
            >
              {/* Active pill background indicator */}
              {isActive && (
                <span className="absolute inset-x-2 inset-y-1 bg-brand-500/10 dark:bg-brand-400/15 rounded-xl -z-10" />
              )}

              {/* Icon Container with Optional Badge */}
              <div className="relative flex items-center justify-center">
                <Icon
                  className={`w-5 h-5 transition-transform duration-200 ${
                    isActive ? 'scale-110 stroke-[2.4]' : 'scale-100'
                  }`}
                />
                {tab.badgeCount !== undefined && tab.badgeCount > 0 && (
                  <span
                    className={`absolute -top-1.5 -right-2.5 px-1.5 py-0.2 rounded-full text-[9px] font-black leading-tight tabular-nums shadow-sm ${
                      isActive
                        ? 'bg-brand-500 text-white'
                        : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                    }`}
                  >
                    {tab.badgeCount > 99 ? '99+' : tab.badgeCount}
                  </span>
                )}
              </div>

              {/* Label */}
              <span className="text-[10px] tracking-tight mt-1 line-clamp-1">
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNav;
