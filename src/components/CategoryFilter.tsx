import React from 'react';
import { 
  Sparkles, 
  Shield, 
  Zap, 
  Activity, 
  Swords, 
  BookOpen, 
  Skull, 
  MapPin, 
  Scroll, 
  Compass,
  Coins,
  Filter,
  X,
  Layers,
  Tag
} from 'lucide-react';
import { 
  CATEGORIES_ENABLED_LIST, 
  isCategoryClickable,
  BOOKS_LIST,
  getSubcategoriesForCategory, 
  getItemTypesForCategory
} from '../data/database';
import type { EntityCategory } from '../types/t20_schema';
import type { SearchFilters } from '../hooks/useUniversalSearch';

interface CategoryFilterProps {
  filters: SearchFilters;
  dynamicCounts: {
    getBookCount: (bookId: string) => number;
    getCategoryCount: (catId: string) => number;
    getSubcategoryCount: (category: string, subcat: string) => number;
    getItemTypeCount: (category: string, subcategory: string, type: string) => number;
  };
  onSelectCategory: (cat: EntityCategory | 'todas') => void;
  onSelectSubcategory: (subcat: string | 'todas') => void;
  onSelectItemType: (type: string | 'todas') => void;
  onSelectBook: (bookId: string | 'todos') => void;
  onMinPriceChange?: (val: number | '') => void;
  onMaxPriceChange?: (val: number | '') => void;
  onSelectPricePreset?: (min: number | '', max: number | '') => void;
  onResetFilters: () => void;
}

const ICON_MAP: Record<string, React.ReactNode> = {
  Compass: <Compass size={17} />,
  Shield: <Shield size={17} />,
  Sparkles: <Sparkles size={17} />,
  Coins: <Coins size={17} />,
  Zap: <Zap size={17} />,
  Activity: <Activity size={17} />,
  Swords: <Swords size={17} />,
  BookOpen: <BookOpen size={17} />,
  Skull: <Skull size={17} />,
  MapPin: <MapPin size={17} />,
  Scroll: <Scroll size={17} />
};

