import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import type { Calculator, ManifestItem } from '@/types/clinical';
import type { BedRecord } from '@/services/storageService';
import { storageService } from '@/services/storageService';
import defaultManifestRaw from '@/data/manifest.json';
import block01Data from '@/data/blocks/block_01.json';
import block03Data from './data/blocks/block_03.json';

import { ThemeToggle } from '@/components/common/ThemeToggle';
import { BottomNav, type TabType } from '@/components/common/BottomNav';
import { AzScoreList } from '@/components/catalog/AzScoreList';
import { FavoritesView, QuickFavoritesCarousel } from '@/components/catalog/FavoritesView';
import { CalculatorView } from '@/components/calculator/CalculatorView';
import { PrescriptionCard } from '@/components/calculator/PrescriptionCard';
import {
  NOREPINEPHRINE_PROTOCOL,
  VASOPRESSIN_PROTOCOL,
  DOBUTAMINE_PROTOCOL,
  NITROGLYCERIN_PROTOCOL
} from '@/engines/infusionEngine';

import {
  Activity,
  BedDouble,
  Plus,
  Trash2,
  AlertCircle,
  Info
} from 'lucide-react';

const manifest = defaultManifestRaw as unknown as ManifestItem[];
const allCalculators = [...block01Data.calculators, ...block03Data.calculators] as unknown as Calculator[];

