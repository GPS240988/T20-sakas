import json
import os
import re
import pymupdf

os.makedirs("data/categories", exist_ok=True)

# Open docs
jda_doc = pymupdf.open("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf")
hda_doc = pymupdf.open("T20-Herois-de-Arton-v1-1_compressed.pdf")
ameacas_doc = pymupdf.open("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf")

equipments = []
id_set = set()

def create_item(
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

print("=== EXTRAINDO EQUIPAMENTOS COMPLETOS DOS 3 LIVROS ===")

book_jda = "Tormenta20 - Jogo do Ano (v1.3)"
book_hda = "Heróis de Arton (v1.1)"
book_ameacas = "Ameaças de Arton (v1.0)"

# =========================================================================
# 1. TORMENTA20: EDIÇÃO JOGO DO ANO (v1.3)
# =========================================================================

# --- 1.1 ARMAS (Tabela 3-3, p. 142-145; Descrições p. 146-151) ---
# Armas Simples Corpo a Corpo - Leves
create_item(
    "arma-adaga", "Adaga", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 2", "1d4", "19", "Perfuração", "Curto", None, None, 1,
    book_jda, 146,
    "Esta faca afiada é usada por muitos habitantes adultos do Reinado, embora seja favorita de ladrões e assassinos, por ser facilmente escondida (fornece +5 em testes de Ladinagem para ocultá-la). Quando ataca com uma adaga, você pode usar sua Destreza em vez de Força nos testes de ataque. Uma adaga pode ser arremessada.",
    ["faca", "acuidade", "arremesso", "ladinagem"]
)

create_item(
    "arma-ataque-desarmado", "Ataque Desarmado", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 0", "1d3", "x2", "Impacto", "-", None, None, 0,
    book_jda, 144,
    "Um soco, chute, cabeçada ou qualquer outro golpe desferido com o próprio corpo. Um ataque desarmado causa dano não letal. Um personagem treinado em Luta pode causar dano letal ou não letal sem penalidades. Você não pode aplicar melhorias ou encantos a ataques desarmados, a menos que esteja usando uma manopla.",
    ["soco", "chute", "não letal", "desarmado"]
)

create_item(
    "arma-espada-curta", "Espada Curta", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 10", "1d6", "19", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "O tipo mais comum de espada, usada por guardas ou como arma secundária de guerreiros.",
    ["espada", "leve", "guarda"]
)

create_item(
    "arma-foice", "Foice", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 4", "1d6", "x3", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Uma ferramenta agrícola com lâmina curva montada em um cabo de madeira curto. Causa dano crítico triplo.",
    ["agrícola", "crítico x3", "camponês"]
)

create_item(
    "arma-manopla", "Manopla", "Armas", "Armas Simples", "Corpo a Corpo / Leve",
    "T$ 5", "-", "-", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Uma luva de couro pesado recoberta de placas de metal. Permite que seus ataques desarmados causem dano letal e recebam melhorias e encantos de armas.",
    ["luva", "metal", "ataque desarmado", "letal"]
)

# Armas Simples Corpo a Corpo - Uma Mão
create_item(
    "arma-clava", "Clava", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 0", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_jda, 147,
    "Um pedaço de madeira empunhado como arma, geralmente usado por bárbaros ou criaturas brutais — ou como arma improvisada, como um galho de árvore ou pedaço de mobília. Sendo fácil de conseguir, seu preço é zero.",
    ["madeira", "porrete", "grátis", "improvisada"]
)

create_item(
    "arma-lanca", "Lança", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 2", "1d6", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 148,
    "Uma haste de madeira com uma ponta afiada de ferro ou pedra. Pode ser arremessada.",
    ["haste", "arremesso", "infantaria"]
)

create_item(
    "arma-maca", "Maça", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Um bastão de madeira ou metal com uma cabeça pesada e flangeada na ponta. Muito utilizada por clérigos que fazem votos de não derramar sangue cortando carne.",
    ["bastão", "impacto", "clérigo"]
)

create_item(
    "arma-martelo", "Martelo", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 1", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Um martelo comum de trabalho com cabo curto, capaz de desferir golpes contundentes em combate.",
    ["trabalho", "ferramenta", "impacto"]
)

# Armas Simples Corpo a Corpo - Duas Mãos
create_item(
    "arma-bordao", "Bordão", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d6/1d6", "x2", "Impacto", "-", None, None, 2,
    book_jda, 147,
    "Um cajado apreciado por viajantes e camponeses por sua praticidade e fácil acesso (seu preço é zero). O bordão é uma arma dupla.",
    ["cajado", "dupla", "grátis", "viajante"]
)

create_item(
    "arma-pique", "Pique", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 5", "1d8", "x2", "Perfuração", "-", None, None, 2,
    book_jda, 149,
    "Uma lança longa de infantaria medindo entre 3 e 4 metros. O pique é uma arma alongada.",
    ["haste longa", "alongada", "antagonista de investida"]
)

create_item(
    "arma-tacape", "Tacape", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_jda, 150,
    "Uma clava pesada de madeira maciça de duas mãos, frequentemente cravada de lascas de pedra ou ossos.",
    ["pesado", "madeira", "bárbaro", "duas mãos"]
)

# Armas Simples Ataque à Distância - Disparo
create_item(
    "arma-arco-curto", "Arco Curto", "Armas", "Armas Simples", "Ataque à Distância / Disparo",
    "T$ 30", "1d6", "x3", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Uma arma antiga e comum, este arco é usado primariamente como ferramenta de caça, embora seja usado como arma de guerra por milícias, bandidos e exércitos menos equipados. Pode ser usado montado.",
    ["arco", "disparo", "caça", "montaria"]
)

create_item(
    "arma-besta-leve", "Besta Leve", "Armas", "Armas Simples", "Ataque à Distância / Disparo",
    "T$ 35", "1d8", "19", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Um arco montado sobre uma coronha de madeira com um gatilho, a besta leve é uma arma que dispara virotes com grande potência. Recarregar uma besta leve é uma ação de movimento.",
    ["besta", "virote", "ação de movimento", "potência"]
)

create_item(
    "arma-funda", "Funda", "Armas", "Armas Simples", "Ataque à Distância / Disparo",
    "T$ 0", "1d4", "x2", "Impacto", "Médio", None, None, 1,
    book_jda, 147,
    "Uma tira de couro na qual se coloca uma pedra ou bala de chumbo. A funda é girada rapidamente e a pedra é arremessada pela força centrífuga. Você aplica sua Força às rolagens de dano da funda. Recarregar a funda é uma ação de movimento.",
    ["funda", "couro", "aplica força", "grátis"]
)

# Armas Simples Ataque à Distância - Arremesso
create_item(
    "arma-azagaia", "Azagaia", "Armas", "Armas Simples", "Ataque à Distância / Arremesso",
    "T$ 1", "1d6", "x2", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Uma lança leve e flexível, própria para arremesso. Pode ser usada como arma corpo a corpo, mas você sofre uma penalidade de -5 no teste de ataque.",
    ["lança leve", "arremesso"]
)

create_item(
    "arma-dardo", "Dardo", "Armas", "Armas Simples", "Ataque à Distância / Arremesso",
    "T$ 5", "1d4", "x2", "Perfuração", "Curto", None, None, 0.5,
    book_jda, 147,
    "Uma pequena flecha de madeira com ponta de metal e penas para estabilização, própria para ser arremessada com as mãos.",
    ["dardo", "arremesso", "leve"]
)

create_item(
    "arma-rede", "Rede", "Armas", "Armas Simples", "Ataque à Distância / Arremesso",
    "T$ 20", "-", "-", "-", "Curto", None, None, 1,
    book_jda, 149,
    "Uma rede de cordas reforçadas com chumbadas nas bordas. Ao acertar um ataque à distância com uma rede contra uma criatura de tamanho Grande ou menor, ela não sofre dano, mas fica enredada (fica vulnerável, sofre -2 em testes de ataque e -5m no deslocamento). A criatura pode se soltar gastando uma ação padrão e passando em um teste de Acrobacia ou Atletismo (CD 15) ou causando 5 pontos de dano cortante à rede.",
    ["enredar", "controle", "captura", "não letal"]
)

# Armas Marciais Corpo a Corpo - Leves
create_item(
    "arma-machado-de-ataque", "Machado de Ataque", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 10", "1d6", "x3", "Corte", "Curto", None, None, 1,
    book_jda, 148,
    "Um machado balanceado de uma mão que pode ser arremessado. É a arma padrão dos anões para combate leve ou à distância.",
    ["machado", "arremesso", "crítico x3", "anão"]
)

create_item(
    "arma-martelo-leve", "Martelo Leve", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 1", "1d6", "x2", "Impacto", "Curto", None, None, 1,
    book_jda, 148,
    "Um martelo balanceado com cabo de madeira e cabeça de ferro, próprio para ser usado em corpo a corpo ou arremessado.",
    ["martelo", "arremesso", "balanceado"]
)

# Armas Marciais Corpo a Corpo - Uma Mão
create_item(
    "arma-cimitarra", "Cimitarra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d6", "18", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Espada com a lâmina curva e muito afiada. A cimitarra é uma arma ágil (beneficia-se de Acuidade com Arma). Margem de ameaça 18-20.",
    ["espada curva", "ágil", "crítico 18", "acuidade"]
)

create_item(
    "arma-espada-longa", "Espada Longa", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "19", "Corte", "-", None, None, 1,
    book_jda, 147,
    "A mais tradicional das espadas, com lâmina reta de dois gumes de cerca de um metro. A arma emblemática dos nobres, cavaleiros e aventureiros de Arton.",
    ["espada", "tradição", "cavaleiro", "nobreza"]
)

create_item(
    "arma-florete", "Florete", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 20", "1d6", "18", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "Uma espada fina e flexível com cesto de proteção para a mão. O florete é uma arma ágil. Margem de ameaça 18-20.",
    ["esgrima", "ágil", "acuidade", "crítico 18"]
)

create_item(
    "arma-machado-de-batalha", "Machado de Batalha", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 10", "1d8", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "Um machado de lâmina larga e pesada montada em cabo curto. É uma arma tradicional dos anões.",
    ["machado", "crítico x3", "anão", "batalha"]
)

create_item(
    "arma-mangual", "Mangual", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Uma haste de madeira ligada por uma corrente a uma esfera de ferro com pontas. O mangual é uma arma versátil, fornecendo +2 em testes para desarmar.",
    ["corrente", "esfera", "versátil", "desarmar"]
)

create_item(
    "arma-martelo-de-guerra", "Martelo de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x3", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Um martelo com cabeça de aço pesada em uma das extremidades e uma ponta na outra. Causa dano crítico triplo.",
    ["martelo", "crítico x3", "guerra", "impacto"]
)

create_item(
    "arma-picareta", "Picareta", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d6", "x4", "Perfuração", "-", None, None, 1,
    book_jda, 149,
    "Uma ferramenta de mineração com ponta de aço curvada reforçada. Causa dano crítico quádruplo (x4).",
    ["mineração", "crítico x4", "perfuração"]
)

create_item(
    "arma-tridente", "Tridente", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 150,
    "Uma lança com três pontas de ferro. O tridente é uma arma versátil, fornecendo +2 em testes para desarmar. Pode ser arremessado.",
    ["três pontas", "versátil", "desarmar", "arremesso"]
)

# Armas Marciais Corpo a Corpo - Duas Mãos
create_item(
    "arma-alabarda", "Alabarda", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d10", "x3", "Corte/Perfuração", "-", None, None, 2,
    book_jda, 146,
    "Uma haste de madeira com 2m de comprimento e uma lâmina de machado com ponta de lança na extremidade. A alabarda é uma arma alongada.",
    ["haste", "alongada", "crítico x3", "guarda"]
)

create_item(
    "arma-alfange", "Alfange", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 75", "2d4", "18", "Corte", "-", None, None, 2,
    book_jda, 146,
    "Uma versão maior da cimitarra, esta espada de lâmina larga e curva é bastante usada por guerreiros do Deserto da Perdição. Margem de ameaça 18-20.",
    ["deserto", "espada curva", "crítico 18"]
)

create_item(
    "arma-foice-grande", "Gadanho", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 18", "2d4", "x4", "Corte", "-", None, None, 2,
    book_jda, 147,
    "Uma grande lâmina curva montada em uma haste de madeira de duas mãos, usada na colheita e temida no combate. Causa dano crítico quádruplo (x4).",
    ["gadanho", "morte", "crítico x4", "colheita"]
)

create_item(
    "arma-lanca-montada", "Lança Montada", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d8", "x3", "Perfuração", "-", None, None, 2,
    book_jda, 148,
    "Uma lança pesada com guarda para a mão, desenvolvida para cavalaria. Se você estiver montado, pode usar uma lança montada com apenas uma mão. Além disso, quando usada numa investida montada, causa +2d8 pontos de dano.",
    ["montada", "cavaleiro", "investida", "uma mão montado"]
)

create_item(
    "arma-machado-de-guerra", "Machado de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "1d12", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Um machado enorme de duas mãos, frequentemente com lâmina dupla, favorito de bárbaros e guerreiros brutais.",
    ["machado gigante", "bárbaro", "crítico x3", "1d12"]
)

create_item(
    "arma-montante", "Montante", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d6", "19", "Corte", "-", None, None, 2,
    book_jda, 150,
    "Enorme e pesada, esta espada de 1,5m de comprimento é uma arma poderosa que desfere golpes devastadores em arcos amplos.",
    ["espada gigante", "2d6", "duas mãos", "devastadora"]
)

# Armas Marciais Ataque à Distância - Disparo
create_item(
    "arma-arco-longo", "Arco Longo", "Armas", "Armas Marciais", "Ataque à Distância / Disparo",
    "T$ 100", "1d8", "x3", "Perfuração", "Longo", None, None, 2,
    book_jda, 146,
    "Este arco reforçado tem a altura de uma pessoa. Ao contrário da versão curta, é primariamente uma arma de guerra. Por ter uma puxada pesada, permite que você aplique sua Força às rolagens de dano (ao contrário de outras armas de disparo). Porém, um arco longo não pode ser usado se você estiver montado.",
    ["arco", "longo", "aplica força", "alcance longo", "guerra"]
)

create_item(
    "arma-besta-pesada", "Besta Pesada", "Armas", "Armas Marciais", "Ataque à Distância / Disparo",
    "T$ 50", "1d12", "19", "Perfuração", "Médio", None, None, 2,
    book_jda, 146,
    "Versão maior e mais potente da besta leve. Recarregar uma besta pesada é uma ação padrão.",
    ["besta pesada", "1d12", "ação padrão", "potência"]
)

# Armas Exóticas
create_item(
    "arma-adaga-de-aparar", "Adaga de Aparar", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 50", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_jda, 146,
    "Esta adaga possui uma guarda reforçada e alargada em cruz. Quando empunha esta adaga em uma das mãos, você recebe +1 na Defesa. É uma arma ágil.",
    ["defesa +1", "ágil", "esgrima", "guarda"]
)

create_item(
    "arma-chicote", "Chicote", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 2", "1d3", "x2", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Esta arma pode ser usada para atacar inimigos a até 4,5m e pode se enroscar nas mãos, pernas ou armas de seus adversários. O chicote é uma arma ágil e versátil, fornecendo +2 em testes para derrubar ou desarmar.",
    ["alcance 4.5m", "ágil", "versátil", "derrubar", "desarmar"]
)

create_item(
    "arma-espada-bastarda", "Espada Bastarda", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 35", "1d10/1d12", "19", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Mais longa e pesada que a espada longa, esta arma é balanceada para ser usada com uma mão (se você tiver proficiência com armas exóticas) ou com duas mãos (como uma arma marcial, causando 1d12 de dano).",
    ["versátil", "uma mão exótica", "duas mãos marcial", "1d10 ou 1d12"]
)

create_item(
    "arma-katana", "Katana", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 100", "1d8/1d10", "19", "Corte", "-", None, None, 1,
    book_jda, 148,
    "A tradicional espada de lâmina curva e de um só gume dos samurais de Tamu-ra. A katana é uma arma ágil. Você pode usá-la com uma mão (se for proficiente com armas exóticas) ou com duas mãos (como arma marcial, causando 1d10 de dano).",
    ["tamu-ra", "samurai", "ágil", "acuidade", "uma ou duas mãos"]
)

create_item(
    "arma-machado-anao", "Machado Anão", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d10", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "Um machado de cabo curto e lâmina pesadíssima forjado em Doherimm. Uma criatura com proficiência em armas marciais pode usá-lo com duas mãos.",
    ["anão", "doherimm", "crítico x3", "1d10"]
)

create_item(
    "arma-corrente-de-espinhos", "Corrente de Espinhos", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 25", "2d4/2d4", "19", "Perfuração", "-", None, None, 2,
    book_jda, 147,
    "Uma corrente de metal flexível recoberta de lâminas e pontas pontiagudas. É uma arma ágil, dupla e versátil (+2 para derrubar ou desarmar). Pode atacar alvos adjacentes ou a até 3m de distância.",
    ["corrente", "dupla", "ágil", "versátil", "alcance 3m"]
)

create_item(
    "arma-espada-taurica", "Espada Táurica", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d8", "x3", "Corte", "-", None, None, 2,
    book_jda, 147,
    "Uma espada maciça criada pelos minotauros de Tapista. Devido ao seu peso descomunal, exige Força 3 ou superior para ser empunhada sem penalidade adicional.",
    ["minotauro", "tapista", "2d8", "força 3", "devastadora"]
)

create_item(
    "arma-machado-taurico", "Machado Táurico", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d8", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Um machado gigantesco com cabeça dupla de bronze maciço criado por artífices táuricos. Exige Força 3 para ser empunhado.",
    ["minotauro", "tapista", "2d8", "crítico x3"]
)

create_item(
    "arma-shuriken", "Shuriken", "Armas", "Armas Exóticas", "Ataque à Distância / Arremesso",
    "T$ 1", "1d4", "x2", "Perfuração", "Curto", None, None, 0.1,
    book_jda, 150,
    "Uma pequena estrela de metal afiada de arremesso originária de Tamu-ra. Sacar um shuriken é uma ação livre. Você pode arremessar múltiplos shurikens com poderes adequados.",
    ["estrela ninja", "tamu-ra", "ação livre sacar", "arremesso rápido"]
)

# Armas de Fogo
create_item(
    "arma-pistola", "Pistola", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 250", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_jda, 149,
    "Uma arma de fogo de cano curto de carregar pela boca originária das oficinas de Zakharov ou Smokestone. Recarregar uma pistola é uma ação padrão (ou de movimento com munição especial). Margem 19 / Crítico x3.",
    ["pólvora", "zakharov", "tiro", "crítico 19/x3"]
)

create_item(
    "arma-mosquete", "Mosquete", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 500", "2d8", "19/x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 150,
    "Uma arma de fogo de uso difícil, mas com poder devastador. Recarregar um mosquete é uma ação completa. Causa 2d8 de dano com crítico 19/x3.",
    ["pólvora", "tiro longo", "devastador", "ação completa recarregar"]
)

# --- 1.1.1 MUNIÇÕES (Tabela 3-4, p. 151) ---
create_item(
    "municao-flechas-20", "Flechas (20)", "Munições", "Munições", "Munição de Arco",
    "T$ 2", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Hastes de madeira com ponta de metal e penas na cauda, usadas para disparar com arcos curtos ou arcos longos. Vendidas em aljavas de 20 unidades.",
    ["flecha", "aljava", "arco"]
)

create_item(
    "municao-virotes-20", "Virotes (20)", "Munições", "Munições", "Munição de Besta",
    "T$ 2", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Projéteis mais curtos e pesados que flechas, feitos para disparar com bestas leves ou pesadas. Vendidos em caixas ou bolsas com 20 unidades.",
    ["virote", "besta", "caixa"]
)

create_item(
    "municao-balas-de-funda-20", "Balas de Funda (20)", "Munições", "Munições", "Munição de Funda",
    "T$ 1", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Esferas de chumbo fundido de peso uniforme, projetadas para conferir máxima precisão e impacto quando arremessadas por fundas. Saco com 20 unidades.",
    ["chumbo", "funda", "esferas"]
)

create_item(
    "municao-balas-e-polvora-10", "Balas de Arma de Fogo e Pólvora (10)", "Munições", "Munições", "Munição de Arma de Fogo",
    "T$ 20", "-", "-", "-", "-", None, None, 1,
    book_jda, 151,
    "Esferas de chumbo e doses de pólvora seca necessárias para alimentar pistolas e mosquetes por 10 disparos.",
    ["pólvora", "tiro", "bala de chumbo", "pistola", "mosquete"]
)

# --- 1.2 ARMADURAS & ESCUDOS (Tabela 3-5, p. 152-153; Descrições p. 154-155) ---
# Armaduras Leves
create_item(
    "armadura-acolchoada", "Armadura Acolchoada", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 5", None, None, None, None, 1, 0, 2,
    book_jda, 154,
    "Uma túnica almofadada feita em linho ou lã acolchoada com camadas de feltro. É a armadura mais leve, mas protege todo o corpo, fornecendo +2 em Fortitude contra frio extremo.",
    ["linho", "lã", "leve", "fortitude"]
)

create_item(
    "armadura-de-couro", "Armadura de Couro", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 20", None, None, None, None, 2, 0, 2,
    book_jda, 154,
    "O peitoral desta armadura é feito de couro curtido em óleo fervente, para ficar mais rígido, enquanto as demais partes são feitas de couro flexível.",
    ["couro", "flexível", "batedor", "ladino"]
)

create_item(
    "armadura-couro-batido", "Couro Batido", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 35", None, None, None, None, 3, -1, 2,
    book_jda, 154,
    "Versão mais pesada da armadura de couro, reforçada com rebites de metal e tiras de aço flexível.",
    ["couro", "rebites", "reforçada"]
)

create_item(
    "armadura-gibao-de-peles", "Gibão de Peles", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 25", None, None, None, None, 4, -3, 2,
    book_jda, 154,
    "Usada principalmente por bárbaros e selvagens, esta armadura é formada por várias camadas de peles e couro espesso de animais.",
    ["peles", "bárbaro", "selvagem", "defesa 4"]
)

create_item(
    "armadura-couraca", "Couraça", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 500", None, None, None, None, 5, -4, 2,
    book_jda, 154,
    "A mais robusta das armaduras leves, formada por uma placa metálica inteiriça que protege o peito e as costas, presa sobre um casaco de couro acolchoado.",
    ["peitoral", "aço", "leve pesada", "defesa 5"]
)

# Armaduras Pesadas
create_item(
    "armadura-brunea", "Brunea", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 50", None, None, None, None, 5, -2, 5,
    book_jda, 154,
    "Colete de couro coberto com plaquetas de metal sobrepostas, como escamas de um peixe. Por ser barata de produzir, é a armadura mais utilizada no Reinado por soldados de infantaria e guardas de castelo.",
    ["escamas", "infantaria", "barata", "defesa 5"]
)

create_item(
    "armadura-cota-de-malha", "Cota de Malha", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 150", None, None, None, None, 6, -2, 5,
    book_jda, 154,
    "Longa veste de anéis metálicos interligados, formando uma malha flexível e resistente, que vai até os joelhos sobre um forro acolchoado.",
    ["anéis", "malha", "flexível", "defesa 6"]
)

create_item(
    "armadura-loriga-segmentada", "Loriga Segmentada", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 250", None, None, None, None, 7, -3, 5,
    book_jda, 154,
    "Composta por tiras horizontais de metal articuladas sobre tiras de couro internas, esta armadura pesada é muito utilizada por legionários do Império de Tauron.",
    ["tiras", "tauron", "legionário", "defesa 7"]
)

create_item(
    "armadura-meia-armadura", "Meia Armadura", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 600", None, None, None, None, 8, -4, 5,
    book_jda, 154,
    "Uma cota de malha reforçada com placas de metal (peitoral, caneleiras e braçadeiras) que protegem as partes vitais do corpo. Inclui um elmo de aço.",
    ["placas", "malha reforçada", "elmo", "defesa 8"]
)

create_item(
    "armadura-armadura-completa", "Armadura Completa", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 3.000", None, None, None, None, 10, -5, 5,
    book_jda, 154,
    "A mais forte e pesada das armaduras, formada por placas de metal forjadas e encaixadas de modo a cobrir o corpo inteiro. Inclui uma túnica acolchoada para ser usada sob as placas. Correias e fivelas distribuem o peso da armadura pelo corpo inteiro. Esta armadura precisa ser feita sob medida para cada usuário; um ferreiro cobra T$ 200 para adaptar uma armadura completa a um novo usuário.",
    ["placas completas", "cavaleiro", "sob medida", "defesa 10"]
)

# Escudos
create_item(
    "armadura-escudo-leve", "Escudo Leve", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 5", None, None, None, None, 1, -1, 1,
    book_jda, 154,
    "Tipicamente feito de madeira, este escudo é amarrado no antebraço, deixando a mão livre. Você pode carregar um objeto na mão que empunha o escudo, mas não manusear uma arma.",
    ["madeira", "antebraço", "mão livre", "defesa 1"]
)

create_item(
    "armadura-escudo-pesado", "Escudo Pesado", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 15", None, None, None, None, 2, -2, 2,
    book_jda, 154,
    "Normalmente feito de aço ou carvalho maciço reforçado, este escudo é preso ao antebraço e também deve ser empunhado com firmeza, impedindo o usuário de usar aquela mão.",
    ["aço", "carvalho", "empunhadura firme", "defesa 2"]
)

# --- 1.3 ITENS GERAIS (Tabela 3-6, p. 155-157; Descrições p. 155-163) ---
# Equipamento de Aventura
create_item(
    "item-agua-benta", "Água Benta", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 10", None, None, None, "Curto", None, None, 0.5,
    book_jda, 155,
    "Água abençoada por um clérigo de uma divindade bondosa. Pode ser arremessada como uma arma de arremesso contra mortos-vivos ou criaturas da Tormenta, causando 2d6 pontos de dano radiante.",
    ["sagrado", "radiante", "morto-vivo", "arremesso"]
)

create_item(
    "item-algemas", "Algemas", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 15", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Um par de braceletes de ferro ligados por uma corrente resistente. Prender uma criatura exige que ela esteja indefesa ou agarrada. Escapar das algemas exige um teste de Acrobacia (CD 25) ou quebrar o metal (Atletismo CD 25).",
    ["ferro", "prender", "captura", "acrobacia"]
)

create_item(
    "item-arpeu", "Arpéu", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Um gancho de metal com três ou quatro garras curvadas. Quando amarrado a uma corda, fornece +2 em testes de Atletismo para escalar superfícies onde possa ser fixado.",
    ["gancho", "escalada", "corda", "atletismo"]
)

create_item(
    "item-bandoleira-de-pocoes", "Bandoleira de Poções", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Um cinto de couro usado a tiracolo com pequenos bolsos para até 4 frascos de preparados alquímicos ou poções. Sacar um item da bandoleira é uma ação livre.",
    ["poções", "ação livre sacar", "cinto", "alquimia"]
)

create_item(
    "item-barraca", "Barraca", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 155,
    "Uma tenda de lona resistente capaz de abrigar até duas pessoas confortavelmente durante o descanso ao relento, protegendo de chuva e vento.",
    ["acampamento", "descanso", "abrigo", "lona"]
)

create_item(
    "item-corda", "Corda", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Uma corda resistente de cânhamo com 15 metros de comprimento. Suporta até 500kg de peso. Fornece +2 em testes de Atletismo para escalada com apoio.",
    ["cânhamo", "escalada", "amarrar", "15 metros"]
)

create_item(
    "item-espelho", "Espelho", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Uma chapa de aço polido de bolso. Útil para espiar ao redor de cantos sem se expor ou para sinalizar com reflexos à luz do sol.",
    ["aço polido", "espiar", "sinalização", "reflexo"]
)

create_item(
    "item-lampiao", "Lampião", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 7", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Um lampião de metal com painéis de vidro e alça. Queima uma dose de óleo por 6 horas, iluminando um raio de 9 metros com luz plena e mais 9 metros com luz fraca.",
    ["luz", "óleo", "iluminação", "visão"]
)

create_item(
    "item-mochila", "Mochila", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 2", None, None, None, None, None, None, 0,
    book_jda, 156,
    "Uma bolsa de couro ou lona com alças para as costas. Permite carregar itens com praticidade.",
    ["mochila", "bolsa", "carga"]
)

create_item(
    "item-mochila-de-aventureiro", "Mochila de Aventureiro", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 0,
    book_jda, 156,
    "Uma mochila de couro reforçado com presilhas, bolsos e divisórias. Aumenta o limite de carga do personagem em +2 espaços.",
    ["carga +2", "mochila", "capacidade", "aventura"]
)

create_item(
    "item-oleo-frasco", "Óleo (Frasco)", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 0.1", None, None, None, None, None, None, 0.5,
    book_jda, 156,
    "Um frasco com óleo combustível suficiente para alimentar um lampião ou tocha por 6 horas. Pode ser derramado no chão e incendiado.",
    ["combustível", "lampião", "fogo", "óleo"]
)

create_item(
    "item-organizador-de-pergaminhos", "Organizador de Pergaminhos", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 25", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Um estojo de couro cilíndrico impermeável com divisórias para até 6 pergaminhos. Sacar um pergaminho guardado no organizador é uma ação livre.",
    ["pergaminhos", "ação livre sacar", "magia", "estojo"]
)

create_item(
    "item-pe-de-cabra", "Pé de Cabra", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 2", None, None, None, None, None, None, 1,
    book_jda, 156,
    "Uma barra de ferro resistente com extremidade curvada e chanfrada. Fornece +2 em testes de Atletismo para forçar portas e quebrar objetos de madeira.",
    ["ferro", "arrombar", "alavanca", "atletismo"]
)

create_item(
    "item-saco-de-dormir", "Saco de Dormir", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Uma manta grossa acolchoada forrada de lã que se fecha com amarras. Fornece o conforto necessário para recuperar PV e PM em acampamentos ao ar livre.",
    ["descanso", "acampamento", "recuperação", "sono"]
)

create_item(
    "item-simbolo-sagrado", "Símbolo Sagrado", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Um medalhão esculpido com o símbolo heráldico de uma divindade do Panteão. Clérigos e paladinos precisam empunhar seu símbolo sagrado para conjurar suas magias divinas.",
    ["deus", "panteão", "foco divino", "clérigo", "paladino"]
)

create_item(
    "item-tocha", "Tocha", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 0.1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Um bastão de madeira com estopa embebida em piche na ponta. Queima por 1 hora, iluminando um raio de 6 metros. Se usada como arma improvisada, causa 1d4 de dano de fogo.",
    ["fogo", "luz", "iluminação", "improvisada"]
)

create_item(
    "item-vara-de-madeira-3m", "Vara de Madeira (3m)", "Itens Gerais", "Itens Gerais", "Equipamento de Aventura",
    "T$ 0.2", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Uma vara longa de madeira flexível e resistente. Muito útil para acionar armadilhas à distância ou testar a profundidade de fossos e poços sem se arriscar.",
    ["haste", "armadilhas", "segurança", "fosso"]
)

# Ferramentas
create_item(
    "item-alaude-elfico", "Alaúde Élfico", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 300", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um instrumento de cordas feito em madeira leve de Lenórienn com cordas de seda mágica. Fornece +2 em testes de Atuação (música) e reduz o custo de uma música de bardo em -1 PM.",
    ["alaúde", "élfico", "bardo", "-1 pm música", "atuação +2"]
)

create_item(
    "item-estojo-de-disfarces", "Estojo de Disfarces", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Maquiagens, perucas, próteses de cera, tinturas e apetrechos teatrais. Permite usar a perícia Enganação para se disfarçar e fornece +2 no teste.",
    ["enganação", "disfarce", "peruca", "maquiagem"]
)

create_item(
    "item-flauta-mistica", "Flauta Mística", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 150", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Uma flauta entalhada em madeira nobre com orifícios de prata. Fornece +1 na CD para resistir às habilidades de música de bardo do usuário.",
    ["bardo", "cd +1", "música", "flauta"]
)

create_item(
    "item-gazua", "Gazua", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um conjunto de arames e palhetas de aço temperado. Permite realizar testes de Ladinagem para abrir fechaduras.",
    ["abrir fechaduras", "ladinagem", "arrombamento"]
)

create_item(
    "item-instrumento-musical", "Instrumento Musical", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 35", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um instrumento comum (flauta, alaúde, tambor ou cítara). Permite usar a perícia Atuação e habilidades de bardo.",
    ["música", "bardo", "atuação"]
)

create_item(
    "item-luneta", "Luneta", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 100", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um tubo com lentes de cristal polido. Fornece +2 em testes de Percepção para observar objetos ou criaturas distantes.",
    ["lentes", "cristal", "percepção", "distância"]
)

create_item(
    "item-maleta-de-medicamentos", "Maleta de Medicamentos", "Itens Gerais", "Itens Gerais", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Faixas de linho, unguentos anti-sépticos, agulhas de sutura e instrumentos cirúrgicos. Permite realizar testes de Cura para primeiros socorros sem penalidade e fornece +2 em testes de Cura.",
    ["primeiros socorros", "cura", "medicina", "sutura"]
)

# Vestuário
create_item(
    "item-chapeu-arcano", "Chapéu Arcano", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um chapéu pontudo ou de abas largas feito de feltro fino ou veludo, símbolo tradicional dos arcanistas. Fornece +1 em testes de Misticismo.",
    ["misticismo", "arcano", "mago", "chapéu"]
)

create_item(
    "item-gorro-de-ervas", "Gorro de Ervas", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 75", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um gorro de lã com forro embebido em infusões de ervas calmantes. Fornece +1 em testes de Vontade.",
    ["vontade +1", "ervas", "mental", "gorro"]
)

create_item(
    "item-luva-de-pelica", "Luva de Pelica", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Luvas finas e flexíveis de couro macio. Fornecem +1 em testes de Ladinagem para prestidigitação e furto de pequenos objetos.",
    ["ladinagem +1", "furto", "couro macio", "luvas"]
)

create_item(
    "item-manto-camuflado", "Manto Camuflado", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 12", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um manto com estampa manchada em tons de verde, marrom ou cinza. Fornece +1 em testes de Furtividade no terreno correspondente.",
    ["furtividade +1", "camuflagem", "floresta", "manto"]
)

create_item(
    "item-manto-eclesiastico", "Manto Eclesiástico", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Uma túnica cerimonial bordada com fios de ouro e símbolos sagrados. Fornece +1 em testes de Religião.",
    ["religião +1", "clérigo", "sagrado", "manto"]
)

create_item(
    "item-robe-mistico", "Robe Místico", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um manto longo de seda com inscrições arcanas tecidas no forro. Fornece +1 na Defesa contra magias.",
    ["defesa contra magia +1", "arcanista", "seda", "robe"]
)

create_item(
    "item-sapatos-de-camurca", "Sapatos de Camurça", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 8", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Calçados com solado macio que abafam o som dos passos. Fornecem +1 em testes de Furtividade para se mover silenciosamente.",
    ["furtividade +1", "silêncio", "passos", "sapatos"]
)

create_item(
    "item-traje-da-corte", "Traje da Corte", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 100", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Roupas finíssimas de seda, veludo e pedrarias com corte nobre. Fornecem +1 em testes de Diplomacia e Nobreza com membros da nobreza.",
    ["diplomacia +1", "nobreza +1", "corte", "elegância"]
)

create_item(
    "item-traje-de-viajante", "Traje de Viajante", "Itens Gerais", "Itens Gerais", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 0,
    book_jda, 159,
    "Botas de couro resistentes, calças grossas, camisa de linho e casaco impermeável. Traje padrão para expedições por terrenos acidentados.",
    ["viagem", "conforto", "explorador"]
)

# Esotéricos
create_item(
    "item-bolsa-de-po", "Bolsa de Pó", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 300", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma bolsinha com pós minerais e pós de fadas. Quando você lança uma magia que afeta uma área, pode aumentar a área em 50% gastando 1 PM adicional.",
    ["área aumentada", "esotérico", "pó mágico", "conjurador"]
)

create_item(
    "item-cajado-arcano", "Cajado Arcano", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 1.000", None, None, None, None, None, None, 2,
    book_jda, 160,
    "Um cajado de madeira nobre talhado com runas e encimado por um cristal canalizador. Permite lançar magias com alcance aumentado em um passo (Curto para Médio, Médio para Longo).",
    ["foco arcano", "alcance", "runas", "cristal"]
)

create_item(
    "item-cetro-elemental", "Cetro Elemental", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma barra de metal adornada com joias elementais (rubi para fogo, safira para frio, topázio para eletricidade, esmeralda para ácido). Aumenta o dano de magias do elemento correspondente em +2 por dado de dano.",
    ["dano elemental +2", "fogo", "frio", "ácido", "eletricidade"]
)

create_item(
    "item-costela-de-lich", "Costela de Lich", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 300", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um fragmento ósseo preservado com necromancia arcana. Suas magias da escola Necromancia têm sua CD aumentada em +1.",
    ["necromancia", "cd +1", "osso", "morto-vivo"]
)

create_item(
    "item-dedo-de-ente", "Dedo de Ente", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 200", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um galho vivo arrancado de um guardião da floresta secular. Aumenta a cura de suas magias curativas em +1 PV por dado rolado.",
    ["cura +1 por dado", "natureza", "druida", "clérigo"]
)

create_item(
    "item-luva-de-ferro", "Luva de Ferro", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 150", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma manopla ornamentada gravada com runas de abjuração. Concede +1 na Defesa enquanto você mantiver uma magia de sustentação ativa.",
    ["defesa +1", "abjuração", "sustentada", "manopla esotérica"]
)

create_item(
    "item-medalhao-de-prata", "Medalhão de Prata", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um amuleto prateado com relevos geométricos sagrados. Suas magias divinas de alcance Pessoal têm sua duração duplicada.",
    ["duração dupla", "divina", "prata", "medalhão"]
)

create_item(
    "item-orbe-cristalino", "Orbe Cristalino", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 750", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma esfera perfeita de quartzo transparente ou obsidiana. Quando empunhado por um conjurador, aumenta a CD para resistir às suas magias em +1.",
    ["cd +1", "cristal", "resistência", "foco esotérico"]
)

create_item(
    "item-tomo-hermetico", "Tomo Hermético", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 1.500", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Um livro encadernado em couro com fecho de prata repleto de anotações místicas arcanas. Permite que um arcanista prepare uma magia adicional.",
    ["magia extra", "grimório", "estudo", "arcanista"]
)

create_item(
    "item-varinha-arcana", "Varinha Arcana", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 100", None, None, None, None, None, None, 1,
    book_jda, 160,
    "Uma haste delgada de madeira nobre ou osso talhado. Quando você lança uma magia que causa dano enquanto empunha uma varinha arcana, essa magia causa +1 ponto de dano por dado de dano.",
    ["dano mágico", "varinha", "foco", "arcanista"]
)

# Alquímicos - Preparados
create_item(
    "item-acido", "Ácido", "Itens Gerais", "Itens Gerais", "Alquímicos - Preparados",
    "T$ 10", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Um frasco com líquido corrosivo que pode ser arremessado. Causa 2d4 pontos de dano de ácido na criatura atingida e 1 ponto de dano de ácido nas criaturas adjacentes.",
    ["ácido", "corrosão", "arremesso", "dano de área"]
)

create_item(
    "item-balsamo-restaurador", "Bálsamo Restaurador", "Itens Gerais", "Itens Gerais", "Alquímicos - Preparados",
    "T$ 10", None, None, None, None, None, None, 0.5,
    book_jda, 161,
    "Uma pasta espessa feita de ervas medicinais e óleos cicatrizantes. Aplicar o bálsamo em ferimentos com uma ação padrão recupera 2d4 pontos de vida.",
    ["cura", "pv", "unguento", "medicina"]
)

create_item(
    "item-bomba", "Bomba", "Itens Gerais", "Itens Gerais", "Alquímicos - Preparados",
    "T$ 50", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Uma esfera de cerâmica recheada de pólvora com pavio curto. Ao explodir, causa 6d6 pontos de dano de impacto e fogo em todas as criaturas a até 3m (Reflexos CD 15 reduz à metade).",
    ["explosão", "6d6", "área 3m", "pólvora"]
)

create_item(
    "item-fogo-alquimico", "Fogo Alquímico", "Itens Gerais", "Itens Gerais", "Alquímicos - Preparados",
    "T$ 10", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Uma substância gelatinosa e volátil que entra em combustão ao contato com o ar. Ao ser arremessado, explode causando 1d6 pontos de dano de fogo no alvo e incendiando-o (1d6 de dano contínuo por rodada até apagar).",
    ["fogo", "combustão", "arremesso", "dano contínuo"]
)

create_item(
    "item-fumaca-negra", "Fumaça Negra", "Itens Gerais", "Itens Gerais", "Alquímicos - Preparados",
    "T$ 15", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Um frasco com pó que produz uma nuvem densa de fumaça escura que ocupa um cubo de 4,5m de lado por 1d4 rodadas, fornecendo camuflagem total.",
    ["fumaça", "camuflagem", "fuga", "cegueira"]
)

create_item(
    "item-po-de-cegueira", "Pó de Cegueira", "Itens Gerais", "Itens Gerais", "Alquímicos - Preparados",
    "T$ 30", None, None, None, "Curto", None, None, 0.5,
    book_jda, 161,
    "Um pó cáustico fino arremessado nos olhos de uma criatura adjacente. O alvo deve passar em um teste de Fortitude (CD 15) ou fica cego por 1d4 rodadas.",
    ["cegueira", "fortitude cd 15", "debilitante"]
)

# Alquímicos - Catalisadores
create_item(
    "item-essencia-de-mana", "Essência de Mana", "Itens Gerais", "Itens Gerais", "Alquímicos - Catalisadores",
    "T$ 50", None, None, None, None, None, None, 0.5,
    book_jda, 162,
    "Um líquido azul brilhante destilado de flores mágicas raras. Beber a essência com uma ação padrão recupera 1d4 pontos de mana (PM) imediatamente.",
    ["pm", "mana", "recuperação", "poção azul"]
)

create_item(
    "item-essencia-abissal", "Essência Abissal", "Itens Gerais", "Itens Gerais", "Alquímicos - Catalisadores",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_jda, 162,
    "Fluido negro destilado do sangue de demônios e extraplanar sombrios. Ao conjurar uma magia de trevas, aumenta o dano causado em +1 por dado de dano.",
    ["trevas", "abissal", "dano aumentado", "catalisador"]
)

# Alquímicos - Venenos
create_item(
    "item-beladona", "Beladona", "Itens Gerais", "Itens Gerais", "Alquímicos - Venenos",
    "T$ 1.500", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Veneno vegetal mortal extraído de bagas raras. Tipo: Ingestão ou Contato. O alvo deve passar em Fortitude (CD 25) ou sofre 4d12 pontos de dano de veneno e fica inconsciente.",
    ["veneno mortal", "cd 25", "4d12", "letal"]
)

create_item(
    "item-peconha-comum", "Peçonha Comum", "Itens Gerais", "Itens Gerais", "Alquímicos - Venenos",
    "T$ 15", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Veneno extraído de víboras e escorpiões do ermo. Tipo: Contato com arma. Causa 1d12 pontos de dano de veneno (Fortitude CD 15 reduz à metade).",
    ["veneno", "arma", "1d12", "peçonha"]
)

create_item(
    "item-peconha-concentrada", "Peçonha Concentrada", "Itens Gerais", "Itens Gerais", "Alquímicos - Venenos",
    "T$ 90", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Versão purificada e destilada da peçonha comum. Causa 2d12 pontos de dano de veneno e impõe a condição fraco por 1 hora (Fortitude CD 18).",
    ["veneno", "fraco", "2d12", "cd 18"]
)

# Alimentação
create_item(
    "item-gorad-quente", "Gorad Quente", "Itens Gerais", "Itens Gerais", "Alimentação",
    "T$ 18", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Uma porção de chocolate espesso e aromático servido fervendo, especialidade das estalagens nobres de Deheon. Concede +1 em testes de Fortitude e Vontade por 4 horas.",
    ["chocolate", "conforto", "bônus resistência", "estalagem"]
)

create_item(
    "item-prato-do-aventureiro", "Prato do Aventureiro", "Itens Gerais", "Itens Gerais", "Alimentação",
    "T$ 1", None, None, None, None, None, None, 0.5,
    book_jda, 163,
    "Ensopado farto de carne de caça, raízes e pão rústico. Uma refeição reforçada que recupera +1 PV adicional durante o descanso.",
    ["refeição", "recuperação", "descanso", "ensopado"]
)

# Animais & Veículos
create_item(
    "item-cavalo-de-guerra", "Cavalo de Guerra", "Itens Gerais", "Itens Gerais", "Animais & Montarias",
    "T$ 400", None, None, None, None, None, None, 0,
    book_jda, 163,
    "Um corcel imponente treinado para não se assustar com o ruído de batalha. Conta como um parceiro Guardião ou Montaria combatente que concede bônus em testes de investida montada.",
    ["montaria", "cavalo", "guerra", "parceiro"]
)

create_item(
    "item-carroca", "Carroça", "Itens Gerais", "Itens Gerais", "Veículos",
    "T$ 150", None, None, None, None, None, None, 0,
    book_jda, 163,
    "Veículo de madeira de quatro rodas tracionado por animais de carga. Tem capacidade de carga para até 100 espaços de itens e suprimentos de expedição.",
    ["transporte", "carga 100", "viagem", "tração animal"]
)

create_item(
    "item-carruagem", "Carruagem", "Itens Gerais", "Itens Gerais", "Veículos",
    "T$ 500", None, None, None, None, None, None, 0,
    book_jda, 163,
    "Veículo fechado e estofado de luxo para transporte confortável de nobres e cortesãos com janelas de vidro e suspensão de correias.",
    ["luxo", "nobreza", "transporte urbano"]
)

# --- 1.4 ITENS SUPERIORES & MATERIAIS ESPECIAIS (Tabela 3-8, p. 164-168) ---
create_item(
    "melhoria-afiada", "Afiada", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, "+1 margem", None, None, None, None, 0,
    book_jda, 165,
    "A lâmina ou ponta da arma é trabalhada com um fio navalha extraordinário. A margem de ameaça da arma aumenta em +1 (ex: de 19 para 18). Só pode ser aplicada a armas que causem dano de corte ou perfuração.",
    ["crítico +1", "ameaça", "fio de navalha", "lâmina"]
)

create_item(
    "melhoria-alongada", "Alongada", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, None, None, "+1.5m", None, None, 0,
    book_jda, 165,
    "A haste ou lâmina é forjada com comprimento estendido sem perder o equilíbrio, permitindo atacar alvos a até 1,5m além do alcance corpo a corpo normal.",
    ["alcance extra", "haste", "espaçamento"]
)

create_item(
    "melhoria-certeira", "Certeira", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 165,
    "O equilíbrio milimétrico da arma concede +1 nos testes de ataque desferidos com ela.",
    ["ataque +1", "precisão", "balanceada"]
)

create_item(
    "melhoria-cruel", "Cruel", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", "+2 dano", None, None, None, None, None, 0,
    book_jda, 165,
    "Dentes serrilhados ou espigões cruéis aumentam a severidade dos ferimentos, fornecendo +2 nas rolagens de dano.",
    ["dano +2", "serrilhado", "ferimentos"]
)

create_item(
    "melhoria-macica", "Maciça", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, "+1 multiplicador", None, None, None, None, 0,
    book_jda, 165,
    "A arma é forjada com distribuição de peso pesada e sólida. O multiplicador de crítico da arma aumenta em +1 (ex: de x2 para x3).",
    ["crítico pesado", "multiplicador", "impacto", "dano bruto"]
)

create_item(
    "melhoria-precisa", "Precisa", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", None, "+1 margem", None, None, None, None, 0,
    book_jda, 165,
    "Para armas de disparo ou arremesso, miras finamente calibradas aumentam a margem de ameaça de ataque à distância em +1.",
    ["tiro certeiro", "mira", "disparo crítico"]
)

create_item(
    "melhoria-pungente", "Pungente", "Itens Superiores", "Melhorias", "Melhoria de Arma",
    "T$ 300", "+2 dano", None, None, None, None, None, 0,
    book_jda, 165,
    "A geometria e peso da arma aumentam o impacto do golpe, fornecendo +2 nas rolagens de dano.",
    ["dano +2", "força", "letal"]
)

create_item(
    "melhoria-reforcada", "Reforçada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, 1, 0, 0,
    book_jda, 166,
    "Placas suplementares ou rebites de liga temperada aumentam o bônus de Defesa da armadura ou escudo em +1.",
    ["defesa +1", "blindagem", "resistência"]
)

create_item(
    "melhoria-ajustada", "Ajustada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, None, -1, 0,
    book_jda, 166,
    "Articulações com dobradiças polidas e correias ergonômicas reduzem a penalidade de armadura em 1 ponto (ex: de -2 para -1).",
    ["mobilidade", "penalidade -1", "agilidade"]
)

create_item(
    "melhoria-blindada", "Blindada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 166,
    "A armadura recebe reforços contra impactos violentos. Fornece Redução de Dano (RD) 2 contra dano de corte e impacto.",
    ["rd 2", "blindagem", "impacto", "corte"]
)

create_item(
    "melhoria-sob-medida", "Sob Medida", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo",
    "T$ 300", None, None, None, None, None, None, -1,
    book_jda, 166,
    "Feita exclusivamente para a compleição anatômica do usuário, reduz o espaço ocupado pela armadura em 1.",
    ["espaço -1", "peso", "ergonomia"]
)

create_item(
    "melhoria-harmonizada", "Harmonizada", "Itens Superiores", "Melhorias", "Melhoria de Esotérico",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 167,
    "O item esotérico é afinado harmonicamente com a energia mística de uma magia específica. Reduz o custo em PM dessa magia em -1 PM.",
    ["-1 pm", "afinidade", "magia favorita", "esotérico"]
)

create_item(
    "melhoria-canalizadora", "Canalizadora", "Itens Superiores", "Melhorias", "Melhoria de Esotérico",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 167,
    "Estrutura com filamentos condutores que facilitam a drenagem de poder. Fornece +1 em testes de Misticismo para identificar magias e manipular itens mágicos.",
    ["canalização", "misticismo +1", "foco"]
)

# Materiais Especiais (pág 167-168)
create_item(
    "material-aco-rubi", "Aço-Rubi", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.000", None, None, None, None, None, None, 0,
    book_jda, 167,
    "Um metal avermelhado raro forjado com cinzas da Tormenta e sangue de dragão. Armas de aço-rubi ignoram 10 pontos de redução de dano (RD) de qualquer alvo. Armaduras fornecem RD 2 contra todos os tipos de dano.",
    ["ignora rd 10", "rd 2", "metal rubi", "tormenta"]
)

create_item(
    "material-adamante", "Adamante", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.500", None, None, None, None, None, None, 0,
    book_jda, 167,
    "O metal mais denso e duro de Arton. Armas de adamante aumentam o dano em um passo (ex: 1d6 para 1d8). Armaduras e escudos pesados feitos de adamante fornecem RD 5 contra dano físico.",
    ["metal indestrutível", "passo de dano +1", "rd 5"]
)

create_item(
    "material-gelo-eterno", "Gelo Eterno", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.000", "+1d6 frio", None, None, None, None, None, 0,
    book_jda, 167,
    "Gelo glacial das Montanhas Uivantes que nunca derrete. Armas feitas de gelo eterno causam +1d6 pontos de dano de frio. Armaduras concedem Resistência a Frio 10.",
    ["frio", "+1d6 frio", "uivantes", "res frio 10"]
)

create_item(
    "material-madeira-de-tollon", "Madeira de Tollon", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 168,
    "Uma madeira negra e densa nativa das florestas de Tollon com propriedades canalizadoras. Reduz o custo em PM de uma magia lançada com o item em -1 PM.",
    ["tollon", "madeira mágica", "-1 pm", "canalizador"]
)

create_item(
    "material-materia-vermelha", "Matéria Vermelha", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.500", "+1d6 lefeu", None, None, None, None, None, 0,
    book_jda, 168,
    "Matéria viva da tempestade rubra cristalizada. Armas causam +1d6 de dano contra criaturas artonianas não lefeu. Concede +1 poder da Tormenta sem contar para perda de Carisma.",
    ["tormenta", "rubra", "lefeu", "poder da tormenta"]
)

create_item(
    "material-mitral", "Mitral", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.000", None, None, None, None, None, -2, -1,
    book_jda, 168,
    "Conhecido como prata élfica, este metal prateado é tão resistente quanto o aço, mas extremamente leve. Armaduras pesadas de mitral contam como leves. Reduz a penalidade de armadura em 2 e o espaço em 1.",
    ["élfico", "ultraleve", "penalidade -2", "armadura pesada vira leve"]
)

create_item(
    "material-prata", "Prata", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 300", None, None, None, None, None, None, 0,
    book_jda, 168,
    "Metal nobre forjado em revestimento sobre lâminas e projéteis. Armas de prata ignoram a RD de licantropos e mortos-vivos incorpóreos.",
    ["licantropo", "lobisomem", "morto-vivo", "prateada"]
)

# =========================================================================
# 2. LIVRO: T20 HERÓIS DE ARTON (v1.1)
# =========================================================================

# Armas (Tabela 3-1, p. 216-222)
create_item(
    "arma-adaga-oposta", "Adaga Oposta", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 30", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_hda, 216,
    "Uma adaga com lâmina curva invertida projetada para combate com duas armas. Quando você luta com duas armas e uma delas é a adaga oposta, recebe +1 na Defesa.",
    ["esgrima", "duas armas", "defesa +1", "acuidade"]
)

create_item(
    "arma-canhao-portatil", "Canhão Portátil", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 1.500", "4d8", "19/x3", "Impacto/Fogo", "Médio", None, None, 4,
    book_hda, 217,
    "Uma versão compacta de canhão naval com alças de sustentação e suporte para disparo individual. Exige Força 3 para ser disparado sem cair. Causa 4d8 de dano devastador.",
    ["canhão", "artilharia", "4d8", "tiro pesado", "força 3"]
)

create_item(
    "arma-clava-pesada", "Clava Pesada", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 5", "2d6", "x2", "Impacto", "-", None, None, 2,
    book_hda, 217,
    "Uma viga de madeira pesada com reforços de ferro nas extremidades, comum entre ogros e gigantes.",
    ["2d6", "brutal", "impacto", "ogro"]
)

create_item(
    "arma-garra-de-tigre", "Garra de Tigre", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve",
    "T$ 25", "1d6", "18", "Corte", "-", None, None, 1,
    book_hda, 217,
    "Lâminas curvas afiadas presas a uma empunhadura transversal que se projeta entre os dedos. Arma ágil com margem 18-20.",
    ["tamu-ra", "lâmina de mão", "crítico 18", "ágil"]
)

create_item(
    "arma-lanca-de-justa", "Lança de Justa", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 15", "1d10", "x3", "Perfuração", "-", None, None, 2,
    book_hda, 218,
    "Uma lança maciça balanceada especificamente para torneios de cavalaria e investidas montadas devastadoras.",
    ["justa", "torneio", "cavalaria", "investida"]
)

create_item(
    "arma-martelo-de-guerra-anao", "Martelo de Guerra Anão", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 45", "1d10", "x3", "Impacto", "-", None, None, 1,
    book_hda, 218,
    "Um martelo com cabeça de aço endurecido pesado esculpido com runas dos clãs de Doherimm.",
    ["anão", "doherimm", "crítico x3", "runas"]
)

create_item(
    "arma-mosquete-de-tambor", "Mosquete de Tambor", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 1.200", "2d8", "19/x3", "Perfuração", "Médio", None, None, 2,
    book_hda, 219,
    "Um mosquete avançado dotado de um cilindro giratório com capacidade para 4 disparos antes de precisar ser totalmente recarregado.",
    ["tambor", "4 tiros", "avanço tecnológico", "disparo rápido"]
)

create_item(
    "arma-pistola-de-tambor", "Pistola de Tambor", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 800", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_hda, 219,
    "Uma pistola com mecanismo de tambor de 4 câmaras de tiro. Permite disparar 4 tiros em rodadas consecutivas.",
    ["tambor", "4 tiros", "revólver artoniano", "pistola rápida"]
)

create_item(
    "arma-sifao-caustico", "Sifão Cáustico", "Armas", "Armas Exóticas", "Ataque à Distância / Disparo",
    "T$ 350", "2d6", "x2", "Ácido", "Curto", None, None, 2,
    book_hda, 222,
    "Um engenho mecânico acoplado a um reservatório que projeta jatos contínuos de fluido alquímico cáustico sob pressão.",
    ["lança chamas", "ácido", "pressão", "engenhoqueiro"]
)

# Armaduras & Escudos (Tabela 3-3, p. 223-226)
create_item(
    "armadura-broquel", "Broquel", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 10", None, None, None, None, 1, 0, 1,
    book_hda, 224,
    "Um pequeno escudo de metal convexo de cerca de 30cm empunhado pela borda. Não impõe penalidade de armadura e pode ser usado para aparar golpes rápidos.",
    ["parry", "esgrima", "penalidade zero", "defesa 1"]
)

create_item(
    "armadura-escudo-torre", "Escudo Torre", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 50", None, None, None, None, 3, -4, 3,
    book_hda, 224,
    "Um escudo retangular gigantesco que cobre o usuário da cabeça aos pés. Fornece Defesa +3 e permite gastar uma ação padrão para receber cobertura total até o próximo turno.",
    ["cobertura total", "defesa 3", "muralha", "pesado"]
)

create_item(
    "armadura-armadura-de-pedra", "Armadura de Pedra", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 500", None, None, None, None, 9, -5, 6,
    book_hda, 225,
    "Placas de granito talhado articuladas criadas por anões e golens. Fornece Defesa +9 e RD 2 contra fogo e ácido.",
    ["granito", "anão", "rd 2 fogo/ácido", "defesa 9"]
)

# Itens Gerais (p. 227-238)
create_item(
    "item-compasso-mistico", "Compasso Místico", "Itens Gerais", "Itens Gerais", "Esotéricos",
    "T$ 400", None, None, None, None, None, None, 1,
    book_hda, 234,
    "Um instrumento de latão polido gravado com coordenadas astrais. Fornece +2 em testes de Navegação e Sobrevivência para orientação e reduz o custo de magias de Adivinhação em -1 PM.",
    ["astronomia", "adivinhação", "-1 pm", "navegação"]
)

create_item(
    "item-essencia-fantasmal", "Essência Fantasmal", "Itens Gerais", "Itens Gerais", "Alquímicos - Catalisadores",
    "T$ 250", None, None, None, None, None, None, 0.5,
    book_hda, 235,
    "Ectoplasma purificado colhido em cemitérios assombrados de Bielefeld. Permite afetar alvos incorpóreos com dano pleno durante 1 combate.",
    ["ectoplasma", "incorpóreo", "fantasma", "catalisador"]
)

# Capangas & Veículos (p. 240-244)
create_item(
    "capanga-guarda-costas", "Guarda-Costas", "Capangas", "Capangas", "Seguidor / Proteção",
    "T$ 50/mês", None, None, None, None, None, None, 0,
    book_hda, 240,
    "Um mercenário veterano contratado para interpor seu escudo em sua defesa. Uma vez por rodada, concede +2 na Defesa contra um ataque direcionado a você.",
    ["mercenário", "defesa +2", "aliado", "contrato"]
)

create_item(
    "capanga-batedor", "Batedor", "Capangas", "Capangas", "Seguidor / Exploração",
    "T$ 40/mês", None, None, None, None, None, None, 0,
    book_hda, 240,
    "Um rastreador experiente contratado para explorar passagens secretas e detectar emboscadas com antecedência. Fornece +2 em Percepção e Sobrevivência do grupo.",
    ["rastreador", "percepção +2", "explorador"]
)

create_item(
    "veiculo-carruagem-blindada", "Carruagem Blindada", "Veículos", "Veículos", "Veículo Terrestre",
    "T$ 500", None, None, None, None, None, None, 10,
    book_hda, 241,
    "Uma carruagem pesada reforçada com placas de metal nas laterais e seteiras para disparo seguro de bestas e armas de fogo.",
    ["transporte", "blindagem", "cavalos", "cobertura"]
)

create_item(
    "veiculo-balao-goblin", "Balão Goblin", "Veículos", "Veículos", "Veículo Aéreo",
    "T$ 1.000", None, None, None, None, None, None, 20,
    book_hda, 242,
    "Um balão de ar quente sustentado por um cesto de vime reforçado com caldeira de óleo pressurizado. Permite sobrevoar terrenos intransponíveis a 12m de altitude.",
    ["vôo", "goblin", "aéreo", "ar quente"]
)

# =========================================================================
# 3. LIVRO: AMEAÇAS DE ARTON (v1.0 - Bazar Monstruoso)
# =========================================================================

# Armas (p. 392-395)
create_item(
    "arma-clava-de-osso", "Clava de Osso", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão",
    "T$ 1", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_ameacas, 392,
    "Esculpida no fêmur de uma fera colossal do ermo. Rústica e contundente, não sofre penalidade ao atacar criaturas de tipo Monstro.",
    ["osso", "bazar monstruoso", "selvagem"]
)

create_item(
    "arma-garra-monstruosa", "Garra Monstruosa", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 15", "1d6", "x3", "Perfuração/Corte", "-", None, None, 1,
    book_ameacas, 393,
    "A garra arrancada de um mantícora ou grifo, adaptada com empunhadura de couro. Causa dano crítico triplo.",
    ["fera", "garra", "mantícora", "crítico x3"]
)

create_item(
    "arma-traque", "Traque", "Armas", "Armas de Fogo", "Ataque à Distância / Disparo",
    "T$ 50", "1d10", "x2", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Uma arma de fogo rudimentar feita de sucata, osso oco e restos de metal amarrados com arame por goblins do ermo. Quando rola um 1 natural no ataque, emperra.",
    ["sucata", "goblin", "improvisada", "fogo barato"]
)

# Armaduras & Escudos Monstruosos (p. 395-396)
create_item(
    "armadura-de-ossos", "Armadura de Ossos", "Armaduras & Escudos", "Armaduras Leves", "Armadura Leve",
    "T$ 40", None, None, None, None, 3, -1, 2,
    book_ameacas, 395,
    "Feita de costelas e vértebras tratadas de monstros do ermo unidas por tiras de couro curtido. Concede +2 em testes de Intimidação.",
    ["ossos", "nezumi", "intimidação +2", "defesa 3"]
)

create_item(
    "armadura-quitinosa", "Armadura Quitinosa", "Armaduras & Escudos", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 800", None, None, None, None, 8, -3, 4,
    book_ameacas, 395,
    "Forjada a partir de placas de carapaça endurecida de artrópodes gigantes ou caranguejos de Lamnor. É imune a corrosão por ácido e fornece Defesa +8.",
    ["quitina", "lamnor", "imune ácido", "defesa 8"]
)

create_item(
    "armadura-escudo-de-carapaca", "Escudo de Carapaça", "Armaduras & Escudos", "Escudos", "Escudo",
    "T$ 60", None, None, None, None, 2, -1, 2,
    book_ameacas, 396,
    "Um escudo pesado esculpido na carapaça dorsal de um besouro gigante do ermo. Fornece Defesa +2 e RD 2 contra perfuração.",
    ["carapaça", "besouro", "rd 2 perfuração", "defesa 2"]
)

# Materiais Monstruosos & Melhorias (p. 399-402)
create_item(
    "material-couro-de-dragao", "Couro de Dragão", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 2.000", None, None, None, None, 1, None, 0,
    book_ameacas, 399,
    "Couro escamado autêntico curtido a partir de um dragão venerável. Fornece Resistência a Energia 10 contra o elemento do dragão e aumenta o bônus de Defesa da armadura em +1.",
    ["dragão", "re 10", "escamas", "lendário"]
)

create_item(
    "material-quitina-razza", "Quitina Razza", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 1.200", None, None, None, None, None, -1, 0,
    book_ameacas, 401,
    "Carapaça ultrarresistente e leve de espécimes Razza de Lamnor. Reduz penalidade de armadura em 1 e concede +2 em testes de resistência contra efeitos de veneno.",
    ["razza", "veneno +2", "leveza", "resistência"]
)

create_item(
    "material-osso-de-behemoth", "Osso de Behemoth", "Itens Superiores", "Materiais Especiais", "Material Especial",
    "T$ 800", "+2 dano impacto", None, None, None, None, None, 0,
    book_ameacas, 401,
    "Osso ultradenso petrificado de monstros colossais. Armas de impacto causam +2 pontos de dano e ignoram 5 pontos de dureza de objetos.",
    ["behemoth", "dano +2", "impacto colossal"]
)

print(f"Total de equipamentos catalogados: {len(equipments)}")

with open("data/categories/equipamentos.json", "w", encoding="utf-8") as f:
    json.dump(equipments, f, ensure_ascii=False, indent=2)

print("data/categories/equipamentos.json gerado com sucesso!")
