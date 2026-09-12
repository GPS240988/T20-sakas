import json
import os
import re
import pymupdf

os.makedirs("data/categories", exist_ok=True)

equipments = []
id_set = set()

def add_item(
    id_slug, name, subcategory, proficiency, purpose,
    price, damage, critical, damage_type, range_dist,
    defense, penalty, space, book, page, description,
    tags=None, is_magic=False, rarity=None
):
    if tags is None:
        tags = []
        
    base_id = id_slug
    counter = 1
    while id_slug in id_set:
        id_slug = f"{base_id}-{counter}"
        counter += 1
    id_set.add(id_slug)
    
    all_tags = set([
        "equipamento",
        subcategory.lower(),
        proficiency.lower(),
        purpose.lower(),
        name.lower()
    ] + [t.lower() for t in tags])
    
    table_data = {
        "price": price,
        "proficiency": proficiency,
        "purpose": purpose,
        "space": space
    }
    if damage and damage != "-": table_data["damage"] = damage
    if critical and critical != "-": table_data["critical"] = critical
    if damage_type and damage_type != "-": table_data["damageType"] = damage_type
    if range_dist and range_dist != "-": table_data["range"] = range_dist
    if defense is not None: table_data["defenseBonus"] = defense
    if penalty is not None and penalty != 0: table_data["armorPenalty"] = penalty
    
    summary_parts = [f"{proficiency} ({purpose})"]
    if damage and damage != "-": summary_parts.append(f"Dano: {damage} ({critical})")
    if defense is not None: summary_parts.append(f"Defesa: +{defense}")
    if penalty is not None and penalty != 0: summary_parts.append(f"Penalidade: {penalty}")
    if price: summary_parts.append(f"Preço: {price}")
    if space is not None: summary_parts.append(f"Espaço: {space}")
    
    clean_desc = description.strip()
    summary = ". ".join(summary_parts) + f". {clean_desc[:90]}..."
    
    version = "v1.3" if "Jogo do Ano" in book else "v1.1" if "Heróis" in book else "v1.0"
    
    item = {
        "id": id_slug,
        "name": name,
        "category": "equipamento",
        "subcategory": subcategory,
        "proficiency": proficiency,
        "purpose": purpose,
        "summary": summary,
        "description": clean_desc,
        "tableData": table_data,
        "sources": [{
            "book": book,
            "page": page,
            "section": f"Equipamentos: {subcategory} ({proficiency})",
            "version": version
        }],
        "tags": sorted(list(all_tags))
    }
    
    if is_magic:
        item["isMagicItem"] = True
        item["magicRarity"] = rarity or "Menor"
        
    equipments.append(item)
    return item

print("=== INICIANDO CONSTRUÇÃO EXAUSTIVA DE EQUIPAMENTOS (3 LIVROS) ===")

book_jda = "Tormenta20 - Jogo do Ano (v1.3)"
book_hda = "Heróis de Arton (v1.1)"
book_ameacas = "Ameaças de Arton (v1.0)"

# =========================================================================================
# 1. LIVRO: TORMENTA20 - EDIÇÃO JOGO DO ANO (v1.3)
# =========================================================================================

# --- 1.1) ARMAS (Tabela 3-3, págs 144-145, Descrições págs 146-151) ---
# Armas Simples Corpo a Corpo - Leves
add_item(
    "arma-adaga", "Adaga", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 2", "1d4", "19", "Perfuração", "Curto", None, None, 1,
    book_jda, 146,
    "Esta faca afiada é usada por muitos habitantes adultos do Reinado, embora seja favorita de ladrões e assassinos, por ser facilmente escondida (fornece +5 em testes de Ladinagem para ocultá-la). Quando ataca com uma adaga, você pode usar sua Destreza em vez de Força nos testes de ataque. Uma adaga pode ser arremessada.",
    ["faca", "acuidade", "arremesso", "ladinagem"]
)

add_item(
    "arma-ataque-desarmado", "Ataque Desarmado", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 0", "1d3", "x2", "Impacto", "-", None, None, 0,
    book_jda, 144,
    "Um soco, chute, cabeçada ou qualquer outro golpe desferido com o próprio corpo. Um ataque desarmado causa dano não letal. Um personagem treinado em Luta pode causar dano letal ou não letal sem penalidades. Você não pode aplicar melhorias ou encantos a ataques desarmados, a menos que esteja usando uma manopla.",
    ["soco", "chute", "não letal", "desarmado"]
)

add_item(
    "arma-espada-curta", "Espada Curta", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 10", "1d6", "19", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "O tipo mais comum de espada, usada por guardas ou como arma secundária de guerreiros.",
    ["espada", "leve", "guarda"]
)

add_item(
    "arma-foice", "Foice", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 4", "1d6", "x3", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Uma ferramenta agrícola com lâmina curva montada em um cabo de madeira curto. Causa dano crítico triplo.",
    ["agrícola", "crítico x3", "camponês"]
)


# Armas Simples Corpo a Corpo - Uma Mão
add_item(
    "arma-clava", "Clava", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 0", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_jda, 147,
    "Um pedaço de madeira empunhado como arma, geralmente usado por bárbaros ou criaturas brutais — ou como arma improvisada, como um galho de árvore ou pedaço de mobília. Sendo fácil de conseguir, seu preço é zero.",
    ["madeira", "porrete", "grátis", "improvisada"]
)

add_item(
    "arma-lanca", "Lança", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 2", "1d6", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 148,
    "Uma haste de madeira com uma ponta afiada de ferro ou pedra. Pode ser arremessada.",
    ["haste", "arremesso", "infantaria"]
)

add_item(
    "arma-maca", "Maça", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Um bastão de madeira ou metal com uma cabeça pesada e flangeada na ponta. Muito utilizada por clérigos que fazem votos de não derramar sangue cortando carne.",
    ["bastão", "impacto", "clérigo"]
)


# Armas Simples Corpo a Corpo - Duas Mãos
add_item(
    "arma-bordao", "Bordão", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d6/1d6", "x2", "Impacto", "-", None, None, 2,
    book_jda, 147,
    "Um cajado apreciado por viajantes e camponeses por sua praticidade e fácil acesso (seu preço é zero). O bordão é uma arma dupla.",
    ["cajado", "dupla", "grátis", "viajante"]
)

add_item(
    "arma-pique", "Pique", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 5", "1d8", "x2", "Perfuração", "-", None, None, 2,
    book_jda, 149,
    "Uma lança longa de infantaria medindo entre 3 e 4 metros. O pique é uma arma alongada.",
    ["haste longa", "alongada", "antagonista de investida"]
)

add_item(
    "arma-tacape", "Tacape", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_jda, 150,
    "Uma clava pesada de madeira maciça de duas mãos, frequentemente cravada de lascas de pedra ou ossos.",
    ["pesado", "madeira", "bárbaro", "duas mãos"]
)

# Armas Simples Ataque à Distância - Disparo
add_item(
    "arma-arco-curto", "Arco Curto", "Armas", "Armas Simples", "Ataque à Distância / Disparo",
    "T$ 30", "1d6", "x3", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Uma arma antiga e comum, este arco é usado primariamente como ferramenta de caça, embora seja usado como arma de guerra por milícias, bandidos e exércitos menos equipados. Pode ser usado montado.",
    ["arco", "disparo", "caça", "montaria"]
)

add_item(
    "arma-besta-leve", "Besta Leve", "Armas", "Armas Simples", "Ataque à Distância / Disparo",
    "T$ 35", "1d8", "19", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Um arco montado sobre uma coronha de madeira com um gatilho, a besta leve é uma arma que dispara virotes com grande potência. Recarregar uma besta leve é uma ação de movimento.",
    ["besta", "virote", "ação de movimento", "potência"]
)

add_item(
    "arma-funda", "Funda", "Armas", "Armas Simples", "Ataque à Distância / Disparo",
    "T$ 0", "1d4", "x2", "Impacto", "Médio", None, None, 1,
    book_jda, 147,
    "Uma tira de couro na qual se coloca uma pedra ou bala de chumbo. A funda é girada rapidamente e a pedra é arremessada pela força centrífuga. Você aplica sua Força às rolagens de dano da funda. Recarregar a funda é uma ação de movimento.",
    ["funda", "couro", "aplica força", "grátis"]
)

# Armas Simples Ataque à Distância - Arremesso
add_item(
    "arma-azagaia", "Azagaia", "Armas", "Armas Simples", "Ataque à Distância / Arremesso",
    "T$ 1", "1d6", "x2", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Uma lança leve e flexível, própria para arremesso. Pode ser usada como arma corpo a corpo, mas você sofre uma penalidade de -5 no teste de ataque.",
    ["lança leve", "arremesso"]
)



# Armas Marciais Corpo a Corpo - Leves
add_item(
    "arma-machadinha", "Machadinha", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 6", "1d6", "x3", "Corte", "Curto", None, None, 1,
    book_jda, 148,
    "Um pequeno machado balanceado de uma mão que pode ser arremessado. É a arma padrão dos anões para combate leve ou à distância.",
    ["machado", "arremesso", "crítico x3", "anão", "leve"]
)


# Armas Marciais Corpo a Corpo - Uma Mão
add_item(
    "arma-cimitarra", "Cimitarra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d6", "18", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Espada com a lâmina curva e muito afiada. A cimitarra é uma arma ágil (beneficia-se de Acuidade com Arma). Margem de ameaça 18-20.",
    ["espada curva", "ágil", "crítico 18", "acuidade"]
)

add_item(
    "arma-espada-longa", "Espada Longa", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "19", "Corte", "-", None, None, 1,
    book_jda, 147,
    "A mais tradicional das espadas, com lâmina reta de dois gumes de cerca de um metro. A arma emblemática dos nobres, cavaleiros e aventureiros de Arton.",
    ["espada", "tradição", "cavaleiro", "nobreza"]
)

add_item(
    "arma-florete", "Florete", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 20", "1d6", "18", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "Uma espada fina e flexível com cesto de proteção para a mão. O florete é uma arma ágil. Margem de ameaça 18-20.",
    ["esgrima", "ágil", "acuidade", "crítico 18"]
)

add_item(
    "arma-machado-de-batalha", "Machado de Batalha", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 10", "1d8", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "Um machado de lâmina larga e pesada montada em cabo curto. É uma arma tradicional dos anões.",
    ["machado", "crítico x3", "anão", "batalha"]
)

add_item(
    "arma-mangual", "Mangual", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Uma haste de madeira ligada por uma corrente a uma esfera de ferro com pontas. O mangual é uma arma versátil, fornecendo +2 em testes para desarmar.",
    ["corrente", "esfera", "versátil", "desarmar"]
)

add_item(
    "arma-martelo-de-guerra", "Martelo de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x3", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Um martelo com cabeça de aço pesada em uma das extremidades e uma ponta na outra. Causa dano crítico triplo.",
    ["martelo", "crítico x3", "guerra", "impacto"]
)

add_item(
    "arma-picareta", "Picareta", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d6", "x4", "Perfuração", "-", None, None, 1,
    book_jda, 149,
    "Uma ferramenta de mineração com ponta de aço curvada reforçada. Causa dano crítico quádruplo (x4).",
    ["mineração", "crítico x4", "perfuração"]
)

add_item(
    "arma-tridente", "Tridente", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 150,
    "Uma lança com três pontas de ferro. O tridente é uma arma versátil, fornecendo +2 em testes para desarmar. Pode ser arremessado.",
    ["três pontas", "versátil", "desarmar", "arremesso"]
)

# Armas Marciais Corpo a Corpo - Duas Mãos
add_item(
    "arma-alabarda", "Alabarda", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d10", "x3", "Corte/Perfuração", "-", None, None, 2,
    book_jda, 146,
    "Uma haste de madeira com 2m de comprimento e uma lâmina de machado com ponta de lança na extremidade. A alabarda é uma arma alongada.",
    ["haste", "alongada", "crítico x3", "guarda"]
)

add_item(
    "arma-alfange", "Alfange", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 75", "2d4", "18", "Corte", "-", None, None, 2,
    book_jda, 146,
    "Uma versão maior da cimitarra, esta espada de lâmina larga e curva é bastante usada por guerreiros do Deserto da Perdição. Margem de ameaça 18-20.",
    ["deserto", "espada curva", "crítico 18"]
)

add_item(
    "arma-foice-grande", "Gadanho", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 18", "2d4", "x4", "Corte", "-", None, None, 2,
    book_jda, 147,
    "Uma grande lâmina curva montada em uma haste de madeira de duas mãos, usada na colheita e temida no combate. Causa dano crítico quádruplo (x4).",
    ["gadanho", "morte", "crítico x4", "colheita"]
)

add_item(
    "arma-lanca-montada", "Lança Montada", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d8", "x3", "Perfuração", "-", None, None, 2,
    book_jda, 148,
    "Uma lança pesada com guarda para a mão, desenvolvida para cavalaria. Se você estiver montado, pode usar uma lança montada com apenas uma mão. Além disso, quando usada numa investida montada, causa +2d8 pontos de dano.",
    ["montada", "cavaleiro", "investida", "uma mão montado"]
)

add_item(
    "arma-machado-de-guerra", "Machado de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "1d12", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Um machado enorme de duas mãos, frequentemente com lâmina dupla, favorito de bárbaros e guerreiros brutais.",
    ["machado gigante", "bárbaro", "crítico x3", "1d12"]
)

add_item(
    "arma-marreta", "Marreta", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "3d4", "x2", "Impacto", "-", None, None, 2,
    book_jda, 148,
    "Uma marreta pesada de duas mãos com uma grande cabeça de ferro montada em um cabo longo de madeira reforçada.",
    ["marreta", "impacto pesado", "3d4", "duas mãos"]
)

