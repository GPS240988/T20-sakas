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
  CATEGORIES_LIST, 
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
  onResetFilters
}) => {
  const subcategories = getSubcategoriesForCategory(filters.category);
  const itemTypes = getItemTypesForCategory(filters.category, filters.subcategory);

  const hasActiveFacets = 
    filters.subcategory !== 'todas' || 
    filters.itemType !== 'todas' ||
    filters.book !== 'todos';

  const showSubcategories = subcategories.length > 0 && filters.category !== 'todas';
  const showItemTypes = itemTypes.length > 1 && filters.subcategory !== 'todas';

  const totalCatCount = dynamicCounts.getCategoryCount(filters.category);
  const totalSubcatCount = dynamicCounts.getSubcategoryCount(filters.category, filters.subcategory);

  const getTypeLabel = () => {
    if (filters.category === 'magia') return 'Escola:';
    if (filters.category === 'poder') return 'Tipo de Poder:';
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
              {CATEGORIES_LIST.map(cat => {
                const count = dynamicCounts.getCategoryCount(cat.id);
                return (
                  <option key={cat.id} value={cat.id}>
                    {cat.label} ({count})
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
            {CATEGORIES_LIST.map(cat => {
              const isSelected = filters.category === cat.id;
              const count = dynamicCounts.getCategoryCount(cat.id);
              return (
                <button
                  key={cat.id}
                  className={`category-tab-btn ${isSelected ? 'category-tab-selected' : ''}`}
                  onClick={() => onSelectCategory(cat.id)}
                  aria-pressed={isSelected}
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
        {(showSubcategories || showItemTypes) && (
          <div className="streamlined-filter-panel parchment-card">
            <div className="streamlined-panel-header">
              <div className="streamlined-panel-title">
                <Filter size={15} className="text-gold" />
                <span>Filtro de {CATEGORIES_LIST.find(c => c.id === filters.category)?.label || 'Categoria'}:</span>
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
          </div>
        )}
      </div>
    </div>
  );
};
