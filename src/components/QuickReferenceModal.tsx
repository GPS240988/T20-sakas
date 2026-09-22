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
  Layers,
  Target,
  Maximize2
} from 'lucide-react';
import { ScrollToTop } from './ScrollToTop';
import { removeAccents } from '../utils/textUtils';

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
  relatedConditions?: string[];
}

export interface HealthRuleCanonical {
  title: string;
  badge: string;
  badgeClass: 'ruby' | 'gold' | 'mana' | 'emerald' | 'amber';
  page: string;
  description: string;
  mechanicalDetails: string;
  relatedConditions?: string[];
}

export interface RangeCanonical {
  name: string;
  distance: string;
  description: string;
  examples: string;
}

export interface CreatureSizeCanonical {
  size: string;
  space: string;
  reach: string;
  stealthMod: string;
  maneuverMod: string;
}

import bookAreasImg from '../assets/regras/areas_de_efeito_livro.png';

export interface AreaEffectCanonical {
  shape: string;
  name: string;
  page: string;
  description: string;
  gridRule: string;
}

export interface SpellTargetTypeCanonical {
  title: string;
  badge: string;
  page: string;
  description: string;
}

export const CANONICAL_AREA_EFFECTS: AreaEffectCanonical[] = [
  {
    shape: 'Cone',
    name: 'Cone',
    page: '225',
    description: 'Surge adjacente a você e se afasta de você na direção escolhida, ficando mais largo com a distância, conforme os modelos da ilustração oficial do livro.',
    gridRule: 'A largura final do cone é igual ao seu comprimento (ex: cone de 6m atinge 6m de largura na extremidade).'
  },
  {
    shape: 'Linha',
    name: 'Linha',
    page: '225',
    description: 'Surge adjacente a você e se afasta de você reta até o fim do alcance.',
    gridRule: 'A menos que indicado o contrário, uma linha tem 1,5m de largura (1 quadrado).'
  },
  {
    shape: 'Esfera',
    name: 'Esfera',
    page: '225',
    description: 'Surge na interseção de quatro quadrados, estendendo-se em todas as direções até o limite de seu raio.',
    gridRule: 'O ponto de origem deve ser uma interseção de cruzamento na grade tática.'
  },
  {
    shape: 'Cilindro',
    name: 'Cilindro',
    page: '225',
    description: 'Surge na interseção de quatro quadrados, estendendo-se pela largura indicada e subindo até o fim da altura indicada.',
    gridRule: 'Possui raio circular no solo e projeção tridimensional de altura vertical.'
  },
  {
    shape: 'Quadrado',
    name: 'Quadrado / Cubo',
    page: '225',
    description: 'Surge no quadrado ou quadrados escolhidos, afetando o piso. Um "cubo" é como um quadrado, mas afeta também a altura.',
    gridRule: 'Um quadrado de 3m de lado afeta uma área de 2x2 quadrados de 1,5m.'
  },
  {
    shape: 'Outros',
    name: 'Outros Formatos',
    page: '225',
    description: 'Algumas habilidades podem ter áreas específicas, citadas em sua descrição oficial.',
    gridRule: 'Consulte o texto descritivo da habilidade ou magia específica.'
  }
];

export const CANONICAL_SPELL_TARGET_TYPES: SpellTargetTypeCanonical[] = [
  {
    title: 'Alvo',
    badge: 'Criatura / Objeto',
    page: '225',
    description: 'O efeito afeta diretamente uma ou mais criaturas ou objetos específicos escolhidos pelo conjurador dentro do alcance. Você precisa ter linha de efeito até o alvo.'
  },
  {
    title: 'Área',
    badge: 'Espaço Físico',
    page: '225',
    description: 'O efeito afeta um espaço físico inteiro e tudo o que estiver contido dentro dele. Você escolhe onde o efeito se inicia (ponto de origem), mas não quais criaturas são afetadas.'
  },
  {
    title: 'Efeito',
    badge: 'Criação / Convocação',
    page: '225',
    description: 'O efeito cria algo físico ou mágico no campo de batalha (como um monstro convocado, uma parede de pedra ou uma ilusão), em vez de afetar algo pré-existente.'
  },
  {
    title: 'Duração',
    badge: 'Tempo de Ação',
    page: '225',
    description: 'Especifica quanto tempo o efeito permanece ativo: Instantânea (imediata), Cena (todo o combate/encontro ~10 min), Sustentada (gasta 1 PM no início do turno para manter), ou Permanente.'
  }
];

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

export interface ManeuverGeneralRuleCanonical {
  title: string;
  page: string;
  description: string;
  keyPoints: string[];
}

export const CANONICAL_MANEUVER_GENERAL_RULES: ManeuverGeneralRuleCanonical = {
  title: 'Regras Gerais de Manobras de Combate (Pág. 238)',
  page: '238',
  description: 'Uma manobra é um ataque corpo a corpo para realizar algo que não seja causar dano — como desarmar o oponente ou empurrá-lo para um precipício.',
  keyPoints: [
    'Teste de Manobra: Faça um teste de ataque corpo a corpo (Luta) oposto ao teste de ataque corpo a corpo do alvo.',
    'Resolução de Empates: Em caso de empate, o personagem com o maior modificador vence. Se os modificadores forem iguais, outro teste deve ser feito.',
    'Bônus de Arma: Você pode usar qualquer arma corpo a corpo para fazer uma manobra, recebendo todos os bônus normais da arma (exceto por bônus numéricos de dano).',
    'Exigências Específicas: Algumas manobras exigem armas específicas ou requerem uma mão livre (veja a descrição de cada manobra).',
    'Modificadores de Tamanho: Criaturas de tamanhos diferentes recebem bônus ou sofrem penalidades no teste de manobra (de –5 para Minúsculo até +10 para Colossal).'
  ]
};

export const CANONICAL_MANEUVERS: ManeuverCanonical[] = [
  {
    id: 'manobra-agarrar',
    name: 'Agarrar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de manobra (Luta) oposto pelo teste de Luta do alvo.',
    description: 'Você usa uma mão livre para segurar o alvo. Faça um teste de manobra (Luta). Se você vencer, o alvo fica agarrado. Um personagem agarrado fica desprevenido e imóvel, sofre –2 em testes de ataque e só pode atacar com armas leves. Para se soltar, a criatura agarrada precisa gastar uma ação padrão e passar em um teste de Luta ou Acrobacia oposto ao seu teste de Luta. Você pode soltar o alvo com uma ação livre. Enquanto estiver agarrando uma criatura, você pode se movimentar à metade do seu deslocamento normal, arrastando o alvo com você. Você pode atacar a criatura agarrada com sua mão livre ou com uma arma leve. Em vez de fazer um ataque, você pode fazer um novo teste de manobra contra a criatura agarrada; se vencer, causa dano desarmado ou da arma natural. Ataques à distância contra um alvo envolvido em uma manobra agarrar têm 50% de chance de acertar o alvo errado.',
    page: '238',
    relatedConditions: ['Agarrado', 'Desprevenido', 'Imóvel']
  },
  {
    id: 'manobra-atropelar',
    name: 'Atropelar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de manobra (Luta) oposto pelo teste de Luta ou Acrobacia do alvo.',
    description: 'Você tenta passar pelo espaço ocupado por uma criatura durante um movimento (requer uma ação padrão durante o movimento ou faz parte de uma ação de investida). A criatura pode escolher deixá-lo passar (ela não sofre nada e você continua o movimento) ou resistir. Se ela resistir, faça um teste de manobra oposto. Se você vencer, a criatura cai no chão (fica caída) e você continua seu movimento, atravessando o espaço dela. Se você perder, é empurrado de volta para o quadrado de onde tentou entrar no espaço da criatura e seu movimento termina.',
    page: '238–239',
    relatedConditions: ['Caído']
  },
  {
    id: 'manobra-derrubar',
    name: 'Derrubar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de manobra (Luta) oposto pelo teste de Luta ou Acrobacia do alvo.',
    description: 'Você faz o alvo cair no chão. Faça um teste de manobra. Se você vencer, o alvo cai no chão e fica caído. Se você vencer o teste por 5 pontos ou mais, além de cair, o alvo é empurrado 1,5m (um quadrado) em uma direção à sua escolha. Se empurrado para um precipício ou superfície perigosa, o alvo tem direito a um teste de Reflexos (CD 20) para se segurar em uma borda.',
    page: '239',
    relatedConditions: ['Caído']
  },
  {
    id: 'manobra-desarmar',
    name: 'Desarmar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de manobra (Luta) oposto pelo teste de Luta do alvo.',
    description: 'Você atinge a arma ou item que o alvo está segurando. Faça um teste de manobra. Se você vencer, o item cai no mesmo espaço do alvo. Se você vencer o teste por 5 pontos ou mais, o item voa para longe, caindo a 1,5m (um quadrado) de distância em uma direção à sua escolha.',
    page: '239'
  },
  {
    id: 'manobra-empurrar',
    name: 'Empurrar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de manobra (Luta) oposto pelo teste de Atletismo ou Luta do alvo.',
    description: 'Você empurra o alvo para longe de você. Faça um teste de manobra (Luta). Se você vencer, empurra o alvo 1,5m. Para cada 5 pontos de diferença a seu favor no resultado do teste, empurra o alvo mais 1,5m. Você pode avançar junto com o alvo para empurrá-lo além do seu alcance natural, gastando seu deslocamento normal para isso.',
    page: '239'
  },
  {
    id: 'manobra-fintar',
    name: 'Fintar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de Enganação oposto pelo teste de Reflexos do alvo (alcance curto).',
    description: 'Você faz um movimento falso para desestabilizar o alvo. Faça um teste de Enganação oposto ao teste de Reflexos do alvo (ele deve estar em alcance curto e ser capaz de vê-lo). Se você vencer, o alvo fica desprevenido contra o seu próximo ataque corpo a corpo ou à distância realizado até o fim do seu próximo turno.',
    page: '239',
    relatedConditions: ['Desprevenido']
  },
  {
    id: 'manobra-quebrar',
    name: 'Quebrar',
    actionType: 'Ação Padrão',
    opposedTest: 'Teste de manobra (Luta) oposto pelo teste de Luta do alvo empunhando o item.',
    description: 'Você golpeia um item empunhado ou vestido pelo alvo para danificá-lo. Faça um teste de manobra. Se vencer, você causa o dano do seu ataque diretamente no item. Veja as regras de quebrando objetos na página 242 (RD e PV dos objetos).',
    page: '239'
  }
];