add_item(
    "arma-montante", "Montante", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d6", "19", "Corte", "-", None, None, 2,
    book_jda, 150,
    "Enorme e pesada, esta espada de 1,5m de comprimento é uma arma poderosa que desfere golpes devastadores em arcos amplos.",
    ["espada gigante", "2d6", "duas mãos", "devastadora"]
)

# Armas Marciais Ataque à Distância - Disparo
add_item(
    "arma-arco-longo", "Arco Longo", "Armas", "Armas Marciais", "Ataque à Distância / Disparo",
    "T$ 100", "1d8", "x3", "Perfuração", "Longo", None, None, 2,
    book_jda, 146,
    "Este arco reforçado tem a altura de uma pessoa. Ao contrário da versão curta, é primariamente uma arma de guerra. Por ter uma puxada pesada, permite que você aplique sua Força às rolagens de dano (ao contrário de outras armas de disparo). Porém, um arco longo não pode ser usado se você estiver montado.",
    ["arco", "longo", "aplica força", "alcance longo", "guerra"]
)

add_item(
    "arma-besta-pesada", "Besta Pesada", "Armas", "Armas Marciais", "Ataque à Distância / Disparo",
    "T$ 50", "1d12", "19", "Perfuração", "Médio", None, None, 2,
    book_jda, 146,
    "Versão maior e mais potente da besta leve. Recarregar uma besta pesada é uma ação padrão.",
    ["besta pesada", "1d12", "ação padrão", "potência"]
)

# Armas Exóticas
add_item(
    "arma-adaga-de-aparar", "Adaga de Aparar", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 50", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_jda, 146,
    "Esta adaga possui uma guarda reforçada e alargada em cruz. Quando empunha esta adaga em uma das mãos, você recebe +1 na Defesa. É uma arma ágil.",
    ["defesa +1", "ágil", "esgrima", "guarda"]
)

add_item(
    "arma-chicote", "Chicote", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 2", "1d3", "x2", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Esta arma pode ser usada para atacar inimigos a até 4,5m e pode se enroscar nas mãos, pernas ou armas de seus adversários. O chicote é uma arma ágil e versátil, fornecendo +2 em testes para derrubar ou desarmar.",
    ["alcance 4.5m", "ágil", "versátil", "derrubar", "desarmar"]
)

add_item(
    "arma-espada-bastarda", "Espada Bastarda", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 35", "1d10/1d12", "19", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Mais longa e pesada que a espada longa, esta arma é balanceada para ser usada com uma mão (se você tiver proficiência com armas exóticas) ou com duas mãos (como uma arma marcial, causando 1d12 de dano).",
    ["versátil", "uma mão exótica", "duas mãos marcial", "1d10 ou 1d12"]
)

add_item(
    "arma-katana", "Katana", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 100", "1d8/1d10", "19", "Corte", "-", None, None, 1,
    book_jda, 148,
    "A tradicional espada de lâmina curva e de um só gume dos samurais de Tamu-ra. A katana é uma arma ágil. Você pode usá-la com uma mão (se for proficiente com armas exóticas) ou com duas mãos (como arma marcial, causando 1d10 de dano).",
    ["tamu-ra", "samurai", "ágil", "acuidade", "uma ou duas mãos"]
)

add_item(
    "arma-machado-anao", "Machado Anão", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d10", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "Um machado de cabo curto e lâmina pesadíssima forjado em Doherimm. Uma criatura com proficiência em armas marciais pode usá-lo com duas mãos.",
    ["anão", "doherimm", "crítico x3", "1d10"]
)

add_item(
    "arma-corrente-de-espinhos", "Corrente de Espinhos", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 25", "2d4/2d4", "19", "Perfuração", "-", None, None, 2,
    book_jda, 147,
    "Uma corrente de metal flexível recoberta de lâminas e pontas pontiagudas. É uma arma ágil, dupla e versátil (+2 para derrubar ou desarmar). Pode atacar alvos adjacentes ou a até 3m de distância.",
    ["corrente", "dupla", "ágil", "versátil", "alcance 3m"]
)

add_item(
    "arma-espada-taurica", "Espada Táurica", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d8", "x3", "Corte", "-", None, None, 2,
    book_jda, 147,
    "Uma espada maciça criada pelos minotauros de Tapista. Devido ao seu peso descomunal, exige Força 3 ou superior para ser empunhada sem penalidade adicional.",
    ["minotauro", "tapista", "2d8", "força 3", "devastadora"]
)

add_item(
    "arma-machado-taurico", "Machado Táurico", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d8", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Um machado gigantesco com cabeça dupla de bronze maciço criado por artífices táuricos. Exige Força 3 para ser empunhado.",
    ["minotauro", "tapista", "2d8", "crítico x3"]
)

add_item(
    "arma-shuriken", "Shuriken", "Armas", "Armas Exóticas", "Ataque à Distância / Arremesso",
    "T$ 1", "1d4", "x2", "Perfuração", "Curto", None, None, 0.1,
    book_jda, 150,
    "Uma pequena estrela de metal afiada de arremesso originária de Tamu-ra. Sacar um shuriken é uma ação livre. Você pode arremessar múltiplos shurikens com poderes adequados.",
    ["estrela ninja", "tamu-ra", "ação livre sacar", "arremesso rápido"]
)

# Armas de Fogo
add_item(
    "arma-pistola", "Pistola", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 250", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_jda, 149,
    "Uma arma de fogo de cano curto de carregar pela boca originária das oficinas de Zakharov ou Smokestone. Recarregar uma pistola é uma ação padrão (ou de movimento com munição especial). Margem 19 / Crítico x3.",
    ["pólvora", "zakharov", "tiro", "crítico 19/x3"]
)

add_item(
    "arma-mosquete", "Mosquete", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 500", "2d8", "19/x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 150,
    "Uma arma de fogo de uso difícil, mas com poder devastador. Recarregar um mosquete é uma ação completa. Causa 2d8 de dano com crítico 19/x3.",
    ["pólvora", "tiro longo", "devastador", "ação completa recarregar"]
)

# --- 1.1.1 MUNIÇÕES (Tabela 3-4, pág 151) ---
add_item(
    "municao-flechas-20", "Flechas (20)", "Munições", "Munições", "Munição de Arco",
    "T$ 2", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Hastes de madeira com ponta de metal e penas na cauda, usadas para disparar com arcos curtos ou arcos longos. Vendidas em aljavas de 20 unidades.",
    ["flecha", "aljava", "arco"]
)

add_item(
    "municao-virotes-20", "Virotes (20)", "Munições", "Munições", "Munição de Besta",
    "T$ 2", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Projéteis mais curtos e pesados que flechas, feitos para disparar com bestas leves ou pesadas. Vendidos em caixas ou bolsas com 20 unidades.",
    ["virote", "besta", "caixa"]
)

add_item(
    "municao-balas-de-funda-20", "Balas de Funda (20)", "Munições", "Munições", "Munição de Funda",
    "T$ 1", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Esferas de chumbo fundido de peso uniforme, projetadas para conferir máxima precisão e impacto quando arremessadas por fundas. Saco com 20 unidades.",
    ["chumbo", "funda", "esferas"]
)

add_item(
    "municao-balas-e-polvora-10", "Balas de Arma de Fogo e Pólvora (10)", "Munições", "Munições", "Munição de Arma de Fogo",
    "T$ 20", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Esferas de chumbo e doses de pólvora seca necessárias para alimentar pistolas e mosquetes por 10 disparos.",
    ["pólvora", "tiro", "bala de chumbo", "pistola", "mosquete"]
)

# --- 1.2 ARMADURAS & ESCUDOS (Tabela 3-5, págs 152-153, Descrições págs 154-155) ---
# Armaduras Leves (JDA)
add_item(
    "armadura-acolchoada", "Armadura Acolchoada", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 5", None, None, None, None, 1, 0, 2,
    book_jda, 154,
    "Uma túnica almofadada feita em linho ou lã acolchoada com camadas de feltro. É a armadura mais leve, mas protege todo o corpo, fornecendo +2 em Fortitude contra frio extremo.",
    ["linho", "lã", "leve", "fortitude"]
)

add_item(
    "armadura-de-couro", "Armadura de Couro", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 20", None, None, None, None, 2, 0, 2,
    book_jda, 154,
    "O peitoral desta armadura é feito de couro curtido em óleo fervente, para ficar mais rígido, enquanto as demais partes são feitas de couro flexível.",
    ["couro", "flexível", "batedor", "ladino"]
)

add_item(
    "armadura-couro-batido", "Couro Batido", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 35", None, None, None, None, 3, -1, 2,
    book_jda, 154,
    "Versão mais pesada da armadura de couro, reforçada com rebites de metal e tiras de aço flexível.",
    ["couro", "rebites", "reforçada"]
)

add_item(
    "armadura-gibao-de-peles", "Gibão de Peles", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 25", None, None, None, None, 4, -3, 2,
    book_jda, 154,
    "Usada principalmente por bárbaros e selvagens, esta armadura é formada por várias camadas de peles e couro espesso de animais.",
    ["peles", "bárbaro", "selvagem", "defesa 4"]
)

add_item(
    "armadura-couraca", "Couraça", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 500", None, None, None, None, 5, -4, 2,
    book_jda, 154,
    "A mais robusta das armaduras leves, formada por uma placa metálica inteiriça que protege o peito e as costas, presa sobre um casaco de couro acolchoado.",
    ["peitoral", "aço", "leve pesada", "defesa 5"]
)

# Armaduras Pesadas (JDA)
add_item(
    "armadura-brunea", "Brunea", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 50", None, None, None, None, 5, -2, 5,
    book_jda, 154,
    "Colete de couro coberto com plaquetas de metal sobrepostas, como escamas de um peixe. Por ser barata de produzir, é a armadura mais utilizada no Reinado por soldados de infantaria e guardas de castelo.",
    ["escamas", "infantaria", "barata", "defesa 5"]
)

add_item(
    "armadura-cota-de-malha", "Cota de Malha", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 150", None, None, None, None, 6, -2, 5,
    book_jda, 154,
    "Longa veste de anéis metálicos interligados, formando uma malha flexível e resistente, que vai até os joelhos sobre um forro acolchoado.",
    ["anéis", "malha", "flexível", "defesa 6"]
)

add_item(
    "armadura-loriga-segmentada", "Loriga Segmentada", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 250", None, None, None, None, 7, -3, 5,
    book_jda, 154,
    "Composta por tiras horizontais de metal articuladas sobre tiras de couro internas, esta armadura pesada é muito utilizada por legionários do Império de Tauron.",
    ["tiras", "tauron", "legionário", "defesa 7"]
)

add_item(
    "armadura-meia-armadura", "Meia Armadura", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 600", None, None, None, None, 8, -4, 5,
    book_jda, 154,
    "Uma cota de malha reforçada com placas de metal (peitoral, caneleiras e braçadeiras) que protegem as partes vitais do corpo. Inclui um elmo de aço.",
    ["placas", "malha reforçada", "elmo", "defesa 8"]
)

add_item(
    "armadura-armadura-completa", "Armadura Completa", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 3.000", None, None, None, None, 10, -5, 5,
    book_jda, 154,
    "A mais forte e pesada das armaduras, formada por placas de metal forjadas e encaixadas de modo a cobrir o corpo inteiro. Inclui uma túnica acolchoada para ser usada sob as placas. Correias e fivelas distribuem o peso da armadura pelo corpo inteiro. Esta armadura precisa ser feita sob medida para cada usuário; um ferreiro cobra T$ 200 para adaptar uma armadura completa a um novo usuário.",
    ["placas completas", "cavaleiro", "sob medida", "defesa 10"]
)

# Escudos (JDA)
add_item(
    "armadura-escudo-leve", "Escudo Leve", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 5", None, None, None, None, 1, -1, 1,
    book_jda, 154,
    "Tipicamente feito de madeira, este escudo é amarrado no antebraço, deixando a mão livre. Você pode carregar um objeto na mão que empunha o escudo, mas não manusear uma arma.",
    ["madeira", "antebraço", "mão livre", "defesa 1"]
)

add_item(
    "armadura-escudo-pesado", "Escudo Pesado", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 15", None, None, None, None, 2, -2, 2,
    book_jda, 154,
    "Normalmente feito de aço ou carvalho maciço reforçado, este escudo é preso ao antebraço e também deve ser empunhado com firmeza, impedindo o usuário de usar aquela mão.",
    ["aço", "carvalho", "empunhadura firme", "defesa 2"]
)

# --- 1.3 ITENS GERAIS (Tabela 3-6, pág 155-157, Descrições págs 155-163) ---
# Equipamento de Aventura
add_item(
    "item-agua-benta", "Água Benta", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 10", None, None, None, "Curto", None, None, 0.5,
    book_jda, 155,
    "Água abençoada por um clérigo de uma divindade bondosa. Pode ser arremessada como uma arma de arremesso contra mortos-vivos ou criaturas da Tormenta, causando 2d6 pontos de dano radiante.",
    ["sagrado", "radiante", "morto-vivo", "arremesso"]
)

add_item(
    "item-algemas", "Algemas", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 15", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Um par de braceletes de ferro ligados por uma corrente resistente. Prender uma criatura exige que ela esteja indefesa ou agarrada. Escapar das algemas exige um teste de Acrobacia (CD 25) ou quebrar o metal (Atletismo CD 25).",
    ["ferro", "prender", "captura", "acrobacia"]
)

