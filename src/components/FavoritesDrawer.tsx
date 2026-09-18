import React, { useState, useMemo, useRef } from 'react';
import { 
  X, 
  Bookmark, 
  Search, 
  Sparkles, 
  Shield, 
  Swords, 
  Zap, 
  Activity, 
  BookOpen, 
  Skull, 
  MapPin, 
  Scroll, 
  Coins, 
  Compass, 
  Download, 
  Upload, 
  MessageSquare, 
  Edit3, 
  Check, 
  Trash2 
} from 'lucide-react';
import { CANONICAL_DATABASE, formatBookName, CATEGORIES_ENABLED_LIST } from '../data/database';
import type { T20CanonicalEntity, SpellEntity, EquipmentEntity, MonsterEntity, PowerEntity, TreasureTableEntity, EntityCategory } from '../types/t20_schema';
import { formatDate } from '../utils/formatters';
import { ScrollToTop } from './ScrollToTop';

interface FavoritesDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  favorites: string[];
  favoritesWithDate: Array<{ id: string; addedAt: string; comment?: string }>;
  onToggleFavorite: (id: string) => void;
  onUpdateComment?: (id: string, comment: string) => void;
  onExportFavorites?: () => void;
  onImportFavorites?: (jsonStr: string) => { success: boolean; count: number; message: string };
  onSelectEntity: (entity: T20CanonicalEntity) => void;
}

const CATEGORY_ICON_MAP: Record<string, React.ReactNode> = {
  todas: <Compass size={14} />,
  equipamento: <Shield size={14} />,
  magia: <Sparkles size={14} />,
  tesouro: <Coins size={14} />,
  poder: <Zap size={14} />,
  condicao: <Activity size={14} />,
  manobra: <Swords size={14} />,
  pericia: <BookOpen size={14} />,
  ameaca: <Skull size={14} />,
  origem_distincao: <MapPin size={14} />,
  regra: <Scroll size={14} />,
  lore: <Scroll size={14} />
};