export const CANONICAL_CREATURE_SIZES: CreatureSizeCanonical[] = [
  { size: 'Minúsculo', space: '0,75m (0,5q)', reach: '1,5m', stealthMod: '+5', maneuverMod: '–5' },
  { size: 'Pequeno', space: '1,5m (1q)', reach: '1,5m', stealthMod: '+2', maneuverMod: '–2' },
  { size: 'Médio', space: '1,5m (1q)', reach: '1,5m', stealthMod: '+0', maneuverMod: '+0' },
  { size: 'Grande', space: '3m (2q)', reach: '3m', stealthMod: '–2', maneuverMod: '+2' },
  { size: 'Enorme', space: '4,5m (3q)', reach: '4,5m', stealthMod: '–5', maneuverMod: '+5' },
  { size: 'Colossal', space: '9m+ (6q+)', reach: '6m+', stealthMod: '–10', maneuverMod: '+10' }
];

export const CANONICAL_SIZE_MODIFIERS = [
  { size: 'Minúsculo', mod: '–5' },
  { size: 'Pequeno', mod: '–2' },
  { size: 'Médio', mod: '+0' },
  { size: 'Grande', mod: '+2' },
  { size: 'Enorme', mod: '+5' },
  { size: 'Colossal', mod: '+10' }
];

export const CANONICAL_HEALTH_RULES: HealthRuleCanonical[] = [
  {
    title: 'PV Negativos & Sangramento',
    badge: 'Morte & Sangramento',
    badgeClass: 'ruby',
    page: '239',
    description: 'Quando seus Pontos de Vida caem para 0 ou menos, você cai inconsciente e fica sangrando. No início de cada um dos seus turnos, você deve fazer um teste de Constituição (CD 15).',
    mechanicalDetails: '• Sucesso: você se estabiliza (para de sangrar e permanece com 0 PV, porém inconsciente).\n• Falha: perde 1d6 PV e continua sangrando.\n• Morte: se seus PV negativos atingirem metade do seu valor total de PV máximos (ou –10 para nível 1), você morre instantaneamente.',
    relatedConditions: ['Inconsciente', 'Sangrando', 'Indefeso']
  },
  {
    title: 'Primeiros Socorros',
    badge: 'Estabilização de Emergência',
    badgeClass: 'emerald',
    page: '240',
    description: 'Você pode gastar uma ação padrão para prestar primeiros socorros em uma criatura sangrando que esteja ao seu alcance.',
    mechanicalDetails: '• Faça um teste de Cura (CD 15).\n• Se passar, a criatura se estabiliza e para de perder PV no início dos turnos dela, mas permanece inconsciente.',
    relatedConditions: ['Sangrando', 'Inconsciente']
  },
  {
    title: 'Golpe de Misericórdia',
    badge: 'Ataque Fatal Completo',
    badgeClass: 'ruby',
    page: '240',
    description: 'Um ataque com ação completa direcionado a uma criatura adjacente que esteja indefesa (como um inimigo inconsciente ou paralisado).',
    mechanicalDetails: '• Acerto Crítico Automático: o ataque atinge automaticamente e causa dano crítico.\n• Teste de Morte: se o alvo sobreviver ao dano, deve passar em um teste de Fortitude (CD 10 + dano sofrido) ou morrerá imediatamente.',
    relatedConditions: ['Indefeso', 'Inconsciente', 'Paralisado']
  },
  {
    title: 'Dano Massivo',
    badge: 'Trauma Grave',
    badgeClass: 'amber',
    page: '240',
    description: 'Se você sofrer um único ataque ou fonte de dano que cause dano igual ou superior a metade dos seus PV máximos (mínimo 50 pontos de dano).',
    mechanicalDetails: '• Faça um teste de Fortitude (CD 15 + 1 para cada 10 pontos de dano acima de 50).\n• Se falhar, seus PV caem imediatamente para 0 e você fica sangrando.',
    relatedConditions: ['Sangrando', 'Inconsciente']
  }
];

