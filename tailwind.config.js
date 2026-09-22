/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        canvas: {
          light: '#f8fafc',
          dark: '#090d16',
        },
        surface: {
          light: '#ffffff',
          dark: '#131b2e',
          raised: {
            light: '#f1f5f9',
            dark: '#1e293b',
          },
        },
        subtle: {
          light: '#e2e8f0',
          dark: '#1e293b',
        },
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        clinical: {
          stable: '#10b981',   // Baixo risco / Higidez
          alert: '#f59e0b',    // Risco moderado / Atenção
          critical: '#ef4444', // Alto risco / Crítico
          info: '#2563eb',     // Ações primárias / Info
        },
      },
      boxShadow: {
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02)',
        'card-hover': '0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.04)',
        'card-dark': '0 4px 20px -2px rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.08)',
        'bevel': 'inset 0 1px 1px rgba(255, 255, 255, 0.6)',
        'bevel-dark': 'inset 0 1px 1px rgba(255, 255, 255, 0.18)',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'SF Pro Text', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Menlo', 'monospace'],
      },
      minHeight: {
        'touch': '48px',
      },
      minWidth: {
        'touch': '48px',
      },
    },
  },
  plugins: [],
};
