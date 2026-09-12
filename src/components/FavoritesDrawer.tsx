import React from 'react';
import { X, Bookmark, Trash2 } from 'lucide-react';
import { CANONICAL_DATABASE } from '../data/database';
import type { T20CanonicalEntity } from '../types/t20_schema';

interface FavoritesDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  favorites: string[];
  onToggleFavorite: (id: string) => void;
  onSelectEntity: (entity: T20CanonicalEntity) => void;
}

export const FavoritesDrawer: React.FC<FavoritesDrawerProps> = ({
  isOpen,
  onClose,
  favorites,
  onToggleFavorite,
  onSelectEntity
}) => {
  if (!isOpen) return null;

  const favoriteEntities = CANONICAL_DATABASE.filter(e => favorites.includes(e.id));

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="favorites-drawer parchment-card ornate-border" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="title-row">
            <span className="badge badge-gold"><Bookmark size={14} /> Tomo Pessoal</span>
            <h2 className="modal-title">Favoritos & Regras Fixadas</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="favorites-body">
          {favoriteEntities.length === 0 ? (
            <div className="empty-favorites-box">
              <Bookmark size={48} className="empty-icon" />
              <h3>Nenhum item fixado</h3>
              <p>Clique no ícone de marcador 🔖 em qualquer magia, manobra, item ou regra para salvá-la aqui para acesso em 1 clique durante a mesa.</p>
            </div>
          ) : (
            <div className="favorites-list">
              {favoriteEntities.map(entity => (
                <div key={entity.id} className="favorite-item-card parchment-card">
                  <div className="fav-item-info" onClick={() => onSelectEntity(entity)}>
                    <span className="badge badge-parchment">{entity.category.toUpperCase()}</span>
                    <h4 className="fav-name">{entity.name}</h4>
                    <p className="fav-desc">{entity.summary || entity.description.slice(0, 80) + '...'}</p>
                  </div>
                  <button 
                    className="fav-delete-btn" 
                    onClick={() => onToggleFavorite(entity.id)}
                    title="Remover dos favoritos"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
