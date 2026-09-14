import { useState, useEffect } from 'react';

const STORAGE_KEY = 't20_sakas_favorites';

export interface FavoriteItem {
  id: string;
  addedAt: string;
  comment?: string;
}

export function useFavorites() {
  const [favorites, setFavorites] = useState<FavoriteItem[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (!stored) return [];
      
      const parsed = JSON.parse(stored);
      // Migration: if old format (string array), convert to new format
      if (parsed.length > 0 && typeof parsed[0] === 'string') {
        const migrated: FavoriteItem[] = parsed.map((id: string) => ({
          id,
          addedAt: new Date().toISOString()
        }));
        localStorage.setItem(STORAGE_KEY, JSON.stringify(migrated));
        return migrated;
      }
      return parsed;
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(favorites));
    } catch (e) {
      console.error('Erro ao salvar favoritos no LocalStorage', e);
    }
  }, [favorites]);

  const toggleFavorite = (id: string) => {
    setFavorites(prev => {
      const exists = prev.some(f => f.id === id);
      if (exists) {
        return prev.filter(fId => fId.id !== id);
      } else {
        return [...prev, { id, addedAt: new Date().toISOString() }];
      }
    });
  };

  const updateFavoriteComment = (id: string, comment: string) => {
    setFavorites(prev =>
      prev.map(item =>
        item.id === id
          ? { ...item, comment: comment.trim() ? comment.trim() : undefined }
          : item
      )
    );
  };

  const isFavorite = (id: string) => favorites.some(f => f.id === id);
  
  const getFavoriteDate = (id: string): string | null => {
    const fav = favorites.find(f => f.id === id);
    return fav ? fav.addedAt : null;
  };

  const exportFavorites = async () => {
    try {
      const dataToExport = {
        app: 'T20 Sakas Compêndio',
        version: '1.0',
        exportedAt: new Date().toISOString(),
        favorites
      };
      const jsonStr = JSON.stringify(dataToExport, null, 2);
      const dateStr = new Date().toISOString().slice(0, 10);
      const filename = `t20_favoritos_${dateStr}.json`;

      // 1. Tentar a API nativa do Chrome / Edge (File System Access API)
      if (typeof window !== 'undefined' && 'showSaveFilePicker' in window) {
        try {
          const handle = await (window as any).showSaveFilePicker({
            suggestedName: filename,
            types: [{
              description: 'Arquivo de Favoritos T20 (*.json)',
              accept: { 'application/json': ['.json'] }
            }]
          });
          const writable = await handle.createWritable();
          await writable.write(jsonStr);
          await writable.close();
          return;
        } catch (err: any) {
          if (err?.name === 'AbortError') return; // Usuário cancelou a janela de salvar
          console.warn('showSaveFilePicker indisponível ou bloqueado, utilizando fallback de download...', err);
        }
      }

      // 2. Fallback universal via Blob e elemento <a> temporário
      const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
      const url = window.URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.setAttribute('download', filename);
      link.style.display = 'none';
      
      document.body.appendChild(link);
      link.click();

      setTimeout(() => {
        if (document.body.contains(link)) {
          document.body.removeChild(link);
        }
        window.URL.revokeObjectURL(url);
      }, 10000);
    } catch (err) {
      console.error('Erro ao exportar favoritos:', err);
    }
  };

  const importFavorites = (jsonString: string): { success: boolean; count: number; message: string } => {
    try {
      const parsed = JSON.parse(jsonString);
      let itemsToImport: FavoriteItem[] = [];

      if (Array.isArray(parsed)) {
        if (parsed.length > 0 && typeof parsed[0] === 'string') {
          itemsToImport = parsed.map((id: string) => ({ id, addedAt: new Date().toISOString() }));
        } else {
          itemsToImport = parsed.filter(item => item && typeof item.id === 'string');
        }
      } else if (parsed && Array.isArray(parsed.favorites)) {
        if (parsed.favorites.length > 0 && typeof parsed.favorites[0] === 'string') {
          itemsToImport = parsed.favorites.map((id: string) => ({ id, addedAt: new Date().toISOString() }));
        } else {
          itemsToImport = parsed.favorites.filter((item: any) => item && typeof item.id === 'string');
        }
      } else {
        return { success: false, count: 0, message: 'Formato de arquivo JSON de favoritos inválido.' };
      }

      if (itemsToImport.length === 0) {
        return { success: false, count: 0, message: 'Nenhum favorito válido foi encontrado no arquivo.' };
      }

      let addedCount = 0;
      setFavorites(prev => {
        const map = new Map<string, FavoriteItem>();
        prev.forEach(item => map.set(item.id, item));
        itemsToImport.forEach(item => {
          if (!map.has(item.id)) {
            map.set(item.id, {
              id: item.id,
              addedAt: item.addedAt || new Date().toISOString(),
              comment: item.comment || undefined
            });
            addedCount++;
          } else if (item.comment && !map.get(item.id)?.comment) {
            // If item exists without comment, adopt imported comment
            const existing = map.get(item.id)!;
            map.set(item.id, { ...existing, comment: item.comment });
          }
        });
        return Array.from(map.values());
      });

      return {
        success: true,
        count: addedCount,
        message: addedCount > 0 
          ? `${addedCount} novo(s) favorito(s) importado(s) com sucesso!` 
          : 'Todos os favoritos do arquivo já pertencem à sua lista.'
      };
    } catch (err) {
      console.error('Erro ao importar favoritos:', err);
      return { success: false, count: 0, message: 'Erro ao processar o arquivo. Verifique se é um arquivo JSON de favoritos válido.' };
    }
  };

  const favoriteIds = favorites.map(f => f.id);

  return {
    favorites: favoriteIds,
    favoritesWithDate: favorites,
    toggleFavorite,
    updateFavoriteComment,
    isFavorite,
    getFavoriteDate,
    exportFavorites,
    importFavorites,
    count: favorites.length
  };
}