const getCategoryBadge = (entity: T20CanonicalEntity) => {
  switch (entity.category) {
    case 'magia':
      const spell = entity as SpellEntity;
      return <span className="badge badge-mana"><Sparkles size={12} /> {spell.spellType} {spell.circle}º</span>;
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

const renderQuickStats = (entity: T20CanonicalEntity) => {
  if (entity.category === 'equipamento') {
    const eq = entity as EquipmentEntity;
    const td = eq.tableData;
    if (!td) return null;
    return (
      <div className="card-quick-stats">
        {td.purpose && <span className="stat-pill"><strong>Tipo:</strong> {td.purpose}</span>}
        {td.damage && <span className="stat-pill"><strong>Dano:</strong> {td.damage}</span>}
        {td.price && <span className="stat-pill stat-gold"><strong>{td.price}</strong></span>}
      </div>
    );
  }

  if (entity.category === 'magia') {
    const sp = entity as SpellEntity;
    return (
      <div className="card-quick-stats">
        <span className="stat-pill"><strong>Escola:</strong> {sp.school}</span>
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
      </div>
    );
  }

  return null;
};

export const FavoritesDrawer: React.FC<FavoritesDrawerProps> = ({
  isOpen,
  onClose,
  favorites,
  favoritesWithDate,
  onToggleFavorite,
  onUpdateComment,
  onExportFavorites,
  onImportFavorites,
  onSelectEntity
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<EntityCategory | 'todas'>('todas');
  const [importStatus, setImportStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Expanded comment panels state
  const [expandedCommentIds, setExpandedCommentIds] = useState<Set<string>>(new Set());
  const [editingCommentId, setEditingCommentId] = useState<string | null>(null);
  const [commentDraft, setCommentDraft] = useState<string>('');

  const fileInputRef = useRef<HTMLInputElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);

  // Reset filters and active edits when drawer opens
  React.useEffect(() => {
    if (isOpen) {
      setSearchQuery('');
      setSelectedCategory('todas');
      setImportStatus(null);
      setEditingCommentId(null);
    }
  }, [isOpen]);

  const favoriteEntities = useMemo(() => {
    return CANONICAL_DATABASE
      .filter(e => favorites.includes(e.id))
      .map(entity => {
        const favData = favoritesWithDate.find(f => f.id === entity.id);
        return {
          entity,
          addedAt: favData?.addedAt || new Date().toISOString(),
          comment: favData?.comment || ''
        };
      });
  }, [favorites, favoritesWithDate]);

  const filteredEntities = useMemo(() => {
    let results = favoriteEntities;

    // Filter by category
    if (selectedCategory !== 'todas') {
      results = results.filter(({ entity }) => entity.category === selectedCategory);
    }

    // Filter by search query (including personal comments!)
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      results = results.filter(({ entity, comment }) => 
        entity.name.toLowerCase().includes(query) ||
        entity.description.toLowerCase().includes(query) ||
        entity.category.toLowerCase().includes(query) ||
        entity.subcategory?.toLowerCase().includes(query) ||
        entity.tags?.some(tag => tag.toLowerCase().includes(query)) ||
        comment.toLowerCase().includes(query)
      );
    }

    // Sort by date (most recent first)
    return results.sort((a, b) => new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime());
  }, [favoriteEntities, selectedCategory, searchQuery]);

  // Get category counts for favorites
  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = { todas: favoriteEntities.length };
    favoriteEntities.forEach(({ entity }) => {
      counts[entity.category] = (counts[entity.category] || 0) + 1;
    });
    return counts;
  }, [favoriteEntities]);

  const handleToggleComment = (id: string, currentComment: string) => {
    setExpandedCommentIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
        if (editingCommentId === id) setEditingCommentId(null);
      } else {
        next.add(id);
        // If there's no comment yet, start editing immediately
        if (!currentComment.trim()) {
          setEditingCommentId(id);
          setCommentDraft('');
        }
      }
      return next;
    });
  };

  const handleStartEdit = (id: string, currentComment: string) => {
    setEditingCommentId(id);
    setCommentDraft(currentComment);
    setExpandedCommentIds(prev => new Set(prev).add(id));
  };

  const handleSaveComment = (id: string) => {
    if (onUpdateComment) {
      onUpdateComment(id, commentDraft);
    }
    setEditingCommentId(null);
    if (!commentDraft.trim()) {
      setExpandedCommentIds(prev => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  const handleDeleteComment = (id: string) => {
    if (onUpdateComment) {
      onUpdateComment(id, '');
    }
    setEditingCommentId(null);
    setExpandedCommentIds(prev => {
      const next = new Set(prev);
      next.delete(id);
      return next;
    });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      if (content && onImportFavorites) {
        const result = onImportFavorites(content);
        setImportStatus({
          type: result.success ? 'success' : 'error',
          message: result.message
        });
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="favorites-drawer parchment-card ornate-border" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="title-row">
            <span className="badge badge-gold"><Bookmark size={14} /> Tomo Pessoal</span>
            <h2 className="modal-title">Favoritos</h2>
          </div>

          <div className="fav-header-actions">
            {onExportFavorites && (
              <button 
                className="btn-fav-action"
                onClick={(e) => {
                  e.stopPropagation();
                  onExportFavorites();
                }}
                title="Exportar favoritos para arquivo JSON"
              >
                <Download size={14} /> Exportar
              </button>
            )}
            {onImportFavorites && (
              <>
                <button 
                  className="btn-fav-action"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  title="Importar favoritos de arquivo JSON"
                >
                  <Upload size={14} /> Importar
                </button>
                <input
                  type="file"
                  ref={fileInputRef}
                  accept=".json"
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />
              </>
            )}
            <button className="modal-close-btn" onClick={onClose} title="Fechar">
              <X size={24} />
            </button>
          </div>
        </div>

        <div className="favorites-body" ref={bodyRef}>
          {importStatus && (
            <div className={`fav-status-banner ${importStatus.type === 'success' ? 'status-success' : 'status-error'}`}>
              <span>{importStatus.message}</span>
              <button className="banner-close-btn" onClick={() => setImportStatus(null)}>
                <X size={14} />
              </button>
            </div>
          )}

          {/* Search and Category Filters */}
          <div className="favorites-filters">
            {/* Search Bar */}
            <div className="favorites-search-wrapper">
              <Search size={18} className="favorites-search-icon" />
              <input
                type="text"
                className="favorites-search-input"
                placeholder="Buscar nos favoritos (nome, descrição, anotação)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button 
                  className="favorites-search-clear"
                  onClick={() => setSearchQuery('')}
                  title="Limpar busca"
                >
                  <X size={16} />
                </button>
              )}
            </div>

            {/* General Category Filter Pills */}
            <div className="favorites-category-pills">
              {CATEGORIES_ENABLED_LIST.map((cat) => {
                const count = categoryCounts[cat.id] || 0;
                const isSelected = selectedCategory === cat.id;
                return (
                  <button
                    key={cat.id}
                    className={`fav-category-pill ${isSelected ? 'fav-category-pill-active' : ''}`}
                    onClick={() => setSelectedCategory(cat.id as any)}
                  >
                    {CATEGORY_ICON_MAP[cat.id]}
                    <span>{cat.label}</span>
                    <span className="fav-pill-count">({count})</span>
                  </button>
                );
              })}
            </div>

            {/* Results Count */}
            {(searchQuery || selectedCategory !== 'todas') && (
              <div className="favorites-results-count">
                {filteredEntities.length} {filteredEntities.length === 1 ? 'resultado' : 'resultados'}
              </div>
            )}
          </div>

          {filteredEntities.length === 0 ? (
            <div className="empty-favorites-box">
              <Bookmark size={48} className="empty-icon" />
              <h3>{searchQuery || selectedCategory !== 'todas' ? 'Nenhum resultado encontrado' : 'Nenhum item fixado'}</h3>
              <p>
                {searchQuery || selectedCategory !== 'todas' 
                  ? 'Tente ajustar os filtros de busca ou categoria.'
                  : 'Clique no ícone de marcador 🔖 em qualquer magia, manobra, item ou regra para salvá-la aqui para acesso em 1 clique durante a mesa.'
                }
              </p>
            </div>
          ) : (
            <div className="favorites-list">
              {filteredEntities.map(({ entity, addedAt, comment }) => {
                const primarySource = entity.sources?.[0];
                const isExpanded = expandedCommentIds.has(entity.id);
                const isEditing = editingCommentId === entity.id;
                const hasComment = Boolean(comment && comment.trim());

                return (
                  <article 
                    key={entity.id} 
                    className="favorite-item-card entity-list-item parchment-card ornate-border"
                    onClick={() => onSelectEntity(entity)}
                  >
                    <div className="card-header">
                      <div className="card-title-group">
                        {getCategoryBadge(entity)}
                        <h3 className="card-name">{entity.name}</h3>
                      </div>

                      {/* Card Action Buttons (Message Comment + Favorite Bookmark) */}
                      <div className="fav-card-actions">
                        <button
                          className={`fav-action-icon-btn ${hasComment ? 'has-comment' : ''} ${isExpanded ? 'active' : ''}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            handleToggleComment(entity.id, comment);
                          }}
                          title={hasComment ? "Ver/editar anotação" : "Adicionar anotação a este favorito"}
                        >
                          <MessageSquare size={16} fill={hasComment ? "currentColor" : "none"} />
                          {hasComment && <span className="comment-indicator-dot" />}
                        </button>

                        <button 
                          className="favorite-btn favorite-active"
                          onClick={(e) => {
                            e.stopPropagation();
                            onToggleFavorite(entity.id);
                          }}
                          title="Remover dos favoritos"
                        >
                          <Bookmark size={18} fill="currentColor" />
                        </button>
                      </div>
                    </div>

                    {renderQuickStats(entity)}

                    {/* Expandable Comment Section */}
                    {isExpanded && (
                      <div className="fav-comment-drawer-box" onClick={(e) => e.stopPropagation()}>
                        {isEditing ? (
                          <div className="fav-comment-edit-mode">
                            <div className="fav-comment-top-bar">
                              <span className="fav-comment-mode-label">
                                <Edit3 size={13} /> {hasComment ? 'Editar Anotação' : 'Nova Anotação'}
                              </span>
                              {hasComment && (
                                <button 
                                  className="btn-comment-delete" 
                                  onClick={() => handleDeleteComment(entity.id)}
                                  title="Remover anotação"
                                >
                                  <Trash2 size={13} /> Excluir
                                </button>
                              )}
                            </div>
                            <textarea
                              className="fav-comment-input"
                              placeholder="Ex: Pegar no nível 5; Usar contra mortos-vivos; Preparada na masmorra..."
                              value={commentDraft}
                              onChange={(e) => setCommentDraft(e.target.value)}
                              rows={2}
                              autoFocus
                            />
                            <div className="fav-comment-btn-row">
                              <button 
                                className="btn-comment-cancel" 
                                onClick={() => setEditingCommentId(null)}
                              >
                                Cancelar
                              </button>
                              <button 
                                className="btn-comment-save" 
                                onClick={() => handleSaveComment(entity.id)}
                              >
                                <Check size={14} /> Salvar
                              </button>
                            </div>
                          </div>
                        ) : (
                          <div className="fav-comment-view-mode">
                            <div className="fav-comment-top-bar">
                              <span className="fav-comment-mode-label">
                                <MessageSquare size={13} /> Anotação de Mesa
                              </span>
                              <button 
                                className="btn-comment-edit" 
                                onClick={() => handleStartEdit(entity.id, comment)}
                                title="Editar anotação"
                              >
                                <Edit3 size={12} /> Editar
                              </button>
                            </div>
                            <p className="fav-comment-text">{comment}</p>
                          </div>
                        )}
                      </div>
                    )}

                    <div className="card-footer">
                      <span className="source-label" title={primarySource?.book}>
                        {primarySource ? `📖 ${formatBookName(primarySource.book)} • Pág. ${primarySource.page}` : 'Tormenta20 Canônico'}
                      </span>
                      <span className="fav-date" title={`Adicionado aos favoritos em ${new Date(addedAt).toLocaleDateString('pt-BR')}`}>
                        <Bookmark size={11} className="text-gold" />
                        <span className="fav-date-label">Adicionado em:</span>
                        <span className="fav-date-value">{formatDate(addedAt)}</span>
                      </span>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </div>

        {/* Botão Flutuante Voltar ao Topo dos Favoritos */}
        <ScrollToTop containerRef={bodyRef} isInsideContainer title="Voltar ao topo dos favoritos" />
      </div>
    </div>
  );
};
