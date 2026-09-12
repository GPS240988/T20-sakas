import json
import re

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    current_equips = json.load(f)

current_map = {e['name'].strip().lower(): e for e in current_equips}
id_map = {e['id'].strip().lower(): e for e in current_equips}

print(f"Total current equipments loaded: {len(current_equips)}")

# 1. Tormenta20 JdA Tabela 3-3: Armas
jda_weapons = [
    # Armas Simples Leves
    "Adaga", "Espada curta", "Foice", "Ataque desarmado",
    # Armas Simples Uma Mão
    "Clava", "Lança", "Maça",
    # Armas Simples Duas Mãos
    "Bordão", "Pique", "Tacape",
    # Armas Simples Distância Uma Mão
    "Azagaia", "Besta leve",
    # Armas Simples Distância Duas Mãos
    "Funda", "Arco curto",
    # Armas Marciais Leves
    "Machadinha",
    # Armas Marciais Uma Mão
    "Cimitarra", "Espada longa", "Florete", "Machado de batalha", "Mangual", "Martelo de guerra", "Picareta", "Tridente",
    # Armas Marciais Duas Mãos
    "Alabarda", "Alfange", "Gadanho", "Lança montada", "Machado de guerra", "Marreta", "Montante",
    # Armas Marciais Distância Duas Mãos
    "Arco longo", "Besta pesada",
    # Armas Exóticas Uma Mão
    "Chicote", "Espada bastarda", "Katana", "Machado anão",
    # Armas Exóticas Duas Mãos
    "Corrente de espinhos", "Machado táurico",
    # Armas Exóticas Distância Uma Mão
    "Rede",
    # Armas de Fogo
    "Pistola", "Mosquete"
]

# 2. Tormenta20 JdA Tabela 3-4: Munições
jda_ammo = ["Balas", "Flechas", "Pedras", "Virotes"]

# 3. Tormenta20 JdA Tabela 3-5: Armaduras & Escudos
jda_armors = [
    "Armadura acolchoada", "Armadura de couro", "Couro batido", "Gibão de peles", "Couraça",
    "Brunea", "Cota de malha", "Loriga segmentada", "Meia armadura", "Armadura completa",
    "Escudo leve", "Escudo pesado"
]

# 4. Tormenta20 JdA Tabela 3-6: Itens Gerais
jda_general = [
    "Água benta", "Algemas", "Arpéu", "Bandoleira de poções", "Barraca", "Corda", "Espelho", "Lampião",
    "Mochila", "Mochila de aventureiro", "Óleo", "Organizador de pergaminhos", "Pé de cabra", "Saco de dormir",
    "Símbolo sagrado", "Tocha", "Vara de madeira (3m)",
    "Alaúde élfico", "Coleção de livros", "Equipamento de viagem", "Estojo de disfarces", "Flauta mística",
    "Gazua", "Instrumentos de <ofício>", "Instrumento musical", "Luneta", "Maleta de medicamentos", "Sela", "Tambor das profundezas",
    "Andrajos de aldeão", "Bandana", "Botas reforçadas", "Camisa bufante", "Capa esvoaçante", "Capa pesada", "Casaco longo",
    "Chapéu arcano", "Enfeite de elmo", "Farrapos de ermitão", "Gorro de ervas", "Luva de pelica", "Manopla",
    "Manto camuflado", "Manto eclesiástico", "Robe místico", "Sapatos de camurça", "Tabardo", "Traje da corte", "Traje de viajante", "Veste de seda",
    "Bolsa de pó", "Cajado arcano", "Cetro elemental", "Costela de lich", "Dedo de ente", "Luva de ferro", "Medalhão de prata", "Orbe cristalino", "Tomo hermético", "Varinha arcana",
    "Ácido", "Bálsamo restaurador", "Bomba", "Cosmético", "Elixir do amor", "Essência de mana", "Fogo alquímico", "Pó do desaparecimento",
    "Baga-de-fogo", "Dente-de-dragão", "Essência abissal", "Líquen lilás", "Musgo púrpura", "Ossos de monstro", "Pó de cristal", "Pó de giz", "Ramo verdejante", "Saco de sal", "Seixo de âmbar", "Terra de cemitério",
    "Beladona", "Bruma sonolenta", "Cicuta", "Essência de sombra", "Névoa tóxica", "Peçonha comum", "Peçonha concentrada", "Peçonha potente", "Pó de lich", "Riso de Nimb",
    "Batata valkariana", "Gorad quente", "Macarrão de Yuvalin", "Prato do aventureiro", "Ração de viagem (por dia)", "Refeição comum", "Sopa de peixe",
    "Alforje", "Cão de caça", "Cavalo", "Cavalo de guerra", "Estábulo (por dia)", "Pônei", "Pônei de guerra", "Trobo",
    "Balão goblin", "Carroça", "Carruagem", "Canoa", "Veleiro",
    "Estadia Comum", "Estadia Confortável", "Estadia Luxuosa", "Condução Terrestre", "Condução Marítima", "Condução Aérea", "Curandeiro", "Serviço de Magia (1º Círculo)", "Serviço de Magia (2º Círculo)", "Serviço de Magia (3º Círculo)", "Mensageiro"
]

