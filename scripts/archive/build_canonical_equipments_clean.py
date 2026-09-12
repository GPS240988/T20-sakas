import json
import os

os.makedirs("data/categories", exist_ok=True)

equipments = []
id_set = set()

def add_item(
    id_slug, name, subcategory, subtype, purpose,
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
        subtype.lower(),
        purpose.lower() if purpose else "",
        name.lower()
    ] + [t.lower() for t in tags])
    all_tags.discard("")
    
    table_data = {
        "price": price,
        "subcategory": subcategory,
        "subtype": subtype,
        "space": space
    }
    if damage and damage != "-": table_data["damage"] = damage
    if critical and critical != "-": table_data["critical"] = critical
    if damage_type and damage_type != "-": table_data["damageType"] = damage_type
    if range_dist and range_dist != "-": table_data["range"] = range_dist
    if defense is not None: table_data["defenseBonus"] = defense
    if penalty is not None and penalty != 0: table_data["armorPenalty"] = penalty
    
    summary_parts = [f"{subcategory} - {subtype}"]
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
        "subtype": subtype,
        "proficiency": subtype, # Backward compatibility
        "purpose": purpose or subtype,
        "summary": summary,
        "description": clean_desc,
        "tableData": table_data,
        "sources": [{
            "book": book,
            "page": page,
            "section": f"Equipamentos: {subcategory} ({subtype})",
            "version": version
        }],
        "tags": sorted(list(all_tags))
    }
    
    if is_magic:
        item["isMagicItem"] = True
        item["magicRarity"] = rarity or "Menor"
        
    equipments.append(item)
    return item

print("=== INICIANDO CONSTRUÇÃO LIMPA E CANÔNICA DE EQUIPAMENTOS (3 LIVROS) ===")

book_jda = "Tormenta20 - Jogo do Ano (v1.3)"
book_hda = "Heróis de Arton (v1.1)"
book_ameacas = "Ameaças de Arton (v1.0)"

# =========================================================================================
# 1. LIVRO: TORMENTA20 - EDIÇÃO JOGO DO ANO (v1.3)
# =========================================================================================

# --- 1.1) ARMAS (Tabela 3-3, págs 144-145, Descrições págs 146-150) ---
# Armas Simples
add_item(
    "arma-adaga", "Adaga", "Armas", "Simples", "Corpo a Corpo / Leve",
    "T$ 2", "1d4", "19", "Perfuração", "Curto", None, None, 1,
    book_jda, 146,
    "Esta faca afiada é usada por muitos habitantes adultos do Reinado, embora seja favorita de ladrões e assassinos, por ser facilmente escondida (fornece +5 em testes de Ladinagem para ocultá-la). Quando ataca com uma adaga, você pode usar sua Destreza em vez de Força nos testes de ataque. Uma adaga pode ser arremessada.",
    ["faca", "acuidade", "arremesso", "ladinagem"]
)

add_item(
    "arma-espada-curta", "Espada Curta", "Armas", "Simples", "Corpo a Corpo / Leve",
    "T$ 10", "1d6", "19", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "O tipo mais comum de espada, usada por guardas ou como arma secundária de guerreiros mais capazes. Mede entre 40 e 50cm.",
    ["espada", "leve", "guarda"]
)

add_item(
    "arma-foice", "Foice", "Armas", "Simples", "Corpo a Corpo / Leve",
    "T$ 4", "1d6", "x3", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Originalmente um instrumento agrícola, consiste de uma lâmina curva presa a um cabo de madeira. Uma arma tradicional de druidas.",
    ["druida", "agrícola", "crítico x3", "camponês"]
)

add_item(
    "arma-clava", "Clava", "Armas", "Simples", "Corpo a Corpo / Uma Mão",
    "T$ 0", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_jda, 147,
    "Um pedaço de madeira pesado, como um galho de árvore ou um cabo de vassoura. Por seu preço nulo, é a arma mais comum de camponeses sem recursos.",
    ["madeira", "camponês", "grátis", "rústica"]
)

add_item(
    "arma-lanca", "Lança", "Armas", "Simples", "Corpo a Corpo / Uma Mão",
    "T$ 2", "1d6", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 148,
    "Qualquer arma feita com uma haste de madeira e uma ponta afiada, natural ou metálica. Por sua facilidade de fabricação, é muito comum entre orcs, kobolds, trogloditas e outras raças. Uma lança pode ser arremessada.",
    ["lança", "haste", "arremesso", "primitiva"]
)

add_item(
    "arma-maca", "Maça", "Armas", "Simples", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Bastão com um peso cheio de protuberâncias na ponta, a maça é usada por clérigos que fazem votos de não derramar sangue. De fato, um golpe de maça nem sempre derrama sangue, mas esmaga ossos.",
    ["clérigo", "esmaga ossos", "impacto"]
)

add_item(
    "arma-bordao", "Bordão", "Armas", "Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d6/1d6", "x2", "Impacto", "-", None, None, 2,
    book_jda, 147,
    "Um cajado apreciado por viajantes e camponeses por sua praticidade e fácil acesso (seu preço é zero). O bordão é uma arma dupla.",
    ["dupla", "cajado", "grátis", "viajante"]
)

add_item(
    "arma-pique", "Pique", "Armas", "Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 2", "1d8", "x2", "Perfuração", "-", None, None, 2,
    book_jda, 149,
    "Essencialmente uma lança muito longa. O pique é uma arma alongada.",
    ["alongada", "lança longa", "infantaria"]
)

add_item(
    "arma-tacape", "Tacape", "Armas", "Simples", "Corpo a Corpo / Duas Mãos",
    "T$ 0", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_jda, 150,
    "Versão maior e/ou com pregos de uma clava. Usado por bárbaros e humanoides bestiais, não é uma arma elegante, mas faz o serviço.",
    ["bárbaro", "pesado", "impacto", "grátis"]
)

add_item(
    "arma-azagaia", "Azagaia", "Armas", "Simples", "Ataque à Distância / Uma Mão",
    "T$ 1", "1d6", "x2", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Uma lança leve e flexível própria para arremesso.",
    ["arremesso", "lança leve", "médio alcance"]
)

add_item(
    "arma-besta-leve", "Besta Leve", "Armas", "Simples", "Ataque à Distância / Uma Mão",
    "T$ 35", "1d8", "19", "Perfuração", "Médio", None, None, 1,
    book_jda, 146,
    "Um arco montado sobre uma coronha de madeira com um gatilho. Recarregar uma besta leve é uma ação de movimento.",
    ["disparo", "virote", "recarregar movimento"]
)

add_item(
    "arma-funda", "Funda", "Armas", "Simples", "Ataque à Distância / Uma Mão",
    "T$ 0", "1d4", "x2", "Impacto", "Médio", None, None, 1,
    book_jda, 147,
    "Uma simples tira de couro usada para arremessar pedras polidas. Na falta de munição adequada, pode disparar pedras comuns, mas o dano é reduzido em um passo. Recarregar uma funda é uma ação de movimento. Ao contrário de outras armas de disparo, você aplica sua Força a rolagens de dano com uma funda.",
    ["pedra", "aplica força", "grátis"]
)

add_item(
    "arma-arco-curto", "Arco Curto", "Armas", "Simples", "Ataque à Distância / Duas Mãos",
    "T$ 30", "1d6", "x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 146,
    "Uma arma antiga e comum, este arco é usado primariamente como ferramenta de caça, embora seja usado como arma de guerra por milícias, bandidos e exércitos menos equipados. Pode ser usado montado.",
    ["flecha", "caça", "montado", "crítico x3"]
)

# Armas Marciais
add_item(
    "arma-machadinha", "Machadinha", "Armas", "Marciais", "Corpo a Corpo / Leve",
    "T$ 6", "1d6", "x3", "Corte", "Curto", None, None, 1,
    book_jda, 148,
    "Ferramenta útil para cortar madeira e também inimigos. Uma machadinha pode ser arremessada.",
    ["arremesso", "machado", "crítico x3"]
)

add_item(
    "arma-cimitarra", "Cimitarra", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d6", "18", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Esta espada de lâmina curva e gume único é a arma favorita dos povos do Deserto da Perdição. A cimitarra é uma arma ágil.",
    ["ágil", "crítico 18", "deserto"]
)

add_item(
    "arma-espada-longa", "Espada Longa", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "19", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Arma típica de soldados e guerreiros, esta espada de dois gumes tem lâmina reta medindo entre 80cm e 1m.",
    ["espada", "soldado", "dois gumes"]
)

