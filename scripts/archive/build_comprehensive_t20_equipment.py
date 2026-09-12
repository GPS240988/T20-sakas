import json
import re
import os

os.makedirs("data/categories", exist_ok=True)

equipments = []

def create_item(id_slug, name, subcategory, proficiency, purpose, price, damage, critical, damage_type, range_dist, defense, penalty, space, book, page, description, tags=None, is_magic=False, rarity=None):
    if tags is None:
        tags = []
    
    # Adicionar tags essenciais para busca universal
    all_tags = set(["equipamento", subcategory.lower(), proficiency.lower(), purpose.lower(), name.lower()] + tags)
    
    table_data = {
        "price": price,
        "proficiency": proficiency,
        "purpose": purpose,
        "space": space
    }
    if damage: table_data["damage"] = damage
    if critical: table_data["critical"] = critical
    if damage_type: table_data["damageType"] = damage_type
    if range_dist and range_dist != "-": table_data["range"] = range_dist
    if defense is not None: table_data["defenseBonus"] = defense
    if penalty is not None: table_data["armorPenalty"] = penalty
    
    summary_parts = [f"{proficiency} ({purpose})"]
    if damage: summary_parts.append(f"Dano: {damage} ({critical})")
    if defense is not None: summary_parts.append(f"Defesa: +{defense}")
    if penalty is not None and penalty != 0: summary_parts.append(f"Penalidade: {penalty}")
    if price: summary_parts.append(f"Preço: {price}")
    
    summary = ". ".join(summary_parts) + f". {description[:80]}..."
    
    item = {
        "id": id_slug,
        "name": name,
        "category": "equipamento",
        "subcategory": subcategory,
        "proficiency": proficiency,
        "purpose": purpose,
        "summary": summary,
        "description": description,
        "tableData": table_data,
        "sources": [{
            "book": book,
            "page": page,
            "section": f"Equipamentos: {subcategory} ({proficiency})",
            "version": "v1.3" if "Jogo do Ano" in book else "v1.1" if "Heróis" in book else "v1.0"
        }],
        "tags": sorted(list(all_tags))
    }
    
    if is_magic:
        item["isMagicItem"] = True
        item["magicRarity"] = rarity or "Menor"
        
    return item

print("Extraindo e compilando Equipamentos completos dos 3 livros...")

# =========================================================================================
# 1. LIVRO: TORMENTA20 - EDIÇÃO JOGO DO ANO (v1.3)
# =========================================================================================
book_jda = "Tormenta20 - Jogo do Ano (v1.3)"

# 1.1) ARMAS (Tabela 3-3: Armas - págs 142-145, Descrições págs 146-151)
# --- Armas Simples Corpo a Corpo ---
equipments.append(create_item(
    "arma-adaga", "Adaga", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 2", "1d4", "19/x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 146,
    "Esta faca afiada é usada por muitos habitantes do Reinado, favorita de ladrões por ser facilmente escondida (+5 em testes de Ladinagem para ocultá-la). Quando ataca com uma adaga, você pode usar Destreza em vez de Força nos testes de ataque. Pode ser arremessada.",
    ["faca", "arremesso", "acuidade", "ladinagem"]
))

equipments.append(create_item(
    "arma-espada-curta", "Espada Curta", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 10", "1d6", "19/x2", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "A mais comum das espadas leves, com lâmina reta de dois gumes medindo cerca de 50cm. Popular entre soldados e batedores.",
    ["espada", "leve"]
))

equipments.append(create_item(
    "arma-foice", "Foice", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 4", "1d6", "x3", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Uma ferramenta agrícola adaptada para o combate, com lâmina curvada em meia-lua montada em cabo de madeira curto. Causa dano crítico triplo.",
    ["agrícola", "crítico x3"]
))

equipments.append(create_item(
    "arma-manopla", "Manopla", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 5", "-", "-", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Uma luva de couro pesado recoberta de placas de metal. Permite que seus ataques desarmados causem dano letal e recebam melhorias e encantos de armas.",
    ["ataque desarmado", "luva de ferro"]
))

equipments.append(create_item(
    "arma-clava", "Clava", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 0", "1d6", "x2", "Impacto", "Curto", None, None, 1,
    book_jda, 147,
    "Um pedaço de madeira pesado, osso grande ou bastão rústico. Pode ser arremessada.",
    ["madeira", "porrete", "grátis"]
))

equipments.append(create_item(
    "arma-lanca", "Lança", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 2", "1d6", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 148,
    "Uma haste de madeira com uma ponta afiada de ferro. Pode ser usada com uma ou duas mãos (se usada com duas mãos, causa 1d8 de dano) e pode ser arremessada.",
    ["haste", "duas mãos versátil", "arremesso"]
))

equipments.append(create_item(
    "arma-maca", "Maça", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Haste de madeira pesada ou metal com uma cabeça de ferro flangeada. A arma padrão dos clérigos do Reinado.",
    ["clérigo", "esmagamento"]
))

equipments.append(create_item(
    "arma-bordao", "Bordão", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d6/1d6", "x2", "Impacto", "-", None, None, 2,
    book_jda, 147,
    "Um cajado de madeira reforçada de cerca de 1,80m. É uma arma dupla (você pode usá-la como duas armas com o poder Estilo de Duas Armas).",
    ["arma dupla", "cajado", "grátis"]
))

