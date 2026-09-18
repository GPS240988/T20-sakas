import React, { useState, useRef } from 'react';
import { X, Dices, Coins, Sparkles, ListOrdered, Eye, ArrowLeft, Copy, Check } from 'lucide-react';
import { ScrollToTop } from './ScrollToTop';
import { 
  evaluateMoneyRoll, 
  resolveItemChain, 
  getTreasureTableById,
  type MoneyRollResult, 
  type ItemRollResult 
} from '../utils/treasureResolver';

interface TreasureRollerProps {
  isOpen: boolean;
  onClose: () => void;
}

const ND_OPTIONS = ['1/4', '1/2', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'];

export const TreasureRoller: React.FC<TreasureRollerProps> = ({ isOpen, onClose }) => {
  const [selectedNd, setSelectedNd] = useState<string>('5');
  const [moneyRoll, setMoneyRoll] = useState<number | ''>('');
  const [itemRoll, setItemRoll] = useState<number | ''>('');
  
  const [moneyResult, setMoneyResult] = useState<MoneyRollResult | null>(null);
  const [itemResult, setItemResult] = useState<ItemRollResult | null>(null);

  // Estado para visualização do Sub-modal de Tabela Referenciada
  const [viewingTableId, setViewingTableId] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const rollerBodyRef = useRef<HTMLDivElement>(null);
  const tableBodyRef = useRef<HTMLDivElement>(null);

  if (!isOpen) return null;

  const handleCopyContent = () => {
    const lines: string[] = [];
    lines.push(`========================================`);
    lines.push(`GERADOR E SIMULADOR DE TESOUROS - ND ${selectedNd}`);
    lines.push(`========================================\n`);

    if (moneyResult) {
      lines.push(`[DINHEIRO (D% ${moneyRoll})]`);
      lines.push(`• Total: ${moneyResult.totalFormatted}`);
      lines.push(`• Faixa Sorteada: ${moneyResult.label}`);
      if (moneyResult.breakdown) lines.push(`• Cálculo: ${moneyResult.breakdown}`);
      lines.push('');
    } else {
      lines.push(`[DINHEIRO]: Nenhum sorteio realizado.\n`);
    }

    if (itemResult) {
      lines.push(`[ITEM (D% ${itemRoll})]`);
      lines.push(`• Item Sorteado: ${itemResult.finalItemName}`);
      if (itemResult.finalItemPrice) lines.push(`• Valor: ${itemResult.finalItemPrice}`);
      if (itemResult.finalItemCategory) lines.push(`• Categoria: ${itemResult.finalItemCategory}`);
      lines.push(`• Descrição / Efeito:\n${itemResult.finalItemDescription}\n`);
      if (itemResult.traceSteps && itemResult.traceSteps.length > 0) {
        lines.push(`• Passos de Sorteio:`);
        itemResult.traceSteps.forEach(s => {
          lines.push(`  Passo ${s.stepIndex}: ${s.title} (D% ${s.d100Rolled}) -> ${s.resultLabel}`);
        });
        lines.push('');
      }
    } else {
      lines.push(`[ITEM]: Nenhum sorteio realizado.\n`);
    }

    navigator.clipboard.writeText(lines.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // 1. Sorteio Exclusivo de Dinheiro
  const handleRollMoneyOnly = () => {
    const d100 = Math.floor(Math.random() * 100) + 1;
    setMoneyRoll(d100);
    const res = evaluateMoneyRoll(selectedNd, d100);
    setMoneyResult(res);
  };

  // 2. Sorteio Exclusivo de Itens
  const handleRollItemOnly = () => {
    const d100 = Math.floor(Math.random() * 100) + 1;
    setItemRoll(d100);
    const res = resolveItemChain(selectedNd, d100);
    setItemResult(res);
  };

  // 3. Sorteio de Ambos
  const handleRollBoth = () => {
    handleRollMoneyOnly();
    handleRollItemOnly();
  };

  // 4. Mudança manual de D% Dinheiro
  const handleManualMoneyChange = (val: string) => {
    const num = parseInt(val, 10);
    if (isNaN(num)) {
      setMoneyRoll('');
      setMoneyResult(null);
    } else {
      const clamped = Math.max(1, Math.min(100, num));
      setMoneyRoll(clamped);
      setMoneyResult(evaluateMoneyRoll(selectedNd, clamped));
    }
  };

  // 5. Mudança manual de D% Item
  const handleManualItemChange = (val: string) => {
    const num = parseInt(val, 10);
    if (isNaN(num)) {
      setItemRoll('');
      setItemResult(null);
    } else {
      const clamped = Math.max(1, Math.min(100, num));
      setItemRoll(clamped);
      setItemResult(resolveItemChain(selectedNd, clamped));
    }
  };

  // 6. Troca de ND (re-avalia os sorteios existentes)
  const handleNdChange = (nd: string) => {
    setSelectedNd(nd);
    if (moneyRoll !== '') {
      setMoneyResult(evaluateMoneyRoll(nd, Number(moneyRoll)));
    }
    if (itemRoll !== '') {
      setItemResult(resolveItemChain(nd, Number(itemRoll)));
    }
  };

  const tableToView = viewingTableId ? getTreasureTableById(viewingTableId) : undefined;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="treasure-roller-modal parchment-card ornate-border" onClick={e => e.stopPropagation()} style={{ maxWidth: '960px', width: '95%', maxHeight: '90vh', display: 'flex', flexDirection: 'column', overflow: 'hidden', position: 'relative' }}>
        <div className="modal-header" style={{ flexShrink: 0, background: 'var(--bg-surface-elevated)', borderBottom: '1px solid var(--border-parchment)' }}>
          <div className="title-row">
            <span className="badge badge-gold"><Coins size={14} /> Recompensas</span>
            <h2 className="modal-title" style={{ fontSize: '1.25rem' }}>Tesouros</h2>
          </div>
          <div className="modal-header-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button 
              className={`copy-btn ${copied ? 'copy-success' : ''}`}
              onClick={handleCopyContent}
              title={copied ? 'Copiado!' : 'Copiar todo o resultado do simulador'}
            >
              {copied ? <Check size={20} className="text-gold" /> : <Copy size={20} />}
            </button>
            <button className="modal-close-btn" onClick={onClose} title="Fechar simulador">
              <X size={24} />
            </button>
          </div>
        </div>

        <div className="treasure-roller-body" ref={rollerBodyRef} style={{ padding: '1rem', overflowY: 'auto', flex: 1 }}>
          <p className="roller-instruction" style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Selecione o <strong>Nível de Desafio (ND)</strong> e role individualmente para <strong>Dinheiro</strong> e <strong>Itens</strong>, ou sorteie ambos de forma automática.
          </p>

          {/* Seletor de ND */}
          <div className="nd-selector-wrapper" style={{ marginBottom: '1rem' }}>
            <span className="nd-label" style={{ fontWeight: '700', fontSize: '0.85rem', color: 'var(--text-primary)', marginBottom: '0.4rem', display: 'block' }}>
              Nível de Desafio (ND):
            </span>
            <div className="nd-buttons-grid">
              {ND_OPTIONS.map(nd => (
                <button
                  key={nd}
                  className={`nd-btn ${selectedNd === nd ? 'nd-btn-active' : ''}`}
                  onClick={() => handleNdChange(nd)}
                  style={{ minHeight: '38px' }}
                >
                  ND {nd}
                </button>
              ))}
            </div>
          </div>

          {/* Seção de Controles Individuais para Dinheiro e Itens */}
          <div className="roller-controls-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', margin: '1rem 0' }}>
            {/* Bloco 1: Dinheiro */}
            <div className="roller-input-group parchment-card" style={{ padding: '0.85rem', borderRadius: '8px', border: '1px solid var(--border-parchment)', background: 'var(--bg-surface)' }}>
              <label className="input-label" style={{ fontWeight: '700', color: 'var(--accent-gold)', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.88rem' }}>
                <Coins size={16} /> D% para Dinheiro (1-100):
              </label>
              <div className="input-with-button" style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                <input
                  type="number"
                  min="1"
                  max="100"
                  placeholder="D%"
                  className="d100-input"
                  style={{ width: '80px', textAlign: 'center', fontWeight: '700', borderRadius: '6px' }}
                  value={moneyRoll}
                  onChange={e => handleManualMoneyChange(e.target.value)}
                />
                <button 
                  className="vital-btn badge-gold" 
                  style={{ flex: 1, padding: '0.55rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', fontWeight: '700', borderRadius: '6px', cursor: 'pointer' }}
                  onClick={handleRollMoneyOnly}
                >
                  <Dices size={16} /> Rolar Dinheiro
                </button>
              </div>
            </div>

            {/* Bloco 2: Itens */}
            <div className="roller-input-group parchment-card" style={{ padding: '0.85rem', borderRadius: '8px', border: '1px solid var(--border-parchment)', background: 'var(--bg-surface)' }}>
              <label className="input-label" style={{ fontWeight: '700', color: 'var(--accent-mana)', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.88rem' }}>
                <Sparkles size={16} /> D% para Itens (1-100):
              </label>
              <div className="input-with-button" style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                <input
                  type="number"
                  min="1"
                  max="100"
                  placeholder="D%"
                  className="d100-input"
                  style={{ width: '80px', textAlign: 'center', fontWeight: '700', borderRadius: '6px' }}
                  value={itemRoll}
                  onChange={e => handleManualItemChange(e.target.value)}
                />
                <button 
                  className="vital-btn badge-mana" 
                  style={{ flex: 1, padding: '0.55rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', fontWeight: '700', borderRadius: '6px', cursor: 'pointer' }}
                  onClick={handleRollItemOnly}
                >
                  <Dices size={16} /> Rolar Item
                </button>
              </div>
            </div>
          </div>

          <div className="roller-action-center" style={{ textAlign: 'center', marginBottom: '1.2rem' }}>
            <button className="btn-gold btn-roll-dice" style={{ padding: '0.65rem 1.6rem', fontSize: '0.92rem', fontWeight: '700', borderRadius: '8px' }} onClick={handleRollBoth}>
              <Dices size={18} />
              Rolar Ambos (Dinheiro + Item)
            </button>
          </div>

          {/* Painel de Resultados */}
          <div className="treasure-results-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem' }}>
            
            {/* Resultado 1: Dinheiro */}
            <div className="result-card parchment-card ornate-border" style={{ padding: '1rem', background: 'var(--bg-surface)' }}>
              <div className="result-card-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-parchment)', paddingBottom: '0.5rem', marginBottom: '0.8rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Coins size={20} className="text-gold" />
                  <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: '700' }}>
                    Resultado: Dinheiro {moneyRoll !== '' ? `(D% ${moneyRoll})` : ''}
                  </h4>
                </div>
              </div>
              
              <div className="result-card-body">
                {moneyResult ? (
                  <div className="result-highlight">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span className="badge badge-gold" style={{ fontSize: '0.85rem', fontWeight: '700' }}>
                        ND {selectedNd}
                      </span>
                      <span style={{ fontSize: '1.15rem', fontWeight: '800', color: 'var(--accent-gold)' }}>
                        {moneyResult.totalFormatted}
                      </span>
                    </div>

                    <p className="result-desc" style={{ fontSize: '0.88rem', lineHeight: '1.4', margin: '0.4rem 0', color: 'var(--text-primary)' }}>
                      <strong>Faixa Sorteada:</strong> {moneyResult.label}
                    </p>

                    {moneyResult.breakdown && (
                      <div style={{ background: 'var(--bg-surface-muted)', padding: '0.6rem 0.8rem', borderRadius: '6px', fontSize: '0.82rem', color: 'var(--text-primary)', marginTop: '0.5rem', border: '1px solid var(--border-parchment)' }}>
                        <strong>Memória de Cálculo:</strong><br />
                        {moneyResult.breakdown}
                      </div>
                    )}

                    {/* Rastreabilidade Passo a Passo de Dinheiro */}
                    {moneyResult.traceSteps && moneyResult.traceSteps.length > 0 && (
                      <div style={{ marginTop: '0.8rem', borderTop: '1px dashed var(--border-parchment)', paddingTop: '0.6rem' }}>
                        <h5 style={{ margin: '0 0 0.5rem 0', fontSize: '0.82rem', color: 'var(--accent-gold)', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                          <ListOrdered size={14} /> Rastreabilidade da Rolagem:
                        </h5>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                          {moneyResult.traceSteps.map((step, idx) => (
                            <div 
                              key={idx} 
                              style={{ 
                                background: 'var(--bg-surface-muted)', 
                                padding: '0.45rem 0.65rem', 
                                borderRadius: '5px', 
                                fontSize: '0.78rem',
                                borderLeft: '3px solid var(--accent-gold)'
                              }}
                            >
                              <div style={{ fontWeight: '700', color: 'var(--text-primary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span>{step.title}</span>
                                {step.tableId && (
                                  <button 
                                    style={{ background: 'none', border: 'none', color: 'var(--accent-gold)', cursor: 'pointer', fontSize: '0.75rem', fontWeight: '700', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}
                                    onClick={() => setViewingTableId(step.tableId!)}
                                  >
                                    <Eye size={12} /> Ver Tabela
                                  </button>
                                )}
                              </div>
                              <div style={{ color: 'var(--text-secondary)', marginTop: '0.15rem' }}>→ {step.detail}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Riquezas sorteadas */}
                    {moneyResult.wealthItems && moneyResult.wealthItems.length > 0 && (
                      <div style={{ marginTop: '0.8rem', borderTop: '1px dashed var(--border-parchment)', paddingTop: '0.6rem' }}>
                        <h5 style={{ margin: '0 0 0.4rem 0', fontSize: '0.82rem', color: 'var(--accent-ruby)', fontWeight: '700' }}>
                          💎 Riqueza(s) Gerada(s):
                        </h5>
                        {moneyResult.wealthItems.map((w, idx) => (
                          <div key={idx} style={{ fontSize: '0.8rem', margin: '0.35rem 0', paddingLeft: '0.5rem', borderLeft: '2px solid var(--accent-gold)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <strong>{w.label}:</strong>
                              {w.tableId && (
                                <button 
                                  style={{ background: 'none', border: 'none', color: 'var(--accent-gold)', cursor: 'pointer', fontSize: '0.73rem', fontWeight: '700' }}
                                  onClick={() => setViewingTableId(w.tableId!)}
                                >
                                  🔍 Ver Tabela
                                </button>
                              )}
                            </div>
                            <div style={{ color: 'var(--text-secondary)' }}>{w.description}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <span className="text-muted" style={{ fontSize: '0.85rem' }}>
                    Selecione o ND e clique em <strong>Rolar Dinheiro</strong> ou digite o D%.
                  </span>
                )}
              </div>
            </div>

            {/* Resultado 2: Itens & Rastreabilidade de Sub-tabelas */}
            <div className="result-card parchment-card ornate-border" style={{ padding: '1rem', background: 'var(--bg-surface)' }}>
              <div className="result-card-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-parchment)', paddingBottom: '0.5rem', marginBottom: '0.8rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Sparkles size={20} className="text-mana" />
                  <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: '700' }}>
                    Resultado: Itens {itemRoll !== '' ? `(D% ${itemRoll})` : ''}
                  </h4>
                </div>
              </div>

              <div className="result-card-body">
                {itemResult ? (
                  <div className="result-highlight">
                    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem' }}>
                      <span className="badge badge-mana" style={{ fontSize: '0.92rem', fontWeight: '800' }}>
                        {itemResult.finalItemName}
                      </span>
                      {itemResult.finalItemPrice && (
                        <span className="badge badge-gold" style={{ fontSize: '0.85rem' }}>
                          {itemResult.finalItemPrice}
                        </span>
                      )}
                    </div>

                    {itemResult.finalItemCategory && (
                      <span className="badge badge-parchment" style={{ fontSize: '0.75rem', marginBottom: '0.4rem', display: 'inline-block' }}>
                        Categoria: {itemResult.finalItemCategory}
                      </span>
                    )}

                    <p className="result-desc" style={{ fontSize: '0.88rem', lineHeight: '1.45', margin: '0.5rem 0', color: 'var(--text-primary)', background: 'var(--bg-surface-elevated)', padding: '0.65rem', borderRadius: '6px', border: '1px solid var(--border-parchment)', whiteSpace: 'pre-line' }}>
                      <strong>Efeito / Regra Mecânica Completa:</strong><br />
                      {itemResult.finalItemDescription}
                    </p>

                    {/* Log de Rastreabilidade Passo a Passo */}
                    {itemResult.traceSteps && itemResult.traceSteps.length > 0 && (
                      <div style={{ marginTop: '0.8rem', borderTop: '1px dashed var(--border-parchment)', paddingTop: '0.6rem' }}>
                        <h5 style={{ margin: '0 0 0.5rem 0', fontSize: '0.82rem', color: 'var(--accent-gold)', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                          <ListOrdered size={14} /> Rastreabilidade da Rolagem (Passo a Passo):
                        </h5>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                          {itemResult.traceSteps.map((step, idx) => (
                            <div 
                              key={idx} 
                              style={{ 
                                background: 'var(--bg-surface-muted)', 
                                padding: '0.45rem 0.65rem', 
                                borderRadius: '5px', 
                                fontSize: '0.78rem',
                                borderLeft: '3px solid var(--accent-mana)'
                              }}
                            >
                              <div style={{ fontWeight: '700', color: 'var(--text-primary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span>Passo {step.stepIndex}: {step.title}</span>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                                  {step.d100Rolled !== undefined && (
                                    <span className="badge badge-parchment" style={{ fontSize: '0.7rem' }}>D% {step.d100Rolled}</span>
                                  )}
                                  {step.tableId && (
                                    <button 
                                      style={{ background: 'none', border: 'none', color: 'var(--accent-gold)', cursor: 'pointer', fontSize: '0.75rem', fontWeight: '700', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}
                                      onClick={() => setViewingTableId(step.tableId!)}
                                      title={`Visualizar ${step.tableName}`}
                                    >
                                      <Eye size={12} /> Ver Tabela
                                    </button>
                                  )}
                                </div>
                              </div>
                              <div style={{ color: 'var(--text-secondary)', marginTop: '0.15rem' }}>
                                → Sorteado: <strong>{step.resultLabel}</strong>
                              </div>
                              {step.detail && (
                                <div style={{ fontSize: '0.73rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>
                                  {step.detail}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <span className="text-muted" style={{ fontSize: '0.85rem' }}>
                    Selecione o ND e clique em <strong>Rolar Item</strong> ou digite o D%.
                  </span>
                )}
              </div>
            </div>

          </div>
        </div>

        {/* Botão Flutuante Voltar ao Topo do Simulador */}
        <ScrollToTop containerRef={rollerBodyRef} isInsideContainer title="Voltar ao início do simulador" />
      </div>

      {/* ========================================================================= */}
      {/* 🔍 SUB-MODAL: VISUALIZADOR DE TABELA REFERENCIADA (POR CIMA DO SIMULADOR) */}
      {/* ========================================================================= */}
      {tableToView && (
        <div className="modal-backdrop" style={{ zIndex: 1100, background: 'rgba(0, 0, 0, 0.65)' }} onClick={() => setViewingTableId(null)}>
          <div className="referenced-table-modal parchment-card ornate-border" onClick={e => e.stopPropagation()} style={{ maxWidth: '850px', width: '92%', maxHeight: '85vh', display: 'flex', flexDirection: 'column', overflow: 'hidden', position: 'relative', padding: '1.2rem', background: 'var(--bg-surface-elevated)' }}>
            <div className="modal-header" style={{ flexShrink: 0, display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid var(--accent-gold)', paddingBottom: '0.6rem', marginBottom: '1rem' }}>
              <div>
                <span className="badge badge-gold">Visualização de Tabela Oficial</span>
                <h3 className="modal-title" style={{ fontSize: '1.2rem', margin: '0.2rem 0 0 0' }}>{tableToView.name}</h3>
              </div>
              <button className="modal-close-btn" onClick={() => setViewingTableId(null)} title="Voltar ao sorteio">
                <X size={24} />
              </button>
            </div>

            <div className="table-modal-body" ref={tableBodyRef} style={{ overflowY: 'auto', flex: 1, paddingRight: '0.4rem' }}>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: '1.45' }}>
                {tableToView.description || tableToView.summary}
              </p>

              <div className="treasure-table-wrapper">
                <table className="treasure-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                  <thead>
                    <tr style={{ background: 'var(--bg-surface-muted)' }}>
                      <th style={{ padding: '0.5rem', border: '1px solid var(--border-parchment)', width: '90px', textAlign: 'center' }}>D% (01-100)</th>
                      <th style={{ padding: '0.5rem', border: '1px solid var(--border-parchment)', minWidth: '180px' }}>Item / Resultado</th>
                      <th style={{ padding: '0.5rem', border: '1px solid var(--border-parchment)' }}>Efeito & Descrição Mecânica</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tableToView.entries.map((entry, idx) => (
                      <tr key={idx} style={{ background: idx % 2 === 0 ? 'var(--bg-surface)' : 'var(--bg-surface-muted)' }}>
                        <td style={{ padding: '0.45rem', border: '1px solid var(--border-parchment)', fontWeight: '700', color: 'var(--accent-gold)', textAlign: 'center' }}>
                          {entry.d100Min.toString().padStart(2, '0')}-{entry.d100Max.toString().padStart(2, '0')}
                        </td>
                        <td style={{ padding: '0.45rem', border: '1px solid var(--border-parchment)', fontWeight: '700', color: 'var(--text-primary)' }}>
                          {entry.label}
                        </td>
                        <td style={{ padding: '0.45rem', border: '1px solid var(--border-parchment)', fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                          {entry.description}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="table-modal-footer" style={{ flexShrink: 0, marginTop: '1.2rem', paddingTop: '0.8rem', borderTop: '1px solid var(--border-parchment)', textAlign: 'right' }}>
              <button 
                className="vital-btn badge-gold" 
                style={{ padding: '0.5rem 1.2rem', fontSize: '0.88rem', fontWeight: '700', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}
                onClick={() => setViewingTableId(null)}
              >
                <ArrowLeft size={16} /> Voltar para o Sorteio
              </button>
            </div>

            {/* Botão Flutuante Voltar ao Topo da Tabela */}
            <ScrollToTop containerRef={tableBodyRef} isInsideContainer title="Voltar ao início da tabela" />
          </div>
        </div>
      )}
    </div>
  );
};