add_item(
    "item-arpeu", "Arpéu", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Um gancho de metal com três ou quatro garras curvadas. Quando amarrado a uma corda, fornece +2 em testes de Atletismo para escalar superfícies onde possa ser fixado.",
    ["gancho", "escalada", "corda", "atletismo"]
)

add_item(
    "item-bandoleira-de-pocoes", "Bandoleira de Poções", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Um cinto de couro usado a tiracolo com pequenos bolsos para até 4 frascos de preparados alquímicos ou poções. Sacar um item da bandoleira é uma ação livre.",
    ["poções", "ação livre sacar", "cinto", "alquimia"]
)

add_item(
    "item-barraca", "Barraca", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Uma tenda de lona resistente capaz de abrigar até duas pessoas confortavelmente durante o descanso ao relento, protegendo de chuva e vento.",
    ["acampamento", "descanso", "abrigo", "lona"]
)

add_item(
    "item-corda", "Corda", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Uma corda resistente de cânhamo com 15 metros de comprimento. Suporta até 500kg de peso. Fornece +2 em testes de Atletismo para escalada com apoio.",
    ["cânhamo", "escalada", "amarrar", "15 metros"]
)

add_item(
    "item-espelho", "Espelho", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Uma chapa de aço polido de bolso. Útil para espiar ao redor de cantos sem se expor ou para sinalizar com reflexos à luz do sol.",
    ["aço polido", "espiar", "sinalização", "reflexo"]
)

add_item(
    "item-lampiao", "Lampião", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 7", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Um lampião de metal com painéis de vidro e alça. Queima uma dose de óleo por 6 horas, iluminando um raio de 9 metros com luz plena e mais 9 metros com luz fraca.",
    ["luz", "óleo", "iluminação", "visão"]
)

add_item(
    "item-mochila", "Mochila", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 2", None, None, None, None, None, None, 0,
    book_jda, 156,
    "Uma bolsa de couro ou lona com alças para as costas. Permite carregar itens com praticidade.",
    ["mochila", "bolsa", "carga"]
)

add_item(
    "item-mochila-de-aventureiro", "Mochila de Aventureiro", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 0,
    book_jda, 156,
    "Uma mochila de couro reforçado com presilhas, bolsos e divisórias. Aumenta o limite de carga do personagem em +2 espaços.",
    ["carga +2", "mochila", "capacidade", "aventura"]
)

add_item(
    "item-oleo-frasco", "Óleo (Frasco)", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 0.1", None, None, None, None, None, None, 0.5,
    book_jda, 156,
    "Um frasco com óleo combustível suficiente para alimentar um lampião ou tocha por 6 horas. Pode ser derramado no chão e incendiado.",
    ["combustível", "lampião", "fogo", "óleo"]
)

add_item(
    "item-organizador-de-pergaminhos", "Organizador de Pergaminhos", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 25", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Um estojo de couro cilíndrico impermeável com divisórias para até 6 pergaminhos. Sacar um pergaminho guardado no organizador é uma ação livre.",
    ["pergaminhos", "ação livre sacar", "magia", "estojo"]
)

add_item(
    "item-pe-de-cabra", "Pé de Cabra", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 2", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Uma barra de ferro resistente com extremidade curvada e chanfrada. Fornece +2 em testes de Atletismo para forçar portas e quebrar objetos de madeira.",
    ["ferro", "arrombar", "alavanca", "atletismo"]
)

add_item(
    "item-saco-de-dormir", "Saco de Dormir", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Uma manta grossa acolchoada forrada de lã que se fecha com amarras. Fornece o conforto necessário para recuperar PV e PM em acampamentos ao ar livre.",
    ["descanso", "acampamento", "recuperação", "sono"]
)

add_item(
    "item-simbolo-sagrado", "Símbolo Sagrado", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Um medalhão esculpido com o símbolo heráldico de uma divindade do Panteão. Clérigos e paladinos precisam empunhar seu símbolo sagrado para conjurar suas magias divinas.",
    ["deus", "panteão", "foco divino", "clérigo", "paladino"]
)

add_item(
    "item-tocha", "Tocha", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 0.1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Um bastão de madeira com estopa embebida em piche na ponta. Queima por 1 hora, iluminando um raio de 6 metros. Se usada como arma improvisada, causa 1d4 de dano de fogo.",
    ["fogo", "luz", "iluminação", "improvisada"]
)

add_item(
    "item-vara-de-madeira-3m", "Vara de Madeira (3m)", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 0.2", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Uma vara longa de madeira flexível e resistente. Muito útil para acionar armadilhas à distância ou testar a profundidade de fossos e poços sem se arriscar.",
    ["haste", "armadilhas", "segurança", "fosso"]
)

# Ferramentas (JDA)
add_item(
    "item-alaude-elfico", "Alaúde Élfico", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 300", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um instrumento de cordas feito em madeira leve de Lenórienn com cordas de seda mágica. Fornece +2 em testes de Atuação (música) e reduz o custo de uma música de bardo em -1 PM.",
    ["alaúde", "élfico", "bardo", "-1 pm música", "atuação +2"]
)

add_item(
    "item-estojo-de-disfarces", "Estojo de Disfarces", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Maquiagens, perucas, próteses de cera, tinturas e apetrechos teatrais. Permite usar a perícia Enganação para se disfarçar e fornece +2 no teste.",
    ["enganação", "disfarce", "peruca", "maquiagem"]
)

add_item(
    "item-flauta-mistica", "Flauta Mística", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 150", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Uma flauta entalhada em madeira nobre com orifícios de prata. Fornece +1 na CD para resistir às habilidades de música de bardo do usuário.",
    ["bardo", "cd +1", "música", "flauta"]
)

add_item(
    "item-gazua", "Gazua", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um conjunto de arames e palhetas de aço temperado. Permite realizar testes de Ladinagem para abrir fechaduras.",
    ["abrir fechaduras", "ladinagem", "arrombamento"]
)

add_item(
    "item-instrumento-musical", "Instrumento Musical", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 35", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um instrumento comum (flauta, alaúde, tambor ou cítara). Permite usar a perícia Atuação e habilidades de bardo.",
    ["música", "bardo", "atuação"]
)

add_item(
    "item-luneta", "Luneta", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 100", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um tubo com lentes de cristal polido. Fornece +2 em testes de Percepção para observar objetos ou criaturas distantes.",
    ["lentes", "cristal", "percepção", "distância"]
)

add_item(
    "item-maleta-de-medicamentos", "Maleta de Medicamentos", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Faixas de linho, unguentos anti-sépticos, agulhas de sutura e instrumentos cirúrgicos. Permite realizar testes de Cura para primeiros socorros sem penalidade e fornece +2 em testes de Cura.",
    ["primeiros socorros", "cura", "medicina", "sutura"]
)

# Vestuário (JDA)
add_item(
    "item-chapeu-arcano", "Chapéu Arcano", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um chapéu pontudo ou de abas largas feito de feltro fino ou veludo, símbolo tradicional dos arcanistas. Fornece +1 em testes de Misticismo.",
    ["misticismo", "arcano", "mago", "chapéu"]
)

add_item(
    "item-gorro-de-ervas", "Gorro de Ervas", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 75", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um gorro de lã com forro embebido em infusões de ervas calmantes. Fornece +1 em testes de Vontade.",
    ["vontade +1", "ervas", "mental", "gorro"]
)

add_item(
    "item-manopla", "Manopla", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Luva metálica que permite socos mais perigosos — o dano de seus ataques desarmados torna-se letal. Uma manopla conta como uma arma para receber melhorias e encantos para usá-los em seus ataques desarmados.",
    ["vestuário", "ataque desarmado", "dano letal", "luva de metal", "manopla"]
)

add_item(
    "item-luva-de-pelica", "Luva de Pelica", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Luvas finas e flexíveis de couro macio. Fornecem +1 em testes de Ladinagem para prestidigitação e furto de pequenos objetos.",
    ["ladinagem +1", "furto", "couro macio", "luvas"]
)

add_item(
    "item-manto-camuflado", "Manto Camuflado", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 12", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um manto com estampa manchada em tons de verde, marrom ou cinza. Fornece +1 em testes de Furtividade no terreno correspondente.",
    ["furtividade +1", "camuflagem", "floresta", "manto"]
)

add_item(
    "item-manto-eclesiastico", "Manto Eclesiástico", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Uma túnica cerimonial bordada com fios de ouro e símbolos sagrados. Fornece +1 em testes de Religião.",
    ["religião +1", "clérigo", "sagrado", "manto"]
)

add_item(
    "item-robe-mistico", "Robe Místico", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um manto longo de seda com inscrições arcanas tecidas no forro. Fornece +1 na Defesa contra magias.",
    ["defesa contra magia +1", "arcanista", "seda", "robe"]
)

add_item(
    "item-sapatos-de-camurca", "Sapatos de Camurça", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 8", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Calçados com solado macio que abafam o som dos passos. Fornecem +1 em testes de Furtividade para se mover silenciosamente.",
    ["furtividade +1", "silêncio", "passos", "sapatos"]
)

add_item(
    "item-traje-da-corte", "Traje da Corte", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 100", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Roupas finíssimas de seda, veludo e pedrarias com corte nobre. Fornecem +1 em testes de Diplomacia e Nobreza com membros da nobreza.",
    ["diplomacia +1", "nobreza +1", "corte", "elegância"]
)

add_item(
    "item-traje-de-viajante", "Traje de Viajante", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 0,
    book_jda, 159,
    "Botas de couro resistentes, calças grossas, camisa de linho e casaco impermeável. Traje padrão para expedições por terrenos acidentados.",
    ["viagem", "conforto", "explorador"]
)

# Esotéricos (JDA)
add_item(
    "item-bolsa-de-po", "Bolsa de Pó", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 300", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma bolsinha com pós minerais e pós de fadas. Quando você lança uma magia que afeta uma área, pode aumentar a área em 50% gastando 1 PM adicional.",
    ["área aumentada", "esotérico", "pó mágico", "conjurador"]
)

add_item(
    "item-cajado-arcano", "Cajado Arcano", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 1.000", None, None, None, None, None, None, 2,
    book_jda, 160,
    "Um cajado de madeira nobre talhado com runas e encimado por um cristal canalizador. Permite lançar magias com alcance aumentado em um passo (Curto para Médio, Médio para Longo).",
    ["foco arcano", "alcance", "runas", "cristal"]
)

add_item(
    "item-cetro-elemental", "Cetro Elemental", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma barra de metal adornada com joias elementais (rubi para fogo, safira para frio, topázio para eletricidade, esmeralda para ácido). Aumenta o dano de magias do elemento correspondente em +2 por dado de dano.",
    ["dano elemental +2", "fogo", "frio", "ácido", "eletricidade"]
)

add_item(
    "item-costela-de-lich", "Costela de Lich", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 300", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um fragmento ósseo preservado com necromancia arcana. Suas magias da escola Necromancia têm sua CD aumentada em +1.",
    ["necromancia", "cd +1", "osso", "morto-vivo"]
)

add_item(
    "item-dedo-de-ente", "Dedo de Ente", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 200", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um galho vivo arrancado de um guardião da floresta secular. Aumenta a cura de suas magias curativas em +1 PV por dado rolado.",
    ["cura +1 por dado", "natureza", "druida", "clérigo"]
)

add_item(
    "item-luva-de-ferro", "Luva de Ferro", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 150", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma manopla ornamentada gravada com runas de abjuração. Concede +1 na Defesa enquanto você mantiver uma magia de sustentação ativa.",
    ["defesa +1", "abjuração", "sustentada", "manopla esotérica"]
)

add_item(
    "item-medalhao-de-prata", "Medalhão de Prata", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um amuleto prateado com relevos geométricos sagrados. Suas magias divinas de alcance Pessoal têm sua duração duplicada.",
    ["duração dupla", "divina", "prata", "medalhão"]
)

add_item(
    "item-orbe-cristalino", "Orbe Cristalino", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma esfera perfeita de quartzo transparente ou obsidiana. Quando empunhado por um conjurador, aumenta a CD para resistir às suas magias em +1.",
    ["cd +1", "cristal", "resistência", "foco esotérico"]
)

add_item(
    "item-tomo-hermetico", "Tomo Hermético", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 1.500", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um livro encadernado em couro com fecho de prata repleto de anotações místicas arcanas. Permite que um arcanista prepare uma magia adicional.",
    ["magia extra", "grimório", "estudo", "arcanista"]
)

add_item(
    "item-varinha-arcana", "Varinha Arcana", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 100", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma haste delgada de madeira nobre ou osso talhado. Quando você lança uma magia que causa dano enquanto empunha uma varinha arcana, essa magia causa +1 ponto de dano por dado de dano.",
    ["dano mágico", "varinha", "foco", "arcanista"]
)

# Alquímicos - Preparados (JDA)
add_item(
    "item-acido", "Ácido", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 10", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Um frasco com líquido corrosivo que pode ser arremessado. Causa 2d4 pontos de dano de ácido na criatura atingida e 1 ponto de dano de ácido nas criaturas adjacentes.",
    ["ácido", "corrosão", "arremesso", "dano de área"]
)

add_item(
    "item-balsamo-restaurador", "Bálsamo Restaurador", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 10", None, None, None, None, None, None, 0.5,
    book_jda, 161,
    "Uma pasta espessa feita de ervas medicinais e óleos cicatrizantes. Aplicar o bálsamo em ferimentos com uma ação padrão recupera 2d4 pontos de vida.",
    ["cura", "pv", "unguento", "medicina"]
)