equipments.append(create_item(
    "arma-pique", "Pique", "Armas", "Armas Simples", "Corpo a Corpo / Haste",
    "T$ 5", "1d8", "x2", "Perfuração", "-", None, None, 2,
    book_jda, 149,
    "Uma lança muito longa (cerca de 3m). É uma arma de haste (permite atacar inimigos a até 3m de distância, mas não inimigos adjacentes).",
    ["haste 3m", "longa"]
))

equipments.append(create_item(
    "arma-tacape", "Tacape", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_jda, 150,
    "Um tronco esculpido ou bastão maciço empunhado com as duas mãos, popular entre trogs, bárbaros e povos primitivos.",
    ["trog", "bárbaro", "duas mãos"]
))

# --- Armas Simples de Disparo e Arremesso ---
equipments.append(create_item(
    "arma-arco-curto", "Arco Curto", "Armas", "Armas Simples", "Disparo / Duas Mãos",
    "T$ 30", "1d6", "x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 146,
    "Arco de tamanho compacto feito de madeira flexível. Pode ser disparado montado sem penalidade.",
    ["disparo", "flecha", "crítico x3"]
))

equipments.append(create_item(
    "arma-besta-leve", "Besta Leve", "Armas", "Armas Simples", "Disparo / Duas Mãos",
    "T$ 35", "1d8", "19/x2", "Perfuração", "Médio", None, None, 2,
    book_jda, 147,
    "Disparador mecânico de virotes montado sobre coronha de madeira. Recarregar uma besta leve é uma ação de movimento.",
    ["disparo", "virote", "recarregar movimento"]
))

equipments.append(create_item(
    "arma-funda", "Funda", "Armas", "Armas Simples", "Disparo / Uma Mão",
    "T$ 0", "1d4", "x2", "Impacto", "Médio", None, None, 1,
    book_jda, 148,
    "Uma tira de couro usada para lançar pedras polidas ou balas de chumbo. Você soma sua Força nas rolagens de dano com a funda.",
    ["pedra", "chumbo", "soma força", "grátis"]
))

equipments.append(create_item(
    "arma-azagaia", "Azagaia", "Armas", "Armas Simples", "Arremesso / Uma Mão",
    "T$ 1", "1d6", "x2", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Uma lança leve de 1,20m balanceada especificamente para arremesso.",
    ["dardo", "arremesso"]
))

# --- Armas Marciais Corpo a Corpo ---
equipments.append(create_item(
    "arma-cimitarra", "Cimitarra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d6", "18/x2", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Espada curva de lâmina fina afiada em um único gume, com margem de ameaça formidável (18-20).",
    ["crítico 18", "corte", "oriental"]
))

equipments.append(create_item(
    "arma-espada-longa", "Espada Longa", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "19/x2", "Corte", "-", None, None, 1,
    book_jda, 147,
    "A mais tradicional das armas dos guerreiros e cavaleiros do Reinado, com lâmina reta de aço de 90cm e guarda em cruz.",
    ["espada", "cavaleiro", "guerreiro"]
))

equipments.append(create_item(
    "arma-florete", "Florete", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 20", "1d6", "18/x2", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "Espada delgada de esgrima com guarda em cesto. Pode ser usada com Acuidade com Arma.",
    ["esgrima", "acuidade", "bucaneiro", "crítico 18"]
))

equipments.append(create_item(
    "arma-machadinha", "Machadinha", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 6", "1d6", "x3", "Corte", "Curto", None, None, 1,
    book_jda, 148,
    "Machado pequeno e balanceado para combate corpo a corpo ou arremesso rápido.",
    ["machado leve", "arremesso", "crítico x3"]
))

equipments.append(create_item(
    "arma-machado-de-batalha", "Machado de Batalha", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 10", "1d8", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "Machado pesado com cabeça de lâmina única ou dupla usado por guerreiros e nobres anões de Doherimm.",
    ["anão", "crítico x3"]
))

equipments.append(create_item(
    "arma-mangual", "Mangual", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Haste de madeira conectada por corrente a uma esfera de ferro com pontas. Fornece +2 em testes para Desarmar e ignora bônus na Defesa de escudos.",
    ["desarmar", "ignora escudo"]
))

equipments.append(create_item(
    "arma-martelo-de-guerra", "Martelo de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x3", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Haste de madeira resistente com uma cabeça de aço pesada em uma ponta e um bico perfurante na outra.",
    ["martelo", "anão", "crítico x3"]
))

equipments.append(create_item(
    "arma-picareta", "Picareta", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d6", "x4", "Perfuração", "-", None, None, 1,
    book_jda, 149,
    "Ferramenta de mineração militarizada com ponta de aço maciço capaz de perfurar couraças. Causa crítico quádruplo (x4).",
    ["crítico x4", "perfurante"]
))

equipments.append(create_item(
    "arma-tridente", "Tridente", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 150,
    "Lança de três pontas com farpas metálicas. Fornece +2 em testes de manobra para Desarmar ou Derrubar e pode ser arremessada.",
    ["tritão", "derrubar", "desarmar", "arremesso"]
))

