import { CANONICAL_DATABASE } from '../data/database';
import type { TreasureTableEntity } from '../types/t20_schema';

export interface MoneyRollResult {
  nd: string;
  d100: number;
  label: string;
  formula: string;
  diceRolled: number[];
  diceSum: number;
  totalFormatted: string;
  breakdown: string;
  traceSteps: Array<{ title: string; detail: string; tableId?: string }>;
  wealthItems?: Array<{ label: string; description: string; tableId?: string }>;
}

export interface TraceStep {
  stepIndex: number;
  title: string;
  d100Rolled?: number;
  diceRolled?: number[];
  tableId?: string;
  tableName: string;
  resultLabel: string;
  detail?: string;
}

export interface ItemRollResult {
  nd: string;
  d100: number;
  label: string;
  finalItemName: string;
  finalItemCategory?: string;
  finalItemPrice?: string;
  finalItemDescription: string;
  traceSteps: TraceStep[];
  subItems?: Array<{ name: string; price?: string; description: string }>;
}

/**
 * Rola N dados de S lados. Retorna array com valores e soma total.
 */
function rollDice(count: number, sides: number): { dice: number[]; sum: number } {
  const dice: number[] = [];
  let sum = 0;
  for (let i = 0; i < count; i++) {
    const r = Math.floor(Math.random() * sides) + 1;
    dice.push(r);
    sum += r;
  }
  return { dice, sum };
}

/**
 * Normaliza o identificador de ND (ex: "ND 5", "5", "1/4", "1/2")
 */
function cleanNdId(nd: string): string {
  return String(nd).replace(/^ND\s*/i, '').trim().replace('/', '-');
}

/**
 * Encontra a tabela de tesouro por ID no banco canônico
 */
export function getTreasureTableById(tableId: string): TreasureTableEntity | undefined {
  return CANONICAL_DATABASE.find(
    e => e.category === 'tesouro' && e.id === tableId
  ) as TreasureTableEntity | undefined;
}

/**
 * Parse robusto para qualquer fórmula de moedas de Tormenta20,
 * lidando com pontuações de milhar ("1.000") e variações de operadores ("x", "X", "*").
 */
function parseMoneyFormula(rawFormula: string): {
  diceCount: number;
  diceSides: number;
  bonus: number;
  multiplier: number;
  currency: string;
} | null {
  if (!rawFormula) return null;

  // 1. Normalizar multiplicadores (x, X, × \u00d7, · \u00b7) -> * e pontos de milhar
  const normalized = rawFormula
    .replace(/[\u00d7\u00b7xX]/g, '*')
    .replace(/(\d+)\.(\d{3})/g, '$1$2')
    .replace(/\s+/g, ' ')
    .trim();

  // 2. Extrair a moeda (TC, TO, T$, TS)
  let currency = 'T$';
  if (/\bTC\b/i.test(normalized) || /cobre/i.test(normalized)) {
    currency = 'TC';
  } else if (/\bTO\b/i.test(normalized) || /ouro/i.test(normalized)) {
    currency = 'TO';
  } else {
    currency = 'T$';
  }

  // 3. Capturar expressão de dados (ex: 1d8, 2d6+1, 4d12) e multiplicador
  const match = normalized.match(/\(?(\d+)d(\d+)(?:\s*\+\s*(\d+))?\)?(?:\s*\*\s*(\d+))?/i);
  if (!match) return null;

  const diceCount = parseInt(match[1], 10);
  const diceSides = parseInt(match[2], 10);
  const bonus = match[3] ? parseInt(match[3], 10) : 0;
  const multiplier = match[4] ? parseInt(match[4], 10) : 1;

  return { diceCount, diceSides, bonus, multiplier, currency };
}

/**
 * Avalia o sorteio de dinheiro para um ND e um D% rolado, garantindo parse correto de número e fórmula.
 */
