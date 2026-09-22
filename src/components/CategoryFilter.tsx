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
  Tag,
  Wand2,
  Target
} from 'lucide-react';
import { 
  CATEGORIES_ENABLED_LIST, 
  isCategoryClickable,
  BOOKS_LIST,
  getSubcategoriesForCategory, 
  getItemTypesForCategory,
  SPELL_CIRCLES_INFO,
  getMagicRarities,
  getTreasureNDRanges
} from '../data/database';
import type { EntityCategory } from '../types/t20_schema';
import type { SearchFilters } from '../hooks/useUniversalSearch';

interface CategoryFilterProps {
  filters: SearchFilters;
  dynamicCounts: {
    getBookCount: (bookId: string) => number;
    getCategoryCount: (catId: string) => number;
    getSubcategoryCount: (category: string, subcat: string) => number;
    getItemTypeCount: (category: string, subcategory: string | string[] | 'todas', type: string) => number;
    getSpellCircleCount?: (circle: number | 'todos') => number;
    getMagicRarityCount?: (rarity: string | 'todas') => number;
    getNdRangeCount?: (ndRange: string | 'todos') => number;
  };
  onSelectCategory: (cat: EntityCategory | 'todas') => void;
  onSelectSubcategory: (subcat: string | 'todas') => void;
  onSelectItemType: (type: string | 'todas') => void;
  onSelectBook: (bookId: string | 'todos') => void;
  onSelectSpellCircle?: (circle: number | 'todos') => void;
  onSelectMagicRarity?: (rarity: string | 'todas') => void;
  onSelectNdRange?: (ndRange: string | 'todos') => void;
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

// ============================================================================
// Helpers de Multi-Seleção
// ============================================================================

/** Verifica se um valor está selecionado num filtro multi-select */
function isSubcatSelected(filter: string[] | 'todas', value: string): boolean {
  if (filter === 'todas') return false;
  return (filter as string[]).includes(value);
}

function isItemTypeSelected(filter: string[] | 'todas', value: string): boolean {
  if (filter === 'todas') return false;
  return (filter as string[]).includes(value);
}

function isCircleSelected(filter: number[] | 'todos' | undefined, value: number): boolean {
  if (filter === undefined || filter === 'todos') return false;
  return (filter as number[]).includes(value);
}

/** Conta quantas seleções ativas existem num filtro */
function multiSelectCount(filter: string[] | number[] | 'todas' | 'todos' | undefined): number {
  if (filter === undefined || filter === 'todas' || filter === 'todos') return 0;
  return (filter as any[]).length;
}


export const CategoryFilter: React.FC<CategoryFilterProps> = ({
  filters,
  dynamicCounts,
  onSelectCategory,
  onSelectSubcategory,
  onSelectItemType,
  onSelectBook,
  onSelectSpellCircle,
  onSelectMagicRarity,
  onSelectNdRange,
  onMinPriceChange,
  onMaxPriceChange,
  onSelectPricePreset,
  onResetFilters
}) => {
  const subcategories = getSubcategoriesForCategory(filters.category);
  const itemTypes = getItemTypesForCategory(filters.category, filters.subcategory === 'todas' ? undefined : filters.subcategory);

  const showPriceFilter = filters.category === 'equipamento';
  const showSubcategories = subcategories.length > 0 && filters.category !== 'todas';
  const showItemTypes = itemTypes.length > 0 && (filters.category === 'magia' || filters.subcategory !== 'todas');
  const showSpellCircles = filters.category === 'magia';
  const showMagicRarities = filters.category === 'equipamento' && 
    filters.subcategory !== 'todas' && 
    (filters.subcategory as string[]).includes('Itens Mágicos');
  const showNdRanges = filters.category === 'tesouro';

  const magicRarities = getMagicRarities();
  const ndRanges = getTreasureNDRanges();

  const hasActiveFacets = 
    filters.subcategory !== 'todas' || 
    filters.itemType !== 'todas' ||
    filters.book !== 'todos' ||
    filters.spellCircle !== 'todos' ||
    filters.magicRarity !== 'todas' ||
    filters.ndRange !== 'todos' ||
    (filters.minPrice !== undefined && filters.minPrice !== '') ||
    (filters.maxPrice !== undefined && filters.maxPrice !== '');

  const totalCatCount = dynamicCounts.getCategoryCount(filters.category);
  const totalSubcatCount = (() => {
    if (filters.subcategory === 'todas') return totalCatCount;
    // Para multi-seleção, soma as contagens das subcategorias selecionadas
    const subs = filters.subcategory as string[];
    let sum = 0;
    for (const sub of subs) {
      sum += dynamicCounts.getSubcategoryCount(filters.category, sub);
    }
    return sum;
  })();

  const getTypeLabel = () => {
    if (filters.category === 'magia') return 'Escola:';
    if (filters.category === 'poder') {
      if (filters.subcategory !== 'todas' && (filters.subcategory as string[]).includes('Poderes de Classe')) return 'Classe:';
      return 'Tipo:';
    }
    if (filters.category === 'manobra') return 'Tipo de Ação:';
    if (filters.category === 'regra') return 'Capítulo:';
    if (filters.category === 'condicao') return 'Categoria:';
    if (filters.category === 'ameaca') return 'Tipo:';
    return 'Tipo:';
  };

  // Para mobile: chips dos filtros ativos de subcategoria
  const activeSubcatChips: string[] = filters.subcategory === 'todas' ? [] : (filters.subcategory as string[]);
  const activeTypeChips: string[] = filters.itemType === 'todas' ? [] : (filters.itemType as string[]);
  const activeCircleChips: number[] = filters.spellCircle === 'todos' || filters.spellCircle === undefined ? [] : (filters.spellCircle as number[]);

  const showPanel = showSubcategories || showItemTypes || showPriceFilter || showSpellCircles || showMagicRarities || showNdRanges;

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

          {/* Combo 3: Subcategoria / Grupo (Multi-Seleção via Select + Chips) */}
          {showSubcategories && (
            <div className="mobile-select-group" style={{ gridColumn: '1 / -1' }}>
              <label className="mobile-select-label">
                <Layers size={13} /> Grupo / Subcategoria
                {activeSubcatChips.length > 0 && (
                  <span className="mobile-filter-badge">{activeSubcatChips.length}</span>
                )}
              </label>
              <select
                className="mobile-select-combo"
                value=""
                onChange={e => {
                  const val = e.target.value;
                  if (val === 'todas') onSelectSubcategory('todas');
                  else if (val) onSelectSubcategory(val);
                }}
              >
                <option value="" disabled>
                  {activeSubcatChips.length > 0 ? `${activeSubcatChips.length} filtros ativos` : 'Selecionar Grupo…'}
                </option>
                <option value="todas">✦ Todas as Subcategorias ({totalCatCount})</option>
                {subcategories.map(sub => {
                  const count = dynamicCounts.getSubcategoryCount(filters.category, sub);
                  const isSelected = isSubcatSelected(filters.subcategory, sub);
                  return (
                    <option key={sub} value={sub}>
                      {isSelected ? '✓ ' : ''}{sub} ({count})
                    </option>
                  );
                })}
              </select>
              {/* Chips ativas mostrando filtros selecionados */}
              {activeSubcatChips.length > 0 && (
                <div className="active-filter-chips">
                  {activeSubcatChips.map(chip => (
                    <button
                      key={chip}
                      className="active-chip"
                      onClick={() => onSelectSubcategory(chip)}
                      title={`Remover filtro: ${chip}`}
                    >
                      {chip}
                      <X size={11} />
                    </button>
                  ))}
                  {activeSubcatChips.length > 1 && (
                    <button
                      className="active-chip active-chip-clear"
                      onClick={() => onSelectSubcategory('todas')}
                    >
                      Limpar todos
                    </button>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Combo 4: Círculo de Magias (Multi-Seleção) */}
          {showSpellCircles && (
            <div className="mobile-select-group">
              <label className="mobile-select-label">
                <Wand2 size={13} className="text-mana" /> Círculo da Magia
                {activeCircleChips.length > 0 && (
                  <span className="mobile-filter-badge">{activeCircleChips.length}</span>
                )}
              </label>
              <select
                className="mobile-select-combo"
                value=""
                onChange={e => {
                  const val = e.target.value;
                  if (val === 'todos') onSelectSpellCircle?.('todos');
                  else if (val) onSelectSpellCircle?.(Number(val));
                }}
              >
                <option value="" disabled>
                  {activeCircleChips.length > 0 ? `${activeCircleChips.length} círculos ativos` : 'Selecionar Círculo…'}
                </option>
                <option value="todos">✦ Todos os Círculos ({dynamicCounts.getSpellCircleCount?.('todos') ?? totalCatCount})</option>
                {SPELL_CIRCLES_INFO.map(sc => {
                  const count = dynamicCounts.getSpellCircleCount?.(sc.circle) ?? 0;
                  const isSelected = isCircleSelected(filters.spellCircle, sc.circle);
                  return (
                    <option key={sc.circle} value={sc.circle}>
                      {isSelected ? '✓ ' : ''}{sc.label} ({sc.pm}) — {count} magias
                    </option>
                  );
                })}
              </select>
              {activeCircleChips.length > 0 && (
                <div className="active-filter-chips">
                  {activeCircleChips.map(circle => {
                    const info = SPELL_CIRCLES_INFO.find(sc => sc.circle === circle);
                    return (
                      <button
                        key={circle}
                        className="active-chip active-chip-mana"
                        onClick={() => onSelectSpellCircle?.(circle)}
                        title={`Remover filtro: ${info?.label}`}
                      >
                        {info?.label}
                        <X size={11} />
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* Combo 5: Tipo / Classificação / Escola (Multi-Seleção) */}
          {showItemTypes && (
            <div className="mobile-select-group" style={{ gridColumn: '1 / -1' }}>
              <label className="mobile-select-label">
                <Tag size={13} /> {getTypeLabel()}
                {activeTypeChips.length > 0 && (
                  <span className="mobile-filter-badge">{activeTypeChips.length}</span>
                )}
              </label>
              <select
                className="mobile-select-combo"
                value=""
                onChange={e => {
                  const val = e.target.value;
                  if (val === 'todas') onSelectItemType('todas');
                  else if (val) onSelectItemType(val);
                }}
              >
                <option value="" disabled>
                  {activeTypeChips.length > 0 ? `${activeTypeChips.length} tipos ativos` : 'Selecionar Tipo…'}
                </option>
                <option value="todas">✦ Todos ({dynamicCounts.getItemTypeCount(filters.category, filters.subcategory, 'todas')})</option>
                {itemTypes.map(type => {
                  const count = dynamicCounts.getItemTypeCount(filters.category, filters.subcategory, type);
                  const isSelected = isItemTypeSelected(filters.itemType, type);
                  return (
                    <option key={type} value={type}>
                      {isSelected ? '✓ ' : ''}{type} ({count})
                    </option>
                  );
                })}
              </select>
              {activeTypeChips.length > 0 && (
                <div className="active-filter-chips">
                  {activeTypeChips.map(type => (
                    <button
                      key={type}
                      className="active-chip"
                      onClick={() => onSelectItemType(type)}
                      title={`Remover filtro: ${type}`}
                    >
                      {type}
                      <X size={11} />
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Combo 6: Raridade Mágica (Exclusivo Itens Mágicos) */}
          {showMagicRarities && (
            <div className="mobile-select-group">
              <label className="mobile-select-label">
                <Sparkles size={13} className="text-gold" /> Raridade Mágica
              </label>
              <select
                className="mobile-select-combo"
                value={filters.magicRarity ?? 'todas'}
                onChange={e => onSelectMagicRarity?.(e.target.value)}
              >
                <option value="todas">Todas as Raridades ({totalSubcatCount})</option>
                {magicRarities.map(r => {
                  const count = dynamicCounts.getMagicRarityCount?.(r) ?? 0;
                  return (
                    <option key={r} value={r}>
                      {r} ({count})
                    </option>
                  );
                })}
              </select>
            </div>
          )}

          {/* Combo 7: Faixa de ND (Exclusivo Tesouros) */}
          {showNdRanges && (
            <div className="mobile-select-group">
              <label className="mobile-select-label">
                <Target size={13} className="text-gold" /> Nível de Desafio (ND)
              </label>
              <select
                className="mobile-select-combo"
                value={filters.ndRange ?? 'todos'}
                onChange={e => onSelectNdRange?.(e.target.value)}
              >
                <option value="todos">Todos os NDs ({totalCatCount})</option>
                {ndRanges.map(nd => {
                  const count = dynamicCounts.getNdRangeCount?.(nd) ?? 0;
                  return (
                    <option key={nd} value={nd}>
                      {nd} ({count})
                    </option>
                  );
                })}
              </select>
            </div>
          )}

          {/* Combo 8: Faixa de Preço (Exclusivo Equipamentos - Mobile) */}
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
        {showPanel && (
          <div className="streamlined-filter-panel parchment-card">
            <div className="streamlined-panel-header">
              <div className="streamlined-panel-title">
                <Filter size={15} className="text-gold" />
                <span>Filtro de {CATEGORIES_ENABLED_LIST.find(c => c.id === filters.category)?.label || 'Categoria'}:</span>
                {multiSelectCount(filters.subcategory) + multiSelectCount(filters.itemType) + multiSelectCount(filters.spellCircle) > 0 && (
                  <span className="multi-select-indicator">
                    {multiSelectCount(filters.subcategory) + multiSelectCount(filters.itemType) + multiSelectCount(filters.spellCircle)} filtros ativos
                  </span>
                )}
              </div>
              {hasActiveFacets && (
                <button className="btn-clean-pill" onClick={onResetFilters} title="Limpar subfiltros">
                  <X size={13} /> Limpar Filtros
                </button>
              )}
            </div>

            {/* Subcategorias Diretas (Multi-Seleção Toggle) */}
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
                    const isSelected = isSubcatSelected(filters.subcategory, sub);
                    return (
                      <button
                        key={sub}
                        className={`pill-btn ${isSelected ? 'pill-btn-active pill-btn-multi' : ''}`}
                        onClick={() => onSelectSubcategory(sub)}
                      >
                        {isSelected && <span className="pill-check">✓</span>}
                        {sub} <span className="pill-badge">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Círculo da Magia (1º ao 5º — Multi-Seleção) */}
            {showSpellCircles && (
              <div className="filter-pill-row circle-pill-row">
                <div className="filter-row-prefix">
                  <Wand2 size={14} className="text-mana" />
                  <span>Círculo:</span>
                </div>
                <div className="filter-pills-container">
                  <button
                    className={`pill-btn pill-btn-mana ${filters.spellCircle === 'todos' ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectSpellCircle?.('todos')}
                  >
                    Todos <span className="pill-badge">({dynamicCounts.getSpellCircleCount?.('todos') ?? totalCatCount})</span>
                  </button>
                  {SPELL_CIRCLES_INFO.map(sc => {
                    const count = dynamicCounts.getSpellCircleCount?.(sc.circle) ?? 0;
                    const isSelected = isCircleSelected(filters.spellCircle, sc.circle);
                    return (
                      <button
                        key={sc.circle}
                        className={`pill-btn pill-btn-mana ${isSelected ? 'pill-btn-active pill-btn-multi' : ''}`}
                        onClick={() => onSelectSpellCircle?.(sc.circle)}
                      >
                        {isSelected && <span className="pill-check">✓</span>}
                        {sc.label} <span className="pill-pm-tag">({sc.pm})</span> <span className="pill-badge">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Tipos / Classificação / Escola (Multi-Seleção) */}
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
                    Todos <span className="pill-badge">({dynamicCounts.getItemTypeCount(filters.category, filters.subcategory, 'todas')})</span>
                  </button>
                  {itemTypes.map(type => {
                    const count = dynamicCounts.getItemTypeCount(filters.category, filters.subcategory, type);
                    const isSelected = isItemTypeSelected(filters.itemType, type);
                    return (
                      <button
                        key={type}
                        className={`pill-btn pill-btn-secondary ${isSelected ? 'pill-btn-active pill-btn-multi' : ''}`}
                        onClick={() => onSelectItemType(type)}
                      >
                        {isSelected && <span className="pill-check">✓</span>}
                        {type} <span className="pill-badge">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Raridade Mágica (Exclusivo Itens Mágicos) */}
            {showMagicRarities && (
              <div className="filter-pill-row rarity-pill-row">
                <div className="filter-row-prefix">
                  <Sparkles size={14} className="text-gold" />
                  <span>Raridade:</span>
                </div>
                <div className="filter-pills-container">
                  <button
                    className={`pill-btn ${filters.magicRarity === 'todas' ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectMagicRarity?.('todas')}
                  >
                    Todas <span className="pill-badge">({totalSubcatCount})</span>
                  </button>
                  {magicRarities.map(r => {
                    const count = dynamicCounts.getMagicRarityCount?.(r) ?? 0;
                    const isSelected = filters.magicRarity === r;
                    return (
                      <button
                        key={r}
                        className={`pill-btn ${isSelected ? 'pill-btn-active' : ''}`}
                        onClick={() => onSelectMagicRarity?.(r)}
                      >
                        {r} <span className="pill-badge">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Faixa de ND (Exclusivo Tesouros) */}
            {showNdRanges && (
              <div className="filter-pill-row nd-pill-row">
                <div className="filter-row-prefix">
                  <Target size={14} className="text-gold" />
                  <span>Faixa de ND:</span>
                </div>
                <div className="filter-pills-container">
                  <button
                    className={`pill-btn ${filters.ndRange === 'todos' ? 'pill-btn-active' : ''}`}
                    onClick={() => onSelectNdRange?.('todos')}
                  >
                    Todos <span className="pill-badge">({totalCatCount})</span>
                  </button>
                  {ndRanges.map(nd => {
                    const count = dynamicCounts.getNdRangeCount?.(nd) ?? 0;
                    const isSelected = filters.ndRange === nd;
                    return (
                      <button
                        key={nd}
                        className={`pill-btn ${isSelected ? 'pill-btn-active' : ''}`}
                        onClick={() => onSelectNdRange?.(nd)}
                      >
                        {nd} <span className="pill-badge">({count})</span>
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
