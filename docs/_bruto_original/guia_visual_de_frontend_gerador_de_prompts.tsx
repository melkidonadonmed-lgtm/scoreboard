import React, { useState, useMemo } from 'react';
import { 
  Sparkles, 
  Smartphone, 
  Layers, 
  Atom, 
  Wind, 
  Zap, 
  Copy, 
  Check, 
  Sliders, 
  Monitor, 
  Palette, 
  BookOpen, 
  Code2, 
  ChevronRight, 
  Menu, 
  X, 
  Sun, 
  Moon, 
  Info, 
  ShieldCheck, 
  CornerDownRight, 
  Layout, 
  MousePointerClick, 
  Terminal, 
  Maximize2 
} from 'lucide-react';

const GLOSSARY_ITEMS = [
  {
    id: 'mobile-first',
    title: 'Mobile First',
    tag: 'Arquitetura CSS / Layout',
    icon: Smartphone,
    summary: 'Projetar a experiência e o CSS primeiro para telas compactas (320px - 480px) e expandir gradativamente para tablets e desktops usando min-width.',
    whyImportant: 'Garante performance extrema em redes móveis e evita que a UI mobile seja uma versão "remendada" ou quebrada do desktop.',
    codeExample: `/* No Tailwind: sem prefixo = mobile, prefixo = desktop */
<div className="w-full flex-col md:flex-row md:space-x-4">
  <div className="text-sm md:text-base font-medium">Responsivo</div>
</div>`,
    goodPromptTip: 'Sempre declare: "Desenvolva com abordagem Mobile-First estrita, testado a partir de 360px de largura e adaptando fluentemente com breakpoints md e lg."'
  },
  {
    id: 'react-components',
    title: 'Componentização Modular & Estado',
    tag: 'Ecossistema React',
    icon: Atom,
    summary: 'Dividir a interface em blocos autônomos, reutilizáveis e com responsabilidade única (Single Responsibility), controlados por reatividade de estado.',
    whyImportant: 'Impede o efeito cascata de erros, viabiliza manutenção a longo prazo e sincroniza o DOM instantaneamente quando dados mudam.',
    codeExample: `// Estado local previsível e props declarativas
function MetricCard({ title, value, icon: Icon }) {
  const [active, setActive] = useState(false);
  return (
    <button onClick={() => setActive(!active)} className="p-4 rounded-xl border">
      <Icon className="w-5 h-5" />
      <span>{title}: {value}</span>
    </button>
  );
}`,
    goodPromptTip: 'Peça: "Crie componentes modulares, puros e isolados, com tipagem e hooks desacoplados para gerenciamento de estado previsível."'
  },
  {
    id: 'tailwind-tokens',
    title: 'Tailwind CSS & Design Tokens',
    tag: 'Estilização Utilitária',
    icon: Wind,
    summary: 'Framework CSS orientado a utilitários diretos no markup com base em uma escala padronizada de espaçamentos, tipografia, cores e sombras.',
    whyImportant: 'Elimina arquivos CSS gigantes paralelos, previne conflitos de especificidade e acelera o tempo de iteração de UI em até 5x.',
    codeExample: `<!-- Classes utilitárias semânticas e consistentes -->
<button className="bg-cyan-500 hover:bg-cyan-400 active:scale-95 text-slate-950 px-4 py-2 rounded-lg font-semibold shadow-lg shadow-cyan-500/25 transition-all">
  Executar Ação
</button>`,
    goodPromptTip: 'Especifique: "Use Tailwind CSS v3+. Favoreça classes semânticas, bordas suaves (rounded-xl), e paleta com contraste WCAG AA mínimo."'
  },
  {
    id: 'vite-esm',
    title: 'Vite & Bundlers Modernos',
    tag: 'Build & Tooling',
    icon: Zap,
    summary: 'Ferramenta de build de última geração que usa Native ES Modules durante o desenvolvimento para Hot Module Replacement (HMR) quase instantâneo.',
    whyImportant: 'Ambiente de desenvolvimento sem espera de bundling prévio, iniciando projetos em milissegundos independente do tamanho da base de código.',
    codeExample: `// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 3000 }
});`,
    goodPromptTip: 'Peça: "Configure ambiente com Vite + React + Tailwind CSS para compilação ultrarrápida e suporte a HMR."'
  },
  {
    id: 'mcp-apis',
    title: 'APIs, Hooks e MCP (Model Context)',
    tag: 'Integração & Agentes',
    icon: Layers,
    summary: 'Camada de comunicação entre a interface visual e os serviços externos ou LLMs, através de chamadas REST/GraphQL ou protocolos padronizados como MCP.',
    whyImportant: 'Garante que a UI reflita estados de carregamento (loading), erro (error state) e dados em cache sem congelar a experiência do usuário.',
    codeExample: `// Exemplo de chamada resiliente com feedback visual
const [state, setState] = useState({ data: null, loading: false, error: null });
async function fetchData() {
  setState(s => ({ ...s, loading: true }));
  try {
    const res = await fetch('/api/tools/weather');
    setState({ data: await res.json(), loading: false, error: null });
  } catch (err) {
    setState({ data: null, loading: false, error: err.message });
  }
}`,
    goodPromptTip: 'Indique no prompt: "Implemente estados visuais completos para requisições: loading spinner/skeleton, empty state amigável e tratamento de erros."'
  }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('lab'); // 'glossary', 'lab', 'prompt-generator', 'checklist'
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  // Interactive Playground State
  const [selectedShadow, setSelectedShadow] = useState('shadow-xl');
  const [activeNavStyle, setActiveNavStyle] = useState('tabs');
  const [copiedId, setCopiedId] = useState(null);

  // Generator Config State
  const [genAppType, setGenAppType] = useState('Dashboard Analítico');
  const [genFramework, setGenFramework] = useState('React (Vite)');
  const [genStyling, setGenStyling] = useState('Tailwind CSS');
  const [genTheme, setGenTheme] = useState('Dark Minimalista (Ciano / Slate)');
  const [genArchitecture, setGenArchitecture] = useState('Mobile-First Rigoroso');
  const [genFeatures, setGenFeatures] = useState([
    'Responsividade fluida (Mobile ao 4K)',
    'Micro-interações táteis e feedback sonoro visual',
    'Componente isolado em arquivo único sem dependências externas'
  ]);
  const [customFeature, setCustomFeature] = useState('');

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const toggleFeature = (feat) => {
    if (genFeatures.includes(feat)) {
      setGenFeatures(genFeatures.filter(f => f !== feat));
    } else {
      setGenFeatures([...genFeatures, feat]);
    }
  };

  const addCustomFeature = (e) => {
    e.preventDefault();
    if (customFeature.trim() && !genFeatures.includes(customFeature.trim())) {
      setGenFeatures([...genFeatures, customFeature.trim()]);
      setCustomFeature('');
    }
  };

  const generatedPrompt = useMemo(() => {
    return `Você é um Engenheiro de Software Frontend Sênior e Especialista em UI/UX.

## OBJETIVO
Construa a interface completa e funcional de um(a) **${genAppType}**.

## STACK TECNOLÓGICA E TOOLING
- Framework: ${genFramework}
- Estilização: ${genStyling}
- Padrão Visual: ${genTheme}
- Filosofia de Layout: ${genArchitecture}

## REQUISITOS OBRIGATÓRIOS
${genFeatures.map((f, idx) => `${idx + 1}. ${f}`).join('\n')}

## DIRETRIZES DE DESIGN SYSTEM E TOKENS
- Botões: Variantes Primary, Secondary e Ghost com transições suaves (transition-all duration-200) e estados de active (active:scale-95).
- Sombras & Elevação: Sistema de camadas hierárquicas usando sombras sutis (ex: shadow-md, shadow-cyan-500/10) para distinguir cartões do plano de fundo.
- Acessibilidade: Contraste mínimo WCAG AA, tags semânticas (header, nav, main, section, button) e foco visível em navegação por teclado.
- Feedback de Ações: Estados vazios (Empty States), animações de clique e indicadores de carregamento claros.

## RESTRIÇÕES E ANTI-PADRÕES
- NÃO use alerts nativos do navegador (alert() ou confirm()). Crie modais, banners ou toasts estilizados.
- NÃO crie layouts rígidos com larguras fixas em pixels (ex: w-[1200px]) que causem overflow horizontal no mobile.
- NÃO deixe botões ou links interativos sem feedback visual de hover/foco.
- Entregue o código completo, 100% executável, autossuficiente em arquivo único, pronto para compilar e testar.`;
  }, [genAppType, genFramework, genStyling, genTheme, genArchitecture, genFeatures]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased selection:bg-cyan-500 selection:text-slate-950">
      {}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/80 border-b border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 ring-1 ring-white/20">
              <Sparkles className="w-5 h-5 text-slate-950 font-bold" />
            </div>
            <div>
              <span className="text-base font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
                FrontCraft Master
              </span>
              <span className="hidden sm:inline-block ml-2 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded-full">
                Guia Visual & Prompt Studio
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800">
            <button
              onClick={() => setActiveTab('lab')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'lab'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/25'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Sliders className="w-4 h-4" />
              <span>Laboratório de UI</span>
            </button>
            <button
              onClick={() => setActiveTab('glossary')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'glossary'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/25'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Dicionário & Conceitos</span>
            </button>
            <button
              onClick={() => setActiveTab('prompt-generator')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'prompt-generator'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/25'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Terminal className="w-4 h-4" />
              <span>Gerador de Prompts</span>
            </button>
            <button
              onClick={() => setActiveTab('checklist')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'checklist'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/25'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Anatomia do Pedido</span>
            </button>
          </nav>

          {/* Mobile Menu Toggle */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden px-4 pt-2 pb-4 space-y-2 bg-slate-900 border-b border-slate-800">
            <button
              onClick={() => { setActiveTab('lab'); setMobileMenuOpen(false); }}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium ${
                activeTab === 'lab' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-300'
              }`}
            >
              <Sliders className="w-4 h-4" />
              <span>Laboratório de UI</span>
            </button>
            <button
              onClick={() => { setActiveTab('glossary'); setMobileMenuOpen(false); }}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium ${
                activeTab === 'glossary' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-300'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Dicionário & Conceitos</span>
            </button>
            <button
              onClick={() => { setActiveTab('prompt-generator'); setMobileMenuOpen(false); }}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium ${
                activeTab === 'prompt-generator' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-300'
              }`}
            >
              <Terminal className="w-4 h-4" />
              <span>Gerador de Prompts</span>
            </button>
            <button
              onClick={() => { setActiveTab('checklist'); setMobileMenuOpen(false); }}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium ${
                activeTab === 'checklist' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-300'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Anatomia do Pedido</span>
            </button>
          </div>
        )}
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {}
        {activeTab === 'lab' && (
          <div className="space-y-12">
            {/* Banner Intro */}
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950 p-8 border border-slate-800 shadow-2xl">
              <div className="max-w-3xl space-y-4">
                <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold uppercase tracking-wider">
                  <MousePointerClick className="w-3.5 h-3.5" />
                  <span>Laboratório Interativo de Design Tokens</span>
                </div>
                <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
                  Experimente os Componentes na Prática
                </h1>
                <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
                  Veja a diferença tátil entre os estilos que você pede nos prompts: variantes de botões, elevações com sombras e menus de navegação modernos.
                </p>
              </div>
            </div>

            {/* Visual Buttons Laboratory */}
            <section className="space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                  <Palette className="w-5 h-5 text-cyan-400" />
                  <span>1. Variantes de Botões e Micro-Interações</span>
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Passe o mouse (hover) e clique (active) para sentir as diferenças de feedback táctil e semântica.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Primary Solid */}
                <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-4 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">Primary (Sólido Ciano)</span>
                    <p className="text-xs text-slate-400 mt-1">Ação principal de maior destaque na tela (CTA).</p>
                  </div>
                  <div className="py-4 flex justify-center">
                    <button className="bg-cyan-500 hover:bg-cyan-400 active:scale-95 text-slate-950 font-bold px-6 py-2.5 rounded-xl shadow-lg shadow-cyan-500/25 transition-all">
                      Confirmar Pedido
                    </button>
                  </div>
                  <code className="text-[11px] bg-slate-950 p-2.5 rounded-lg text-slate-400 font-mono block overflow-x-auto border border-slate-800/50">
                    bg-cyan-500 hover:bg-cyan-400 active:scale-95 shadow-cyan-500/25
                  </code>
                </div>

                {/* Secondary Neutral */}
                <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-4 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">Secondary (Neutro/Outline)</span>
                    <p className="text-xs text-slate-400 mt-1">Ações alternativas ou de cancelamento sem competir visualmente.</p>
                  </div>
                  <div className="py-4 flex justify-center">
                    <button className="bg-slate-800/90 hover:bg-slate-700 active:scale-95 text-slate-200 border border-slate-700 font-medium px-6 py-2.5 rounded-xl transition-all">
                      Editar Opções
                    </button>
                  </div>
                  <code className="text-[11px] bg-slate-950 p-2.5 rounded-lg text-slate-400 font-mono block overflow-x-auto border border-slate-800/50">
                    bg-slate-800/90 hover:bg-slate-700 border-slate-700
                  </code>
                </div>

                {/* Glassmorphism */}
                <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900/90 to-cyan-950/40 border border-cyan-500/20 space-y-4 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-cyan-300 uppercase tracking-wider">Glassmorphism (Vidro Fosco)</span>
                    <p className="text-xs text-slate-400 mt-1">Translúcido com desfoque de fundo e borda reflexiva.</p>
                  </div>
                  <div className="py-4 flex justify-center">
                    <button className="backdrop-blur-md bg-white/10 hover:bg-white/15 active:scale-95 text-white border border-white/20 font-medium px-6 py-2.5 rounded-xl shadow-lg transition-all">
                      Explorar Vidro
                    </button>
                  </div>
                  <code className="text-[11px] bg-slate-950 p-2.5 rounded-lg text-slate-400 font-mono block overflow-x-auto border border-slate-800/50">
                    backdrop-blur-md bg-white/10 border-white/20
                  </code>
                </div>

                {/* Neumorphic Accent */}
                <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-4 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">Soft Emboss (Neumórfico Dark)</span>
                    <p className="text-xs text-slate-400 mt-1">Efeito táctil de relevo suave simulando extrusão física.</p>
                  </div>
                  <div className="py-4 flex justify-center">
                    <button className="bg-slate-900 text-slate-200 font-semibold px-6 py-2.5 rounded-xl shadow-[4px_4px_10px_#050811,-4px_-4px_10px_#1e293b] active:shadow-[inset_2px_2px_5px_#050811,inset_-2px_-2px_5px_#1e293b] transition-all">
                      Botão Relevo
                    </button>
                  </div>
                  <code className="text-[11px] bg-slate-950 p-2.5 rounded-lg text-slate-400 font-mono block overflow-x-auto border border-slate-800/50">
                    shadow-[4px_4px_10px_#050811,-4px_-4px_10px_#1e293b]
                  </code>
                </div>

                {/* Cyberpunk Brutalism */}
                <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-4 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">Neo-Brutalism (Geométrico)</span>
                    <p className="text-xs text-slate-400 mt-1">Bordas grossas retas e sombra sólida deslocada sem desfoque.</p>
                  </div>
                  <div className="py-4 flex justify-center">
                    <button className="bg-amber-400 hover:bg-amber-300 text-slate-950 font-black tracking-wide uppercase px-6 py-2.5 border-2 border-white shadow-[4px_4px_0px_0px_#ffffff] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all">
                      Cyber Brutal
                    </button>
                  </div>
                  <code className="text-[11px] bg-slate-950 p-2.5 rounded-lg text-slate-400 font-mono block overflow-x-auto border border-slate-800/50">
                    border-2 shadow-[4px_4px_0px_#fff] active:translate-x-1
                  </code>
                </div>

                {/* Ghost Action */}
                <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-4 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Ghost / Text Button</span>
                    <p className="text-xs text-slate-400 mt-1">Sem borda ou fundo em repouso, acendendo apenas com foco/hover.</p>
                  </div>
                  <div className="py-4 flex justify-center">
                    <button className="text-slate-400 hover:text-cyan-400 hover:bg-cyan-500/10 active:scale-95 px-6 py-2.5 rounded-xl font-medium transition-all flex items-center space-x-1.5">
                      <span>Ver Documentação</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                  <code className="text-[11px] bg-slate-950 p-2.5 rounded-lg text-slate-400 font-mono block overflow-x-auto border border-slate-800/50">
                    text-slate-400 hover:text-cyan-400 hover:bg-cyan-500/10
                  </code>
                </div>
              </div>
            </section>

            {/* Shadows and Elevation System */}
            <section className="space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                  <Layers className="w-5 h-5 text-cyan-400" />
                  <span>2. Sistema de Sombras & Elevação Visual (Z-Index Físico)</span>
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Selecione o nível de sombra para observar como a elevação cria hierarquia e profundidade na interface.
                </p>
              </div>

              {/* Shadow Selector Controls */}
              <div className="flex flex-wrap gap-2">
                {[
                  { label: 'Sombra Suave (sm)', value: 'shadow-sm', desc: 'Para botões sutis e inputs' },
                  { label: 'Padrão (md)', value: 'shadow-md', desc: 'Para cards comuns' },
                  { label: 'Elevação Alta (xl)', value: 'shadow-xl', desc: 'Para cards flutuantes' },
                  { label: 'Modais / Destaque (2xl)', value: 'shadow-2xl', desc: 'Para modais e flyouts' },
                  { label: 'Glow Neon Ciano', value: 'shadow-[0_0_35px_rgba(6,182,212,0.35)]', desc: 'Acento futurista vibrante' },
                  { label: 'Sombra Interna (inner)', value: 'shadow-inner', desc: 'Para campos afundados e toggles' },
                ].map((s) => (
                  <button
                    key={s.value}
                    onClick={() => setSelectedShadow(s.value)}
                    className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                      selectedShadow === s.value
                        ? 'bg-cyan-500 text-slate-950 font-bold shadow-lg shadow-cyan-500/30'
                        : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {s.label}
                  </button>
                ))}
              </div>

              {/* Dynamic Preview Card */}
              <div className="p-10 rounded-3xl bg-slate-900/40 border border-slate-800/80 flex flex-col md:flex-row items-center justify-around gap-8">
                <div className={`w-64 sm:w-72 h-44 rounded-2xl bg-slate-900 border border-slate-700/80 p-6 flex flex-col justify-between transition-all duration-300 ${selectedShadow}`}>
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-semibold text-cyan-400">Card Elevado</span>
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-white">Profundidade Z</h4>
                    <p className="text-xs text-slate-400 mt-1">A sombra comunica a distância relativa da superfície de fundo.</p>
                  </div>
                  <div className="text-[11px] text-slate-500 font-mono truncate">
                    classe: {selectedShadow}
                  </div>
                </div>

                <div className="max-w-md space-y-3 text-sm text-slate-300">
                  <div className="flex items-start space-x-2">
                    <CornerDownRight className="w-4 h-4 text-cyan-400 shrink-0 mt-1" />
                    <span><strong>Por que isso importa no prompt:</strong> Dizer "use sombras boas" gera resultados genéricos. Dizer "use elevação com shadow-xl em cards no hover e shadow-cyan-500/20 em estados ativos" cria acabamento profissional.</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <CornerDownRight className="w-4 h-4 text-cyan-400 shrink-0 mt-1" />
                    <span><strong>Regra de ouro:</strong> Quanto maior o elemento ou sua prioridade (ex: Modal de Confirmação), maior deve ser a dispersão da sombra.</span>
                  </div>
                </div>
              </div>
            </section>

            {/* Navigation Patterns */}
            <section className="space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                  <Layout className="w-5 h-5 text-cyan-400" />
                  <span>3. Menus e Padrões de Navegação</span>
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Alterne entre os padrões mais comuns em Web Apps para entender a mecânica de cada um.
                </p>
              </div>

              <div className="flex space-x-2 border-b border-slate-800 pb-3">
                <button
                  onClick={() => setActiveNavStyle('tabs')}
                  className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                    activeNavStyle === 'tabs' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Abas Segmentadas (Tabs)
                </button>
                <button
                  onClick={() => setActiveNavStyle('sidebar')}
                  className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                    activeNavStyle === 'sidebar' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Sidebar Colapsável
                </button>
                <button
                  onClick={() => setActiveNavStyle('drawer')}
                  className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                    activeNavStyle === 'drawer' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Drawer Lateral Mobile
                </button>
              </div>

              {/* Navigation Style Simulator */}
              <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 min-h-[220px] flex items-center justify-center">
                {activeNavStyle === 'tabs' && (
                  <div className="w-full max-w-md space-y-3">
                    <div className="text-xs text-slate-400 font-medium text-center">Padrão: Segmented Control Bar</div>
                    <div className="flex bg-slate-950 p-1.5 rounded-2xl border border-slate-800">
                      <button className="flex-1 py-2 text-xs font-semibold rounded-xl bg-cyan-500 text-slate-950 shadow-md">Visão Geral</button>
                      <button className="flex-1 py-2 text-xs font-semibold rounded-xl text-slate-400 hover:text-white">Relatórios</button>
                      <button className="flex-1 py-2 text-xs font-semibold rounded-xl text-slate-400 hover:text-white">Configurações</button>
                    </div>
                  </div>
                )}

                {activeNavStyle === 'sidebar' && (
                  <div className="w-full max-w-lg bg-slate-950 rounded-2xl border border-slate-800 p-4 flex gap-4">
                    <div className="w-44 bg-slate-900 rounded-xl p-3 space-y-2 border border-slate-800/60">
                      <div className="text-[11px] font-bold text-slate-400 uppercase">Dashboard Menu</div>
                      <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 text-xs font-medium flex items-center space-x-2">
                        <Monitor className="w-3.5 h-3.5" />
                        <span>Painel</span>
                      </div>
                      <div className="p-2 rounded-lg text-slate-400 hover:bg-slate-800 text-xs font-medium flex items-center space-x-2">
                        <Palette className="w-3.5 h-3.5" />
                        <span>Temas</span>
                      </div>
                    </div>
                    <div className="flex-1 p-3 bg-slate-900/40 rounded-xl border border-slate-800/40 flex items-center justify-center text-xs text-slate-500">
                      Área principal do aplicativo
                    </div>
                  </div>
                )}

                {activeNavStyle === 'drawer' && (
                  <div className="w-full max-w-sm border border-slate-800 bg-slate-950 rounded-2xl p-4 relative overflow-hidden">
                    <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                      <span className="text-xs font-bold text-white">Menu Deslizante (Off-Canvas)</span>
                      <span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400 text-[10px]">Mobile</span>
                    </div>
                    <div className="mt-3 space-y-2">
                      <div className="p-2.5 rounded-lg bg-slate-900 text-xs text-slate-300 flex items-center justify-between">
                        <span>Minha Conta</span>
                        <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-900 text-xs text-slate-300 flex items-center justify-between">
                        <span>Notificações</span>
                        <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-900 text-xs text-slate-300 flex items-center justify-between">
                        <span>Preferências</span>
                        <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </section>
          </div>
        )}

        {}
        {activeTab === 'glossary' && (
          <div className="space-y-8">
            <div className="border-b border-slate-800 pb-4">
              <h1 className="text-3xl font-extrabold text-white tracking-tight">
                Dicionário Visual de Conceitos Frontend
              </h1>
              <p className="text-slate-400 text-sm sm:text-base mt-2">
                Entenda a função real de cada termo para saber exatamente o que exigir nas suas solicitações de código e UI.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {GLOSSARY_ITEMS.map((item) => {
                const IconComponent = item.icon;
                return (
                  <div
                    key={item.id}
                    className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800/80 hover:border-cyan-500/40 transition-all flex flex-col justify-between space-y-6"
                  >
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="p-3 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                          <IconComponent className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                          {item.tag}
                        </span>
                      </div>
                      <h3 className="text-xl font-bold text-white tracking-tight">{item.title}</h3>
                      <p className="text-sm text-slate-300 leading-relaxed">{item.summary}</p>
                      
                      <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 space-y-1">
                        <span className="text-[11px] font-bold uppercase text-cyan-400">Por que é crucial:</span>
                        <p className="text-xs text-slate-400">{item.whyImportant}</p>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <span className="text-[11px] font-bold uppercase text-slate-400 flex items-center space-x-1">
                        <Code2 className="w-3.5 h-3.5 text-cyan-400" />
                        <span>Snippet Prático</span>
                      </span>
                      <pre className="text-[11px] bg-slate-950 p-3 rounded-xl text-slate-300 font-mono overflow-x-auto border border-slate-800/80">
                        {item.codeExample}
                      </pre>
                      
                      <div className="p-3 rounded-xl bg-cyan-950/20 border border-cyan-500/30 text-xs text-cyan-200">
                        <strong>💡 Como pedir no prompt:</strong> {item.goodPromptTip}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {}
        {activeTab === 'prompt-generator' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Options Builder Panel */}
            <div className="lg:col-span-6 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
                  <Terminal className="w-6 h-6 text-cyan-400" />
                  <span>Gerador de Prompts de Frontend</span>
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Selecione as premissas arquiteturais e técnicas para montar o prompt sem ambiguidades.
                </p>
              </div>

              {/* Input Type */}
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase text-slate-300">1. Tipo de Aplicação</label>
                <div className="grid grid-cols-2 gap-2">
                  {['Dashboard Analítico', 'E-commerce / Catálogo', 'Landing Page Interativa', 'App SaaS / Painel'].map(type => (
                    <button
                      key={type}
                      onClick={() => setGenAppType(type)}
                      className={`p-3 rounded-xl text-xs font-semibold text-left transition-all border ${
                        genAppType === type
                          ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50'
                          : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Framework & Tooling */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase text-slate-300">2. Tooling / Framework</label>
                  <select
                    value={genFramework}
                    onChange={(e) => setGenFramework(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                  >
                    <option value="React 18/19 (Vite)">React (Vite Bundler)</option>
                    <option value="Next.js (App Router)">Next.js (App Router)</option>
                    <option value="HTML5 + Vanilla JS Puro">HTML5 / Vanilla JS</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase text-slate-300">3. Estilização</label>
                  <select
                    value={genStyling}
                    onChange={(e) => setGenStyling(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                  >
                    <option value="Tailwind CSS v3+">Tailwind CSS</option>
                    <option value="CSS Modules + Variáveis">CSS Modules Moderno</option>
                    <option value="Tailwind + shadcn/ui">Tailwind + shadcn/ui</option>
                  </select>
                </div>
              </div>

              {/* Theme and Layout Architecture */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase text-slate-300">4. Linguagem Visual</label>
                  <select
                    value={genTheme}
                    onChange={(e) => setGenTheme(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                  >
                    <option value="Dark Minimalista (Ciano / Slate)">Dark Minimalista (Ciano)</option>
                    <option value="Glassmorphism Translúcido">Glassmorphism / Frosted Glass</option>
                    <option value="Clean Light Moderno (Branco / Cinza 50)">Clean Light (Neutro)</option>
                    <option value="Neo-Brutalism de Alto Contraste">Neo-Brutalism Contrastante</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase text-slate-300">5. Layout Principal</label>
                  <select
                    value={genArchitecture}
                    onChange={(e) => setGenArchitecture(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                  >
                    <option value="Mobile-First Rigoroso">Mobile-First Rigoroso</option>
                    <option value="Sidebar Esquerda com Conteúdo Dinâmico">Sidebar Esquerda Fixa</option>
                    <option value="Centralizado em Cartões com Abas">Cartões Centrais / Tabs</option>
                  </select>
                </div>
              </div>

              {/* Feature Checklist */}
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase text-slate-300">6. Requisitos & Funcionalidades Chave</label>
                <div className="space-y-2">
                  {[
                    'Responsividade fluida (Mobile ao 4K)',
                    'Micro-interações táteis e feedback sonoro visual',
                    'Componente isolado em arquivo único sem dependências externas',
                    'Estados de Loading e Empty State explícitos',
                    'Acessibilidade e navegação completa por teclado (Tabindex/Focus)'
                  ].map((feat) => (
                    <div
                      key={feat}
                      onClick={() => toggleFeature(feat)}
                      className={`p-3 rounded-xl border text-xs cursor-pointer flex items-center justify-between transition-all ${
                        genFeatures.includes(feat)
                          ? 'bg-cyan-500/10 border-cyan-500/40 text-cyan-200'
                          : 'bg-slate-900/50 border-slate-800 text-slate-400'
                      }`}
                    >
                      <span>{feat}</span>
                      <div className={`w-4 h-4 rounded-md flex items-center justify-center border ${
                        genFeatures.includes(feat) ? 'bg-cyan-500 border-cyan-400 text-slate-950' : 'border-slate-700'
                      }`}>
                        {genFeatures.includes(feat) && <Check className="w-3 h-3 stroke-[3]" />}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Custom feature input */}
                <form onSubmit={addCustomFeature} className="flex gap-2 pt-2">
                  <input
                    type="text"
                    value={customFeature}
                    onChange={(e) => setCustomFeature(e.target.value)}
                    placeholder="Adicionar outro requisito específico..."
                    className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                  />
                  <button
                    type="submit"
                    className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-xl text-slate-200"
                  >
                    Adicionar
                  </button>
                </form>
              </div>
            </div>

            {/* Generated Output Preview Panel */}
            <div className="lg:col-span-6 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-cyan-400" />
                  <span className="text-base font-bold text-white">Prompt Estruturado Pronto</span>
                </div>
                <button
                  onClick={() => copyToClipboard(generatedPrompt, 'generated-prompt')}
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-bold transition-all shadow-md shadow-cyan-500/20"
                >
                  {copiedId === 'generated-prompt' ? (
                    <>
                      <Check className="w-4 h-4" />
                      <span>Copiado!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      <span>Copiar Prompt</span>
                    </>
                  )}
                </button>
              </div>

              <div className="relative">
                <textarea
                  readOnly
                  value={generatedPrompt}
                  rows={20}
                  className="w-full bg-slate-900/90 border border-slate-800 rounded-2xl p-4 text-xs font-mono text-cyan-300/90 focus:outline-none resize-none leading-relaxed selection:bg-cyan-500 selection:text-slate-950"
                />
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/50 border border-slate-800 text-xs text-slate-400 space-y-2">
                <div className="flex items-center space-x-2 text-slate-200 font-semibold">
                  <Info className="w-4 h-4 text-cyan-400" />
                  <span>Dica de ouro para usar este prompt:</span>
                </div>
                <p>
                  Cole este texto no ChatGPT, Claude ou Gemini. O segredo de não haver retrabalho está em já ter definido previamente as restrições negativas (como evitar alerts nativos e tamanhos fixos).
                </p>
              </div>
            </div>
          </div>
        )}

        {}
        {activeTab === 'checklist' && (
          <div className="space-y-10">
            <div className="border-b border-slate-800 pb-4">
              <h1 className="text-3xl font-extrabold text-white tracking-tight">
                Como Pedir Frontend Sem Retrabalho
              </h1>
              <p className="text-slate-400 text-sm sm:text-base mt-2">
                A anatomia definitiva de uma especificação clara. Modelos de IA não adivinham preferências silenciosas; entregue intenções estruturadas.
              </p>
            </div>

            {/* The 5 Pillars of a Great Frontend Spec */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-3">
                <div className="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold">1</div>
                <h3 className="text-base font-bold text-white">Objetivo & Papel</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Defina claramente o que o usuário fará na tela e qual o papel do agente (ex: Engenheiro Frontend especialista em React).
                </p>
                <div className="text-[11px] font-mono text-cyan-300/80 bg-slate-950 p-2 rounded-lg">
                  Evite: "Faça uma tela legal"
                  <br />
                  Prefira: "Crie um Dashboard financeiro com balanço e transações recentes"
                </div>
              </div>

              <div className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-3">
                <div className="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold">2</div>
                <h3 className="text-base font-bold text-white">Design Tokens Explícitos</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Indique a paleta (Dark slate com ciano), formato de cantos (rounded-xl) e estilo de profundidade (sombras sutis e glassmorphism).
                </p>
                <div className="text-[11px] font-mono text-cyan-300/80 bg-slate-950 p-2 rounded-lg">
                  Evite: "Deixe bonito"
                  <br />
                  Prefira: "Tema escuro, fundo slate-950, acentos em cyan-400 e contraste WCAG AA"
                </div>
              </div>

              <div className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-3">
                <div className="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold">3</div>
                <h3 className="text-base font-bold text-white">Interatividade & Estados</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Todo componente dinâmico precisa de 3 estados: Normal, Loading (carregamento) e Feedback de Sucesso/Erro.
                </p>
                <div className="text-[11px] font-mono text-cyan-300/80 bg-slate-950 p-2 rounded-lg">
                  Evite: Esquecer o feedback
                  <br />
                  Prefira: "Ao clicar, simule loading de 1.5s e mostre toast de sucesso"
                </div>
              </div>
            </div>

            {/* Anti-Patterns Table */}
            <div className="space-y-4">
              <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                <ShieldCheck className="w-5 h-5 text-red-400" />
                <span>Anti-Padrões Proibidos em Pedidos de Frontend</span>
              </h2>

              <div className="overflow-x-auto rounded-2xl border border-slate-800">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="bg-slate-900 border-b border-slate-800 text-slate-400 uppercase font-semibold">
                      <th className="p-4">Anti-Padrão Comum</th>
                      <th className="p-4">Por que quebra a aplicação</th>
                      <th className="p-4">Como formular da forma correta</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 bg-slate-950/50">
                    <tr>
                      <td className="p-4 font-semibold text-red-400">Usar alert() ou confirm() nativos</td>
                      <td className="p-4 text-slate-400">Trava a thread de execução do navegador e parece amador.</td>
                      <td className="p-4 text-cyan-300 font-mono">"Crie um modal animado ou toast de confirmação in-page."</td>
                    </tr>
                    <tr>
                      <td className="p-4 font-semibold text-red-400">Larguras fixas rígidas (ex: w-[1200px])</td>
                      <td className="p-4 text-slate-400">Gera barra de rolagem horizontal quebrada em smartphones.</td>
                      <td className="p-4 text-cyan-300 font-mono">"Use w-full max-w-7xl mx-auto com padding responsivo px-4 sm:px-6."</td>
                    </tr>
                    <tr>
                      <td className="p-4 font-semibold text-red-400">Botões sem active:scale ou hover</td>
                      <td className="p-4 text-slate-400">O usuário clica e tem a sensação de que o app travou.</td>
                      <td className="p-4 text-cyan-300 font-mono">"Adicione transition-all active:scale-95 e hover:brightness-110."</td>
                    </tr>
                    <tr>
                      <td className="p-4 font-semibold text-red-400">Cores sem contraste (cinza sobre cinza)</td>
                      <td className="p-4 text-slate-400">Texto ilegível ao ar livre ou em monitores com pouco brilho.</td>
                      <td className="p-4 text-cyan-300 font-mono">"Garanta contraste mínimo WCAG AA (texto slate-100 sobre slate-900)."</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>

      {}
      <footer className="border-t border-slate-900 bg-slate-950 mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <div className="flex items-center space-x-2">
            <Atom className="w-4 h-4 text-cyan-400" />
            <span>FrontCraft Master Guide & Prompt Studio</span>
          </div>
          <div>
            Projetado com React, Tailwind CSS e Arquitetura Mobile-First
          </div>
        </div>
      </footer>
    </div>
  );
}