export function evaluateMoneyRoll(nd: string, rawD100: number | string): MoneyRollResult {
  const numD100 = Math.max(1, Math.min(100, typeof rawD100 === 'number' ? rawD100 : parseInt(String(rawD100), 10) || 1));
  const cleanNd = cleanNdId(nd);
  const tableId = `tesouro-tabela-nd-${cleanNd}`;
  const table = getTreasureTableById(tableId);

  const traceSteps: Array<{ title: string; detail: string; tableId?: string }> = [];

  if (!table) {
    return {
      nd,
      d100: numD100,
      label: 'ND Inválido',
      formula: '',
      diceRolled: [],
      diceSum: 0,
      totalFormatted: 'T$ 0',
      breakdown: 'Tabela de ND não encontrada.',
      traceSteps: [{ title: 'Erro', detail: `Tabela de ND ${nd} não encontrada no banco.` }]
    };
  }

  // Busca a entrada de dinheiro na tabela de ND com comparação numérica rigorosa
  const entry = table.entries.find(
    e => e.entryType === 'money' && numD100 >= e.d100Min && numD100 <= e.d100Max
  ) || table.entries.find(e => e.entryType === 'money') || table.entries[0];

  const label = entry ? entry.label : 'Nenhum';
  const formula = entry?.moneyFormula || label;

  traceSteps.push({
    title: `Passo 1: Tabela 8-1 ND ${nd} (Coluna Dinheiro)`,
    detail: `D% rolado: ${numD100} (Faixa ${entry?.d100Min.toString().padStart(2, '0')}-${entry?.d100Max.toString().padStart(2, '0')}%) -> Sorteado: "${label}"`,
    tableId: table.id
  });

  if (label === 'Nenhum' || formula === '0 T$' || /^0\s*T\$$/i.test(formula.trim())) {
    return {
      nd,
      d100: numD100,
      label,
      formula: 'Nenhum',
      diceRolled: [],
      diceSum: 0,
      totalFormatted: 'T$ 0',
      breakdown: 'Nenhum dinheiro sorteado para esta faixa de D%.',
      traceSteps
    };
  }

  // 1. Caso de Riquezas (Tabela 8-2A, 8-2B, 8-2C)
  if (label.toLowerCase().includes('riqueza')) {
    let count = 1;
    let rollTrace = '1 riqueza';

    // Determina a quantidade de riquezas (1, 1d3, 1d3+1, 1d4+1, etc.)
    if (label.includes('1d3+1')) {
      const { dice, sum } = rollDice(1, 3);
      count = sum + 1;
      rollTrace = `Rolagem (1d3+1) riquezas: dado [${dice.join(', ')}] + 1 = ${count} riqueza(s)`;
    } else if (label.includes('1d4+1')) {
      const { dice, sum } = rollDice(1, 4);
      count = sum + 1;
      rollTrace = `Rolagem (1d4+1) riquezas: dado [${dice.join(', ')}] + 1 = ${count} riqueza(s)`;
    } else if (label.includes('1d3')) {
      const { dice, sum } = rollDice(1, 3);
      count = sum;
      rollTrace = `Rolagem 1d3 riquezas: dado [${dice.join(', ')}] = ${count} riqueza(s)`;
    }

    let subTableId = 'tabela-8-2a-riqueza-menor';
    let subTableName = 'Tabela 8-2A: Riquezas Menores';

    if (label.toLowerCase().includes('média') || label.toLowerCase().includes('media')) {
      subTableId = 'tabela-8-2b-riqueza-media';
      subTableName = 'Tabela 8-2B: Riquezas Médias';
    } else if (label.toLowerCase().includes('maior')) {
      subTableId = 'tabela-8-2c-riqueza-maior';
      subTableName = 'Tabela 8-2C: Riquezas Maiores';
    }

    traceSteps.push({
      title: `Passo 2: Determinar Quantidade de Riquezas`,
      detail: `${rollTrace} a serem sorteadas na ${subTableName}`,
      tableId: subTableId
    });

    const wealthTable = getTreasureTableById(subTableId);
    const wealthItems: Array<{ label: string; description: string; tableId?: string }> = [];

    if (wealthTable) {
      for (let i = 1; i <= count; i++) {
        const subD100 = Math.floor(Math.random() * 100) + 1;
        const subEntry = wealthTable.entries.find(e => subD100 >= e.d100Min && subD100 <= e.d100Max);
        if (subEntry) {
          wealthItems.push({
            label: subEntry.label,
            description: subEntry.description,
            tableId: subTableId
          });
          traceSteps.push({
            title: `Passo ${2 + i}: Riqueza ${i} de ${count} (${subTableName})`,
            detail: `D% rolado: ${subD100} -> Item: ${subEntry.label} (${subEntry.description})`,
            tableId: subTableId
          });
        }
      }
    }

    return {
      nd,
      d100: numD100,
      label,
      formula: label,
      diceRolled: [count],
      diceSum: count,
      totalFormatted: `${count}x Riqueza(s) (${subTableName.replace('Tabela 8-2: ', '')})`,
      breakdown: `Sorteado ${count} riqueza(s) individualmente na ${subTableName}.`,
      traceSteps,
      wealthItems
    };
  }

  // 2. Parse de fórmulas de dados de moedas (ex: 2d10 x 1.000 T$, 3d8 * 10 T$, 1d4 * 100 T$, (2d6+1) * 100 T$, 1d8 * 10 TO)
  const parsed = parseMoneyFormula(formula) || parseMoneyFormula(label);

  if (parsed) {
    const { diceCount, diceSides, bonus, multiplier, currency } = parsed;
    const { dice, sum } = rollDice(diceCount, diceSides);
    const sumWithBonus = sum + bonus;
    const totalRaw = sumWithBonus * multiplier;

    let totalFormatted = `${currency} ${totalRaw.toLocaleString('pt-BR')}`;
    let valueInT = totalRaw;

    if (currency === 'TC') {
      valueInT = totalRaw / 10;
      totalFormatted = `${totalRaw.toLocaleString('pt-BR')} TC (Tibares de Cobre) = T$ ${valueInT.toLocaleString('pt-BR')}`;
    } else if (currency === 'TO') {
      valueInT = totalRaw * 10;
      totalFormatted = `${totalRaw.toLocaleString('pt-BR')} TO (Tibares de Ouro) = T$ ${valueInT.toLocaleString('pt-BR')}`;
    }

    const bonusStr = bonus > 0 ? ` + ${bonus}` : '';
    const multStr = multiplier > 1 ? ` x ${multiplier.toLocaleString('pt-BR')}` : '';

    traceSteps.push({
      title: `Passo 2: Rolagem dos dados da fórmula (${diceCount}d${diceSides}${bonusStr}${multStr} ${currency})`,
      detail: `Dados rolados [${diceCount}d${diceSides}]: [${dice.join(', ')}] = ${sum}${bonusStr ? ` (+${bonus} = ${sumWithBonus})` : ''}`
    });

    traceSteps.push({
      title: `Passo 3: Cálculo e Totalização`,
      detail: `Cálculo: (${sumWithBonus})${multStr} = ${totalFormatted}`
    });

    const breakdown = `Fórmula: ${diceCount}d${diceSides}${bonusStr}${multStr} ${currency} | Dados rolados: [${dice.join(', ')}] = ${sum}${bonusStr ? ` (+${bonus} = ${sumWithBonus})` : ''}`;

    return {
      nd,
      d100: numD100,
      label,
      formula,
      diceRolled: dice,
      diceSum: sumWithBonus,
      totalFormatted,
      breakdown,
      traceSteps
    };
  }

  return {
    nd,
    d100: numD100,
    label,
    formula,
    diceRolled: [],
    diceSum: 0,
    totalFormatted: label,
    breakdown: `Valor sorteado conforme a tabela: ${label}`,
    traceSteps
  };
}