# 5. Tormenta20 JdA Tabela 3-8 & 3-9: Melhorias & Materiais
jda_upgrades_materials = [
    "Certeira", "Pungente", "Cruel", "Atroz", "Equilibrada", "Harmonizada (Arma)", "Injeção alquímica", "Maciça", "Mira telescópica", "Precisa",
    "Ajustada", "Sob medida", "Delicada", "Espinhosa (Armadura)", "Espinhoso (Escudo)", "Polida", "Reforçada", "Selada",
    "Canalizador", "Energético", "Harmonizado (Esotérico)", "Poderoso", "Vigilante",
    "Aprimorado", "Banhado a ouro", "Cravejado de gemas", "Discreto", "Macabro",
    "Aço-Rubi", "Adamante", "Gelo Eterno", "Madeira Tollon", "Matéria Vermelha", "Mitral"
]

# 6. Heróis de Arton Tabela 3-1: Novas Armas
hda_weapons = [
    "Bastão lúdico", "Besta de mão",
    "Adaga oposta", "Agulha de Ahlen", "Cinquedea", "Dirk", "Martelo leve",
    "Espada larga", "Espadim", "Maça-estrela", "Serrilheira",
    "Bico de corvo", "Desmontador", "Espada de execução", "Lança de justa", "Malho", "Martelo longo", "Tan-korak",
    "Tai-tai", "Arco montado", "Besta dupla",
    "Kimbata", "Clava-grão", "Espada canora", "Espada-gadanho", "Khopesh", "Lança de falange", "Machado de haste", "Rapieira",
    "Marrão", "Montante cinético",
    "Boleadeira", "Chakram", "Arco de guerra", "Balestra", "Besta de repetição",
    "Garrucha", "Canhão portátil", "Sifão cáustico"
]

# 7. Heróis de Arton Tabela 3-3: Novas Armaduras & Escudos
hda_armors = [
    "Armadura sensual", "Armadura de folhas", "Armadura de engenhoqueiro goblin", "Cota de moedas", "Colete fora da lei",
    "Brigantina", "Armadura de chumbo", "Armadura de justa", "Armadura de hussardo alado", "Armadura de pedra",
    "Broquel", "Escudo de vime", "Escudo torre", "Sagna"
]

