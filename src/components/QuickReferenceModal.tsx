import React, { useState, useMemo, useRef } from 'react';
import { 
  X, 
  Swords, 
  Activity, 
  BookOpen, 
  Search, 
  Copy, 
  Check, 
  ChevronDown, 
  ChevronUp, 
  ShieldAlert, 
  Zap, 
  HelpCircle,
  Moon,
  Sparkles,
  Layers
} from 'lucide-react';
import { ScrollToTop } from './ScrollToTop';

// ============================================================================
// Tipagens e Dados Canônicos — Tormenta20 (Jogo do Ano)
// TEXTO 100% CANÔNICO E VERBATIM CONFORME PUBLICAÇÃO OFICIAL
// ============================================================================

export interface QuickReferenceModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialTab?: 'manobras' | 'condicoes' | 'tabela';
}

export interface ManeuverCanonical {
  id: string;
  name: string;
  actionType: 'Ação Padrão';
  opposedTest: string;
  description: string;
  page: string;
  typeNote?: string;
  relatedConditions?: string[];
}

export interface ActionCanonical {
  name: string;
  type: 'Ação Padrão' | 'Ação de Movimento' | 'Ação Completa' | 'Ação Livre' | 'Reação';
  page: string;
  description: string;
  examples: string;
}

export interface ConditionCanonical {
  name: string;
  type?: 'Mental' | 'Medo' | 'Movimento' | 'Sentidos' | 'Metabolismo' | 'Metamorfose' | 'Cansaço' | 'Veneno' | null;
  description: string;
  page: string;
}

export const CANONICAL_ACTIONS: ActionCanonical[] = [
  {
    name: 'Ação Padrão',
    type: 'Ação Padrão',
    page: '233',
    description: 'Uma ação padrão representa a coisa mais importante que você faz em seu turno. Atacar com uma arma ou lançar uma magia comum são os exemplos mais típicos de ações padrão.',
    examples: 'Agredir (ataque corpo a corpo ou à distância), Lançar Magia, Usar Habilidade ou Item, Manobras de Combate.'
  },
  {
    name: 'Ação de Movimento',
    type: 'Ação de Movimento',
    page: '234',
    description: 'Uma ação de movimento representa deslocamento físico ou manipulação rápida de objetos. Exemplos: andar até o seu deslocamento, sacar ou guardar uma arma, levantar-se do chão, abrir uma porta não trancada.',
    examples: 'Movimentar-se (até seu deslocamento), Sacar ou guardar item/arma, Levantar-se do chão, Abrir porta.'
  },
  {
    name: 'Ação Completa',
    type: 'Ação Completa',
    page: '235',
    description: 'Uma ação completa consome todo o seu esforço e tempo do turno. Se fizer uma ação completa, você não pode fazer nenhuma ação padrão nem de movimento. Exemplos: Investida, Golpe de Misericórdia, Correr.',
    examples: 'Investida (+2 no teste de ataque, –2 na Defesa), Golpe de Misericórdia (em alvo indefeso), Correr (4x deslocamento).'
  },
  {
    name: 'Ação Livre',
    type: 'Ação Livre',
    page: '235',
    description: 'Ações livres consomem pouquíssimo tempo e esforço. Você pode realizar qualquer quantidade razoável de ações livres por turno, a critério do mestre.',
    examples: 'Falar uma frase curta, Soltar um item empunhado, Desativar uma habilidade livre.'
  },
  {
    name: 'Reação',
    type: 'Reação',
    page: '235',
    description: 'Uma reação é uma resposta instantânea a um gatilho específico, que pode acontecer fora do seu turno. Você só pode reagir se não estiver indefeso ou sob efeito que impeça ações.',
    examples: 'Teste de Reflexos contra uma bola de fogo, Teste de Percepção contra Furtividade, Habilidades reativas.'
  }
];

