import React from 'react';
import { BookMarked, ShieldAlert } from 'lucide-react';
import { CONSOLIDATION_AUDIT } from '../data/database';

interface HeaderProps {
  onOpenCombatTracker: () => void;
  onOpenFavorites: () => void;
  onOpenTreasure: () => void;
  favoritesCount: number;
  activeConditionsCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenCombatTracker,
  onOpenFavorites,
  onOpenTreasure,
  favoritesCount,
  activeConditionsCount
}) => {
  return (
    <header className="header-container">
      <div className="header-content">
        <div className="brand-wrapper">
          <div className="shield-icon">
            <span className="heraldic-symbol">⚔️</span>
          </div>
          <div>
            <div className="title-row">
              <h1 className="header-title">TORMENTA 20</h1>
              <span className="badge badge-gold">Compêndio Canônico</span>
            </div>
            <p className="header-subtitle">
              Base Consolidada dos 4 Livros • <span className="highlight-text">{CONSOLIDATION_AUDIT.total} Regras & Entidades</span>
            </p>
          </div>
        </div>

        <div className="header-actions">
          <button 
            className="header-btn" 
            onClick={onOpenTreasure}
            title="Simulador e Tabela de Tesouros"
          >
            <span className="btn-icon">🎲</span>
            <span className="btn-label">Tesouros</span>
          </button>

          <button 
            className={`header-btn ${activeConditionsCount > 0 ? 'header-btn-active-ruby' : ''}`} 
            onClick={onOpenCombatTracker}
            title="Condições de Mesa"
          >
            <ShieldAlert size={18} className="btn-icon" />
            <span className="btn-label">Condições</span>
            {activeConditionsCount > 0 && (
              <span className="counter-badge badge-ruby">{activeConditionsCount}</span>
            )}
          </button>

          <button 
            className="header-btn" 
            onClick={onOpenFavorites}
            title="Favoritos e Regras Fixadas"
          >
            <BookMarked size={18} className="btn-icon" />
            <span className="btn-label">Favoritos</span>
            {favoritesCount > 0 && (
              <span className="counter-badge badge-gold">{favoritesCount}</span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
