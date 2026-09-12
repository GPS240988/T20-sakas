# 📜 GAME RULES: PROJETO SAKAS (TORMENTA20)

> **DIRETRIZ SUPREMA DO PROJETO**: Qualquer alteração, criação ou refatoração no repositório "Project Sakas" DEVE respeitar rigorosamente este contrato de regras, padrões visuais e arquitetura.

---

## 1. 🎨 IDENTIDADE VISUAL: LIGHT MEDIEVAL PARCHMENT (PERGAMINHO DE ARTON)

O visual do projeto adota uma estética **Medieval Clara (Pergaminho Real de Arton)**, inspirada nos manuscritos e tomos da Grande Biblioteca de Valkaria. Substitui o dark fantasy tradicional por uma paleta clara, calorosa, elegante e de altíssima legibilidade para uso sob iluminação de mesa de RPG.

### 1.1. Sistema de Cores (Paleta HSL Semântica)
```css
:root {
  /* 📜 Canvas & Superfícies (Pergaminho Claro) */
  --bg-canvas: hsl(40, 35%, 94%);          /* Pergaminho suave de fundo */
  --bg-surface: hsl(40, 45%, 98%);         /* Superfície do cartão / tomo */
  --bg-surface-elevated: hsl(0, 0%, 100%);  /* Superfície elevada / popovers */
  --bg-surface-muted: hsl(38, 25%, 90%);    /* Áreas secundárias / tags */

  /* ⚜️ Acentos Nobres & Heráldica de Arton */
  --accent-gold: hsl(38, 82%, 40%);        /* Ouro nobre polido (botões / bordas nobres) */
  --accent-gold-light: hsl(42, 75%, 55%);  /* Destaque dourado suave */
  --accent-gold-subtle: hsla(38, 80%, 40%, 0.12); /* Fundo de destaque ouro */

  /* 🩸 Acentos Temáticos & Ações */
  --accent-ruby: hsl(350, 72%, 44%);       /* Rubi de Arton / Ataque / Dano / Alertas */
  --accent-ruby-subtle: hsla(350, 72%, 44%, 0.10);
  --accent-mana: hsl(215, 65%, 45%);       /* Azul Wynna / Pontos de Mana / Magias */
  --accent-mana-subtle: hsla(215, 65%, 45%, 0.10);
  --accent-emerald: hsl(150, 50%, 35%);    /* Verde Khalmyr / Cura / Sucesso / Vantagens */
  --accent-amber: hsl(32, 85%, 45%);       /* Âmbar de Tanna-Toh / Avisos / Notas */

  /* 🖋️ Tipografia & Contraste Máximo (Nanquim Escuro) */
  --text-primary: hsl(220, 24%, 15%);      /* Nanquim profundo (WCAG AAA) */
  --text-secondary: hsl(30, 15%, 38%);     /* Castanho pergaminho */
  --text-muted: hsl(30, 10%, 55%);         /* Metadados / Legendas */
  --text-inverse: hsl(40, 35%, 98%);       /* Texto sobre botões dourados/rubis */

  /* 🛡️ Bordas, Sombras & Glassmorphism Claro */
  --border-parchment: hsl(38, 30%, 82%);   /* Linhas divisórias suaves */
  --border-ornate: hsl(38, 55%, 68%);      /* Bordas de cartões com acabamento */
  --border-active: hsl(38, 82%, 45%);      /* Foco / Seleção */
  
  --shadow-sm: 0 1px 3px hsla(35, 30%, 20%, 0.08);
  --shadow-md: 0 4px 14px hsla(35, 30%, 20%, 0.09);
  --shadow-lg: 0 8px 24px hsla(35, 30%, 20%, 0.12);

  --glass-bg: hsla(40, 45%, 98%, 0.88);
  --glass-blur: blur(10px);
}
```

### 1.2. Regras de Design e Componentes
- **Legibilidade em Mesa:** Proibido fundos pretos/dark agressivos. Assegurar contraste superior a 7:1 para corpo de texto.
- **Glassmorphism Claro:** Usar cartões com leve transparência sobre textura de pergaminho suave, com bordas douradas/bronze sutis.
- **Micro-interações:** Feedback tátil suave em toques e cliques, transições de hover elegantes sem piscar.
- **Ícones & Heráldica:** Ícones limpos com acabamento metálico ou estilizado em nanquim/ouro.