/**
 * Resolução encadeada de sorteio de ITENS com implementação direta das regras oficiais da pág. 329:
 * 1. Diverso -> Tabela 8-3
 * 2. Equipamento -> 1d6 (1-3 Arma 8-4A, 4-5 Armadura 8-4B, 6 Esotérico 8-4C)
 * 3. Superior -> 1d6 para tipo, depois 1d100 na Tabela 8-5 para cada melhoria
 * 4. Poções -> 1d100 na Tabela 8-12 (ou rolagem de quantidade se 1d3, 1d4+1, 1d6+1)
 * 5. Mágico -> 1d6 para tipo (1-2 Arma 8-8/8-9, 3 Armadura 8-10/8-11, 4-6 Acessório 8-13/8-14/8-15)
 */
export function resolveItemChain(nd: string, rawD100: number | string): ItemRollResult {
  const numD100 = Math.max(1, Math.min(100, typeof rawD100 === 'number' ? rawD100 : parseInt(String(rawD100), 10) || 1));
  const cleanNd = cleanNdId(nd);
  const tableId = `tesouro-tabela-nd-${cleanNd}`;
  const table = getTreasureTableById(tableId);

  const traceSteps: TraceStep[] = [];

  if (!table) {
    return {
      nd,
      d100: numD100,
      label: 'ND Inválido',
      finalItemName: 'Nenhum',
      finalItemDescription: 'Tabela de ND não encontrada.',
      traceSteps: []
    };
  }

  // Busca entrada de item com comparação numérica estrita
  const entry = table.entries.find(
    e => e.entryType === 'item' && numD100 >= e.d100Min && numD100 <= e.d100Max
  ) || table.entries.find(e => e.entryType === 'item') || table.entries[0];

  const label = entry ? entry.label : 'Nenhum';

  traceSteps.push({
    stepIndex: 1,
    title: `Tabela 8-1: Tesouro por ND (${table.threatLevelLabel})`,
    d100Rolled: numD100,
    tableId: table.id,
    tableName: `ND ${nd}`,
    resultLabel: label,
    detail: entry?.description || `D% rolado ${numD100}: ${label}`
  });

  if (label === 'Nenhum' || label.startsWith('Nenhum')) {
    return {
      nd,
      d100: numD100,
      label,
      finalItemName: 'Nenhum Item Sorteado',
      finalItemCategory: 'Nenhum',
      finalItemDescription: 'A rolagem nesta faixa de D% não concedeu nenhum item de valor.',
      traceSteps
    };
  }

  // --------------------------------------------------------------------------
  // A. ITEM DIVERSO (Tabela 8-3, pág. 330)
  // --------------------------------------------------------------------------
  if (label.toLowerCase().includes('diverso')) {
    const subD100 = Math.floor(Math.random() * 100) + 1;
    const subTable = getTreasureTableById('tabela-8-3-itens-diversos');
    const subEntry = subTable?.entries.find(e => subD100 >= e.d100Min && subD100 <= e.d100Max);

    traceSteps.push({
      stepIndex: 2,
      title: 'Tabela 8-3: Itens Diversos',
      d100Rolled: subD100,
      tableId: 'tabela-8-3-itens-diversos',
      tableName: 'Tabela 8-3: Itens Diversos',
      resultLabel: subEntry?.label || 'Item Diverso',
      detail: subEntry?.description
    });

    return {
      nd,
      d100: numD100,
      label,
      finalItemName: subEntry?.label || label,
      finalItemCategory: 'Item Diverso',
      finalItemPrice: subEntry?.description?.match(/T\$\s*[\d.]+/)?.[0] || 'Varia',
      finalItemDescription: subEntry?.description || `Item diverso sorteado: ${subEntry?.label}`,
      traceSteps
    };
  }

  // --------------------------------------------------------------------------
  // B. EQUIPAMENTO COMUM (Tabela 8-4, pág. 331)
  // Regra Oficial: Role 1d6: 1-3 arma, 4-5 armadura ou escudo, 6 esotérico.
  // --------------------------------------------------------------------------
  if (label.toLowerCase().includes('equipamento comum') || label.toLowerCase().includes('equipamento')) {
    const { dice } = rollDice(1, 6);
    const d = dice[0];
    const chosenCategory = d <= 3 ? 1 : d <= 5 ? 2 : 3;
    const catName = chosenCategory === 1 ? 'Arma' : chosenCategory === 2 ? 'Armadura / Escudo' : 'Item Esotérico';

    const eqTableId = chosenCategory === 1 ? 'tabela-8-4a-equipamento-armas'
      : chosenCategory === 2 ? 'tabela-8-4b-equipamento-armaduras'
      : 'tabela-8-4c-equipamento-esotericos';
    
    const eqTable = getTreasureTableById(eqTableId);
    const subD100 = Math.floor(Math.random() * 100) + 1;
    const subEntry = eqTable?.entries.find(e => subD100 >= e.d100Min && subD100 <= e.d100Max);

    traceSteps.push({
      stepIndex: 2,
      title: `Tipo de Equipamento (Rolagem 1d6: [${d}] -> ${catName})`,
      d100Rolled: subD100,
      tableId: eqTableId,
      tableName: eqTable?.name || 'Equipamentos',
      resultLabel: subEntry?.label || 'Equipamento Sorteado',
      detail: `Sorteado na ${eqTable?.name}: ${subEntry?.label}. ${subEntry?.description || ''}`
    });

    return {
      nd,
      d100: numD100,
      label,
      finalItemName: subEntry?.label || label,
      finalItemCategory: `Equipamento (${catName})`,
      finalItemPrice: subEntry?.description?.match(/T\$\s*[\d.]+/)?.[0] || 'T$ 10',
      finalItemDescription: subEntry?.description || `Equipamento comum sorteado: ${subEntry?.label}`,
      traceSteps
    };
  }

  // --------------------------------------------------------------------------
  // C. ITEM SUPERIOR (Tabela 8-5, pág. 332)
  // Regra Oficial: Role 1d6 para tipo (1-3 arma, 4-5 armadura, 6 esotérico).
  // Para cada melhoria (1 a 4), role na Tabela 8-5 correspondente.
  // --------------------------------------------------------------------------
  if (label.toLowerCase().includes('superior')) {
    const improvementsCount = label.includes('4 melhorias') ? 4
      : label.includes('3 melhorias') ? 3
      : label.includes('2 melhorias') ? 2
      : 1;

    const { dice } = rollDice(1, 6);
    const d = dice[0];
    const chosenCategory = d <= 3 ? 1 : d <= 5 ? 2 : 3;
    const catName = chosenCategory === 1 ? 'Arma Superior' : chosenCategory === 2 ? 'Armadura/Escudo Superior' : 'Esotérico Superior';

    const supTableId = chosenCategory === 1 ? 'tabela-8-5a-itens-superiores-armas'
      : chosenCategory === 2 ? 'tabela-8-5b-itens-superiores-armaduras'
      : 'tabela-8-5c-itens-superiores-esotericos';
    
    const supTable = getTreasureTableById(supTableId);

    traceSteps.push({
      stepIndex: 2,
      title: `Tipo de Item Superior (Rolagem 1d6: [${d}] -> ${catName})`,
      tableId: supTableId,
      tableName: supTable?.name || 'Tabela 8-5',
      resultLabel: `${catName} com ${improvementsCount} melhoria(s)`,
      detail: `Será(ão) realizada(s) ${improvementsCount} rolagem(ns) na ${supTable?.name}`
    });

    const mods: string[] = [];
    const modDescs: string[] = [];

    for (let i = 1; i <= improvementsCount; i++) {
      const subD100 = Math.floor(Math.random() * 100) + 1;
      const subEntry = supTable?.entries.find(e => subD100 >= e.d100Min && subD100 <= e.d100Max);
      if (subEntry) {
        mods.push(subEntry.label);
        modDescs.push(`Melhoria ${i} (${subEntry.label}): ${subEntry.description}`);
        traceSteps.push({
          stepIndex: 2 + i,
          title: `Melhoria ${i} de ${improvementsCount} (${supTable?.name})`,
          d100Rolled: subD100,
          tableId: supTableId,
          tableName: supTable?.name || 'Tabela 8-5',
          resultLabel: subEntry.label,
          detail: subEntry.description
        });
      }
    }

    return {
      nd,
      d100: numD100,
      label,
      finalItemName: `${catName} (${mods.join(' + ')})`,
      finalItemCategory: `Item Superior (${catName})`,
      finalItemDescription: `Item Superior com ${improvementsCount} melhoria(s):\n` + modDescs.join('\n'),
      traceSteps
    };
  }

  // --------------------------------------------------------------------------
  // D. POÇÕES & PREPARADOS (Tabela 8-12, pág. 341)
  // Regra Oficial: Se a faixa indicar quantidade (1d3, 1d4+1, 1d6+1), rola a quantidade.
  // Depois rola d100 na Tabela 8-12 para cada poção.
  // --------------------------------------------------------------------------
  if (label.toLowerCase().includes('poção') || label.toLowerCase().includes('poções')) {
    let count = 1;
    let countRollText = '1 poção';

    if (label.includes('1d3')) {
      const { dice, sum } = rollDice(1, 3);
      count = sum;
      countRollText = `1d3 poções -> [${dice.join(', ')}] = ${count} poção(ões)`;
    } else if (label.includes('1d4+1')) {
      const { dice, sum } = rollDice(1, 4);
      count = sum + 1;
      countRollText = `(1d4+1) poções -> [${dice.join(', ')}] + 1 = ${count} poção(ões)`;
    } else if (label.includes('1d6+1')) {
      const { dice, sum } = rollDice(1, 6);
      count = sum + 1;
      countRollText = `(1d6+1) poções -> [${dice.join(', ')}] + 1 = ${count} poção(ões)`;
    }

    traceSteps.push({
      stepIndex: 2,
      title: `Determinar Quantidade de Poções`,
      tableId: 'tabela-8-12-pocoes',
      tableName: 'Tabela 8-12: Poções',
      resultLabel: countRollText,
      detail: `Sorteando ${count} poção(ões) na Tabela 8-12`
    });

    const pocoeTable = getTreasureTableById('tabela-8-12-pocoes');
    const subItems: Array<{ name: string; price?: string; description: string }> = [];

    for (let i = 1; i <= count; i++) {
      const subD100 = Math.floor(Math.random() * 100) + 1;
      const pocoeEntry = pocoeTable?.entries.find(e => subD100 >= e.d100Min && subD100 <= e.d100Max);

      const pName = pocoeEntry?.label || 'Poção';
      const pPrice = pocoeEntry?.description || 'T$ 30';

      subItems.push({
        name: pName,
        price: pPrice,
        description: `Poção ou óleo alquímico: ${pName}. Preço oficial: ${pPrice}.`
      });

      traceSteps.push({
        stepIndex: 2 + i,
        title: `Poção ${i} de ${count} (Tabela 8-12)`,
        d100Rolled: subD100,
        tableId: 'tabela-8-12-pocoes',
        tableName: 'Tabela 8-12: Poções',
        resultLabel: pName,
        detail: `Preço: ${pPrice}`
      });
    }

    const namesJoined = subItems.map(s => s.name).join(', ');

    return {
      nd,
      d100: numD100,
      label,
      finalItemName: `${count}x Poção(ões): ${namesJoined}`,
      finalItemCategory: 'Poções & Alquimias',
      finalItemDescription: `Poção(ões) sorteada(s) na Tabela 8-12:\n` +
        subItems.map((s, idx) => `${idx + 1}. ${s.name} (${s.price})`).join('\n'),
      traceSteps,
      subItems
    };
  }

  // --------------------------------------------------------------------------
  // E. ITEM MÁGICO (Tabelas 8-8 a 8-15, págs. 336-342)
  // Regra Oficial: Role 1d6 para tipo: 1-2 Arma Mágica, 3 Armadura/Escudo Mágico, 4-6 Acessório Mágico.
  // --------------------------------------------------------------------------
  if (label.toLowerCase().includes('mágico') || label.toLowerCase().includes('magico')) {
    const isMedium = label.toLowerCase().includes('médio') || label.toLowerCase().includes('medio');
    const isMajor = label.toLowerCase().includes('maior');
    
    const { dice } = rollDice(1, 6);
    const d = dice[0];
    const chosenCategory = d <= 2 ? 1 : d === 3 ? 2 : 3;
    const catName = chosenCategory === 1 ? 'Arma Mágica' : chosenCategory === 2 ? 'Armadura / Escudo Mágico' : 'Acessório Mágico';

    let magicTableId = 'tabela-8-8-armas-magicas';

    if (chosenCategory === 1) {
      magicTableId = 'tabela-8-8-armas-magicas';
    } else if (chosenCategory === 2) {
      magicTableId = 'tabela-8-10-armaduras-escudos-magicos';
    } else {
      magicTableId = isMajor ? 'tabela-8-15-acessorios-maiores'
        : isMedium ? 'tabela-8-14-acessorios-medios'
        : 'tabela-8-13-acessorios-menores';
    }

    const magTable = getTreasureTableById(magicTableId);
    const subD100 = Math.floor(Math.random() * 100) + 1;
    const subEntry = magTable?.entries.find(e => subD100 >= e.d100Min && subD100 <= e.d100Max);

    traceSteps.push({
      stepIndex: 2,
      title: `Tipo de Item Mágico (Rolagem 1d6: [${d}] -> ${catName})`,
      d100Rolled: subD100,
      tableId: magicTableId,
      tableName: magTable?.name || 'Itens Mágicos',
      resultLabel: subEntry?.label || 'Item Mágico Sorteado',
      detail: subEntry?.description
    });

    return {
      nd,
      d100: numD100,
      label,
      finalItemName: subEntry?.label || `Item Mágico (${label})`,
      finalItemCategory: `Item Mágico (${catName})`,
      finalItemPrice: subEntry?.description?.match(/T\$\s*[\d.]+/)?.[0] || 'Item Mágico Oficial',
      finalItemDescription: subEntry?.description || `Item mágico sorteado na ${magTable?.name}: ${subEntry?.label}`,
      traceSteps
    };
  }

  // Fallback genérico
  return {
    nd,
    d100: numD100,
    label,
    finalItemName: label,
    finalItemCategory: 'Geral',
    finalItemDescription: entry?.description || `Item sorteado conforme a Tabela de ND ${nd}: ${label}`,
    traceSteps
  };
}
