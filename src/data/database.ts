import { removeAccents } from '../utils/textUtils';
import canonicalData from '../../data/t20_canonical_database.json';
import auditData from '../../data/consolidation_audit.json';
import type { T20CanonicalEntity, EntityCategory, SpellEntity, MonsterEntity } from '../types/t20_schema';

export const CANONICAL_DATABASE: T20CanonicalEntity[] = canonicalData as unknown as T20CanonicalEntity[];
export const CONSOLIDATION_AUDIT = auditData;

// ---------------------------------------------------------------------------
// Categorias excluidas da interface E da busca (dados permanecem na base
// canonica, mas nao sao navegaveis nem retornam em resultados).
//   - pericia .............. excluida (Perícias)
//   - origem_distincao ..... excluida (Origens & Lore)
//   - ameaca ............... excluida (Ameaças)
//
// Alem disso, 'manobra' e 'regra' sao EXIBIDAS na interface, porem NAO
// CLICAVEIS (ver flag `clickable: false` em CATEGORIES_LIST).
// ---------------------------------------------------------------------------
export const DISABLED_CATEGORIES: EntityCategory[] = ['pericia', 'origem_distincao', 'ameaca'];

export function isCategoryEnabled(cat: EntityCategory): boolean {
  return !DISABLED_CATEGORIES.includes(cat);
}

/** Somente entidades de categorias visiveis na interface/busca. */
export const VISIBLE_DATABASE: T20CanonicalEntity[] = CANONICAL_DATABASE.filter(
  e => isCategoryEnabled(e.category)
);

export type SearchableEntity = T20CanonicalEntity & {
  _searchText: string;
  _parsedPrice: number | null;
  _itemType: string;
  _normalizedBooks: string[];
  _spellCircle?: number;
  _magicRarity?: string;
  _ndRange?: string;
};

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

function buildSearchText(item: any): string {
  const parts: string[] = [
    item.name || '',
    (item.tags || []).join(' '),
    item.subcategory || '',
    item.description || '',
    item.summary || '',
    item.proficiency || '',
    item.type || '',
    item.school || '',
    item.subtype || '',
    item.chapter || '',
    item.regionOrDeity || '',
    item.deity || ''
  ];
  if (item.entries) {
    for (const e of item.entries) {
      if (e.label) parts.push(e.label);
      if (e.description) parts.push(e.description);
    }
  }
  if (item.enhancements) {
    for (const e of item.enhancements) {
      if (e.cost) parts.push(e.cost);
      if (e.description) parts.push(e.description);
    }
  }
  if (item.uses) {
    for (const u of item.uses) {
      if (u.name) parts.push(u.name);
      if (u.description) parts.push(u.description);
    }
  }
  if (item.attacks) {
    for (const a of item.attacks) {
      if (a.name) parts.push(a.name);
      if (a.description) parts.push(a.description);
    }
  }
  if (item.specialAbilities) {
    for (const s of item.specialAbilities) {
      if (s.name) parts.push(s.name);
      if (s.description) parts.push(s.description);
    }
  }
  if (item.auxiliaryNotes) {
    for (const n of item.auxiliaryNotes) {
      parts.push(n);
    }
  }
  return removeAccents(parts.join(' '));
}

/**
 * Normaliza subcategorias com variações ortográficas no banco canônico.
 * Unifica "Magias Universals" e "Magias Universais" → "Magia Universal".
 * NÃO altera o JSON canônico original — apenas a camada de busca indexada.
 */
function normalizeSubcategory(category: string, subcategory: string): string {
  if (category === 'magia') {
    const lower = subcategory.toLowerCase().trim();
    if (lower === 'magias universals' || lower === 'magias universais') {
      return 'Magia Universal';
    }
  }
  return subcategory;
}

export const SEARCHABLE_DATABASE: SearchableEntity[] = VISIBLE_DATABASE.map(item => {
  const anyItem = item as any;
  const rawType = anyItem.proficiency || anyItem.type || anyItem.school || anyItem.subtype || anyItem.actionType || anyItem.effectType || anyItem.subchapter || '';
  const normalizedBooks = (item.sources || []).map(s => s.book).filter(Boolean);
  const normalizedSubcategory = item.subcategory ? normalizeSubcategory(item.category, item.subcategory) : item.subcategory;

  let ndRange = '';
  if (item.category === 'tesouro') {
    const min = anyItem.threatLevelMin ?? 0;
    if (min <= 4) ndRange = 'ND 1-4';
    else if (min <= 10) ndRange = 'ND 5-10';
    else if (min <= 16) ndRange = 'ND 11-16';
    else ndRange = 'ND 17+';
  }
  
  return {
    ...item,
    subcategory: normalizedSubcategory,
    _searchText: buildSearchText(item),
    _parsedPrice: item.category === 'equipamento' ? parseEquipmentPrice(anyItem.tableData?.price) : null,
    _itemType: typeof rawType === 'string' ? rawType.trim() : '',
    _normalizedBooks: normalizedBooks,
    _spellCircle: item.category === 'magia' ? anyItem.circle : undefined,
    _magicRarity: item.category === 'equipamento' ? anyItem.magicRarity : undefined,
    _ndRange: ndRange || undefined
  };
});