equipments.append(create_item(
    "arma-alabarda", "Alabarda", "Armas", "Armas Marciais", "Corpo a Corpo / Haste",
    "T$ 10", "1d10", "x3", "Corte ou Perfuração", "-", None, None, 2,
    book_jda, 146,
    "Haste de madeira de 2m com uma lâmina de machado encimada por ponta de lança. Arma de haste (alcance 3m).",
    ["haste 3m", "machado longo", "crítico x3"]
))

equipments.append(create_item(
    "arma-alfange", "Alfange", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 75", "2d4", "18/x2", "Corte", "-", None, None, 2,
    book_jda, 146,
    "Uma versão maior da cimitarra, de lâmina larga e curva de duas mãos, favorita de guerreiros do Deserto da Perdição.",
    ["crítico 18", "duas mãos", "deserto"]
))

equipments.append(create_item(
    "arma-guisarme", "Guisarme", "Armas", "Armas Marciais", "Corpo a Corpo / Haste",
    "T$ 9", "2d4", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Haste longa com lâmina curva em gancho. Arma de haste (alcance 3m) que fornece +2 em testes para Derrubar.",
    ["haste 3m", "derrubar"]
))

equipments.append(create_item(
    "arma-lanca-montada", "Lança Montada", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d10", "x3", "Perfuração", "-", None, None, 2,
    book_jda, 148,
    "Lança pesada de torneio. Quando usada em investida montada, o dano base da arma é multiplicado por 2.",
    ["montaria", "investida dobrada", "cavaleiro"]
))

equipments.append(create_item(
    "arma-machado-de-guerra", "Machado de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "1d12", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Machado colossal de duas lâminas empunhado com as duas mãos para golpes destruidores.",
    ["duas mãos", "crítico x3", "bárbaro"]
))

equipments.append(create_item(
    "arma-montante", "Montante", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d6", "19/x2", "Corte", "-", None, None, 2,
    book_jda, 148,
    "A maior de todas as espadas de infantaria, com lâmina de mais de 1,50m e contra-guarda para defesa.",
    ["espada gigante", "duas mãos", "2d6"]
))

# --- Armas Marciais de Disparo e Arremesso ---
equipments.append(create_item(
    "arma-arco-longo", "Arco Longo", "Armas", "Armas Marciais", "Disparo / Duas Mãos",
    "T$ 100", "1d8", "x3", "Perfuração", "Longo", None, None, 2,
    book_jda, 146,
    "Arco de grande envergadura feito de teixo ou freixo. Você soma sua Força nas rolagens de dano (até o limite de +2, ou mais com melhorias).",
    ["disparo", "alcance longo", "soma força"]
))

equipments.append(create_item(
    "arma-besta-pesada", "Besta Pesada", "Armas", "Armas Marciais", "Disparo / Duas Mãos",
    "T$ 50", "1d12", "19/x2", "Perfuração", "Médio", None, None, 2,
    book_jda, 147,
    "Besta armada com arco de aço de alta tensão e manivela mecânica. Recarregar exige uma ação padrão.",
    ["disparo", "recarregar padrão", "1d12"]
))

equipments.append(create_item(
    "arma-rede", "Rede", "Armas", "Armas Marciais", "Arremesso / Uma Mão",
    "T$ 20", "-", "-", "-", "Curto", None, None, 1,
    book_jda, 149,
    "Rede com pesos de chumbo nas bordas. Se acertar o alvo, causa a condição Enredado.",
    ["enredar", "imobilizar", "gladiador"]
))

# --- Armas Exóticas & Armas de Fogo ---
equipments.append(create_item(
    "arma-katana", "Katana", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão ou Duas Mãos",
    "T$ 100", "1d10", "19/x2", "Corte", "-", None, None, 1,
    book_jda, 148,
    "A lendária espada dos samurais de Tamu-ra. Pode ser usada como arma marcial com as duas mãos ou como arma exótica de uma mão (permitindo usar com Acuidade com Arma).",
    ["samurai", "tamu-ra", "acuidade"]
))

equipments.append(create_item(
    "arma-corrente-de-espinhos", "Corrente de Espinhos", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 25", "2d4/2d4", "19/x2", "Perfuração", "-", None, None, 2,
    book_jda, 147,
    "Corrente de elos de aço reforçada com farpas pontiagudas. É uma arma dupla e de haste flexível que pode atacar alvos adjacentes ou a até 3m de distância.",
    ["arma dupla", "haste 3m", "desarmar", "derrubar"]
))

equipments.append(create_item(
    "arma-espada-bastarda", "Espada Bastarda", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão ou Duas Mãos",
    "T$ 35", "1d10/1d12", "19/x2", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Uma espada longa e pesada de cabo estendido. Usada com as duas mãos como arma marcial (1d12) ou com uma mão como arma exótica (1d10).",
    ["versátil", "espada pesada"]
))

equipments.append(create_item(
    "arma-pistola", "Pistola", "Armas", "Armas de Fogo", "Disparo / Uma Mão",
    "T$ 250", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_jda, 149,
    "Arma de fogo portátil de pólvora desenvolvida pelos artesãos klirens de Zakharov. Recarregar exige uma ação padrão.",
    ["fogo", "zakharov", "pólvora", "crítico x3", "2d6"]
))