add_item(
    "arma-florete", "Florete", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 20", "1d6", "18", "Perfuração", "-", None, None, 1,
    book_jda, 147,
    "A lâmina leve e fina desta espada torna a arma muito precisa. O florete é uma arma ágil.",
    ["ágil", "crítico 18", "precisão", "esgrima"]
)

add_item(
    "arma-machado-de-batalha", "Machado de Batalha", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 10", "1d8", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "Adaptado do machado de lenhador, este não é um instrumento para corte de árvores, mas sim uma arma capaz de causar ferimentos terríveis.",
    ["machado", "uma mão", "crítico x3"]
)

add_item(
    "arma-mangual", "Mangual", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d8", "x2", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Uma haste metálica ligada a uma corrente com uma esfera de aço na ponta, que pode se enroscar na arma do adversário. O mangual é uma arma versátil, fornecendo +2 em testes para desarmar.",
    ["versátil", "desarmar +2", "corrente"]
)

add_item(
    "arma-martelo-de-guerra", "Martelo de Guerra", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d8", "x3", "Impacto", "-", None, None, 1,
    book_jda, 148,
    "Outra ferramenta adaptada para combate, esta é a arma favorita de quase todos os anões que não usam machados.",
    ["anão", "crítico x3", "impacto"]
)

add_item(
    "arma-picareta", "Picareta", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 8", "1d6", "x4", "Perfuração", "-", None, None, 1,
    book_jda, 149,
    "Usada por mineradores, esta ferramenta quebra pedras com facilidade. Imagine o que pode fazer com carne e osso!",
    ["crítico x4", "mineração", "perfuração"]
)

add_item(
    "arma-tridente", "Tridente", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d8", "x2", "Perfuração", "Curto", None, None, 1,
    book_jda, 150,
    "Uma lança com três pontas, favorita de povos marinhos e gladiadores e própria para prender as pernas do oponente. O tridente é uma arma versátil, fornecendo +2 em testes para derrubar. Um tridente pode ser arremessado.",
    ["versátil", "derrubar +2", "arremesso", "marinho"]
)

add_item(
    "arma-alabarda", "Alabarda", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d10", "x3", "Corte ou Perfuração", "-", None, None, 2,
    book_jda, 146,
    "Uma haste de madeira com 2m de comprimento e uma lâmina de machado na ponta. A alabarda é uma arma alongada.",
    ["alongada", "haste", "duas mãos", "crítico x3"]
)

add_item(
    "arma-alfange", "Alfange", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 75", "2d4", "18", "Corte", "-", None, None, 2,
    book_jda, 146,
    "Uma versão maior da cimitarra, esta espada de lâmina larga e curva é bastante usada por guerreiros do Deserto da Perdição.",
    ["deserto", "2d4", "crítico 18", "duas mãos"]
)

add_item(
    "arma-gadanho", "Gadanho", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 18", "2d4", "x4", "Corte", "-", None, None, 2,
    book_jda, 147,
    "Outra ferramenta agrícola, o gadanho é uma versão maior da foice, para uso com as duas mãos. Foi criada para ceifar cereais, mas também pode ceifar vidas.",
    ["crítico x4", "2d4", "ceifar", "duas mãos"]
)

add_item(
    "arma-lanca-montada", "Lança Montada", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 10", "1d8", "x3", "Perfuração", "-", None, None, 2,
    book_jda, 148,
    "A lança montada é uma arma alongada. Se você estiver montado, pode usá-la com apenas uma mão. Além disso, quando usada numa investida montada, causa +2d8 pontos de dano.",
    ["alongada", "montaria", "investida +2d8"]
)

add_item(
    "arma-machado-de-guerra", "Machado de Guerra", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "1d12", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Este imenso machado de lâmina dupla é uma arma extremamente perigosa.",
    ["machado", "1d12", "crítico x3", "duas mãos"]
)

add_item(
    "arma-marreta", "Marreta", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "3d4", "x2", "Impacto", "-", None, None, 2,
    book_jda, 149,
    "Uma haste de madeira resistente com uma pesada cabeça de metal ou pedra.",
    ["3d4", "impacto", "pesada", "duas mãos"]
)

add_item(
    "arma-montante", "Montante", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d6", "19", "Corte", "-", None, None, 2,
    book_jda, 150,
    "Enorme e pesada, esta espada de 1,5m de comprimento é uma arma poderosa.",
    ["espada", "2d6", "duas mãos", "crítico 19"]
)

add_item(
    "arma-arco-longo", "Arco Longo", "Armas", "Marciais", "Ataque à Distância / Duas Mãos",
    "T$ 100", "1d8", "x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 146,
    "Este arco reforçado tem a altura de uma pessoa. Ao contrário da versão curta, é primariamente uma arma de guerra. Por ter uma puxada pesada, permite que você aplique sua Força às rolagens de dano (ao contrário de outras armas de disparo).",
    ["flecha", "aplica força", "guerra", "crítico x3"]
)

add_item(
    "arma-besta-pesada", "Besta Pesada", "Armas", "Marciais", "Ataque à Distância / Duas Mãos",
    "T$ 50", "1d12", "19", "Perfuração", "Médio", None, None, 2,
    book_jda, 146,
    "Esta besta é grande e pesada, com uma armação de metal reforçada. Recarregar uma besta pesada é uma ação padrão.",
    ["virote", "1d12", "recarregar padrão", "crítico 19"]
)

# Armas Exóticas
add_item(
    "arma-chicote", "Chicote", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 2", "1d3", "x2", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Uma tira flexível de couro trançado. O chicote é uma arma ágil, alongada e versátil, fornecendo +2 em testes para derrubar ou desarmar. Você pode atacar alvos adjacentes com um chicote sem penalidade.",
    ["ágil", "alongada", "versátil", "derrubar +2", "desarmar +2"]
)

add_item(
    "arma-espada-bastarda", "Espada Bastarda", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 35", "1d10 / 1d12", "19", "Corte", "-", None, None, 1,
    book_jda, 147,
    "Maior e mais pesada que a espada longa, esta arma é tradicionalmente usada pelos cavaleiros de Bielefeld. A espada bastarda é uma arma adaptável. É muito grande para ser usada com uma só mão sem treinamento especial; por isso é uma arma exótica. Ela pode ser usada como uma arma marcial de duas mãos (dano 1d12).",
    ["adaptável", "bielefeld", "uma ou duas mãos"]
)

add_item(
    "arma-katana", "Katana", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 100", "1d8 / 1d10", "19", "Corte", "-", None, None, 1,
    book_jda, 148,
    "A espada tradicional do samurai tem lâmina levemente curva e apenas um gume. A katana é uma arma adaptável e ágil. É muito grande para ser empunhada com uma só mão sem treinamento especial; por isso, é uma arma exótica. Ela pode ser usada como uma arma marcial de duas mãos (dano 1d10).",
    ["adaptável", "ágil", "samurai", "tamu-ra"]
)

add_item(
    "arma-machado-anao", "Machado Anão", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d10", "x3", "Corte", "-", None, None, 1,
    book_jda, 148,
    "A arma preferida de onze entre dez guerreiros anões. Um machado anão é muito grande para ser usado com uma só mão sem treinamento especial; por isso é uma arma exótica. Ele pode ser usado como uma arma marcial de duas mãos.",
    ["anão", "1d10", "crítico x3", "doherimm"]
)

add_item(
    "arma-corrente-de-espinhos", "Corrente de Espinhos", "Armas", "Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 25", "2d4/2d4", "19", "Corte", "-", None, None, 2,
    book_jda, 147,
    "Uma corrente pesada coberta de espinhos afiados. A corrente de espinhos é uma arma ágil, dupla e versátil, fornecendo +2 em testes para derrubar ou desarmar.",
    ["ágil", "dupla", "versátil", "derrubar +2", "desarmar +2"]
)

add_item(
    "arma-machado-taurico", "Machado Táurico", "Armas", "Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 50", "2d8", "x3", "Corte", "-", None, None, 2,
    book_jda, 148,
    "Uma haste comprida com uma lâmina extremamente grossa na ponta, esta é uma arma ancestral dos minotauros. Um machado táurico é uma arma desbalanceada. Além disso, é muito grande para ser usado sem treinamento especial; por isso, é uma arma exótica.",
    ["minotauro", "desbalanceada", "2d8", "crítico x3", "tapista"]
)