export interface CategoryMetadata {
  id: EntityCategory | 'todas';
  label: string;
  iconName: string;
  count: number;
  badgeClass: string;
  /** Quando false, a categoria existe mas fica desabilitada na UI. */
  enabled?: boolean;
  /** Quando false, a categoria é exibida mas NÃO pode ser selecionada. */
  clickable?: boolean;
}

export interface BookMetadata {
  id: string;
  label: string;
  shortLabel: string;
  version: string;
  count: number;
  badgeClass: string;
}

export function formatBookName(bookName?: string): string {
  if (!bookName) return '';
  if (bookName.includes('Jogo do Ano') || bookName.includes('Jogo do ano')) return 'Tormenta20';
  if (bookName.includes('Heróis')) return 'Heróis';
  if (bookName.includes('Ameaças')) return 'Ameaças';
  if (bookName.includes('Atlas')) return 'Atlas';
  return bookName;
}

export const BOOKS_LIST: BookMetadata[] = [
  { 
    id: 'todos', 
    label: 'Todos os Livros', 
    shortLabel: 'Todos os Livros', 
    version: '', 
    count: VISIBLE_DATABASE.length, 
    badgeClass: 'badge-gold' 
  },
  { 
    id: 'Tormenta20 - Jogo do Ano', 
    label: 'Tormenta20', 
    shortLabel: 'Tormenta20', 
    version: '', 
    count: VISIBLE_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Jogo do Ano'))).length, 
    badgeClass: 'badge-gold' 
  },
  { 
    id: 'Heróis de Arton', 
    label: 'Heróis', 
    shortLabel: 'Heróis', 
    version: '', 
    count: VISIBLE_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Heróis'))).length, 
    badgeClass: 'badge-ruby' 
  },
  { 
    id: 'Ameaças de Arton', 
    label: 'Ameaças', 
    shortLabel: 'Ameaças', 
    version: '', 
    count: VISIBLE_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Ameaças'))).length, 
    badgeClass: 'badge-emerald' 
  },
  { 
    id: 'Atlas de Arton', 
    label: 'Atlas', 
    shortLabel: 'Atlas', 
    version: '', 
    count: VISIBLE_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Atlas'))).length, 
    badgeClass: 'badge-parchment' 
  }
];

/**
 * Lista de categorias da interface.
 */
export const CATEGORIES_LIST: CategoryMetadata[] = [
  { id: 'todas', label: 'Tudo', iconName: 'Compass', count: VISIBLE_DATABASE.length, badgeClass: 'badge-gold' },
  { id: 'equipamento', label: 'Equipamentos', iconName: 'Shield', count: CANONICAL_DATABASE.filter(e => e.category === 'equipamento').length, badgeClass: 'badge-gold' },
  { id: 'magia', label: 'Magias', iconName: 'Sparkles', count: CANONICAL_DATABASE.filter(e => e.category === 'magia').length, badgeClass: 'badge-mana' },
  { id: 'tesouro', label: 'Tesouros', iconName: 'Coins', count: CANONICAL_DATABASE.filter(e => e.category === 'tesouro').length, badgeClass: 'badge-gold' },
  { id: 'poder', label: 'Poderes', iconName: 'Zap', count: CANONICAL_DATABASE.filter(e => e.category === 'poder').length, badgeClass: 'badge-ruby' },
  { id: 'condicao', label: 'Condições', iconName: 'Activity', count: CANONICAL_DATABASE.filter(e => e.category === 'condicao').length, badgeClass: 'badge-ruby' },
  { id: 'manobra', label: 'Manobras', iconName: 'Swords', count: CANONICAL_DATABASE.filter(e => e.category === 'manobra').length, badgeClass: 'badge-gold' },
  { id: 'ameaca', label: 'Ameaças', iconName: 'Skull', count: CANONICAL_DATABASE.filter(e => e.category === 'ameaca').length, badgeClass: 'badge-ruby', enabled: false },
  { id: 'regra', label: 'Regras de Mesa', iconName: 'Scroll', count: CANONICAL_DATABASE.filter(e => e.category === 'regra').length, badgeClass: 'badge-parchment' }
];

/** Categorias efetivamente navegáveis (exclui as desabilitadas). */
export const CATEGORIES_ENABLED_LIST: CategoryMetadata[] = CATEGORIES_LIST.filter(
  cat => cat.enabled !== false && (cat.id === 'todas' || isCategoryEnabled(cat.id as EntityCategory))
);

/** Categorias exibidas na UI, porém não selecionáveis. */
export function isCategoryClickable(cat: CategoryMetadata): boolean {
  return cat.clickable !== false;
}

