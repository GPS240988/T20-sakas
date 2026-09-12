# 🗺️ Roadmap de Execução: Projeto Sakas (Tormenta20)

## Fase 1: Governança, Setup e Separação de Skills (Concluída / Em Curso)
- [x] Criação de `GAME_RULES.md` com o tema **Light Medieval Parchment** e regras de negócio.
- [x] Isolamento das 20 skills selecionadas na pasta `.agents/skills/`.
- [x] Criação do repositório de planejamento GSD (`.planning/`).

## Fase 2: Modelagem Canônica de Dados e Pipeline de Extração (PDFs -> JSON)
- [ ] Definição dos Schemas Canônicos em TypeScript/Zod para Entidades de Tormenta20 (Regras, Condições, Magias, Poderes, Itens, Criaturas).
- [ ] Criação do script de extração e parsing estruturado a partir dos 4 PDFs oficiais.
- [ ] Geração do banco de dados consolidado com metadados de rastreabilidade (livro, página, versão).

## Fase 3: Motor de Busca Universal & Armazenamento Offline-First
- [ ] Implementação da camada de armazenamento cliente (IndexedDB / Local Cache).
- [ ] Configuração do motor de busca local instantânea (FlexSearch / MiniSearch) com suporte a sinônimos e tags.
- [ ] Criação de endpoints locais para consulta de conceitos em < 50ms.

## Fase 4: Frontend Mobile-First & Design System Light Medieval
- [ ] Configuração da aplicação web (Vite/React/TypeScript + Vanilla CSS Design Tokens).
- [ ] Implementação das variáveis de tema *Light Medieval Parchment* (pergaminho, ouro nobre, rubi de Arton, nanquim).
- [ ] Componentes de busca universal, visualizador de regras em tomos/cards, badges de condições e gaveta de favoritos.

## Fase 5: Ações Rápidas de Mesa, PWA Offline e Polimento
- [ ] Suporte a Progressive Web App (PWA) e Service Worker com offline 100%.
- [ ] Painel de combate (consulta expressa de manobras e condições).
- [ ] Auditoria de performance, ergonomia touch e validação visual de fidelidade.
