import { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { Header } from './components/Header';
import { SearchBar } from './components/SearchBar';
import { CategoryFilter } from './components/CategoryFilter';
import { EntityCard } from './components/EntityCard';
import { EntityModal } from './components/EntityModal';
import { TreasureRoller } from './components/TreasureRoller';
import { CombatTrackerModal } from './components/CombatTrackerModal';
import { QuickReferenceModal } from './components/QuickReferenceModal';
import { FavoritesDrawer } from './components/FavoritesDrawer';
import { BottomNav } from './components/BottomNav';
import { ScrollToTop } from './components/ScrollToTop';
import { useUniversalSearch } from './hooks/useUniversalSearch';
import { useFavorites } from './hooks/useFavorites';
import type { T20CanonicalEntity } from './types/t20_schema';
import './App.css';

const INITIAL_BATCH_SIZE = 36;
const BATCH_INCREMENT = 24;

export function App() {
  const {
    query,
    setQuery,
    filters,
    setCategory,
    setSubcategory,
    setItemType,
    setBook,
    setMinPrice,
    setMaxPrice,
    setPriceRange,
    resetFilters,
    dynamicCounts,
    results,
    totalCount
  } = useUniversalSearch();

  const { 
    favorites, 
    favoritesWithDate, 
    toggleFavorite, 
    updateFavoriteComment,
    isFavorite, 
    exportFavorites, 
    importFavorites, 
    count: favoritesCount 
  } = useFavorites();

  // Modais de Estado
  const [selectedEntity, setSelectedEntity] = useState<T20CanonicalEntity | null>(null);
  const [isTreasureOpen, setIsTreasureOpen] = useState<boolean>(false);
  const [isCombatTrackerOpen, setIsCombatTrackerOpen] = useState<boolean>(false);
  const [isQuickReferenceOpen, setIsQuickReferenceOpen] = useState<boolean>(false);
  const [isFavoritesOpen, setIsFavoritesOpen] = useState<boolean>(false);
  const [modalOrigin, setModalOrigin] = useState<'main' | 'favorites'>('main');

  // Renderização Incremental / Infinite Scroll
  const [displayLimit, setDisplayLimit] = useState<number>(INITIAL_BATCH_SIZE);
  const sentinelRef = useRef<HTMLDivElement>(null);

  // Reset do limite visível sempre que a busca ou os filtros mudarem
  useEffect(() => {
    setDisplayLimit(INITIAL_BATCH_SIZE);
  }, [query, filters]);

  const visibleResults = useMemo(() => {
    return results.slice(0, displayLimit);
  }, [results, displayLimit]);

  const hasMore = displayLimit < results.length;

  const handleLoadMore = useCallback(() => {
    setDisplayLimit(prev => Math.min(prev + BATCH_INCREMENT, results.length));
  }, [results.length]);

  // Observer de Scroll Infinito
  useEffect(() => {
    if (!hasMore) return;
    const sentinel = sentinelRef.current;
    if (!sentinel) return;

    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) {
          handleLoadMore();
        }
      },
      { rootMargin: '300px' }
    );

    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [hasMore, handleLoadMore]);

  const handleSelectEntity = useCallback((entity: T20CanonicalEntity) => {
    setModalOrigin('main');
    setSelectedEntity(entity);
  }, []);

  const handleCardToggleFavorite = useCallback((id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    toggleFavorite(id);
  }, [toggleFavorite]);

  return (
    <div className="app-root">
      <Header
        onOpenQuickReference={() => setIsQuickReferenceOpen(true)}
        onOpenFavorites={() => setIsFavoritesOpen(true)}
        onOpenTreasure={() => setIsTreasureOpen(true)}
        favoritesCount={favoritesCount}
      />

      <main className="main-content">
        <SearchBar
          query={query}
          onQueryChange={setQuery}
          resultsCount={results.length}
          totalCount={totalCount}
        />

        <CategoryFilter
          filters={filters}
          dynamicCounts={dynamicCounts}
          onSelectCategory={setCategory}
          onSelectSubcategory={setSubcategory}
          onSelectItemType={setItemType}
          onSelectBook={setBook}
          onMinPriceChange={setMinPrice}
          onMaxPriceChange={setMaxPrice}
          onSelectPricePreset={setPriceRange}
          onResetFilters={resetFilters}
        />

        {results.length === 0 ? (
          <div className="empty-favorites-box parchment-card">
            <span style={{ fontSize: '2.5rem' }}>📜</span>
            <h3>Nenhum tomo ou regra encontrada com os filtros atuais</h3>
            <p>Tente alterar os filtros de subcategoria, proficiência ou clique em "Limpar Filtros".</p>
            <button className="btn-gold" style={{ marginTop: '0.8rem' }} onClick={resetFilters}>
              Limpar Todos os Filtros
            </button>
          </div>
        ) : (
          <>
            <div className="results-grid">
              {visibleResults.map(entity => (
                <EntityCard
                  key={entity.id}
                  entity={entity}
                  onClick={() => handleSelectEntity(entity)}
                  isFavorite={isFavorite(entity.id)}
                  onToggleFavorite={e => handleCardToggleFavorite(entity.id, e)}
                />
              ))}
            </div>

            {hasMore && (
              <div className="load-more-container" ref={sentinelRef}>
                <button 
                  className="load-more-btn" 
                  onClick={handleLoadMore}
                >
                  📜 Exibindo {visibleResults.length} de {results.length} tomos — Carregar Mais
                </button>
              </div>
            )}
          </>
        )}
      </main>

      {/* Visualizador Canônico de Tomo */}
      <EntityModal
        entity={selectedEntity}
        onClose={() => {
          setSelectedEntity(null);
          if (modalOrigin === 'favorites') {
            setIsFavoritesOpen(true);
            setModalOrigin('main');
          }
        }}
        isFavorite={selectedEntity ? isFavorite(selectedEntity.id) : false}
        onToggleFavorite={() => {
          if (selectedEntity) toggleFavorite(selectedEntity.id);
        }}
        onSelectRelatedEntity={rel => setSelectedEntity(rel)}
      />

      {/* Tomo de Consulta Rápida (Pág. 220 e 240 + Cheat-sheet) */}
      <QuickReferenceModal
        isOpen={isQuickReferenceOpen}
        onClose={() => setIsQuickReferenceOpen(false)}
      />

      {/* Simulador & Filtro de Tesouros D% */}
      <TreasureRoller
        isOpen={isTreasureOpen}
        onClose={() => setIsTreasureOpen(false)}
      />

      {/* Rastreador de Combate & Condições Dinâmicas */}
      <CombatTrackerModal
        isOpen={isCombatTrackerOpen}
        onClose={() => setIsCombatTrackerOpen(false)}
        onOpenQuickReference={() => setIsQuickReferenceOpen(true)}
      />

      {/* Gaveta de Favoritos */}
      <FavoritesDrawer
        isOpen={isFavoritesOpen}
        onClose={() => setIsFavoritesOpen(false)}
        favorites={favorites}
        favoritesWithDate={favoritesWithDate}
        onToggleFavorite={toggleFavorite}
        onUpdateComment={updateFavoriteComment}
        onExportFavorites={exportFavorites}
        onImportFavorites={importFavorites}
        onSelectEntity={entity => {
          setModalOrigin('favorites');
          setIsFavoritesOpen(false);
          setSelectedEntity(entity);
        }}
      />

      {/* Barra de Navegação Inferior Mobile */}
      <BottomNav
        onOpenSearch={() => {
          window.scrollTo({ top: 0, behavior: 'smooth' });
          const searchInput = document.querySelector('.search-input') as HTMLInputElement;
          searchInput?.focus();
        }}
        onOpenQuickReference={() => setIsQuickReferenceOpen(true)}
        onOpenTreasure={() => setIsTreasureOpen(true)}
        onOpenFavorites={() => setIsFavoritesOpen(true)}
        favoritesCount={favoritesCount}
      />

      {/* Botão Flutuante Voltar ao Topo */}
      <ScrollToTop />
    </div>
  );
}

export default App;
