import React, { useState } from 'react';
import { X, Bookmark, ExternalLink, Copy, Check } from 'lucide-react';
import type { 
  T20CanonicalEntity, 
  SpellEntity, 
  EquipmentEntity, 
  MonsterEntity, 
  ManeuverEntity,
  SkillEntity,
  TreasureTableEntity
} from '../types/t20_schema';
import { getEntityById, formatBookName } from '../data/database';
import { formatEntityToClipboardText } from '../utils/clipboardFormatter';

interface EntityModalProps {
  entity: T20CanonicalEntity | null;
  onClose: () => void;
  isFavorite: boolean;
  onToggleFavorite: () => void;
  onSelectRelatedEntity: (entity: T20CanonicalEntity) => void;
}

export const EntityModal: React.FC<EntityModalProps> = ({
  entity,
  onClose,
  isFavorite,
  onToggleFavorite,
  onSelectRelatedEntity
}) => {
  const [copied, setCopied] = useState(false);

  if (!entity) return null;

  const handleCopyContent = () => {
    const text = formatEntityToClipboardText(entity);
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderSpecificDetails = () => {
    // 1. Magia
    if (entity.category === 'magia') {
      const sp = entity as SpellEntity;
      return (
        <div className="modal-specs-grid">
          <div className="spec-item"><span className="spec-label">Tipo & Círculo:</span> <span className="spec-val">{sp.spellType} {sp.circle}º Círculo ({sp.school})</span></div>
          <div className="spec-item"><span className="spec-label">Execução:</span> <span className="spec-val">{sp.execution}</span></div>
          <div className="spec-item"><span className="spec-label">Alcance:</span> <span className="spec-val">{sp.range}</span></div>
          {sp.targetOrArea && <div className="spec-item"><span className="spec-label">Alvo / Área:</span> <span className="spec-val">{sp.targetOrArea}</span></div>}
          <div className="spec-item"><span className="spec-label">Duração:</span> <span className="spec-val">{sp.duration}</span></div>
          {sp.resistance && <div className="spec-item"><span className="spec-label">Resistência:</span> <span className="spec-val">{sp.resistance}</span></div>}
          <div className="spec-item"><span className="spec-label">Custo Base:</span> <span className="spec-val highlight-mana">{sp.manaCost} PM</span></div>
        </div>
      );
    }

    // 2. Equipamento
    if (entity.category === 'equipamento') {
      const eq = entity as EquipmentEntity;
      const td = eq.tableData;
      if (!td) return null;
      return (
        <div className="modal-specs-grid">
          {eq.subcategory && <div className="spec-item"><span className="spec-label">Subcategoria:</span> <span className="spec-val">{eq.subcategory}</span></div>}
          {eq.proficiency && <div className="spec-item"><span className="spec-label">Proficiência:</span> <span className="spec-val">{eq.proficiency}</span></div>}
          {eq.purpose && <div className="spec-item"><span className="spec-label">Propósito / Uso:</span> <span className="spec-val">{eq.purpose}</span></div>}
          {td.price && <div className="spec-item"><span className="spec-label">Preço:</span> <span className="spec-val highlight-gold">{td.price}</span></div>}
          {td.damage && <div className="spec-item"><span className="spec-label">Dano:</span> <span className="spec-val">{td.damage} (Crítico: {td.critical})</span></div>}
          {td.damageType && <div className="spec-item"><span className="spec-label">Tipo de Dano:</span> <span className="spec-val">{td.damageType}</span></div>}
          {td.range && td.range !== '-' && <div className="spec-item"><span className="spec-label">Alcance:</span> <span className="spec-val">{td.range}</span></div>}
          {td.defenseBonus !== undefined && <div className="spec-item"><span className="spec-label">Bônus de Defesa:</span> <span className="spec-val">+{td.defenseBonus}</span></div>}
          {td.armorPenalty !== undefined && <div className="spec-item"><span className="spec-label">Penalidade de Armadura:</span> <span className="spec-val">{td.armorPenalty}</span></div>}
          {td.space !== undefined && <div className="spec-item"><span className="spec-label">Espaço:</span> <span className="spec-val">{td.space}</span></div>}
        </div>
      );
    }

    // 3. Manobra
    if (entity.category === 'manobra') {
      const man = entity as ManeuverEntity;
      return (
        <div className="modal-specs-grid">
          <div className="spec-item"><span className="spec-label">Tipo de Ação:</span> <span className="spec-val">{man.actionType}</span></div>
          <div className="spec-item"><span className="spec-label">Teste Oposto:</span> <span className="spec-val">{man.opposedTest}</span></div>
        </div>
      );
    }

    // 4. Perícia
    if (entity.category === 'pericia') {
      const sk = entity as SkillEntity;
      return (
        <div className="modal-specs-grid">
          <div className="spec-item"><span className="spec-label">Atributo-Chave:</span> <span className="spec-val">{sk.keyAttribute}</span></div>
          <div className="spec-item"><span className="spec-label">Somente Treinada:</span> <span className="spec-val">{sk.onlyTrained ? 'Sim' : 'Não'}</span></div>
          <div className="spec-item"><span className="spec-label">Penalidade de Armadura:</span> <span className="spec-val">{sk.armorPenalty ? 'Sim' : 'Não'}</span></div>
        </div>
      );
    }

    // 5. Ameaça
    if (entity.category === 'ameaca') {
      const mon = entity as MonsterEntity;
      return (
        <div className="monster-statblock-modal">
          <div className="monster-header-row">
            <span className="monster-nd">{mon.threatLevel}</span>
            <span className="monster-type">{mon.creatureType} • {mon.size} • {mon.role}</span>
          </div>
          <div className="monster-combat-stats">
            <div><strong>Iniciativa:</strong> +{mon.initiative}</div>
            <div><strong>Percepção:</strong> +{mon.perception}</div>
            <div><strong>Defesa:</strong> {mon.defense}</div>
            <div><strong>PV:</strong> {mon.hp}</div>
            <div><strong>PM:</strong> {mon.mp}</div>
            <div><strong>Deslocamento:</strong> {mon.speed}</div>
          </div>
          <div className="monster-saves">
            <span><strong>Fort:</strong> +{mon.fortitude}</span>
            <span><strong>Ref:</strong> +{mon.reflexes}</span>
            <span><strong>Vont:</strong> +{mon.will}</span>
          </div>
          <div className="monster-attributes">
            <span><strong>FOR:</strong> {mon.attributes.for}</span>
            <span><strong>DES:</strong> {mon.attributes.des}</span>
            <span><strong>CON:</strong> {mon.attributes.con}</span>
            <span><strong>INT:</strong> {mon.attributes.int}</span>
            <span><strong>SAB:</strong> {mon.attributes.sab}</span>
            <span><strong>CAR:</strong> {mon.attributes.car}</span>
          </div>
          {mon.attacks && mon.attacks.length > 0 && (
            <div className="monster-section">
              <h4>Ataques:</h4>
              {mon.attacks.map((atk, idx) => (
                <div key={idx} className="monster-action-row">
                  <strong>{atk.name} ({atk.type}):</strong> {atk.description}
                </div>
              ))}
            </div>
          )}
          {mon.specialAbilities && mon.specialAbilities.length > 0 && (
            <div className="monster-section">
              <h4>Habilidades Especiais:</h4>
              {mon.specialAbilities.map((ab, idx) => (
                <div key={idx} className="monster-action-row">
                  <strong>{ab.name} ({ab.type}):</strong> {ab.description}
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }

    // 6. Tesouros
    if (entity.category === 'tesouro') {
      const tr = entity as TreasureTableEntity;
      const moneyEntries = tr.entries.filter(e => e.entryType === 'money');
      const itemEntries = tr.entries.filter(e => e.entryType === 'item');

      if (moneyEntries.length > 0 && itemEntries.length > 0) {
        return (
          <div className="treasure-table-view">
            <div className="treasure-tables-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
              <div className="treasure-section-box">
                <h4 style={{ color: 'var(--accent-gold)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem', fontSize: '0.92rem', fontWeight: '700' }}>
                  💰 Rolagem de Dinheiro (D%)
                </h4>
                <div className="treasure-table-wrapper">
                  <table className="treasure-table">
                    <thead>
                      <tr>
                        <th>D% (01-100)</th>
                        <th>Moedas / Riquezas</th>
                      </tr>
                    </thead>
                    <tbody>
                      {moneyEntries.map((entry, idx) => (
                        <tr key={idx}>
                          <td className="d100-cell">{entry.d100Min.toString().padStart(2, '0')}-{entry.d100Max.toString().padStart(2, '0')}</td>
                          <td>{entry.label.replace(/^Dinheiro \(\d{2}-\d{2}%\):\s*/, '')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="treasure-section-box">
                <h4 style={{ color: 'var(--accent-ruby)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem', fontSize: '0.92rem', fontWeight: '700' }}>
                  🎒 Rolagem de Itens (D%)
                </h4>
                <div className="treasure-table-wrapper">
                  <table className="treasure-table">
                    <thead>
                      <tr>
                        <th>D% (01-100)</th>
                        <th>Equipamentos / Itens Mágicos</th>
                      </tr>
                    </thead>
                    <tbody>
                      {itemEntries.map((entry, idx) => (
                        <tr key={idx}>
                          <td className="d100-cell">{entry.d100Min.toString().padStart(2, '0')}-{entry.d100Max.toString().padStart(2, '0')}</td>
                          <td>{entry.label.replace(/^Item \(\d{2}-\d{2}%\):\s*/, '')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        );
      }

      return (
        <div className="treasure-table-view">
          <h4 style={{ marginBottom: '0.6rem', color: 'var(--text-primary)', fontWeight: '700' }}>Faixas de Sorteio no Dado Percentual (D%):</h4>
          <div className="treasure-table-wrapper">
            <table className="treasure-table">
              <thead>
                <tr>
                  <th style={{ width: '100px' }}>D% (01-100)</th>
                  <th style={{ minWidth: '180px' }}>Item / Resultado</th>
                  <th>Efeito & Regra Mecânica Completa</th>
                </tr>
              </thead>
              <tbody>
                {tr.entries.map((entry, idx) => (
                  <tr key={idx}>
                    <td className="d100-cell">{entry.d100Min.toString().padStart(2, '0')}-{entry.d100Max.toString().padStart(2, '0')}</td>
                    <td style={{ fontWeight: '600', color: 'var(--accent-gold)' }}>{entry.label}</td>
                    <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.45' }}>{entry.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );
    }

    return null;
  };

  const renderEnhancements = () => {
    if (entity.category !== 'magia') return null;
    const sp = entity as SpellEntity;
    if (!sp.enhancements || sp.enhancements.length === 0) return null;

    return (
      <div className="enhancements-box">
        <h4 className="enhancements-title">Aprimoramentos de Mana:</h4>
        <ul className="enhancements-list">
          {sp.enhancements.map((enh, idx) => (
            <li key={idx} className="enhancement-item">
              <span className="enhancement-cost">{enh.cost}:</span>
              <span className="enhancement-desc">{enh.description}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  const renderRelatedEntities = () => {
    if (!entity.relatedIds || entity.relatedIds.length === 0) return null;

    return (
      <div className="related-entities-section">
        <h4 className="related-title">Conceitos Relacionados:</h4>
        <div className="related-chips">
          {entity.relatedIds.map(relId => {
            const relEntity = getEntityById(relId);
            if (!relEntity) return null;
            return (
              <button
                key={relId}
                className="chip-btn chip-btn-related"
                onClick={() => onSelectRelatedEntity(relEntity)}
              >
                <ExternalLink size={12} /> {relEntity.name} ({relEntity.category})
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-tome-wrapper parchment-card ornate-border" onClick={e => e.stopPropagation()}>
        {/* Cabeçalho do Tomo */}
        <div className="modal-header">
          <div>
            <div className="modal-header-badges">
              <span className="badge badge-gold modal-category-badge">{entity.category.toUpperCase()}</span>
              {entity.subcategory && <span className="badge badge-parchment">{entity.subcategory}</span>}
              {entity.proficiency && <span className="badge badge-ruby">{entity.proficiency}</span>}
            </div>
            <h2 className="modal-title">{entity.name}</h2>
          </div>
          <div className="modal-header-actions">
            <button 
              className={`copy-btn ${copied ? 'copy-success' : ''}`}
              onClick={handleCopyContent}
              title={copied ? 'Copiado!' : 'Copiar todo o conteúdo do modal'}
            >
              {copied ? <Check size={20} className="text-gold" /> : <Copy size={20} />}
            </button>
            <button 
              className={`favorite-btn ${isFavorite ? 'favorite-active' : ''}`}
              onClick={onToggleFavorite}
              title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
            >
              <Bookmark size={22} fill={isFavorite ? 'currentColor' : 'none'} />
            </button>
            <button className="modal-close-btn" onClick={onClose}>
              <X size={24} />
            </button>
          </div>
        </div>

        {/* Corpo do Tomo */}
        <div className="modal-body-content">
          {renderSpecificDetails()}

          <div className="modal-description-box">
            <h4 className="section-heading">Descrição</h4>
            <p className="modal-description-text">{entity.description}</p>
          </div>

          {renderEnhancements()}
          {renderRelatedEntities()}

          {/* Rastreabilidade de Fontes */}
          <div className="modal-sources-section">
            <h4 className="sources-title">Rastreabilidade Bibliográfica Oficial:</h4>
            <div className="sources-list">
              {entity.sources?.map((src, idx) => (
                <div key={idx} className="source-item">
                  <span className="source-book-name">📖 {formatBookName(src.book)}</span>
                  <span className="source-page-tag">Página {src.page}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
