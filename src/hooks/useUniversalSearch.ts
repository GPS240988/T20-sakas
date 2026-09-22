import { useState, useMemo } from 'react';
import { SEARCHABLE_DATABASE, type SearchableEntity } from '../data/database';
import type { EntityCategory } from '../types/t20_schema';
import { removeAccents } from '../utils/textUtils';

export interface SearchFilters {
  category: EntityCategory | 'todas';
  subcategory: string[] | 'todas';
  itemType: string[] | 'todas';
  book: string | 'todos';
  minPrice?: number | '';
  maxPrice?: number | '';
  spellCircle?: number[] | 'todos';
  magicRarity?: string | 'todas';
  ndRange?: string | 'todos';
}

// ============================================================================
// Helpers de Matching
// ============================================================================

function matchesBook(item: SearchableEntity, bookId: string): boolean {
  if (bookId === 'todos') return true;
  return item._normalizedBooks.some(b => {
    if (bookId.includes('Jogo do Ano')) return b.includes('Jogo do Ano');
    if (bookId.includes('Heróis')) return b.includes('Heróis');
    if (bookId.includes('Ameaças')) return b.includes('Ameaças');
    if (bookId.includes('Atlas')) return b.includes('Atlas');
    return b === bookId;
  });
}

function matchesQuery(item: SearchableEntity, qTokens: string[]): boolean {
  if (qTokens.length === 0) return true;
  for (let i = 0; i < qTokens.length; i++) {
    if (!item._searchText.includes(qTokens[i])) return false;
  }
  return true;
}

/** Verifica se um valor está incluído em um filtro multi-seleção */
function matchesMultiFilter<T>(filterVal: T[] | 'todas' | 'todos', itemVal: T | undefined): boolean {
  if (filterVal === 'todas' || filterVal === 'todos') return true;
  if (itemVal === undefined) return false;
  return (filterVal as T[]).includes(itemVal);
}