add_item(
    "item-bomba", "Bomba", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 50", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Uma esfera de cerâmica recheada de pólvora com pavio curto. Ao explodir, causa 6d6 pontos de dano de impacto e fogo em todas as criaturas a até 3m (Reflexos CD 15 reduz à metade).",
    ["explosão", "6d6", "área 3m", "pólvora"]
)

add_item(
    "item-fogo-alquimico", "Fogo Alquímico", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 10", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Uma substância gelatinosa e volátil que entra em combustão ao contato com o ar. Ao ser arremessado, explode causando 1d6 pontos de dano de fogo no alvo e incendiando-o (1d6 de dano contínuo por rodada até apagar).",
    ["fogo", "combustão", "arremesso", "dano contínuo"]
)

add_item(
    "item-fumaca-negra", "Fumaça Negra", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 15", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Um frasco com pó que produz uma nuvem densa de fumaça escura que ocupa um cubo de 4,5m de lado por 1d4 rodadas, fornecendo camuflagem total.",
    ["fumaça", "camuflagem", "fuga", "cegueira"]
)

add_item(
    "item-po-de-cegueira", "Pó de Cegueira", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 30", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Um pó cáustico fino arremessado nos olhos de uma criatura adjacente. O alvo deve passar em um teste de Fortitude (CD 15) ou fica cego por 1d4 rodadas.",
    ["cegueira", "fortitude cd 15", "debilitante"]
)

# Alquímicos - Catalisadores (JDA)
add_item(
    "item-essencia-de-mana", "Essência de Mana", "Itens Gerais", "Alquímicos - Catalisadores", "Alquímicos - Catalisadores",
    "T$ 50", None, None, None, None, None, None, 0.5,
    book_jda, 162,
    "Um líquido azul brilhante destilado de flores mágicas raras. Beber a essência com uma ação padrão recupera 1d4 pontos de mana (PM) imediatamente.",
    ["pm", "mana", "recuperação", "poção azul"]
)

add_item(
    "item-essencia-abissal", "Essência Abissal", "Itens Gerais", "Alquímicos - Catalisadores", "Alquímicos - Catalisadores",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_jda, 162,
    "Fluido negro destilado do sangue de demônios e extraplanar sombrios. Ao conjurar uma magia de trevas, aumenta o dano causado em +1 por dado de dano.",
    ["trevas", "abissal", "dano aumentado", "catalisador"]
)

# Alquímicos - Venenos (JDA)
add_item(
    "item-beladona", "Beladona", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 1.500", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Veneno vegetal mortal extraído de bagas raras. Tipo: Ingestão ou Contato. O alvo deve passar em Fortitude (CD 25) ou sofre 4d12 pontos de dano de veneno e fica inconsciente.",
    ["veneno mortal", "cd 25", "4d12", "letal"]
)

add_item(
    "item-peconha-comum", "Peçonha Comum", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 15", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Veneno extraído de víboras e escorpiões do ermo. Tipo: Contato com arma. Causa 1d12 pontos de dano de veneno (Fortitude CD 15 reduz à metade).",
    ["veneno", "arma", "1d12", "peçonha"]
)

add_item(
    "item-peconha-concentrada", "Peçonha Concentrada", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 90", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Versão purificada e destilada da peçonha comum. Causa 2d12 pontos de dano de veneno e impõe a condição fraco por 1 hora (Fortitude CD 18).",
    ["veneno", "fraco", "2d12", "cd 18"]
)

# Alimentação (JDA)
add_item(
    "item-gorad-quente", "Gorad Quente", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 18", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Uma porção de chocolate espesso e aromático servido fervendo, especialidade das estalagens nobres de Deheon. Concede +1 em testes de Fortitude e Vontade por 4 horas.",
    ["chocolate", "conforto", "bônus resistência", "estalagem"]
)

add_item(
    "item-prato-do-aventureiro", "Prato do Aventureiro", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 1", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Ensopado farto de carne de caça, raízes e pão rústico. Uma refeição reforçada que recupera +1 PV adicional durante o descanso.",
    ["refeição", "recuperação", "descanso", "ensopado"]
)

# Animais (JDA)
add_item(
    "item-cavalo-de-guerra", "Cavalo de Guerra", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 400", None, None, None, None, None, None, 0,
    book_jda, 163,
    "Um corcel imponente treinado para não se assustar com o ruído de batalha. Conta como um parceiro Guardião ou Montaria combatente que concede bônus em testes de investida montada.",
    ["montaria", "cavalo", "guerra", "parceiro"]
)

# Veículos (JDA)
add_item(
    "item-carroca", "Veículos", "Veículos", "Veículos", "Veículo Terrestre",
    "T$ 150", None, None, None, None, None, None, 0,
    book_jda, 163,
    "Veículo de madeira de quatro rodas tracionado por animais de carga. Tem capacidade de carga para até 100 espaços de itens e suprimentos de expedição.",
    ["transporte", "carga 100", "viagem", "tração animal"]
)

add_item(
    "item-carruagem", "Veículos", "Veículos", "Veículos", "Veículo Terrestre",
    "T$ 500", None, None, None, None, None, None, 0,
    book_jda, 163,
    "Veículo fechado e estofado de luxo para transporte confortável de nobres e cortesãos com janelas de vidro e suspensão de correias.",
    ["luxo", "nobreza", "transporte urbano"]
)

# --- 1.4) ITENS SUPERIORES & MATERIAIS ESPECIAIS (JDA, Tabela 3-8, pág 164-168) ---
add_item(
    "melhoria-afiada", "Afiada", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, "+1 margem", None, None, None, None, 0,
    book_jda, 165,
    "A lâmina ou ponta da arma é trabalhada com um fio navalha extraordinário. A margem de ameaça da arma aumenta em +1 (ex: de 19 para 18). Só pode ser aplicada a armas que causem dano de corte ou perfuração.",
    ["crítico +1", "ameaça", "fio de navalha", "lâmina"]
)

add_item(
    "melhoria-alongada", "Alongada", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, None, None, "+1.5m", None, None, 0,
    book_jda, 165,
    "A haste ou lâmina é forjada com comprimento estendido sem perder o equilíbrio, permitindo atacar alvos a até 1,5m além do alcance corpo a corpo normal.",
    ["alcance extra", "haste", "espaçamento"]
)

add_item(
    "melhoria-certeira", "Certeira", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 165,
    "O equilíbrio milimétrico da arma concede +1 nos testes de ataque desferidos com ela.",
    ["ataque +1", "precisão", "balanceada"]
)

add_item(
    "melhoria-cruel", "Cruel", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", "+2 dano", None, None, None, None, None, 0,
    book_jda, 165,
    "Dentes serrilhados ou espigões cruéis aumentam a severidade dos ferimentos, fornecendo +2 nas rolagens de dano.",
    ["dano +2", "serrilhado", "ferimentos"]
)

add_item(
    "melhoria-macica", "Maciça", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, "+1 multiplicador", None, None, None, None, 0,
    book_jda, 165,
    "A arma é forjada com distribuição de peso pesada e sólida. O multiplicador de crítico da arma aumenta em +1 (ex: de x2 para x3).",
    ["crítico pesado", "multiplicador", "impacto", "dano bruto"]
)

add_item(
    "melhoria-precisa", "Precisa", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, "+1 margem", None, None, None, None, 0,
    book_jda, 165,
    "Para armas de disparo ou arremesso, miras finamente calibradas aumentam a margem de ameaça de ataque à distância em +1.",
    ["tiro certeiro", "mira", "disparo crítico"]
)

add_item(
    "melhoria-pungente", "Pungente", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", "+2 dano", None, None, None, None, None, 0,
    book_jda, 165,
    "A geometria e peso da arma aumentam o impacto do golpe, fornecendo +2 nas rolagens de dano.",
    ["dano +2", "força", "letal"]
)

add_item(
    "melhoria-reforcada", "Reforçada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, 1, 0, 0,
    book_jda, 166,
    "Placas suplementares ou rebites de liga temperada aumentam o bônus de Defesa da armadura ou escudo em +1.",
    ["defesa +1", "blindagem", "resistência"]
)

add_item(
    "melhoria-ajustada", "Ajustada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, None, -1, 0,
    book_jda, 166,
    "Articulações com dobradiças polidas e correias ergonômicas reduzem a penalidade de armadura em 1 ponto (ex: de -2 para -1).",
    ["mobilidade", "penalidade -1", "agilidade"]
)

add_item(
    "melhoria-blindada", "Blindada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 166,
    "A armadura recebe reforços contra impactos violentos. Fornece Redução de Dano (RD) 2 contra dano de corte e impacto.",
    ["rd 2", "blindagem", "impacto", "corte"]
)

add_item(
    "melhoria-sob-medida", "Sob Medida", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, None, None, -1,
    book_jda, 166,
    "Feita exclusivamente para a compleição anatômica do usuário, reduz o espaço ocupado pela armadura em 1.",
    ["espaço -1", "peso", "ergonomia"]
)

add_item(
    "melhoria-harmonizada", "Harmonizada", "Itens Superiores", "Melhorias", "Melhoria de Esotérico",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 167,
    "O item esotérico é afinado harmonicamente com a energia mística de uma magia específica. Reduz o custo em PM dessa magia em -1 PM.",
    ["-1 pm", "afinidade", "magia favorita", "esotérico"]
)

add_item(
    "melhoria-canalizadora", "Canalizadora", "Itens Superiores", "Melhorias", "Melhoria de Esotérico",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 167,
    "Estrutura com filamentos condutores que facilitam a drenagem de poder. Fornece +1 em testes de Misticismo para identificar magias e manipular itens mágicos.",
    ["canalização", "misticismo +1", "foco"]
)

# Materiais Especiais (JDA)
add_item(
    "material-aco-rubi", "Aço-Rubi", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.000", None, None, None, None, None, None, 0,
    book_jda, 167,
    "Um metal avermelhado raro forjado com cinzas da Tormenta e sangue de dragão. Armas de aço-rubi ignoram 10 pontos de redução de dano (RD) de qualquer alvo. Armaduras fornecem RD 2 contra todos os tipos de dano.",
    ["ignora rd 10", "rd 2", "metal rubi", "tormenta"]
)

add_item(
    "material-adamante", "Adamante", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.500", None, None, None, None, None, None, 0,
    book_jda, 167,
    "O metal mais denso e duro de Arton. Armas de adamante aumentam o dano em um passo (ex: 1d6 para 1d8). Armaduras e escudos pesados feitos de adamante fornecem RD 5 contra dano físico.",
    ["metal indestrutível", "passo de dano +1", "rd 5"]
)

add_item(
    "material-gelo-eterno", "Gelo Eterno", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.000", "+1d6 frio", None, None, None, None, None, 0,
    book_jda, 167,
    "Gelo glacial das Montanhas Uivantes que nunca derrete. Armas feitas de gelo eterno causam +1d6 pontos de dano de frio. Armaduras concedem Resistência a Frio 10.",
    ["frio", "+1d6 frio", "uivantes", "res frio 10"]
)

add_item(
    "material-madeira-de-tollon", "Madeira de Tollon", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 168,
    "Uma madeira negra e densa nativa das florestas de Tollon com propriedades canalizadoras. Reduz o custo em PM de uma magia lançada com o item em -1 PM.",
    ["tollon", "madeira mágica", "-1 pm", "canalizador"]
)

add_item(
    "material-materia-vermelha", "Matéria Vermelha", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.500", "+1d6 lefeu", None, None, None, None, None, 0,
    book_jda, 168,
    "Matéria viva da tempestade rubra cristalizada. Armas causam +1d6 de dano contra criaturas artonianas não lefeu. Concede +1 poder da Tormenta sem contar para perda de Carisma.",
    ["tormenta", "rubra", "lefeu", "poder da tormenta"]
)

add_item(
    "material-mitral", "Mitral", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.000", None, None, None, None, None, -2, -1,
    book_jda, 168,
    "Conhecido como prata élfica, este metal prateado é tão resistente quanto o aço, mas extremamente leve. Armaduras pesadas de mitral contam como leves. Reduz a penalidade de armadura em 2 e o espaço em 1.",
    ["élfico", "ultraleve", "penalidade -2", "armadura pesada vira leve"]
)

add_item(
    "material-prata", "Prata", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 168,
    "Metal nobre forjado em revestimento sobre lâminas e projéteis. Armas de prata ignoram a RD de licantropos e mortos-vivos incorpóreos.",
    ["licantropo", "lobisomem", "morto-vivo", "prateada"]
)

# =========================================================================================
# 2. LIVRO: T20 HERÓIS DE ARTON (v1.1)
# =========================================================================================

# --- 2.1) ARMAS (HDA, Tabela 3-1, págs 218-219, Descrições págs 216-222) ---
# Armas Simples
add_item(
    "arma-bastao-ludico", "Bastão Lúdico", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 5", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_hda, 218,
    "Um bastão de madeira com acolchoamento e sinos, usado por bufões e artistas para apresentações. Causa dano não letal e concede +2 em testes de Atuação.",
    ["bufão", "bardo", "não letal", "apresentação"]
)

add_item(
    "arma-besta-de-mao", "Besta de Mão", "Armas", "Armas Simples", "Ataque à Distância / Uma Mão",
    "T$ 30", "1d6", "19", "Perfuração", "Curto", None, None, 1,
    book_hda, 218,
    "Uma besta compacta de uma mão favorita de espiões e assassinos. Pode ser disparada com apenas uma mão e ocultada facilmente (+2 em Ladinagem). Recarregar é uma ação de movimento.",
    ["besta compacta", "uma mão", "espião", "disparo"]
)