export const CANONICAL_MANEUVERS: ManeuverCanonical[] = [
  {
    id: 'manobra-agarrar',
    name: 'Agarrar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Luta (ataque corpo a corpo) oposto pelo teste de Luta do alvo.',
    description: 'Você usa uma mão livre para segurar o alvo. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, o alvo fica agarrado. Um personagem agarrado fica desprevenido e imóvel, sofre –2 em testes de ataque e só pode atacar com armas leves. Para se soltar, a criatura agarrada precisa gastar uma ação padrão e passar em um teste de Luta ou Acrobacia oposto ao seu teste de Luta. Manter a manobra nas rodadas seguintes exige gastar uma ação padrão e passar em um novo teste de Luta oposto.',
    page: '238',
    relatedConditions: ['Agarrado', 'Desprevenido', 'Imóvel']
  },
  {
    id: 'manobra-atropelar',
    name: 'Atropelar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo.',
    description: 'Você avança contra o alvo montado ou correndo. Faça um teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo. Se vencer, você derruba o alvo e pode continuar seu movimento até o limite do seu deslocamento, inclusive passando pelo espaço ocupado por ele. Se perder, você é impedido de avançar e seu movimento termina.',
    page: '239',
    relatedConditions: ['Caído']
  },
  {
    id: 'manobra-derrubar',
    name: 'Derrubar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo.',
    description: 'Você faz uma rasteira ou golpe corporal para fazer o alvo cair. Faça um teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo. Se você vencer, o alvo cai no chão e fica caído.',
    page: '239',
    relatedConditions: ['Caído']
  },
  {
    id: 'manobra-desarmar',
    name: 'Desarmar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Luta oposto pelo teste de Luta do alvo.',
    description: 'Você atinge a arma ou item empunhado pelo alvo para fazê-lo soltar o objeto. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, a arma ou item cai no chão no mesmo quadrado do alvo. Se você tiver uma mão livre e vencer por 5 ou mais, pode ficar com o item para si.',
    page: '239'
  },
  {
    id: 'manobra-empurrar',
    name: 'Empurrar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Luta oposto pelo teste de Atletismo ou Luta do alvo.',
    description: 'Você empurra o alvo para afastá-lo. Faça um teste de Luta oposto pelo teste de Atletismo ou Luta do alvo. Se vencer, você empurra o alvo 1,5m mais 1,5m para cada 5 pontos de diferença no teste. Você pode avançar junto com o alvo para empurrá-lo ainda mais longe.',
    page: '239'
  },
  {
    id: 'manobra-fintar',
    name: 'Fintar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Enganação oposto pelo teste de Percepção do alvo.',
    description: 'Você faz um movimento falso para confundir o oponente. Faça um teste de Enganação oposto pelo teste de Percepção do alvo. Se vencer, o alvo fica desprevenido contra o seu próximo ataque até o final do seu próximo turno.',
    page: '239',
    relatedConditions: ['Desprevenido']
  },
  {
    id: 'manobra-quebrar',
    name: 'Quebrar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Luta oposto pelo teste de Luta do alvo empunhando o item.',
    description: 'Você atinge um item que o alvo está empunhando ou vestindo para danificá-lo. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, causa o dano do seu ataque diretamente no item. Veja as regras de quebrando objetos na página 242.',
    page: '239'
  }
];

export const CANONICAL_SIZE_MODIFIERS = [
  { size: 'Minúsculo', mod: '–5' },
  { size: 'Pequeno', mod: '–2' },
  { size: 'Médio', mod: '+0' },
  { size: 'Grande', mod: '+2' },
  { size: 'Enorme', mod: '+5' },
  { size: 'Colossal', mod: '+10' }
];