# 8. Heróis de Arton Tabela 3-4: Novos Itens Gerais
hda_general = [
    # Equipamento de Aventura
    "Ábaco", "Ampulheta", "Aparelho de chá", "Astrolábio", "Armação para mochila", "Asas do texugo", "Bainha adornada",
    "Bússola", "Cinto de utilidades", "Condecoração militar", "Dente falso", "Diagrama anatômico", "Espelho refletor",
    "Estetoscópio", "Estrepes (bolsa para 3m)", "Favor da pessoa amada", "Lampião de foco", "Leque", "Livro de métodos anti-Nimb",
    "Lupa", "Mapa", "Mecanismo de mola", "Mochila discreta", "Prancheta", "Sinete",
    # Ferramentas Gerais
    "Apito de caça", "Baralho marcado", "Espelho cirúrgico", "Estandarte", "Estandarte portátil", "Molde pré-fabricado",
    # Instrumentos Musicais
    "Clarim deheoni", "Cítara heptatônica", "Cornamusa de Doherimm", "Flauta sar-allan", "Gaita de foles",
    "Lira de casco de tartaruga", "Marionetes", "Pandeiro das estradas", "Tamborete marcial", "Trombeta tapistana", "Violino soprano",
    # Vestuário
    "Avental de forja", "Camisolão", "Capa com dragonas", "Casaca de apetrechos", "Chapéu emplumado", "Elmo leve", "Elmo pesado",
    "Jaqueta de couro", "Luva de falcoaria", "Luva magnética", "Máscara bucal", "Máscara completa", "Máscara de baile",
    "Máscara de soldador", "Monóculo", "Óculos de aeronauta", "Palmar", "Peruca", "Rondel", "Roupão elegante", "Rufo",
    "Sapatos confortáveis", "Sapatos de salto alto", "Veste acolchoada",
    # Esotéricos
    "Compasso místico", "Flauta convocadora", "Mandala onírica", "Varinha armamentista",
    # Alquímicos - Preparados
    "Ácido concentrado", "Analgésico", "Estalinho Gury", "Extrato de gelo eterno", "Extrato de oxxdon", "Frasco abissal", "Pó de cinza", "Pó do aparecimento", "Visco persistente",
    # Alquímicos - Catalisadores
    "Cristal reflexivo", "Essência fantasmal", "Noz saltadora", "Presa de Hyninn",
    # Alquímicos - Venenos
    "Bolor hemorrágico", "Fumaça onírica", "Gás moroso", "Seiva necrótica",
    # Aparatos
    "Captador de luz", "Comutador", "Conversor-alimentador", "Engenho de automação", "Espera para melhorias", "Estabilizador",
    "Estimulador de sobrecarga", "Gatilho de corda", "Giroscópio", "Ligação de convergência", "Remontagem de portabilidade",
    "Sequenciador de ativação", "Sistema de refrigeração", "Supressor de segurança", "Transformador místico",
    # Alimentação - Pratos
    "Baga celeste cozida", "Cozido de pimenta", "Manjar de sombras",
    # Alimentação - Bebidas
    "Baba de troll", "Barba queimada", "Cerveja deheoni", "Dilínio", "Grogue negro", "Grogue rubro", "Hidromel uivante", "Licor feérico", "Sidra ahleniense", "Vinho Pruss", "Vinho élfico",
    # Animais & Acessórios
    "Armadura de montaria leve", "Armadura de montaria pesada", "Arreios namalkahnianos", "Caparazão", "Estribos", "Ornamento",
    # Veículos
    "Barcaça", "Biga de guerra", "Dirigível goblin", "Jangada", "Veleiro",
    # Serviços & Capangas
    "Banho quente", "Bigode encerado", "Instrução marcial", "Maquiagem profissional",
    "Mercenário (Parceiro Iniciante)", "Mercenário (Parceiro Veterano)", "Mercenário (Capangas Iniciantes)", "Mercenário (Capangas Veteranos)",
    "Ópera", "Sarau informativo",
    "Bando Duyshidakk", "Esqueletos Animados", "Pelotão de Infantaria", "Tripulação", "Turba de Camponeses", "Unidade de Arqueiros"
]

# 9. Heróis de Arton Tabela 3-5: Novas Melhorias
hda_upgrades = [
    "Farpada", "Fósforo", "Guarda", "Incendiária", "Pressurizada",
    "Balístico", "Injetora", "Prudente",
    "Potencializador",
    "Brasonado", "Usado",
    "Deslumbrante"
]

# 10. Ameaças de Arton Tabela 3-1: Novas Armas
ameacas_weapons = [
    "Porrete", "Zarabatana", "Neko-te", "Gládio", "Tetsubo",
    "Traque", "Arcabuz", "Bacamarte",
    "Açoite finntroll", "Espada vespa", "Pistola-punhal", "Mordida do diabo", "Presa de serpente", "Lança de fogo", "Shuriken", "Arpão"
]

# 11. Ameaças de Arton Tabela 3-2: Novas Armaduras & Escudos
ameacas_armors = [
    "Armadura de ossos", "Veste de teia de aranha",
    "Armadura de quitina",
    "Escudo de couro"
]

