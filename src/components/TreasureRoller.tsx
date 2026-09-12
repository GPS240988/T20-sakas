import React, { useState, useMemo } from 'react';
import { X, Dices, Coins, Sparkles } from 'lucide-react';
import { CANONICAL_DATABASE } from '../data/database';
import type { TreasureTableEntity, TreasureRollEntry } from '../types/t20_schema';

interface TreasureRollerProps {
  isOpen: boolean;
  onClose: () => void;
}

const ND_OPTIONS = ['1/4', '1/2', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'];

export const TreasureRoller: React.FC<TreasureRollerProps> = ({ isOpen, onClose }) => {
  const [selectedNd, setSelectedNd] = useState<string>('5');
  const [moneyRoll, setMoneyRoll] = useState<number | ''>('');
  const [itemRoll, setItemRoll] = useState<number | ''>('');
  const [lastRolledMoney, setLastRolledMoney] = useState<TreasureRollEntry | null>(null);
  const [lastRolledItem, setLastRolledItem] = useState<TreasureRollEntry | null>(null);

  // Encontrar a tabela de tesouro correspondente ao ND selecionado
  const treasureTable = useMemo(() => {
    return CANONICAL_DATABASE.find(
      e => e.category === 'tesouro' && e.id === `tesouro-tabela-nd-${selectedNd.replace('/', '-')}`
    ) as TreasureTableEntity | undefined;
  }, [selectedNd]);

  if (!isOpen) return null;

  const handleRollDice = () => {
    const rolledM = Math.floor(Math.random() * 100) + 1;
    const rolledI = Math.floor(Math.random() * 100) + 1;
    setMoneyRoll(rolledM);
    setItemRoll(rolledI);
    evaluateRolls(rolledM, rolledI);
  };

  const evaluateRolls = (mVal: number, iVal: number) => {
    if (!treasureTable) return;

    // Achar entrada de dinheiro
    const mEntry = treasureTable.entries.find(
      e => e.label.startsWith('Dinheiro') && mVal >= e.d100Min && mVal <= e.d100Max
    );
    // Achar entrada de item
    const iEntry = treasureTable.entries.find(
      e => e.label.startsWith('Item') && iVal >= e.d100Min && iVal <= e.d100Max
    );

    setLastRolledMoney(mEntry || null);
    setLastRolledItem(iEntry || null);
  };

  const handleManualMoneyChange = (val: string) => {
    const num = parseInt(val, 10);
    if (isNaN(num)) {
      setMoneyRoll('');
      setLastRolledMoney(null);
    } else {
      const clamped = Math.max(1, Math.min(100, num));
      setMoneyRoll(clamped);
      if (treasureTable) {
        const mEntry = treasureTable.entries.find(
          e => e.label.startsWith('Dinheiro') && clamped >= e.d100Min && clamped <= e.d100Max
        );
        setLastRolledMoney(mEntry || null);
      }
    }
  };

  const handleManualItemChange = (val: string) => {
    const num = parseInt(val, 10);
    if (isNaN(num)) {
      setItemRoll('');
      setLastRolledItem(null);
    } else {
      const clamped = Math.max(1, Math.min(100, num));
      setItemRoll(clamped);
      if (treasureTable) {
        const iEntry = treasureTable.entries.find(
          e => e.label.startsWith('Item') && clamped >= e.d100Min && clamped <= e.d100Max
        );
        setLastRolledItem(iEntry || null);
      }
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="treasure-roller-modal parchment-card ornate-border" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="title-row">
            <span className="badge badge-gold"><Coins size={14} /> Espólios & Recompensas</span>
            <h2 className="modal-title">Simulador & Filtro de Tesouros</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="treasure-roller-body">
          <p className="roller-instruction">
            Selecione o <strong>Nível de Desafio (ND)</strong> da criatura ou combate e informe o valor rolado no dado percentual (D% / 01-100) para Dinheiro e Itens, ou clique em <strong>Rolar Dados 🎲</strong>:
          </p>

          {/* Seletor de ND */}
          <div className="nd-selector-wrapper">
            <span className="nd-label">Nível de Desafio (ND):</span>
            <div className="nd-buttons-grid">
              {ND_OPTIONS.map(nd => (
                <button
                  key={nd}
                  className={`nd-btn ${selectedNd === nd ? 'nd-btn-active' : ''}`}
                  onClick={() => {
                    setSelectedNd(nd);
                    if (moneyRoll !== '' && itemRoll !== '') {
                      evaluateRolls(Number(moneyRoll), Number(itemRoll));
                    }
                  }}
                >
                  ND {nd}
                </button>
              ))}
            </div>
          </div>

          {/* Seção de Rolagem / Inputs */}
          <div className="roller-controls-grid">
            <div className="roller-input-group">
              <label className="input-label">D% Rolado para Dinheiro (1-100):</label>
              <div className="input-with-button">
                <input
                  type="number"
                  min="1"
                  max="100"
                  placeholder="Ex: 85"
                  className="d100-input"
                  value={moneyRoll}
                  onChange={e => handleManualMoneyChange(e.target.value)}
                />
              </div>
            </div>

            <div className="roller-input-group">
              <label className="input-label">D% Rolado para Itens (1-100):</label>
              <div className="input-with-button">
                <input
                  type="number"
                  min="1"
                  max="100"
                  placeholder="Ex: 92"
                  className="d100-input"
                  value={itemRoll}
                  onChange={e => handleManualItemChange(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="roller-action-center">
            <button className="btn-gold btn-roll-dice" onClick={handleRollDice}>
              <Dices size={20} />
              Rolar Dados D% Automaticamente
            </button>
          </div>

          {/* Painel de Resultados */}
          <div className="treasure-results-grid">
            {/* Resultado de Dinheiro */}
            <div className="result-card parchment-card">
              <div className="result-card-header">
                <Coins size={18} className="text-gold" />
                <h4>Resultado: Dinheiro ({moneyRoll ? `${moneyRoll}%` : 'Aguardando D%'})</h4>
              </div>
              <div className="result-card-body">
                {lastRolledMoney ? (
                  <div className="result-highlight">
                    <span className="result-name">{lastRolledMoney.label.replace(/^Dinheiro\s*\([^)]+\):\s*/, '')}</span>
                    <p className="result-desc">{lastRolledMoney.description}</p>
                  </div>
                ) : (
                  <span className="text-muted">Informe ou role o D% de Dinheiro acima.</span>
                )}
              </div>
            </div>

            {/* Resultado de Itens */}
            <div className="result-card parchment-card">
              <div className="result-card-header">
                <Sparkles size={18} className="text-mana" />
                <h4>Resultado: Itens ({itemRoll ? `${itemRoll}%` : 'Aguardando D%'})</h4>
              </div>
              <div className="result-card-body">
                {lastRolledItem ? (
                  <div className="result-highlight">
                    <span className="result-name">{lastRolledItem.label.replace(/^Item\s*\([^)]+\):\s*/, '')}</span>
                    <p className="result-desc">{lastRolledItem.description}</p>
                    {lastRolledItem.itemCategory && lastRolledItem.itemCategory !== 'Nenhum' && (
                      <span className="badge badge-gold mt-2">Categoria: {lastRolledItem.itemCategory}</span>
                    )}
                  </div>
                ) : (
                  <span className="text-muted">Informe ou role o D% de Itens acima.</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