equipments.append(create_item(
    "arma-mosquete", "Mosquete", "Armas", "Armas de Fogo", "Disparo / Duas Mãos",
    "T$ 500", "2d8", "19/x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 148,
    "Arma de fogo de cano longo com alcance e poder devastadores. Recarregar exige uma ação completa.",
    ["fogo", "cano longo", "pólvora", "2d8", "crítico x3"]
))

# 1.1.1) MUNIÇÃO (Tabela 3-4: Munições - pág 151)
equipments.append(create_item(
    "municao-flechas", "Flechas (aljava com 20)", "Munições", "Munições", "Munição de Disparo",
    "T$ 1", "-", "-", "Perfuração", "-", None, None, 1,
    book_jda, 151,
    "Hastes de madeira emplumadas com ponta de aço afiada para arcos. Vendidas em aljavas com 20 flechas.",
    ["arco", "aljava 20"]
))

equipments.append(create_item(
    "municao-virotes", "Virotes (aljava com 20)", "Munições", "Munições", "Munição de Disparo",
    "T$ 2", "-", "-", "Perfuração", "-", None, None, 1,
    book_jda, 151,
    "Projéteis curtos e pesados para bestas leves e pesadas. Vendidos em caixas com 20 virotes.",
    ["besta", "caixa 20"]
))

equipments.append(create_item(
    "municao-balas-funda", "Balas de Funda (saco com 20)", "Munições", "Munições", "Munição de Disparo",
    "T$ 1", "-", "-", "Impacto", "-", None, None, 1,
    book_jda, 151,
    "Esferas de chumbo fundido perfeitamente esféricas para fundas.",
    ["funda", "chumbo 20"]
))

equipments.append(create_item(
    "municao-balas-polvora", "Balas e Pólvora (cartucho com 20)", "Munições", "Munições", "Munição de Fogo",
    "T$ 20", "-", "-", "Perfuração", "-", None, None, 1,
    book_jda, 151,
    "Doses individuais de pólvora e balas de chumbo para pistolas e mosquetes.",
    ["pólvora", "cartucho 20", "fogo"]
))

# 1.2) ARMADURAS & ESCUDOS (Tabela 3-5: Armaduras & Escudos - pág 152-154)
equipments.append(create_item(
    "armadura-armadura-acolchoada", "Armadura Acolchoada", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 5", None, None, None, None, 1, 0, 1,
    book_jda, 152,
    "Várias camadas de tecido acolchoado e costurado. Oferece proteção básica sem prejudicar a agilidade do portador.",
    ["tecido", "sem penalidade"]
))

equipments.append(create_item(
    "armadura-couro-batido", "Couro Batido", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 25", None, None, None, None, 2, 0, 1,
    book_jda, 153,
    "Armadura de couro curtido endurecido com rebites metálicos. Excelente equilíbrio entre proteção e mobilidade.",
    ["couro", "sem penalidade"]
))

equipments.append(create_item(
    "armadura-gibao-de-peles", "Gibão de Peles", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 15", None, None, None, None, 3, -1, 2,
    book_jda, 153,
    "Camadas grossas de peles e couros rústicos de animais selvagens, favorita de bárbaros e druidas.",
    ["bárbaro", "druida", "peles"]
))

equipments.append(create_item(
    "armadura-couraca", "Couraça", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 500", None, None, None, None, 5, -2, 2,
    book_jda, 153,
    "Peitoral inteiriço de aço moldado com caneleiras e braçadeiras de couro reforçado. A melhor armadura leve de Arton.",
    ["peitoral", "aço", "alta defesa"]
))

equipments.append(create_item(
    "armadura-brunea", "Brunea", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 50", None, None, None, None, 5, -2, 2,
    book_jda, 153,
    "Colete de couro recoberto com escamas metálicas sobrepostas de bronze ou ferro.",
    ["escamas", "pesada básica"]
))

equipments.append(create_item(
    "armadura-cota-de-malha", "Cota de Malha", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 150", None, None, None, None, 6, -2, 3,
    book_jda, 153,
    "Túnica feita de milhares de anéis de ferro entrelaçados sobre acolchoado de feltro grosso.",
    ["anéis", "ferro", "túnica"]
))

equipments.append(create_item(
    "armadura-loriga-segmentada", "Loriga Segmentada", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 250", None, None, None, None, 7, -3, 3,
    book_jda, 153,
    "Tiras horizontais de metal sobrepostas e presas com correias de couro internas, tradicional das legiões de Tapista.",
    ["minotauro", "tapista", "segmentada"]
))

equipments.append(create_item(
    "armadura-armadura-completa", "Armadura Completa", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 1.000", None, None, None, None, 10, -5, 5,
    book_jda, 153,
    "A proteção máxima de um cavaleiro: placas de aço forjadas e articuladas que cobrem o corpo inteiro com elmo fechado.",
    ["cavaleiro", "placas", "defesa 10"]
))

equipments.append(create_item(
    "armadura-escudo-leve", "Escudo Leve", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 5", None, None, None, None, 1, -1, 1,
    book_jda, 154,
    "Escudo de madeira leve afixado no antebraço. Deixa a mão livre para segurar itens, mas não para empunhar armas.",
    ["madeira", "mão livre"]
))

