import { useState, useEffect } from 'react';

const STORAGE_KEY = 't20_sakas_combat_tracker';

export interface CombatTrackerState {
  characterName: string;
  currentHp: number;
  maxHp: number;
  currentMp: number;
  maxMp: number;
  activeConditionIds: string[];
}

const DEFAULT_STATE: CombatTrackerState = {
  characterName: 'Herói de Arton',
  currentHp: 20,
  maxHp: 20,
  currentMp: 10,
  maxMp: 10,
  activeConditionIds: []
};

export function useCombatTracker() {
  const [tracker, setTracker] = useState<CombatTrackerState>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : DEFAULT_STATE;
    } catch {
      return DEFAULT_STATE;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tracker));
    } catch (e) {
      console.error('Erro ao salvar estado de combate', e);
    }
  }, [tracker]);

  const toggleCondition = (conditionId: string) => {
    setTracker(prev => {
      const exists = prev.activeConditionIds.includes(conditionId);
      return {
        ...prev,
        activeConditionIds: exists
          ? prev.activeConditionIds.filter(id => id !== conditionId)
          : [...prev.activeConditionIds, conditionId]
      };
    });
  };

  const removeCondition = (conditionId: string) => {
    setTracker(prev => ({
      ...prev,
      activeConditionIds: prev.activeConditionIds.filter(id => id !== conditionId)
    }));
  };

  const updateHp = (delta: number) => {
    setTracker(prev => ({
      ...prev,
      currentHp: Math.min(prev.maxHp, prev.currentHp + delta)
    }));
  };

  const updateMp = (delta: number) => {
    setTracker(prev => ({
      ...prev,
      currentMp: Math.min(prev.maxMp, Math.max(0, prev.currentMp + delta))
    }));
  };

  const setStats = (maxHp: number, maxMp: number) => {
    setTracker(prev => ({
      ...prev,
      maxHp,
      currentHp: maxHp,
      maxMp,
      currentMp: maxMp
    }));
  };

  return {
    tracker,
    toggleCondition,
    removeCondition,
    updateHp,
    updateMp,
    setStats,
    isConditionActive: (id: string) => tracker.activeConditionIds.includes(id)
  };
}