# Armas Marciais - Leves
add_item(
    "arma-adaga-oposta", "Adaga Oposta", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 12", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Uma adaga com lâmina curva invertida projetada para combate com duas armas. Quando você luta com duas armas e uma delas é a adaga oposta, recebe +1 na Defesa.",
    ["esgrima", "duas armas", "defesa +1", "acuidade"]
)

add_item(
    "arma-agulha-de-ahlen", "Agulha de Ahlen", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 10", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Uma lâmina extremamente fina e afiada sem gume cortante, feita para perfurar através de frestas e tecidos. É uma arma ágil e penetrante.",
    ["ahlen", "perfurante", "veneno", "ágil"]
)

add_item(
    "arma-cinquedea", "Cinquedea", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 18", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Uma adaga larga com lâmina triangular de cinco dedos de largura na base. Causa sangramento em acertos críticos.",
    ["adaga larga", "sangramento", "nobreza"]
)

add_item(
    "arma-dirk", "Dirk", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 15", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Adaga de lâmina reta e rígida de oficiais navais e marinheiros de Portsmouth.",
    ["marinheiro", "naval", "combate fechado"]
)

# Armas Marciais - Uma Mão
add_item(
    "arma-espada-larga", "Espada Larga", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "2d4", "x2", "Corte", "-", None, None, 1,
    book_hda, 218,
    "Espada de lâmina pesada de dois gumes largos forjada para corte contundente contra armaduras.",
    ["espada pesada", "2d4", "corte"]
)

add_item(
    "arma-espadim", "Espadim", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 300", "1d8", "20", "Corte", "-", None, None, 1,
    book_hda, 218,
    "Espada cerimonial de aço purificado com detalhes dourados e cesto de proteção. Concede +1 em Iniciativa e Diplomacia.",
    ["cerimonial", "nobre", "iniciativa +1"]
)

add_item(
    "arma-maca-estrela", "Maça-Estrela", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 20", "2d4", "x2", "Impacto e Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Uma cabeça de ferro esférica repleta de espigões cônicos forjados. Causa dano simultâneo de impacto e perfuração.",
    ["espetos", "impacto e perfuração", "clérigo de guerra"]
)

add_item(
    "arma-serrilheira", "Serrilheira", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 25", "1d6", "19", "Corte", "-", None, None, 1,
    book_hda, 218,
    "Espada curta com dentes de serra na parte posterior da lâmina. Concede +2 em manobras para quebrar armas inimigas.",
    ["dentes de serra", "quebrar", "desarmar"]
)

# Armas Marciais - Duas Mãos
add_item(
    "arma-bico-de-corvo", "Bico de Corvo", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 15", "1d8", "x3", "Impacto/Perfuração", "-", None, None, 2,
    book_hda, 218,
    "Um martelo de cabo longo encimado por uma ponta recurvada em forma de bico afiado projetado para perfurar armaduras completas.",
    ["perfurar armadura", "crítico x3", "bico de corvo"]
)

add_item(
    "arma-espada-de-execucao", "Espada de Execução", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 75", "2d6", "18/x4", "Corte", "-", None, None, 2,
    book_hda, 218,
    "Uma enorme lâmina reta de ponta quadrada e peso massivo na ponta. Possui margem de ameaça 18 e multiplicador de crítico devastador x4.",
    ["carrasco", "18/x4", "decapitação", "devastadora"]
)

add_item(
    "arma-lanca-de-justa-hda", "Lança de Justa", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 3", "1d8", "x2", "Perfuração", "-", None, None, 2,
    book_hda, 218,
    "Uma lança reforçada para torneios de cavalaria e investidas montadas.",
    ["justa", "torneio", "cavalaria", "investida"]
)

add_item(
    "arma-malho", "Malho", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 8", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_hda, 218,
    "Um martelo pesado de madeira maciça e ferragens para estacar e golpear.",
    ["malho", "impacto", "duas mãos"]
)

add_item(
    "arma-martelo-longo", "Martelo Longo", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 12", "2d4", "x4", "Impacto/Perfuração", "-", None, None, 2,
    book_hda, 218,
    "Uma haste de duas mãos encimada por cabeça de martelo e ponta perfurante com crítico x4.",
    ["crítico x4", "haste", "impacto"]
)

add_item(
    "arma-tan-korak", "Tan-Korak", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 40", "1d8", "x2", "Impacto", "-", None, None, 2,
    book_hda, 218,
    "Arma tradicional dos trogs das profundezas formada por garras unidas a bastões duplos.",
    ["trog", "subterrâneo", "impacto"]
)

add_item(
    "arma-tai-tai", "Tai-Tai", "Armas", "Armas Marciais", "Ataque à Distância / Uma Mão",
    "T$ 60", "2d4", "x2", "Impacto", "Médio", None, None, 2,
    book_hda, 218,
    "Um propulsor mecânico táurico de arremesso que dispara esferas pesadas.",
    ["propulsor", "táurico", "disparo"]
)

add_item(
    "arma-arco-montado", "Arco Montado", "Armas", "Armas Marciais", "Ataque à Distância / Duas Mãos",
    "T$ 45", "1d6", "x3", "Perfuração", "Médio", None, None, 2,
    book_hda, 218,
    "Um arco recurvo curto reforçado desenhado para disparos em alta velocidade montado a cavalo.",
    ["arco", "montaria", "cavalaria", "disparo"]
)

add_item(
    "arma-besta-dupla", "Besta Dupla", "Armas", "Armas Marciais", "Ataque à Distância / Duas Mãos",
    "T$ 125", "1d8", "19", "Perfuração", "Médio", None, None, 2,
    book_hda, 218,
    "Besta com dois arcos paralelos e travas independentes permitindo disparar dois virotes antes de recarregar.",
    ["dois tiros", "besta", "disparo duplo"]
)

# Armas Exóticas (HDA)
add_item(
    "arma-kimbata", "Kimbata", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 12", "1d4", "18", "Corte", "-", None, None, 1,
    book_hda, 219,
    "Faca em formato de meia-lua com argola na empunhadura para giros rápidos. Arma ágil e surpreendente que permite usar Furtividade para o ataque contra alvos desprevenidos.",
    ["faca meia-lua", "furtividade no ataque", "ágil", "crítico 18"]
)

add_item(
    "arma-clava-grao", "Clava-Grão", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 90", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_hda, 219,
    "Clava de sementes e fibras endurecidas dos devotos de Allihanna que floresce ao acertar.",
    ["allihanna", "druida", "natureza"]
)

add_item(
    "arma-espada-canora", "Espada Canora", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 50", "1d6", "19", "Perfuração", "-", None, None, 1,
    book_hda, 219,
    "Espada com canais acústicos na lâmina que produzem notas musicais ao cortar o ar. Concede bônus em Atuação e reduz custo de magias de ilusão.",
    ["música", "bardo", "ilusão", "canção"]
)

add_item(
    "arma-espada-gadanho", "Espada-Gadanho", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 40", "1d6", "18", "Corte", "-", None, None, 1,
    book_hda, 219,
    "Lâmina curva agressiva inspirada em gadanhos camponeses com margem 18-20.",
    ["crítico 18", "curva", "corte"]
)

add_item(
    "arma-khopesh", "Khopesh", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 20", "1d8", "19/x3", "Corte", "-", None, None, 1,
    book_hda, 219,
    "Espada em foice dos impérios ancestrais de Zarkhass e Nardmyr. Margem 19 / Crítico x3.",
    ["ancestral", "zarkhass", "19/x3", "foice"]
)

add_item(
    "arma-lanca-de-falange", "Lança de Falange", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "x3", "Perfuração", "Curto", None, None, 1,
    book_hda, 219,
    "Lança tática que pode ser usada com uma mão juntamente com escudos pesados em formação de falange.",
    ["falange", "escudo pesado", "uma mão"]
)

add_item(
    "arma-machado-de-haste", "Machado de Haste", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 40", "1d8/1d10", "x3", "Corte", "-", None, None, 1,
    book_hda, 219,
    "Machado versátil com empunhadura extensível. Causa 1d8 com uma mão ou 1d10 com duas mãos.",
    ["versátil", "uma ou duas mãos", "crítico x3"]
)

add_item(
    "arma-rapieira", "Rapieira", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 50", "1d8", "18", "Perfuração", "-", None, None, 1,
    book_hda, 219,
    "Espada de estocada rápida e cesto rebuscado para duelistas nobres de Bielefeld. Margem 18.",
    ["duelista", "esgrima", "crítico 18", "acuidade"]
)

add_item(
    "arma-marrao", "Marrão", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "4d4", "x2", "Impacto", "-", None, None, 2,
    book_hda, 219,
    "Marreta colossal de demolição com 4d4 de dano maciço.",
    ["4d4", "marreta", "demolição"]
)

add_item(
    "arma-montante-cinetico", "Montante Cinético", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 3.000", "2d6", "19/x4", "Corte", "-", None, None, 2,
    book_hda, 219,
    "Espada de duas mãos com mecanismo giroscópico interno que amplifica a inércia do golpe para crítico 19/x4.",
    ["cinético", "19/x4", "mecanismo", "tecnologia"]
)

add_item(
    "arma-boleadeira", "Boleadeira", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão",
    "T$ 12", "1d4", "x2", "Impacto", "Curto", None, None, 1,
    book_hda, 219,
    "Esferas de pedra unidas por tiras de couro. Derruba e enreda o alvo ao acertar.",
    ["derrubar", "arremesso", "tiras de couro"]
)

add_item(
    "arma-chakram", "Chakram", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão",
    "T$ 15", "1d6", "x3", "Corte", "Curto", None, None, 1,
    book_hda, 219,
    "Disco de metal com borda afiada que pode ser arremessado e recuperado por guerreiros treinados.",
    ["disco", "arremesso", "crítico x3"]
)

add_item(
    "arma-arco-de-guerra", "Arco de Guerra", "Armas", "Armas Exóticas", "Ataque à Distância / Duas Mãos",
    "T$ 200", "1d12", "x3", "Perfuração", "Médio", None, None, 2,
    book_hda, 219,
    "Arco composto pesadíssimo que exige Força 3 e dispara flechas devastadoras de 1d12.",
    ["1d12", "força 3", "disparo pesado"]
)

add_item(
    "arma-balestra", "Balestra", "Armas", "Armas Exóticas", "Ataque à Distância / Duas Mãos",
    "T$ 180", "1d12", "19", "Perfuração", "Médio", None, None, 2,
    book_hda, 219,
    "Besta pesada com guincho de tração mecânica e arco de aço reforçado causando 1d12.",
    ["balestra", "1d12", "guincho"]
)

add_item(
    "arma-besta-de-repeticao", "Besta de Repetição", "Armas", "Armas Exóticas", "Ataque à Distância / Duas Mãos",
    "T$ 250", "1d8", "19", "Perfuração", "Médio", None, None, 2,
    book_hda, 219,
    "Besta com carregador superior para 5 virotes que recarrega com o movimento da alavanca.",
    ["repetição", "5 tiros", "alavanca rápida"]
)

# Armas de Fogo (HDA)
add_item(
    "arma-garrucha", "Garrucha", "Armas", "Armas de Fogo", "Ataque à Distância / Leve",
    "T$ 250", "2d4", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_hda, 219,
    "Esta pequena arma de fogo, do tamanho de uma mão espalmada, pode ser facilmente escondida em uma manga ou nas dobras de uma veste. Uma garrucha é uma arma ocultável e surpreendente; recarregá-la é uma ação padrão.",
    ["garrucha", "ocultável", "pólvora", "2d4"]
)

add_item(
    "arma-canhao-portatil-hda", "Canhão Portátil", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos",
    "T$ 3.000", "4d10", "19/x3", "Impacto", "Curto", None, None, 2,
    book_hda, 219,
    "Uma versão menor dos canhões utilizados em embarcações, esta arma possui alças reforçadas e suporte para disparo individual. Exige Força 3 e causa 4d10 de impacto.",
    ["canhão", "artilharia", "4d10", "força 3"]
)

add_item(
    "arma-sifao-caustico-hda", "Sifão Cáustico", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos",
    "T$ 600", "4d6", "x2", "Ácido", "Especial", None, None, 2,
    book_hda, 219,
    "Um engenho mecânico acoplado a um reservatório que projeta jatos contínuos de ácido pressurizado causando 4d6 em cone de 4,5m.",
    ["ácido", "cone 4.5m", "pressurizado", "4d6"]
)

# --- 2.2) ARMADURAS & ESCUDOS (HDA, Tabela 3-3, pág 224, Descrições págs 223-226) ---
# Armaduras Leves (HDA - TODAS AS 5)
add_item(
    "armadura-sensual", "Armadura Sensual", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 55", None, None, None, None, 1, 0, 2,
    book_hda, 224,
    "Feita com tiras estratégicas de couro, seda e anéis de metal polido, esta armadura protege pouco, mas valoriza os atributos físicos do usuário. Se você não estiver usando nenhum outro vestuário além da armadura, recebe +2 em testes de Enganação e Diplomacia contra humanoides inteligentes.",
    ["sensual", "enganação +2", "diplomacia +2", "seda e couro", "defesa 1"]
)

add_item(
    "armadura-de-folhas", "Armadura de Folhas", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 75", None, None, None, None, 2, 0, 2,
    book_hda, 224,
    "Esta armadura é um traje de tecido leve sobre o qual são costuradas várias camadas de folhas especialmente preparadas com óleos naturais. É uma armadura leve que fornece pouca defesa, mas permite que o usuário se mantenha conectado com as forças da natureza. Se for treinado em Sobrevivência, você recebe +2 PM com esta armadura (somente após 1 dia de uso), cumulativo com outros efeitos de itens.",
    ["folhas", "druida", "natureza", "+2 pm", "defesa 2"]
)

