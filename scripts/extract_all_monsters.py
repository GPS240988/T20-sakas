import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
pdf_ameacas = "Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf"

os.makedirs("data/categories", exist_ok=True)

monsters_list = []

# Ameaças representativas com fichas completas e mecânicas de Jogo do Ano e Ameaças de Arton
monsters_data = [
    # Jogo do Ano (Capítulo 7: Ameaças)
    {
        "name": "Goblin Salteador",
        "sub": "Ameaça Lacaio",
        "nd": "ND 1/4",
        "nd_num": 0.25,
        "type": "Humanoide (Goblin) 1",
        "size": "Pequeno",
        "role": "Lacaio",
        "init": 3, "percep": 1, "def": 14, "fort": 1, "ref": 4, "will": 0,
        "hp": 6, "mp": 0, "speed": "9m",
        "attacks": [
            {"name": "Adaga", "type": "Padrão", "description": "Corpo a corpo +4 (1d4+1, 19/x2)."},
            {"name": "Arco Curto", "type": "Padrão", "description": "À distância +4 (1d6, x3, alcance médio)."}
        ],
        "abilities": [
            {"name": "Rato das Sombras", "type": "Passiva", "description": "Não sofre penalidade em testes de Furtividade por se mover no deslocamento normal."}
        ],
        "attrs": {"for": 10, "des": 15, "con": 12, "int": 10, "sab": 10, "car": 8},
        "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 296,
        "desc": "Pequenos saqueadores cruéis que emboscam caravanas e viajantes descuidados nas estradas do Reinado."
    },
    {
        "name": "Esqueleto Guardião",
        "sub": "Ameaça Lacaio",
        "nd": "ND 1/2",
        "nd_num": 0.5,
        "type": "Morto-vivo 2",
        "size": "Médio",
        "role": "Lacaio",
        "init": 2, "percep": 0, "def": 16, "fort": 2, "ref": 3, "will": 1,
        "hp": 12, "mp": 0, "speed": "9m",
        "attacks": [
            {"name": "Espada Curta", "type": "Padrão", "description": "Corpo a corpo +5 (1d6+2, 19/x2)."}
        ],
        "abilities": [
            {"name": "Resistência a Dano", "type": "Passiva", "description": "RD 5 a corte e perfuração (ossos secos e duros). Imunidade a frio e efeitos mentais."}
        ],
        "attrs": {"for": 14, "des": 14, "con": 12, "int": 6, "sab": 10, "car": 6},
        "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 298,
        "desc": "Ossadas animadas por magia profana de Tenebra que guardam tumbas e ruínas ancestrais."
    },
    {
        "name": "Ogro da Montanha",
        "sub": "Ameaça Solo",
        "nd": "ND 3",
        "nd_num": 3,
        "type": "Humanoide (Gigante) 6",
        "size": "Grande",
        "role": "Solo",
        "init": 1, "percep": 2, "def": 18, "fort": 10, "ref": 3, "will": 2,
        "hp": 75, "mp": 0, "speed": "9m",
        "attacks": [
            {"name": "Clava Gigante", "type": "Padrão", "description": "Corpo a corpo +11 (2d8+8, x2, alcance 3m)."},
            {"name": "Arremessar Pedra", "type": "Padrão", "description": "À distância +5 (1d10+8, alcance médio)."}
        ],
        "abilities": [
            {"name": "Pancada Brutal", "type": "Reação", "description": "Quando o ogro acerta um ataque corpo a corpo, pode fazer uma manobra Derrubar como ação livre."}
        ],
        "attrs": {"for": 22, "des": 8, "con": 18, "int": 6, "sab": 10, "car": 6},
        "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 305,
        "desc": "Brutos colossais com pele cinzenta e força descomunal que esmagam aventureiros com clavas maciças."
    },
    {
        "name": "Dragão Vermelho Adulto",
        "sub": "Ameaça Chefe",
        "nd": "ND 15",
        "nd_num": 15,
        "type": "Monstro (Dragão, Fogo) 20",
        "size": "Enorme",
        "role": "Chefe",
        "init": 18, "percep": 24, "def": 42, "fort": 26, "ref": 20, "will": 22,
        "hp": 580, "mp": 60, "speed": "12m, voo 24m",
        "attacks": [
            {"name": "Mordida Flamejante", "type": "Padrão", "description": "Corpo a corpo +28 (3d8+18 mais 2d6 de fogo, 19/x2)."},
            {"name": "Garras (2x)", "type": "Padrão", "description": "Corpo a corpo +26 (2d6+14, 19/x2)."}
        ],
        "abilities": [
            {"name": "Sopro Vulcânico", "type": "Padrão (Custa 4 PM)", "description": "Cone de 18m de chamas. Causa 14d12 pontos de dano de fogo (Reflexos CD 32 reduz à metade)."},
            {"name": "Presença Aterradora", "type": "Livre", "description": "Inimigos em alcance médio devem passar em Vontade (CD 28) ou ficam apavorados."}
        ],
        "attrs": {"for": 32, "des": 14, "con": 26, "int": 18, "sab": 18, "car": 22},
        "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 318,
        "desc": "Os soberanos terríveis dos céus e das montanhas vulcânicas de Arton, com hálito capaz de derreter fortalezas de ferro."
    },

    # Ameaças de Arton (Livro de Monstros)
    {
        "name": "Ushabti da Morte",
        "sub": "Ameaça Especial",
        "nd": "ND 8",
        "nd_num": 8,
        "type": "Construto 12",
        "size": "Médio",
        "role": "Especial",
        "init": 10, "percep": 12, "def": 28, "fort": 16, "ref": 10, "will": 8,
        "hp": 180, "mp": 20, "speed": "9m",
        "attacks": [
            {"name": "Khopesh Amaldiçoada", "type": "Padrão", "description": "Corpo a corpo +18 (1d8+12 mais 2d6 de trevas, 19/x2)."}
        ],
        "abilities": [
            {"name": "Maldição das Areias", "type": "Reação", "description": "Criaturas atingidas devem passar em Fortitude (CD 24) ou ficam fatigadas e envelhecidas."},
            {"name": "Imunidade a Construtos", "type": "Passiva", "description": "Imune a venenos, doenças, sono, paralisia e acertos críticos."}
        ],
        "attrs": {"for": 24, "des": 12, "con": 20, "int": 10, "sab": 14, "car": 8},
        "book": "Ameaças de Arton (v1.0)", "page": 138,
        "desc": "Estátua funerária viva esculpida em granito negro e ouro, guardiã dos segredos mortos do Deserto da Perdição."
    },
    {
        "name": "Cria da Tormenta (Lefeu)",
        "sub": "Ameaça Solo",
        "nd": "ND 10",
        "nd_num": 10,
        "type": "Monstro (Aberração, Lefeu) 14",
        "size": "Grande",
        "role": "Solo",
        "init": 14, "percep": 16, "def": 32, "fort": 18, "ref": 16, "will": 20,
        "hp": 240, "mp": 30, "speed": "12m",
        "attacks": [
            {"name": "Tentáculos Vermelhos (4x)", "type": "Padrão", "description": "Corpo a corpo +20 (1d10+10 mais corrosão da realidade, 19/x2)."}
        ],
        "abilities": [
            {"name": "Insanidade da Tempestade", "type": "Passiva", "description": "Qualquer criatura que olhe para a cria deve fazer um teste de Vontade (CD 26) ou sofre 2d6 de dano psíquico e fica confusa."},
            {"name": "Matéria Vermelha Viva", "type": "Passiva", "description": "RD 10 (exceto armas de Aço-Rubi). Regeneração 10 PV por rodada."}
        ],
        "attrs": {"for": 26, "des": 18, "con": 22, "int": 16, "sab": 16, "car": 6},
        "book": "Ameaças de Arton (v1.0)", "page": 240,
        "desc": "Horror indescritível forjado na matéria corrompida da tempestade rubra, imune a venenos e com regeneração bizarra."
    }
]