add_item(
    "arma-rede", "Rede", "Armas", "Exóticas", "Ataque à Distância / Uma Mão",
    "T$ 20", "-", "-", "-", "Curto", None, None, 1,
    book_jda, 150,
    "A rede tem pequenos dentes em sua trama e uma corda para controlar os inimigos presos. Se você acertar um ataque com a rede, não causa dano. Em vez disso, a vítima fica enredada (deslocamento reduzido à metade, não pode correr nem fazer investidas e sofre -2 na Defesa e em testes de ataque).",
    ["enredar", "corda", "controle", "gladiador"]
)

# Armas de Fogo
add_item(
    "arma-pistola", "Pistola", "Armas", "Armas de Fogo", "Ataque à Distância / Leve",
    "T$ 250", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_jda, 149,
    "A arma de fogo mais comum. Recarregar uma pistola é uma ação padrão (ou de movimento com Saque Rápido).",
    ["fogo", "pólvora", "bala", "crítico 19/x3"]
)

add_item(
    "arma-mosquete", "Mosquete", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos",
    "T$ 500", "2d8", "19/x3", "Perfuração", "Médio", None, None, 2,
    book_jda, 150,
    "Uma arma de fogo de uso difícil, mas com poder devastador. Recarregar um mosquete é uma ação padrão.",
    ["fogo", "pólvora", "2d8", "médio alcance", "crítico 19/x3"]
)

# --- 1.2) MUNIÇÕES (Tabela 3-4, pág 151) ---
add_item(
    "municao-flechas-20", "Flechas (20)", "Munições", "Munições", "Munição de Arco",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 151,
    "Uma aljava com 20 flechas, hastes de madeira com ponta metálica e penas para estabilizar o voo. Recarregar um arco com uma flecha é uma ação livre.",
    ["aljava", "arco", "ação livre"]
)

add_item(
    "municao-virotes-20", "Virotes (20)", "Munições", "Munições", "Munição de Besta",
    "T$ 2", None, None, None, None, None, None, 1,
    book_jda, 151,
    "Uma aljava com 20 setas de madeira com pontas de aço balanceadas para bestas. Recarregar uma besta leve é uma ação de movimento; besta pesada é uma ação padrão.",
    ["besta", "setas", "tiro certeiro"]
)

add_item(
    "municao-pedras-20", "Pedras de Funda (20)", "Munições", "Munições", "Munição de Funda",
    "T$ 0,5", None, None, None, None, None, None, 1,
    book_jda, 151,
    "Um saco de couro com 20 pedras polidas e balanceadas para disparo de funda.",
    ["funda", "pedras polidas"]
)

add_item(
    "municao-balas-e-polvora-20", "Balas de Arma de Fogo (20)", "Munições", "Munições", "Munição de Fogo",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 151,
    "Uma bolsa com 20 balas (pequenas esferas de chumbo fundido) e um polvorinho com pólvora suficiente para 20 disparos.",
    ["pólvora", "chumbo", "tiro"]
)

# --- 1.3) ARMADURAS & ESCUDOS (Tabela 3-5, pág 153, Descrições págs 154-155) ---
add_item(
    "armadura-acolchoada", "Armadura Acolchoada", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 5", None, None, None, None, 1, 0, 1,
    book_jda, 154,
    "Mais que simples roupas, esta armadura é composta por várias camadas de tecido sobrepostas e acolchoadas. É a armadura mais leve e barata disponível.",
    ["tecido", "sem penalidade", "defesa 1"]
)

add_item(
    "armadura-de-couro", "Armadura de Couro", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 20", None, None, None, None, 2, 0, 2,
    book_jda, 154,
    "O peitoral desta armadura é feito de couro curtido em óleo fervente, para ficar mais rígido. As demais partes são feitas de couro flexível.",
    ["couro", "sem penalidade", "defesa 2"]
)

add_item(
    "armadura-couro-batido", "Couro Batido", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 45", None, None, None, None, 3, -1, 2,
    book_jda, 154,
    "Uma versão mais pesada da armadura de couro, reforçada com rebites de metal.",
    ["rebites", "defesa 3", "penalidade -1"]
)

add_item(
    "armadura-gibao-de-peles", "Gibão de Peles", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 15", None, None, None, None, 4, -3, 3,
    book_jda, 154,
    "Usada principalmente por bárbaros e povos selvagens, esta armadura é feita de camadas de pele e couro grossos. É desajeitada, mas oferece boa proteção.",
    ["bárbaro", "peles", "defesa 4", "penalidade -3"]
)

add_item(
    "armadura-couraca", "Couraça", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 500", None, None, None, None, 5, -4, 3,
    book_jda, 154,
    "Composta por uma placa de metal que cobre o peito e as costas e peças flexíveis de couro ou malha para proteger os membros. É a melhor armadura que ainda permite que você aplique sua Destreza na Defesa.",
    ["peitoral de aço", "defesa 5", "penalidade -4"]
)

add_item(
    "armadura-brunea", "Brunea", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 50", None, None, None, None, 5, -2, 5,
    book_jda, 154,
    "Colete de couro coberto com plaquetas de metal sobrepostas, como escamas de um peixe.",
    ["escamas", "defesa 5", "penalidade -2", "pesada"]
)

add_item(
    "armadura-cota-de-malha", "Cota de Malha", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 150", None, None, None, None, 6, -2, 5,
    book_jda, 154,
    "Longa veste de anéis metálicos interligados, formando uma malha flexível que vai até os joelhos. Inclui um capuz de malha.",
    ["anéis", "defesa 6", "penalidade -2", "pesada"]
)

add_item(
    "armadura-loriga-segmentada", "Loriga Segmentada", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 250", None, None, None, None, 7, -3, 5,
    book_jda, 154,
    "Composta por tiras horizontais de metal articuladas sobre tiras de couro, que envolvem o tronco e os ombros.",
    ["tiras de metal", "defesa 7", "penalidade -3", "pesada"]
)

add_item(
    "armadura-meia-armadura", "Meia Armadura", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 600", None, None, None, None, 8, -4, 5,
    book_jda, 154,
    "Uma cota de malha reforçada com placas de metal (peitoral, caneleiras e braçadeiras) que protegem as partes vitais do corpo. Inclui um elmo de aço.",
    ["placas e malha", "defesa 8", "penalidade -4", "pesada"]
)

add_item(
    "armadura-completa", "Armadura Completa", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 3.000", None, None, None, None, 10, -5, 5,
    book_jda, 154,
    "A armadura mais resistente e protetora que existe. É formada por placas de metal moldadas para cobrir o corpo inteiro. Inclui manoplas, botas de couro com placas de metal e um elmo com viseira.",
    ["placas completas", "defesa 10", "penalidade -5", "cavaleiro"]
)

add_item(
    "escudo-leve", "Escudo Leve", "Escudos", "Escudos", "Escudo",
    "T$ 5", None, None, None, None, 1, -1, 1,
    book_jda, 154,
    "Geralmente redondo e feito de madeira, este escudo é preso no antebraço, deixando a mão livre para segurar uma tocha ou outro item (mas não uma arma).",
    ["madeira", "mão livre", "defesa 1"]
)

add_item(
    "escudo-pesado", "Escudo Pesado", "Escudos", "Escudos", "Escudo",
    "T$ 15", None, None, None, None, 2, -2, 2,
    book_jda, 154,
    "Grande e feito de aço ou madeira reforçada com ferro, este escudo é preso ao antebraço e empunhado com a mão, impedindo o uso dessa mão.",
    ["aço", "defesa 2", "penalidade -2"]
)

# --- 1.4) ITENS GERAIS (Tabela 3-6, págs 156-157, Descrições págs 155-163) ---
# Vestuário (INCLUINDO MANOPLA CORRETA PÁG. 159!)
add_item(
    "item-manopla", "Manopla", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Luva metálica que permite socos mais perigosos — o dano de seus ataques desarmados torna-se letal. Uma manopla conta como uma arma para receber melhorias e encantos para usá-los em seus ataques desarmados.",
    ["manopla", "vestuário", "soco letal", "melhoria de arma"]
)

add_item(
    "item-capa", "Capa", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Um manto de tecido leve usado sobre os ombros para proteger contra o vento e poeira.",
    ["capa", "tecido", "viagem"]
)

add_item(
    "item-casaco-de-inverno", "Casaco de Inverno", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 15", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Feito de couro forrado com lã grossa. Fornece +5 em testes de Fortitude contra efeitos de frio extremo.",
    ["frio", "fortitude +5", "inverno"]
)

add_item(
    "item-luva-de-pelica", "Luvas de Pelica", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Luvas de couro fino e macio que mantêm a sensibilidade dos dedos. Fornecem +1 em testes de Ladinagem.",
    ["ladinagem +1", "luvas finas"]
)