add_item(
    "armadura-de-engenhoqueiro-goblin", "Armadura de Engenhoqueiro Goblin", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 85", None, None, None, None, 3, -2, 2,
    book_hda, 224,
    "Desenvolvida por artífices goblins, esta armadura é uma parafernália de bolsos, ganchos e coldres. Permite carregar até 2 espaços de itens guardados na armadura sem contar no limite normal de carga. Pode levar até mais 8 espaços dessa forma (total 10), mas sua penalidade aumenta em -1 para cada espaço extra (até -10). Não aplica sua penalidade em testes para ativar engenhocas.",
    ["goblin", "inventor", "engenhocas", "bolsos extras", "defesa 3"]
)

add_item(
    "armadura-cota-de-moedas", "Cota de Moedas", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 350", None, None, None, None, 4, -3, 2,
    book_hda, 224,
    "Uma armadura feita inteiramente de moedas de prata e ouro perfuradas e unidas por anéis de ferro. Além de sua defesa, ostenta riqueza inigualável, fornecendo +2 em testes de Diplomacia e Nobreza com membros da alta sociedade.",
    ["moedas", "ouro e prata", "nobreza +2", "diplomacia +2", "defesa 4"]
)

add_item(
    "armadura-colete-fora-da-lei", "Colete Fora da Lei", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 750", None, None, None, None, 5, -5, 2,
    book_hda, 224,
    "Este peitoral metálico único foi desenvolvido por uma quadrilha de Smokestone — um bando com muita criatividade e pouco caráter. A forma arredondada da armadura e as ranhuras em sua superfície redirecionam projéteis, tornando-a ideal para proteger o usuário contra balas e flechas. Contra armas de disparo, o bônus na Defesa de um colete fora da lei aumenta em +2.",
    ["smokestone", "tiro", "+2 defesa contra disparo", "defesa 5"]
)

# Armaduras Pesadas (HDA - TODAS AS 5)
add_item(
    "armadura-brigantina", "Brigantina", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 75", None, None, None, None, 6, 0, 5,
    book_hda, 224,
    "Uma túnica de lona ou couro grosso forrada internamente com placas de aço rebitadas. Por distribuir o peso perfeitamente sobre o tronco, não impõe penalidade de armadura inicial (Penalidade 0), sendo a mais confortável das armaduras pesadas de infantaria.",
    ["brigantina", "penalidade zero", "confortável", "defesa 6"]
)

add_item(
    "armadura-de-chumbo", "Armadura de Chumbo", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 750", None, None, None, None, 7, -5, 5,
    book_hda, 224,
    "Pesada e espessa, esta armadura possui placas forjadas com camadas de chumbo maciço. Fornece Defesa +7 e concede Resistência a Eletricidade e Necromancia 10, além de proteger o usuário contra efeitos de detecção mágica de auras.",
    ["chumbo", "res eletricidade 10", "antimagia", "defesa 7"]
)

add_item(
    "armadura-de-justa", "Armadura de Justa", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 1.200", None, None, None, None, 9, -5, 5,
    book_hda, 224,
    "Uma armadura completa com placas reforçadas no lado esquerdo do tronco e elmo fixo desenvolvida para torneios de cavalaria. Quando você está montado, fornece +2 na Defesa adicional contra ataques frontais e investidas.",
    ["justa", "torneio", "cavalaria", "+2 defesa montado", "defesa 9"]
)

add_item(
    "armadura-de-hussardo-alado", "Armadura de Hussardo Alado", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 4.500", None, None, None, None, 10, -6, 5,
    book_hda, 224,
    "Uma armadura completa com duas hastes longas curvas nas costas cobertas de penas, simulando asas. Quando você avança a galope numa investida montada, o vento produz um sibilo aterrador: você pode fazer um teste de Intimidação como ação livre para abalar todos os inimigos a até 9m.",
    ["hussardo", "asas", "investida", "intimidação em área", "defesa 10"]
)

add_item(
    "armadura-de-pedra", "Armadura de Pedra", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 5.500", None, None, None, None, 12, -5, 5,
    book_hda, 224,
    "Esta armadura completa monumental foi projetada por facções tradicionalistas da Guilda dos Armeiros de Doherimm com placas de granito anão polido e articulações reforçadas. Fornece Defesa +12, RD 2 contra fogo e ácido, e Redução de Dano físico 5.",
    ["granito", "anão", "doherimm", "rd 5", "defesa 12"]
)

# Escudos (HDA - TODOS OS 4)
add_item(
    "armadura-broquel", "Broquel", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 25", None, None, None, None, 0, -1, 0.5,
    book_hda, 224,
    "Um pequeno escudo de metal convexo de cerca de 30cm empunhado pela borda com a mão secundária. Não concede defesa passiva permanente, mas permite usar uma reação para desviar um ataque corpo a corpo desferido contra você, recebendo +2 na Defesa contra aquele ataque.",
    ["parry", "aparar", "esgrima", "reação"]
)

add_item(
    "armadura-escudo-de-vime", "Escudo de Vime", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 15", None, None, None, None, 2, -2, 2,
    book_hda, 224,
    "Este escudo é grande e desajeitado, mas extremamente leve devido a seu material. A trama aberta de vime confunde os inimigos e fornece camuflagem leve ao usuário e a um aliado adjacente escolhido no seu turno.",
    ["vime", "camuflagem", "proteção aliada", "defesa 2"]
)

add_item(
    "armadura-escudo-torre", "Escudo Torre", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 45", None, None, None, None, 2, -4, 2,
    book_hda, 224,
    "Um escudo retangular gigantesco de madeira reforçado com aço e couro. Você pode gastar uma ação de movimento para fixá-lo no chão, transformando-o em uma barreira que fornece cobertura leve.",
    ["cobertura", "muralha", "fixar no chão", "defesa 2"]
)

add_item(
    "armadura-sagna", "Sagna", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 20", None, None, None, None, 2, -3, 2,
    book_hda, 224,
    "Desenvolvido por devotos de Oceano, este grande escudo de madeira curva pode ser usado para deslizar pelas ondas em superfícies aquáticas. Anula penalidades de natação e aumenta o deslocamento de natação em +3m.",
    ["oceano", "mar", "natação +3m", "prancha de surf", "defesa 2"]
)

# --- 2.3) ITENS GERAIS (HDA, Tabela 3-4, págs 228-229) ---
add_item(
    "item-abaco", "Ábaco", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 45", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Instrumento sar-allan para cálculos rápidos. Permite obter Tibares de Ouro (TO) em testes de Ofício para sustento e aumenta o limite de Poder Monetário em +2.",
    ["sar-allan", "ouro", "cálculo", "comércio"]
)

add_item(
    "item-ampulheta", "Ampulheta", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 45", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Mede ciclos de uma hora. Ao escolher 10 em testes de Ofício (alquimista), considera o resultado do d20 como um 12 automático.",
    ["alquimia", "tempo", "escolher 10 vira 12"]
)

add_item(
    "item-asas-do-texugo", "Asas do Texugo", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 200", None, None, None, None, None, None, 2,
    book_hda, 227,
    "Mochila com asas retráteis de kobold e manivelas. Com um salto de Atletismo (CD 15), concede deslocamento de voo 12m por 1 ou mais rodadas.",
    ["voo 12m", "kobold", "asas", "engenhoqueiro"]
)

add_item(
    "item-astrolabio", "Astrolábio", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 90", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Instrumento de navegação estelar. Permite usar Conhecimento no lugar de Sobrevivência para orientar-se.",
    ["navegação", "estrelas", "conhecimento"]
)

add_item(
    "item-bainha-adornada", "Bainha Adornada", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 100", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Coberta de fios de ouro e gemas, permite portar armas em bailes e festas da corte sem chamar atenção.",
    ["corte", "ouro", "disfarce armado"]
)

add_item(
    "item-bussola", "Bússola", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 45", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Instrumento magnético com agulha imantada. Ao fazer testes de Sobrevivência para orientar-se, rola dois dados e usa o melhor.",
    ["ímã", "norte", "sobrevivência vantagem"]
)

add_item(
    "item-cinto-de-utilidades", "Cinto de Utilidades", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Cinturão de couro com presilhas especiais. Permite sacar e guardar engenhocas de inventor como uma ação livre.",
    ["inventor", "engenhocas", "ação livre sacar"]
)

add_item(
    "item-dente-falso", "Dente Falso", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 300", None, None, None, None, None, None, 0,
    book_hda, 227,
    "Frasco minúsculo disfarçado na boca contendo uma poção ou elixir que pode ser ingerido como ação de movimento ao quebrar o dente.",
    ["poção secreta", "ação de movimento", "espião"]
)

# Capangas & Veículos (HDA, págs 240-244)
add_item(
    "capanga-guarda-costas", "Guarda-Costas", "Capangas", "Capangas", "Seguidor / Proteção",
    "T$ 50/mês", None, None, None, None, None, None, 0,
    book_hda, 240,
    "Um mercenário veterano contratado para interpor seu escudo em sua defesa. Uma vez por rodada, concede +2 na Defesa contra um ataque direcionado a você.",
    ["mercenário", "defesa +2", "aliado", "contrato"]
)

add_item(
    "capanga-batedor", "Batedor", "Capangas", "Capangas", "Seguidor / Exploração",
    "T$ 40/mês", None, None, None, None, None, None, 0,
    book_hda, 240,
    "Um rastreador experiente contratado para explorar passagens secretas e detectar emboscadas com antecedência. Fornece +2 em Percepção e Sobrevivência do grupo.",
    ["rastreador", "percepção +2", "explorador"]
)

add_item(
    "veiculo-carruagem-blindada", "Veículos", "Veículos", "Veículos", "Veículo Terrestre",
    "T$ 500", None, None, None, None, None, None, 10,
    book_hda, 241,
    "Uma carruagem pesada reforçada com placas de metal nas laterais e seteiras para disparo seguro de bestas e armas de fogo.",
    ["transporte", "blindagem", "cavalos", "cobertura"]
)

add_item(
    "veiculo-balao-goblin", "Veículos", "Veículos", "Veículos", "Veículo Aéreo",
    "T$ 1.000", None, None, None, None, None, None, 20,
    book_hda, 242,
    "Um balão de ar quente sustentado por um cesto de vime reforçado com caldeira de óleo pressurizado. Permite sobrevoar terrenos intransponíveis a 12m de altitude.",
    ["vôo", "goblin", "aéreo", "ar quente"]
)

# =========================================================================================
# 3. LIVRO: AMEAÇAS DE ARTON (v1.0 - Bazar Monstruoso)
# =========================================================================================

# --- 3.1) NOVAS ARMAS (Ameaças, Tabela 3-1, pág 394, Descrições págs 392-395) ---
# Armas Simples - Corpo a Corpo - Leve
add_item(
    "arma-porrete", "Porrete", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 2", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_ameacas, 394,
    "Pedaço pesado de madeira maciça ou osso bruto com empunhadura entalhada. Uma arma rústica e barata, comum entre tribos e bandidos.",
    ["simples", "leve", "madeira", "porrete", "bazar monstruoso"]
)

# Armas Simples - Ataque à Distância - Uma Mão
add_item(
    "arma-zarabatana", "Zarabatana", "Armas", "Armas Simples", "Ataque à Distância / Uma Mão",
    "T$ 5", "1d3", "x2", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Pequeno tubo oco usado para disparar dardos. Causa dano mínimo, mas é excelente para inocular venenos; a CD para resistir ao veneno dos dardos aumenta em +2. Um pacote de munição contém 20 dardos, custa T$ 2 e ocupa 0,5 espaço.",
    ["zarabatana", "veneno +2 cd", "dardos", "silenciosa"]
)

# Armas Marciais - Corpo a Corpo - Leve
add_item(
    "arma-neko-te", "Neko-te", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 10", "1d4", "19", "Corte", "-", None, None, 1,
    book_ameacas, 394,
    "Luva com garras metálicas afiadas nas pontas dos dedos, desenvolvida em Tamu-ra para assassinato furtivo. Conta como arma ágil. Se você tiver a habilidade Ataque Furtivo, o dado extra de dano aumenta em +1d6.",
    ["tamu-ra", "garras", "ninja", "ataque furtivo +1d6", "ágil"]
)

# Armas Marciais - Corpo a Corpo - Uma Mão
add_item(
    "arma-gladio", "Gládio", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d6", "19/x3", "Perfuração", "-", None, None, 1,
    book_ameacas, 394,
    "Espada curta de lâmina reta e ponta aguçada com gume duplo reforçado, tradicional entre legiões e infantaria pesada. Muito eficaz para estocadas em formação de escudo cerrado.",
    ["gládio", "legião", "estocada", "crítico 19/x3", "uma mão"]
)

# Armas Marciais - Corpo a Corpo - Duas Mãos
add_item(
    "arma-tetsubo", "Tetsubo", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_ameacas, 394,
    "Uma versão mais pesada e sofisticada do tacape, geralmente reforçado com anéis e cravos metálicos. Ao realizar manobras derrubar ou quebrar com um tetsubo, você recebe +2 no teste de manobra.",
    ["tetsubo", "duas mãos", "impacto", "manobra derrubar +2", "quebrar +2"]
)

