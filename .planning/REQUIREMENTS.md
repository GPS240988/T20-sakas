# 📋 Requisitos do Projeto: Compêndio Tormenta20 (MVP)

## 1. Requisitos Funcionais (RF)

### RF01: Base de Conhecimento Consolidada
- O sistema deve integrar o conteúdo dos 4 PDFs oficiais (*Jogo do Ano*, *Ameaças*, *Atlas*, *Heróis*) em uma única base de dados relacional/orientada a documentos.
- Entidades duplicadas ou atualizadas devem ser mescladas em uma única entidade canônica com histórico de publicação.

### RF02: Rastreabilidade de Regras
- Cada entidade deve exibir o nome do livro oficial e o número exato da página de onde o texto foi extraído.
- Se houver errata oficial ou nota de esclarecimento, deve ser exibida como tag suplementar demarcada.

### RF03: Busca Universal Instantânea
- O sistema deve fornecer uma barra de busca global acessível em qualquer tela.
- A busca deve operar com pesquisa por texto completo, prefixo, fonética/aproximação e tags de jogo (ex.: "Magia 2º Círculo", "Manobra", "Condição", "Veneno").
- A resposta da busca deve ser imediata (< 50ms) no cliente.

### RF04: Navegação por Conceito de Jogo
- Categorias de busca:
  - **Regras & Combate** (Ações, Manobras, Descanso, Terreno, Sufocamento)
  - **Condições** (Abalado, Cego, Agarrado, Sangrando, etc.)
  - **Magias** (Arcanas, Divinas, Círculos, Escolas, Aprimoramentos)
  - **Poderes & Habilidades** (Gerais, Concedidos, de Classe, Tormenta)
  - **Equipamentos & Itens** (Armas, Armaduras, Esotéricos, Poções, Itens Superiores)
  - **Ameaças & Criaturas** (Fichas, ND, Tipo, Habilidades, Táticas)
  - **Geografia & Lore** (Reinos, Deuses, Organizações)

### RF05: Painel de Ações Rápidas de Mesa & Favoritos
- Permitir fixar regras e magias na bandeja de favoritos de acesso rápido.
- Calculadora/tabela de referência rápida de manobras e condições ativas.

---

## 2. Requisitos Não-Funcionais (RNF)

### RNF01: Arquitetura Offline-First
- A aplicação deve funcionar 100% offline após o primeiro carregamento, utilizando IndexedDB / Service Workers.

### RNF02: Ergonomia Mobile-First
- Elementos interativos com dimensões mínimas de $44 \times 44\text{px}$.
- Interface adaptada para navegação com polegar em smartphones.

### RNF03: Identidade Visual Light Medieval Parchment
- Implementação estrita do tema claro de pergaminho definido em `GAME_RULES.md`.
- Contraste visual em conformidade com WCAG AAA (texto nanquim escuro sobre fundo pergaminho claro).

### RNF04: Zero Fricção de Navegação
- Máximo de 3 cliques/toques da tela inicial até o conteúdo completo de qualquer regra.