add_item(
    "item-manto-camuflado", "Manto Camuflado", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 12", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Um manto camuflado para um tipo específico de terreno (floresta, deserto, etc.). Fornece +2 em Furtividade no terreno escolhido.",
    ["furtividade +2", "camuflagem"]
)

add_item(
    "item-manto-eclesiastico", "Manto Eclesiástico", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Manto adornado com símbolos e cores sagradas de uma divindade. Concede +1 em testes de Religião.",
    ["clérigo", "religião +1", "sagrado"]
)

add_item(
    "item-robe-mistico", "Robe Místico", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Túnica cerimonial usada por arcanistas, com bolsos internos e símbolos arcanos. Concede +1 em testes de Misticismo.",
    ["arcanista", "misticismo +1", "magia"]
)

add_item(
    "item-sapatos-de-camurca", "Sapatos de Camurça", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 8", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Sapatos de sola macia e silenciosa. Fornecem +1 em testes de Furtividade para mover-se em silêncio.",
    ["silêncio", "furtividade +1"]
)

add_item(
    "item-tabardo", "Tabardo", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Sobreveste aberta nas laterais exibindo o brasão de uma ordem de cavalaria, reino ou nobreza. Concede +1 em Diplomacia e Nobreza.",
    ["nobreza", "brasão", "diplomacia +1"]
)

add_item(
    "item-traje-de-gala", "Traje de Gala", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Roupas luxuosas feitas de seda e veludo para frequentar a alta corte. Concede +1 em testes de perícias sociais com nobres.",
    ["nobreza", "corte", "luxo"]
)

add_item(
    "item-traje-de-viajante", "Traje de Viajante", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 159,
    "Roupas resistentes e confortáveis compostas de calças reforçadas, camisa de linho, botas e cinto largo.",
    ["viagem", "conforto", "básico"]
)

# Equipamentos de Aventura
add_item(
    "item-agua-benta", "Água Benta", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Frasco de cerâmica com água purificada e abençoada. Pode ser arremessada em alcance curto contra mortos-vivos ou espíritos, causando 2d6 pontos de dano de luz.",
    ["mortos-vivos", "dano luz 2d6", "abominação"]
)

add_item(
    "item-algemas", "Algemas", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 15", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Par de braceletes de ferro unidos por corrente curta com chave. Escapar exige teste de Acrobacia (CD 25) ou quebrar com Força (CD 28).",
    ["ferro", "prisão", "acrobacia cd 25"]
)

add_item(
    "item-arpeu", "Arpéu", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 5", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Gancho de quatro pontas de ferro preso a uma corda para escalada. Concede +2 em testes de Atletismo para escalar.",
    ["escalada", "gancho", "atletismo +2"]
)

add_item(
    "item-bandoleira-de-pocoes", "Bandoleira de Poções", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 20", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Cinto de couro transpassado no peito que acomoda até 4 poções ou preparados alquímicos, permitindo sacá-los como ação livre.",
    ["poções", "saque livre", "alquimia"]
)

add_item(
    "item-barraca", "Barraca", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Abrigo de lona impermeável para duas pessoas. Dormir numa barraca protege contra intempéries e garante descanso confortável.",
    ["descanso", "acampamento", "abrigo"]
)

add_item(
    "item-corda", "Corda (15m)", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Rolo de corda de cânhamo de 15 metros de extensão com capacidade de suportar até 500kg.",
    ["cânhamo", "escalada", "15m"]
)

add_item(
    "item-espelho", "Espelho de Bolso", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Pequeno espelho de aço polido. Permite espiar ao redor de esquinas sem expor o corpo.",
    ["espelho", "aço polido", "visão angular"]
)

add_item(
    "item-lampiao", "Lampião", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 7", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Lanterna com compartimento para óleo e painéis móveis. Ilumina um raio de 9 metros por 6 horas com um frasco de óleo.",
    ["luz", "iluminação 9m", "óleo"]
)

add_item(
    "item-mochila", "Mochila", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 2", None, None, None, None, None, None, 0,
    book_jda, 157,
    "Bolsa de lona resistente com alças para costas. Aumenta sua capacidade de carga em +2 espaços.",
    ["carga +2", "transporte"]
)

add_item(
    "item-mochila-de-aventureiro", "Mochila de Aventureiro", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 50", None, None, None, None, None, None, 0,
    book_jda, 157,
    "Mochila de couro especial com múltiplos compartimentos e bolsos externos. Aumenta sua capacidade de carga em +5 espaços.",
    ["carga +5", "mochila reforçada"]
)

add_item(
    "item-pe-de-cabra", "Pé de Cabra", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 2", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Barra de ferro curvada que concede +2 em testes de Força para arrombar portas e baús.",
    ["arrombamento", "força +2", "ferro"]
)

add_item(
    "item-pederneira", "Pederneira", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 0,
    book_jda, 157,
    "Pedra e lâmina de aço que produzem faíscas ao serem raspadas. Permite acender fogo como ação padrão.",
    ["fogo", "faísca", "ação padrão"]
)

add_item(
    "item-saco-de-dormir", "Saco de Dormir", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Leito estofado leve e enrolável para descanso ao ar livre.",
    ["descanso", "acampamento"]
)

add_item(
    "item-tocha", "Tocha (4)", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 0,1", None, None, None, None, None, None, 1,
    book_jda, 157,
    "Bastão de madeira embebido em piche que queima por 1 hora, iluminando um raio de 6 metros.",
    ["fogo", "iluminação 6m", "piche"]
)

# Ferramentas
add_item(
    "item-kit-de-alquimia", "Kit de Alquimia", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Tubos de ensaio, almofariz, queimador e reagentes básicos. Permite fabricar itens alquímicos e poções.",
    ["ofício alquimia", "fabricação", "reagentes"]
)

add_item(
    "item-kit-de-culinaria", "Kit de Culinária", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Panelas, frigideira, talheres e temperos de viagem. Permite preparar pratos e refeições nutritivas.",
    ["ofício culinária", "comida", "temperos"]
)

add_item(
    "item-kit-de-disfarce", "Kit de Disfarce", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Maquiagens, perucas, próteses e tecidos variados. Permite realizar testes de Enganação para disfarçar-se.",
    ["disfarce", "enganação", "maquiagem"]
)

add_item(
    "item-kit-de-ladrao", "Kit de Ladrão", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 30", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Gazuas, arames e pequenas ferramentas para destrancar fechaduras e desarmar armadilhas com Ladinagem.",
    ["ladinagem", "gazua", "fechaduras", "armadilhas"]
)

add_item(
    "item-kit-de-medicamentos", "Kit de Medicamentos", "Itens Gerais", "Ferramentas", "Ferramentas",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Bandagens, agulhas, unguentos e ervas medicinais. Permite realizar testes de Cura para primeiros socorros.",
    ["cura", "primeiros socorros", "estabilizar"]
)

# Esotéricos
add_item(
    "esoterico-cajado-arcano", "Cajado Arcano", "Esotéricos", "Esotéricos", "Esotéricos",
    "T$ 100", None, None, None, None, None, None, 2,
    book_jda, 161,
    "Cajado de madeira tratada com foco de cristal no topo. Concede +1 na CD para resistir às suas magias.",
    ["esotérico", "magia", "cd +1", "arcanista"]
)

add_item(
    "esoterico-varinha-arcana", "Varinha Arcana", "Esotéricos", "Esotéricos", "Esotéricos",
    "T$ 50", None, None, None, None, None, None, 1,
    book_jda, 161,
    "Vara fina de madeira especial ou osso entalhado. Suas magias causam +1 ponto de dano por dado de dano.",
    ["esotérico", "magia", "dano +1/dado", "arcanista"]
)

add_item(
    "esoterico-orbe-cristalino", "Orbe Cristalino", "Esotéricos", "Esotéricos", "Esotéricos",
    "T$ 150", None, None, None, None, None, None, 1,
    book_jda, 161,
    "Esfera perfeita de quartzo ou vidro vulcânico. Aumenta o alcance de suas magias em um passo (de curto para médio, etc.).",
    ["esotérico", "alcance ampliado", "orbe"]
)

add_item(
    "esoterico-tomo-hermetico", "Tomo Hermético", "Esotéricos", "Esotéricos", "Esotéricos",
    "T$ 200", None, None, None, None, None, None, 1,
    book_jda, 161,
    "Livro de fórmulas místicas encadernado em couro trabalhado. Concede +1 PM temporário por cena ao lançar magias arcanas.",
    ["esotérico", "livro", "pm extra", "arcanista"]
)