# Armas de Fogo - Ataque à Distância - Leve
add_item(
    "arma-traque", "Traque", "Armas", "Armas de Fogo", "Ataque à Distância / Leve",
    "T$ 75", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Uma pistola rústica e curta feita com cano reforçado improvisado por armeiros goblins. Quando rola um 1 natural no ataque, ela é avariada. Recarregá-la é uma ação padrão.",
    ["fogo", "leve", "goblin", "curto alcance", "crítico 19/x3"]
)

# Armas de Fogo - Ataque à Distância - Duas Mãos
add_item(
    "arma-arcabuz", "Arcabuz", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos",
    "T$ 800", "2d10", "19/x3", "Perfuração", "Médio", None, None, 2,
    book_ameacas, 394,
    "Versão mais pesada e mais potente do mosquete. Por seu peso e recuo, é uma arma formidável que causa grande estrago em disparos a média distância. Recarregá-la é uma ação padrão (ou de movimento com Saque Rápido).",
    ["arcabuz", "fogo", "duas mãos", "2d10", "médio alcance"]
)

add_item(
    "arma-bacamarte", "Bacamarte", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos",
    "T$ 450", "4d6", "19/x3", "Perfuração", "Especial", None, None, 2,
    book_ameacas, 394,
    "Esta arma de fogo tem boca larga, capaz de espalhar a munição como um cone de estilhaços. Ao disparar, atinge todas as criaturas em um cone de 4,5m (Reflexos CD Des reduz à metade).",
    ["bacamarte", "fogo", "cone 4.5m", "área", "estilhaços"]
)

# Armas Exóticas - Corpo a Corpo - Uma Mão
add_item(
    "arma-acoite-finntroll", "Açoite Finntroll", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d8", "x2", "Corte", "-", None, None, 1,
    book_ameacas, 394,
    "Feito de tiras de couro com farpas de aço e espinhos venenosos nas pontas, é também um instrumento de tortura. Fornece +2 em testes de Intimidação e manobras desarmar.",
    ["finntroll", "chicote", "farpas", "intimidação +2", "desarmar +2"]
)

add_item(
    "arma-espada-vespa", "Espada Vespa", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 75", "2d4", "18", "Corte ou Perfuração", "-", None, None, 1,
    book_ameacas, 394,
    "Esta arma estranha é feita com três ferrões de vespas gigantes presos a uma empunhadura articulada. Ao acertar um ataque com a espada vespa, você pode gastar 1 PM para deixar o alvo sangrando.",
    ["vespa gigante", "ferrões", "sangramento", "crítico 18"]
)

add_item(
    "arma-pistola-punhal", "Pistola-Punhal", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 300", "1d4 / 2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Esta arma é formada por uma lâmina pontiaguda com um mecanismo acoplado que permite disparar uma bala de arma de fogo. É uma arma híbrida: pode ser usada para ataques corpo a corpo (1d4, 19) ou disparos à distância (2d6, 19/x3, alcance curto).",
    ["híbrida", "pistola", "punhal", "fogo e lâmina"]
)

add_item(
    "arma-mordida-do-diabo", "Mordida do Diabo", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d4", "x2", "Perfuração", "-", None, None, 1,
    book_ameacas, 394,
    "Garra mecânica dentada inspirada em armadilhas para ursos. Quando acerta um ataque, você pode iniciar uma manobra agarrar como ação livre com +2 no teste.",
    ["armadilha", "dentes", "agarrar livre", "manobra +2"]
)

add_item(
    "arma-presa-de-serpente", "Presa de Serpente", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 1.000", "1d8", "17", "Corte", "-", None, None, 1,
    book_ameacas, 394,
    "Lâmina esguia e ondulada forjada em cerâmica verde ou presa de naga fossilizada. Possui uma margem de ameaça formidável (crítico 17-20).",
    ["naga", "ondulada", "crítico 17", "afiada"]
)

# Armas Exóticas - Corpo a Corpo - Duas Mãos
add_item(
    "arma-lanca-de-fogo", "Lança de Fogo", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 1.000", "1d8 / 4d6", "x3 / 19/x3", "Perfuração", "Especial", None, None, 2,
    book_ameacas, 394,
    "Esta arma é formada por um longo cano com uma coronha de madeira e uma ponta de lança metálica. Arma híbrida: funciona como lança corpo a corpo (1d8, x3) ou bacamarte de disparo em cone (4d6 de fogo/perfuração).",
    ["lança de fogo", "híbrida", "cone de fogo", "duas mãos"]
)

# Armas Exóticas - Ataque à Distância - Leve
add_item(
    "arma-shuriken", "Shuriken", "Armas", "Armas Exóticas", "Ataque à Distância / Leve",
    "T$ 1", "1d4", "x2", "Perfuração", "Curto", None, None, 0.5,
    book_ameacas, 394,
    "Pequenos projéteis metálicos para arremesso, em forma de estrelas ou dardos. Uma vez por rodada, quando ataca com uma shuriken, você pode gastar 1 PM para fazer um ataque adicional de shuriken contra o mesmo alvo.",
    ["shuriken", "arremesso", "ninja", "ataque extra", "leve"]
)

# Armas Exóticas - Ataque à Distância - Uma Mão
add_item(
    "arma-arpao", "Arpão", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão",
    "T$ 30", "1d10", "x3", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Instrumento de pesca costeira convertido em arma militar, esta haste tem farpas na extremidade e vem presa a uma corda de 10m. Se acertar o ataque, você pode puxar o alvo ou prendê-lo.",
    ["arpão", "pesca", "corda", "puxar", "farpas"]
)

# --- 3.2) ARMADURAS & ESCUDOS (Ameaças, Tabela 3-2, pág 395) ---
add_item(
    "armadura-de-ossos", "Armadura de Ossos", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 120", None, None, None, None, 3, -2, 2,
    book_ameacas, 395,
    "Os nezumi e outros povos são conhecidos por produzir estas armaduras sinistras. Combinando um aspecto assustador e energias negativas de ossadas, esta armadura fornece +1 em Intimidação e na CD de seus efeitos de medo (cumulativo com a melhoria macabra).",
    ["nezumi", "ossos", "intimidação +1", "medo cd +1", "defesa 3"]
)

add_item(
    "armadura-veste-de-teia-de-aranha", "Veste de Teia de Aranha", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 3.000", None, None, None, None, 4, 0, 2,
    book_ameacas, 395,
    "Feita com teia de aranha gigante, esta veste é cinza-escura, maleável e silenciosa, mas também forte como aço. Fornece +5 em Furtividade, mas não pode receber a melhoria material especial.",
    ["teia gigante", "furtividade +5", "penalidade zero", "defesa 4"]
)

add_item(
    "armadura-de-quitina", "Armadura de Quitina", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 350", None, None, None, None, 7, -3, 5,
    book_ameacas, 395,
    "Feita com carapaças selecionadas de grandes insetos, esta armadura dos povos-trovão é mais leve que suas contrapartes metálicas. Embora seja uma armadura pesada, não reduz o deslocamento do usuário.",
    ["quitina", "povo-trovão", "deslocamento normal", "defesa 7"]
)

add_item(
    "armadura-escudo-de-couro", "Escudo de Couro", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 3", None, None, None, None, 1, -1, 1,
    book_ameacas, 395,
    "Por sua leveza, este escudo é popular entre velocis e ubaneri. É feito com uma armação de madeira esticando uma membrana de couro flexível e amarrado ao braço. Contra ataques à distância, o bônus na Defesa do escudo aumenta em +2.",
    ["couro", "velocis", "defesa contra disparo +2", "defesa 1"]
)

# --- 3.3) NOVOS ITENS GERAIS (Ameaças, Tabela 3-3, pág 398, Descrições págs 396-399) ---
# Alimentação
add_item(
    "item-algravia", "Algravia", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 3", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Bebida alcoólica adocicada feita da seiva de feras-cactos. Você recebe +1 em testes de Fortitude e em rolagens de dano desarmado até o fim do dia.",
    ["cacto", "bebida", "fortitude +1", "desarmado +1"]
)

add_item(
    "item-banquete-de-canceronte", "Banquete de Canceronte", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 36", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Um canceronte adulto é suficiente para produzir um pequeno banquete para até seis pessoas. Aqueles que participam recebem RD 2 contra todos os tipos de dano durante as próximas 24 horas.",
    ["banquete", "canceronte", "rd 2", "6 pessoas"]
)

add_item(
    "item-coc-au-triz", "Coc-au-Triz", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 54", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Ovos de cocatriz são ingredientes mágicos poderosos, e esta guloseima reflete esse poder: é um ninho de fios de ovos assados e gratinados. Ao consumir, escolha uma habilidade com custo em PM. Seu custo diminui em -1 PM até a próxima refeição.",
    ["cocatriz", "pm -1", "guloseima mágica"]
)

add_item(
    "item-cozido-de-serpe", "Cozido de Serpe", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 12", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Quando cozida por várias horas em uma sopa específica, a carne da serpe fica livre de seu veneno natural e concede +1 em todos os testes de perícia por um dia inteiro.",
    ["serpe", "perícias +1", "sopa", "cozinha"]
)

add_item(
    "item-gorlogg-ensopado", "Gorlogg Ensopado", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 6", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Criado nas cozinhas de Yuvalin pela chef élfica Rizzelena, este ensopado nutritivo aumenta sua recuperação natural de PV e PM em +1 por nível em sua próxima noite de sono.",
    ["yuvalin", "recuperação pv pm", "ensopado"]
)

add_item(
    "item-omelete-monstruosa", "Omelete Monstruosa", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 3", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Feita com ovos de qualquer praga monstruosa ou corcel de Kally. Você recebe +2 em rolagens de dano físico e -2 em testes de perícias baseadas em Sabedoria por um dia.",
    ["omelete", "monstro", "dano +2", "ferocidade"]
)

add_item(
    "item-sashimi-de-kraken", "Sashimi de Kraken", "Itens Gerais", "Alimentação", "Alimentação",
    "T$ 60", None, None, None, None, None, None, 0,
    book_ameacas, 398,
    "Iguaria exótica criada pelos maiores mestres de Tamu-ra. Você recebe +2 em Diplomacia e ganha 5 PM temporários por 24 horas.",
    ["tamu-ra", "kraken", "diplomacia +2", "5 pm temporários"]
)

# Animais & Montarias (pág 399)
add_item(
    "animal-bulette", "Bulette", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 500", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Fera encouraçada escavadora da Grande Savana e Deserto da Perdição. Pode ser usada como parceiro montaria iniciante.",
    ["montaria", "bulette", "escavação", "parceiro"]
)

add_item(
    "animal-capivara", "Capivara", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 60", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Simpática, amistosa e dotada de fortes dentes, muito apreciada por ginetes Pequenos (hynne e goblins) como parceiro montaria.",
    ["capivara", "hynne", "goblin", "montaria pequena"]
)

add_item(
    "animal-corcel-do-deserto", "Corcel do Deserto", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 150", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Cavalo insetoide ágil adaptado a suportar o calor e as areias escaldantes do Deserto da Perdição. Parceiro montaria.",
    ["deserto", "insetoide", "montaria", "velocidade"]
)

add_item(
    "animal-dromedario", "Dromedário", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 75", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Animal de carga e transporte resiliente a longas viagens sem água no ermo. Parceiro montaria.",
    ["dromedário", "deserto", "carga", "montaria"]
)

add_item(
    "animal-elefante", "Elefante", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 1.500", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Gigantesco quadrúpede dotado de presas e tromba, empregado em áreas abertas e guerra como montaria pesada e besta de tração.",
    ["elefante", "colossal", "tração", "guerra"]
)

add_item(
    "animal-hiena", "Hiena", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 220", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Predador do ermo que pode ser usado como parceiro especial por personagens treinados em Adestramento, ou montaria para personagens Pequenos.",
    ["hiena", "adestramento", "parceiro especial", "montaria"]
)

add_item(
    "animal-leao", "Leão", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 800", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Símbolo de nobreza, ferocidade e liderança na Grande Savana. Pode ser treinado para ser usado como parceiro montaria de combate.",
    ["leão", "savana", "combate", "montaria"]
)

add_item(
    "animal-rinoceronte", "Rinoceronte", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 600", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Animal blindado dotado de chifre maciço, excelente para atropelar inimigos em investida como parceiro montaria.",
    ["rinoceronte", "chifre", "investida", "montaria"]
)

add_item(
    "animal-urso-pardo", "Urso Pardo", "Itens Gerais", "Animais", "Animais & Montarias",
    "T$ 300", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Grande predador das florestas do norte de Arton, resistente e leal quando adestrado como parceiro montaria.",
    ["urso", "floresta", "força", "montaria"]
)

# Equipamento de Aventura
add_item(
    "item-caixa-de-voz", "Caixa de Voz", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Este complexo mecanismo purista tem 1d4 cargas: ao usar uma habilidade de bardo ou nobre de alcance curto ou médio, gasta 1 carga para aumentar o alcance em um passo.",
    ["bardo", "nobre", "alcance ampliado", "supremacia"]
)

add_item(
    "item-corda-de-teia", "Corda de Teia", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 100", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Corda de 10m tecida a partir de teia de aranha gigante. Extremamente resistente, arrebentá-la exige 5 pontos de dano de corte ou teste de Força CD 28.",
    ["corda", "teia de aranha", "cd 28 força"]
)

add_item(
    "item-dente-de-wisphago", "Dente de Wisphago", "Itens Gerais", "Equipamento de Aventura", "Equipamento de Aventura",
    "T$ 100", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Usado como amuleto. Quando faz um teste de resistência contra uma magia arcana, você pode gastar o amuleto para rolar novamente com bônus de +2.",
    ["wisphago", "amuleto", "resistência magia arcana +2"]
)

