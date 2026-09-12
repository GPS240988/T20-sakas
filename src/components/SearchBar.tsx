import React, { useRef, useEffect } from 'react';
import { Search, X } from 'lucide-react';

interface SearchBarProps {
  query: string;
  onQueryChange: (query: string) => void;
  resultsCount: number;
  totalCount: number;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  query,
  onQueryChange,
  resultsCount,
  totalCount
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
      if (e.key === '/' && document.activeElement !== inputRef.current) {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="searchbar-container">
      <div className="searchbar-wrapper parchment-card">
        <Search className="search-icon" size={20} />
        <input
          ref={inputRef}
          type="text"
          className="search-input"
          placeholder="Buscar qualquer regra, magia, manobra, arma, condição... (ex: Agarrar, Bola de Fogo, ND 5, Zakharov)"
          value={query}
          onChange={e => onQueryChange(e.target.value)}
        />
        {query && (
          <button 
            className="clear-btn" 
            onClick={() => onQueryChange('')}
            title="Limpar busca"
          >
            <X size={18} />
          </button>
        )}
        <div className="search-shortcut-badge">
          <kbd className="kbd-key">/</kbd>
        </div>
      </div>
      
      <div className="search-status-bar">
        <span className="results-text">
          {query ? (
            <>Exibindo <strong>{resultsCount}</strong> de {totalCount} resultados</>
          ) : (
            <>Total de <strong>{totalCount}</strong> entidades canônicas em Arton</>
          )}
        </span>
      </div>
    </div>
  );
};