---

## 2. 🏛️ DECISÕES DE PRODUTO & REGRAS DE CANONICIDADE T20

### 2.1. Base de Conhecimento Única (Sem Silos por Livro)
- A aplicação **NÃO** organiza sua navegação primária por livros.
- Os 4 livros-fonte alimentam um compêndio unificado de Tormenta20:
  1. *Tormenta20 Edição Jogo do Ano (v1.3)*
  2. *Ameaças de Arton (v1.0)*
  3. *Atlas de Arton (v1.0)*
  4. *Heróis de Arton (v1.1)*
- O usuário busca pelo **conceito de jogo** (ex.: "Agarrar", "Bola de Fogo", "Condição Cego", "Poder Geral") e tem **um único caminho principal**.

### 2.2. Preservação Integral das Regras Mecânicas
- **Inviolabilidade do Texto:** Todo conteúdo mecânico (regras, frases, fórmulas, requisitos, condições, exceções e resultados) deve ser preservado **literalmente** como consta nas publicações oficiais.
- **Proibição de Reinterpretação:** O sistema é estritamente proibido de "corrigir", resumir ou reinterpretar regras silenciosamente. 
- **Conteúdo Auxiliar/Erratas:** Dicas da comunidade ou esclarecimentos devem ser claramente rotulados com tags visuais dedicadas (`[Esclarecimento / FAQ]`, `[Errata Oficial]`).

### 2.3. Registro Canônico & Rastreabilidade
- Quando uma entidade/regra estiver em mais de um livro (ex.: atualização da Jogo do Ano vs suplementos), ela consolida-se em um **Registro Canônico**.
- Todo registro possui **metadados completos de rastreabilidade**:
  - `source_book`: Livro de origem canônico e referências cruzadas.
  - `page`: Número da página oficial.
  - `version`: Versão da publicação (ex.: v1.3).
  - `canonical_id`: Identificador único universal.

---

## 3. 📱 ARQUITETURA TÉCNICA, MOBILE-FIRST & OFFLINE-FIRST

### 3.1. Princípios de Engenharia
- **Mobile-First Real:** Projetado para operação com uma mão em celulares durante a sessão de RPG (alvos de toque $\ge 44\text{px}$, navegação inferior acessível).
- **Offline-First:** Todo o compêndio canônico e regras essenciais de consulta devem funcionar **100% offline** (IndexedDB / Local Cache / Service Worker).
- **Velocidade de Consulta (Zero Fricção):** Acesso à qualquer regra em **menos de 3 cliques** através da Busca Universal.

### 3.2. Estrutura de Estado e Dados
- **Gerenciamento de Estado Previsível:** Reducers puros, tipagem estrita com TypeScript/Zod para validação em runtime.
- **Indexação Instantânea:** Busca local rápida por prefixo, sinônimos e tags de jogo (MiniSearch / FlexSearch / Trie).
- **Favoritos e Ações Rápidas de Mesa:** Salvar condições ativas, magias preparadas e tabelas rápidas (manobras, descanso, sufocamento).

---

## 4. 🚫 PADRÕES PROIBIDOS (FORBIDDEN PATTERNS)

1. ❌ **Divisão por Livro na Navegação:** Criar menus onde o usuário precise escolher o livro antes de ver as magias/poderes/regras.
2. ❌ **Alteração Silenciosa de Regra:** Alterar valores numéricos de dano, alcance, PM ou texto oficial sem marcação explícita de errata.
3. ❌ **Visual Dark Puro/Ilegível:** Usar paletas pretas ou texto com baixo contraste que cansem a vista ou dificultem a leitura na mesa.
4. ❌ **Dependência Obrigatória de Conexão:** Fazer com que a busca de regras falhe quando não houver internet.
5. ❌ **Textos Cortados sem Expansão:** Cortar frases de regras com ellipsis (`...`) sem permitir a leitura completa imediata.