# Alquímicos
add_item(
    "alquimico-acido", "Ácido", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 10", "2d4", "x2", "Ácido", "Curto", None, None, 0.5,
    book_jda, 160,
    "Frasco de cerâmica com líquido corrosivo. Ao ser arremessado, causa 2d4 pontos de dano de ácido na criatura atingida.",
    ["arremesso", "ácido 2d4", "corrosivo"]
)

add_item(
    "alquimico-fogo-alquimico", "Fogo Alquímico", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 10", "1d6", "x2", "Fogo", "Curto", None, None, 0.5,
    book_jda, 160,
    "Frasco com substância gelatinosa que queima em contato com o ar. Causa 1d6 de fogo e deixa o alvo em chamas.",
    ["fogo 1d6", "em chamas", "arremesso"]
)

add_item(
    "alquimico-balsamo-restaurador", "Bálsamo Restaurador", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 5", None, None, None, None, None, None, 0.5,
    book_jda, 160,
    "Pasta vegetal cicatrizante. Aplicar é uma ação padrão e recupera 2d4 pontos de vida.",
    ["cura 2d4", "pasta", "ação padrão"]
)

add_item(
    "alquimico-essencia-de-mana", "Essência de Mana", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 50", None, None, None, None, None, None, 0.5,
    book_jda, 160,
    "Líquido azul brilhante destilado de flores raras. Beber é uma ação padrão e recupera 1d4 pontos de mana.",
    ["mana 1d4", "pm", "poção azul"]
)

# Melhorias & Materiais Especiais (JdA)
add_item(
    "melhoria-afiada", "Afiada", "Melhorias & Materiais", "Melhorias", "Melhoria de Arma",
    "Item Superior", None, None, None, None, None, None, 0,
    book_jda, 165,
    "Aumenta a margem de ameaça da arma em +1. Não cumulativo com efeitos semelhantes.",
    ["margem de ameaça +1", "crítico"]
)

add_item(
    "melhoria-certeira", "Certeira", "Melhorias & Materiais", "Melhorias", "Melhoria de Arma",
    "Item Superior", None, None, None, None, None, None, 0,
    book_jda, 165,
    "Concede +1 em testes de ataque com a arma.",
    ["ataque +1", "precisão"]
)

add_item(
    "melhoria-cruel", "Cruel", "Melhorias & Materiais", "Melhorias", "Melhoria de Arma",
    "Item Superior", None, None, None, None, None, None, 0,
    book_jda, 165,
    "Concede +1 em rolagens de dano com a arma.",
    ["dano +1", "letalidade"]
)

add_item(
    "material-mitral", "Mitral", "Melhorias & Materiais", "Materiais Especiais", "Material Especial",
    "+T$ 1.000", None, None, None, None, None, None, 0,
    book_jda, 166,
    "Metal prateado ultra-leve. Armas aumentam a margem de ameaça em +1. Armaduras e escudos têm sua penalidade reduzida em 2 e o peso reduzido à metade.",
    ["mitral", "leve", "penalidade -2", "crítico +1"]
)

add_item(
    "material-adamante", "Adamante", "Melhorias & Materiais", "Materiais Especiais", "Material Especial",
    "+T$ 1.500", None, None, None, None, None, None, 0,
    book_jda, 166,
    "O metal mais duro de Arton. Armas aumentam o dano em um passo. Armaduras fornecem RD 2 (leves) ou RD 5 (pesadas).",
    ["adamante", "+1 passo dano", "rd 2/5", "dureza"]
)

# Veículos (JdA)
add_item(
    "veiculo-carroca", "Carroça", "Veículos & Capangas", "Veículos", "Veículo Terrestre",
    "T$ 30", None, None, None, None, None, None, 4,
    book_jda, 163,
    "Veículo de duas rodas puxado por um animal de tração com espaço para 200kg de carga.",
    ["transporte", "carga", "tração"]
)

add_item(
    "veiculo-carruagem", "Carruagem", "Veículos & Capangas", "Veículos", "Veículo Terrestre",
    "T$ 200", None, None, None, None, None, None, 8,
    book_jda, 163,
    "Veículo de quatro rodas fechado e estofado, puxado por dois a quatro cavalos com capacidade para quatro passageiros e bagagem.",
    ["transporte nobre", "luxo", "cavalos"]
)

# =========================================================================================
# 2. LIVRO: HERÓIS DE ARTON (v1.1)
# =========================================================================================

# Armas (HDA, Tabela 3-1, págs 218-219, Descrições págs 217-223)
add_item(
    "arma-bastao-ludico", "Bastão Lúdico", "Armas", "Simples", "Corpo a Corpo / Leve",
    "T$ 5", "1d4", "x2", "Impacto", "-", None, None, 1,
    book_hda, 218,
    "Bastão oco recheado de pequenos chocalhos ou sinos, usado por bufões e artistas populares. Fornece +1 em testes de Atuação.",
    ["atuação +1", "bardo", "bufão", "hda"]
)

add_item(
    "arma-besta-de-mao", "Besta de Mão", "Armas", "Simples", "Ataque à Distância / Uma Mão",
    "T$ 50", "1d4", "19", "Perfuração", "Curto", None, None, 1,
    book_hda, 218,
    "Besta minúscula que pode ser disparada e recarregada com apenas uma mão. Uma arma ágil e discreta para espiões.",
    ["disparo", "uma mão", "espião", "hda"]
)

add_item(
    "arma-adaga-oposta", "Adaga Oposta", "Armas", "Marciais", "Corpo a Corpo / Leve",
    "T$ 25", "1d4", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Adaga de guarda curva projetada para combate com duas armas. Fornece +1 na Defesa quando empunhada na mão inábil.",
    ["duas armas", "defesa +1", "parry", "hda"]
)

add_item(
    "arma-agulha-de-ahlen", "Agulha de Ahlen", "Armas", "Marciais", "Corpo a Corpo / Leve",
    "T$ 30", "1d4", "18", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Estilete fino e agudo típico dos nobres envenenadores de Ahlen. Facilmente ocultável e ótimo para aplicar peçonhas.",
    ["estilete", "veneno", "crítico 18", "ahlen"]
)

add_item(
    "arma-cinquedea", "Cinquedea", "Armas", "Marciais", "Corpo a Corpo / Leve",
    "T$ 20", "1d8", "19", "Perfuração/Corte", "-", None, None, 1,
    book_hda, 218,
    "Adaga larga com lâmina da largura de cinco dedos. Causa dano comparável a uma espada mantendo o tamanho compacto.",
    ["larga", "1d8 dano", "cinco dedos", "hda"]
)

add_item(
    "arma-espadim", "Espadim", "Armas", "Marciais", "Corpo a Corpo / Leve",
    "T$ 15", "1d6", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Espada curta e elegante com ponta reforçada para estocada rápida. Arma ágil.",
    ["ágil", "estocada", "leve", "hda"]
)

add_item(
    "arma-machado-de-haste", "Machado de Haste", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 15", "1d10", "x3", "Corte", "-", None, None, 2,
    book_hda, 218,
    "Lâmina pesada de machado montada em cabo longo de 1,8m. Arma alongada.",
    ["alongada", "machado", "crítico x3", "hda"]
)

add_item(
    "arma-martelo-longo", "Martelo Longo", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 15", "1d10", "x3", "Impacto", "-", None, None, 2,
    book_hda, 218,
    "Haste longa encimada por cabeça cilíndrica maciça de aço. Arma alongada de impacto.",
    ["alongada", "impacto", "crítico x3", "hda"]
)

add_item(
    "arma-chicote-faropado", "Chicote Faropado", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 15", "1d6", "x2", "Corte", "-", None, None, 1,
    book_hda, 218,
    "Chicote grosso trançado com lascas de ferro e cacos afiados ao longo das tiras.",
    ["chicote", "farpas", "hda"]
)

add_item(
    "arma-desmontador", "Desmontador", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 25", "1d6", "x3", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Arma com ganchos opostos criada para derrubar cavaleiros de suas montarias com facilidade.",
    ["anti-montaria", "derrubar +2", "ganchos", "hda"]
)

add_item(
    "arma-estocada-dupla", "Estocada Dupla", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 35", "1d6/1d6", "19", "Perfuração", "-", None, None, 1,
    book_hda, 218,
    "Lâmina bifurcada que permite aplicar dois golpes de estocada num único movimento.",
    ["bifurcada", "estocada", "crítico 19", "hda"]
)