export const CANONICAL_CONDITIONS: ConditionCanonical[] = [
  {
    name: 'Abalado',
    type: 'Medo',
    description: 'O personagem sofre –2 em testes de perícia. Se ficar abalado novamente, em vez disso fica apavorado.',
    page: '394'
  },
  {
    name: 'Agarrado',
    type: 'Movimento',
    description: 'O personagem fica desprevenido e imóvel, sofre –2 em testes de ataque e só pode atacar com armas leves. Ataques à distância contra um alvo envolvido em uma manobra agarrar têm 50% de chance de acertar o alvo errado.',
    page: '394'
  },
  {
    name: 'Alquebrado',
    type: 'Mental',
    description: 'O custo em pontos de mana das habilidades do personagem aumenta em +1.',
    page: '394'
  },
  {
    name: 'Apavorado',
    type: 'Medo',
    description: 'O personagem sofre –5 em testes de perícia e não pode se aproximar voluntariamente da fonte do medo.',
    page: '394'
  },
  {
    name: 'Atordoado',
    type: 'Mental',
    description: 'O personagem fica desprevenido e não pode fazer ações.',
    page: '394'
  },
  {
    name: 'Caído',
    type: null,
    description: 'O personagem sofre –5 na Defesa contra ataques corpo a corpo e recebe +5 na Defesa contra ataques à distância (cumulativos com outras condições). Além disso, sofre –5 em ataques corpo a corpo e seu deslocamento é reduzido a 1,5m.',
    page: '394'
  },
  {
    name: 'Cego',
    type: 'Sentidos',
    description: 'O personagem fica desprevenido e lento, não pode fazer testes de Percepção para observar e sofre –5 em testes de perícias baseadas em Força ou Destreza. Todos os alvos de seus ataques recebem camuflagem total. Você é considerado cego enquanto estiver em uma área de escuridão total, a menos que algo lhe permita perceber no escuro.',
    page: '394'
  },
  {
    name: 'Confuso',
    type: 'Mental',
    description: 'O personagem comporta-se de modo aleatório. Role 1d6 no início de seus turnos: 1) Movimenta-se em uma direção escolhida por uma rolagem de 1d8; 2-3) Não pode fazer ações, e fica balbuciando incoerentemente; 4-5) Usa a arma que estiver empunhando para atacar a criatura mais próxima, ou a si mesmo se estiver sozinho (nesse caso, apenas role o dano); 6) A condição termina e pode agir normalmente.',
    page: '394'
  },
  {
    name: 'Debilitado',
    type: null,
    description: 'O personagem sofre –5 em testes de Força, Destreza e Constituição e de perícias baseadas nesses atributos. Se o personagem ficar debilitado novamente, em vez disso fica inconsciente.',
    page: '394'
  },
  {
    name: 'Desprevenido',
    type: null,
    description: 'O personagem sofre –5 na Defesa e em Reflexos. Você fica desprevenido contra inimigos que não possa perceber.',
    page: '394'
  },
  {
    name: 'Doente',
    type: 'Metabolismo',
    description: 'Sob efeito de uma doença.',
    page: '394'
  },
  {
    name: 'Em Chamas',
    type: null,
    description: 'O personagem está pegando fogo. No início de seus turnos, sofre 1d6 pontos de dano de fogo. O personagem pode gastar uma ação padrão para apagar o fogo com as mãos. Imersão em água também apaga as chamas.',
    page: '394'
  },
  {
    name: 'Enfeitiçado',
    type: 'Mental',
    description: 'O personagem se torna prestativo em relação à fonte da condição. Ele não fica sob controle da fonte, mas percebe suas palavras e ações da maneira mais favorável possível. A fonte da condição recebe +10 em testes de Diplomacia com o personagem.',
    page: '394'
  },
  {
    name: 'Enjoado',
    type: 'Metabolismo',
    description: 'O personagem só pode realizar uma ação padrão ou de movimento (não ambas) por rodada. Ele pode gastar uma ação padrão para fazer uma investida, mas pode avançar no máximo seu deslocamento (e não o dobro).',
    page: '394'
  },
  {
    name: 'Enredado',
    type: 'Movimento',
    description: 'O personagem fica lento, vulnerável e sofre –2 em testes de ataque.',
    page: '395'
  },
  {
    name: 'Envenenado',
    type: 'Veneno',
    description: 'O efeito desta condição varia de acordo com o veneno. Pode ser perda de vida recorrente ou outra condição (como fraco ou enjoado). Perda de vida recorrente por venenos é cumulativa.',
    page: '395'
  },
  {
    name: 'Esmorecido',
    type: 'Mental',
    description: 'O personagem sofre –5 em testes de Inteligência, Sabedoria e Carisma e de perícias baseadas nesses atributos.',
    page: '395'
  },
  {
    name: 'Exausto',
    type: 'Cansaço',
    description: 'O personagem fica debilitado, lento e vulnerável. Se ficar exausto novamente, em vez disso fica inconsciente.',
    page: '395'
  },
  {
    name: 'Fascinado',
    type: 'Mental',
    description: 'Com a atenção presa em alguma coisa. O personagem sofre –5 em Percepção e não pode fazer ações, exceto observar aquilo que o fascinou. Esta condição é anulada por ações hostis contra o personagem ou se o que o fascinou não estiver mais visível. Balançar uma criatura fascinada para tirá-la desse estado gasta uma ação padrão.',
    page: '395'
  },
  {
    name: 'Fatigado',
    type: 'Cansaço',
    description: 'O personagem fica fraco e vulnerável. Se ficar fatigado novamente, em vez disso fica exausto.',
    page: '395'
  },
  {
    name: 'Fraco',
    type: null,
    description: 'O personagem sofre –2 em testes de Força, Destreza e Constituição e de perícias baseadas nesses atributos. Se ficar fraco novamente, em vez disso fica debilitado.',
    page: '395'
  },
  {
    name: 'Frustrado',
    type: 'Mental',
    description: 'O personagem sofre –2 em testes de Inteligência, Sabedoria e Carisma e de perícias baseadas nesses atributos. Se ficar frustrado novamente, em vez disso fica esmorecido.',
    page: '395'
  },
  {
    name: 'Imóvel',
    type: 'Movimento',
    description: 'Todas as formas de deslocamento do personagem são reduzidas a 0m.',
    page: '395'
  },
  {
    name: 'Inconsciente',
    type: null,
    description: 'O personagem fica indefeso e não pode fazer ações, incluindo reações (mas ainda pode fazer testes que sejam naturalmente feitos quando se está inconsciente, como testes de Constituição para estabilizar sangramento). Balançar uma criatura para acordá-la gasta uma ação padrão.',
    page: '395'
  },
  {
    name: 'Indefeso',
    type: null,
    description: 'O personagem fica desprevenido, mas sofre –10 na Defesa, falha automaticamente em testes de Reflexos e pode sofrer golpes de misericórdia.',
    page: '395'
  },
  {
    name: 'Lento',
    type: 'Movimento',
    description: 'Todas as formas de deslocamento do personagem são reduzidas à metade (arredonde para baixo para o primeiro incremento de 1,5m) e ele não pode correr ou fazer investidas.',
    page: '395'
  },
  {
    name: 'Ofuscado',
    type: 'Sentidos',
    description: 'O personagem sofre –2 em testes de ataque e de Percepção.',
    page: '395'
  },
  {
    name: 'Paralisado',
    type: 'Movimento',
    description: 'Fica imóvel e indefeso e só pode realizar ações puramente mentais.',
    page: '395'
  },
  {
    name: 'Pasmo',
    type: 'Mental',
    description: 'Não pode fazer ações.',
    page: '395'
  },
  {
    name: 'Petrificado',
    type: 'Metamorfose',
    description: 'O personagem fica inconsciente e recebe redução de dano 8.',
    page: '395'
  },
  {
    name: 'Sangrando',
    type: 'Metabolismo',
    description: 'No início de seu turno, o personagem deve fazer um teste de Constituição (CD 15). Se falhar, perde 1d6 pontos de vida e continua sangrando. Se passar, remove essa condição.',
    page: '395'
  },
  {
    name: 'Sobrecarregado',
    type: 'Movimento',
    description: 'O personagem sofre penalidade de armadura –5 e seu deslocamento é reduzido em –3m.',
    page: '395'
  },
  {
    name: 'Surdo',
    type: 'Sentidos',
    description: 'O personagem não pode fazer testes de Percepção para ouvir e sofre –5 em testes de Iniciativa. Além disso, é considerado em condição ruim para lançar magias.',
    page: '395'
  },
  {
    name: 'Surpreendido',
    type: null,
    description: 'O personagem fica desprevenido e não pode fazer ações.',
    page: '395'
  },
  {
    name: 'Vulnerável',
    type: null,
    description: 'O personagem sofre –2 na Defesa.',
    page: '395'
  }
];

