/**
 * Schemas Canônicos e Contratos de Tipagem de Tormenta20 (T20 Sakas)
 * 
 * Este arquivo define as estruturas de dados para todas as entidades do jogo,
 * divididas por Categoria, Subcategoria, Proficiência e Propósito, com suporte
 * a filtros multifacetados extensíveis para todas as categorias.
 */

export type SourceBook = 
  | 'Tormenta20 - Jogo do Ano'
  | 'Ameaças de Arton'
  | 'Atlas de Arton'
  | 'Heróis de Arton'
  | 'Errata / FAQ Oficial';

export interface SourceReference {
  book: SourceBook;
  page: number;
  section?: string;
  version?: string;
  notes?: string;
}

export type EntityCategory = 
  | 'equipamento'
  | 'tesouro'
  | 'magia'
  | 'poder'
  | 'ameaca'
  | 'condicao'
  | 'manobra'
  | 'pericia'
  | 'regra'
  | 'origem_distincao'
  | 'lore';

export interface BaseEntity {
  id: string; // Ex: 'arma-adaga', 'tesouro-tabela-nd-5', 'magia-bola-de-fogo'
  name: string; // Nome canônico em PT-BR
  category: EntityCategory;
  subcategory: string; // Ex: 'Armas', 'Armaduras & Escudos', 'Itens Gerais', 'Magias Arcanas'
  subtype?: string; // Ex: 'Arcanista', 'Paladino', etc.
  proficiency?: string; // Ex: 'Armas Simples', 'Armas Marciais', 'Armaduras Leves'
  purpose?: string; // Ex: 'Corpo a Corpo', 'Disparo', 'Alquimias & Preparados'
  summary?: string;
  description: string;
  sources: SourceReference[];
  tags: string[];
  relatedIds?: string[];
  auxiliaryNotes?: string[];
}

// ============================================================================
// 1. EQUIPAMENTO (Armas, Munições, Armaduras, Escudos, Itens Gerais, Superiores)
// ============================================================================

export interface EquipmentTableData {
  price?: string;
  damage?: string;
  critical?: string;
  damageType?: string;
  range?: string;
  defenseBonus?: number;
  armorPenalty?: number;
  space?: number | string;
  proficiency?: string;
  purpose?: string;
  wielding?: string;
  material?: string;
  improvements?: string[];
}

export interface EquipmentEntity extends BaseEntity {
  category: 'equipamento';
  subcategory: 
    | 'Armas'
    | 'Munições'
    | 'Armaduras & Escudos'
    | 'Itens Gerais'
    | 'Itens Superiores'
    | 'Capangas'
    | 'Veículos'
    | 'Itens Mágicos'
    | string;
  proficiency?: 
    | 'Armas Simples'
    | 'Armas Marciais'
    | 'Armas Exóticas'
    | 'Armas de Fogo'
    | 'Munições'
    | 'Armaduras Leves'
    | 'Armaduras Pesadas'
    | 'Escudos'
    | 'Itens Gerais'
    | 'Melhorias'
    | 'Materiais Especiais'
    | 'Capangas'
    | 'Veículos'
    | string;
  purpose?: 
    | 'Corpo a Corpo / Leve'
    | 'Corpo a Corpo / Uma Mão'
    | 'Corpo a Corpo / Duas Mãos'
    | 'Corpo a Corpo / Haste'
    | 'Disparo / Uma Mão'
    | 'Disparo / Duas Mãos'
    | 'Arremesso / Uma Mão'
    | 'Armadura Leve'
    | 'Armadura Pesada'
    | 'Escudo'
    | 'Equipamento de Aventura'
    | 'Alquimias & Preparados'
    | 'Itens Esotéricos'
    | 'Ferramentas & Aventura'
    | 'Melhoria de Arma'
    | 'Melhoria de Armadura / Escudo'
    | 'Material Especial'
    | 'Capanga / Aliado'
    | 'Veículo Terrestre'
    | 'Veículo Aéreo'
    | 'Veículo Aquático'
    | string;
  tableData?: EquipmentTableData;
  isMagicItem?: boolean;
  magicRarity?: 'Menor' | 'Médio' | 'Maior' | 'Artefato';
}

// ============================================================================
// 2. TESOUROS & TABELAS D% (Rolagens de Recompensa por ND)
// ============================================================================

export interface TreasureRollEntry {
  d100Min: number;
  d100Max: number;
  label: string;
  moneyFormula?: string;
  itemCategory?: 'Nenhum' | 'Comum' | 'Superior' | 'Mágico Menor' | 'Mágico Médio' | 'Mágico Maior';
  itemRollCount?: string;
  itemRollTableRef?: string;
  description: string;
  entryType?: 'money' | 'item';
}

export interface TreasureTableEntity extends BaseEntity {
  category: 'tesouro';
  subcategory: 'Tabela de Tesouro por ND' | 'Riqueza/Equipamentos/Itens/Superiores' | 'Itens Mágicos';
  threatLevelMin: number;
  threatLevelMax: number;
  threatLevelLabel: string;
  averageMoney?: string;
  entries: TreasureRollEntry[];
}