# 12. Ameaças de Arton Tabela 3-3: Novos Itens Gerais
ameacas_general = [
    "Algravia", "Banquete de canceronte", "Coc-au-triz", "Cozido de serpe", "Gorlogg ensopado", "Omelete monstruosa", "Sashimi de kraken",
    "Bulette", "Capivara", "Corcel do deserto", "Dromedário", "Elefante", "Hiena", "Leão", "Rinoceronte", "Urso pardo",
    "Caixa de voz", "Corda de teia", "Dente de wisphago",
    "Ankh solar", "Tomo de guerra", "Tomo do rancor",
    "Bálsamo de drogadora", "Bomba de fumaça", "Elixir quimérico", "Éter elemental", "Isca putrefata", "Lágrima pétrea", "Óleo de baleia", "Óleo de besouro", "Pó azul",
    "Corrosivo mineral", "Gelo extremo", "Pedaço de língua", "Raio cristalizado",
    "Esporos de cogumelo", "Peçonha anciã", "Peçonha irritante", "Veneno batráquio",
    "Garra feroz", "Manto do mantor", "Manto pesado", "Sombreiro", "Traje selako"
]

# 13. Ameaças de Arton Tabela 3-4: Novos Materiais & Melhorias
ameacas_materials_upgrades = [
    "Multifuncional", "Penetrante",
    "Casco de Monstro", "Couraça de Kaiju", "Couro de Bulette", "Cristal de Sol", "Lanajuste", "Pena de Kraken", "Prata", "Espada de Coral"
]

all_checklists = [
    ("Tormenta20 JdA - Tabela 3-3: Armas", jda_weapons),
    ("Tormenta20 JdA - Tabela 3-4: Munições", jda_ammo),
    ("Tormenta20 JdA - Tabela 3-5: Armaduras & Escudos", jda_armors),
    ("Tormenta20 JdA - Tabela 3-6: Itens Gerais", jda_general),
    ("Tormenta20 JdA - Tabelas 3-8 e 3-9: Melhorias e Materiais", jda_upgrades_materials),
    ("Heróis de Arton - Tabela 3-1: Novas Armas", hda_weapons),
    ("Heróis de Arton - Tabela 3-3: Novas Armaduras & Escudos", hda_armors),
    ("Heróis de Arton - Tabela 3-4 & Capangas: Novos Itens Gerais", hda_general),
    ("Heróis de Arton - Tabela 3-5: Novas Melhorias", hda_upgrades),
    ("Ameaças de Arton - Tabela 3-1: Novas Armas", ameacas_weapons),
    ("Ameaças de Arton - Tabela 3-2: Novas Armaduras & Escudos", ameacas_armors),
    ("Ameaças de Arton - Tabela 3-3: Novos Itens Gerais", ameacas_general),
    ("Ameaças de Arton - Tabela 3-4: Novos Materiais & Melhorias", ameacas_materials_upgrades)
]

total_checked = 0
total_missing = 0

def find_match(target):
    target_clean = target.strip().lower()
    target_simplified = re.sub(r'\(.*?\)', '', target_clean).strip()
    target_slug = re.sub(r'[^a-z0-9]', '', target_simplified)
    
    # 1. Exact Name
    if target_clean in current_map:
        return current_map[target_clean]['name']
    if target_simplified in current_map:
        return current_map[target_simplified]['name']
        
    # 2. Match in ID
    for eid, item in id_map.items():
        if target_slug and target_slug in eid.replace('-', ''):
            return item['name']
            
    # 3. Substring match in name
    for cname, item in current_map.items():
        if target_simplified in cname or cname in target_simplified:
            return item['name']
            
    return None

for cat_title, items in all_checklists:
    print(f"\n=======================================================")
    print(f"AUDITANDO: {cat_title} (Total de itens na tabela: {len(items)})")
    print(f"=======================================================")
    missing_in_cat = []
    for it in items:
        total_checked += 1
        matched = find_match(it)
        if matched:
            # print(f"  [OK] {it} -> {matched}")
            pass
        else:
            total_missing += 1
            missing_in_cat.append(it)
            print(f"  [FALTANDO] {it}")
    if not missing_in_cat:
        print(f"  --> SUCESSO: 100% dos {len(items)} itens estao devidamente catalogados!")
    else:
        print(f"  --> ALERTA: {len(missing_in_cat)} itens faltando nesta secao!")

print("\n" + "="*60)
print(f"AUDITORIA GLOBAL CONCLUÍDA:")
print(f"Total de itens auditados nas tabelas oficiais: {total_checked}")
print(f"Total de itens faltantes: {total_missing}")
print(f"Total de itens no banco de dados ativo: {len(current_equips)}")
print("="*60)