# Esotéricos
add_item(
    "item-ankh-solar", "Ankh Solar", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 450", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Símbolo sagrado de Azgher esculpido em ouro polido. Suas magias de luz e fogo causam +1 ponto de dano por dado e a CD para resistir aumenta em +1.",
    ["esotérico", "azgher", "luz", "fogo", "cd +1"]
)

add_item(
    "item-tomo-de-guerra", "Tomo de Guerra", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 300", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Quando lança uma magia de evocação, você recebe +1 PM temporário para gastar exclusivamente em aprimoramentos dessa magia.",
    ["esotérico", "tomo", "evocação", "+1 pm aprimoramento"]
)

add_item(
    "item-tomo-do-rancor", "Tomo do Rancor", "Itens Gerais", "Esotéricos", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Suas magias de dano recebem o aprimoramento especial (+2 PM): além do dano normal, deixam o alvo debilitado por 1 rodada caso falhe na resistência.",
    ["esotérico", "tomo", "rancor", "debilitado"]
)

# Alquímicos - Preparados
add_item(
    "item-balsamo-de-drogadora", "Bálsamo de Drogadora", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 60", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Produzido por curandeiras dos povos-trovão, este unguento aplicado como ação padrão restaura 3d6+3 pontos de vida e remove a condição sangrando.",
    ["cura 3d6+3", "sangrando", "povo-trovão", "preparado"]
)

add_item(
    "item-bomba-de-fumaca", "Bomba de Fumaça", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 15", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Saco de estopa com pólvora especial. Ao ser arremessado em alcance curto, cria uma nuvem de fumaça espessa de 3m de raio que concede camuflagem total por 2 rodadas.",
    ["fumaça", "camuflagem total", "arremesso", "ninja"]
)

add_item(
    "item-elixir-quimerico", "Elixir Quimérico", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 120", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Beber este elixir é uma ação padrão; até o fim da cena você ganha uma arma natural de mordida (1d6 corte) ou chifres (1d6 perfuração).",
    ["mutação", "arma natural", "quimera", "elixir"]
)

add_item(
    "item-eter-elemental", "Éter Elemental", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 60", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Frasco com essência pura dos planos elementais. Ao ser aplicado em uma arma como ação de movimento, adiciona +1d6 de dano de fogo, frio, eletricidade ou ácido por 3 rodadas.",
    ["elemental", "dano extra 1d6", "óleo de arma"]
)

add_item(
    "item-isca-putrefata", "Isca Putrefata", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 60", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Solução fétida que atrai monstros e mortos-vivos num raio de 100m ou impõe -2 em testes de Percepção contra alvos ungidos com o odor.",
    ["isca", "monstros", "odor", "distração"]
)

add_item(
    "item-lagrima-petrea", "Lágrima Pétrea", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 30", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Líquido cristalino com o poder de anular a condição petrificado ou conceder RD 5 contra petrificação por 1 hora.",
    ["petrificação", "cura", "resistência"]
)

add_item(
    "item-oleo-de-baleia", "Óleo de Baleia", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 30", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Óleo denso e inflamável que queima debaixo d'água e em tempestades, fornecendo iluminação contínua por até 12 horas.",
    ["submerso", "luz", "iluminação", "óleo"]
)

add_item(
    "item-oleo-de-besouro", "Óleo de Besouro", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 50", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "O líquido inflamável do besouro-do-óleo dobra a área iluminada por tochas e lampiões ou pode ser arremessado para causar 2d6 de fogo.",
    ["besouro", "fogo 2d6", "iluminação dobrada"]
)

add_item(
    "item-po-azul", "Pó Azul", "Itens Gerais", "Alquímicos - Preparados", "Alquímicos - Preparados",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Extraído de plantas mágicas de Galrasia, ao ser soprado em um alvo adjacente impõe a condição inconsciente (Fortitude CD 18 evita).",
    ["galrasia", "sono", "inconsciente", "cd 18"]
)

# Alquímicos - Catalisadores
add_item(
    "item-corrosivo-mineral", "Corrosivo Mineral", "Itens Gerais", "Alquímicos - Catalisadores", "Alquímicos - Catalisadores",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Pasta mineral corrosiva natural. Ao lançar magias de ácido, adiciona +1 ponto de dano por dado e corrói 1 ponto de Defesa da armadura do alvo por 1 rodada.",
    ["catalisador", "ácido", "corrosão", "dano +1/dado"]
)

add_item(
    "item-gelo-extremo", "Gelo Extremo", "Itens Gerais", "Alquímicos - Catalisadores", "Alquímicos - Catalisadores",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Cristais que eliminam calor ambiente. Aumenta os dados de dano de frio de suas magias em um passo (de d6 para d8, etc.).",
    ["catalisador", "frio", "aumento de passo de dano"]
)

add_item(
    "item-pedaco-de-lingua", "Pedaço de Língua", "Itens Gerais", "Alquímicos - Catalisadores", "Alquímicos - Catalisadores",
    "T$ 30", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Glândula de sapo monstruoso usada como catalisador que concede +1 na CD para resistir a magias de encantamento ou veneno.",
    ["catalisador", "cd +1", "encantamento"]
)

add_item(
    "item-raio-cristalizado", "Raio Cristalizado", "Itens Gerais", "Alquímicos - Catalisadores", "Alquímicos - Catalisadores",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Eletricidade solidificada de elementais. Aumenta em +2 o dano por dado de suas magias de eletricidade.",
    ["catalisador", "eletricidade", "dano +2/dado"]
)

# Alquímicos - Venenos
add_item(
    "item-esporos-de-cogumelo", "Esporos de Cogumelo", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 75", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Inalado. O alvo sofre 1d6 de dano de veneno e fica confuso por 1d4 rodadas (Fortitude CD 15 reduz para 1 rodada).",
    ["veneno", "inalado", "confuso", "cd 15"]
)

add_item(
    "item-peconha-ancia", "Peçonha Anciã", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 1.800", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Veneno lendário extraído de serpes anciãs e hidras. Causa 4d12 de dano de veneno e deixa o alvo fraco e debilitado (Fortitude CD 25 reduz à metade).",
    ["veneno lendário", "4d12", "debilitado", "cd 25"]
)

add_item(
    "item-peconha-irritante", "Peçonha Irritante", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 10", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Veneno de contato brando. Causa 1d4 de dano de ácido e impõe -2 em testes de perícias físicas por 1 minuto (Fortitude CD 12 evita).",
    ["veneno leve", "irritante", "-2 perícias", "cd 12"]
)

add_item(
    "item-veneno-batraquio", "Veneno Batráquio", "Itens Gerais", "Alquímicos - Venenos", "Alquímicos - Venenos",
    "T$ 30", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Saliva viscosa de rãs tóxicas. Causa 1d8 de dano e deixa o alvo vulnerável por 1d4 rodadas (Fortitude CD 14 reduz para 1 rodada).",
    ["veneno", "vulnerável", "1d8 dano", "cd 14"]
)

# Vestuário
add_item(
    "item-garra-feroz", "Garra Feroz", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 60", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Pinças de insetos gigantes presas com couro, funcionam como manopla e seus benefícios também se aplicam a garras ou armas naturais sob efeito de Forma Selvagem.",
    ["vestuário", "druida", "forma selvagem", "manopla garra"]
)

add_item(
    "item-manto-do-mantor", "Manto do Mantor", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 450", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Manto de couro de mantor. Na escuridão completa fornece camuflagem total mesmo contra criaturas com visão no escuro.",
    ["manto", "mantor", "camuflagem total", "escuridão"]
)

add_item(
    "item-manto-pesado", "Manto Pesado", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Vestes pesadas com capuz largo que protegem contra tempestades de areia e calor extremo do deserto, concedendo +2 em testes de Sobrevivência.",
    ["manto", "deserto", "areia", "sobrevivência +2"]
)

add_item(
    "item-sombreiro", "Sombreiro", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Chapéu de abas largas tradicional de Smokestone. Concede +1 em testes de resistência contra efeitos de ofuscamento e calor.",
    ["sombreiro", "smokestone", "sol", "ofuscamento"]
)

add_item(
    "item-traje-selako", "Traje Selako", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 90", None, None, None, None, None, None, 1,
    book_ameacas, 396,
    "Traje impermeável de couro de selako. Concede +2 em testes de Atletismo para natação e deslocamento de natação igual ao deslocamento normal.",
    ["selako", "natação", "aquático", "atletismo +2"]
)

# --- 3.4) NOVAS MELHORIAS (Ameaças, pág 399) ---
add_item(
    "melhoria-multifuncional", "Multifuncional", "Itens Superiores", "Melhorias", "Melhoria de Equipamento",
    "Item Superior", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Esta melhoria só pode ser aplicada em um item que modifica uma perícia. Escolha outra perícia que usa o mesmo atributo-chave; o item passa a funcionar também para a segunda perícia.",
    ["melhoria", "perícias", "versatilidade", "bazar monstruoso"]
)

add_item(
    "melhoria-penetrante", "Penetrante", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "Item Superior", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "A arma ignora 5 pontos da redução de dano do alvo. Pré-requisito: cruel.",
    ["melhoria", "arma", "ignora rd 5", "penetrante", "cruel"]
)

# --- 3.5) NOVOS MATERIAIS ESPECIAIS (Ameaças, Tabela 3-4, pág 400, Descrições págs 399-401) ---
add_item(
    "material-casco-de-monstro", "Casco de Monstro", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 750 (Arma/Leve/Escudo) | +T$ 6.000 (Pesada/Esotérico)", None, None, None, None, 1, None, 0,
    book_ameacas, 400,
    "Os cascos protetores de monstros substituem aço. Arma: conta como primitiva para magias como Armamento da Natureza. Armadura/Escudo: penalidade diminui em 1 (armaduras pesadas permitem aplicar 1 ponto de Destreza na Defesa). Esotérico: concede RD 5 contra o próximo dano após lançar magia.",
    ["casco", "quelônio", "destreza armadura pesada", "penalidade -1", "rd 5"]
)

add_item(
    "material-couraca-de-kaiju", "Couraça de Kaiju", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "Raríssimo / Espólio Lendário", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Arma: dano aumenta em um passo; pode gastar 2 PM para ignorar efeitos que reduzem o dano (como Durão). Armadura/Escudo: armadura leve e escudo fornecem RD 10/mágico; armadura pesada fornece RD 20/mágico. Esotérico: pode gastar 2 PM para ignorar efeitos redutores como Evasão.",
    ["kaiju", "rd 10 mágico", "rd 20 mágico", "+1 passo dano", "ignora durão"]
)

add_item(
    "material-couro-de-bulette", "Couro de Bulette", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "Raro / Espólio", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Armadura leve: fornece deslocamento de escavação igual à metade do normal e redução de ácido 5. Armadura pesada: escavação e redução de ácido 10. Esotérico: pode rolar novamente qualquer resultado 1 no dano de magias de ácido.",
    ["bulette", "escavação", "redução ácido", "esotérico ácido"]
)

add_item(
    "material-cristal-de-sol", "Cristal de Sol", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "Raro / Espólio Neve", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Arma: causa +2 pontos de dano por fogo. Armadura/Escudo: rola dois dados e usa o melhor em testes contra efeitos de frio. Esotérico: ao lançar magia de fogo pode gastar 1 PM para colocar os alvos em chamas.",
    ["cristal de sol", "fogo +2", "resistência frio vantagem", "em chamas"]
)

add_item(
    "material-lanajuste", "Lanajuste", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 600 (Arma) | +T$ 1.500 (Leve/Escudo) | +T$ 3.000 (Pesada/Esotérico)", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Também chamado de coral-de-ferro de Khubar. Arma: ataques ignoram penalidades de combate submerso e não violam restrições de devotos do Oceano. Armadura/Escudo: fornece redução de corte 5 (leves/escudos) ou 10 (pesadas). Esotérico: rola novamente resultados 1 no dano de magias de corte.",
    ["coral de ferro", "khubar", "combate submerso", "oceano", "redução corte 5/10"]
)

add_item(
    "material-pena-de-kraken", "Pena de Kraken", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "Raro / Espólio Kraken", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Material vítreo da concha de um kraken. Arma: em acertos críticos, o dano aumenta dois passos. Armadura/Escudo: quando uma criatura erra um ataque corpo a corpo contra você, perde 5 PV (leve/escudo) ou 10 PV (pesada). Esotérico: se o item fornece bônus numérico, ele aumenta em +1.",
    ["kraken", "+2 passos dano crítico", "retaliação 5/10 pv", "bônus esotérico +1"]
)

add_item(
    "material-prata", "Prata", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "+T$ 600 (Arma) | +T$ 1.500 (Leve/Escudo) | +T$ 3.000 (Pesada) | +T$ 400 (Esotérico)", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Arma: causa +2 pontos de dano em espíritos e mortos-vivos e é considerada mágica contra eles. Armadura/Escudo: fornece RD 5 (leves/escudos) ou RD 10 (pesadas) contra dano de espíritos e mortos-vivos. Pode ser combinada com outro material especial.",
    ["prata", "mortos-vivos", "espíritos", "rd 5/10", "arma mágica"]
)

print(f"Total de equipamentos canônicos catalogados: {len(equipments)}")

with open("data/categories/equipamentos.json", "w", encoding="utf-8") as f:
    json.dump(equipments, f, ensure_ascii=False, indent=2)

print("data/categories/equipamentos.json gerado com sucesso!")

