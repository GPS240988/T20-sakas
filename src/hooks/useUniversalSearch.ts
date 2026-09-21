import { useState, useMemo } from 'react';
import { SEARCHABLE_DATABASE, type SearchableEntity } from '../data/database';
import type { EntityCategory } from '../types/t20_schema';
import { removeAccents } from '../utils/textUtils';

export interface SearchFilters {
  category: EntityCategory | 'todas';
  subcategory: string | 'todas';
  itemType: string | 'todas';
  book: string | 'todos';
  minPrice?: number | '';
  maxPrice?: number | '';
}

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

export function useUniversalSearch() {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({
    category: 'todas',
    subcategory: 'todas',
    itemType: 'todas',
    book: 'todos'
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

      // 3. Filtro de Subcategoria Direta
      if (filters.subcategory !== 'todas' && item.subcategory !== filters.subcategory) {
        return false;
      }

      // 4. Filtro de Tipo / Classificação / Escola
      if (filters.itemType !== 'todas' && item._itemType !== filters.itemType) {
        return false;
      }

      // 4.5. Filtro de Faixa de Valor (Exclusivo para Equipamentos)
      if (item.category === 'equipamento') {
        if (minP !== null && (item._parsedPrice === null || item._parsedPrice < minP)) return false;
        if (maxP !== null && (item._parsedPrice === null || item._parsedPrice > maxP)) return false;
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

    // 1. Filtrar entidades que atendem à Query e ao Preço (Pre-filter comum)
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

    const targetCategory = filters.category;
    const targetSubcat = filters.subcategory;
    const targetType = filters.itemType;
    const targetBook = filters.book;

    for (let i = 0; i < baseCandidates.length; i++) {
      const item = baseCandidates[i];

      // Agregação de Categorias e Subcategorias (respeitando o filtro de Livro ativo)
      if (matchesBook(item, targetBook)) {
        categoryCountMap.set(item.category, (categoryCountMap.get(item.category) || 0) + 1);
        categoryCountMap.set('todas', (categoryCountMap.get('todas') || 0) + 1);

        if (item.subcategory) {
          const subKey = `${item.category}:::${item.subcategory}`;
          subcategoryCountMap.set(subKey, (subcategoryCountMap.get(subKey) || 0) + 1);

          if (item._itemType) {
            const typeKey = `${item.category}:::${item.subcategory}:::${item._itemType}`;
            itemTypeCountMap.set(typeKey, (itemTypeCountMap.get(typeKey) || 0) + 1);
          }
        }
      }

      // Agregação de Livros (respeitando filtros de Categoria, Subcategoria e Tipo ativos)
      const matchesCurrentFacets = 
        (targetCategory === 'todas' || item.category === targetCategory) &&
        (targetSubcat === 'todas' || item.subcategory === targetSubcat) &&
        (targetType === 'todas' || item._itemType === targetType);

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
      getItemTypeCount: (category: string, subcategory: string, type: string) => {
        if (type === 'todas') return subcategoryCountMap.get(`${category}:::${subcategory}`) || 0;
        return itemTypeCountMap.get(`${category}:::${subcategory}:::${type}`) || 0;
      }
    };
  }, [query, filters]);

  const setCategory = (cat: EntityCategory | 'todas') => {
    setFilters(prev => ({ 
      ...prev,
      category: cat, 
      subcategory: 'todas',
      itemType: 'todas',
      minPrice: cat === 'equipamento' ? prev.minPrice : '',
      maxPrice: cat === 'equipamento' ? prev.maxPrice : ''
    }));
  };

  const setSubcategory = (subcat: string | 'todas') => {
    setFilters(prev => ({ 
      ...prev, 
      subcategory: subcat, 
      itemType: 'todas'
    }));
  };

  const setItemType = (type: string | 'todas') => {
    setFilters(prev => ({ 
      ...prev, 
      itemType: type
    }));
  };

  const setBook = (bookId: string | 'todos') => {
    setFilters(prev => ({
      ...prev,
      book: bookId
    }));
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
      maxPrice: ''
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
    setMinPrice,
    setMaxPrice,
    setPriceRange,
    resetFilters,
    dynamicCounts,
    results: filteredResults,
    totalCount: SEARCHABLE_DATABASE.length
  };
}
