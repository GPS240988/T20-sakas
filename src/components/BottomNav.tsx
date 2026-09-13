import React from 'react';
import { Search, Coins, ShieldAlert, Bookmark } from 'lucide-react';

interface BottomNavProps {
  onOpenSearch: () => void;
  onOpenTreasure: () => void;
  onOpenCombatTracker: () => void;
  onOpenFavorites: () => void;
  favoritesCount: number;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  onOpenSearch,
  onOpenTreasure,
  onOpenCombatTracker,
  onOpenFavorites,
  favoritesCount,
}) => {
  return (
    <nav className="bottom-nav-container parchment-card">
      <button className="bottom-nav-btn" onClick={onOpenSearch}>
        <Search size={20} />
        <span>Busca</span>
      </button>

      <button className="bottom-nav-btn" onClick={onOpenTreasure}>
        <Coins size={20} />
        <span>Tesouros</span>
      </button>

      <button className="bottom-nav-btn" onClick={onOpenCombatTracker}>
        <ShieldAlert size={20} />
        <span>Condições</span>
      </button>

      <button className="bottom-nav-btn" onClick={onOpenFavorites}>
        <div className="nav-icon-wrapper">
          <Bookmark size={20} />
          {favoritesCount > 0 && (
            <span className="nav-badge badge-gold">{favoritesCount}</span>
          )}
        </div>
        <span>Favoritos</span>
      </button>
    </nav>
  );
};