export const CategoryFilter: React.FC<CategoryFilterProps> = ({
  filters,
  dynamicCounts,
  onSelectCategory,
  onSelectSubcategory,
  onSelectItemType,
  onSelectBook,
  onMinPriceChange,
  onMaxPriceChange,
  onSelectPricePreset,
  onResetFilters
}) => {
  const subcategories = getSubcategoriesForCategory(filters.category);
  const itemTypes = getItemTypesForCategory(filters.category, filters.subcategory);

  const showPriceFilter = filters.category === 'equipamento';
  const showSubcategories = subcategories.length > 0 && filters.category !== 'todas';
  const showItemTypes = itemTypes.length > 0 && filters.subcategory !== 'todas';

  const hasActiveFacets = 
    filters.subcategory !== 'todas' || 
    filters.itemType !== 'todas' ||
    filters.book !== 'todos' ||
    (filters.minPrice !== undefined && filters.minPrice !== '') ||
    (filters.maxPrice !== undefined && filters.maxPrice !== '');

  const totalCatCount = dynamicCounts.getCategoryCount(filters.category);
  const totalSubcatCount = dynamicCounts.getSubcategoryCount(filters.category, filters.subcategory);

  const getTypeLabel = () => {
    if (filters.category === 'magia') return 'Escola:';
    if (filters.category === 'poder') {
      if (filters.subcategory === 'Poderes de Classe') return 'Classe:';
      return 'Tipo:';
    }
    if (filters.category === 'manobra') return 'Tipo de Ação:';
    if (filters.category === 'regra') return 'Capítulo:';
    if (filters.category === 'condicao') return 'Categoria:';
    if (filters.category === 'ameaca') return 'Tipo:';
    return 'Tipo:';
  };

  return (
    <div className="category-filter-section">
      {/* ========================================================================= */}
      {/* 📱 1. VISÃO MOBILE: COMBOS DE SELEÇÃO ELEGANTES (UX OTIMIZADA PARA TOUCH) */}
      {/* ========================================================================= */}
      <div className="mobile-filter-combos parchment-card">
        <div className="mobile-combo-header">
          <div className="mobile-combo-title">
            <Filter size={15} className="text-gold" />
            <span>Filtros do Compêndio</span>
          </div>
          {hasActiveFacets && (
            <button className="btn-clean-pill" onClick={onResetFilters}>
              <X size={12} /> Limpar
            </button>
          )}
        </div>

        <div className="mobile-combos-grid">
          {/* Combo 1: Livros */}
          <div className="mobile-select-group">
            <label className="mobile-select-label">
              <BookOpen size={13} /> Livro / Suplemento
            </label>
            <select
              className="mobile-select-combo"
              value={filters.book}
              onChange={e => onSelectBook(e.target.value)}
            >
              {BOOKS_LIST.map(book => {
                const count = dynamicCounts.getBookCount(book.id);
                return (
                  <option key={book.id} value={book.id}>
                    {book.shortLabel} ({count})
                  </option>
                );
              })}
            </select>
          </div>

          {/* Combo 2: Categoria Principal */}
          <div className="mobile-select-group">
            <label className="mobile-select-label">
              <Compass size={13} /> Categoria
            </label>
            <select
              className="mobile-select-combo"
              value={filters.category}
              onChange={e => onSelectCategory(e.target.value as any)}
            >
              {CATEGORIES_ENABLED_LIST.map(cat => {
                const count = dynamicCounts.getCategoryCount(cat.id);
                const isLocked = !isCategoryClickable(cat);
                return (
                  <option key={cat.id} value={cat.id} disabled={isLocked}>
                    {cat.label} ({count}){isLocked ? ' 🔒' : ''}
                  </option>
                );
              })}
            </select>
          </div>

          {/* Combo 3: Subcategoria / Grupo (Quando aplicável) */}
          {showSubcategories && (
            <div className="mobile-select-group">
              <label className="mobile-select-label">
                <Layers size={13} /> Grupo / Subcategoria
              </label>
              <select
                className="mobile-select-combo"
                value={filters.subcategory}
                onChange={e => onSelectSubcategory(e.target.value)}
              >
                <option value="todas">Todas as Subcategorias ({totalCatCount})</option>
                {subcategories.map(sub => {
                  const count = dynamicCounts.getSubcategoryCount(filters.category, sub);
                  return (
                    <option key={sub} value={sub}>
                      {sub} ({count})
                    </option>
                  );
                })}
              </select>
            </div>
          )}

          {/* Combo 4: Tipo / Classificação (Quando aplicável) */}
          {showItemTypes && (
            <div className="mobile-select-group">
              <label className="mobile-select-label">
                <Tag size={13} /> {getTypeLabel()}
              </label>
              <select
                className="mobile-select-combo"
                value={filters.itemType}
                onChange={e => onSelectItemType(e.target.value)}
              >
                <option value="todas">Todos ({totalSubcatCount})</option>
                {itemTypes.map(type => {
                  const count = dynamicCounts.getItemTypeCount(filters.category, filters.subcategory, type);
                  return (
                    <option key={type} value={type}>
                      {type} ({count})
                    </option>
                  );
                })}
              </select>
            </div>
          )}

          {/* Combo 5: Faixa de Preço (Exclusivo Equipamentos - Mobile) */}
          {showPriceFilter && (
            <div className="mobile-select-group" style={{ gridColumn: '1 / -1' }}>
              <label className="mobile-select-label">
                <Coins size={13} /> Faixa de Preço (Tibares - T$)
              </label>
              <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                <input
                  type="number"
                  placeholder="Mín T$"
                  className="mobile-select-combo"
                  value={filters.minPrice ?? ''}
                  onChange={e => onMinPriceChange?.(e.target.value ? Number(e.target.value) : '')}
                  style={{ flex: 1 }}
                />
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>até</span>
                <input
                  type="number"
                  placeholder="Máx T$"
                  className="mobile-select-combo"
                  value={filters.maxPrice ?? ''}
                  onChange={e => onMaxPriceChange?.(e.target.value ? Number(e.target.value) : '')}
                  style={{ flex: 1 }}
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 💻 2. VISÃO DESKTOP: BARRAS DE PILHAS E ABAS MEDIEVAIS DURAIS */}
      {/* ========================================================================= */}
      <div className="desktop-filter-view">
        {/* 0. Filtro por Livro Canônico (Barra de Tomos) */}
        <div className="book-filter-bar">
          <div className="book-filter-label">
            <BookOpen size={15} className="text-gold" />
            <span>Livro / Suplemento:</span>
          </div>
          <div className="book-filter-scroll">
            <div className="book-filter-pills">
              {BOOKS_LIST.map(book => {
                const isSelected = filters.book === book.id;
                const count = dynamicCounts.getBookCount(book.id);
                return (
                  <button
                    key={book.id}
                    className={`book-pill-btn ${isSelected ? 'book-pill-active' : ''}`}
                    onClick={() => onSelectBook(book.id)}
                    aria-pressed={isSelected}
                  >
                    <span className="book-pill-name">{book.shortLabel}</span>
                    <span className={`book-pill-count ${book.badgeClass}`}>({count})</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* 1. Abas Principais de Categoria */}
        <div className="category-tabs-scroll">
          <div className="category-tabs-wrapper">
            {CATEGORIES_ENABLED_LIST.map(cat => {
              const isSelected = filters.category === cat.id;
              const count = dynamicCounts.getCategoryCount(cat.id);
              const isLocked = !isCategoryClickable(cat);
              return (
                <button
                  key={cat.id}
                  className={`category-tab-btn ${isSelected ? 'category-tab-selected' : ''} ${isLocked ? 'category-tab-locked' : ''}`}
                  onClick={isLocked ? undefined : () => onSelectCategory(cat.id)}
                  disabled={isLocked}
                  aria-pressed={isSelected}
                  aria-disabled={isLocked}
                  title={isLocked ? `${cat.label} — em breve` : undefined}
                >
                  <span className="tab-icon">{ICON_MAP[cat.iconName]}</span>
                  <span className="tab-label">{cat.label}</span>
                  <span className={`tab-count ${cat.badgeClass}`}>({count})</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* 2. Painel de Subfiltros Diretos */}
        {(showSubcategories || showItemTypes || showPriceFilter) && (
          <div className="streamlined-filter-panel parchment-card">
            <div className="streamlined-panel-header">
              <div className="streamlined-panel-title">
                <Filter size={15} className="text-gold" />
                <span>Filtro de {CATEGORIES_ENABLED_LIST.find(c => c.id === filters.category)?.label || 'Categoria'}:</span>
              </div>
              {hasActiveFacets && (
                <button className="btn-clean-pill" onClick={onResetFilters} title="Limpar subfiltros">
                  <X size={13} /> Limpar Filtros
                </button>
              )}
            </div>

            {/* Subcategorias Diretas */}
            {showSubcategories && (
              <div className="filter-pill-row">
                <div className="filter-row-prefix">
                  <Layers size={14} className="text-muted" />
                  <span>Grupo:</span>
                </div>
                <div className="filter-pills-container">
                  <button
                    className={`pill-btn ${filters.subcategory === 'todas' ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectSubcategory('todas')}
                  >
                    Todas <span className="pill-badge">({totalCatCount})</span>
                  </button>
                  {subcategories.map(sub => {
                    const count = dynamicCounts.getSubcategoryCount(filters.category, sub);
                    const isSelected = filters.subcategory === sub;
                    return (
                      <button
                        key={sub}
                        className={`pill-btn ${isSelected ? 'pill-btn-active' : ''}`}
                        onClick={() => onSelectSubcategory(sub)}
                      >
                        {sub} <span className="pill-badge">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Tipos / Classificação */}
            {showItemTypes && (
              <div className="filter-pill-row type-pill-row">
                <div className="filter-row-prefix">
                  <Tag size={14} className="text-gold" />
                  <span>{getTypeLabel()}</span>
                </div>
                <div className="filter-pills-container">
                  <button
                    className={`pill-btn pill-btn-secondary ${filters.itemType === 'todas' ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectItemType('todas')}
                  >
                    Todos <span className="pill-badge">({totalSubcatCount})</span>
                  </button>
                  {itemTypes.map(type => {
                    const count = dynamicCounts.getItemTypeCount(filters.category, filters.subcategory, type);
                    const isSelected = filters.itemType === type;
                    return (
                      <button
                        key={type}
                        className={`pill-btn pill-btn-secondary ${isSelected ? 'pill-btn-active' : ''}`}
                        onClick={() => onSelectItemType(type)}
                      >
                        {type} <span className="pill-badge">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Faixa de Valor (Exclusivo Equipamentos) */}
            {showPriceFilter && (
              <div className="filter-pill-row price-filter-row">
                <div className="filter-row-prefix">
                  <Coins size={14} className="text-gold" />
                  <span>Faixa de Valor:</span>
                </div>
                <div className="filter-pills-container" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
                  <button
                    className={`pill-btn ${(!filters.minPrice && !filters.maxPrice) ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectPricePreset?.('', '')}
                  >
                    Todas
                  </button>
                  <button
                    className={`pill-btn ${(filters.minPrice === '' && filters.maxPrice === 10) ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectPricePreset?.('', 10)}
                  >
                    Até T$ 10
                  </button>
                  <button
                    className={`pill-btn ${(filters.minPrice === 10 && filters.maxPrice === 100) ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectPricePreset?.(10, 100)}
                  >
                    T$ 10–100
                  </button>
                  <button
                    className={`pill-btn ${(filters.minPrice === 100 && filters.maxPrice === 1000) ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectPricePreset?.(100, 1000)}
                  >
                    T$ 100–1.000
                  </button>
                  <button
                    className={`pill-btn ${(filters.minPrice === 1000 && filters.maxPrice === '') ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectPricePreset?.(1000, '')}
                  >
                    T$ 1.000+
                  </button>

                  <div className="price-inputs-inline" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', marginLeft: '0.4rem' }}>
                    <input
                      type="number"
                      placeholder="Mín (T$)"
                      value={filters.minPrice ?? ''}
                      onChange={e => onMinPriceChange?.(e.target.value ? Number(e.target.value) : '')}
                      style={{ width: '85px', padding: '0.22rem 0.4rem', fontSize: '0.8rem', borderRadius: '4px', border: '1px solid var(--border-parchment)', background: 'var(--bg-surface)' }}
                    />
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>até</span>
                    <input
                      type="number"
                      placeholder="Máx (T$)"
                      value={filters.maxPrice ?? ''}
                      onChange={e => onMaxPriceChange?.(e.target.value ? Number(e.target.value) : '')}
                      style={{ width: '85px', padding: '0.22rem 0.4rem', fontSize: '0.8rem', borderRadius: '4px', border: '1px solid var(--border-parchment)', background: 'var(--bg-surface)' }}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