equipments.append(create_item(
    "armadura-escudo-pesado", "Escudo Pesado", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 15", None, None, None, None, 2, -2, 2,
    book_jda, 154,
    "Escudo grande de madeira reforçada ou aço com empunhadura central. Ocupa uma mão inteira.",
    ["aço", "empunhadura central"]
))

# 1.3) ITENS GERAIS (Tabela 3-6: Itens Gerais - págs 155-163)
equipments.append(create_item(
    "item-mochila-de-aventureiro", "Mochila de Aventureiro", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 0,
    book_jda, 155,
    "Mochila de couro reforçado com bolsos e presilhas externas. Aumenta o limite de carga do personagem em +2 espaços.",
    ["carga +2", "mochila"]
))

equipments.append(create_item(
    "item-corda-15m", "Corda (15m)", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Corda resistente de cânhamo com 15 metros de comprimento.",
    ["cânhamo", "escalada"]
))

equipments.append(create_item(
    "item-tocha", "Tocha (4 unidades)", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Haste de madeira com ponta embebida em piche. Ilumina um raio de 9m por 1 hora.",
    ["luz 9m", "fogo"]
))

equipments.append(create_item(
    "item-balsamo-restaurador", "Bálsamo Restaurador", "Itens Gerais", "Itens Gerais", "Alquimias & Preparados",
    "T$ 10", None, None, None, None, None, None, 0.5,
    book_jda, 157,
    "Pomada curativa feita com ervas medicinais de Arton. Recupera 2d4 pontos de vida ao ser aplicada (ação padrão).",
    ["cura 2d4", "alquimia", "vida"]
))

equipments.append(create_item(
    "item-essencia-de-mana", "Essência de Mana", "Itens Gerais", "Itens Gerais", "Alquimias & Preparados",
    "T$ 50", None, None, None, None, None, None, 0.5,
    book_jda, 157,
    "Líquido azulado brilhante destilado de flores de Wynlla. Recupera 1d4 pontos de mana ao ser consumido (ação padrão).",
    ["mana 1d4", "alquimia", "pm"]
))

equipments.append(create_item(
    "item-fogo-alquimico", "Fogo Alquímico", "Itens Gerais", "Itens Gerais", "Alquimias & Preparados",
    "T$ 10", "1d6", "-", "Fogo", "Curto", None, None, 0.5,
    book_jda, 157,
    "Frasco de óleo incandescente que explode em chamas ao contato com o ar. O alvo sofre 1d6 pontos de dano de fogo e fica em chamas.",
    ["fogo", "em chamas", "arremesso"]
))

equipments.append(create_item(
    "item-acido", "Ácido (frasco)", "Itens Gerais", "Itens Gerais", "Alquimias & Preparados",
    "T$ 10", "2d4", "-", "Ácido", "Curto", None, None, 0.5,
    book_jda, 157,
    "Frasco de vidro grosso contendo líquido corrosivo verde. Causa 2d4 pontos de dano de ácido ao ser arremessado.",
    ["ácido", "corrosivo"]
))

equipments.append(create_item(
    "item-varinha-esoterica", "Varinha", "Itens Gerais", "Itens Gerais", "Itens Esotéricos",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Canalizador de madeira nobre polida para conjuradores arcanos. Concede +1 em testes de Misticismo para identificar magias.",
    ["esotérico", "arcano", "varinha"]
))

equipments.append(create_item(
    "item-cetro-elemental", "Cetro Elemental", "Itens Gerais", "Itens Gerais", "Itens Esotéricos",
    "T$ 250", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Haste de metal nobre encimada por gema pura. Aumenta em +1 por dado o dano de magias do elemento escolhido (fogo, frio, ácido ou eletricidade).",
    ["esotérico", "dano mágico", "elemental"]
))

# 1.4) ITENS SUPERIORES & MELHORIAS (Tabela 3-8: Melhorias - pág 164-168)
equipments.append(create_item(
    "melhoria-certeira", "Melhoria: Certeira", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300 (1 melhoria)", None, None, None, None, None, None, 0,
    book_jda, 165,
    "A arma é perfeitamente balanceada e concede +1 em testes de ataque.",
    ["ataque +1", "arma"]
))

equipments.append(create_item(
    "melhoria-cruel", "Melhoria: Cruel", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300 (1 melhoria)", None, None, None, None, None, None, 0,
    book_jda, 165,
    "A arma possui fio afiadíssimo ou cravos adicionais e concede +1 nas rolagens de dano.",
    ["dano +1", "arma"]
))

equipments.append(create_item(
    "melhoria-macabra", "Melhoria: Macabra", "Itens Superiores", "Melhorias", "Melhoria de Arma / Armadura",
    "T$ 300 (1 melhoria)", None, None, None, None, None, None, 0,
    book_jda, 166,
    "Item adornado com ossos e runas sinistras de Tenebra. Concede +2 em testes de Intimidação.",
    ["intimidação +2"]
))

equipments.append(create_item(
    "melhoria-reforcada", "Melhoria: Reforçada", "Itens Superiores", "Melhorias", "Melhoria de Armadura / Escudo",
    "T$ 300 (1 melhoria)", None, None, None, None, 1, 0, 0,
    book_jda, 166,
    "A armadura ou escudo recebe placas adicionais forjadas, aumentando seu bônus de Defesa em +1.",
    ["defesa +1", "armadura", "escudo"]
))