add_item(
    "arma-khopesh", "Khopesh", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d8", "19", "Corte", "-", None, None, 1,
    book_hda, 218,
    "Lâmina curvada em foice tradicional dos faraós do Deserto da Perdição. Arma versátil (+2 em manobras).",
    ["deserto", "versátil", "foice", "hda"]
)

# Armaduras & Escudos (HDA, Tabela 3-3, pág 224, Descrições págs 223-226)
add_item(
    "armadura-sensual", "Armadura Sensual", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 100", None, None, None, None, 1, 0, 1,
    book_hda, 224,
    "Traje ousado e revelador feito de tiras de couro e joias. Concede +2 em testes de Diplomacia e Enganação com alvos atraídos pelo usuário.",
    ["sensual", "diplomacia +2", "enganação +2", "defesa 1"]
)

add_item(
    "armadura-de-folhas", "Armadura de Folhas", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 120", None, None, None, None, 2, 0, 1,
    book_hda, 224,
    "Tecido leve coberto por camadas de folhas tratadas com óleos naturais. Se treinado em Sobrevivência, concede +2 PM após 1 dia de uso.",
    ["druida", "pm +2", "sobrevivência", "natureza"]
)

add_item(
    "armadura-de-engenhoqueiro-goblin", "Armadura de Engenhoqueiro Goblin", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 150", None, None, None, None, 3, -2, 2,
    book_hda, 224,
    "Armadura enjambrada de couro, placas soltas e dezenas de bolsos. Permite carregar até +2 espaços em itens pequenos e não aplica penalidade em testes de Ofício (Engenhoqueiro).",
    ["inventor", "engenhoqueiro", "bolsos", "goblin"]
)

add_item(
    "armadura-cota-de-moedas", "Cota de Moedas", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 400", None, None, None, None, 4, -2, 2,
    book_hda, 224,
    "Armadura forjada costurando moedas de prata e ouro sobrepostas. Pode ter moedas gastas em emergências (até T$ 100).",
    ["moedas", "ouro", "luxo", "nobre"]
)

add_item(
    "armadura-colete-fora-da-lei", "Colete Fora da Lei", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 250", None, None, None, None, 3, -1, 2,
    book_hda, 224,
    "Colete de couro endurecido com coldres ocultos. Permite sacar armas de fogo ou adagas como ação livre.",
    ["pistoleiro", "saque rápido", "fogo", "smokestone"]
)

add_item(
    "armadura-brigantina", "Brigantina", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 350", None, None, None, None, 7, -3, 4,
    book_hda, 224,
    "Placas de aço rebitadas por dentro de uma resistente capa de veludo ou couro. Oferece proteção de cota de malha pesada com melhor mobilidade.",
    ["brigantina", "rebitada", "pesada", "defesa 7"]
)

add_item(
    "armadura-de-chumbo", "Armadura de Chumbo", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 800", None, None, None, None, 8, -5, 6,
    book_hda, 224,
    "Armadura maciça revestida de chumbo denso. Fornece Redução de Dano 2/mundano e +2 em testes de resistência contra magias.",
    ["chumbo", "rd 2", "resistência magia +2", "pesada"]
)

add_item(
    "armadura-de-justa", "Armadura de Justa", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 1.000", None, None, None, None, 9, -5, 5,
    book_hda, 224,
    "Meia armadura reforçada com placas assimétricas para torneios de cavalaria. Concede +5 em testes para resistir a manobra derrubar.",
    ["justa", "cavalaria", "derrubar +5", "torneio"]
)

add_item(
    "armadura-de-hussardo-alado", "Armadura de Hussardo Alado", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 4.000", None, None, None, None, 10, -5, 5,
    book_hda, 224,
    "Armadura completa imponente com duas asas plumadas nas costas. Em investida montada, permite fazer teste de Intimidação gratuito para assustar o oponente.",
    ["hussardo", "asas", "investida", "intimidação"]
)

add_item(
    "armadura-de-pedra", "Armadura de Pedra", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 500", None, None, None, None, 8, -5, 6,
    book_hda, 224,
    "Esculpida em placas maciças de granito de Doherimm. Concede Redução de Dano 2/impacto.",
    ["pedra", "granito", "anão", "doherimm", "rd 2 impacto"]
)

add_item(
    "escudo-broquel", "Broquel", "Escudos", "Escudos", "Escudo",
    "T$ 10", None, None, None, None, 1, 0, 1,
    book_hda, 224,
    "Pequeno escudo de aço preso ao punho. Não impõe penalidade de armadura e permite empunhar armas de arremesso com a mesma mão.",
    ["broquel", "sem penalidade", "ágil", "defesa 1"]
)

add_item(
    "escudo-de-vime", "Escudo de Vime", "Escudos", "Escudos", "Escudo",
    "T$ 2", None, None, None, None, 1, 0, 1,
    book_hda, 224,
    "Trançado com fibras vegetais leves. É extremamente barato e não impõe penalidade de armadura.",
    ["vime", "leve", "barato", "defesa 1"]
)

add_item(
    "escudo-torre", "Escudo Torre", "Escudos", "Escudos", "Escudo",
    "T$ 50", None, None, None, None, 3, -3, 3,
    book_hda, 224,
    "Escudo retangular colossal que cobre o corpo inteiro. Permite gastar uma ação padrão para receber cobertura total até sua próxima rodada.",
    ["torre", "cobertura total", "defesa 3", "maciço"]
)

add_item(
    "escudo-sagna", "Escudo Sagna", "Escudos", "Escudos", "Escudo",
    "T$ 35", None, None, None, None, 2, -1, 2,
    book_hda, 224,
    "Escudo com reentrâncias para apoiar lanças e armas de haste em formação de infantaria.",
    ["sagna", "haste", "defesa 2", "infantaria"]
)

# Itens Gerais & Aventura (HDA)
add_item(
    "item-abaco", "Ábaco", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 10", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Instrumento de cálculo com contas em hastes de metal. Fornece +1 em testes de Ofício (Comércio, Administrador) e Jogatina.",
    ["cálculo", "comércio", "ofício +1"]
)

add_item(
    "item-ampulheta", "Ampulheta", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 25", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Dispositivo de vidro com areia calibrada para medir intervalos de tempo precisos de 1 hora.",
    ["tempo", "hora", "medição"]
)

add_item(
    "item-asas-do-texugo", "Asas do Texugo", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 200", None, None, None, None, None, None, 2,
    book_hda, 227,
    "Mochila com asas retráteis de kobold e manivelas. Com um salto de Atletismo (CD 15), concede deslocamento de voo 12m por 1 ou mais rodadas.",
    ["voo 12m", "kobold", "asas", "engenhoqueiro"]
)

add_item(
    "item-astrolabio", "Astrolábio", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 90", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Instrumento de navegação estelar. Permite usar Conhecimento no lugar de Sobrevivência para orientar-se.",
    ["navegação", "estrelas", "conhecimento"]
)

add_item(
    "item-bainha-adornada", "Bainha Adornada", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 100", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Coberta de fios de ouro e gemas, permite portar armas em bailes e festas da corte sem chamar atenção.",
    ["corte", "ouro", "disfarce armado"]
)

add_item(
    "item-bussola", "Bússola", "Itens Gerais", "Aventura", "Equipamento de Aventura",
    "T$ 45", None, None, None, None, None, None, 1,
    book_hda, 227,
    "Instrumento magnético com agulha imantada. Ao fazer testes de Sobrevivência para orientar-se, rola dois dados e usa o melhor.",
    ["ímã", "norte", "sobrevivência vantagem"]
)

# Capangas & Veículos (HDA)
add_item(
    "capanga-guarda-costas", "Guarda-Costas", "Veículos & Capangas", "Capangas", "Seguidor / Proteção",
    "T$ 50/mês", None, None, None, None, None, None, 0,
    book_hda, 240,
    "Um mercenário veterano contratado para interpor seu escudo em sua defesa. Uma vez por rodada, concede +2 na Defesa contra um ataque direcionado a você.",
    ["mercenário", "defesa +2", "aliado", "contrato"]
)

add_item(
    "capanga-batedor", "Batedor", "Veículos & Capangas", "Capangas", "Seguidor / Exploração",
    "T$ 40/mês", None, None, None, None, None, None, 0,
    book_hda, 240,
    "Um rastreador experiente contratado para explorar passagens secretas e detectar emboscadas com antecedência. Fornece +2 em Percepção e Sobrevivência do grupo.",
    ["rastreador", "percepção +2", "explorador"]
)

