import type { 
  T20CanonicalEntity, 
  SpellEntity, 
  EquipmentEntity, 
  MonsterEntity, 
  ManeuverEntity,
  SkillEntity,
  TreasureTableEntity
} from '../types/t20_schema';
import { formatBookName } from '../data/database';

/**
 * Formata todo o conteúdo de qualquer entidade do compêndio em texto puro
 * bonito e legível para copiar e colar em qualquer aplicativo.
 */
export function formatEntityToClipboardText(entity: T20CanonicalEntity): string {
  const lines: string[] = [];

  // Header
  lines.push(`========================================`);
  lines.push(`${entity.name.toUpperCase()}`);
  lines.push(`Categoria: ${entity.category.toUpperCase()}${entity.subcategory ? ` | ${entity.subcategory}` : ''}`);
  if (entity.proficiency) lines.push(`Proficiência: ${entity.proficiency}`);
  lines.push(`========================================\n`);

  // Category specific specs
  if (entity.category === 'magia') {
    const sp = entity as SpellEntity;
    lines.push(`[ESPECIFICAÇÕES ME CÂNICAS]`);
    lines.push(`• Tipo & Círculo: ${sp.spellType} ${sp.circle}º Círculo (${sp.school})`);
    lines.push(`• Execução: ${sp.execution}`);
    lines.push(`• Alcance: ${sp.range}`);
    if (sp.targetOrArea) lines.push(`• Alvo / Área: ${sp.targetOrArea}`);
    lines.push(`• Duração: ${sp.duration}`);
    if (sp.resistance) lines.push(`• Resistência: ${sp.resistance}`);
    lines.push(`• Custo Base: ${sp.manaCost} PM\n`);
  } else if (entity.category === 'equipamento') {
    const eq = entity as EquipmentEntity;
    const td = eq.tableData;
    if (td) {
      lines.push(`[ESPECIFICAÇÕES]`);
      if (eq.subcategory) lines.push(`• Subcategoria: ${eq.subcategory}`);
      if (eq.proficiency) lines.push(`• Proficiência: ${eq.proficiency}`);
      if (eq.purpose) lines.push(`• Propósito / Uso: ${eq.purpose}`);
      if (td.price) lines.push(`• Preço: ${td.price}`);
      if (td.damage) lines.push(`• Dano: ${td.damage} (Crítico: ${td.critical})`);
      if (td.damageType) lines.push(`• Tipo de Dano: ${td.damageType}`);
      if (td.range && td.range !== '-') lines.push(`• Alcance: ${td.range}`);
      if (td.defenseBonus !== undefined) lines.push(`• Bônus de Defesa: +${td.defenseBonus}`);
      if (td.armorPenalty !== undefined) lines.push(`• Penalidade de Armadura: ${td.armorPenalty}`);
      if (td.space !== undefined) lines.push(`• Espaço: ${td.space}`);
      lines.push('');
    }
  } else if (entity.category === 'manobra') {
    const man = entity as ManeuverEntity;
    lines.push(`[ESPECIFICAÇÕES]`);
    lines.push(`• Tipo de Ação: ${man.actionType}`);
    lines.push(`• Teste Oposto: ${man.opposedTest}\n`);
  } else if (entity.category === 'pericia') {
    const sk = entity as SkillEntity;
    lines.push(`[ESPECIFICAÇÕES]`);
    lines.push(`• Atributo-Chave: ${sk.keyAttribute}`);
    lines.push(`• Somente Treinada: ${sk.onlyTrained ? 'Sim' : 'Não'}`);
    lines.push(`• Penalidade de Armadura: ${sk.armorPenalty ? 'Sim' : 'Não'}\n`);
  } else if (entity.category === 'ameaca') {
    const mon = entity as MonsterEntity;
    lines.push(`[FICHA DA AMEAÇA]`);
    lines.push(`ND ${mon.threatLevel} | ${mon.creatureType} • ${mon.size} • ${mon.role}`);
    lines.push(`Iniciativa: +${mon.initiative} | Percepção: +${mon.perception} | Defesa: ${mon.defense}`);
    lines.push(`PV: ${mon.hp} | PM: ${mon.mp} | Deslocamento: ${mon.speed}`);
    lines.push(`Fort: +${mon.fortitude} | Ref: +${mon.reflexes} | Vont: +${mon.will}`);
    lines.push(`FOR ${mon.attributes.for}, DES ${mon.attributes.des}, CON ${mon.attributes.con}, INT ${mon.attributes.int}, SAB ${mon.attributes.sab}, CAR ${mon.attributes.car}`);
    if (mon.attacks && mon.attacks.length > 0) {
      lines.push(`\nAtaques:`);
      mon.attacks.forEach(a => lines.push(`• ${a.name} (${a.type}): ${a.description}`));
    }
    if (mon.specialAbilities && mon.specialAbilities.length > 0) {
      lines.push(`\nHabilidades Especiais:`);
      mon.specialAbilities.forEach(a => lines.push(`• ${a.name} (${a.type}): ${a.description}`));
    }
    lines.push('');
  } else if (entity.category === 'tesouro') {
    const tr = entity as TreasureTableEntity;
    lines.push(`[TABELA OFICIAL D%]`);
    tr.entries.forEach(e => {
      const range = `${e.d100Min.toString().padStart(2, '0')}-${e.d100Max.toString().padStart(2, '0')}%`;
      lines.push(`• [D% ${range}] ${e.label}${e.description ? ` - ${e.description}` : ''}`);
    });
    lines.push('');
  }

  // Description
  if (entity.description) {
    lines.push(`[DESCRIÇÃO & REGRAS]`);
    lines.push(entity.description);
    lines.push('');
  }

  // Spell Enhancements
  if (entity.category === 'magia') {
    const sp = entity as SpellEntity;
    if (sp.enhancements && sp.enhancements.length > 0) {
      lines.push(`[APRIMORAMENTOS DE MANA]`);
      sp.enhancements.forEach(enh => lines.push(`• ${enh.cost}: ${enh.description}`));
      lines.push('');
    }
  }

  // Sources
  if (entity.sources && entity.sources.length > 0) {
    lines.push(`[FONTE BIBLIOGRÁFICA OFICIAL]`);
    entity.sources.forEach(src => lines.push(`• ${formatBookName(src.book)}, pág. ${src.page}`));
  }

  return lines.join('\n');
}