equipments.append(create_item(
    "melhoria-sob-medida", "Melhoria: Sob Medida", "Itens Superiores", "Melhorias", "Melhoria de Armadura",
    "T$ 300 (1 melhoria)", None, None, None, None, None, 1, 0,
    book_jda, 166,
    "A armadura é ajustada com precisão anatômica ao corpo do usuário, reduzindo sua penalidade de armadura em 1.",
    ["penalidade -1", "armadura"]
))

equipments.append(create_item(
    "material-aco-rubi", "Material Especial: Aço-Rubi", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 1.000", None, None, None, None, None, None, 0,
    book_jda, 167,
    "Metal avermelhado extraído de áreas purificadas da Tormenta. Em armas, ignora 10 pontos de Redução de Dano (RD) do alvo. Em armaduras, concede RD 2 contra criaturas da Tormenta.",
    ["aço-rubi", "ignora rd 10", "tormenta"]
))

equipments.append(create_item(
    "material-mitral", "Material Especial: Mitral", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 1.500", None, None, None, None, None, 2, 0,
    book_jda, 167,
    "Metal prateado levíssimo dos reinos élficos e anões. Reduz a penalidade de armadura em 2 e diminui a categoria de peso do item.",
    ["mitral", "penalidade -2", "leve"]
))

equipments.append(create_item(
    "material-madeira-de-tollon", "Material Especial: Madeira de Tollon", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 500", None, None, None, None, None, None, 0,
    book_jda, 167,
    "Madeira nobre com veios arcanos de Tollon. Reduz em 1 PM o custo de habilidades mágicas e manobras do portador (mínimo 1 PM).",
    ["tollon", "reduz custo pm", "madeira"]
))

equipments.append(create_item(
    "material-gelo-eterno", "Material Especial: Gelo Eterno", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 1.000", "+1d6", None, "Frio", None, None, None, 0,
    book_jda, 167,
    "Gelo mágico imperecível das Uivantes. Causa +1d6 de dano de frio em armas ou concede resistência a fogo 5 em armaduras.",
    ["gelo eterno", "frio +1d6", "uivantes"]
))


# =========================================================================================
# 2. LIVRO: HERÓIS DE ARTON (v1.1) - ARSENAL DOS HERÓIS (PÁG 216+)
# =========================================================================================
book_herois = "Heróis de Arton (v1.1)"

# 2.1) Armas do Arsenal (Tabela 3-1: Armas e Continuação - págs 218-222)
equipments.append(create_item(
    "arma-adaga-de-duelo", "Adaga de Duelo", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 25", "1d4", "18/x2", "Perfuração", "-", 1, None, 1,
    book_herois, 218,
    "Adaga de lâmina reforçada com guarda em cruz longa desenhada para aparar ataques. Quando empunhada na mão inábil, concede +1 na Defesa.",
    ["duelo", "parada", "defesa +1"]
))

equipments.append(create_item(
    "arma-arco-composto", "Arco Composto", "Armas", "Armas Marciais", "Disparo / Duas Mãos",
    "T$ 200", "1d10", "x3", "Perfuração", "Longo", None, None, 2,
    book_herois, 220,
    "Arco reforçado com lâminas de chifre, madeira e osso sob tensão. Você soma todo o seu modificador de Força nas rolagens de dano com este arco.",
    ["arco", "disparo", "soma toda força", "1d10"]
))

equipments.append(create_item(
    "arma-pistola-de-tambor", "Pistola de Tambor", "Armas", "Armas de Fogo", "Disparo / Uma Mão",
    "T$ 750", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_herois, 222,
    "Arma de fogo com tambor rotativo de 6 tiros de Zakharov. Permite disparar 6 vezes antes de precisar recarregar (recarregar o tambor inteiro é uma ação completa).",
    ["fogo", "tambor 6 tiros", "zakharov"]
))

equipments.append(create_item(
    "arma-machado-taurico", "Machado Táurico", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 150", "2d8", "x3", "Corte", "-", None, None, 3,
    book_herois, 221,
    "Machado monumental de lâmina dupla assimétrica forjado pelos campeões da arena de Tiberus. Causa 2d8 de dano de corte com crítico x3.",
    ["minotauro", "tiberus", "2d8", "exótica"]
))

# 2.2) Munições de Heróis (Tabela 3-2: Munições - pág 223)
equipments.append(create_item(
    "municao-flechas-assobiadoras", "Flechas Assobiadoras (aljava com 20)", "Munições", "Munições", "Munição de Disparo",
    "T$ 10", "-", "-", "Perfuração", "-", None, None, 1,
    book_herois, 223,
    "Flechas com ponta oca perfurada que emite um assobio agudo aterrorizante ao voar. Fornece +2 no teste de Intimidação para desmoralizar inimigos.",
    ["assobio", "intimidação", "flecha"]
))

equipments.append(create_item(
    "municao-balas-dumdum", "Balas Dum-Dum (cartucho com 20)", "Munições", "Munições", "Munição de Fogo",
    "T$ 50", "+2", "-", "Perfuração", "-", None, None, 1,
    book_herois, 223,
    "Balas de chumbo com ponta cavada que se expandem no impacto. Concedem +2 nas rolagens de dano com armas de fogo.",
    ["fogo", "dano +2", "dumdum"]
))