add_item(
    "veiculo-carruagem-blindada", "Carruagem Blindada", "Veículos & Capangas", "Veículos", "Veículo Terrestre",
    "T$ 500", None, None, None, None, None, None, 10,
    book_hda, 241,
    "Uma carruagem pesada reforçada com placas de metal nas laterais e seteiras para disparo seguro de bestas e armas de fogo.",
    ["transporte", "blindagem", "cavalos", "cobertura"]
)

add_item(
    "veiculo-balao-goblin", "Balão Goblin", "Veículos & Capangas", "Veículos", "Veículo Aéreo",
    "T$ 1.000", None, None, None, None, None, None, 20,
    book_hda, 242,
    "Um balão de ar quente sustentado por um cesto de vime reforçado com caldeira de óleo pressurizado. Permite sobrevoar terrenos intransponíveis a 12m de altitude.",
    ["vôo", "goblin", "aéreo", "ar quente"]
)

# =========================================================================================
# 3. LIVRO: AMEAÇAS DE ARTON (v1.0 - Bazar Monstruoso)
# =========================================================================================

# Armas (Ameaças, Tabela 3-1, pág 394)
add_item(
    "arma-porrete", "Porrete", "Armas", "Simples", "Corpo a Corpo / Leve",
    "T$ 2", "1d6", "x2", "Impacto", "-", None, None, 1,
    book_ameacas, 394,
    "Pedaço pesado de madeira maciça ou osso bruto com empunhadura entalhada. Uma arma rústica e barata, comum entre tribos e bandidos.",
    ["simples", "leve", "madeira", "porrete", "bazar monstruoso"]
)

add_item(
    "arma-zarabatana", "Zarabatana", "Armas", "Simples", "Ataque à Distância / Uma Mão",
    "T$ 5", "1d3", "x2", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Pequeno tubo oco usado para disparar dardos. Causa dano mínimo, mas é excelente para inocular venenos; a CD para resistir ao veneno dos dardos aumenta em +2. Um pacote de munição contém 20 dardos, custa T$ 2 e ocupa 0,5 espaço.",
    ["zarabatana", "veneno +2 cd", "dardos", "silenciosa"]
)

add_item(
    "arma-neko-te", "Neko-te", "Armas", "Marciais", "Corpo a Corpo / Leve",
    "T$ 10", "1d4", "19", "Corte", "-", None, None, 1,
    book_ameacas, 394,
    "Luva com garras metálicas afiadas nas pontas dos dedos, desenvolvida em Tamu-ra para assassinato furtivo. Conta como arma ágil. Se você tiver a habilidade Ataque Furtivo, o dado extra de dano aumenta em +1d6.",
    ["tamu-ra", "garras", "ninja", "ataque furtivo +1d6", "ágil"]
)

add_item(
    "arma-gladio", "Gládio", "Armas", "Marciais", "Corpo a Corpo / Uma Mão",
    "T$ 12", "1d6", "19/x3", "Perfuração", "-", None, None, 1,
    book_ameacas, 394,
    "Espada curta de lâmina reta e ponta aguçada com gume duplo reforçado, tradicional entre legiões e infantaria pesada. Muito eficaz para estocadas em formação de escudo cerrado.",
    ["gládio", "legião", "estocada", "crítico 19/x3", "uma mão"]
)

add_item(
    "arma-tetsubo", "Tetsubo", "Armas", "Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "1d10", "x2", "Impacto", "-", None, None, 2,
    book_ameacas, 394,
    "Uma versão mais pesada e sofisticada do tacape, geralmente reforçado com anéis e cravos metálicos. Ao realizar manobras derrubar ou quebrar com um tetsubo, você recebe +2 no teste de manobra.",
    ["tetsubo", "duas mãos", "impacto", "manobra derrubar +2", "quebrar +2"]
)

add_item(
    "arma-traque", "Traque", "Armas", "Armas de Fogo", "Ataque à Distância / Leve",
    "T$ 75", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Uma pistola rústica e curta feita com cano reforçado improvisado por armeiros goblins. Quando rola um 1 natural no ataque, ela é avariada. Recarregá-la é uma ação padrão.",
    ["fogo", "leve", "goblin", "curto alcance", "crítico 19/x3"]
)

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

add_item(
    "arma-acoite-finntroll", "Açoite Finntroll", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d8", "x2", "Corte", "-", None, None, 1,
    book_ameacas, 394,
    "Feito de tiras de couro com farpas de aço e espinhos venenosos nas pontas, é também um instrumento de tortura. Fornece +2 em testes de Intimidação e manobras desarmar.",
    ["finntroll", "chicote", "farpas", "intimidação +2", "desarmar +2"]
)

add_item(
    "arma-espada-vespa", "Espada Vespa", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 75", "2d4", "18", "Corte ou Perfuração", "-", None, None, 1,
    book_ameacas, 394,
    "Esta arma estranha é feita com três ferrões de vespas gigantes presos a uma empunhadura articulada. Ao acertar um ataque com a espada vespa, você pode gastar 1 PM para deixar o alvo sangrando.",
    ["vespa gigante", "ferrões", "sangramento", "crítico 18"]
)

add_item(
    "arma-pistola-punhal", "Pistola-Punhal", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 300", "1d4 / 2d6", "19/x3", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Esta arma é formada por uma lâmina pontiaguda com um mecanismo acoplado que permite disparar uma bala de arma de fogo. É uma arma híbrida: pode ser usada para ataques corpo a corpo (1d4, 19) ou disparos à distância (2d6, 19/x3, alcance curto).",
    ["híbrida", "pistola", "punhal", "fogo e lâmina"]
)

add_item(
    "arma-mordida-do-diabo", "Mordida do Diabo", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 30", "1d4", "x2", "Perfuração", "-", None, None, 1,
    book_ameacas, 394,
    "Garra mecânica dentada inspirada em armadilhas para ursos. Quando acerta um ataque, você pode iniciar uma manobra agarrar como ação livre com +2 no teste.",
    ["armadilha", "dentes", "agarrar livre", "manobra +2"]
)

add_item(
    "arma-presa-de-serpente", "Presa de Serpente", "Armas", "Exóticas", "Corpo a Corpo / Uma Mão",
    "T$ 1.000", "1d8", "17", "Corte", "-", None, None, 1,
    book_ameacas, 394,
    "Lâmina esguia e ondulada forjada em cerâmica verde ou presa de naga fossilizada. Possui uma margem de ameaça formidável (crítico 17-20).",
    ["naga", "ondulada", "crítico 17", "afiada"]
)

add_item(
    "arma-lanca-de-fogo", "Lança de Fogo", "Armas", "Exóticas", "Corpo a Corpo / Duas Mãos",
    "T$ 1.000", "1d8 / 4d6", "x3 / 19/x3", "Perfuração", "Especial", None, None, 2,
    book_ameacas, 394,
    "Esta arma é formada por um longo cano com uma coronha de madeira e uma ponta de lança metálica. Arma híbrida: funciona como lança corpo a corpo (1d8, x3) ou bacamarte de disparo em cone (4d6 de fogo/perfuração).",
    ["lança de fogo", "híbrida", "cone de fogo", "duas mãos"]
)

add_item(
    "arma-shuriken", "Shuriken", "Armas", "Exóticas", "Ataque à Distância / Leve",
    "T$ 1", "1d4", "x2", "Perfuração", "Curto", None, None, 0.5,
    book_ameacas, 394,
    "Pequenos projéteis metálicos para arremesso, em forma de estrelas ou dardos. Uma vez por rodada, quando ataca com uma shuriken, você pode gastar 1 PM para fazer um ataque adicional de shuriken contra o mesmo alvo.",
    ["shuriken", "arremesso", "ninja", "ataque extra", "leve"]
)

add_item(
    "arma-arpao", "Arpão", "Armas", "Exóticas", "Ataque à Distância / Uma Mão",
    "T$ 30", "1d10", "x3", "Perfuração", "Curto", None, None, 1,
    book_ameacas, 394,
    "Instrumento de pesca costeira convertido em arma militar, esta haste tem farpas na extremidade e vem presa a uma corda de 10m. Se acertar o ataque, você pode puxar o alvo ou prendê-lo.",
    ["arpão", "pesca", "corda", "puxar", "farpas"]
)

# Armaduras & Escudos (Ameaças, Tabela 3-2, pág 395)
add_item(
    "armadura-de-ossos", "Armadura de Ossos", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 120", None, None, None, None, 3, -2, 2,
    book_ameacas, 395,
    "Os nezumi e outros povos são conhecidos por produzir estas armaduras sinistras. Combinando um aspecto assustador e energias negativas de ossadas, esta armadura fornece +1 em Intimidação e na CD de seus efeitos de medo (cumulativo com a melhoria macabra).",
    ["nezumi", "ossos", "intimidação +1", "medo cd +1", "defesa 3"]
)

