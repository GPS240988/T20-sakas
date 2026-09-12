import React, { useState } from 'react';
import { X, ShieldAlert, Heart, Zap, Trash2 } from 'lucide-react';
import { CANONICAL_DATABASE } from '../data/database';
import type { ConditionEntity, T20CanonicalEntity } from '../types/t20_schema';

interface CombatTrackerModalProps {
  isOpen: boolean;
  onClose: () => void;
  tracker: {
    characterName: string;
    currentHp: number;
    maxHp: number;
    currentMp: number;
    maxMp: number;
    activeConditionIds: string[];
  };
  onToggleCondition: (id: string) => void;
  onRemoveCondition: (id: string) => void;
  onUpdateHp: (delta: number) => void;
  onUpdateMp: (delta: number) => void;
  onSelectEntity: (entity: T20CanonicalEntity) => void;
}

export const CombatTrackerModal: React.FC<CombatTrackerModalProps> = ({
  isOpen,
  onClose,
  tracker,
  onToggleCondition,
  onRemoveCondition,
  onUpdateHp,
  onUpdateMp,
  onSelectEntity
}) => {
  const [conditionSearch, setConditionSearch] = useState('');
  const [selectedConditionId, setSelectedConditionId] = useState<string | null>(null);

  const allConditions = CANONICAL_DATABASE.filter(
    e => e.category === 'condicao'
  ) as ConditionEntity[];

  const filteredConditions = allConditions.filter(c =>
    c.name.toLowerCase().includes(conditionSearch.toLowerCase()) ||
    c.description.toLowerCase().includes(conditionSearch.toLowerCase())
  );

  const selectedCondition = allConditions.find(c => c.id === selectedConditionId) || 
    (tracker.activeConditionIds.length > 0 ? allConditions.find(c => c.id === tracker.activeConditionIds[0]) : filteredConditions[0]);

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="combat-tracker-modal parchment-card ornate-border" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="title-row">
            <span className="badge badge-ruby"><ShieldAlert size={14} /> Condições</span>
            <h2 className="modal-title">Condições de Tormenta20</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="combat-tracker-body">
          {/* Barra de PV & PM */}
          <div className="vitals-panel">
            <div className="vital-box vital-hp">
              <div className="vital-header">
                <span className="vital-label"><Heart size={16} /> Pontos de Vida (PV)</span>
                <span className="vital-value">{tracker.currentHp} / {tracker.maxHp}</span>
              </div>
              <div className="vital-bar-track">
                <div 
                  className="vital-bar-fill fill-hp" 
                  style={{ width: `${Math.max(0, Math.min(100, (tracker.currentHp / tracker.maxHp) * 100))}%` }}
                />
              </div>
              <div className="vital-controls">
                <button className="vital-btn" onClick={() => onUpdateHp(-5)}>-5</button>
                <button className="vital-btn" onClick={() => onUpdateHp(-1)}>-1</button>
                <button className="vital-btn" onClick={() => onUpdateHp(1)}>+1</button>
                <button className="vital-btn" onClick={() => onUpdateHp(5)}>+5</button>
              </div>
            </div>

            <div className="vital-box vital-mp">
              <div className="vital-header">
                <span className="vital-label"><Zap size={16} /> Pontos de Mana (PM)</span>
                <span className="vital-value">{tracker.currentMp} / {tracker.maxMp}</span>
              </div>
              <div className="vital-bar-track">
                <div 
                  className="vital-bar-fill fill-mp" 
                  style={{ width: `${Math.max(0, Math.min(100, (tracker.currentMp / tracker.maxMp) * 100))}%` }}
                />
              </div>
              <div className="vital-controls">
                <button className="vital-btn" onClick={() => onUpdateMp(-3)}>-3</button>
                <button className="vital-btn" onClick={() => onUpdateMp(-1)}>-1</button>
                <button className="vital-btn" onClick={() => onUpdateMp(1)}>+1</button>
                <button className="vital-btn" onClick={() => onUpdateMp(3)}>+3</button>
              </div>
            </div>
          </div>

          {/* Painel da Condição Selecionada (Texto Exato do Livro) */}
          {selectedCondition && (
            <div className="selected-condition-detail-box parchment-card ornate-border" style={{ marginBottom: '1rem', padding: '1rem', background: 'var(--bg-surface)', borderRadius: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className="badge badge-ruby" style={{ fontWeight: '700' }}>{selectedCondition.name}</span>
                  {(selectedCondition.effectType || (selectedCondition as any).type) && (
                    <span className="badge badge-parchment">{selectedCondition.effectType || (selectedCondition as any).type}</span>
                  )}
                  {selectedCondition.subcategory && <span className="badge badge-gold">{selectedCondition.subcategory}</span>}
                </div>
                <button
                  className={`vital-btn ${tracker.activeConditionIds.includes(selectedCondition.id) ? 'badge-ruby' : 'badge-gold'}`}
                  style={{ padding: '0.3rem 0.8rem', fontSize: '0.8rem', height: 'auto' }}
                  onClick={() => onToggleCondition(selectedCondition.id)}
                >
                  {tracker.activeConditionIds.includes(selectedCondition.id) ? '✓ Ativa no Personagem' : '+ Aplicar ao Personagem'}
                </button>
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: '1.5', margin: '0.5rem 0', fontStyle: 'normal' }}>
                {selectedCondition.description}
              </p>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem', borderTop: '1px solid var(--border-parchment)', paddingTop: '0.4rem' }}>
                <span>📖 Tormenta20 (Jogo do Ano) • Apêndice: Condições • Pág. 400</span>
                <button 
                  style={{ background: 'none', border: 'none', color: 'var(--accent-gold)', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600' }}
                  onClick={() => onSelectEntity(selectedCondition)}
                >
                  Abrir no Compêndio →
                </button>
              </div>
            </div>
          )}

          {/* Condições Ativas */}
          <div className="active-conditions-section">
            <h4>Condições Ativas no Personagem ({tracker.activeConditionIds.length}):</h4>
            {tracker.activeConditionIds.length === 0 ? (
              <p className="no-conditions-text">Nenhuma condição ativa. Selecione abaixo para aplicar.</p>
            ) : (
              <div className="active-conditions-list">
                {tracker.activeConditionIds.map(condId => {
                  const cond = allConditions.find(c => c.id === condId);
                  if (!cond) return null;
                  const isSelected = selectedCondition?.id === cond.id;
                  return (
                    <div 
                      key={condId} 
                      className={`active-condition-card parchment-card ${isSelected ? 'ornate-border' : ''}`}
                      onClick={() => setSelectedConditionId(cond.id)}
                      style={{ cursor: 'pointer', borderLeft: isSelected ? '4px solid var(--accent-ruby)' : undefined }}
                    >
                      <div className="cond-card-top">
                        <span className="cond-name">{cond.name}</span>
                        <button className="cond-remove-btn" onClick={(e) => { e.stopPropagation(); onRemoveCondition(condId); }}>
                          <Trash2 size={16} />
                        </button>
                      </div>
                      <p className="cond-effect">{cond.description}</p>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Seletor Rápido de Condições */}
          <div className="condition-picker-section">
            <div className="picker-header">
              <h4>Lista de Condições Oficial:</h4>
              <input
                type="text"
                className="condition-search-input"
                placeholder="Filtrar condições... (ex: Cego, Abalado, Caído)"
                value={conditionSearch}
                onChange={e => setConditionSearch(e.target.value)}
              />
            </div>
            <div className="conditions-grid-chips">
              {filteredConditions.map(cond => {
                const isActive = tracker.activeConditionIds.includes(cond.id);
                const isSelected = selectedCondition?.id === cond.id;
                return (
                  <button
                    key={cond.id}
                    className={`cond-toggle-btn ${isActive ? 'cond-toggle-active' : ''} ${isSelected ? 'cond-selected-chip' : ''}`}
                    onClick={() => {
                      setSelectedConditionId(cond.id);
                      onToggleCondition(cond.id);
                    }}
                    style={{
                      outline: isSelected ? '2px solid var(--accent-gold)' : 'none'
                    }}
                  >
                    {isActive ? '✓ ' : '+ '} {cond.name}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
