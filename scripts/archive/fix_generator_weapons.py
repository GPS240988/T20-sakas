import re

with open('scripts/build_full_comprehensive_canon_equipments.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove arma-manopla
content = re.sub(
    r'add_item\(\s*"arma-manopla".*?\n\)\n',
    '',
    content,
    flags=re.DOTALL
)

# 2. Remove fake arma-martelo (simple)
content = re.sub(
    r'add_item\(\s*"arma-martelo",\s*"Martelo".*?\n\)\n',
    '',
    content,
    flags=re.DOTALL
)

# 3. Remove fake arma-dardo
content = re.sub(
    r'add_item\(\s*"arma-dardo".*?\n\)\n',
    '',
    content,
    flags=re.DOTALL
)

# 4. Remove fake arma-machado-de-ataque and replace with Machadinha
content = re.sub(
    r'add_item\(\s*"arma-machado-de-ataque".*?\n\)\n',
    '''add_item(
    "arma-machadinha", "Machadinha", "Armas", "Armas Marciais", "Corpo a Corpo / Leve",
    "T$ 6", "1d6", "x3", "Corte", "Curto", None, None, 1,
    book_jda, 148,
    "Um pequeno machado balanceado de uma mão que pode ser arremessado. É a arma padrão dos anões para combate leve ou à distância.",
    ["machado", "arremesso", "crítico x3", "anão", "leve"]
)
''',
    content,
    flags=re.DOTALL
)

# 5. Remove any old fake martelo-leve if redundant or update it
content = re.sub(
    r'add_item\(\s*"arma-martelo-leve".*?\n\)\n',
    '',
    content,
    flags=re.DOTALL
)

# 6. Remove any simple Rede if present
content = re.sub(
    r'add_item\(\s*"arma-rede",\s*"Rede",\s*"Armas",\s*"Armas Simples".*?\n\)\n',
    '',
    content,
    flags=re.DOTALL
)

# Ensure Rede is under Armas Exóticas
if 'arma-rede' not in content:
    content = content.replace(
        '# --- 1.1.4) Armas de Fogo',
        '''# Armas Exóticas Ataque à Distância - Uma Mão
add_item(
    "arma-rede", "Rede", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão",
    "T$ 20", "-", "-", "-", "Curto", None, None, 1,
    book_jda, 149,
    "Uma rede de cordas reforçadas com chumbadas nas bordas. Ao acertar um ataque à distância com uma rede contra uma criatura de tamanho Grande ou menor, ela não sofre dano, mas fica enredada (fica vulnerável, sofre -2 em testes de ataque e -5m no deslocamento). A criatura pode se soltar gastando uma ação padrão e passando em um teste de Acrobacia ou Atletismo (CD 15) ou causando 5 pontos de dano cortante à rede.",
    ["enredar", "controle", "captura", "exótica"]
)

# --- 1.1.4) Armas de Fogo'''
    )

# Ensure Marreta is in Armas Marciais Duas Mãos
if 'arma-marreta' not in content:
    content = content.replace(
        'add_item(\n    "arma-montante"',
        '''add_item(
    "arma-marreta", "Marreta", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos",
    "T$ 20", "3d4", "x2", "Impacto", "-", None, None, 2,
    book_jda, 148,
    "Uma marreta pesada de duas mãos com uma grande cabeça de ferro montada em um cabo longo de madeira reforçada.",
    ["marreta", "impacto pesado", "3d4", "duas mãos"]
)

add_item(
    "arma-montante"'''
    )

# Ensure Besta Pesada is in Armas Marciais Disparo
if 'arma-besta-pesada' not in content:
    content = content.replace(
        '# --- 1.1.3) Armas Exóticas',
        '''add_item(
    "arma-besta-pesada", "Besta Pesada", "Armas", "Armas Marciais", "Ataque à Distância / Disparo",
    "T$ 50", "1d12", "19", "Perfuração", "Médio", None, None, 2,
    book_jda, 147,
    "Uma versão maior e mais potente da besta leve, com coronha reforçada e arco de aço. Recarregar uma besta pesada é uma ação de movimento.",
    ["besta pesada", "1d12", "crítico 19", "disparo"]
)

# --- 1.1.3) Armas Exóticas'''
    )

# 7. Add Manopla in Vestuário (JDA)
if 'item-manopla' not in content:
    content = content.replace(
        'add_item(\n    "item-luva-de-pelica"',
        '''add_item(
    "item-manopla", "Manopla", "Itens Gerais", "Vestuário", "Vestuário",
    "T$ 10", None, None, None, None, None, None, 1,
    book_jda, 158,
    "Luva metálica que permite socos mais perigosos — o dano de seus ataques desarmados torna-se letal. Uma manopla conta como uma arma para receber melhorias e encantos para usá-los em seus ataques desarmados.",
    ["vestuário", "ataque desarmado", "dano letal", "luva de metal", "manopla"]
)

add_item(
    "item-luva-de-pelica"'''
    )

with open('scripts/build_full_comprehensive_canon_equipments.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully cleaned up build_full_comprehensive_canon_equipments.py!")
