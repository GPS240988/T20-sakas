import React from 'react';
import { BookMarked, BookOpen } from 'lucide-react';
import cabecalho from '../../cabecalho.jpg';

interface HeaderProps {
  onOpenQuickReference: () => void;
  onOpenFavorites: () => void;
  onOpenTreasure: () => void;
  favoritesCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenQuickReference,
  onOpenFavorites,
  onOpenTreasure,
  favoritesCount,
}) => {
  return (
    <header className="header-container">
      <div className="header-content">
        <div className="header-brand">
          <img
            src={cabecalho}
            alt="Tormenta 20 - Cabecalho"
            className="header-logo"
          />
        </div>

        <div className="header-title-wrapper">
          <h1 className="header-title">Tormenta 20 — SAKA'S</h1>
        </div>

        <div className="header-actions">
          <button
            className="header-btn"
            onClick={onOpenQuickReference}
            title="Tomo de Regras (Pág. 220) e Condições (Pág. 240)"
          >
            <BookOpen size={18} className="btn-icon" />
            <span className="btn-label">Regras & Manobras</span>
          </button>

          <button
            className="header-btn"
            onClick={onOpenTreasure}
            title="Simulador e Tabela de Tesouros"
          >
            <span className="btn-icon">🎲</span>
            <span className="btn-label">Tesouros</span>
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
