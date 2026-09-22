import React, { useEffect, useState } from 'react';
import { Sun, Moon } from 'lucide-react';

export type Theme = 'light' | 'dark';

export interface ThemeToggleProps {
  className?: string;
  showLabel?: boolean;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ className = '', showLabel = false }) => {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'light';
    try {
      const saved = localStorage.getItem('theme') as Theme | null;
      if (saved === 'dark' || saved === 'light') return saved;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } catch {
      return 'light';
    }
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    try {
      localStorage.setItem('theme', theme);
    } catch {
      // Ignore localStorage errors in private mode
    }
  }, [theme]);

  // Listen for system theme changes if user has not stored explicit preference
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      try {
        const saved = localStorage.getItem('theme');
        if (!saved) {
          setTheme(e.matches ? 'dark' : 'light');
        }
      } catch {
        setTheme(e.matches ? 'dark' : 'light');
      }
    };

    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } else if ((mediaQuery as any).addListener) {
      (mediaQuery as any).addListener(handleChange);
      return () => (mediaQuery as any).removeListener(handleChange);
    }
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const isDark = theme === 'dark';

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className={`relative inline-flex items-center justify-center p-2.5 rounded-xl min-w-touch min-h-touch text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light dark:border-subtle-dark shadow-sm hover:shadow-card transition-all duration-200 active:scale-95 focus:outline-none focus:ring-2 focus:ring-brand-500/50 ${className}`}
      aria-label={isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
      title={isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
    >
      <div className="relative w-5 h-5 flex items-center justify-center overflow-hidden">
        <Sun
          className={`w-5 h-5 text-amber-500 transition-all duration-300 transform ${
            isDark ? '-rotate-90 scale-0 opacity-0 absolute' : 'rotate-0 scale-100 opacity-100'
          }`}
          aria-hidden="true"
        />
        <Moon
          className={`w-5 h-5 text-indigo-400 transition-all duration-300 transform ${
            isDark ? 'rotate-0 scale-100 opacity-100' : 'rotate-90 scale-0 opacity-0 absolute'
          }`}
          aria-hidden="true"
        />
      </div>
      {showLabel && (
        <span className="ml-2 text-xs font-medium select-none">
          {isDark ? 'Escuro' : 'Claro'}
        </span>
      )}
    </button>
  );
};

export default ThemeToggle;