export function getSubcategoriesForCategory(category: EntityCategory | 'todas'): string[] {
  if (category === 'todas') return [];
  const set = new Set<string>();
  SEARCHABLE_DATABASE.filter(e => e.category === category).forEach(e => {
    if (e.subcategory) set.add(e.subcategory);
  });
  return Array.from(set).sort((a, b) => a.localeCompare(b, 'pt-BR'));
}

export function getSubcategoryCount(category: EntityCategory | 'todas', subcategory: string): number {
  if (category === 'todas') {
    return SEARCHABLE_DATABASE.filter(e => e.subcategory === subcategory).length;
  }
  return SEARCHABLE_DATABASE.filter(e => e.category === category && e.subcategory === subcategory).length;
}

export function getItemTypesForCategory(category: EntityCategory | 'todas', subcategory?: string | string[]): string[] {
  if (category === 'todas') return [];
  const set = new Set<string>();
  let items = SEARCHABLE_DATABASE.filter(e => e.category === category);
  if (subcategory && subcategory !== 'todas') {
    if (Array.isArray(subcategory)) {
      if (subcategory.length > 0) {
        items = items.filter(e => e.subcategory && subcategory.includes(e.subcategory));
      }
    } else {
      items = items.filter(e => e.subcategory === subcategory);
    }
  }
  items.forEach(e => {
    const val = e._itemType;
    if (val && typeof val === 'string' && val.trim() !== '') {
      if (Array.isArray(subcategory) ? !subcategory.includes(val) : val !== subcategory) {
        set.add(val.trim());
      }
    }
  });
  return Array.from(set).sort((a, b) => a.localeCompare(b, 'pt-BR'));
}

export function getItemTypeCount(category: EntityCategory | 'todas', subcategory: string | string[] | undefined, itemType: string): number {
  let items = category === 'todas' ? SEARCHABLE_DATABASE : SEARCHABLE_DATABASE.filter(e => e.category === category);
  if (subcategory && subcategory !== 'todas') {
    if (Array.isArray(subcategory)) {
      if (subcategory.length > 0) {
        items = items.filter(e => e.subcategory && subcategory.includes(e.subcategory));
      }
    } else {
      items = items.filter(e => e.subcategory === subcategory);
    }
  }
  return items.filter(e => e._itemType === itemType).length;
}

export function getTotalCountForCategory(category: EntityCategory | 'todas', subcategory?: string | string[]): number {
  if (category === 'todas') return SEARCHABLE_DATABASE.length;
  let items = SEARCHABLE_DATABASE.filter(e => e.category === category);
  if (subcategory && subcategory !== 'todas') {
    if (Array.isArray(subcategory)) {
      if (subcategory.length > 0) {
        items = items.filter(e => e.subcategory && subcategory.includes(e.subcategory));
      }
    } else {
      items = items.filter(e => e.subcategory === subcategory);
    }
  }
  return items.length;
}

export function getSpellSchools(): string[] {
  const set = new Set<string>();
  SEARCHABLE_DATABASE.filter(e => e.category === 'magia').forEach(e => {
    const sp = e as SpellEntity;
    if (sp.school) set.add(sp.school);
  });
  return Array.from(set).sort((a, b) => a.localeCompare(b, 'pt-BR'));
}

export function getSpellCircles(): number[] {
  const set = new Set<number>();
  CANONICAL_DATABASE.filter(e => e.category === 'magia').forEach(e => {
    const sp = e as SpellEntity;
    if (sp.circle) set.add(sp.circle);
  });
  return Array.from(set).sort((a, b) => a - b);
}

export interface SpellCircleInfo {
  circle: number;
  label: string;
  pm: string;
}

export const SPELL_CIRCLES_INFO: SpellCircleInfo[] = [
  { circle: 1, label: '1º Círculo', pm: '1 PM' },
  { circle: 2, label: '2º Círculo', pm: '3 PM' },
  { circle: 3, label: '3º Círculo', pm: '6 PM' },
  { circle: 4, label: '4º Círculo', pm: '10 PM' },
  { circle: 5, label: '5º Círculo', pm: '15 PM' }
];

export function getMagicRarities(): string[] {
  return ['Menor', 'Médio', 'Maior', 'Artefato'];
}

export function getTreasureNDRanges(): string[] {
  return ['ND 1-4', 'ND 5-10', 'ND 11-16', 'ND 17+'];
}

export function getThreatLevels(): string[] {
  const set = new Set<string>();
  CANONICAL_DATABASE.filter(e => e.category === 'ameaca').forEach(e => {
    const mon = e as MonsterEntity;
    if (mon.threatLevel) set.add(mon.threatLevel);
  });
  return Array.from(set);
}

export function getSourceBooks(): string[] {
  const set = new Set<string>();
  CANONICAL_DATABASE.forEach(e => {
    e.sources?.forEach(s => {
      if (s.book) set.add(s.book.split(' - ')[0]);
    });
  });
  return Array.from(set).sort();
}

export function getEntityById(id: string): T20CanonicalEntity | undefined {
  return CANONICAL_DATABASE.find(e => e.id === id);
}