export function useUniversalSearch() {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({
    category: 'todas',
    subcategory: 'todas',
    itemType: 'todas',
    book: 'todos',
    spellCircle: 'todos',
    magicRarity: 'todas',
    ndRange: 'todos'
  });

  const filteredResults = useMemo(() => {
    const q = removeAccents(query.trim());
    const qTokens = q ? q.split(/\s+/).filter(Boolean) : [];
    const minP = filters.minPrice !== undefined && filters.minPrice !== '' ? Number(filters.minPrice) : null;
    const maxP = filters.maxPrice !== undefined && filters.maxPrice !== '' ? Number(filters.maxPrice) : null;

    return SEARCHABLE_DATABASE.filter(item => {
      // 1. Filtro de Livro Oficial
      if (filters.book !== 'todos' && !matchesBook(item, filters.book)) {
        return false;
      }

      // 2. Filtro de Categoria Principal
      if (filters.category !== 'todas' && item.category !== filters.category) {
        return false;
      }

      // 3. Filtro de Subcategoria Direta (Multi-Seleção)
      if (!matchesMultiFilter(filters.subcategory, item.subcategory)) {
        return false;
      }

      // 4. Filtro de Tipo / Classificação / Escola (Multi-Seleção)
      if (!matchesMultiFilter(filters.itemType, item._itemType || undefined)) {
        return false;
      }

      // 4.5. Filtro de Faixa de Valor (Exclusivo para Equipamentos)
      if (item.category === 'equipamento') {
        if (minP !== null && (item._parsedPrice === null || item._parsedPrice < minP)) return false;
        if (maxP !== null && (item._parsedPrice === null || item._parsedPrice > maxP)) return false;
      }

      // 4.6. Filtro de Círculo de Magia (Multi-Seleção)
      if (filters.spellCircle !== undefined && filters.spellCircle !== 'todos' && item.category === 'magia') {
        if (!matchesMultiFilter(filters.spellCircle, item._spellCircle)) return false;
      }

      // 4.7. Filtro de Raridade Mágica
      if (filters.magicRarity !== undefined && filters.magicRarity !== 'todas' && item.category === 'equipamento') {
        if (item._magicRarity !== filters.magicRarity) return false;
      }

      // 4.8. Filtro de Faixa de ND (Tesouros)
      if (filters.ndRange !== undefined && filters.ndRange !== 'todos' && item.category === 'tesouro') {
        if (item._ndRange !== filters.ndRange) return false;
      }

      // 5. Busca Universal Instantânea
      if (qTokens.length > 0 && !matchesQuery(item, qTokens)) {
        return false;
      }

      return true;
    });
  }, [query, filters]);

  // Contadores dinâmicos agregados em passada única O(N) com Map Hash
  const dynamicCounts = useMemo(() => {
    const q = removeAccents(query.trim());
    const qTokens = q ? q.split(/\s+/).filter(Boolean) : [];
    const minP = filters.minPrice !== undefined && filters.minPrice !== '' ? Number(filters.minPrice) : null;
    const maxP = filters.maxPrice !== undefined && filters.maxPrice !== '' ? Number(filters.maxPrice) : null;

    // Pre-filter comum por Query e Preço
    const baseCandidates = SEARCHABLE_DATABASE.filter(item => {
      if (minP !== null && item.category === 'equipamento') {
        if (item._parsedPrice === null || item._parsedPrice < minP) return false;
      }
      if (maxP !== null && item.category === 'equipamento') {
        if (item._parsedPrice === null || item._parsedPrice > maxP) return false;
      }
      if (qTokens.length > 0 && !matchesQuery(item, qTokens)) return false;
      return true;
    });

    const bookCountMap = new Map<string, number>();
    const categoryCountMap = new Map<string, number>();
    const subcategoryCountMap = new Map<string, number>();
    const itemTypeCountMap = new Map<string, number>();
    const itemTypeTotalCountMap = new Map<string, number>();
    const spellCircleCountMap = new Map<number | 'todos', number>();
    const magicRarityCountMap = new Map<string, number>();
    const ndRangeCountMap = new Map<string, number>();

    const targetCategory = filters.category;
    const targetSubcat = filters.subcategory;
    const targetType = filters.itemType;
    const targetBook = filters.book;
    const targetCircle = filters.spellCircle;
    const targetRarity = filters.magicRarity;
    const targetNdRange = filters.ndRange;

    for (let i = 0; i < baseCandidates.length; i++) {
      const item = baseCandidates[i];

      // Agregação de Categorias e Subcategorias (respeitando o filtro de Livro ativo)
      if (matchesBook(item, targetBook)) {
        categoryCountMap.set(item.category, (categoryCountMap.get(item.category) || 0) + 1);
        categoryCountMap.set('todas', (categoryCountMap.get('todas') || 0) + 1);

        if (item.subcategory) {
          const subKey = `${item.category}:::${item.subcategory}`;
          subcategoryCountMap.set(subKey, (subcategoryCountMap.get(subKey) || 0) + 1);
        }

        // Agregação de Tipos / Escolas (itemType):
        // Para Magias: respeita targetCircle (quando filtrado por Círculo, a contagem de cada Escola atualiza)
        const matchesCategoryForType = targetCategory === 'todas' || item.category === targetCategory;
        const matchesCircleForType = item.category !== 'magia' || targetCircle === undefined || targetCircle === 'todos' || matchesMultiFilter(targetCircle, item._spellCircle);
        const matchesSubcatForType = targetSubcat === 'todas' || matchesMultiFilter(targetSubcat, item.subcategory);

        if (matchesCategoryForType && matchesCircleForType && matchesSubcatForType) {
          itemTypeTotalCountMap.set(item.category, (itemTypeTotalCountMap.get(item.category) || 0) + 1);
          if (item._itemType) {
            if (item.subcategory) {
              const typeKey = `${item.category}:::${item.subcategory}:::${item._itemType}`;
              itemTypeCountMap.set(typeKey, (itemTypeCountMap.get(typeKey) || 0) + 1);
            }
            const globalTypeKey = `${item.category}:::todas:::${item._itemType}`;
            itemTypeCountMap.set(globalTypeKey, (itemTypeCountMap.get(globalTypeKey) || 0) + 1);
          }
        }

        // Agregação de Círculos de Magia:
        // Respeita targetSubcat (Grupo) e targetType (Escola) se ativos!
        if (item.category === 'magia' && item._spellCircle !== undefined) {
          const matchesSubcatForCircle = targetSubcat === 'todas' || matchesMultiFilter(targetSubcat, item.subcategory);
          const matchesTypeForCircle = targetType === 'todas' || matchesMultiFilter(targetType, item._itemType);
          if (matchesSubcatForCircle && matchesTypeForCircle) {
            spellCircleCountMap.set(item._spellCircle, (spellCircleCountMap.get(item._spellCircle) || 0) + 1);
            spellCircleCountMap.set('todos', (spellCircleCountMap.get('todos') || 0) + 1);
          }
        }

        // Agregação de Raridade Mágica (Equipamentos)
        if (item.category === 'equipamento' && item._magicRarity) {
          magicRarityCountMap.set(item._magicRarity, (magicRarityCountMap.get(item._magicRarity) || 0) + 1);
        }

        // Agregação de Faixa de ND (Tesouros)
        if (item.category === 'tesouro' && item._ndRange) {
          ndRangeCountMap.set(item._ndRange, (ndRangeCountMap.get(item._ndRange) || 0) + 1);
        }
      }

      // Agregação de Livros
      const matchesCurrentFacets = 
        (targetCategory === 'todas' || item.category === targetCategory) &&
        (targetSubcat === 'todas' || matchesMultiFilter(targetSubcat, item.subcategory)) &&
        (targetType === 'todas' || matchesMultiFilter(targetType, item._itemType || undefined)) &&
        (item.category !== 'magia' || targetCircle === undefined || targetCircle === 'todos' || matchesMultiFilter(targetCircle, item._spellCircle)) &&
        (item.category !== 'equipamento' || targetRarity === undefined || targetRarity === 'todas' || item._magicRarity === targetRarity) &&
        (item.category !== 'tesouro' || targetNdRange === undefined || targetNdRange === 'todos' || item._ndRange === targetNdRange);

      if (matchesCurrentFacets) {
        bookCountMap.set('todos', (bookCountMap.get('todos') || 0) + 1);
        for (let b = 0; b < item._normalizedBooks.length; b++) {
          const bk = item._normalizedBooks[b];
          bookCountMap.set(bk, (bookCountMap.get(bk) || 0) + 1);
        }
      }
    }

    return {
      getBookCount: (bookId: string) => {
        if (bookId === 'todos') return bookCountMap.get('todos') || 0;
        let count = 0;
        for (const [bk, cnt] of bookCountMap.entries()) {
          if (bk === 'todos') continue;
          if (bookId.includes('Jogo do Ano') && bk.includes('Jogo do Ano')) count += cnt;
          else if (bookId.includes('Heróis') && bk.includes('Heróis')) count += cnt;
          else if (bookId.includes('Ameaças') && bk.includes('Ameaças')) count += cnt;
          else if (bookId.includes('Atlas') && bk.includes('Atlas')) count += cnt;
          else if (bk === bookId) count += cnt;
        }
        return count;
      },
      getCategoryCount: (catId: string) => {
        return categoryCountMap.get(catId) || 0;
      },
      getSubcategoryCount: (category: string, subcat: string) => {
        if (subcat === 'todas') return categoryCountMap.get(category) || 0;
        return subcategoryCountMap.get(`${category}:::${subcat}`) || 0;
      },
      getItemTypeCount: (category: string, _subcategory: string | string[] | 'todas', type: string) => {
        if (type === 'todas') return itemTypeTotalCountMap.get(category) || 0;
        return itemTypeCountMap.get(`${category}:::todas:::${type}`) || 0;
      },
      getSpellCircleCount: (circle: number | 'todos') => {
        return spellCircleCountMap.get(circle) || 0;
      },
      getMagicRarityCount: (rarity: string | 'todas') => {
        if (rarity === 'todas') return subcategoryCountMap.get('equipamento:::Itens Mágicos') || 0;
        return magicRarityCountMap.get(rarity) || 0;
      },
      getNdRangeCount: (ndRange: string | 'todos') => {
        if (ndRange === 'todos') return categoryCountMap.get('tesouro') || 0;
        return ndRangeCountMap.get(ndRange) || 0;
      }
    };
  }, [query, filters]);

  // ============================================================================
  // Setters com Toggle Multi-Seleção
  // ============================================================================

  const setCategory = (cat: EntityCategory | 'todas') => {
    setFilters(prev => ({ 
      ...prev,
      category: cat, 
      subcategory: 'todas',
      itemType: 'todas',
      spellCircle: 'todos',
      magicRarity: 'todas',
      ndRange: 'todos',
      minPrice: cat === 'equipamento' ? prev.minPrice : '',
      maxPrice: cat === 'equipamento' ? prev.maxPrice : ''
    }));
  };

  /** Toggle multi-seleção para subcategoria (Grupo) */
  const setSubcategory = (subcat: string | 'todas') => {
    setFilters(prev => {
      if (subcat === 'todas') {
        return { ...prev, subcategory: 'todas', itemType: 'todas', magicRarity: 'todas' };
      }
      const current = prev.subcategory === 'todas' ? [] : (prev.subcategory as string[]);
      const idx = current.indexOf(subcat);
      let next: string[];
      if (idx >= 0) {
        next = current.filter(s => s !== subcat);
      } else {
        next = [...current, subcat];
      }
      if (next.length === 0) {
        return { ...prev, subcategory: 'todas', itemType: 'todas', magicRarity: 'todas' };
      }
      return { ...prev, subcategory: next, itemType: 'todas', magicRarity: 'todas' };
    });
  };

  /** Toggle multi-seleção para itemType (Escola/Tipo) */
  const setItemType = (type: string | 'todas') => {
    setFilters(prev => {
      if (type === 'todas') {
        return { ...prev, itemType: 'todas' };
      }
      const current = prev.itemType === 'todas' ? [] : (prev.itemType as string[]);
      const idx = current.indexOf(type);
      let next: string[];
      if (idx >= 0) {
        next = current.filter(t => t !== type);
      } else {
        next = [...current, type];
      }
      if (next.length === 0) {
        return { ...prev, itemType: 'todas' };
      }
      return { ...prev, itemType: next };
    });
  };

  const setBook = (bookId: string | 'todos') => {
    setFilters(prev => ({
      ...prev,
      book: bookId
    }));
  };

  /** Toggle multi-seleção para Círculo de Magia */
  const setSpellCircle = (circle: number | 'todos') => {
    setFilters(prev => {
      if (circle === 'todos') {
        return { ...prev, spellCircle: 'todos' };
      }
      const current = prev.spellCircle === 'todos' || prev.spellCircle === undefined ? [] : (prev.spellCircle as number[]);
      const idx = current.indexOf(circle);
      let next: number[];
      if (idx >= 0) {
        next = current.filter(c => c !== circle);
      } else {
        next = [...current, circle];
      }
      if (next.length === 0) {
        return { ...prev, spellCircle: 'todos' };
      }
      return { ...prev, spellCircle: next };
    });
  };

  const setMagicRarity = (rarity: string | 'todas') => {
    setFilters(prev => ({ ...prev, magicRarity: rarity }));
  };

  const setNdRange = (ndRange: string | 'todos') => {
    setFilters(prev => ({ ...prev, ndRange: ndRange }));
  };

  const setMinPrice = (val: number | '') => {
    setFilters(prev => ({ ...prev, minPrice: val }));
  };

  const setMaxPrice = (val: number | '') => {
    setFilters(prev => ({ ...prev, maxPrice: val }));
  };

  const setPriceRange = (min: number | '', max: number | '') => {
    setFilters(prev => ({ ...prev, minPrice: min, maxPrice: max }));
  };

  const resetFilters = () => {
    setQuery('');
    setFilters({
      category: 'todas',
      subcategory: 'todas',
      itemType: 'todas',
      book: 'todos',
      minPrice: '',
      maxPrice: '',
      spellCircle: 'todos',
      magicRarity: 'todas',
      ndRange: 'todos'
    });
  };

  return {
    query,
    setQuery,
    filters,
    setCategory,
    setSubcategory,
    setItemType,
    setBook,
    setSpellCircle,
    setMagicRarity,
    setNdRange,
    setMinPrice,
    setMaxPrice,
    setPriceRange,
    resetFilters,
    dynamicCounts,
    results: filteredResults,
    totalCount: SEARCHABLE_DATABASE.length
  };
}
