import { useState } from 'react';
import { Header } from './components/Header';
import { SearchBar } from './components/SearchBar';
import { CategoryFilter } from './components/CategoryFilter';
import { EntityCard } from './components/EntityCard';
import { EntityModal } from './components/EntityModal';
import { TreasureRoller } from './components/TreasureRoller';
import { CombatTrackerModal } from './components/CombatTrackerModal';
import { FavoritesDrawer } from './components/FavoritesDrawer';
import { BottomNav } from './components/BottomNav';
import { useUniversalSearch } from './hooks/useUniversalSearch';
import { useFavorites } from './hooks/useFavorites';
import { useCombatTracker } from './hooks/useCombatTracker';
import type { T20CanonicalEntity } from './types/t20_schema';
import './App.css';

export function App() {
  const {
    query,
    setQuery,
    filters,
    setCategory,
    setSubcategory,
    setItemType,
    setBook,
    resetFilters,
    dynamicCounts,
    results,
    totalCount
  } = useUniversalSearch();

  const { favorites, toggleFavorite, isFavorite, count: favoritesCount } = useFavorites();
  const combatTracker = useCombatTracker();

  // Modais de Estado
  const [selectedEntity, setSelectedEntity] = useState<T20CanonicalEntity | null>(null);
  const [isTreasureOpen, setIsTreasureOpen] = useState<boolean>(false);
  const [isCombatTrackerOpen, setIsCombatTrackerOpen] = useState<boolean>(false);
  const [isFavoritesOpen, setIsFavoritesOpen] = useState<boolean>(false);

  return (
    <div className="app-root">
      <Header
        onOpenCombatTracker={() => setIsCombatTrackerOpen(true)}
        onOpenFavorites={() => setIsFavoritesOpen(true)}
        onOpenTreasure={() => setIsTreasureOpen(true)}
        favoritesCount={favoritesCount}
        activeConditionsCount={combatTracker.tracker.activeConditionIds.length}
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
          <div className="results-grid">
            {results.map(entity => (
              <EntityCard
                key={entity.id}
                entity={entity}
                onClick={() => setSelectedEntity(entity)}
                isFavorite={isFavorite(entity.id)}
                onToggleFavorite={e => {
                  e.stopPropagation();
                  toggleFavorite(entity.id);
                }}
              />
            ))}
          </div>
        )}
      </main>

      {/* Visualizador Canônico de Tomo */}
      <EntityModal
        entity={selectedEntity}
        onClose={() => setSelectedEntity(null)}
        isFavorite={selectedEntity ? isFavorite(selectedEntity.id) : false}
        onToggleFavorite={() => {
          if (selectedEntity) toggleFavorite(selectedEntity.id);
        }}
        onSelectRelatedEntity={rel => setSelectedEntity(rel)}
      />

      {/* Simulador & Filtro de Tesouros D% */}
      <TreasureRoller
        isOpen={isTreasureOpen}
        onClose={() => setIsTreasureOpen(false)}
      />

      {/* Rastreador de Combate & Condições */}
      <CombatTrackerModal
        isOpen={isCombatTrackerOpen}
        onClose={() => setIsCombatTrackerOpen(false)}
        tracker={combatTracker.tracker}
        onToggleCondition={combatTracker.toggleCondition}
        onRemoveCondition={combatTracker.removeCondition}
        onUpdateHp={combatTracker.updateHp}
        onUpdateMp={combatTracker.updateMp}
        onSelectEntity={entity => setSelectedEntity(entity)}
      />

      {/* Gaveta de Favoritos */}
      <FavoritesDrawer
        isOpen={isFavoritesOpen}
        onClose={() => setIsFavoritesOpen(false)}
        favorites={favorites}
        onToggleFavorite={toggleFavorite}
        onSelectEntity={entity => setSelectedEntity(entity)}
      />

      {/* Barra de Navegação Inferior Mobile */}
      <BottomNav
        onOpenSearch={() => {
          window.scrollTo({ top: 0, behavior: 'smooth' });
          const searchInput = document.querySelector('.search-input') as HTMLInputElement;
          searchInput?.focus();
        }}
        onOpenTreasure={() => setIsTreasureOpen(true)}
        onOpenCombatTracker={() => setIsCombatTrackerOpen(true)}
        onOpenFavorites={() => setIsFavoritesOpen(true)}
        favoritesCount={favoritesCount}
        activeConditionsCount={combatTracker.tracker.activeConditionIds.length}
      />
    </div>
  );
}

export default App;
