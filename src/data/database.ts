import canonicalData from '../../data/t20_canonical_database.json';
import auditData from '../../data/consolidation_audit.json';
import type { T20CanonicalEntity, EntityCategory, SpellEntity, MonsterEntity } from '../types/t20_schema';

export const CANONICAL_DATABASE: T20CanonicalEntity[] = canonicalData as unknown as T20CanonicalEntity[];
export const CONSOLIDATION_AUDIT = auditData;

export interface CategoryMetadata {
  id: EntityCategory | 'todas';
  label: string;
  iconName: string;
  count: number;
  badgeClass: string;
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
    count: CANONICAL_DATABASE.length, 
    badgeClass: 'badge-gold' 
  },
  { 
    id: 'Tormenta20 - Jogo do Ano', 
    label: 'Tormenta20', 
    shortLabel: 'Tormenta20', 
    version: '', 
    count: CANONICAL_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Jogo do Ano'))).length, 
    badgeClass: 'badge-gold' 
  },
  { 
    id: 'Heróis de Arton', 
    label: 'Heróis', 
    shortLabel: 'Heróis', 
    version: '', 
    count: CANONICAL_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Heróis'))).length, 
    badgeClass: 'badge-ruby' 
  },
  { 
    id: 'Ameaças de Arton', 
    label: 'Ameaças', 
    shortLabel: 'Ameaças', 
    version: '', 
    count: CANONICAL_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Ameaças'))).length, 
    badgeClass: 'badge-emerald' 
  },
  { 
    id: 'Atlas de Arton', 
    label: 'Atlas', 
    shortLabel: 'Atlas', 
    version: '', 
    count: CANONICAL_DATABASE.filter(e => e.sources?.some(s => s.book.includes('Atlas'))).length, 
    badgeClass: 'badge-parchment' 
  }
];

export const CATEGORIES_LIST: CategoryMetadata[] = [
  { id: 'todas', label: 'Tudo', iconName: 'Compass', count: CANONICAL_DATABASE.length, badgeClass: 'badge-gold' },
  { id: 'equipamento', label: 'Equipamentos', iconName: 'Shield', count: CANONICAL_DATABASE.filter(e => e.category === 'equipamento').length, badgeClass: 'badge-gold' },
  { id: 'magia', label: 'Magias', iconName: 'Sparkles', count: CANONICAL_DATABASE.filter(e => e.category === 'magia').length, badgeClass: 'badge-mana' },
  { id: 'tesouro', label: 'Tesouros', iconName: 'Coins', count: CANONICAL_DATABASE.filter(e => e.category === 'tesouro').length, badgeClass: 'badge-gold' },
  { id: 'poder', label: 'Poderes', iconName: 'Zap', count: CANONICAL_DATABASE.filter(e => e.category === 'poder').length, badgeClass: 'badge-ruby' },
  { id: 'condicao', label: 'Condições', iconName: 'Activity', count: CANONICAL_DATABASE.filter(e => e.category === 'condicao').length, badgeClass: 'badge-ruby' },
  { id: 'manobra', label: 'Manobras', iconName: 'Swords', count: CANONICAL_DATABASE.filter(e => e.category === 'manobra').length, badgeClass: 'badge-gold' },
  { id: 'pericia', label: 'Perícias', iconName: 'BookOpen', count: CANONICAL_DATABASE.filter(e => e.category === 'pericia').length, badgeClass: 'badge-emerald' },
  { id: 'ameaca', label: 'Ameaças', iconName: 'Skull', count: CANONICAL_DATABASE.filter(e => e.category === 'ameaca').length, badgeClass: 'badge-ruby' },
  { id: 'origem_distincao', label: 'Origens & Lore', iconName: 'MapPin', count: CANONICAL_DATABASE.filter(e => e.category === 'origem_distincao').length, badgeClass: 'badge-emerald' },
  { id: 'regra', label: 'Regras de Mesa', iconName: 'Scroll', count: CANONICAL_DATABASE.filter(e => e.category === 'regra').length, badgeClass: 'badge-parchment' }
];

export function getSubcategoriesForCategory(category: EntityCategory | 'todas'): string[] {
  if (category === 'todas') return [];
  const set = new Set<string>();
  CANONICAL_DATABASE.filter(e => e.category === category).forEach(e => {
    if (e.subcategory) set.add(e.subcategory);
  });
  return Array.from(set).sort();
}

export function getSubcategoryCount(category: EntityCategory | 'todas', subcategory: string): number {
  if (category === 'todas') {
    return CANONICAL_DATABASE.filter(e => e.subcategory === subcategory).length;
  }
  return CANONICAL_DATABASE.filter(e => e.category === category && e.subcategory === subcategory).length;
}

export function getItemTypesForCategory(category: EntityCategory | 'todas', subcategory?: string): string[] {
  if (category === 'todas') return [];
  const set = new Set<string>();
  let items = CANONICAL_DATABASE.filter(e => e.category === category);
  if (subcategory && subcategory !== 'todas') {
    items = items.filter(e => e.subcategory === subcategory);
  }
  items.forEach(e => {
    const item = e as any;
    // For Equipments: proficiency/subtype holds the classification (Armas Simples, Armaduras Leves, Vestuário, etc.)
    // For Spells: school
    // For Powers: powerType or subtype
    const val = item.proficiency || item.type || item.school || item.subtype;
    if (val && val !== subcategory && typeof val === 'string' && val.trim() !== '') {
      set.add(val.trim());
    }
  });
  return Array.from(set).sort();
}

export function getItemTypeCount(category: EntityCategory | 'todas', subcategory: string | undefined, itemType: string): number {
  let items = category === 'todas' ? CANONICAL_DATABASE : CANONICAL_DATABASE.filter(e => e.category === category);
  if (subcategory && subcategory !== 'todas') {
    items = items.filter(e => e.subcategory === subcategory);
  }
  return items.filter(e => {
    const item = e as any;
    const val = item.proficiency || item.type || item.school || item.subtype;
    return val === itemType;
  }).length;
}

export function getTotalCountForCategory(category: EntityCategory | 'todas', subcategory?: string): number {
  if (category === 'todas') return CANONICAL_DATABASE.length;
  let items = CANONICAL_DATABASE.filter(e => e.category === category);
  if (subcategory && subcategory !== 'todas') {
    items = items.filter(e => e.subcategory === subcategory);
  }
  return items.length;
}

export function getSpellSchools(): string[] {
  const set = new Set<string>();
  CANONICAL_DATABASE.filter(e => e.category === 'magia').forEach(e => {
    const sp = e as SpellEntity;
    if (sp.school) set.add(sp.school);
  });
  return Array.from(set).sort();
}

export function getSpellCircles(): number[] {
  const set = new Set<number>();
  CANONICAL_DATABASE.filter(e => e.category === 'magia').forEach(e => {
    const sp = e as SpellEntity;
    if (sp.circle) set.add(sp.circle);
  });
  return Array.from(set).sort((a, b) => a - b);
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
