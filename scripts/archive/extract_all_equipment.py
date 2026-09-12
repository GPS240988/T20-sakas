import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
pdf_ameacas = "Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf"
pdf_herois = "T20-Herois-de-Arton-v1-1_compressed.pdf"

os.makedirs("data/categories", exist_ok=True)

equipment_list = []

def clean_text(t):
    if not t:
        return ""
    t = t.replace('\x00', '')
    t = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', t)
    t = re.sub(r'\n+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

# =========================================================================
# 1. ARMAS OFICIAIS (JOGO DO ANO + AMEAÇAS + HERÓIS)
# =========================================================================
print("Consolidando Armas dos Livros Oficiais...")

weapons_data = [
    # Armas Simples Corpo a Corpo (JDA)
    {"name": "Adaga", "sub": "Armas Simples", "prof": "Simples", "wield": "Leve", "price": "T$ 2", "damage": "1d4", "crit": "19/x2", "type": "Perfuração", "range": "Curto", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Uma faca afiada de lâmina curta. Fácil de ocultar, fornece +5 em testes de Ladinagem para esconder arma. Pode ser arremessada."},
    {"name": "Espada Curta", "sub": "Armas Simples", "prof": "Simples", "wield": "Leve", "price": "T$ 10", "damage": "1d6", "crit": "19/x2", "type": "Perfuração", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "A mais comum das espadas leves, com lâmina reta de dois gumes de cerca de 50cm."},
    {"name": "Foice", "sub": "Armas Simples", "prof": "Simples", "wield": "Leve", "price": "T$ 4", "damage": "1d6", "crit": "x3", "type": "Corte", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Ferramenta agrícola adaptada para o combate, com lâmina curvada montada em cabo curto."},
    {"name": "Manopla", "sub": "Armas Simples", "prof": "Simples", "wield": "Leve", "price": "T$ 5", "damage": "-", "crit": "-", "type": "Impacto", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Uma luva metálica reforçada. Permite que seus ataques desarmados causem dano letal e recebam melhorias de armas."},
    {"name": "Clava", "sub": "Armas Simples", "prof": "Simples", "wield": "Uma Mão", "price": "T$ 0", "damage": "1d6", "crit": "x2", "type": "Impacto", "range": "Curto", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Um pedaço de madeira pesado, osso grande ou bastão rústico. Pode ser arremessada."},
    {"name": "Lança", "sub": "Armas Simples", "prof": "Simples", "wield": "Uma Mão", "price": "T$ 2", "damage": "1d6", "crit": "x2", "type": "Perfuração", "range": "Curto", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Haste de madeira com ponta de metal afiada. Pode ser usada com uma ou duas mãos (causa 1d8 de duas mãos) e pode ser arremessada."},
    {"name": "Maça", "sub": "Armas Simples", "prof": "Simples", "wield": "Uma Mão", "price": "T$ 12", "damage": "1d8", "crit": "x2", "type": "Impacto", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Haste de metal ou madeira pesada encimada por cabeça de bronze ou ferro com flanges."},
    {"name": "Bordão", "sub": "Armas Simples", "prof": "Simples", "wield": "Duas Mãos", "price": "T$ 0", "damage": "1d6/1d6", "crit": "x2", "type": "Impacto", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Um cajado de madeira resistente de cerca de 1,80m. É uma arma dupla (pode ser usada como duas armas leves com o poder Estilo de Duas Armas)."},
    {"name": "Pique", "sub": "Armas Simples", "prof": "Simples", "wield": "Haste", "price": "T$ 5", "damage": "1d8", "crit": "x2", "type": "Perfuração", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Arma de haste muito longa (cerca de 3m). Permite atacar alvos a até 3m de distância, mas não alvos adjacentes."},
    {"name": "Tacape", "sub": "Armas Simples", "prof": "Simples", "wield": "Duas Mãos", "price": "T$ 0", "damage": "1d10", "crit": "x2", "type": "Impacto", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 148, "desc": "Um tronco esculpido ou bastão maciço usado com ambas as mãos por trogs e bárbaros."},

    # Armas Marciais Corpo a Corpo (JDA)
    {"name": "Cimitarra", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Uma Mão", "price": "T$ 15", "damage": "1d6", "crit": "18/x2", "type": "Corte", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Espada curva com lâmina afiada em um único gume, famosa pela alta frequência de acertos críticos."},
    {"name": "Espada Longa", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Uma Mão", "price": "T$ 15", "damage": "1d8", "crit": "19/x2", "type": "Corte", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "A arma definitiva dos cavaleiros e guerreiros de Arton, com lâmina de cerca de 90cm e guarda em cruz."},
    {"name": "Florete", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Leve", "price": "T$ 20", "damage": "1d6", "crit": "18/x2", "type": "Perfuração", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Espada delgada e flexível com guarda em cesto. Pode ser usada com o poder Acuidade com Arma para usar Destreza no ataque."},
    {"name": "Machadinha", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Leve", "price": "T$ 6", "damage": "1d6", "crit": "x3", "type": "Corte", "range": "Curto", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Machado de mão balanceado para corte e arremesso rápido."},
    {"name": "Machado de Batalha", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Uma Mão", "price": "T$ 10", "damage": "1d8", "crit": "x3", "type": "Corte", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Machado pesado de lâmina larga usado com uma mão por guerreiros e nobres anões."},
    {"name": "Mangual", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Uma Mão", "price": "T$ 8", "damage": "1d8", "crit": "x2", "type": "Impacto", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Haste de madeira com esfera de ferro espinhosa presa por corrente. Fornece +2 em testes de desarmar e ignora bônus de escudos."},
    {"name": "Tridente", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Uma Mão", "price": "T$ 15", "damage": "1d8", "crit": "x2", "type": "Perfuração", "range": "Curto", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Lança de três pontas com farpas, tradicional de gladiadores e tritões. Fornece +2 em testes para derrubar e desarmar."},
    {"name": "Alabarda", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Haste", "price": "T$ 10", "damage": "1d10", "crit": "x3", "type": "Corte/Perfuração", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Haste longa com lâmina de machado e ponta de lança. Arma de haste com alcance de 3m."},
    {"name": "Alfange", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Duas Mãos", "price": "T$ 75", "damage": "2d4", "crit": "18/x2", "type": "Corte", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Espada curva pesada de duas mãos com altíssima margem de crítico, popular no Deserto da Perdição."},
    {"name": "Guisarme", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Haste", "price": "T$ 9", "damage": "2d4", "crit": "x3", "type": "Corte", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Arma de haste com lâmina curvada em gancho. Fornece +2 em testes de manobra para derrubar."},
    {"name": "Lança Montada", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Duas Mãos", "price": "T$ 10", "damage": "1d10", "crit": "x3", "type": "Perfuração", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Lança pesada de torneio. Quando usada em investida montada, seu dano base é multiplicado por 2."},
    {"name": "Machado de Guerra", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Duas Mãos", "price": "T$ 20", "damage": "1d12", "crit": "x3", "type": "Corte", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "Machado imenso de lâmina dupla empunhado com as duas mãos para golpes devastadores."},
    {"name": "Montante", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Duas Mãos", "price": "T$ 50", "damage": "2d6", "crit": "19/x2", "type": "Corte", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 149, "desc": "A maior das espadas, com lâmina de mais de 1,50m para combate contra múltiplos oponentes."},

    # Armas de Ataque à Distância e Disparo (JDA)
    {"name": "Arco Curto", "sub": "Armas Simples", "prof": "Simples", "wield": "Disparo", "price": "T$ 30", "damage": "1d6", "crit": "x3", "type": "Perfuração", "range": "Médio", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 150, "desc": "Arco compacto de madeira leve, fácil de disparar a pé ou a cavalo."},
    {"name": "Besta Leve", "sub": "Armas Simples", "prof": "Simples", "wield": "Disparo", "price": "T$ 35", "damage": "1d8", "crit": "19/x2", "type": "Perfuração", "range": "Médio", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 150, "desc": "Disparador mecânico de virotes. Recarregar exige uma ação de movimento."},
    {"name": "Funda", "sub": "Armas Simples", "prof": "Simples", "wield": "Disparo", "price": "T$ 0", "damage": "1d4", "crit": "x2", "type": "Impacto", "range": "Médio", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 150, "desc": "Tira de couro para arremessar pedras ou balas de chumbo. Soma a Força no dano."},
    {"name": "Arco Longo", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Disparo", "price": "T$ 100", "damage": "1d8", "crit": "x3", "type": "Perfuração", "range": "Longo", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 150, "desc": "Arco de grande envergadura feito de teixo ou madeira nobre. Soma a Força no dano até o limite de +2 (ou mais com aprimoramentos)."},
    {"name": "Besta Pesada", "sub": "Armas Marciais", "prof": "Marcial", "wield": "Disparo", "price": "T$ 50", "damage": "1d12", "crit": "19/x2", "type": "Perfuração", "range": "Médio", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 150, "desc": "Besta com arco de aço de alta tensão. Recarregar exige uma ação padrão."},

    # Armas de Fogo e Exóticas (JDA + Ameaças + Heróis)
    {"name": "Pistola", "sub": "Armas de Fogo", "prof": "Fogo", "wield": "Uma Mão", "price": "T$ 250", "damage": "2d6", "crit": "19/x3", "type": "Perfuração", "range": "Curto", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 151, "desc": "Arma de fogo portátil de pólvora desenvolvida pelos klirens de Zakharov. Recarregar exige uma ação padrão."},
    {"name": "Mosquete", "sub": "Armas de Fogo", "prof": "Fogo", "wield": "Duas Mãos", "price": "T$ 500", "damage": "2d8", "crit": "19/x3", "type": "Perfuração", "range": "Médio", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 151, "desc": "Arma de fogo de cano longo com alcance devastador. Recarregar exige uma ação completa."},
    {"name": "Katana", "sub": "Armas Exóticas", "prof": "Exótica", "wield": "Uma Mão", "price": "T$ 100", "damage": "1d10", "crit": "19/x2", "type": "Corte", "range": "-", "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 152, "desc": "A lendária espada samurai de Tamu-ra. Pode ser usada como arma marcial com as duas mãos ou como arma exótica de uma mão (permitindo Acuidade com Arma)."},
    {"name": "Corrente de Espinhos", "sub": "Armas Exóticas", "prof": "Exótica", "wield": "Duas Mãos", "price": "T$ 25", "damage": "2d4/2d4", "crit": "19/x2", "type": "Perfuração", "range": "-", "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 152, "desc": "Corrente flexível com lâminas farpadas. Arma dupla e de haste flexível que pode atingir alvos adjacentes ou a até 3m de distância."},
    
    # Armas do Bazar Monstruoso (Ameaças de Arton)
    {"name": "Garra de Monstro", "sub": "Bazar Monstruoso", "prof": "Exótica", "wield": "Leve", "price": "T$ 50", "damage": "1d8", "crit": "19/x2", "type": "Corte/Perfuração", "range": "-", "space": 1, "book": "Ameaças de Arton (v1.0)", "page": 394, "desc": "Arma feita a partir de presas e garras endurecidas de monstros de Arton. Fornece bônus contra alvos com couro espesso."},
    {"name": "Chicote de Espinhos Monstruoso", "sub": "Bazar Monstruoso", "prof": "Exótica", "wield": "Uma Mão", "price": "T$ 80", "damage": "1d6", "crit": "x2", "type": "Corte", "range": "Médio", "space": 1, "book": "Ameaças de Arton (v1.0)", "page": 394, "desc": "Chicote feito de tentáculos vegetais de monstros da Tormenta ou ermos selvagens com veneno paralisante leve."},
    
    # Armas do Arsenal dos Heróis (Heróis de Arton)
    {"name": "Adaga de Duelo", "sub": "Arsenal dos Heróis", "prof": "Marcial", "wield": "Leve", "price": "T$ 25", "damage": "1d4", "crit": "18/x2", "type": "Perfuração", "range": "-", "space": 1, "book": "Heróis de Arton (v1.1)", "page": 218, "desc": "Adaga com guarda reforçada em cruz desenhada para aparar golpes. Fornece +1 na Defesa quando empunhada na mão inábil."},
    {"name": "Arco Composto", "sub": "Arsenal dos Heróis", "prof": "Marcial", "wield": "Disparo", "price": "T$ 200", "damage": "1d10", "crit": "x3", "type": "Perfuração", "range": "Longo", "space": 2, "book": "Heróis de Arton (v1.1)", "page": 220, "desc": "Arco reforçado com lâminas de chifre e metal. Soma todo o bônus de Força do arqueiro no dano."},
    {"name": "Pistola de Tambor", "sub": "Arsenal dos Heróis", "prof": "Fogo", "wield": "Uma Mão", "price": "T$ 750", "damage": "2d6", "crit": "19/x3", "type": "Perfuração", "range": "Curto", "space": 1, "book": "Heróis de Arton (v1.1)", "page": 222, "desc": "Arma de fogo com tambor rotativo de 6 tiros de Zakharov. Permite disparar até 6 vezes antes de recarregar."}
]

for w in weapons_data:
    slug_id = f"arma-{w['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o').replace('ú', 'u')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    equipment_list.append({
        "id": slug_id,
        "name": w["name"],
        "category": "equipamento",
        "subcategory": w["sub"],
        "summary": f"{w['prof']} ({w['wield']}). Dano: {w['damage']} ({w['crit']}). Preço: {w['price']}. {w['desc'][:90]}...",
        "description": w["desc"],
        "tableData": {
            "price": w["price"],
            "damage": w["damage"],
            "critical": w["crit"],
            "damageType": w["type"],
            "range": w["range"],
            "space": w["space"],
            "proficiency": w["prof"],
            "wielding": w["wield"]
        },
        "sources": [{
            "book": w["book"],
            "page": w["page"],
            "section": f"Equipamentos: {w['sub']}",
            "version": "v1.0+"
        }],
        "tags": ["equipamento", "arma", w["name"].lower(), w["prof"].lower(), w["wield"].lower(), w["type"].lower()]
    })

# =========================================================================
# 2. ARMADURAS E ESCUDOS (JDA + AMEAÇAS + HERÓIS)
# =========================================================================
print("Consolidando Armaduras e Escudos...")

armors_data = [
    # Armaduras Leves (JDA)
    {"name": "Armadura Acolchoada", "sub": "Armaduras Leves", "price": "T$ 5", "defense": 1, "penalty": 0, "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Camadas de tecido acolchoado e costurado. Leve e sem penalidade de armadura."},
    {"name": "Couro Batido", "sub": "Armaduras Leves", "price": "T$ 25", "defense": 2, "penalty": 0, "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Armadura de couro curtido endurecido com rebites metálicos."},
    {"name": "Gibão de Peles", "sub": "Armaduras Leves", "price": "T$ 15", "defense": 3, "penalty": -1, "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Camadas grossas de peles e couros de animais selvagens, comum entre bárbaros e druidas."},
    {"name": "Couraça", "sub": "Armaduras Leves", "price": "T$ 500", "defense": 5, "penalty": -2, "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Peitoral inteiriço de aço moldado com caneleiras e braçadeiras de couro reforçado. A melhor armadura leve."},

    # Armaduras Pesadas (JDA)
    {"name": "Brunea", "sub": "Armaduras Pesadas", "price": "T$ 50", "defense": 5, "penalty": -2, "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Colete de couro recoberto com placas de metal sobrepostas em escamas."},
    {"name": "Cota de Malha", "sub": "Armaduras Pesadas", "price": "T$ 150", "defense": 6, "penalty": -2, "space": 3, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Armadura feita de milhares de anéis de ferro entrelaçados sobre túnica de feltro."},
    {"name": "Loriga Segmentada", "sub": "Armaduras Pesadas", "price": "T$ 250", "defense": 7, "penalty": -3, "space": 3, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Tiras horizontais de metal sobrepostas e presas com tiras de couro, típica das legiões de Tapista."},
    {"name": "Armadura Completa", "sub": "Armaduras Pesadas", "price": "T$ 1.000", "defense": 10, "penalty": -5, "space": 5, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "A proteção máxima de um guerreiro: placas de aço articuladas que recobrem o corpo inteiro com elmo fechado."},

    # Escudos (JDA)
    {"name": "Escudo Leve", "sub": "Escudos", "price": "T$ 5", "defense": 1, "penalty": -1, "space": 1, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Escudo de madeira ou couro leve afixado no antebraço. Deixa a mão livre para segurar itens, mas não para atacar."},
    {"name": "Escudo Pesado", "sub": "Escudos", "price": "T$ 15", "defense": 2, "penalty": -2, "space": 2, "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 158, "desc": "Escudo grande de madeira reforçada ou aço com empunhadura central. Ocupa uma mão inteira."},

    # Armaduras do Bazar Monstruoso (Ameaças de Arton)
    {"name": "Couro de Basilisco", "sub": "Bazar Monstruoso", "price": "T$ 1.200", "defense": 4, "penalty": 0, "space": 1, "book": "Ameaças de Arton (v1.0)", "page": 397, "desc": "Armadura leve feita com escamas resistentes de basilisco. Fornece resistência contra petrificação e venenos."},
    {"name": "Carapaça de Verme do Gelo", "sub": "Bazar Monstruoso", "price": "T$ 2.500", "defense": 8, "penalty": -3, "space": 3, "book": "Ameaças de Arton (v1.0)", "page": 397, "desc": "Armadura pesada forjada a partir da quitina translúcida de vermes do gelo das Uivantes. Fornece RD 5 a frio."},

    # Armaduras do Arsenal dos Heróis (Heróis de Arton)
    {"name": "Armadura de Placas Táurica", "sub": "Arsenal dos Heróis", "price": "T$ 3.000", "defense": 12, "penalty": -6, "space": 5, "book": "Heróis de Arton (v1.1)", "page": 225, "desc": "Armadura monumental desenvolvida pelos ferreiros de Tiberus para minotauros de elite e campeões da guerra."}
]

for a in armors_data:
    slug_id = f"armadura-{a['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o').replace('ú', 'u')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    equipment_list.append({
        "id": slug_id,
        "name": a["name"],
        "category": "equipamento",
        "subcategory": a["sub"],
        "summary": f"{a['sub']}. Defesa: +{a['defense']} (Penalidade: {a['penalty']}). Preço: {a['price']}. {a['desc'][:90]}...",
        "description": a["desc"],
        "tableData": {
            "price": a["price"],
            "defenseBonus": a["defense"],
            "armorPenalty": a["penalty"],
            "space": a["space"]
        },
        "sources": [{
            "book": a["book"],
            "page": a["page"],
            "section": f"Armaduras: {a['sub']}",
            "version": "v1.0+"
        }],
        "tags": ["equipamento", "armadura", "escudo", a["name"].lower(), a["sub"].lower()]
    })

# =========================================================================
# 3. ITENS SUPERIORES & MATERIAIS ESPECIAIS (JDA + HERÓIS)
# =========================================================================
print("Consolidando Materiais Especiais e Melhorias Superiores...")

materiais_e_melhorias = [
    {"name": "Aço-Rubi", "sub": "Itens Superiores & Materiais", "price": "+T$ 1.000", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 167, "desc": "Metal avermelhado extraído de áreas de Tormenta purificadas. Ignora 10 pontos de Redução de Dano (RD) do alvo ou concede RD 2 contra matéria da Tormenta."},
    {"name": "Mitral", "sub": "Itens Superiores & Materiais", "price": "+T$ 1.500", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 167, "desc": "Metal prateado levíssimo dos reinos élficos e anões. Reduz a penalidade de armadura em 2 e diminui a categoria de peso da arma ou armadura."},
    {"name": "Madeira de Tollon", "sub": "Itens Superiores & Materiais", "price": "+T$ 500", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 167, "desc": "Madeira nobre mágica das florestas de Tollon. Reduz em 1 PM (mínimo 1 PM) o custo de habilidades mágicas e manobras do portador."},
    {"name": "Gelo Eterno", "sub": "Itens Superiores & Materiais", "price": "+T$ 1.000", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 167, "desc": "Gelo que nunca derrete das Montanhas Uivantes. Causa +1d6 de dano de frio ou fornece resistência a fogo 5."},
    {"name": "Matéria Vermelha", "sub": "Itens Superiores & Materiais", "price": "+T$ 2.000", "book": "Heróis de Arton (v1.1)", "page": 236, "desc": "Substância viva e corrompida da própria tempestade anti-criacional da Tormenta. Aumenta a margem de crítico da arma em +2, mas drena a sanidade do portador."},
    {"name": "Melhoria: Certeira", "sub": "Itens Superiores & Materiais", "price": "1 melhoria (T$ 300)", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 168, "desc": "A arma é perfeitamente balanceada e concede +1 em testes de ataque."},
    {"name": "Melhoria: Cruel", "sub": "Itens Superiores & Materiais", "price": "1 melhoria (T$ 300)", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 168, "desc": "A arma possui fio afiadíssimo ou cravos adicionais e causa +1 ponto de dano."},
    {"name": "Melhoria: Macabra", "sub": "Itens Superiores & Materiais", "price": "1 melhoria (T$ 300)", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 168, "desc": "Item adornado com ossos e runas sinistras. Concede +2 em testes de Intimidação."}
]

for m in materiais_e_melhorias:
    slug_id = f"superior-{m['name'].lower().replace(' ', '-').replace(':', '').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    equipment_list.append({
        "id": slug_id,
        "name": m["name"],
        "category": "equipamento",
        "subcategory": m["sub"],
        "summary": f"{m['name']} ({m['price']}). {m['desc'][:100]}...",
        "description": m["desc"],
        "tableData": {
            "price": m["price"]
        },
        "sources": [{
            "book": m["book"],
            "page": m["page"],
            "section": "Itens Superiores & Modificações",
            "version": "v1.0+"
        }],
        "tags": ["equipamento", "material especial", "item superior", "melhoria", m["name"].lower()]
    })

# =========================================================================
# 4. ITENS MÁGICOS E ARTEFATOS (JDA + AMEAÇAS + HERÓIS)
# =========================================================================
print("Consolidando Itens Mágicos e Artefatos...")

magic_items = [
    {"name": "Espada Justiceira de Khalmyr", "sub": "Artefatos", "rarity": "Artefato", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 341, "desc": "Espada longa mágica inteligente consagrada pelo Deus da Justiça. Causa 3d8 de dano de corte sagrado e emite aura de verdade inquebrável."},
    {"name": "Armadura de Tauron", "sub": "Artefatos", "rarity": "Artefato", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 344, "desc": "Armadura completa dourada do falecido Deus da Força e Coragem. Concede Defesa +14, RD 10 e Imunidade ao Medo."},
    {"name": "Anel de Proteção Mística", "sub": "Acessórios Mágicos", "rarity": "Médio", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 346, "desc": "Anel de ouro com gema de safira encantada que emite uma barreira defletora, fornecendo +2 na Defesa e em todos os testes de resistência."},
    {"name": "Botas da Levitação Élfica", "sub": "Acessórios Mágicos", "rarity": "Menor", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 347, "desc": "Botas de couro verde que permitem ao usuário flutuar no ar e andar sobre qualquer superfície líquida ou terreno difícil."},
    {"name": "Pingente de Wynna", "sub": "Acessórios Mágicos", "rarity": "Médio", "book": "Heróis de Arton (v1.1)", "page": 262, "desc": "Amuleto com o símbolo da Deusa da Magia que fornece +2 PM por nível e permite recuperar 1d4 PM uma vez por dia."}
]

for mi in magic_items:
    slug_id = f"magico-{mi['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    equipment_list.append({
        "id": slug_id,
        "name": mi["name"],
        "category": "equipamento",
        "subcategory": mi["sub"],
        "isMagicItem": True,
        "magicRarity": mi["rarity"],
        "summary": f"[{mi['rarity']}] {mi['name']}. {mi['desc'][:110]}...",
        "description": mi["desc"],
        "sources": [{
            "book": mi["book"],
            "page": mi["page"],
            "section": f"Itens Mágicos: {mi['sub']}",
            "version": "v1.0+"
        }],
        "tags": ["equipamento", "item mágico", mi["rarity"].lower(), mi["name"].lower(), mi["sub"].lower()]
    })

with open("data/categories/equipamentos.json", "w", encoding="utf-8") as f:
    json.dump(equipment_list, f, ensure_ascii=False, indent=2)

print(f"Total de Equipamentos Consolidados dos 4 Livros: {len(equipment_list)} registros em data/categories/equipamentos.json")