// ============================================================================
// 3. MAGIAS (1º ao 5º Círculo, Arcanas, Divinas, Universais)
// ============================================================================

export interface SpellEnhancement {
  cost: string;
  description: string;
}

export interface SpellEntity extends BaseEntity {
  category: 'magia';
  subcategory: 'Magias Arcanas' | 'Magias Divinas' | 'Magias Universais' | 'Magias de Ameaças';
  spellType: 'Arcana' | 'Divina' | 'Universal';
  circle: 1 | 2 | 3 | 4 | 5;
  school: 'Abjuração' | 'Adivinhação' | 'Convocação' | 'Encantamento' | 'Evocação' | 'Ilusão' | 'Necromancia' | 'Transmutação';
  execution: string;
  range: string;
  targetOrArea: string;
  duration: string;
  resistance?: string;
  manaCost: number;
  enhancements?: SpellEnhancement[];
}

// ============================================================================
// 4. PODERES & DISTINÇÕES
// ============================================================================

export interface PowerEntity extends BaseEntity {
  category: 'poder';
  subcategory: 
    | 'Poderes de Combate'
    | 'Poderes de Destino'
    | 'Poderes de Magia'
    | 'Poderes da Tormenta'
    | 'Poderes Concedidos'
    | 'Poderes de Classe'
    | 'Poderes de Raça'
    | 'Poderes de Grupo'
    | 'Distinções de Arton';
  powerType: 'Combate' | 'Destino' | 'Magia' | 'Tormenta' | 'Concedido' | 'Classe' | 'Raça' | 'Grupo' | 'Distinção';
  requirements?: string[];
  cost?: string;
  deity?: string;
}

// ============================================================================
// 5. AMEAÇAS & MONSTROS
// ============================================================================

export interface MonsterAction {
  name: string;
  type: string;
  description: string;
}

export interface MonsterEntity extends BaseEntity {
  category: 'ameaca';
  subcategory: 'Ameaça Solo' | 'Ameaça Lacaio' | 'Ameaça Especial' | 'Ameaça Chefe' | 'Perigo Complexo';
  threatLevel: string;
  threatLevelNumeric: number;
  creatureType: string;
  size: 'Minúsculo' | 'Pequeno' | 'Médio' | 'Grande' | 'Enorme' | 'Colossal';
  role: 'Lacaio' | 'Solo' | 'Especial' | 'Chefe';
  initiative: number;
  perception: number;
  defense: number;
  fortitude: number;
  reflexes: number;
  will: number;
  hp: number;
  mp: number;
  speed: string;
  attacks: MonsterAction[];
  specialAbilities: MonsterAction[];
  attributes: {
    for: number;
    des: number;
    con: number;
    int: number;
    sab: number;
    car: number;
  };
}

// ============================================================================
// 6. CONDIÇÕES, MANOBRAS, PERÍCIAS E REGRAS
// ============================================================================

export interface ConditionEntity extends BaseEntity {
  category: 'condicao';
  subcategory: 'Condições Físicas' | 'Condições Mentais' | 'Condições de Sentidos' | 'Condições de Saúde' | 'Condições Metabólicas';
  effectType?: 'Mental' | 'Medo' | 'Movimento' | 'Sentidos' | 'Metabólica' | 'Mágica';
  isCumulative: boolean;
}

export interface ManeuverEntity extends BaseEntity {
  category: 'manobra';
  subcategory: 'Manobras de Combate';
  actionType: 'Ação Padrão' | 'Ação de Movimento' | 'Ação Livre' | 'Reação';
  opposedTest: string;
  resultingConditionIds?: string[];
}

export interface SkillEntity extends BaseEntity {
  category: 'pericia';
  subcategory: 'Perícias Gerais';
  keyAttribute: 'FOR' | 'DES' | 'CON' | 'INT' | 'SAB' | 'CAR';
  onlyTrained: boolean;
  armorPenalty: boolean;
  uses?: Array<{
    name: string;
    dcOrOpposed: string;
    description: string;
  }>;
}

export interface RuleEntity extends BaseEntity {
  category: 'regra';
  subcategory: 'Combate' | 'Ações' | 'Descanso' | 'Regras Gerais' | 'Perigos';
  chapter: string;
}

export interface OriginDistinctionEntity extends BaseEntity {
  category: 'origem_distincao';
  subcategory: 'Origens Regionais' | 'Distinções de Heróis' | 'Organizações';
  regionOrDeity?: string;
  benefits?: string[];
  admissionRequirements?: string[];
}

export type T20CanonicalEntity = 
  | EquipmentEntity
  | TreasureTableEntity
  | SpellEntity
  | PowerEntity
  | MonsterEntity
  | ConditionEntity
  | ManeuverEntity
  | SkillEntity
  | RuleEntity
  | OriginDistinctionEntity
  | BaseEntity;
