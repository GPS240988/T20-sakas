import React, { useRef, useEffect, useState, useCallback } from 'react';
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
  const [localValue, setLocalValue] = useState(query);
  const timerRef = useRef<number | null>(null);

  // Keep local value synced if parent query changes (e.g. resetFilters)
  useEffect(() => {
    setLocalValue(query);
  }, [query]);

  const triggerDebouncedChange = useCallback((val: string) => {
    if (timerRef.current) {
      window.clearTimeout(timerRef.current);
    }
    timerRef.current = window.setTimeout(() => {
      onQueryChange(val);
    }, 150);
  }, [onQueryChange]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setLocalValue(val);
    triggerDebouncedChange(val);
  };

  const handleClear = () => {
    if (timerRef.current) {
      window.clearTimeout(timerRef.current);
    }
    setLocalValue('');
    onQueryChange('');
    inputRef.current?.focus();
  };

  const handleKeyDownInput = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      if (timerRef.current) {
        window.clearTimeout(timerRef.current);
      }
      onQueryChange(localValue);
    }
  };

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
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      if (timerRef.current) window.clearTimeout(timerRef.current);
    };
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
          value={localValue}
          onChange={handleChange}
          onKeyDown={handleKeyDownInput}
        />
        {localValue && (
          <button 
            className="clear-btn" 
            onClick={handleClear}
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
