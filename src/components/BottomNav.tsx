import React from 'react';
import { Search, Coins, Bookmark, BookOpen } from 'lucide-react';

interface BottomNavProps {
  onOpenSearch: () => void;
  onOpenQuickReference: () => void;
  onOpenTreasure: () => void;
  onOpenFavorites: () => void;
  favoritesCount: number;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  onOpenSearch,
  onOpenQuickReference,
  onOpenTreasure,
  onOpenFavorites,
  favoritesCount,
}) => {
  return (
    <nav className="bottom-nav-container parchment-card">
      <button className="bottom-nav-btn" onClick={onOpenSearch} title="Busca Universal">
        <Search size={19} />
        <span>Busca</span>
      </button>

      <button className="bottom-nav-btn" onClick={onOpenQuickReference} title="Regras (Pág. 220 & 240)">
        <BookOpen size={19} />
        <span>Regras</span>
      </button>

      <button className="bottom-nav-btn" onClick={onOpenTreasure} title="Gerador de Tesouros">
        <Coins size={19} />
        <span>Tesouros</span>
      </button>

      <button className="bottom-nav-btn" onClick={onOpenFavorites} title="Favoritos & Anotações">
        <div className="nav-icon-wrapper">
          <Bookmark size={19} />
          {favoritesCount > 0 && (
            <span className="nav-badge badge-gold">{favoritesCount}</span>
          )}
        </div>
        <span>Favoritos</span>
      </button>
    </nav>
  );
};