export const App: React.FC = () => {
  // Navigation State
  const [activeTab, setActiveTab] = useState<TabType>('catalog');
  const [selectedCalculatorId, setSelectedCalculatorId] = useState<string | null>(null);

  // Global Clinical State
  const [patientWeight, setPatientWeight] = useState<number>(70);
  const [favoriteIds, setFavoriteIds] = useState<string[]>([]);
  const [beds, setBeds] = useState<BedRecord[]>([]);
  const [activeBedId, setActiveBedId] = useState<string>('bed_default');

  // Load favorites & beds from local storage on mount
  useEffect(() => {
    let isMounted = true;

    storageService.getFavorites().then((favs) => {
      if (isMounted) setFavoriteIds(favs);
    }).catch(() => {});

    storageService.getBeds().then((savedBeds) => {
      if (isMounted) {
        if (savedBeds && savedBeds.length > 0) {
          setBeds(savedBeds);
          setActiveBedId(savedBeds[0].id);
          if (savedBeds[0].patientWeightKg) {
            setPatientWeight(savedBeds[0].patientWeightKg);
          }
        } else {
          // Initialize with default anonymous bed
          const defaultBed: BedRecord = {
            id: 'bed_default',
            label: 'Leito 04 - UTI',
            sector: 'UTI Geral',
            patientWeightKg: 70,
            updatedAt: new Date().toISOString()
          };
          storageService.saveBed(defaultBed).catch(() => {});
          setBeds([defaultBed]);
        }
      }
    }).catch(() => {});

    return () => {
      isMounted = false;
    };
  }, []);

  // Sync favorites change
  const handleToggleFavorite = useCallback(async (calculatorId: string) => {
    try {
      const isNowFav = await storageService.toggleFavorite(calculatorId);
      setFavoriteIds((prev) =>
        isNowFav ? [...prev, calculatorId] : prev.filter((id) => id !== calculatorId)
      );
    } catch {
      // Fallback local toggle
      setFavoriteIds((prev) =>
        prev.includes(calculatorId)
          ? prev.filter((id) => id !== calculatorId)
          : [...prev, calculatorId]
      );
    }
  }, []);

  // Active bed object
  const activeBed = useMemo(() => {
    return beds.find((b) => b.id === activeBedId) || beds[0];
  }, [beds, activeBedId]);

  // Catalog scroll preservation ref
  const catalogScrollPosRef = useRef<number>(0);

  // Handle calculator selection: save catalog scroll and reset to top
  const handleSelectCalculator = useCallback((calcId: string) => {
    if (typeof window !== 'undefined') {
      catalogScrollPosRef.current = window.scrollY || 0;
      if (typeof window.scrollTo === 'function') {
        window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
      }
    }
    setSelectedCalculatorId(calcId);
  }, []);

  // Handle Back to previous catalog/tab: restore scroll position
  const handleBackToCatalog = useCallback(() => {
    setSelectedCalculatorId(null);
    if (typeof window !== 'undefined') {
      const restorePos = catalogScrollPosRef.current;
      const doScroll = () => {
        if (typeof window.scrollTo === 'function') {
          window.scrollTo({ top: restorePos, behavior: 'instant' });
        }
      };
      if (typeof requestAnimationFrame === 'function') {
        requestAnimationFrame(doScroll);
      } else {
        setTimeout(doScroll, 0);
      }
    }
  }, []);

  // Handle BottomNav Tab change
  const handleTabChange = useCallback((tab: TabType) => {
    setSelectedCalculatorId(null);
    setActiveTab(tab);
    if (typeof window !== 'undefined' && typeof window.scrollTo === 'function') {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    }
  }, []);

  // Selected calculator definition
  const selectedCalculator = useMemo(() => {
    if (!selectedCalculatorId) return null;
    return allCalculators.find(
      (c) => c.id === selectedCalculatorId || c.slug === selectedCalculatorId
    );
  }, [selectedCalculatorId]);

  // Bed management actions
  const handleCreateBed = async () => {
    const nextNumber = beds.length + 1;
    const padded = nextNumber < 10 ? `0${nextNumber}` : `${nextNumber}`;
    const newBed: BedRecord = {
      id: `bed_${Date.now()}`,
      label: `Leito ${padded} - UTI`,
      sector: 'UTI Geral',
      patientWeightKg: 70,
      updatedAt: new Date().toISOString()
    };

    try {
      await storageService.saveBed(newBed);
      setBeds((prev) => [...prev, newBed]);
      setActiveBedId(newBed.id);
      setPatientWeight(70);
    } catch (e: any) {
      alert(e.message || 'Erro ao criar leito.');
    }
  };

  const handleDeleteBed = async (id: string) => {
    if (beds.length <= 1) return;
    try {
      await storageService.deleteBed(id);
      setBeds((prev) => prev.filter((b) => b.id !== id));
      if (activeBedId === id) {
        const remaining = beds.filter((b) => b.id !== id);
        setActiveBedId(remaining[0].id);
        if (remaining[0].patientWeightKg) {
          setPatientWeight(remaining[0].patientWeightKg);
        }
      }
    } catch {}
  };

  const handleSelectBed = (bed: BedRecord) => {
    setActiveBedId(bed.id);
    if (bed.patientWeightKg) {
      setPatientWeight(bed.patientWeightKg);
    }
  };

  const handleUpdateBedWeight = async (weight: number) => {
    setPatientWeight(weight);
    if (activeBed) {
      const updated: BedRecord = {
        ...activeBed,
        patientWeightKg: weight,
        updatedAt: new Date().toISOString()
      };
      setBeds((prev) => prev.map((b) => (b.id === activeBed.id ? updated : b)));
      await storageService.saveBed(updated).catch(() => {});
    }
  };

  return (
    <div className="min-h-full flex flex-col bg-canvas-light dark:bg-canvas-dark text-slate-900 dark:text-slate-100 transition-colors duration-200 relative overflow-x-hidden selection:bg-brand-500 selection:text-white">
      {/* Ambient background glow for premium depth */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-lg h-96 bg-gradient-to-b from-brand-500/10 via-brand-500/5 to-transparent pointer-events-none blur-3xl -z-10" />

      {/* 1. Global Mobile-First Header */}
      {!selectedCalculator && (
        <header className="sticky top-0 z-20 backdrop-blur-xl bg-surface-light/90 dark:bg-surface-dark/90 border-b border-subtle-light/80 dark:border-subtle-dark/80 px-4 py-3 pt-safe transition-colors duration-200 shadow-xs">
          <div className="max-w-md mx-auto flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-xl bg-brand-500/10 dark:bg-brand-400/15 flex items-center justify-center text-brand-600 dark:text-brand-400 shadow-xs">
                <Activity className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center space-x-1.5">
                  <h1 className="text-base font-bold tracking-tight text-slate-900 dark:text-white">
                    Scoreboard
                  </h1>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-brand-500/15 text-brand-600 dark:text-brand-400 border border-brand-500/20">
                    CDSS
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-tight">
                  {activeBed?.label || 'Leito 04 - UTI'} • {patientWeight} kg
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <ThemeToggle />
            </div>
          </div>

          {/* Quick Starred Favorites Carousel in Catalog Header */}
          {activeTab === 'catalog' && (
            <div className="max-w-md mx-auto mt-2">
              <QuickFavoritesCarousel
                favorites={favoriteIds}
                items={manifest}
                onSelectCalculator={handleSelectCalculator}
              />
            </div>
          )}
        </header>
      )}

      {/* 2. Main Content Router */}
      <main className="flex-1 w-full pb-16">
        {/* View A: Calculator View */}
        {selectedCalculatorId ? (
          selectedCalculator ? (
            <CalculatorView
              key={selectedCalculator.id}
              calculator={selectedCalculator}
              onBack={handleBackToCatalog}
              patientWeightKg={patientWeight}
              onWeightChange={handleUpdateBedWeight}
              bedLabel={activeBed?.label}
              isFavorite={favoriteIds.includes(selectedCalculator.id)}
              onToggleFavorite={handleToggleFavorite}
            />
          ) : (
            <div className="max-w-md mx-auto p-6 space-y-4 text-center">
              <div className="w-12 h-12 rounded-2xl bg-amber-500/15 text-amber-600 flex items-center justify-center mx-auto">
                <AlertCircle className="w-6 h-6" />
              </div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                Calculadora em Preparação
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Este escore faz parte dos próximos blocos monográficos e será disponibilizado na próxima atualização com integridade monográfica total.
              </p>
              <button
                type="button"
                onClick={handleBackToCatalog}
                className="min-h-touch px-4 py-2.5 rounded-xl bg-brand-500 text-white text-xs font-semibold"
              >
                Voltar ao Catálogo
              </button>
            </div>
          )
        ) : (
          <>
            {/* View B: A-Z Catalog Tab */}
            {activeTab === 'catalog' && (
              <div data-testid="az-score-list" className="w-full">
                <AzScoreList
                  items={manifest}
                  onSelectCalculator={handleSelectCalculator}
                  initialFavorites={favoriteIds}
                  onToggleFavorite={handleToggleFavorite}
                />
              </div>
            )}

            {/* View C: Star Favorites Tab */}
            {activeTab === 'favorites' && (
              <FavoritesView
                items={manifest}
                onSelectCalculator={handleSelectCalculator}
                onNavigateToCatalog={() => setActiveTab('catalog')}
              />
            )}

            {/* View D: Anonymous Local Beds Tab */}
            {activeTab === 'beds' && (
              <div className="max-w-md mx-auto p-4 space-y-4" data-testid="beds-view">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-bold text-slate-900 dark:text-white">
                      Meus Leitos
                    </h2>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Rastreio anônimo local à beira do leito (Zero Risco LGPD)
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={handleCreateBed}
                    className="min-h-touch min-w-touch px-3 py-2 rounded-xl bg-brand-500 text-white text-xs font-semibold flex items-center space-x-1.5 shadow-sm active:scale-95"
                    data-testid="create-bed-btn"
                  >
                    <Plus className="w-4 h-4" />
                    <span>Novo Leito</span>
                  </button>
                </div>

                <div className="space-y-2.5">
                  {beds.map((bed) => {
                    const isSelected = bed.id === activeBedId;
                    return (
                      <div
                        key={bed.id}
                        onClick={() => handleSelectBed(bed)}
                        className={`p-4 rounded-2xl border transition-all cursor-pointer select-none flex items-center justify-between ${
                          isSelected
                            ? 'bg-brand-50/80 dark:bg-brand-950/40 border-2 border-brand-500 shadow-sm'
                            : 'bg-surface-light dark:bg-surface-dark border-subtle-light dark:border-subtle-dark hover:bg-slate-50 dark:hover:bg-slate-800/60'
                        }`}
                        data-testid={`bed-card-${bed.id}`}
                      >
                        <div className="flex items-center space-x-3">
                          <div
                            className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                              isSelected
                                ? 'bg-brand-500 text-white'
                                : 'bg-surface-raised-light dark:bg-surface-raised-dark text-slate-500'
                            }`}
                          >
                            <BedDouble className="w-5 h-5" />
                          </div>
                          <div>
                            <div className="flex items-center space-x-2">
                              <span className="text-sm font-bold text-slate-900 dark:text-white">
                                {bed.label}
                              </span>
                              {isSelected && (
                                <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-brand-500 text-white">
                                  Ativo
                                </span>
                              )}
                            </div>
                            <span className="text-xs text-slate-500 dark:text-slate-400">
                              {bed.sector || 'UTI'} • Peso: <strong className="text-slate-700 dark:text-slate-300">{bed.patientWeightKg || 70} kg</strong>
                            </span>
                          </div>
                        </div>

                        {beds.length > 1 && (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteBed(bed.id);
                            }}
                            className="w-9 h-9 rounded-lg flex items-center justify-center text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors"
                            aria-label={`Excluir ${bed.label}`}
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>

                <div className="p-3.5 rounded-xl bg-surface-raised-light dark:bg-surface-raised-dark border border-subtle-light/60 dark:border-subtle-dark/60 text-[11px] text-slate-500 leading-relaxed flex items-start space-x-2">
                  <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                  <span>
                    Conformidade Estrita com LGPD: Nenhum dado nominal (nome civil, CPF ou prontuário) é aceito ou armazenado. Os dados residem exclusivamente no armazenamento IndexedDB local do seu navegador.
                  </span>
                </div>
              </div>
            )}

            {/* View E: Plantão (Bedside BIC Reference) Tab */}
            {activeTab === 'infusions' && (
              <div className="max-w-md mx-auto p-4 space-y-4" data-testid="infusions-view">
                <div>
                  <h2 className="text-base font-bold text-slate-900 dark:text-white">
                    Plantão: Drogas Vasoativas em BIC
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Cálculo rápido de vazão (mL/h) à beira do leito para {activeBed?.label || 'Leito Ativo'} ({patientWeight} kg)
                  </p>
                </div>

                <div className="space-y-4">
                  {/* 1. Noradrenalina */}
                  <PrescriptionCard
                    protocol={NOREPINEPHRINE_PROTOCOL}
                    patientWeightKg={patientWeight}
                    onWeightChange={handleUpdateBedWeight}
                    bedLabel={activeBed?.label}
                    defaultExpanded={true}
                  />

                  {/* 2. Vasopressina */}
                  <PrescriptionCard
                    protocol={VASOPRESSIN_PROTOCOL}
                    patientWeightKg={patientWeight}
                    onWeightChange={handleUpdateBedWeight}
                    bedLabel={activeBed?.label}
                    defaultExpanded={false}
                  />

                  {/* 3. Dobutamina */}
                  <PrescriptionCard
                    protocol={DOBUTAMINE_PROTOCOL}
                    patientWeightKg={patientWeight}
                    onWeightChange={handleUpdateBedWeight}
                    bedLabel={activeBed?.label}
                    defaultExpanded={false}
                  />

                  {/* 4. Nitroglicerina */}
                  <PrescriptionCard
                    protocol={NITROGLYCERIN_PROTOCOL}
                    patientWeightKg={patientWeight}
                    onWeightChange={handleUpdateBedWeight}
                    bedLabel={activeBed?.label}
                    defaultExpanded={false}
                  />
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* 3. Global 4-Tab Bottom Navigation */}
      <BottomNav
        activeTab={activeTab}
        onTabChange={handleTabChange}
        favoritesCount={favoriteIds.length}
        bedsCount={beds.length}
      />
    </div>
  );
};

export default App;