export const QuickReferenceModal: React.FC<QuickReferenceModalProps> = ({
  isOpen,
  onClose,
  initialTab = 'manobras'
}) => {
  const [activeTab, setActiveTab] = useState<'manobras' | 'condicoes' | 'tabela'>(initialTab);
  const bodyRef = useRef<HTMLDivElement>(null);
  
  // Tab 1: Manobras & Ações
  const [expandedManeuverId, setExpandedManeuverId] = useState<string | null>(null);

  // Tab 2: Condições
  const [condSearch, setCondSearch] = useState<string>('');
  const [selectedCondType, setSelectedCondType] = useState<string>('Todas');
  const [expandedCondName, setExpandedCondName] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  // Tipos de efeito de condição disponíveis
  const conditionTypesList = useMemo(() => {
    const set = new Set<string>();
    CANONICAL_CONDITIONS.forEach(c => {
      if (c.type) set.add(c.type);
    });
    return ['Todas', 'Gerais (Sem Tipo)', ...Array.from(set).sort((a, b) => a.localeCompare(b, 'pt-BR'))];
  }, []);

  // Condições filtradas
  const filteredConditions = useMemo(() => {
    return CANONICAL_CONDITIONS.filter(item => {
      if (selectedCondType === 'Gerais (Sem Tipo)') {
        if (item.type !== null && item.type !== undefined) return false;
      } else if (selectedCondType !== 'Todas') {
        if (item.type !== selectedCondType) return false;
      }

      if (!condSearch.trim()) return true;
      const term = condSearch.toLowerCase();
      return (
        item.name.toLowerCase().includes(term) ||
        item.description.toLowerCase().includes(term) ||
        (item.type && item.type.toLowerCase().includes(term))
      );
    });
  }, [selectedCondType, condSearch]);

  const handleCopyConditions = () => {
    const lines: string[] = [];
    lines.push(`==================================================`);
    lines.push(`📜 CONDIÇÕES DE JOGO — TORMENTA20 (PÁG. 394-395)`);
    lines.push(`==================================================\n`);

    filteredConditions.forEach(cond => {
      const typeStr = cond.type ? ` [${cond.type}]` : '';
      lines.push(`• ${cond.name.toUpperCase()}${typeStr} (pág. ${cond.page})`);
      lines.push(`  ${cond.description}\n`);
    });

    navigator.clipboard.writeText(lines.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div 
        className="quick-ref-modal parchment-card ornate-border" 
        onClick={e => e.stopPropagation()}
      >
        {/* Header Nobre */}
        <div className="quick-ref-header">
          <div className="quick-ref-title-group">
            <div className="quick-ref-icon-gold">
              <BookOpen size={24} />
            </div>
            <div>
              <h2 className="quick-ref-title">Tomo de Consulta Rápida</h2>
              <p className="quick-ref-subtitle">Regras Oficiais de Combate (Pág. 220) & Condições (Pág. 240 / 394)</p>
            </div>
          </div>
          <button className="quick-ref-close-btn" onClick={onClose} aria-label="Fechar Guia">
            <X size={20} />
          </button>
        </div>

        {/* Abas de Navegação Segmentadas */}
        <div className="quick-ref-nav-tabs">
          <button 
            className={`quick-ref-tab-btn ${activeTab === 'manobras' ? 'active' : ''}`}
            onClick={() => setActiveTab('manobras')}
          >
            <Swords size={18} />
            <span>Ações & Manobras (Pág. 220)</span>
          </button>

          <button 
            className={`quick-ref-tab-btn ${activeTab === 'condicoes' ? 'active' : ''}`}
            onClick={() => setActiveTab('condicoes')}
          >
            <Activity size={18} />
            <span>Condições de Jogo (Pág. 240)</span>
            <span className="tab-pill-count">{CANONICAL_CONDITIONS.length}</span>
          </button>

          <button 
            className={`quick-ref-tab-btn ${activeTab === 'tabela' ? 'active' : ''}`}
            onClick={() => setActiveTab('tabela')}
          >
            <Layers size={18} />
            <span>Tabela de Resumo (Cola)</span>
          </button>
        </div>

        {/* Conteúdo Principal */}
        <div className="quick-ref-body" ref={bodyRef}>
          {/* ============================================================= */}
          {/* ABA 1: AÇÕES & MANOBRAS (PÁG. 220 / 233-239)                  */}
          {/* ============================================================= */}
          {activeTab === 'manobras' && (
            <div className="quick-ref-tab-content">
              {/* Tabela de Modificadores de Tamanho */}
              <div className="size-modifiers-banner parchment-subcard">
                <div className="size-banner-header">
                  <Zap size={18} className="text-gold" />
                  <h4>Modificadores de Tamanho em Manobras (Pág. 238)</h4>
                </div>
                <p className="size-banner-text">
                  Ao realizar ou resistir a qualquer manobra de combate, aplique o modificador da criatura no teste de Luta:
                </p>
                <div className="size-grid">
                  {CANONICAL_SIZE_MODIFIERS.map(item => (
                    <div key={item.size} className="size-chip">
                      <span className="size-name">{item.size}</span>
                      <span className={`size-mod ${item.mod.startsWith('+') ? 'size-mod-pos' : item.mod.startsWith('–') ? 'size-mod-neg' : 'size-mod-zero'}`}>
                        {item.mod}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Seção de Manobras Canônicas */}
              <div className="section-divider-title">
                <Swords size={16} />
                <span>Manobras de Combate (Pág. 238–239)</span>
              </div>

              <div className="maneuvers-list">
                {CANONICAL_MANEUVERS.map(man => {
                  const isExpanded = expandedManeuverId === man.id;
                  return (
                    <div 
                      key={man.id} 
                      className={`maneuver-card parchment-subcard ${isExpanded ? 'expanded' : ''}`}
                    >
                      <div 
                        className="maneuver-card-header"
                        onClick={() => setExpandedManeuverId(isExpanded ? null : man.id)}
                      >
                        <div className="maneuver-title-left">
                          <h3 className="maneuver-name">{man.name}</h3>
                          <span className="badge-gold action-tag">{man.actionType}</span>
                          <span className="maneuver-page">pág. {man.page}</span>
                        </div>

                        <div className="maneuver-header-right">
                          <div className="opposed-test-badge">
                            <span className="opposed-label">Teste Oposto:</span>
                            <span className="opposed-val">{man.opposedTest}</span>
                          </div>
                          <button className="expand-icon-btn" aria-label="Expandir Manobra">
                            {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                          </button>
                        </div>
                      </div>

                      {/* Texto Integral */}
                      <div className="maneuver-body">
                        <p className="maneuver-description">{man.description}</p>

                        {man.relatedConditions && man.relatedConditions.length > 0 && (
                          <div className="maneuver-conditions-row">
                            <span className="cond-rel-label">Condições associadas:</span>
                            {man.relatedConditions.map(c => (
                              <span key={c} className="badge-ruby cond-chip">{c}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Ações Básicas do Turno */}
              <div className="section-divider-title mt-4">
                <BookOpen size={16} />
                <span>Tipos de Ação em Combate (Pág. 233–236)</span>
              </div>

              <div className="actions-info-grid">
                {CANONICAL_ACTIONS.map(act => (
                  <div key={act.name} className="action-info-card parchment-subcard">
                    <div className="action-info-header">
                      <span className="badge-parchment action-badge-name">{act.name}</span>
                      <span className="maneuver-page">pág. {act.page}</span>
                    </div>
                    <p className="action-info-desc">{act.description}</p>
                    <div className="action-info-examples">
                      <strong>Exemplos:</strong> {act.examples}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ============================================================= */}
          {/* ABA 2: CONDIÇÕES DE JOGO (PÁG. 240 / 394-395)                 */}
          {/* ============================================================= */}
          {activeTab === 'condicoes' && (
            <div className="quick-ref-tab-content">
              {/* Barra de Filtro e Busca */}
              <div className="cond-toolbar">
                <div className="cond-search-box">
                  <Search size={18} className="search-icon-muted" />
                  <input
                    type="text"
                    placeholder="Pesquisar condição canônica (ex: defesa, caído, -5, sentidos)..."
                    value={condSearch}
                    onChange={e => setCondSearch(e.target.value)}
                    className="cond-search-input"
                  />
                  {condSearch && (
                    <button className="clear-search-btn" onClick={() => setCondSearch('')}>
                      <X size={16} />
                    </button>
                  )}
                </div>

                <button 
                  className={`copy-btn parchment-btn ${copied ? 'btn-copied' : ''}`}
                  onClick={handleCopyConditions}
                  title="Copiar lista de condições"
                >
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                  <span>{copied ? 'Copiado!' : 'Copiar'}</span>
                </button>
              </div>

              {/* Filtro por Tipo de Efeito Oficial */}
              <div className="cond-cat-chips">
                {conditionTypesList.map(cat => (
                  <button
                    key={cat}
                    className={`cat-chip-btn ${selectedCondType === cat ? 'active' : ''}`}
                    onClick={() => setSelectedCondType(cat)}
                  >
                    {cat}
                  </button>
                ))}
              </div>

              {/* Lista de Condições com Texto Verbatim */}
              <div className="conditions-catalog-list">
                {filteredConditions.length === 0 ? (
                  <div className="no-conditions-found parchment-subcard">
                    <HelpCircle size={32} className="text-muted" />
                    <p>Nenhuma condição encontrada para "{condSearch}".</p>
                  </div>
                ) : (
                  filteredConditions.map(cond => {
                    const isExpanded = expandedCondName === cond.name;
                    return (
                      <div 
                        key={cond.name} 
                        className={`condition-item-card parchment-subcard ${isExpanded ? 'expanded' : ''}`}
                      >
                        <div 
                          className="condition-item-header"
                          onClick={() => setExpandedCondName(isExpanded ? null : cond.name)}
                        >
                          <div className="condition-title-block">
                            <h3 className="condition-name">{cond.name}</h3>
                            {cond.type && (
                              <span className="badge-ruby cond-cat-badge">
                                <em>{cond.type}</em>
                              </span>
                            )}
                            <span className="cond-page-ref">pág. {cond.page}</span>
                          </div>

                          <button className="expand-icon-btn" aria-label="Expandir Condição">
                            {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                          </button>
                        </div>

                        <div className="condition-item-body">
                          <p className="condition-text">{cond.description}</p>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          )}

          {/* ============================================================= */}
          {/* ABA 3: TABELA DE RESUMO DE REGRAS (PÁG. 224, 226, 237-238)     */}
          {/* ============================================================= */}
          {activeTab === 'tabela' && (
            <div className="quick-ref-tab-content">
              {/* Tabela de Descanso */}
              <div className="cheat-section parchment-subcard">
                <div className="cheat-section-header">
                  <Moon size={20} className="text-mana" />
                  <h3>Descanso e Recuperação (Pág. 224)</h3>
                </div>
                <p className="cheat-desc">
                  Um descanso de 8 horas permite recuperar Pontos de Vida (PV) e Pontos de Mana (PM). Condições de descanso:
                </p>
                <div className="cheat-table-wrapper">
                  <table className="cheat-table">
                    <thead>
                      <tr>
                        <th>Condição</th>
                        <th>Exemplo de Local</th>
                        <th>Recuperação de PV / PM</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td><strong>Ruim</strong></td>
                        <td>Acampamento exposto ao relento</td>
                        <td><span className="badge-ruby">PV e PM = 1x nível</span></td>
                      </tr>
                      <tr>
                        <td><strong>Normal</strong></td>
                        <td>Estalagem comum, barraca confortável</td>
                        <td><span className="badge-gold">PV e PM = 2x nível</span></td>
                      </tr>
                      <tr>
                        <td><strong>Confortável</strong></td>
                        <td>Quarto de luxo, mansão nobre</td>
                        <td><span className="badge-emerald">PV e PM = 3x nível</span></td>
                      </tr>
                      <tr>
                        <td><strong>Luxuoso</strong></td>
                        <td>Palácio real, santuário protegido</td>
                        <td><span className="badge-mana">PV e PM = 4x nível</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Regras de Acúmulo de Bônus */}
              <div className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header">
                  <Sparkles size={20} className="text-gold" />
                  <h3>Acúmulo de Bônus e Efeitos (Pág. 226)</h3>
                </div>
                <div className="stacking-rules-grid">
                  <div className="stacking-box rule-no-stack">
                    <h4>❌ Mesma Fonte</h4>
                    <p>Bônus de mesma fonte (duas magias, dois itens com o mesmo encanto, ou a mesma habilidade usada duas vezes) <strong>NÃO se acumulam</strong> — aplique apenas o maior.</p>
                  </div>
                  <div className="stacking-box rule-stack">
                    <h4>✅ Fontes Diferentes</h4>
                    <p>Bônus de tipos e fontes diferentes (um item, uma magia e uma habilidade de classe) <strong>se acumulam normalmente</strong>.</p>
                  </div>
                  <div className="stacking-box rule-penalties">
                    <h4>⚠️ Penalidades</h4>
                    <p>Penalidades <strong>sempre se acumulam</strong>, a menos que venham da mesma condição ou efeito idêntico.</p>
                  </div>
                </div>
              </div>

              {/* Cobertura, Camuflagem e Modificadores */}
              <div className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header">
                  <ShieldAlert size={20} className="text-ruby" />
                  <h3>Cobertura, Camuflagem e Modificadores de Combate (Pág. 225, 237)</h3>
                </div>
                <div className="cheat-table-wrapper">
                  <table className="cheat-table">
                    <thead>
                      <tr>
                        <th>Situação</th>
                        <th>Efeito Mecânico</th>
                        <th>Referência Oficial</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td><strong>Cobertura Leve</strong></td>
                        <td><span className="badge-emerald">+2 na Defesa</span></td>
                        <td>Mureta baixa, criatura no caminho</td>
                      </tr>
                      <tr>
                        <td><strong>Cobertura Total</strong></td>
                        <td><span className="badge-emerald">+5 na Defesa</span></td>
                        <td>Parede inteira, obstáculo sólido total</td>
                      </tr>
                      <tr>
                        <td><strong>Camuflagem Leve</strong></td>
                        <td><span className="badge-amber">20% de chance de erro (1 em 1d5)</span></td>
                        <td>Névoa suave, penumbra, folhagem</td>
                      </tr>
                      <tr>
                        <td><strong>Camuflagem Total</strong></td>
                        <td><span className="badge-ruby">50% de chance de erro (1-5 em 1d10)</span></td>
                        <td>Escuridão total, invisibilidade, cegueira</td>
                      </tr>
                      <tr>
                        <td><strong>Flanquear</strong></td>
                        <td><span className="badge-gold">+2 no teste de ataque corpo a corpo</span></td>
                        <td>Você e um aliado em lados opostos do alvo</td>
                      </tr>
                      <tr>
                        <td><strong>Posição Elevada</strong></td>
                        <td><span className="badge-gold">+2 no teste de ataque corpo a corpo</span></td>
                        <td>Atacando de cima de mesa, montaria ou terreno alto</td>
                      </tr>
                      <tr>
                        <td><strong>Investida</strong></td>
                        <td><span className="badge-gold">+2 no teste de ataque</span> / <span className="badge-ruby">–2 na Defesa</span></td>
                        <td>Avança o dobro do deslocamento em linha reta</td>
                      </tr>
                      <tr>
                        <td><strong>Alvo Caído</strong></td>
                        <td><span className="badge-ruby">–5 Defesa (C. a C.)</span> / <span className="badge-emerald">+5 Defesa (Distância)</span></td>
                        <td>Sofre –5 em ataques corpo a corpo e deslocamento 1,5m</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Rodapé de Ajuda */}
        <div className="quick-ref-footer">
          <span className="footer-meta-note">
            📜 Tormenta20: Edição Jogo do Ano • Regras canônicas oficiais preservadas literalmente
          </span>
          <button className="parchment-btn btn-gold" onClick={onClose}>
            Fechar Tomo
          </button>
        </div>

        <ScrollToTop containerRef={bodyRef} isInsideContainer />
      </div>
    </div>
  );
};