# 2.3) Armaduras & Escudos de Heróis (Tabela 3-3: Armaduras & Escudos - págs 223-224)
equipments.append(create_item(
    "armadura-gibao-nobre", "Gibão de Peles Nobres", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 150", None, None, None, None, 3, 0, 1,
    book_herois, 223,
    "Gibão trabalhado com peles de animais nobres e forro de seda suave. Concede Defesa +3 sem qualquer penalidade de armadura.",
    ["peles nobres", "sem penalidade"]
))

equipments.append(create_item(
    "armadura-armadura-taurica-completa", "Armadura Completa Táurica", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 3.000", None, None, None, None, 12, -6, 5,
    book_herois, 224,
    "Armadura monumental forjada em placas duplas maciças com elmo de touro de combate. Concede Defesa +12.",
    ["minotauro", "placas táuricas", "defesa 12"]
))

# 2.4) Itens Gerais de Heróis (Tabela 3-4: Itens Gerais e Continuação - págs 227-238)
equipments.append(create_item(
    "item-catalisador-de-wynna", "Catalisador de Wynna", "Itens Gerais", "Itens Gerais", "Itens Esotéricos",
    "T$ 300", None, None, None, None, None, None, 1,
    book_herois, 230,
    "Esfera de cristal flutuante que armazena energia mágica. Reduz em 1 PM o custo do primeiro aprimoramento de qualquer magia arcana.",
    ["esotérico", "wynna", "aprimoramento"]
))

equipments.append(create_item(
    "item-kit-de-cirurgiao-de-campo", "Kit de Cirurgião de Campo", "Itens Gerais", "Itens Gerais", "Ferramentas & Aventura",
    "T$ 100", None, None, None, None, None, None, 1,
    book_herois, 232,
    "Estojo completo com bisturis esterilizados, agulhas e unguentos coagulantes. Concede +2 em testes de Cura para estabilizar moribundos e tratar ferimentos graves.",
    ["cura +2", "cirurgião", "primeiros socorros"]
))

# 2.5) Itens Superiores & Materiais de Heróis (Tabela 3-5: Novas Melhorias - pág 239)
equipments.append(create_item(
    "material-materia-vermelha", "Material Especial: Matéria Vermelha", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 2.000", None, "+2", None, None, None, None, 0,
    book_herois, 239,
    "Substância viva e pulsante colhida diretamente de áreas de tempestade aberrante da Tormenta. Aumenta a margem de ameaça de crítico da arma em +2, mas exige teste de Vontade diário.",
    ["tormenta", "crítico +2", "matéria vermelha"]
))

# 2.6) Capangas (pág 240)
equipments.append(create_item(
    "capanga-escudeiro-fiel", "Capanga: Escudeiro Fiel", "Capangas", "Capangas", "Capanga / Aliado",
    "T$ 10/dia", None, None, None, None, 2, None, 0,
    book_herois, 240,
    "Um jovem aprendiz leal que carrega suas armas reservas e cuida do seu cavalo. Em combate, fornece +2 na Defesa contra ataques corpo a corpo.",
    ["capanga", "aliado", "escudeiro", "defesa +2"]
))

equipments.append(create_item(
    "capanga-guia-dos-ermos", "Capanga: Guia dos Ermos", "Capangas", "Capangas", "Capanga / Aliado",
    "T$ 15/dia", None, None, None, None, None, None, 0,
    book_herois, 240,
    "Batedor experiente que conhece as trilhas secretas de Arton. Concede +2 em testes de Sobrevivência e evita encontros aleatórios desfavoráveis.",
    ["guia", "ermos", "sobrevivência"]
))

# 2.7) Veículos (pág 241)
equipments.append(create_item(
    "veiculo-carruagem-blindada", "Carruagem Blindada de Valkaria", "Veículos", "Veículos", "Veículo Terrestre",
    "T$ 1.500", None, None, None, None, 18, None, 10,
    book_herois, 241,
    "Veículo de quatro rodas reforçado com placas de ferro e seteiras para arqueiros. Transporta até 6 passageiros com cobertura total contra disparos.",
    ["veículo", "carruagem", "transporte", "blindada"]
))

equipments.append(create_item(
    "veiculo-balao-goblin", "Balão de Ar Quente Goblin", "Veículos", "Veículos", "Veículo Aéreo",
    "T$ 3.000", None, None, None, None, 12, None, 12,
    book_herois, 241,
    "Veículo voador impulsionado por queimadores alquímicos a vapor goblin. Permite cruzar montanhas e florestas com deslocamento de voo de 18m.",
    ["balão", "voo", "goblin", "aéreo"]
))


# =========================================================================================
# 3. LIVRO: AMEAÇAS DE ARTON (v1.0) - BAZAR MONSTRUOSO (PÁG 390+)
# =========================================================================================
book_ameacas = "Ameaças de Arton (v1.0)"

# 3.1) Armas do Bazar (pág 392, Tabela 3-1: Armas pág 394)
equipments.append(create_item(
    "arma-garra-de-monstro", "Garra de Monstro", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 50", "1d8", "19/x2", "Corte ou Perfuração", "-", None, None, 1,
    book_ameacas, 392,
    "Arma empunhada sobre os nós dos dedos, confeccionada com garras tratadas de monstros de Arton. Fornece +2 no dano contra criaturas com armadura natural.",
    ["monstro", "garra", "bazar monstruoso"]
))

