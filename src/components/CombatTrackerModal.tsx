import React, { useState, useMemo, useRef } from 'react';
import { 
  X, 
  ShieldAlert, 
  Search, 
  ChevronDown, 
  ChevronUp, 
  Copy, 
  Check, 
  Plus, 
  Trash2, 
  Play, 
  RotateCcw, 
  Heart, 
  UserPlus, 
  Flame, 
  BookOpen,
  Swords,
  Activity
} from 'lucide-react';
import { ScrollToTop } from './ScrollToTop';
import { CANONICAL_CONDITIONS, type ConditionCanonical } from './QuickReferenceModal';

// ============================================================================
// Modelo de Combatente
// ============================================================================

export interface Combatant {
  id: string;
  name: string;
  initiative: number;
  currentHp: number;
  maxHp: number;
  isPlayer: boolean;
  conditions: string[]; // Nomes das condições ativas
  notes?: string;
}

interface CombatTrackerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenQuickReference?: () => void;
}

export const CombatTrackerModal: React.FC<CombatTrackerModalProps> = ({
  isOpen,
  onClose,
  onOpenQuickReference,
}) => {
  const [activeTab, setActiveTab] = useState<'tracker' | 'consulta'>('tracker');
  const trackerBodyRef = useRef<HTMLDivElement>(null);
  
  // Estado do Combate
  const [round, setRound] = useState<number>(1);
  const [currentTurnIndex, setCurrentTurnIndex] = useState<number>(0);
  const [combatants, setCombatants] = useState<Combatant[]>([
    {
      id: 'c1',
      name: 'Guerreiro (Jogador)',
      initiative: 18,
      currentHp: 38,
      maxHp: 42,
      isPlayer: true,
      conditions: []
    },
    {
      id: 'c2',
      name: 'Líder Ogro',
      initiative: 14,
      currentHp: 65,
      maxHp: 80,
      isPlayer: false,
      conditions: ['Abalado']
    },
    {
      id: 'c3',
      name: 'Goblinoide Arqueiro',
      initiative: 12,
      currentHp: 18,
      maxHp: 18,
      isPlayer: false,
      conditions: ['Caído']
    }
  ]);

  // Form para novo combatente
  const [newName, setNewName] = useState('');
  const [newInit, setNewInit] = useState('');
  const [newHp, setNewHp] = useState('');
  const [newIsPlayer, setNewIsPlayer] = useState(false);
  const [isAddingCombatant, setIsAddingCombatant] = useState(false);

  // Popover de visualização de condição
  const [inspectCondition, setInspectCondition] = useState<ConditionCanonical | null>(null);
  const [conditionPickerTargetId, setConditionPickerTargetId] = useState<string | null>(null);

  // Aba de Consulta Rápida
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const [copied, setCopied] = useState(false);

  // Ordenação por Iniciativa Decrescente
  const sortedCombatants = useMemo(() => {
    return [...combatants].sort((a, b) => b.initiative - a.initiative);
  }, [combatants]);

  const filteredConditions = useMemo(() => {
    if (!searchTerm.trim()) return CANONICAL_CONDITIONS;
    const term = searchTerm.toLowerCase();
    return CANONICAL_CONDITIONS.filter(
      c =>
        c.name.toLowerCase().includes(term) ||
        c.description.toLowerCase().includes(term) ||
        (c.type && c.type.toLowerCase().includes(term))
    );
  }, [searchTerm]);

  const handleAddCombatant = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    const initVal = parseInt(newInit, 10) || 10;
    const hpVal = parseInt(newHp, 10) || 20;

    const newCombatant: Combatant = {
      id: `c_${Date.now()}`,
      name: newName.trim(),
      initiative: initVal,
      currentHp: hpVal,
      maxHp: hpVal,
      isPlayer: newIsPlayer,
      conditions: []
    };

    setCombatants(prev => [...prev, newCombatant]);
    setNewName('');
    setNewInit('');
    setNewHp('');
    setIsAddingCombatant(false);
  };

  const handleRemoveCombatant = (id: string) => {
    setCombatants(prev => prev.filter(c => c.id !== id));
  };

  const handleUpdateHp = (id: string, delta: number) => {
    setCombatants(prev =>
      prev.map(c => {
        if (c.id !== id) return c;
        const updated = Math.max(0, c.currentHp + delta);
        return { ...c, currentHp: updated };
      })
    );
  };

  const handleToggleConditionOnCombatant = (combatantId: string, conditionName: string) => {
    setCombatants(prev =>
      prev.map(c => {
        if (c.id !== combatantId) return c;
        const exists = c.conditions.includes(conditionName);
        const nextConditions = exists
          ? c.conditions.filter(name => name !== conditionName)
          : [...c.conditions, conditionName];
        return { ...c, conditions: nextConditions };
      })
    );
    setConditionPickerTargetId(null);
  };

  const handleNextTurn = () => {
    if (sortedCombatants.length === 0) return;
    if (currentTurnIndex + 1 >= sortedCombatants.length) {
      setCurrentTurnIndex(0);
      setRound(prev => prev + 1);
    } else {
      setCurrentTurnIndex(prev => prev + 1);
    }
  };

  const handleResetCombat = () => {
    setRound(1);
    setCurrentTurnIndex(0);
  };

  const handleCopyContent = () => {
    const lines: string[] = [];
    lines.push(`========================================`);
    lines.push(`CONDIÇÕES DE JOGO (TORMENTA20 - PÁG. 394-395)`);
    lines.push(`========================================\n`);

    filteredConditions.forEach(cond => {
      const typeStr = cond.type ? ` [${cond.type}]` : '';
      lines.push(`• ${cond.name.toUpperCase()}${typeStr} (pág. ${cond.page})`);
      lines.push(`  ${cond.description}\n`);
    });

    navigator.clipboard.writeText(lines.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="combat-tracker-modal parchment-card ornate-border"
        onClick={e => e.stopPropagation()}
      >
        {/* Header do Tracker */}
        <div className="tracker-header">
          <div className="tracker-title-group">
            <div className="tracker-icon-ruby">
              <ShieldAlert size={24} />
            </div>
            <div>
              <h2 className="tracker-title">Rastreador de Combate & Condições</h2>
              <p className="tracker-subtitle">Controle de Turnos, PV e Status de Jogo (Pág. 394)</p>
            </div>
          </div>
          <button className="tracker-close-btn" onClick={onClose} aria-label="Fechar Tracker">
            <X size={20} />
          </button>
        </div>

        {/* Abas Superiores */}
        <div className="tracker-nav-tabs">
          <button
            className={`tracker-tab-btn ${activeTab === 'tracker' ? 'active' : ''}`}
            onClick={() => setActiveTab('tracker')}
          >
            <Swords size={18} />
            <span>Mesa de Combate ({sortedCombatants.length})</span>
          </button>

          <button
            className={`tracker-tab-btn ${activeTab === 'consulta' ? 'active' : ''}`}
            onClick={() => setActiveTab('consulta')}
          >
            <Activity size={18} />
            <span>Guia Geral de Condições ({CANONICAL_CONDITIONS.length})</span>
          </button>
        </div>

        {/* Corpo do Tracker */}
        <div className="tracker-body" ref={trackerBodyRef}>
          {/* ============================================================= */}
          {/* MODO 1: RASTREADOR DE COMBATE EM TEMPO REAL                   */}
          {/* ============================================================= */}
          {activeTab === 'tracker' && (
            <div className="tracker-content-flow">
              {/* Barra de Rodadas & Controles */}
              <div className="tracker-round-banner parchment-subcard">
                <div className="round-info">
                  <span className="round-label">Rodada</span>
                  <span className="round-number">{round}</span>
                </div>

                <div className="round-actions">
                  <button className="parchment-btn btn-gold btn-next-turn" onClick={handleNextTurn}>
                    <Play size={16} />
                    <span>Próximo Turno</span>
                  </button>

                  <button className="parchment-btn btn-ghost" onClick={handleResetCombat} title="Reiniciar Rodadas">
                    <RotateCcw size={16} />
                  </button>

                  <button 
                    className="parchment-btn btn-gold btn-add-combatant"
                    onClick={() => setIsAddingCombatant(!isAddingCombatant)}
                  >
                    <UserPlus size={16} />
                    <span>{isAddingCombatant ? 'Cancelar' : 'Adicionar'}</span>
                  </button>
                </div>
              </div>

              {/* Form de Adicionar Combatente */}
              {isAddingCombatant && (
                <form className="add-combatant-form parchment-subcard" onSubmit={handleAddCombatant}>
                  <h4>Novo Combatente</h4>
                  <div className="form-row">
                    <input
                      type="text"
                      placeholder="Nome do personagem / monstro"
                      value={newName}
                      onChange={e => setNewName(e.target.value)}
                      className="form-input flex-2"
                      required
                    />
                    <input
                      type="number"
                      placeholder="Iniciativa"
                      value={newInit}
                      onChange={e => setNewInit(e.target.value)}
                      className="form-input flex-1"
                    />
                    <input
                      type="number"
                      placeholder="PV Máx"
                      value={newHp}
                      onChange={e => setNewHp(e.target.value)}
                      className="form-input flex-1"
                    />
                  </div>
                  <div className="form-actions-row">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={newIsPlayer}
                        onChange={e => setNewIsPlayer(e.target.checked)}
                      />
                      <span>Jogador / Aliado</span>
                    </label>

                    <button type="submit" className="parchment-btn btn-ruby">
                      Salvar Combatente
                    </button>
                  </div>
                </form>
              )}

              {/* Lista de Combatentes Ordenados */}
              <div className="combatants-list">
                {sortedCombatants.map((c, index) => {
                  const isCurrentTurn = index === currentTurnIndex;
                  return (
                    <div 
                      key={c.id} 
                      className={`combatant-card parchment-subcard ${isCurrentTurn ? 'active-turn' : ''} ${c.isPlayer ? 'is-player' : 'is-enemy'}`}
                    >
                      {/* Topo do Combatente */}
                      <div className="combatant-top">
                        <div className="combatant-name-block">
                          {isCurrentTurn && <span className="active-turn-indicator">★ Turno Atual</span>}
                          <h3 className="combatant-name">{c.name}</h3>
                          <span className={`badge-${c.isPlayer ? 'emerald' : 'ruby'} combatant-type-tag`}>
                            {c.isPlayer ? 'Jogador' : 'Ameaça'}
                          </span>
                        </div>

                        <div className="combatant-init-badge">
                          <span className="init-label">Inic.</span>
                          <span className="init-val">{c.initiative}</span>
                        </div>
                      </div>

                      {/* Controle de PV */}
                      <div className="combatant-hp-bar-row">
                        <div className="hp-info">
                          <Heart size={16} className={c.currentHp > 0 ? 'text-ruby' : 'text-muted'} />
                          <span className="hp-text"><strong>{c.currentHp}</strong> / {c.maxHp} PV</span>
                        </div>

                        <div className="hp-controls">
                          <button className="hp-btn" onClick={() => handleUpdateHp(c.id, -5)}>-5</button>
                          <button className="hp-btn" onClick={() => handleUpdateHp(c.id, -1)}>-1</button>
                          <button className="hp-btn" onClick={() => handleUpdateHp(c.id, 1)}>+1</button>
                          <button className="hp-btn" onClick={() => handleUpdateHp(c.id, 5)}>+5</button>
                        </div>

                        <button 
                          className="combatant-del-btn" 
                          onClick={() => handleRemoveCombatant(c.id)}
                          title="Remover combatente"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>

                      {/* Condições Ativas do Combatente */}
                      <div className="combatant-conditions-section">
                        <div className="conditions-header-row">
                          <span className="cond-title">Condições ({c.conditions.length}):</span>
                          <button 
                            className="add-cond-btn"
                            onClick={() => setConditionPickerTargetId(conditionPickerTargetId === c.id ? null : c.id)}
                          >
                            <Plus size={14} />
                            <span>Aplicar Condição</span>
                          </button>
                        </div>

                        <div className="combatant-cond-chips-wrap">
                          {c.conditions.length === 0 ? (
                            <span className="no-cond-text">Nenhuma condição ativa</span>
                          ) : (
                            c.conditions.map(condName => {
                              const found = CANONICAL_CONDITIONS.find(x => x.name === condName);
                              return (
                                <button
                                  key={condName}
                                  className="combatant-cond-pill"
                                  onClick={() => found && setInspectCondition(found)}
                                  title="Clique para ler a regra desta condição"
                                >
                                  <Flame size={12} className="cond-flame-icon" />
                                  <span>{condName}</span>
                                  <span 
                                    className="remove-cond-x" 
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      handleToggleConditionOnCombatant(c.id, condName);
                                    }}
                                  >
                                    ×
                                  </span>
                                </button>
                              );
                            })
                          )}
                        </div>

                        {/* Picker retrátil de condições */}
                        {conditionPickerTargetId === c.id && (
                          <div className="condition-picker-dropdown parchment-subcard ornate-border">
                            <div className="picker-header">
                              <span>Selecione a condição para {c.name}:</span>
                              <button onClick={() => setConditionPickerTargetId(null)}>
                                <X size={14} />
                              </button>
                            </div>
                            <div className="picker-grid">
                              {CANONICAL_CONDITIONS.map(cd => {
                                const has = c.conditions.includes(cd.name);
                                return (
                                  <button
                                    key={cd.name}
                                    className={`picker-cond-btn ${has ? 'active' : ''}`}
                                    onClick={() => handleToggleConditionOnCombatant(c.id, cd.name)}
                                  >
                                    {cd.name}
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* ============================================================= */}
          {/* MODO 2: CONSULTA GERAL DE CONDIÇÕES (PÁG. 240 / 394-395)      */}
          {/* ============================================================= */}
          {activeTab === 'consulta' && (
            <div className="tracker-content-flow">
              <div className="tracker-search-row">
                <div className="tracker-search-box">
                  <Search size={18} className="search-icon-muted" />
                  <input
                    type="text"
                    placeholder="Filtrar por nome ou efeito..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    className="tracker-search-input"
                  />
                  {searchTerm && (
                    <button className="clear-search-btn" onClick={() => setSearchTerm('')}>
                      <X size={16} />
                    </button>
                  )}
                </div>

                <button
                  className={`copy-btn parchment-btn ${copied ? 'btn-copied' : ''}`}
                  onClick={handleCopyContent}
                  title="Copiar lista"
                >
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                  <span>{copied ? 'Copiado!' : 'Copiar'}</span>
                </button>
              </div>

              <div className="conditions-list-flow">
                {filteredConditions.map((cond, idx) => {
                  const isExpanded = expandedIndex === idx;
                  return (
                    <div 
                      key={cond.name}
                      className={`cond-card-item parchment-subcard ${isExpanded ? 'expanded' : ''}`}
                    >
                      <div 
                        className="cond-card-header"
                        onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                      >
                        <div className="cond-title-left">
                          <h4 className="cond-name-title">{cond.name}</h4>
                          {cond.type && (
                            <span className="badge-ruby cond-type-badge"><em>{cond.type}</em></span>
                          )}
                          <span className="badge-parchment cond-page-badge">pág. {cond.page}</span>
                        </div>

                        <div className="cond-header-right">
                          <button className="expand-icon-btn">
                            {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                          </button>
                        </div>
                      </div>

                      <div className="cond-card-body">
                        <p className="cond-desc-text">{cond.description}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Modal Popover de Inspeção de Regra de Condição */}
        {inspectCondition && (
          <div className="condition-inspect-popover" onClick={() => setInspectCondition(null)}>
            <div className="inspect-box parchment-card ornate-border" onClick={e => e.stopPropagation()}>
              <div className="inspect-header">
                <div className="inspect-title-group">
                  <ShieldAlert size={20} className="text-ruby" />
                  <h3>{inspectCondition.name}</h3>
                  {inspectCondition.type && (
                    <span className="badge-ruby"><em>{inspectCondition.type}</em></span>
                  )}
                  <span className="badge-gold">pág. {inspectCondition.page}</span>
                </div>
                <button onClick={() => setInspectCondition(null)}>
                  <X size={18} />
                </button>
              </div>

              <div className="inspect-body">
                <p>{inspectCondition.description}</p>
              </div>

              <div className="inspect-footer">
                <button className="parchment-btn btn-gold" onClick={() => setInspectCondition(null)}>
                  Fechar
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer do Tracker */}
        <div className="tracker-footer">
          <span className="tracker-meta-text">
            Tormenta20 • Rastreamento oficial de combate e condições canônicas
          </span>
          {onOpenQuickReference && (
            <button 
              className="parchment-btn btn-gold"
              onClick={() => {
                onClose();
                onOpenQuickReference();
              }}
            >
              <BookOpen size={16} />
              <span>Abrir Tomo de Regras (Pág. 220)</span>
            </button>
          )}
        </div>

        <ScrollToTop containerRef={trackerBodyRef} isInsideContainer />
      </div>
    </div>
  );
};