add_item(
    "armadura-veste-de-teia-de-aranha", "Veste de Teia de Aranha", "Armaduras", "Armaduras Leves", "Armadura Leve",
    "T$ 3.000", None, None, None, None, 4, 0, 2,
    book_ameacas, 395,
    "Feita com teia de aranha gigante, esta veste é cinza-escura, maleável e silenciosa, mas também forte como aço. Fornece +5 em Furtividade, mas não pode receber a melhoria material especial.",
    ["teia gigante", "furtividade +5", "penalidade zero", "defesa 4"]
)

add_item(
    "armadura-de-quitina", "Armadura de Quitina", "Armaduras", "Armaduras Pesadas", "Armadura Pesada",
    "T$ 350", None, None, None, None, 7, -3, 5,
    book_ameacas, 395,
    "Feita com carapaças selecionadas de grandes insetos, esta armadura dos povos-trovão é mais leve que suas contrapartes metálicas. Embora seja uma armadura pesada, não reduz o deslocamento do usuário.",
    ["quitina", "povo-trovão", "deslocamento normal", "defesa 7"]
)

add_item(
    "armadura-escudo-de-couro", "Escudo de Couro", "Escudos", "Escudos", "Escudo",
    "T$ 3", None, None, None, None, 1, -1, 1,
    book_ameacas, 395,
    "Por sua leveza, este escudo é popular entre velocis e ubaneri. É feito com uma armação de madeira esticando uma membrana de couro flexível e amarrado ao braço. Contra ataques à distância, o bônus na Defesa do escudo aumenta em +2.",
    ["couro", "velocis", "defesa contra disparo +2", "defesa 1"]
)

# Itens Gerais (Ameaças, Tabela 3-3, pág 398)
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

# Animais
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

# Alquímicos (Ameaças)
add_item(
    "alquimico-balsamo-de-drogadora", "Bálsamo de Drogadora", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 60", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Produzido por curandeiras dos povos-trovão, este unguento aplicado como ação padrão restaura 3d6+3 pontos de vida e remove a condição sangrando.",
    ["cura 3d6+3", "sangrando", "povo-trovão", "preparado"]
)

add_item(
    "alquimico-bomba-de-fumaca", "Bomba de Fumaça", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 15", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Saco de estopa com pólvora especial. Ao ser arremessado em alcance curto, cria uma nuvem de fumaça espessa de 3m de raio que concede camuflagem total por 2 rodadas.",
    ["fumaça", "camuflagem total", "arremesso", "ninja"]
)

add_item(
    "alquimico-elixir-quimerico", "Elixir Quimérico", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 120", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Beber este elixir é uma ação padrão; até o fim da cena você ganha uma arma natural de mordida (1d6 corte) ou chifres (1d6 perfuração).",
    ["mutação", "arma natural", "quimera", "elixir"]
)

add_item(
    "alquimico-eter-elemental", "Éter Elemental", "Alquímicos", "Preparados", "Alquímicos",
    "T$ 60", None, None, None, None, None, None, 0.5,
    book_ameacas, 396,
    "Frasco com essência pura dos planos elementais. Ao ser aplicado em uma arma como ação de movimento, adiciona +1d6 de dano de fogo, frio, eletricidade ou ácido por 3 rodadas.",
    ["elemental", "dano extra 1d6", "óleo de arma"]
)

add_item(
    "alquimico-corrosivo-mineral", "Corrosivo Mineral", "Alquímicos", "Catalisadores", "Alquímicos",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Pasta mineral corrosiva natural. Ao lançar magias de ácido, adiciona +1 ponto de dano por dado e corrói 1 ponto de Defesa da armadura do alvo por 1 rodada.",
    ["catalisador", "ácido", "corrosão", "dano +1/dado"]
)

add_item(
    "alquimico-gelo-extremo", "Gelo Extremo", "Alquímicos", "Catalisadores", "Alquímicos",
    "T$ 150", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Cristais que eliminam calor ambiente. Aumenta os dados de dano de frio de suas magias em um passo (de d6 para d8, etc.).",
    ["catalisador", "frio", "aumento de passo de dano"]
)

add_item(
    "alquimico-esporos-de-cogumelo", "Esporos de Cogumelo", "Alquímicos", "Venenos", "Alquímicos",
    "T$ 75", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Inalado. O alvo sofre 1d6 de dano de veneno e fica confuso por 1d4 rodadas (Fortitude CD 15 reduz para 1 rodada).",
    ["veneno", "inalado", "confuso", "cd 15"]
)

add_item(
    "alquimico-peconha-ancia", "Peçonha Anciã", "Alquímicos", "Venenos", "Alquímicos",
    "T$ 1.800", None, None, None, None, None, None, 0.5,
    book_ameacas, 397,
    "Veneno lendário extraído de serpes anciãs e hidras. Causa 4d12 de dano de veneno e deixa o alvo fraco e debilitado (Fortitude CD 25 reduz à metade).",
    ["veneno lendário", "4d12", "debilitado", "cd 25"]
)

# Melhorias & Materiais (Ameaças)
add_item(
    "melhoria-multifuncional", "Multifuncional", "Melhorias & Materiais", "Melhorias", "Melhoria de Equipamento",
    "Item Superior", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "Esta melhoria só pode ser aplicada em um item que modifica uma perícia. Escolha outra perícia que usa o mesmo atributo-chave; o item passa a funcionar também para a segunda perícia.",
    ["melhoria", "perícias", "versatilidade", "bazar monstruoso"]
)

add_item(
    "melhoria-penetrante", "Penetrante", "Melhorias & Materiais", "Melhorias", "Melhoria de Arma",
    "Item Superior", None, None, None, None, None, None, 0,
    book_ameacas, 399,
    "A arma ignora 5 pontos da redução de dano do alvo. Pré-requisito: cruel.",
    ["melhoria", "arma", "ignora rd 5", "penetrante", "cruel"]
)

add_item(
    "material-casco-de-monstro", "Casco de Monstro", "Melhorias & Materiais", "Materiais Especiais", "Material Especial",
    "+T$ 750 (Arma/Leve/Escudo) | +T$ 6.000 (Pesada/Esotérico)", None, None, None, None, 1, None, 0,
    book_ameacas, 400,
    "Os cascos protetores de monstros substituem aço. Arma: conta como primitiva para magias como Armamento da Natureza. Armadura/Escudo: penalidade diminui em 1 (armaduras pesadas permitem aplicar 1 ponto de Destreza na Defesa). Esotérico: concede RD 5 contra o próximo dano após lançar magia.",
    ["casco", "quelônio", "destreza armadura pesada", "penalidade -1", "rd 5"]
)

add_item(
    "material-lanajuste", "Lanajuste", "Melhorias & Materiais", "Materiais Especiais", "Material Especial",
    "+T$ 600 (Arma) | +T$ 1.500 (Leve/Escudo) | +T$ 3.000 (Pesada/Esotérico)", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Também chamado de coral-de-ferro de Khubar. Arma: ataques ignoram penalidades de combate submerso e não violam restrições de devotos do Oceano. Armadura/Escudo: fornece redução de corte 5 (leves/escudos) ou 10 (pesadas). Esotérico: rola novamente resultados 1 no dano de magias de corte.",
    ["coral de ferro", "khubar", "combate submerso", "oceano", "redução corte 5/10"]
)

add_item(
    "material-prata", "Prata", "Melhorias & Materiais", "Materiais Especiais", "Material Especial",
    "+T$ 600 (Arma) | +T$ 1.500 (Leve/Escudo) | +T$ 3.000 (Pesada) | +T$ 400 (Esotérico)", None, None, None, None, None, None, 0,
    book_ameacas, 400,
    "Arma: causa +2 pontos de dano em espíritos e mortos-vivos e é considerada mágica contra eles. Armadura/Escudo: fornece RD 5 (leves/escudos) ou RD 10 (pesadas) contra dano de espíritos e mortos-vivos. Pode ser combinada com outro material especial.",
    ["prata", "mortos-vivos", "espíritos", "rd 5/10", "arma mágica"]
)

print(f"Total de equipamentos canônicos limpos catalogados: {len(equipments)}")

with open("data/categories/equipamentos.json", "w", encoding="utf-8") as f:
    json.dump(equipments, f, ensure_ascii=False, indent=2)

print("data/categories/equipamentos.json gerado com sucesso!")
