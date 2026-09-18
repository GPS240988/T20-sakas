import React from 'react';
import { Bookmark, Sparkles, Shield, Swords, Zap, Activity, BookOpen, Skull, MapPin, Scroll, Coins } from 'lucide-react';
import type { T20CanonicalEntity, SpellEntity, EquipmentEntity, MonsterEntity, PowerEntity, TreasureTableEntity } from '../types/t20_schema';
import { formatBookName } from '../data/database';
import { formatDate } from '../utils/formatters';

interface EntityCardProps {
  entity: T20CanonicalEntity;
  onClick: () => void;
  isFavorite: boolean;
  onToggleFavorite: (e: React.MouseEvent) => void;
  dateAdded?: string | Date;
}

const EntityCardComponent: React.FC<EntityCardProps> = ({
  entity,
  onClick,
  isFavorite,
  onToggleFavorite,
  dateAdded
}) => {
  const getCategoryBadge = () => {
    switch (entity.category) {
      case 'magia':
        const spell = entity as SpellEntity;
        return <span className="badge badge-mana"><Sparkles size={12} /> {spell.spellType} {spell.circle}º Círculo</span>;
      case 'equipamento':
        const eq = entity as EquipmentEntity;
        return (
          <div className="card-badge-group">
            <span className="badge badge-gold"><Shield size={12} /> {eq.subcategory}</span>
            {eq.proficiency && <span className="badge badge-parchment">{eq.proficiency}</span>}
          </div>
        );
      case 'tesouro':
        const tr = entity as TreasureTableEntity;
        return <span className="badge badge-gold"><Coins size={12} /> {tr.threatLevelLabel}</span>;
      case 'poder':
        const pow = entity as PowerEntity;
        return <span className="badge badge-ruby"><Zap size={12} /> {pow.subcategory}</span>;
      case 'condicao':
        return <span className="badge badge-ruby"><Activity size={12} /> Condição</span>;
      case 'manobra':
        return <span className="badge badge-gold"><Swords size={12} /> Manobra</span>;
      case 'pericia':
        return <span className="badge badge-emerald"><BookOpen size={12} /> Perícia</span>;
      case 'ameaca':
        const mon = entity as MonsterEntity;
        return <span className="badge badge-ruby"><Skull size={12} /> {mon.threatLevel}</span>;
      case 'origem_distincao':
        return <span className="badge badge-emerald"><MapPin size={12} /> Origem</span>;
      default:
        return <span className="badge badge-parchment"><Scroll size={12} /> Regra</span>;
    }
  };

  const renderQuickStats = () => {
    if (entity.category === 'equipamento') {
      const eq = entity as EquipmentEntity;
      const td = eq.tableData;
      if (!td) return null;
      return (
        <div className="card-quick-stats">
          {td.purpose && <span className="stat-pill"><strong>Tipo:</strong> {td.purpose}</span>}
          {td.damage && <span className="stat-pill"><strong>Dano:</strong> {td.damage} ({td.critical})</span>}
          {td.defenseBonus !== undefined && <span className="stat-pill"><strong>Defesa:</strong> +{td.defenseBonus}</span>}
          {td.armorPenalty !== undefined && td.armorPenalty !== 0 && <span className="stat-pill"><strong>Pen:</strong> {td.armorPenalty}</span>}
          {td.price && <span className="stat-pill stat-gold"><strong>{td.price}</strong></span>}
        </div>
      );
    }

    if (entity.category === 'magia') {
      const sp = entity as SpellEntity;
      return (
        <div className="card-quick-stats">
          <span className="stat-pill"><strong>Escola:</strong> {sp.school}</span>
          <span className="stat-pill"><strong>Execução:</strong> {sp.execution}</span>
          <span className="stat-pill stat-mana"><strong>Custo:</strong> {sp.manaCost} PM</span>
        </div>
      );
    }

    if (entity.category === 'ameaca') {
      const mon = entity as MonsterEntity;
      return (
        <div className="card-quick-stats">
          <span className="stat-pill"><strong>Defesa:</strong> {mon.defense}</span>
          <span className="stat-pill"><strong>PV:</strong> {mon.hp}</span>
          <span className="stat-pill"><strong>Papel:</strong> {mon.role}</span>
        </div>
      );
    }

    return null;
  };

  const primarySource = entity.sources?.[0];

  return (
    <article className="entity-card entity-list-item parchment-card ornate-border" onClick={onClick}>
      <div className="card-header">
        <div className="card-title-group">
          {getCategoryBadge()}
          <h3 className="card-name">{entity.name}</h3>
        </div>
        <button
          className={`favorite-btn ${isFavorite ? 'favorite-active' : ''}`}
          onClick={onToggleFavorite}
          title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
        >
          <Bookmark size={18} fill={isFavorite ? 'currentColor' : 'none'} />
        </button>
      </div>

      {renderQuickStats()}

      <div className="card-footer">
        <div className="card-footer-left">
          {primarySource ? (
            <span className="source-label" title={primarySource.book}>
              📖 {formatBookName(primarySource.book)} • Pág. {primarySource.page}
            </span>
          ) : (
            <span className="source-label">Tormenta20 Canônico</span>
          )}
          {dateAdded && (
            <span className="fav-date" title={`Adicionado aos favoritos em ${typeof dateAdded === 'string' ? formatDate(dateAdded) : dateAdded.toLocaleDateString('pt-BR')}`}>
              <Bookmark size={11} className="text-gold" />
              <span className="fav-date-label">Adicionado aos favoritos em:</span>
              <span className="fav-date-value">{formatDate(dateAdded)}</span>
            </span>
          )}
        </div>
        <span className="click-detail-hint">Ver Detalhes →</span>
      </div>
    </article>
  );
};

export const EntityCard = React.memo(EntityCardComponent, (prev, next) => {
  return (
    prev.entity.id === next.entity.id &&
    prev.isFavorite === next.isFavorite &&
    prev.dateAdded === next.dateAdded
  );
});

