import json
import re

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    current_equips = json.load(f)

current_names = {e['name'].strip().lower(): e for e in current_equips}
print(f"Total current equipments loaded: {len(current_equips)}")

# 1. Check Tormenta20 JdA Tabela 3-6 (Itens Gerais)
jda_itens_gerais = [
    # Equipamento de Aventura
    ("Água benta", "T$ 10", 0.5, "Equipamento de Aventura", 158),
    ("Algemas", "T$ 15", 1, "Equipamento de Aventura", 158),
    ("Arpéu", "T$ 5", 1, "Equipamento de Aventura", 158),
    ("Bandoleira de poções", "T$ 20", 1, "Equipamento de Aventura", 158),
    ("Barraca", "T$ 10", 1, "Equipamento de Aventura", 158),
    ("Corda", "T$ 1", 1, "Equipamento de Aventura", 158),
    ("Espelho", "T$ 10", 1, "Equipamento de Aventura", 158),
    ("Lampião", "T$ 7", 1, "Equipamento de Aventura", 158),
    ("Mochila", "T$ 2", 0, "Equipamento de Aventura", 158),
    ("Mochila de aventureiro", "T$ 50", 0, "Equipamento de Aventura", 158),
    ("Óleo", "T$ 0,1", 0.5, "Equipamento de Aventura", 158),
    ("Organizador de pergaminhos", "T$ 25", 1, "Equipamento de Aventura", 158),
    ("Pé de cabra", "T$ 2", 1, "Equipamento de Aventura", 158),
    ("Saco de dormir", "T$ 1", 1, "Equipamento de Aventura", 158),
    ("Símbolo sagrado", "T$ 5", 1, "Equipamento de Aventura", 158),
    ("Tocha", "T$ 0,1", 1, "Equipamento de Aventura", 158),
    ("Vara de madeira (3m)", "T$ 0,2", 1, "Equipamento de Aventura", 158),
    # Ferramentas
    ("Alaúde élfico", "T$ 300", 1, "Ferramentas", 158),
    ("Coleção de livros", "T$ 75", 1, "Ferramentas", 158),
    ("Equipamento de viagem", "T$ 10", 1, "Ferramentas", 158),
    ("Estojo de disfarces", "T$ 50", 1, "Ferramentas", 158),
    ("Flauta mística", "T$ 150", 1, "Ferramentas", 158),
    ("Gazua", "T$ 5", 1, "Ferramentas", 158),
    ("Instrumentos de <ofício>", "T$ 30", 1, "Ferramentas", 158),
    ("Instrumento musical", "T$ 35", 1, "Ferramentas", 158),
    ("Luneta", "T$ 100", 1, "Ferramentas", 158),
    ("Maleta de medicamentos", "T$ 50", 1, "Ferramentas", 158),
    ("Sela", "T$ 20", 1, "Ferramentas", 158),
    ("Tambor das profundezas", "T$ 80", 1, "Ferramentas", 158),
    # Vestuário
    ("Andrajos de aldeão", "T$ 1", 1, "Vestuário", 158),
    ("Bandana", "T$ 5", 1, "Vestuário", 158),
    ("Botas reforçadas", "T$ 20", 1, "Vestuário", 158),
    ("Camisa bufante", "T$ 25", 1, "Vestuário", 158),
    ("Capa esvoaçante", "T$ 25", 1, "Vestuário", 158),
    ("Capa pesada", "T$ 15", 1, "Vestuário", 158),
    ("Casaco longo", "T$ 20", 1, "Vestuário", 158),
    ("Chapéu arcano", "T$ 50", 1, "Vestuário", 158),
    ("Enfeite de elmo", "T$ 15", 1, "Vestuário", 158),
    ("Farrapos de ermitão", "T$ 1", 1, "Vestuário", 158),
    ("Gorro de ervas", "T$ 75", 1, "Vestuário", 158),
    ("Luva de pelica", "T$ 5", 1, "Vestuário", 158),
    ("Manopla", "T$ 10", 1, "Vestuário", 158),
    ("Manto camuflado", "T$ 12", 1, "Vestuário", 158),
    ("Manto eclesiástico", "T$ 20", 1, "Vestuário", 158),
    ("Robe místico", "T$ 50", 1, "Vestuário", 158),
    ("Sapatos de camurça", "T$ 8", 1, "Vestuário", 158),
    ("Tabardo", "T$ 10", 1, "Vestuário", 158),
    ("Traje da corte", "T$ 100", 1, "Vestuário", 158),
    ("Traje de viajante", "T$ 10", 0, "Vestuário", 158),
    ("Veste de seda", "T$ 25", 1, "Vestuário", 158),
    # Esotéricos
    ("Bolsa de pó", "T$ 300", 1, "Esotéricos", 159),
    ("Cajado arcano", "T$ 1.000", 2, "Esotéricos", 159),
    ("Cetro elemental", "T$ 750", 1, "Esotéricos", 159),
    ("Costela de lich", "T$ 300", 1, "Esotéricos", 159),
    ("Dedo de ente", "T$ 200", 1, "Esotéricos", 159),
    ("Luva de ferro", "T$ 150", 1, "Esotéricos", 159),
    ("Medalhão de prata", "T$ 750", 1, "Esotéricos", 159),
    ("Orbe cristalino", "T$ 750", 1, "Esotéricos", 159),
    ("Tomo hermético", "T$ 1.500", 1, "Esotéricos", 159),
    ("Varinha arcana", "T$ 100", 1, "Esotéricos", 159),
    # Alquímicos - Preparados
    ("Ácido", "T$ 10", 0.5, "Alquímicos - Preparados", 160),
    ("Bálsamo restaurador", "T$ 10", 0.5, "Alquímicos - Preparados", 160),
    ("Bomba", "T$ 50", 0.5, "Alquímicos - Preparados", 160),
    ("Cosmético", "T$ 30", 0.5, "Alquímicos - Preparados", 160),
    ("Elixir do amor", "T$ 100", 0.5, "Alquímicos - Preparados", 160),
    ("Essência de mana", "T$ 50", 0.5, "Alquímicos - Preparados", 160),
    ("Fogo alquímico", "T$ 10", 0.5, "Alquímicos - Preparados", 160),
    ("Pó do desaparecimento", "T$ 100", 0.5, "Alquímicos - Preparados", 160),
    # Alquímicos - Catalisadores
    ("Baga-de-fogo", "T$ 30", 0.5, "Alquímicos - Catalisadores", 160),
    ("Dente-de-dragão", "T$ 45", 0.5, "Alquímicos - Catalisadores", 160),
    ("Essência abissal", "T$ 150", 0.5, "Alquímicos - Catalisadores", 160),
    ("Líquen lilás", "T$ 30", 0.5, "Alquímicos - Catalisadores", 160),
    ("Musgo púrpura", "T$ 45", 0.5, "Alquímicos - Catalisadores", 160),
    ("Ossos de monstro", "T$ 45", 0.5, "Alquímicos - Catalisadores", 160),
    ("Pó de cristal", "T$ 30", 0.5, "Alquímicos - Catalisadores", 160),
    ("Pó de giz", "T$ 30", 0.5, "Alquímicos - Catalisadores", 160),
    ("Ramo verdejante", "T$ 45", 0.5, "Alquímicos - Catalisadores", 160),
    ("Saco de sal", "T$ 45", 0.5, "Alquímicos - Catalisadores", 160),
    ("Seixo de âmbar", "T$ 30", 0.5, "Alquímicos - Catalisadores", 160),
    ("Terra de cemitério", "T$ 30", 0.5, "Alquímicos - Catalisadores", 160),
    # Alquímicos - Venenos
    ("Beladona", "T$ 1.500", 0.5, "Alquímicos - Venenos", 160),
    ("Bruma sonolenta", "T$ 150", 0.5, "Alquímicos - Venenos", 160),
    ("Cicuta", "T$ 60", 0.5, "Alquímicos - Venenos", 160),
    ("Essência de sombra", "T$ 100", 0.5, "Alquímicos - Venenos", 160),
    ("Névoa tóxica", "T$ 30", 0.5, "Alquímicos - Venenos", 160),
    ("Peçonha comum", "T$ 15", 0.5, "Alquímicos - Venenos", 160),
    ("Peçonha concentrada", "T$ 90", 0.5, "Alquímicos - Venenos", 160),
    ("Peçonha potente", "T$ 600", 0.5, "Alquímicos - Venenos", 160),
    ("Pó de lich", "T$ 3.000", 0.5, "Alquímicos - Venenos", 160),
    ("Riso de Nimb", "T$ 150", 0.5, "Alquímicos - Venenos", 160),
    # Alimentação
    ("Batata valkariana", "T$ 2", 0.5, "Alimentação", 161),
    ("Gorad quente", "T$ 18", 0.5, "Alimentação", 161),
    ("Macarrão de Yuvalin", "T$ 6", 0.5, "Alimentação", 161),
    ("Prato do aventureiro", "T$ 1", 0.5, "Alimentação", 161),
    ("Ração de viagem (por dia)", "T$ 0,5", 0.5, "Alimentação", 161),
    ("Refeição comum", "T$ 0,3", 0.5, "Alimentação", 161),
    ("Sopa de peixe", "T$ 1", 0.5, "Alimentação", 161),
    # Animais
    ("Alforje", "T$ 30", 0, "Animais", 162),
    ("Cão de caça", "T$ 150", 0, "Animais", 162),
    ("Cavalo", "T$ 75", 0, "Animais", 162),
    ("Cavalo de guerra", "T$ 400", 0, "Animais", 162),
    ("Estábulo (por dia)", "T$ 0,1", 0, "Animais", 162),
    ("Pônei", "T$ 5", 0, "Animais", 162),
    ("Pônei de guerra", "T$ 30", 0, "Animais", 162),
    ("Trobo", "T$ 60", 0, "Animais", 162),
    # Veículos
    ("Balão goblin", "T$ 200", 0, "Veículos", 162),
    ("Carroça", "T$ 150", 0, "Veículos", 162),
    ("Carruagem", "T$ 500", 0, "Veículos", 162),
    ("Canoa", "T$ 70", 0, "Veículos", 162),
    ("Veleiro", "T$ 10.000", 0, "Veículos", 162),
    # Serviços
    ("Estadia Comum", "T$ 0,5", 0, "Serviços", 162),
    ("Estadia Confortável", "T$ 4", 0, "Serviços", 162),
    ("Estadia Luxuosa", "T$ 20", 0, "Serviços", 162),
    ("Condução Terrestre", "T$ 0,5 / km", 0, "Serviços", 162),
    ("Condução Marítima", "T$ 0,1 / km", 0, "Serviços", 162),
    ("Condução Aérea", "T$ 10 / km", 0, "Serviços", 162),
    ("Curandeiro", "T$ 5", 0, "Serviços", 162),
    ("Serviço de Magia (1º Círculo)", "T$ 10", 0, "Serviços", 162),
    ("Serviço de Magia (2º Círculo)", "T$ 90", 0, "Serviços", 162),
    ("Serviço de Magia (3º Círculo)", "T$ 360", 0, "Serviços", 162),
    ("Mensageiro", "T$ 0,5 / km", 0, "Serviços", 162)
]

print("\n=== AUDITORIA: ITENS GERAIS DO JDA (Tabela 3-6) ===")
missing_jda = []
for name, price, space, group, page in jda_itens_gerais:
    norm = name.strip().lower()
    if norm not in current_names:
        # Check without parenthesized part
        short_norm = re.sub(r'\(.*?\)', '', norm).strip()
        matched = None
        for cn in current_names:
            if short_norm in cn or cn in short_norm:
                matched = cn
                break
        if matched:
            print(f"  [OK / Variacao] '{name}' encontrado como '{matched}'")
        else:
            missing_jda.append((name, price, space, group, page))
            print(f"  [FALTANDO] '{name}' (Preco: {price}, Espaco: {space}, Grupo: {group})")

print(f"\nTotal faltando em JDA Tabela 3-6: {len(missing_jda)}")
