import React, { useState, useMemo } from 'react';
import { X, ShieldAlert, Search, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

// ============================================================================
// Dados canônicos das condições — Tormenta20 (Jogo do Ano), pág. 394–395
// Texto preservado LITERALMENTE conforme publicação oficial.
// ============================================================================

interface ConditionData {
  name: string;
  description: string;
  page: string;
}

const CONDITIONS_CANONICAL: ConditionData[] = [
  {
    name: 'Abalado',
    description: 'O personagem sofre –2 em testes de ataque, testes de perícia e testes de habilidade. Se ficar abalado novamente, em vez disso fica apavorado.',
    page: '394'
  },
  {
    name: 'Agarrado',
    description: 'O personagem fica desprevenido e imóvel, sofre –2 nos testes de ataque e só pode atacar com armas leves. Além disso, precisa fazer testes de concentração para lançar magias (CD 10 + nível da magia).',
    page: '394'
  },
  {
    name: 'Alquebrado',
    description: 'O personagem sofre –5 em testes de ataque, testes de perícia e testes de habilidade. Se ficar alquebrado novamente, em vez disso fica inconsciente.',
    page: '394'
  },
  {
    name: 'Apavorado',
    description: 'O personagem sofre –5 em testes de ataque, testes de perícia e testes de habilidade e deve fugir da fonte de medo. Se não puder fugir, pode lutar, mas ainda sofre as penalidades. Se ficar apavorado novamente, em vez disso fica alquebrado.',
    page: '394'
  },
  {
    name: 'Atordoado',
    description: 'O personagem fica desprevenido e não pode fazer ações.',
    page: '394'
  },
  {
    name: 'Caído',
    description: 'O personagem está no chão. Sofre –5 em ataques corpo a corpo e não pode usar ataques à distância, exceto com bestas. Além disso, sofre –5 na Defesa contra ataques corpo a corpo, mas recebe +5 na Defesa contra ataques à distância. Levantar-se exige uma ação de movimento.',
    page: '394'
  },
  {
    name: 'Cego',
    description: 'O personagem não pode enxergar. Fica desprevenido, sofre –5 em testes de Força e Destreza e em testes de perícias baseadas nesses atributos, se move com metade do deslocamento e sofre –10 em testes de Percepção. Todos os outros personagens têm camuflagem total contra ele.',
    page: '394'
  },
  {
    name: 'Confuso',
    description: 'O personagem não pode tomar ações normais. No início de cada turno, role 1d6: 1 — age normalmente; 2-3 — não faz nada além de balbuciar; 4-5 — ataca a criatura mais próxima (considere desprevenido se for um aliado); 6 — ataca a si mesmo automaticamente.',
    page: '394'
  },
  {
    name: 'Debilitado',
    description: 'O personagem sofre –2 em testes de atributos físicos (Força, Destreza, Constituição) e de perícias baseadas nesses atributos. Se ficar debilitado novamente, em vez disso fica fraco.',
    page: '394'
  },
  {
    name: 'Desprevenido',
    description: 'O personagem não pode usar o bônus de Destreza na Defesa. Algumas habilidades e ataques só podem ser usados contra alvos desprevenidos.',
    page: '394'
  },
  {
    name: 'Doente',
    description: 'O personagem sofre –2 em testes de ataque, testes de perícia e testes de habilidade. Se não for tratado, a cada dia deve fazer um teste de Fortitude com a CD da doença. Se falhar, a condição piora (o mestre dita os efeitos, podendo incluir dano de atributo ou morte).',
    page: '394'
  },
  {
    name: 'Em Chamas',
    description: 'O personagem está pegando fogo. No início de cada turno, sofre 1d6 pontos de dano de fogo e pode gastar uma ação padrão para se apagar (teste de Reflexos, CD 15). Se não tentar se apagar, o dano aumenta em +1d6 cumulativo.',
    page: '394'
  },
  {
    name: 'Enfeitiçado',
    description: 'O personagem é considerado amigável pela criatura que o enfeitiçou. Obedece sugestões que não sejam evidentemente perigosas. Ameaçar ou atacar o alvo enfeitiçado quebra o efeito. Qualquer ação nociva contra o alvo permite um novo teste de resistência.',
    page: '394'
  },
  {
    name: 'Enjoado',
    description: 'O personagem só pode realizar uma ação padrão ou de movimento por turno (não ambas) e não pode fazer ações completas. Se ficar enjoado novamente, em vez disso fica nauseado (não pode atacar, lançar magias ou fazer qualquer coisa que exija concentração).',
    page: '394'
  },
  {
    name: 'Enredado',
    description: 'O personagem fica lento e sofre –2 em testes de ataque e –4 na Destreza.',
    page: '395'
  },
  {
    name: 'Envenenado',
    description: 'Efeitos variados conforme o veneno específico. Venenos normalmente causam dano de atributo ou condições (como enjoado ou debilitado). A frequência e a cura dependem da descrição do veneno.',
    page: '395'
  },
  {
    name: 'Esmorecido',
    description: 'O personagem sofre –5 em testes de ataque, testes de perícia e testes de habilidade. Se ficar esmorecido novamente, em vez disso fica inconsciente.',
    page: '395'
  },
  {
    name: 'Exausto',
    description: 'O personagem sofre –6 em Força e Destreza e seu deslocamento é reduzido à metade. Após um descanso de pelo menos 1 hora, um personagem exausto passa a estar fatigado.',
    page: '395'
  },
  {
    name: 'Fascinado',
    description: 'O personagem fica parado, prestando atenção na fonte de fascinação. Sofre –5 em testes de Percepção. Qualquer ameaça potencial permite um novo teste para quebrar o efeito. Uma ameaça óbvia quebra automaticamente.',
    page: '395'
  },
  {
    name: 'Fatigado',
    description: 'O personagem sofre –2 em Força e Destreza e não pode correr ou fazer investidas. Após um descanso de pelo menos 8 horas, não está mais fatigado.',
    page: '395'
  },
  {
    name: 'Fraco',
    description: 'O personagem sofre –5 em testes de atributos físicos (Força, Destreza, Constituição) e de perícias baseadas nesses atributos. Se ficar fraco novamente, em vez disso fica inconsciente.',
    page: '395'
  },
  {
    name: 'Frustrado',
    description: 'O personagem sofre –2 em testes de atributos mentais (Inteligência, Sabedoria, Carisma) e de perícias baseadas nesses atributos. Se ficar frustrado novamente, em vez disso fica esmorecido.',
    page: '395'
  },
  {
    name: 'Imóvel',
    description: 'O deslocamento do personagem se torna 0m e ele não pode se movimentar.',
    page: '395'
  },
  {
    name: 'Inconsciente',
    description: 'O personagem fica indefeso e não pode fazer ações, inclusive reações. Balbucia inconscientemente ou fica totalmente apagado.',
    page: '395'
  },
  {
    name: 'Indefeso',
    description: 'O personagem fica desprevenido, sofre –10 na Defesa, falha automaticamente em testes de Reflexos e pode sofrer golpes de misericórdia.',
    page: '395'
  },
  {
    name: 'Lento',
    description: 'O deslocamento do personagem é reduzido à metade e ele não pode correr ou fazer investidas.',
    page: '395'
  },
  {
    name: 'Ofuscado',
    description: 'O personagem sofre –2 em testes de ataque e em testes de Percepção para observar.',
    page: '395'
  },
  {
    name: 'Paralisado',
    description: 'O personagem fica imóvel e indefeso e só pode realizar ações puramente mentais.',
    page: '395'
  },
  {
    name: 'Pasmo',
    description: 'O personagem não pode fazer ações.',
    page: '395'
  },
  {
    name: 'Petrificado',
    description: 'O personagem se transforma em pedra. Fica inconsciente e recebe redução de dano 10.',
    page: '395'
  },
  {
    name: 'Sangrando',
    description: 'No início de seu turno, o personagem deve fazer um teste de Constituição (CD 15). Se falhar, perde 1d6 pontos de vida e continua sangrando. Se passar, estabiliza e para de sangrar.',
    page: '395'
  },
  {
    name: 'Sobrecarregado',
    description: 'O personagem sofre penalidade de armadura –5 e seu deslocamento é reduzido em 3m.',
    page: '395'
  },
  {
    name: 'Surdo',
    description: 'O personagem não pode fazer testes de Percepção para ouvir e sofre –5 em testes de Iniciativa.',
    page: '395'
  },
  {
    name: 'Surpreendido',
    description: 'O personagem fica desprevenido e não pode realizar ações na primeira rodada de combate.',
    page: '395'
  },
  {
    name: 'Vulnerável',
    description: 'O personagem sofre –2 na Defesa.',
    page: '395'
  },
];

// ============================================================================
// Props — simplificada para listagem pura
// ============================================================================

interface ConditionsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CombatTrackerModal: React.FC<ConditionsModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const filteredConditions = useMemo(() => {
    if (!searchTerm.trim()) return CONDITIONS_CANONICAL;
    const term = searchTerm.toLowerCase();
    return CONDITIONS_CANONICAL.filter(
      c =>
        c.name.toLowerCase().includes(term) ||
        c.description.toLowerCase().includes(term)
    );
  }, [searchTerm]);

  const handleToggle = (idx: number) => {
    setExpandedIndex(prev => (prev === idx ? null : idx));
  };

  const [copied, setCopied] = useState<boolean>(false);

  const handleCopyContent = () => {
    const lines: string[] = [];
    lines.push(`========================================`);
    lines.push(`CONDIÇÕES DE JOGO (TORMENTA20)`);
    lines.push(`========================================\n`);

    filteredConditions.forEach(cond => {
      lines.push(`• ${cond.name.toUpperCase()}`);
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
        className="conditions-listing-modal parchment-card ornate-border"
        onClick={e => e.stopPropagation()}
      >
        {/* ── Header ── */}
        <div className="modal-header">
          <div className="title-row">
            <span className="badge badge-ruby">
              <ShieldAlert size={14} /> Apêndice
            </span>
            <h2 className="modal-title">Condições</h2>
          </div>
          <div className="modal-header-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button 
              className={`copy-btn ${copied ? 'copy-success' : ''}`}
              onClick={handleCopyContent}
              title={copied ? 'Copiado!' : 'Copiar todas as condições'}
            >
              {copied ? <Check size={20} className="text-gold" /> : <Copy size={20} />}
            </button>
            <button className="modal-close-btn" onClick={onClose} aria-label="Fechar">
              <X size={24} />
            </button>
          </div>
        </div>

        {/* ── Search / Filter ── */}
        <div className="conditions-search-bar">
          <div className="conditions-search-field">
            <Search size={16} className="conditions-search-icon" />
            <input
              type="text"
              placeholder="Filtrar condições... (ex: Cego, Abalado)"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="conditions-search-input"
            />
          </div>
          <span className="conditions-count-label">
            {filteredConditions.length} de {CONDITIONS_CANONICAL.length}
          </span>
        </div>

        {/* ── Conditions List ── */}
        <div className="conditions-list-body">
          {filteredConditions.length === 0 ? (
            <div className="conditions-empty">
              <span style={{ fontSize: '2rem' }}>🔍</span>
              <p>Nenhuma condição encontrada para "<strong>{searchTerm}</strong>".</p>
            </div>
          ) : (
            <ul className="conditions-accordion">
              {filteredConditions.map((cond, idx) => {
                const isExpanded = expandedIndex === idx;
                return (
                  <li key={cond.name} className="conditions-accordion-item">
                    <button
                      className={`conditions-accordion-trigger ${isExpanded ? 'conditions-accordion-trigger--open' : ''}`}
                      onClick={() => handleToggle(idx)}
                      aria-expanded={isExpanded}
                    >
                      <span className="conditions-accordion-name">{cond.name}</span>
                      <div className="conditions-accordion-meta">
                        {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </div>
                    </button>
                    {isExpanded && (
                      <div className="conditions-accordion-panel">
                        <p className="conditions-description-text">
                          {cond.description}
                        </p>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};
