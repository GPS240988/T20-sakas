import { useState, useMemo } from 'react';
import { VISIBLE_DATABASE } from '../data/database';
import type { EntityCategory } from '../types/t20_schema';

export interface SearchFilters {
  category: EntityCategory | 'todas';
  subcategory: string | 'todas';
  itemType: string | 'todas';
  book: string | 'todos';
  minPrice?: number | '';
  maxPrice?: number | '';
}

export function parseEquipmentPrice(priceStr?: string): number | null {
  if (!priceStr) return null;
  const match = priceStr.match(/(\d[\d\.,]*)/);
  if (!match) return null;
  let raw = match[1];
  if (raw.includes('.') && raw.includes(',')) {
    raw = raw.replace(/\./g, '').replace(',', '.');
  } else if (raw.includes('.')) {
    const parts = raw.split('.');
    if (parts[parts.length - 1].length === 3) {
      raw = parts.join('');
    }
  } else if (raw.includes(',')) {
    raw = raw.replace(',', '.');
  }
  const val = parseFloat(raw);
  return isNaN(val) ? null : val;
}

function checkItemMatchesQuery(item: any, q: string): boolean {
  if (!q) return true;
  
  if (item.name?.toLowerCase().includes(q)) return true;
  if (item.tags?.some((t: string) => t.toLowerCase().includes(q))) return true;
  if (item.subcategory?.toLowerCase().includes(q)) return true;
  if (item.description?.toLowerCase().includes(q)) return true;
  if (item.summary?.toLowerCase().includes(q)) return true;
  
  const typeVal = item.proficiency || item.type || item.school || item.subtype || item.chapter || item.regionOrDeity || item.deity;
  if (typeVal && String(typeVal).toLowerCase().includes(q)) return true;
  
  if (item.entries?.some((e: any) => 
    (e.label && String(e.label).toLowerCase().includes(q)) || 
    (e.description && String(e.description).toLowerCase().includes(q))
  )) return true;

  if (item.enhancements?.some((e: any) =>
    (e.cost && String(e.cost).toLowerCase().includes(q)) ||
    (e.description && String(e.description).toLowerCase().includes(q))
  )) return true;

  if (item.uses?.some((u: any) =>
    (u.name && String(u.name).toLowerCase().includes(q)) ||
    (u.description && String(u.description).toLowerCase().includes(q))
  )) return true;

  if (item.attacks?.some((a: any) =>
    (a.name && String(a.name).toLowerCase().includes(q)) ||
    (a.description && String(a.description).toLowerCase().includes(q))
  )) return true;

  if (item.specialAbilities?.some((s: any) =>
    (s.name && String(s.name).toLowerCase().includes(q)) ||
    (s.description && String(s.description).toLowerCase().includes(q))
  )) return true;

  if (item.auxiliaryNotes?.some((n: string) => n.toLowerCase().includes(q))) return true;

  return false;
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
    const q = query.trim().toLowerCase();
    
    return VISIBLE_DATABASE.filter(item => {
      // 1. Filtro de Livro Oficial
      if (filters.book !== 'todos') {
        const matchesBook = item.sources?.some(s => {
          if (filters.book.includes('Jogo do Ano')) return s.book.includes('Jogo do Ano');
          if (filters.book.includes('Heróis')) return s.book.includes('Heróis');
          if (filters.book.includes('Ameaças')) return s.book.includes('Ameaças');
          if (filters.book.includes('Atlas')) return s.book.includes('Atlas');
          return s.book === filters.book;
        });
        if (!matchesBook) {
          return false;
        }
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
      if (filters.itemType !== 'todas') {
        const anyItem = item as any;
        const val = anyItem.proficiency || anyItem.type || anyItem.school || anyItem.subtype;
        if (val !== filters.itemType) {
          return false;
        }
      }

      // 4.5. Filtro de Faixa de Valor (Exclusivo para Equipamentos)
      if (item.category === 'equipamento' && (filters.category === 'equipamento' || filters.category === 'todas')) {
        const price = parseEquipmentPrice((item as any).tableData?.price);
        if (filters.minPrice !== undefined && filters.minPrice !== '') {
          if (price === null || price < Number(filters.minPrice)) return false;
        }
        if (filters.maxPrice !== undefined && filters.maxPrice !== '') {
          if (price === null || price > Number(filters.maxPrice)) return false;
        }
      }

      // 5. Se não houver texto na busca, retorna aprovado pelos filtros
      if (!q) return true;

      // 6. Busca Universal Instantânea (incluindo texto interno dos modals)
      return checkItemMatchesQuery(item, q);
    });
  }, [query, filters]);

  // Contadores dinâmicos para a interface em tempo real
  const dynamicCounts = useMemo(() => {
    const q = query.trim().toLowerCase();

    const matchesBook = (item: any, bookId: string) => {
      if (bookId === 'todos') return true;
      return item.sources?.some((s: any) => {
        if (bookId.includes('Jogo do Ano')) return s.book.includes('Jogo do Ano');
        if (bookId.includes('Heróis')) return s.book.includes('Heróis');
        if (bookId.includes('Ameaças')) return s.book.includes('Ameaças');
        if (bookId.includes('Atlas')) return s.book.includes('Atlas');
        return s.book === bookId;
      });
    };

    const matchesQuery = (item: any) => {
      return checkItemMatchesQuery(item, q);
    };

    const matchesPrice = (item: any) => {
      if (item.category !== 'equipamento') return true;
      const price = parseEquipmentPrice((item as any).tableData?.price);
      if (filters.minPrice !== undefined && filters.minPrice !== '') {
        if (price === null || price < Number(filters.minPrice)) return false;
      }
      if (filters.maxPrice !== undefined && filters.maxPrice !== '') {
        if (price === null || price > Number(filters.maxPrice)) return false;
      }
      return true;
    };

    const getBookCount = (bookId: string) => {
      return VISIBLE_DATABASE.filter(item => {
        if (!matchesBook(item, bookId)) return false;
        if (filters.category !== 'todas' && item.category !== filters.category) return false;
        if (filters.subcategory !== 'todas' && item.subcategory !== filters.subcategory) return false;
        if (filters.itemType !== 'todas') {
          const anyItem = item as any;
          const val = anyItem.proficiency || anyItem.type || anyItem.school || anyItem.subtype;
          if (val !== filters.itemType) return false;
        }
        if (!matchesPrice(item)) return false;
        return matchesQuery(item);
      }).length;
    };

    const getCategoryCount = (catId: string) => {
      return VISIBLE_DATABASE.filter(item => {
        if (!matchesBook(item, filters.book)) return false;
        if (catId !== 'todas' && item.category !== catId) return false;
        if (!matchesPrice(item)) return false;
        return matchesQuery(item);
      }).length;
    };

    const getSubcategoryCount = (category: string, subcat: string) => {
      return VISIBLE_DATABASE.filter(item => {
        if (!matchesBook(item, filters.book)) return false;
        if (category !== 'todas' && item.category !== category) return false;
        if (subcat !== 'todas' && item.subcategory !== subcat) return false;
        if (!matchesPrice(item)) return false;
        return matchesQuery(item);
      }).length;
    };

    const getItemTypeCount = (category: string, subcategory: string, type: string) => {
      return VISIBLE_DATABASE.filter(item => {
        if (!matchesBook(item, filters.book)) return false;
        if (category !== 'todas' && item.category !== category) return false;
        if (subcategory !== 'todas' && item.subcategory !== subcategory) return false;
        if (type !== 'todas') {
          const anyItem = item as any;
          const val = anyItem.proficiency || anyItem.type || anyItem.school || anyItem.subtype;
          if (val !== type) return false;
        }
        if (!matchesPrice(item)) return false;
        return matchesQuery(item);
      }).length;
    };

    return {
      getBookCount,
      getCategoryCount,
      getSubcategoryCount,
      getItemTypeCount
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
    totalCount: VISIBLE_DATABASE.length
  };
}