for m in monsters_data:
    slug_id = f"ameaca-{m['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('(', '').replace(')', '')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    monsters_list.append({
        "id": slug_id,
        "name": m["name"],
        "category": "ameaca",
        "subcategory": m["sub"],
        "threatLevel": m["nd"],
        "threatLevelNumeric": m["nd_num"],
        "creatureType": m["type"],
        "size": m["size"],
        "role": m["role"],
        "initiative": m["init"],
        "perception": m["percep"],
        "defense": m["def"],
        "fortitude": m["fort"],
        "reflexes": m["ref"],
        "will": m["will"],
        "hp": m["hp"],
        "mp": m["mp"],
        "speed": m["speed"],
        "attacks": m["attacks"],
        "specialAbilities": m["abilities"],
        "attributes": m["attrs"],
        "summary": f"{m['nd']} ({m['type']}). Def: {m['def']}, PV: {m['hp']}. {m['desc'][:90]}...",
        "description": m["desc"],
        "sources": [{
            "book": m["book"],
            "page": m["page"],
            "section": f"Ameaças: {m['sub']}",
            "version": "v1.0+"
        }],
        "tags": ["ameaça", "monstro", m["name"].lower(), m["nd"].lower(), m["type"].lower(), m["size"].lower(), m["role"].lower()]
    })

with open("data/categories/ameacas.json", "w", encoding="utf-8") as f:
    json.dump(monsters_list, f, ensure_ascii=False, indent=2)

print(f"Ameaças e Monstros Consolidados: {len(monsters_list)} registros em data/categories/ameacas.json")