export const CANONICAL_RANGES: RangeCanonical[] = [
  {
    name: 'Pessoal',
    distance: '0 metros',
    description: 'O efeito afeta apenas o próprio executante/conjurador ou um objeto por ele empunhado.',
    examples: 'Magia Armadura Arcana, habilidades corporais do próprio personagem.'
  },
  {
    name: 'Toque',
    distance: '1,5 metros (Adjacente)',
    description: 'Requer contato físico ou toque com a mão/corpo na criatura ou objeto alvo.',
    examples: 'Magia Curar Ferimentos, manobras de toque, primeiros socorros.'
  },
  {
    name: 'Curto',
    distance: '9 metros (6 quadrados)',
    description: 'Alcance padrão para arremessos de armas, pistolas e magias de curta distância.',
    examples: 'Arremesso de adaga/machadinha, disparo de pistola, magia Flecha Ácida.'
  },
  {
    name: 'Médio',
    distance: '18 metros (12 quadrados)',
    description: 'Alcance intermediário de combate tático, cobrindo a maioria das salas e arenas.',
    examples: 'Magia Bola de Fogo, arcos curtos, habilidades de comando.'
  },
  {
    name: 'Longo',
    distance: '30 metros (20 quadrados)',
    description: 'Alcance estendido para atiradores de elite e magias de grande alcance.',
    examples: 'Disparo de arco longo, besta leve/pesada, magia Relâmpago.'
  },
  {
    name: 'Extremo',
    distance: '90 metros (60 quadrados)',
    description: 'Alcance de artilharia e imensa distância para grandes descampados e cercos.',
    examples: 'Magia Meteoro, disparos de cerco, armas à distância com encantos de alcance.'
  }
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

// ============================================================================
// Regras e Termos para Detecção Inteligente de Links (Chips Interativos)
// ============================================================================

interface KeywordRule {
  regex: RegExp;
  type: 'condition' | 'maneuver' | 'section';
  target: string;
  badgeClass: 'ruby' | 'gold' | 'mana' | 'emerald' | 'amber';
  tooltip: string;
  tab?: 'manobras' | 'condicoes' | 'tabela';
}

const KEYWORD_RULES: KeywordRule[] = [
  // Específicos compostos de tabela, combate e saúde
  { regex: /\b(golpe de miseric[oó]rdia)\b/gi, type: 'section', tab: 'tabela', target: 'section-health', badgeClass: 'ruby', tooltip: 'Ver Golpe de Misericórdia (Pág. 240)' },
  { regex: /\b(dano massivo)\b/gi, type: 'section', tab: 'tabela', target: 'section-health', badgeClass: 'amber', tooltip: 'Ver Dano Massivo (Pág. 240)' },
  { regex: /\b(primeiros socorros)\b/gi, type: 'section', tab: 'tabela', target: 'section-health', badgeClass: 'emerald', tooltip: 'Ver Primeiros Socorros (Pág. 240)' },
  { regex: /\b(pv negativos)\b/gi, type: 'section', tab: 'tabela', target: 'section-health', badgeClass: 'ruby', tooltip: 'Ver PV Negativos & Sangramento (Pág. 239)' },
  { regex: /\b(descanso e recupera[cç][aã]o)\b/gi, type: 'section', tab: 'tabela', target: 'section-rest', badgeClass: 'mana', tooltip: 'Ver Descanso e Recuperação (Pág. 224)' },
  { regex: /\b(cobertura total)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'emerald', tooltip: 'Ver Cobertura Total (+5 Defesa - Pág. 237)' },
  { regex: /\b(cobertura leve)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'emerald', tooltip: 'Ver Cobertura Leve (+2 Defesa - Pág. 237)' },
  { regex: /\b(camuflagem total)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'ruby', tooltip: 'Ver Camuflagem Total (50% de erro - Pág. 238)' },
  { regex: /\b(camuflagem leve)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'amber', tooltip: 'Ver Camuflagem Leve (20% de erro - Pág. 238)' },
  { regex: /\b(posi[cç][aã]o elevada)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'gold', tooltip: 'Ver Posição Elevada (+2 Ataque C.a C. - Pág. 237)' },
  { regex: /\b(modificadores de tamanho)\b/gi, type: 'section', tab: 'manobras', target: 'section-size-modifiers', badgeClass: 'gold', tooltip: 'Ver Modificadores de Tamanho em Manobras (Pág. 238)' },
  { regex: /\b([aá]reas? de efeito)\b/gi, type: 'section', tab: 'tabela', target: 'section-areas', badgeClass: 'ruby', tooltip: 'Ver Áreas de Efeito, Alvos e Duração (Pág. 225)' },
  { regex: /\b(linha de efeito)\b/gi, type: 'section', tab: 'tabela', target: 'section-areas', badgeClass: 'mana', tooltip: 'Ver Linha de Efeito (Pág. 225)' },
  { regex: /\b(ponto de origem)\b/gi, type: 'section', tab: 'tabela', target: 'section-areas', badgeClass: 'mana', tooltip: 'Ver Ponto de Origem na Grade (Pág. 225)' },
  { regex: /\b(alcance curto)\b/gi, type: 'section', tab: 'tabela', target: 'section-ranges', badgeClass: 'gold', tooltip: 'Ver Alcance Curto (9m - Pág. 138, 224)' },
  { regex: /\b(alcance m[eé]dio)\b/gi, type: 'section', tab: 'tabela', target: 'section-ranges', badgeClass: 'gold', tooltip: 'Ver Alcance Médio (18m - Pág. 138, 224)' },
  { regex: /\b(alcance longo)\b/gi, type: 'section', tab: 'tabela', target: 'section-ranges', badgeClass: 'gold', tooltip: 'Ver Alcance Longo (30m - Pág. 138, 224)' },
  { regex: /\b(alcance extremo)\b/gi, type: 'section', tab: 'tabela', target: 'section-ranges', badgeClass: 'gold', tooltip: 'Ver Alcance Extremo (90m - Pág. 138, 224)' },
  { regex: /\b(alcance de toque)\b/gi, type: 'section', tab: 'tabela', target: 'section-ranges', badgeClass: 'gold', tooltip: 'Ver Alcance Toque (1,5m - Pág. 138, 224)' },
  { regex: /\b(alcance pessoal)\b/gi, type: 'section', tab: 'tabela', target: 'section-ranges', badgeClass: 'gold', tooltip: 'Ver Alcance Pessoal (0m - Pág. 138, 224)' },
  { regex: /\b(flanquear)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'gold', tooltip: 'Ver Flanquear (+2 no ataque - Pág. 237)' },
  { regex: /\b(investida(?:s)?)\b/gi, type: 'section', tab: 'tabela', target: 'section-modifiers', badgeClass: 'gold', tooltip: 'Ver Investida (+2 ataque / –2 Defesa - Pág. 238)' },
  { regex: /\b(manobras? de combate|testes? de manobra)\b/gi, type: 'section', tab: 'manobras', target: 'section-maneuver-rules', badgeClass: 'gold', tooltip: 'Ver Regras Gerais de Manobras de Combate (Pág. 238)' },
  
  // Manobras de combate individuais
  { regex: /\b(agarrar)\b/gi, type: 'maneuver', target: 'manobra-agarrar', badgeClass: 'gold', tooltip: 'Ver Manobra Agarrar (Pág. 238)' },
  { regex: /\b(atropelar)\b/gi, type: 'maneuver', target: 'manobra-atropelar', badgeClass: 'gold', tooltip: 'Ver Manobra Atropelar (Pág. 238–239)' },
  { regex: /\b(derrubar)\b/gi, type: 'maneuver', target: 'manobra-derrubar', badgeClass: 'gold', tooltip: 'Ver Manobra Derrubar (Pág. 239)' },
  { regex: /\b(desarmar)\b/gi, type: 'maneuver', target: 'manobra-desarmar', badgeClass: 'gold', tooltip: 'Ver Manobra Desarmar (Pág. 239)' },
  { regex: /\b(empurrar)\b/gi, type: 'maneuver', target: 'manobra-empurrar', badgeClass: 'gold', tooltip: 'Ver Manobra Empurrar (Pág. 239)' },
  { regex: /\b(fintar)\b/gi, type: 'maneuver', target: 'manobra-fintar', badgeClass: 'gold', tooltip: 'Ver Manobra Fintar (Pág. 239)' },
  { regex: /\b(quebrar)\b/gi, type: 'maneuver', target: 'manobra-quebrar', badgeClass: 'gold', tooltip: 'Ver Manobra Quebrar (Pág. 239)' },

  // Condições canônicas de T20 (com flexões)
  { regex: /\b(agarrad[oas]|agarrando)\b/gi, type: 'condition', target: 'Agarrado', badgeClass: 'ruby', tooltip: 'Ver Condição Agarrado (Pág. 394)' },
  { regex: /\b(desprevenid[oas])\b/gi, type: 'condition', target: 'Desprevenido', badgeClass: 'ruby', tooltip: 'Ver Condição Desprevenido (Pág. 394)' },
  { regex: /\b(im[oó]ve(?:l|is))\b/gi, type: 'condition', target: 'Imóvel', badgeClass: 'ruby', tooltip: 'Ver Condição Imóvel (Pág. 395)' },
  { regex: /\b(ca[ií]d[oas])\b/gi, type: 'condition', target: 'Caído', badgeClass: 'ruby', tooltip: 'Ver Condição Caído (Pág. 394)' },
  { regex: /\b(inconsciente(?:s)?)\b/gi, type: 'condition', target: 'Inconsciente', badgeClass: 'ruby', tooltip: 'Ver Condição Inconsciente (Pág. 395)' },
  { regex: /\b(sangrando)\b/gi, type: 'condition', target: 'Sangrando', badgeClass: 'ruby', tooltip: 'Ver Condição Sangrando (Pág. 395)' },
  { regex: /\b(indefes[oas])\b/gi, type: 'condition', target: 'Indefeso', badgeClass: 'ruby', tooltip: 'Ver Condição Indefeso (Pág. 395)' },
  { regex: /\b(paralisad[oas])\b/gi, type: 'condition', target: 'Paralisado', badgeClass: 'ruby', tooltip: 'Ver Condição Paralisado (Pág. 395)' },
  { regex: /\b(ceg[oas])\b/gi, type: 'condition', target: 'Cego', badgeClass: 'ruby', tooltip: 'Ver Condição Cego (Pág. 394)' },
  { regex: /\b(lent[oas])\b/gi, type: 'condition', target: 'Lento', badgeClass: 'ruby', tooltip: 'Ver Condição Lento (Pág. 395)' },
  { regex: /\b(vulner[aá]ve(?:l|is))\b/gi, type: 'condition', target: 'Vulnerável', badgeClass: 'ruby', tooltip: 'Ver Condição Vulnerável (Pág. 395)' },
  { regex: /\b(frac[oas])\b/gi, type: 'condition', target: 'Fraco', badgeClass: 'ruby', tooltip: 'Ver Condição Fraco (Pág. 395)' },
  { regex: /\b(debilitad[oas])\b/gi, type: 'condition', target: 'Debilitado', badgeClass: 'ruby', tooltip: 'Ver Condição Debilitado (Pág. 394)' },
  { regex: /\b(exausto(?:s)?|exaust[as])\b/gi, type: 'condition', target: 'Exausto', badgeClass: 'ruby', tooltip: 'Ver Condição Exausto (Pág. 395)' },
  { regex: /\b(fatigad[oas])\b/gi, type: 'condition', target: 'Fatigado', badgeClass: 'ruby', tooltip: 'Ver Condição Fatigado (Pág. 395)' },
  { regex: /\b(enjoad[oas])\b/gi, type: 'condition', target: 'Enjoado', badgeClass: 'ruby', tooltip: 'Ver Condição Enjoado (Pág. 394)' },
  { regex: /\b(enredad[oas])\b/gi, type: 'condition', target: 'Enredado', badgeClass: 'ruby', tooltip: 'Ver Condição Enredado (Pág. 395)' },
  { regex: /\b(envenenad[oas])\b/gi, type: 'condition', target: 'Envenenado', badgeClass: 'ruby', tooltip: 'Ver Condição Envenenado (Pág. 395)' },
  { regex: /\b(fascinad[oas])\b/gi, type: 'condition', target: 'Fascinado', badgeClass: 'ruby', tooltip: 'Ver Condição Fascinado (Pág. 395)' },
  { regex: /\b(ofuscad[oas])\b/gi, type: 'condition', target: 'Ofuscado', badgeClass: 'ruby', tooltip: 'Ver Condição Ofuscado (Pág. 395)' },
  { regex: /\b(petrificad[oas])\b/gi, type: 'condition', target: 'Petrificado', badgeClass: 'ruby', tooltip: 'Ver Condição Petrificado (Pág. 395)' },
  { regex: /\b(sobrecarregad[oas])\b/gi, type: 'condition', target: 'Sobrecarregado', badgeClass: 'ruby', tooltip: 'Ver Condição Sobrecarregado (Pág. 395)' },
  { regex: /\b(surd[oas])\b/gi, type: 'condition', target: 'Surdo', badgeClass: 'ruby', tooltip: 'Ver Condição Surdo (Pág. 395)' },
  { regex: /\b(surpreendid[oas])\b/gi, type: 'condition', target: 'Surpreendido', badgeClass: 'ruby', tooltip: 'Ver Condição Surpreendido (Pág. 395)' },
  { regex: /\b(esmorecid[oas])\b/gi, type: 'condition', target: 'Esmorecido', badgeClass: 'ruby', tooltip: 'Ver Condição Esmorecido (Pág. 395)' },
  { regex: /\b(frustrad[oas])\b/gi, type: 'condition', target: 'Frustrado', badgeClass: 'ruby', tooltip: 'Ver Condição Frustrado (Pág. 395)' },
  { regex: /\b(abalad[oas])\b/gi, type: 'condition', target: 'Abalado', badgeClass: 'ruby', tooltip: 'Ver Condição Abalado (Pág. 394)' },
  { regex: /\b(apavorad[oas])\b/gi, type: 'condition', target: 'Apavorado', badgeClass: 'ruby', tooltip: 'Ver Condição Apavorado (Pág. 394)' },
  { regex: /\b(atordoad[oas])\b/gi, type: 'condition', target: 'Atordoado', badgeClass: 'ruby', tooltip: 'Ver Condição Atordoado (Pág. 394)' },
  { regex: /\b(confus[oas])\b/gi, type: 'condition', target: 'Confuso', badgeClass: 'ruby', tooltip: 'Ver Condição Confuso (Pág. 394)' },
  { regex: /\b(doente(?:s)?)\b/gi, type: 'condition', target: 'Doente', badgeClass: 'ruby', tooltip: 'Ver Condição Doente (Pág. 394)' },
  { regex: /\b(em chamas)\b/gi, type: 'condition', target: 'Em Chamas', badgeClass: 'ruby', tooltip: 'Ver Condição Em Chamas (Pág. 394)' },
  { regex: /\b(enfeiti[cç]ad[oas])\b/gi, type: 'condition', target: 'Enfeitiçado', badgeClass: 'ruby', tooltip: 'Ver Condição Enfeitiçado (Pág. 394)' },
  { regex: /\b(pasm[oas])\b/gi, type: 'condition', target: 'Pasmo', badgeClass: 'ruby', tooltip: 'Ver Condição Pasmo (Pág. 395)' },
  { regex: /\b(alquebrad[oas])\b/gi, type: 'condition', target: 'Alquebrado', badgeClass: 'ruby', tooltip: 'Ver Condição Alquebrado (Pág. 394)' },

  // Formas de Área
  { regex: /\b(cilindro)\b/gi, type: 'section', tab: 'tabela', target: 'section-areas', badgeClass: 'mana', tooltip: 'Ver Forma Cilindro (Pág. 225)' },
  { regex: /\b(esfera)\b/gi, type: 'section', tab: 'tabela', target: 'section-areas', badgeClass: 'mana', tooltip: 'Ver Forma Esfera (Pág. 225)' },
  { regex: /\b(cone)\b/gi, type: 'section', tab: 'tabela', target: 'section-areas', badgeClass: 'mana', tooltip: 'Ver Forma Cone (Pág. 225)' }
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
  const [copiedSectionId, setCopiedSectionId] = useState<string | null>(null);
  const [isImageZoomed, setIsImageZoomed] = useState<boolean>(false);

  // Helper de cópia individual por seção/card com feedback visual
  const handleCopySection = (id: string, text: string) => {
    navigator.clipboard.writeText(text.trim());
    setCopiedSectionId(id);
    setTimeout(() => {
      setCopiedSectionId(prev => (prev === id ? null : prev));
    }, 2200);
  };

  // Navegação entre abas e scroll suave para âncora/elemento
  const handleNavigateToSection = (tab: 'manobras' | 'condicoes' | 'tabela', elementId?: string) => {
    setActiveTab(tab);
    setTimeout(() => {
      if (elementId) {
        const el = document.getElementById(elementId);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          return;
        }
      }
      if (bodyRef.current) bodyRef.current.scrollTop = 0;
    }, 60);
  };

  const handleSelectManeuver = (maneuverId: string) => {
    setActiveTab('manobras');
    setExpandedManeuverId(maneuverId);
    setTimeout(() => {
      const el = document.getElementById(maneuverId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 60);
  };

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
      const term = removeAccents(condSearch.trim());
      return (
        removeAccents(item.name).includes(term) ||
        removeAccents(item.description).includes(term) ||
        (item.type && removeAccents(item.type).includes(term))
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

  const handleSelectChip = (targetName: string) => {
    const normTarget = removeAccents(targetName);
    const condMatch = CANONICAL_CONDITIONS.find(
      c => removeAccents(c.name) === normTarget
    );
    if (condMatch) {
      setActiveTab('condicoes');
      setCondSearch(condMatch.name);
      setSelectedCondType('Todas');
      setExpandedCondName(condMatch.name);
      if (bodyRef.current) bodyRef.current.scrollTop = 0;
      return;
    }

    const manMatch = CANONICAL_MANEUVERS.find(
      m => removeAccents(m.name) === normTarget
    );
    if (manMatch) {
      setActiveTab('manobras');
      setExpandedManeuverId(manMatch.id);
      if (bodyRef.current) bodyRef.current.scrollTop = 0;
      return;
    }

    setActiveTab('condicoes');
    setCondSearch(targetName);
    if (bodyRef.current) bodyRef.current.scrollTop = 0;
  };

  // Renderizador inteligente de links e chips dentro de qualquer texto de regra
  const renderLinkedRuleText = (text: string, currentSelfTerm?: string): React.ReactNode => {
    if (!text) return null;
    const selfNormalized = currentSelfTerm ? removeAccents(currentSelfTerm) : null;

    interface FoundMatch {
      start: number;
      end: number;
      matchedText: string;
      rule: KeywordRule;
    }

    const matches: FoundMatch[] = [];

    for (const rule of KEYWORD_RULES) {
      if (selfNormalized && removeAccents(rule.target) === selfNormalized) {
        continue;
      }
      const regex = new RegExp(rule.regex.source, rule.regex.flags);
      let m: RegExpExecArray | null;
      while ((m = regex.exec(text)) !== null) {
        const start = m.index;
        const end = start + m[0].length;
        const overlaps = matches.some(existing => !(end <= existing.start || start >= existing.end));
        if (!overlaps) {
          matches.push({
            start,
            end,
            matchedText: m[0],
            rule
          });
        }
      }
    }

    if (matches.length === 0) {
      return text;
    }

    matches.sort((a, b) => a.start - b.start);

    const elements: React.ReactNode[] = [];
    let cursor = 0;

    matches.forEach((match, idx) => {
      if (match.start > cursor) {
        elements.push(text.substring(cursor, match.start));
      }

      elements.push(
        <button
          key={`chip-${match.rule.target}-${idx}-${match.start}`}
          type="button"
          className={`badge-${match.rule.badgeClass} cond-chip interactive-chip inline-chip`}
          onClick={(e) => {
            e.stopPropagation();
            if (match.rule.type === 'condition') {
              handleSelectChip(match.rule.target);
            } else if (match.rule.type === 'maneuver') {
              handleSelectManeuver(match.rule.target);
            } else if (match.rule.tab) {
              handleNavigateToSection(match.rule.tab, match.rule.target);
            }
          }}
          title={match.rule.tooltip}
        >
          {match.matchedText}
        </button>
      );

      cursor = match.end;
    });

    if (cursor < text.length) {
      elements.push(text.substring(cursor));
    }

    return <>{elements}</>;
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
              <div id="section-size-modifiers" className="size-modifiers-banner parchment-subcard">
                <div className="size-banner-header">
                  <div className="flex items-center gap-2">
                    <Zap size={18} className="text-gold" />
                    <h4>Modificadores de Tamanho em Manobras (Pág. 238)</h4>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'size-mods' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '⚖️ MODIFICADORES DE TAMANHO EM MANOBRAS (Pág. 238)',
                        'Ao realizar ou resistir a qualquer manobra de combate, aplique o modificador no teste de Luta:',
                        ...CANONICAL_SIZE_MODIFIERS.map(s => `• ${s.size}: ${s.mod}`),
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('size-mods', text);
                    }}
                    title="Copiar Modificadores de Tamanho formatados"
                    aria-label="Copiar Modificadores de Tamanho"
                  >
                    {copiedSectionId === 'size-mods' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar</span>
                      </>
                    )}
                  </button>
                </div>
                <p className="size-banner-text">
                  Ao realizar ou resistir a qualquer {renderLinkedRuleText('manobra de combate', 'modificadores de tamanho')}, aplique o modificador da criatura no teste de Luta:
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

              {/* Banner das Regras Gerais de Manobras */}
              <div id="section-maneuver-rules" className="cheat-section parchment-subcard">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <Swords size={18} className="text-gold" />
                    <h3>{CANONICAL_MANEUVER_GENERAL_RULES.title}</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'maneuver-rules-general' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        `⚔️ ${CANONICAL_MANEUVER_GENERAL_RULES.title}`,
                        `${CANONICAL_MANEUVER_GENERAL_RULES.description}\n`,
                        ...CANONICAL_MANEUVER_GENERAL_RULES.keyPoints.map(p => `• ${p}`),
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('maneuver-rules-general', text);
                    }}
                    title="Copiar Regras Gerais de Manobras formatadas"
                    aria-label="Copiar Regras Gerais de Manobras"
                  >
                    {copiedSectionId === 'maneuver-rules-general' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar</span>
                      </>
                    )}
                  </button>
                </div>
                <p className="cheat-desc">
                  {renderLinkedRuleText(CANONICAL_MANEUVER_GENERAL_RULES.description)}
                </p>
                <div className="maneuver-keypoints-list">
                  {CANONICAL_MANEUVER_GENERAL_RULES.keyPoints.map((point, idx) => (
                    <div key={idx} className="maneuver-keypoint-item">
                      <span className="keypoint-bullet">⚔️</span>
                      <div className="keypoint-text">{renderLinkedRuleText(point)}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Seção de Manobras Canônicas */}
              <div className="section-divider-title">
                <Swords size={16} />
                <span>Manobras de Combate (Pág. 238–239)</span>
              </div>

              <div id="section-maneuvers" className="maneuvers-list">
                {CANONICAL_MANEUVERS.map(man => {
                  const isExpanded = expandedManeuverId === man.id;
                  const copyKey = `man-${man.id}`;
                  const formatText = () => {
                    const conds = man.relatedConditions?.length ? `\n• Condições associadas: ${man.relatedConditions.join(', ')}` : '';
                    return [
                      `⚔️ ${man.name.toUpperCase()} (${man.actionType} • Pág. ${man.page})`,
                      `• Teste Oposto: ${man.opposedTest}`,
                      `• Descrição: ${man.description}${conds}`,
                      '— Tormenta20: Edição Jogo do Ano'
                    ].join('\n');
                  };

                  return (
                    <div 
                      key={man.id} 
                      id={man.id}
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
                          
                          <button
                            type="button"
                            className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCopySection(copyKey, formatText());
                            }}
                            title={`Copiar manobra ${man.name} formatada`}
                            aria-label={`Copiar manobra ${man.name}`}
                          >
                            {copiedSectionId === copyKey ? (
                              <>
                                <Check size={13} className="text-emerald" />
                                <span className="copy-label">Copiado!</span>
                              </>
                            ) : (
                              <>
                                <Copy size={13} />
                                <span className="copy-label">Copiar</span>
                              </>
                            )}
                          </button>

                          <button className="expand-icon-btn" aria-label="Expandir Manobra">
                            {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                          </button>
                        </div>
                      </div>

                      {/* Texto Integral */}
                      <div className="maneuver-body">
                        <p className="maneuver-description">
                          {renderLinkedRuleText(man.description, man.name)}
                        </p>

                        {man.relatedConditions && man.relatedConditions.length > 0 && (
                          <div className="maneuver-conditions-row">
                            <span className="cond-rel-label">Condições associadas:</span>
                            {man.relatedConditions.map(c => (
                              <button 
                                key={c} 
                                type="button"
                                className="badge-ruby cond-chip interactive-chip inline-chip"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleSelectChip(c);
                                }}
                                title={`Ver detalhes da condição ${c}`}
                              >
                                {c}
                              </button>
                            ))}
                          </div>
                        )}

                        {/* Barra de ações quando o card está expandido (Permite fechar o modal no mobile e copiar) */}
                        <div className="card-expanded-actions">
                          <button
                            type="button"
                            className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCopySection(copyKey, formatText());
                            }}
                          >
                            {copiedSectionId === copyKey ? (
                              <>
                                <Check size={13} className="text-emerald" />
                                <span>Copiado!</span>
                              </>
                            ) : (
                              <>
                                <Copy size={13} />
                                <span>Copiar Manobra</span>
                              </>
                            )}
                          </button>

                          <button
                            type="button"
                            className="card-close-modal-btn"
                            onClick={(e) => {
                              e.stopPropagation();
                              onClose();
                            }}
                            title="Fechar Tomo de Consulta"
                            aria-label="Fechar Tomo"
                          >
                            <X size={14} />
                            <span>Fechar Tomo</span>
                          </button>
                        </div>
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

              <div id="section-actions" className="actions-info-grid">
                {CANONICAL_ACTIONS.map(act => {
                  const copyKey = `act-${act.name}`;
                  const formatText = () => {
                    return [
                      `⏱️ ${act.name.toUpperCase()} (Pág. ${act.page})`,
                      `• Tipo: ${act.type}`,
                      `• Descrição: ${act.description}`,
                      `• Exemplos: ${act.examples}`,
                      '— Tormenta20: Edição Jogo do Ano'
                    ].join('\n');
                  };

                  return (
                    <div key={act.name} className="action-info-card parchment-subcard">
                      <div className="action-info-header justify-between">
                        <div className="flex items-center gap-2">
                          <span className="badge-parchment action-badge-name">{act.name}</span>
                          <span className="maneuver-page">pág. {act.page}</span>
                        </div>
                        <button
                          type="button"
                          className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCopySection(copyKey, formatText());
                          }}
                          title={`Copiar ${act.name} formatada`}
                          aria-label={`Copiar ${act.name}`}
                        >
                          {copiedSectionId === copyKey ? (
                            <>
                              <Check size={12} className="text-emerald" />
                              <span className="copy-label">Copiado!</span>
                            </>
                          ) : (
                            <>
                              <Copy size={12} />
                              <span className="copy-label">Copiar</span>
                            </>
                          )}
                        </button>
                      </div>
                      <p className="action-info-desc">{renderLinkedRuleText(act.description, act.name)}</p>
                      <div className="action-info-examples">
                        <strong>Exemplos:</strong> {renderLinkedRuleText(act.examples)}
                      </div>
                    </div>
                  );
                })}
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
                  title="Copiar lista de condições filtradas"
                >
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                  <span>{copied ? 'Copiado!' : 'Copiar Todas'}</span>
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
                    const copyKey = `cond-${cond.name}`;
                    const formatText = () => {
                      const typeStr = cond.type ? ` [${cond.type}]` : '';
                      const rel = cond.relatedConditions?.length ? `\n• Gera / relaciona com: ${cond.relatedConditions.join(', ')}` : '';
                      return [
                        `🩸 ${cond.name.toUpperCase()}${typeStr} (Pág. ${cond.page})`,
                        cond.description + rel,
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                    };

                    return (
                      <div 
                        key={cond.name} 
                        id={`cond-${cond.name}`}
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

                          <div className="flex items-center gap-2">
                            <button
                              type="button"
                              className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleCopySection(copyKey, formatText());
                              }}
                              title={`Copiar condição ${cond.name} formatada`}
                              aria-label={`Copiar condição ${cond.name}`}
                            >
                              {copiedSectionId === copyKey ? (
                                <>
                                  <Check size={13} className="text-emerald" />
                                  <span className="copy-label">Copiado!</span>
                                </>
                              ) : (
                                <>
                                  <Copy size={13} />
                                  <span className="copy-label">Copiar</span>
                                </>
                              )}
                            </button>

                            <button className="expand-icon-btn" aria-label="Expandir Condição">
                              {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </button>
                          </div>
                        </div>

                        <div className="condition-item-body">
                          <p className="condition-text">
                            {renderLinkedRuleText(cond.description, cond.name)}
                          </p>

                          {cond.relatedConditions && cond.relatedConditions.length > 0 && (
                            <div className="maneuver-conditions-row mt-2">
                              <span className="cond-rel-label">Gera / relaciona com:</span>
                              {cond.relatedConditions.map(r => (
                                <button
                                  key={r}
                                  type="button"
                                  className="badge-ruby cond-chip interactive-chip inline-chip"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleSelectChip(r);
                                  }}
                                  title={`Ver detalhes da condição ${r}`}
                                >
                                  {r}
                                </button>
                              ))}
                            </div>
                          )}

                          {/* Ações do card expandido: copiar e fechar modal no mobile */}
                          <div className="card-expanded-actions">
                            <button
                              type="button"
                              className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleCopySection(copyKey, formatText());
                              }}
                            >
                              {copiedSectionId === copyKey ? (
                                <>
                                  <Check size={13} className="text-emerald" />
                                  <span>Copiado!</span>
                                </>
                              ) : (
                                <>
                                  <Copy size={13} />
                                  <span>Copiar Condição</span>
                                </>
                              )}
                            </button>

                            <button
                              type="button"
                              className="card-close-modal-btn"
                              onClick={(e) => {
                                e.stopPropagation();
                                onClose();
                              }}
                              title="Fechar Tomo de Consulta"
                              aria-label="Fechar Tomo"
                            >
                              <X size={14} />
                              <span>Fechar Tomo</span>
                            </button>
                          </div>
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
              <div id="section-rest" className="cheat-section parchment-subcard">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <Moon size={20} className="text-mana" />
                    <h3>Descanso e Recuperação (Pág. 224)</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'sec-rest' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '🌙 DESCANSO E RECUPERAÇÃO (Pág. 224)',
                        'Um descanso de 8 horas permite recuperar Pontos de Vida (PV) e Pontos de Mana (PM):',
                        '• Ruim (Acampamento ao relento): PV e PM = 1x nível',
                        '• Normal (Estalagem comum, barraca confortável): PV e PM = 2x nível',
                        '• Confortável (Quarto de luxo, mansão nobre): PV e PM = 3x nível',
                        '• Luxuoso (Palácio real, santuário protegido): PV e PM = 4x nível',
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('sec-rest', text);
                    }}
                    title="Copiar tabela de Descanso e Recuperação formatada"
                    aria-label="Copiar Descanso e Recuperação"
                  >
                    {copiedSectionId === 'sec-rest' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar</span>
                      </>
                    )}
                  </button>
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
              <div id="section-stacking" className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles size={20} className="text-gold" />
                    <h3>Acúmulo de Bônus e Efeitos (Pág. 226)</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'sec-stacking' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '✨ ACÚMULO DE BÔNUS E EFEITOS (Pág. 226)',
                        '• Mesma Fonte: Bônus de mesma fonte (duas magias, dois itens com o mesmo encanto, ou a mesma habilidade usada duas vezes) NÃO se acumulam — aplique apenas o maior.',
                        '• Fontes Diferentes: Bônus de tipos e fontes diferentes (um item, uma magia e uma habilidade de classe) se acumulam normalmente.',
                        '• Penalidades: Penalidades sempre se acumulam, a menos que venham da mesma condição ou efeito idêntico.',
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('sec-stacking', text);
                    }}
                    title="Copiar regras de Acúmulo de Bônus formatadas"
                    aria-label="Copiar Acúmulo de Bônus"
                  >
                    {copiedSectionId === 'sec-stacking' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar</span>
                      </>
                    )}
                  </button>
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
              <div id="section-modifiers" className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <ShieldAlert size={20} className="text-ruby" />
                    <h3>Cobertura, Camuflagem e Modificadores de Combate (Pág. 225, 237)</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'sec-modifiers' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '🛡️ COBERTURA, CAMUFLAGEM E MODIFICADORES DE COMBATE (Pág. 225, 237)',
                        '• Cobertura Leve: +2 na Defesa (Mureta baixa, criatura no caminho - Pág. 237)',
                        '• Cobertura Total: +5 na Defesa (Parede inteira, obstáculo sólido - Pág. 237)',
                        '• Camuflagem Leve: 20% de chance de erro (Névoa suave, penumbra, folhagem - Pág. 238)',
                        '• Camuflagem Total: 50% de chance de erro (Escuridão total, invisibilidade. Alvo considerado Cego - Pág. 238)',
                        '• Flanquear: +2 no teste de ataque corpo a corpo (Aliado no lado oposto do alvo - Pág. 237)',
                        '• Posição Elevada: +2 no teste de ataque corpo a corpo (Atacando de cima de mesa, montaria ou terreno alto - Pág. 237)',
                        '• Investida: +2 no teste de ataque / –2 na Defesa (Avança o dobro do deslocamento em linha reta - Pág. 238)',
                        '• Alvo Caído: –5 Defesa (C. a C.) / +5 Defesa (Distância)',
                        '• Alvo Desprevenido: –5 na Defesa e –5 em Reflexos',
                        '• Alvo Indefeso: –10 na Defesa / Falha automática em Reflexos',
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('sec-modifiers', text);
                    }}
                    title="Copiar tabela de Cobertura, Camuflagem e Modificadores formatada"
                    aria-label="Copiar Modificadores de Combate"
                  >
                    {copiedSectionId === 'sec-modifiers' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar</span>
                      </>
                    )}
                  </button>
                </div>
                <div className="cheat-table-wrapper">
                  <table className="cheat-table">
                    <thead>
                      <tr>
                        <th>Situação</th>
                        <th>Efeito Mecânico</th>
                        <th>Referência & Condição</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td><strong>Cobertura Leve</strong></td>
                        <td><span className="badge-emerald">+2 na Defesa</span></td>
                        <td>Mureta baixa, criatura no caminho (Pág. 237)</td>
                      </tr>
                      <tr>
                        <td><strong>Cobertura Total</strong></td>
                        <td><span className="badge-emerald">+5 na Defesa</span></td>
                        <td>Parede inteira, obstáculo sólido total (Pág. 237)</td>
                      </tr>
                      <tr>
                        <td><strong>Camuflagem Leve</strong></td>
                        <td><span className="badge-amber">20% de chance de erro (1 em 1d5)</span></td>
                        <td>Névoa suave, penumbra, folhagem (Pág. 238)</td>
                      </tr>
                      <tr>
                        <td><strong>Camuflagem Total</strong></td>
                        <td><span className="badge-ruby">50% de chance de erro (1-5 em 1d10)</span></td>
                        <td>
                          Escuridão total, invisibilidade. Alvo considerado{' '}
                          <button
                            type="button"
                            className="badge-ruby cond-chip interactive-chip inline-chip"
                            onClick={() => handleSelectChip('Cego')}
                          >
                            Cego
                          </button>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Flanquear</strong></td>
                        <td><span className="badge-gold">+2 no teste de ataque corpo a corpo</span></td>
                        <td>Aliado no lado oposto do alvo (Pág. 237)</td>
                      </tr>
                      <tr>
                        <td><strong>Posição Elevada</strong></td>
                        <td><span className="badge-gold">+2 no teste de ataque corpo a corpo</span></td>
                        <td>Atacando de cima de mesa, montaria ou terreno alto (Pág. 237)</td>
                      </tr>
                      <tr>
                        <td><strong>Investida</strong></td>
                        <td><span className="badge-gold">+2 no teste de ataque</span> / <span className="badge-ruby">–2 na Defesa</span></td>
                        <td>Avança o dobro do deslocamento em linha reta (Pág. 238)</td>
                      </tr>
                      <tr>
                        <td><strong>Alvo Caído</strong></td>
                        <td><span className="badge-ruby">–5 Defesa (C. a C.)</span> / <span className="badge-emerald">+5 Defesa (Distância)</span></td>
                        <td>
                          Alvo na condição{' '}
                          <button
                            type="button"
                            className="badge-ruby cond-chip interactive-chip inline-chip"
                            onClick={() => handleSelectChip('Caído')}
                          >
                            Caído
                          </button>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Alvo Desprevenido</strong></td>
                        <td><span className="badge-ruby">–5 na Defesa e –5 em Reflexos</span></td>
                        <td>
                          Alvo na condição{' '}
                          <button
                            type="button"
                            className="badge-ruby cond-chip interactive-chip inline-chip"
                            onClick={() => handleSelectChip('Desprevenido')}
                          >
                            Desprevenido
                          </button>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Alvo Indefeso</strong></td>
                        <td><span className="badge-ruby">–10 Defesa / Falha auto em Reflexos</span></td>
                        <td>
                          Alvo na condição{' '}
                          <button
                            type="button"
                            className="badge-ruby cond-chip interactive-chip inline-chip"
                            onClick={() => handleSelectChip('Indefeso')}
                          >
                            Indefeso
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Saúde, Sangramento e Morte */}
              <div id="section-health" className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header">
                  <ShieldAlert size={20} className="text-ruby" />
                  <h3>Saúde, Sangramento e Morte (Pág. 239–240)</h3>
                </div>
                <div className="health-rules-grid">
                  {CANONICAL_HEALTH_RULES.map(rule => {
                    const copyKey = `health-${rule.title}`;
                    const formatText = () => {
                      return [
                        `❤️ ${rule.title.toUpperCase()} [${rule.badge}] (Pág. ${rule.page})`,
                        rule.description,
                        rule.mechanicalDetails,
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                    };

                    return (
                      <div key={rule.title} className="health-card parchment-subcard">
                        <div className="health-card-header justify-between">
                          <div className="flex items-center gap-2">
                            <span className={`badge-${rule.badgeClass}`}>{rule.badge}</span>
                            <span className="maneuver-page">pág. {rule.page}</span>
                          </div>
                          <button
                            type="button"
                            className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCopySection(copyKey, formatText());
                            }}
                            title={`Copiar regra ${rule.title} formatada`}
                            aria-label={`Copiar regra ${rule.title}`}
                          >
                            {copiedSectionId === copyKey ? (
                              <>
                                <Check size={12} className="text-emerald" />
                                <span className="copy-label">Copiado!</span>
                              </>
                            ) : (
                              <>
                                <Copy size={12} />
                                <span className="copy-label">Copiar</span>
                              </>
                            )}
                          </button>
                        </div>
                        <h4 className="health-card-title">{rule.title}</h4>
                        <p className="health-card-desc">{renderLinkedRuleText(rule.description)}</p>
                        <pre className="health-card-details">{rule.mechanicalDetails}</pre>
                        
                        {rule.relatedConditions && rule.relatedConditions.length > 0 && (
                          <div className="maneuver-conditions-row mt-2">
                            <span className="cond-rel-label">Condições:</span>
                            {rule.relatedConditions.map(c => (
                              <button
                                key={c}
                                type="button"
                                className="badge-ruby cond-chip interactive-chip inline-chip"
                                onClick={() => handleSelectChip(c)}
                                title={`Ir para condição ${c}`}
                              >
                                {c}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Categorias de Alcance */}
              <div id="section-ranges" className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <Zap size={20} className="text-gold" />
                    <h3>Categorias de Alcance (Pág. 138, 224)</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'sec-ranges' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '🎯 CATEGORIAS DE ALCANCE (Pág. 138, 224)',
                        ...CANONICAL_RANGES.map(r => `• ${r.name} (${r.distance}): ${r.description} (Exemplos: ${r.examples})`),
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('sec-ranges', text);
                    }}
                    title="Copiar todas as Categorias de Alcance formatadas"
                    aria-label="Copiar Categorias de Alcance"
                  >
                    {copiedSectionId === 'sec-ranges' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar Todos</span>
                      </>
                    )}
                  </button>
                </div>
                <div className="range-grid">
                  {CANONICAL_RANGES.map(r => {
                    const copyKey = `range-${r.name}`;
                    const formatText = () => {
                      return [
                        `🎯 ALCANCE ${r.name.toUpperCase()} (${r.distance}) (Pág. 138, 224)`,
                        `• Descrição: ${r.description}`,
                        `• Exemplos: ${r.examples}`,
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                    };

                    return (
                      <div key={r.name} className="range-card parchment-subcard">
                        <div className="range-card-header justify-between">
                          <div className="flex items-center gap-2">
                            <span className="range-name">{r.name}</span>
                            <span className="badge-gold range-dist">{r.distance}</span>
                          </div>
                          <button
                            type="button"
                            className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCopySection(copyKey, formatText());
                            }}
                            title={`Copiar alcance ${r.name} formatado`}
                            aria-label={`Copiar alcance ${r.name}`}
                          >
                            {copiedSectionId === copyKey ? (
                              <>
                                <Check size={12} className="text-emerald" />
                                <span className="copy-label">Copiado!</span>
                              </>
                            ) : (
                              <>
                                <Copy size={12} />
                                <span className="copy-label">Copiar</span>
                              </>
                            )}
                          </button>
                        </div>
                        <p className="range-desc">{renderLinkedRuleText(r.description, r.name)}</p>
                        <div className="range-examples">
                          <strong>Exemplos:</strong> {renderLinkedRuleText(r.examples)}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Espaço Ocupado e Alcance por Tamanho */}
              <div id="section-creature-sizes" className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <Layers size={20} className="text-mana" />
                    <h3>Espaço Ocupado, Alcance Natural e Tamanho (Pág. 106, 238)</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'sec-creature-sizes' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '📐 ESPAÇO OCUPADO, ALCANCE NATURAL E TAMANHO (Pág. 106, 238)',
                        ...CANONICAL_CREATURE_SIZES.map(s => `• ${s.size}: Espaço ${s.space} | Alcance ${s.reach} | Furtividade ${s.stealthMod} | Manobra ${s.maneuverMod}`),
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('sec-creature-sizes', text);
                    }}
                    title="Copiar tabela de Espaço e Alcance por Tamanho formatada"
                    aria-label="Copiar Espaço e Tamanho"
                  >
                    {copiedSectionId === 'sec-creature-sizes' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar</span>
                      </>
                    )}
                  </button>
                </div>
                <div className="cheat-table-wrapper">
                  <table className="cheat-table">
                    <thead>
                      <tr>
                        <th>Tamanho da Criatura</th>
                        <th>Espaço Ocupado (Quadrados)</th>
                        <th>Alcance Natural</th>
                        <th>Furtividade</th>
                        <th>Manobra (Luta)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {CANONICAL_CREATURE_SIZES.map(s => (
                        <tr key={s.size}>
                          <td><strong>{s.size}</strong></td>
                          <td>{s.space}</td>
                          <td>{s.reach}</td>
                          <td>
                            <span className={s.stealthMod.startsWith('+') ? 'text-emerald' : s.stealthMod.startsWith('–') ? 'text-ruby' : ''}>
                              {s.stealthMod}
                            </span>
                          </td>
                          <td>
                            <span className={s.maneuverMod.startsWith('+') ? 'text-emerald font-bold' : s.maneuverMod.startsWith('–') ? 'text-ruby font-bold' : ''}>
                              {s.maneuverMod}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Áreas de Efeito, Alvos e Duração (Pág. 225) */}
              <div id="section-areas" className="cheat-section parchment-subcard mt-4">
                <div className="cheat-section-header justify-between">
                  <div className="flex items-center gap-2">
                    <Target size={20} className="text-ruby" />
                    <h3>Áreas de Efeito, Alvos e Duração (Pág. 225)</h3>
                  </div>
                  <button
                    type="button"
                    className={`section-copy-btn ${copiedSectionId === 'sec-areas-summary' ? 'copied' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      const text = [
                        '🔮 ÁREAS DE EFEITO, ALVOS E DURAÇÃO (Pág. 225)',
                        '• ALVO: Afeta diretamente uma ou mais criaturas/objetos específicos escolhidos dentro do alcance (requer linha de efeito).',
                        '• ÁREA: Afeta um espaço físico inteiro e tudo contido nele (origem definida na grade tática).',
                        '• EFEITO: Cria algo físico ou mágico no campo de batalha em vez de afetar algo pré-existente.',
                        '• DURAÇÃO: Instantânea, Cena (~10 min), Sustentada (gasta 1 PM no início do turno) ou Permanente.',
                        '\nModelos de Formas:',
                        ...CANONICAL_AREA_EFFECTS.map(a => `• ${a.name}: ${a.description} (${a.gridRule})`),
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                      handleCopySection('sec-areas-summary', text);
                    }}
                    title="Copiar resumo de Áreas de Efeito formatado"
                    aria-label="Copiar Áreas de Efeito"
                  >
                    {copiedSectionId === 'sec-areas-summary' ? (
                      <>
                        <Check size={13} className="text-emerald" />
                        <span className="copy-label">Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={13} />
                        <span className="copy-label">Copiar Resumo</span>
                      </>
                    )}
                  </button>
                </div>
                <p className="cheat-desc">
                  Muitas magias e habilidades afetam áreas específicas da grade tática ou alvos individuais. Conforme as regras oficiais de Tormenta20 (Jogo do Ano, Pág. 225):
                </p>

                {/* Categorias de Alvo, Área, Efeito e Duração */}
                <div className="stacking-rules-grid mb-4">
                  {CANONICAL_SPELL_TARGET_TYPES.map(t => (
                    <div key={t.title} className="stacking-box rule-stack">
                      <div className="flex items-center justify-between mb-1">
                        <h4>{t.title}</h4>
                        <span className="badge-gold text-xs">{t.badge}</span>
                      </div>
                      <p>{renderLinkedRuleText(t.description, t.title)}</p>
                    </div>
                  ))}
                </div>

                {/* Banner com a Imagem Oficial do Livro (Pág. 225) */}
                <div className="section-divider-title mb-3">
                  <Maximize2 size={16} />
                  <span>Ilustração Oficial: Grade Tática de Áreas de Efeito (Livro Pág. 225)</span>
                </div>

                <div 
                  className="official-book-image-card parchment-subcard"
                  onClick={() => setIsImageZoomed(true)}
                  title="Clique para ampliar o diagrama oficial em tela cheia"
                >
                  <div className="book-image-wrapper">
                    <img 
                      src={bookAreasImg} 
                      alt="Modelos Oficiais de Áreas de Efeito - Tormenta20 Edição Jogo do Ano Pág. 225" 
                      className="official-book-img"
                      loading="lazy"
                    />
                    <div className="image-zoom-overlay">
                      <Maximize2 size={24} />
                      <span>Clique para Zoom em Alta Resolução</span>
                    </div>
                  </div>
                  <div className="book-image-caption">
                    <span>📜 <em>Tormenta20: Edição Jogo do Ano • Pág. 225</em> — Ilustração oficial com modelos em grade tática</span>
                  </div>
                </div>

                {/* Lista de Formas de Área Canônicas */}
                <div className="area-effects-grid mt-4">
                  {CANONICAL_AREA_EFFECTS.map(area => {
                    const copyKey = `area-${area.shape}`;
                    const formatText = () => {
                      return [
                        `📐 ÁREA DE EFEITO: ${area.name.toUpperCase()} (Pág. ${area.page})`,
                        `• Descrição: ${area.description}`,
                        `• Regra na Grade: ${area.gridRule}`,
                        '— Tormenta20: Edição Jogo do Ano'
                      ].join('\n');
                    };

                    return (
                      <div key={area.shape} className="area-card parchment-subcard">
                        <div className="area-card-header justify-between">
                          <div className="flex items-center gap-2">
                            <h4 className="area-card-title">{area.name}</h4>
                            <span className="maneuver-page">pág. {area.page}</span>
                          </div>
                          <button
                            type="button"
                            className={`section-copy-btn ${copiedSectionId === copyKey ? 'copied' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCopySection(copyKey, formatText());
                            }}
                            title={`Copiar modelo ${area.name} formatado`}
                            aria-label={`Copiar modelo ${area.name}`}
                          >
                            {copiedSectionId === copyKey ? (
                              <>
                                <Check size={12} className="text-emerald" />
                                <span className="copy-label">Copiado!</span>
                              </>
                            ) : (
                              <>
                                <Copy size={12} />
                                <span className="copy-label">Copiar</span>
                              </>
                            )}
                          </button>
                        </div>
                        <p className="area-card-desc">{renderLinkedRuleText(area.description, area.name)}</p>
                        <div className="area-card-rule">
                          <strong>Grade:</strong> {renderLinkedRuleText(area.gridRule)}
                        </div>
                      </div>
                    );
                  })}
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

        {/* Lightbox / Modal de Zoom em Alta Resolução da Imagem do Livro */}
        {isImageZoomed && (
          <div className="image-lightbox-backdrop" onClick={() => setIsImageZoomed(false)}>
            <div className="image-lightbox-content parchment-card ornate-border" onClick={e => e.stopPropagation()}>
              <div className="image-lightbox-header">
                <div className="flex items-center gap-2">
                  <Target size={18} className="text-ruby" />
                  <h3 className="lightbox-title">Áreas de Efeito na Grade Tática (Pág. 225)</h3>
                </div>
                <button 
                  className="quick-ref-close-btn" 
                  onClick={() => setIsImageZoomed(false)}
                  aria-label="Fechar Zoom"
                >
                  <X size={22} />
                </button>
              </div>
              <div className="image-lightbox-body">
                <img 
                  src={bookAreasImg} 
                  alt="Modelos Oficiais de Áreas de Efeito Ampliados" 
                  className="lightbox-full-img"
                />
              </div>
              <div className="image-lightbox-footer">
                <span className="footer-meta-note">Tormenta20: Edição Jogo do Ano • Ilustração Original Pág. 225</span>
                <button className="parchment-btn btn-gold" onClick={() => setIsImageZoomed(false)}>
                  Fechar Visualização
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