equipments.append(create_item(
    "arma-arpao-tritao", "Arpão de Caça Tritão", "Armas", "Armas Marciais", "Arremesso / Uma Mão",
    "T$ 40", "1d8", "x3", "Perfuração", "Médio", None, None, 1,
    book_ameacas, 393,
    "Arpão com farpas afiadas e cabo com corda de tripa marinha. Se acertar o alvo, você pode gastar uma ação de movimento para puxá-lo em sua direção.",
    ["arpão", "tritão", "puxar", "arremesso"]
))

equipments.append(create_item(
    "arma-chicote-de-tentaculo", "Chicote de Espinhos Monstruoso", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 80", "1d6", "x2", "Corte", "Médio", None, None, 1,
    book_ameacas, 393,
    "Chicote feito de tentáculos espinhosos preservados por alquimia. Causa dano letal e pode aplicar venenos diretamente no corte.",
    ["chicote", "tentáculo", "veneno"]
))

# 3.2) Armaduras e Escudos do Bazar (pág 395, Tabela 3-2 pág 395)
equipments.append(create_item(
    "armadura-couro-de-basilisco", "Couro de Basilisco", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 1.200", None, None, None, None, 4, 0, 1,
    book_ameacas, 395,
    "Armadura leve feita com escamas densas de basilisco do Deserto. Concede +4 em testes de resistência contra efeitos de Petrificação e Venenos.",
    ["basilisco", "petrificação", "veneno", "leve"]
))

equipments.append(create_item(
    "armadura-escudo-de-quitina", "Escudo de Quitina Monstruosa", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 350", None, None, None, None, 3, -1, 1,
    book_ameacas, 395,
    "Escudo feito a partir da carapaça de insetos gigantes das florestas de Sambúrdia. Fornece Defesa +3 com penalidade de apenas -1.",
    ["quitina", "inseto gigante", "leve e resistente"]
))

equipments.append(create_item(
    "armadura-carapaca-do-gelo", "Carapaça de Verme do Gelo", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 2.500", None, None, None, None, 8, -3, 3,
    book_ameacas, 395,
    "Armadura pesada forjada com placas de gelo e quitina de vermes das Montanhas Uivantes. Concede Redução de Dano 5 a frio.",
    ["verme do gelo", "rd frio 5", "uivantes"]
))

# 3.3) Itens Gerais do Bazar (pág 396, Tabela 3-3 pág 398)
equipments.append(create_item(
    "item-peconha-de-manticora", "Peçonha de Mantícora", "Itens Gerais", "Itens Gerais", "Alquimias & Preparados",
    "T$ 250", None, None, "Veneno", "Curto", None, None, 0.5,
    book_ameacas, 396,
    "Veneno mortal extraído da cauda de espinhos de uma mantícora. Causa a condição Envenenado (perde 2d12 PV por rodada, Fortitude CD 22 reduz à metade).",
    ["veneno", "mantícora", "2d12 dano"]
))

equipments.append(create_item(
    "item-po-de-pedra-de-gargula", "Pó de Pedra de Gárgula", "Itens Gerais", "Itens Gerais", "Alquimias & Preparados",
    "T$ 120", None, None, "Alquímico", "-", None, None, 0.5,
    book_ameacas, 397,
    "Pó mineral que endurece instantaneamente a pele do usuário ao ser aspirado, concedendo Redução de Dano 2 por 1 cena.",
    ["rd 2", "gárgula", "pele de pedra"]
))

# 3.4) Itens Superiores e Materiais do Bazar (pág 399, Tabela 3-4 e 3-5 págs 400-401)
equipments.append(create_item(
    "material-osso-de-dragao", "Material Especial: Osso de Dragão", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 1.200", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Armas e armaduras esculpidas em ossos fossilizados de dragões anciões. Em armas, concede +2 em rolagens de dano. Em armaduras, concede resistência a energia 5.",
    ["dragão", "osso", "dano +2"]
))

equipments.append(create_item(
    "material-madeira-abissal", "Material Especial: Madeira Abissal", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 800", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Troncos recolhidos das profundezas do Oceano ou de pântanos negros de Tollon. Concede camuflagem leve sob a água e na escuridão.",
    ["abissal", "camuflagem", "madeira"]
))

with open("data/categories/equipamentos.json", "w", encoding="utf-8") as f:
    json.dump(equipments, f, ensure_ascii=False, indent=2)

print(f"\n=======================================================")
print(f"EQUIPAMENTOS CONSOLIDADOS COM SUCESSO!")
print(f"Total de Itens de Equipamento: {len(equipments)}")
print(f"- Jogo do Ano (pág 142-168): {len([e for e in equipments if book_jda in e['sources'][0]['book']])}")
print(f"- Heróis de Arton (pág 216-241): {len([e for e in equipments if book_herois in e['sources'][0]['book']])}")
print(f"- Ameaças de Arton (pág 390-401): {len([e for e in equipments if book_ameacas in e['sources'][0]['book']])}")
print(f"Arquivo gerado: data/categories/equipamentos.json")
print("=======================================================\n")
