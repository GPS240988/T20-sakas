# -*- coding: utf-8 -*-
"""
Gerador Canônico de Equipamentos: Heróis de Arton (v1.1)
100% completo, exaustivo e fiel às tabelas e páginas do livro oficial.
"""

from equipment_common import make_item

def get_hda_equipments():
    book = "Heróis de Arton (v1.1)"
    items = []

    # =========================================================================
    # 1. NOVAS ARMAS (Tabela 3-1, Páginas 218-219; Descrições Páginas 219-223)
    # =========================================================================

    # Armas Simples
    items.append(make_item("arma-bastao-ludico", "Bastão Lúdico", "Armas", "Armas Simples", "Corpo a Corpo / Leve", "T$ 5", "1d6", "x2", "Impacto", "-", None, None, 1, book, 218, 
        "A aristocracia de Deheon, Namalkah e outros reinos vem recentemente adotando esportes praticados com tacos ou bastões de madeira. O bastão lúdico é uma arma versátil. Quando você acerta um ataque com um bastão lúdico, se tiver uma pedra em sua mão livre, pode desferir um ataque à distância adicional com essa pedra contra o mesmo alvo sem gastar munição ou ação.", 
        ["esporte", "bastão", "versátil", "namalkah"]))

    items.append(make_item("arma-besta-de-mao", "Besta de Mão", "Armas", "Armas Simples", "Ataque à Distância / Uma Mão", "T$ 30", "1d6", "19", "Perfuração", "Curto", None, None, 1, book, 218, 
        "Esta besta pequena e discreta pode ser disparada com apenas uma mão. É uma arma ocultável (fornece +5 em testes de Ladinagem para ocultá-la). Recarregar uma besta de mão é uma ação de movimento.", 
        ["besta", "ocultável", "uma mão", "ladinagem"]))

    # Armas Marciais - Corpo a Corpo - Leves
    items.append(make_item("arma-adaga-oposta", "Adaga Oposta", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 12", "1d4", "19", "Perfuração", "-", None, None, 1, book, 218, 
        "Muito usada por espadachins como arma secundária, esta adaga possui uma guarda elaborada que a torna mais pesada, mas permite que seja usada defensivamente. A adaga oposta é uma arma ágil que fornece +1 na Defesa se você estiver empunhando outra arma corpo a corpo.", 
        ["adaga", "ágil", "defensiva", "acuidade", "esgrima"]))

    items.append(make_item("arma-agulha-de-ahlen", "Agulha de Ahlen", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 10", "1d4", "19", "Perfuração", "-", None, None, 1, book, 218, 
        "Esta lâmina longa, muito fina e afiada, lembra um estilete. Não possui corte, mas penetra facilmente por entre juntas de armaduras. A agulha de Ahlen é uma arma ágil que ignora 2 pontos da Defesa fornecida por armaduras e escudos.", 
        ["estilete", "ágil", "perfurante", "ahlen", "acuidade"]))

    items.append(make_item("arma-cinquedea", "Cinquedea", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 18", "1d4", "19", "Perfuração", "-", None, None, 1, book, 218, 
        "Esta adaga pesada possui uma lâmina larga na base (com a largura de 'cinco dedos', o que dá origem ao seu nome) que se afunila até uma ponta perfurante afiada. É uma arma ágil e versátil que fornece +2 em testes de manobra desarmar.", 
        ["adaga larga", "ágil", "versátil", "desarmar"]))

    items.append(make_item("arma-dirk", "Dirk", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 15", "1d4", "19", "Perfuração", "-", None, None, 1, book, 218, 
        "Uma adaga longa com lâmina reta de um só gume e ponta afiada reforçada. O dirk é uma arma ágil. Ao atacar com um dirk, se você estiver flanqueando o alvo, sua margem de ameaça com esta arma aumenta em +2.", 
        ["adaga", "ágil", "flanquear", "crítico", "ladino"]))

    items.append(make_item("arma-martelo-leve", "Martelo Leve", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 2", "1d4", "x4", "Impacto", "Curto", None, None, 1, book, 218, 
        "Uma versão pequena do martelo de guerra, balanceada para ser usada em combate veloz ou arremessada contra oponentes. Pode ser arremessada.", 
        ["martelo", "arremesso", "crítico x4"]))

    # Armas Marciais - Corpo a Corpo - Uma Mão
    items.append(make_item("arma-espada-larga", "Espada Larga", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 8", "2d4", "x2", "Corte", "-", None, None, 1, book, 218, 
        "Muito comum entre infantarias e companhias de mercenários, tem a lâmina menos afiada, mas mais larga e pesada, que a da espada longa, desferindo golpes de grande contusão cortante.", 
        ["espada", "mercenário", "pesada"]))

    items.append(make_item("arma-espadim", "Espadim", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 300", "1d8", "20", "Corte", "-", None, None, 1, book, 218, 
        "Uma espada elegante com guarnições de prata e cabo de marfim, portada por oficiais militares e nobres como símbolo de patente e autoridade. É uma arma ágil que fornece +2 em testes de Diplomacia e Nobreza.", 
        ["nobreza", "oficial", "ágil", "diplomacia"]))

    items.append(make_item("arma-maca-estrela", "Maça-Estrela", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 20", "2d4", "x2", "Impacto e perfuração", "-", None, None, 1, book, 218, 
        "Uma maça com uma esfera de aço cravejada de pontas piramidais afiadas, combinando contusão violenta com perfuração profunda.", 
        ["maça", "cravos", "duplo tipo de dano"]))

    items.append(make_item("arma-serrilheira", "Serrilheira", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 25", "1d6", "19", "Corte", "-", None, None, 1, book, 218, 
        "Uma espada reta cujo gume é serrilhado como dentes de tubarão. A serrilheira é uma arma ágil e pungente que causa sangramento severo em acertos críticos.", 
        ["espada serrilhada", "ágil", "sangramento"]))

    # Armas Marciais - Corpo a Corpo - Duas Mãos
    items.append(make_item("arma-bico-de-corvo", "Bico de Corvo", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 15", "1d8", "x3", "Impacto/perfuração", "-", None, None, 2, book, 218, 
        "Uma haste de madeira com cabeça de martelo de um lado e um longo bico pontiagudo curvado do outro, projetado para perfurar elmos de cavaleiros.", 
        ["haste", "perfurar elmos", "crítico x3"]))

    items.append(make_item("arma-desmontador", "Desmontador", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 20", "-", "-", "-", "-", None, None, 2, book, 218, 
        "Uma haste longa com ganchos e pontas curvas opostas, feita especialmente para derrubar cavaleiros de suas montarias. É uma arma alongada que concede +4 em testes para derrubar cavaleiros.", 
        ["haste", "derrubar", "anti-cavalaria", "alongada"]))

    items.append(make_item("arma-espada-de-execucao", "Espada de Execução", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 75", "2d6", "18/x4", "Corte", "-", None, None, 2, book, 218, 
        "Uma lâmina de dois gumes sem ponta, pesadíssima e afiada como navalha, usada por carrascos e verdugos de reinos imperiais. Exige muita força para manejo.", 
        ["carrasco", "execução", "crítico devastador"]))

    items.append(make_item("arma-lanca-de-justa", "Lança de Justa", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 3", "1d8", "x2", "Perfuração", "-", None, None, 2, book, 218, 
        "Lança de madeira leve com ponta rombuda ou acolchoada projetada especificamente para torneios de cavaleiros sem causar dano letal.", 
        ["torneio", "justa", "não letal", "cavalaria"]))

    items.append(make_item("arma-malho", "Malho", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 8", "1d10", "x2", "Impacto", "-", None, None, 2, book, 218, 
        "Um martelo pesado de madeira maciça ou ferro bruto, usado na construção e marretagem que esmaga oponentes no campo de batalha.", 
        ["marreta", "impacto", "duas mãos"]))

    items.append(make_item("arma-martelo-longo", "Martelo Longo", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 12", "2d4", "x4", "Impacto/perfuração", "-", None, None, 2, book, 218, 
        "Uma haste longa encimada por cabeça de martelo de guerra e ponta de lança. É uma arma alongada com multiplicador de crítico formidável.", 
        ["alongada", "martelo de haste", "crítico x4"]))

    items.append(make_item("arma-tan-korak", "Tan-korak", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 40", "1d8", "x2", "Impacto", "-", None, None, 2, book, 218, 
        "Arma tradicional dos orcs e guerreiros do leste, composta por dois bastões pesados unidos por elos de corrente reforçados. É uma arma ágil, dupla e versátil.", 
        ["orc", "dupla", "versátil", "ágil"]))

    # Armas Marciais - Distância
    items.append(make_item("arma-tai-tai", "Tai-tai", "Armas", "Armas Marciais", "Ataque à Distância / Uma Mão", "T$ 60", "2d4", "x2", "Impacto", "Médio", None, None, 2, book, 218, 
        "Um propulsor de dardos pesado dos povos da floresta que lança projéteis com enorme velocidade e impacto contundente.", 
        ["propulsor", "dardo", "distância"]))

    items.append(make_item("arma-arco-montado", "Arco Montado", "Armas", "Armas Marciais", "Ataque à Distância / Duas Mãos", "T$ 45", "1d6", "x3", "Perfuração", "Médio", None, None, 2, book, 218, 
        "Arco recurvo composto de madeira, osso e tendão de Namalkah, desenvolvido especificamente para disparos em alta velocidade sobre montarias.", 
        ["namalkah", "montaria", "arco recurvo"]))

    items.append(make_item("arma-besta-dupla", "Besta Dupla", "Armas", "Armas Marciais", "Ataque à Distância / Duas Mãos", "T$ 125", "1d8", "19", "Perfuração", "Médio", None, None, 2, book, 218, 
        "Uma besta que possui dois arcos sobrepostos e dois gatilhos independentes, permitindo disparar dois virotes simultaneamente ou em turnos consecutivos.", 
        ["besta", "dois disparos", "mecânica"]))

    # Armas Exóticas
    items.append(make_item("arma-kimbata", "Kimbata", "Armas", "Armas Exóticas", "Corpo a Corpo / Leve", "T$ 12", "1d4", "18", "Corte", "-", None, None, 1, book, 219, 
        "Faca curva em formato de meia-lua com argola na extremidade do cabo. É uma arma ocultável e surpreendente. Ao atacar um alvo desprevenido, você pode usar Furtividade em vez de Luta no ataque.", 
        ["adaga de meia-lua", "ocultável", "furtividade no ataque"]))

    items.append(make_item("arma-clava-grao", "Clava-Grão", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 90", "1d6", "x2", "Impacto", "-", None, None, 1, book, 219, 
        "Clava sagrada dos monges de Lin-Fei em Tamu-ra, com cabo oco preenchido com sementes e esferas de chumbo que geram ressonância mística a cada impacto.", 
        ["tamura", "monge", "místico"]))

    items.append(make_item("arma-espada-canora", "Espada Canora", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 50", "1d6", "19", "Perfuração", "-", None, None, 1, book, 219, 
        "Espada de lâmina vazada com ranhuras sonoras que emite um assobio agudo hipnótico ao ser brandida. Concede +2 em testes de Atuação e intimidação.", 
        ["som", "bardo", "ágil", "acuidade"]))

    items.append(make_item("arma-espada-gadanho", "Espada-Gadanho", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 40", "1d6", "18", "Corte", "-", None, None, 1, book, 219, 
        "Espada com a lâmina afiada pelo lado interno da curvatura, permitindo puxar e enganchar as defesas do adversário para desarmá-lo ou derrubá-lo.", 
        ["curva invertida", "gancho", "desarmar"]))

    items.append(make_item("arma-khopesh", "Khopesh", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 20", "1d8", "19/x3", "Corte", "-", None, None, 1, book, 219, 
        "Espada em foice tradicional de impérios ancestrais do deserto. A curvatura de sua lâmina forma um gancho versátil que concede +2 em testes para derrubar.", 
        ["deserto", "espada em foice", "derrubar", "crítico 19/x3"]))

    items.append(make_item("arma-lanca-de-falange", "Lança de Falange", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 15", "1d8", "x3", "Perfuração", "Curto", None, None, 1, book, 219, 
        "Lança reforçada usada por formações de legionários. Pode ser empunhada com uma mão enquanto você usa um escudo pesado sem sofrer penalidades.", 
        ["falange", "legião", "escudo pesado", "uma mão"]))

    items.append(make_item("arma-machado-de-haste", "Machado de Haste", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 40", "1d8/1d10", "x3", "Corte", "-", None, None, 1, book, 219, 
        "Machado montado sobre cabo alongado de ferro, permitindo uso versátil com uma ou duas mãos para golpear com grande alavancagem.", 
        ["machado", "uma ou duas mãos", "alavancagem"]))

    items.append(make_item("arma-rapieira", "Rapieira", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 50", "1d8", "18", "Perfuração", "-", None, None, 1, book, 219, 
        "A lâmina nobre suprema de duelistas artonianos. Lâmina longa e delgada com guarda em cesta complexa. É uma arma ágil que fornece +1 na Defesa quando usada em duelo.", 
        ["duelista", "esgrima", "ágil", "acuidade", "crítico 18"]))

    items.append(make_item("arma-marrao", "Marrão", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos", "T$ 50", "4d4", "x2", "Impacto", "-", None, None, 2, book, 219, 
        "Marreta colossal maciça de ferro e rocha minerada em Doherimm. Requer força bruta descomunal e causa dano de concussão maciço.", 
        ["marreta gigante", "anão", "esmagar", "dano maciço"]))

    items.append(make_item("arma-montante-cinetico", "Montante Cinético", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos", "T$ 3.000", "2d6", "19/x4", "Corte", "-", None, None, 2, book, 219, 
        "Uma arma mecânica fabulosa desenvolvida por armeiros de Yuvalin, que armazena energia cinética em molas internas durante o balanço para explodir em impactos brutais.", 
        ["engenhoca", "yuvalin", "mola", "crítico 19/x4"]))

    items.append(make_item("arma-boleadeira", "Boleadeira", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão", "T$ 12", "1d4", "x2", "Impacto", "Curto", None, None, 1, book, 219, 
        "Três esferas de chumbo ligadas por tiras de couro trançado. Ao acertar um ataque com uma boleadeira, você pode fazer um teste de manobra derrubar como ação livre.", 
        ["arremesso", "derrubar", "namalkah", "enredar"]))

    items.append(make_item("arma-chakram", "Chakram", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão", "T$ 15", "1d6", "x3", "Corte", "Curto", None, None, 1, book, 219, 
        "Um disco de metal circular com o gume externo afiado como uma navalha. Pode ser arremessado e ricocheteia retornando à mão do arremessador habilidoso.", 
        ["disco", "arremesso", "crítico x3", "retorno"]))

    items.append(make_item("arma-arco-de-guerra", "Arco de Guerra", "Armas", "Armas Exóticas", "Ataque à Distância / Duas Mãos", "T$ 200", "1d12", "x3", "Perfuração", "Médio", None, None, 2, book, 219, 
        "Um arco colossal com envergadura superior a dois metros que exige força descomunal para ser puxado. Aplica o dobro do seu modificador de Força às rolagens de dano.", 
        ["arco colossal", "força dobrada", "disparo maciço"]))

    items.append(make_item("arma-balestra", "Balestra", "Armas", "Armas Exóticas", "Ataque à Distância / Duas Mãos", "T$ 180", "1d12", "19", "Perfuração", "Médio", None, None, 2, book, 219, 
        "Uma besta de aço inteiriço com arco quadruplicado de extrema potência. Recarregar uma balestra é uma ação padrão.", 
        ["besta pesada", "aço", "perfurante"]))

    items.append(make_item("arma-besta-de-repeticao", "Besta de Repetição", "Armas", "Armas Exóticas", "Ataque à Distância / Duas Mãos", "T$ 250", "1d8", "19", "Perfuração", "Médio", None, None, 2, book, 219, 
        "Possui um carregador superior com 5 virotes e uma alavanca de recarga rápida que permite recarregar a besta como uma ação livre.", 
        ["carregador", "recarga livre", "disparo rápido"]))

    # Armas de Fogo HdA
    items.append(make_item("arma-garrucha", "Garrucha", "Armas", "Armas de Fogo", "Ataque à Distância / Leve", "T$ 250", "2d4", "19/x3", "Perfuração", "Curto", None, None, 1, book, 219, 
        "Esta pequena arma de fogo do tamanho de uma mão espalmada pode ser facilmente escondida em mangas ou dobras de roupas. É uma arma ocultável e surpreendente; recarregá-la é uma ação padrão.", 
        ["arma de fogo", "ocultável", "pólvora"]))

    items.append(make_item("arma-canhao-portatil", "Canhão Portátil", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos", "T$ 3.000", "4d10", "19/x3", "Impacto", "Curto", None, None, 2, book, 219, 
        "Um pequeno canhão de ferro montado sobre uma armação com correias para disparar esferas de ferro maciço. Causa recuo violento e estrondo ensurdecedor.", 
        ["canhão", "dano massivo", "artilharia", "pólvora"]))

    items.append(make_item("arma-sifao-caustico", "Sifão Cáustico", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos", "T$ 600", "4d6", "x2", "Ácido", "Especial", None, None, 2, book, 219, 
        "Um projetor de fluidos químicos pressurizados com tanque de vidro blindado que cospe jatos corrosivos em cone de 6 metros.", 
        ["ácido", "cone", "área", "alquimia"]))

    # =========================================================================
    # 2. NOVAS ARMADURAS & ESCUDOS (Tabela 3-3, Página 224; Páginas 224-227)
    # =========================================================================

    # Armaduras Leves
    items.append(make_item("armadura-armadura-sensual", "Armadura Sensual", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 55", None, None, None, None, "+1", "0", 2, book, 224, 
        "Feita para revelar mais do que proteger, com tiras de couro e placas douradas estrategicamente posicionadas. Concede +1 em testes de Enganação e Diplomacia.", 
        ["sensual", "social", "sem penalidade"]))

    items.append(make_item("armadura-armadura-de-folhas", "Armadura de Folhas", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 75", None, None, None, None, "+2", "0", 2, book, 224, 
        "Costurada com folhas tratadas com óleos alquímicos e seiva encantada. Se for treinado em Sobrevivência, você recebe +2 PM adicionais.", 
        ["druida", "natureza", "pm extra", "sem penalidade"]))

    items.append(make_item("armadura-armadura-de-engenhoqueiro-goblin", "Armadura de Engenhoqueiro Goblin", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 85", None, None, None, None, "+3", "–2 a –10", 2, book, 224, 
        "Cheia de bolsos, ganchos e alças para acoplar engenhocas. Para cada engenhoca vestida nela, o bônus de Defesa aumenta em +1 (máx +5), aumentando a penalidade em -2.", 
        ["goblin", "engenhocas", "inventor", "customizável"]))

    items.append(make_item("armadura-cota-de-moedas", "Cota de Moedas", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 350", None, None, None, None, "+4", "-3", 2, book, 224, 
        "Feita de milhares de moedas de prata e ouro costuradas em escamas. Fornece +2 em testes de Diplomacia e Nobreza ao negociar.", 
        ["moedas", "ouro", "nobreza", "ostentação"]))

    items.append(make_item("armadura-colete-fora-da-lei", "Colete Fora da Lei", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 750", None, None, None, None, "+5", "-5", 2, book, 224, 
        "Um colete de couro endurecido reforçado com placas de aço embutidas usado por pistoleiros e bandoleiros do oeste.", 
        ["fora da lei", "pistoleiro", "couro reforçado"]))

    # Armaduras Pesadas
    items.append(make_item("armadura-brigantina", "Brigantina", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 75", None, None, None, None, "+6", "0", 5, book, 224, 
        "Placas de aço rebitadas entre camadas de linho e lona grossa. Uma armadura pesada econômica e funcional sem penalidade de armadura excessiva.", 
        ["placas", "econômica", "pesada"]))

    items.append(make_item("armadura-armadura-de-chumbo", "Armadura de Chumbo", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 750", None, None, None, None, "+7", "-5", 5, book, 224, 
        "Uma armadura colossal forrada de chumbo maciço. Fornece Resistência a Magia +2 e imunidade a efeitos de adivinhação e detecção mental.", 
        ["chumbo", "anti-magia", "adivinhação", "pesada"]))

    items.append(make_item("armadura-armadura-de-justa", "Armadura de Justa", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 1.200", None, None, None, None, "+9", "-5", 5, book, 224, 
        "Meia armadura de placas assimétricas reforçadas especialmente para o lado da lança. Fornece Defesa +11 contra ataques frontais de investidas.", 
        ["justa", "torneio", "cavalaria", "pesada"]))

    items.append(make_item("armadura-armadura-de-hussardo-alado", "Armadura de Hussardo Alado", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 4.500", None, None, None, None, "+10", "-6", 5, book, 224, 
        "Armadura de placas completas encimada por duas asas de penas presas nas costas que emitem um sibilo apavorante em investidas (+2 em Intimidação e bônus contra ataques à distância).", 
        ["hussardo", "asas", "cavalaria alada", "pesada"]))

    items.append(make_item("armadura-armadura-de-pedra", "Armadura de Pedra", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 5.500", None, None, None, None, "+12", "-5", 5, book, 224, 
        "Esculpida em rocha densa e granito anão de Doherimm com juntas reforçadas por runas. Fornece redução de dano RD 5 e bônus máximo de proteção.", 
        ["pedra", "anão", "doherimm", "rd 5", "pesada máxima"]))

    # Escudos
    items.append(make_item("armadura-broquel", "Broquel", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 25", None, None, None, None, "—", "-1", 0.5, book, 224, 
        "Pequeno escudo redondo de aço preso ao antebraço que deixa a mão livre para segurar itens. Permite desviar de ataques usando a reação com teste de Acrobacia.", 
        ["broquel", "mão livre", "esgrima", "acrobacia"]))

    items.append(make_item("armadura-escudo-de-vime", "Escudo de Vime", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 15", None, None, None, None, "+2", "-2", 2, book, 224, 
        "Escudo leve trançado em vime tratado e reforçado com couro cru. Muito leve, flutua na água e fornece bônus em testes de Atletismo para natação.", 
        ["vime", "leve", "flutuar", "escudo"]))

    items.append(make_item("armadura-escudo-torre", "Escudo Torre", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 45", None, None, None, None, "+2", "-4", 2, book, 224, 
        "Um enorme escudo retangular que cobre quase todo o corpo. Você pode gastar uma ação de movimento para fincá-lo no solo e receber cobertura total.", 
        ["torre", "cobertura total", "defesa pesada"]))

    items.append(make_item("armadura-sagna", "Sagna", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 20", None, None, None, None, "+2", "-3", 2, book, 224, 
        "Grande escudo de madeira desenvolvido por devotos do Oceano que pode ser usado como prancha para deslizar sobre as ondas.", 
        ["oceano", "mar", "prancha", "escudo"]))

    # =========================================================================
    # 3. NOVOS ITENS GERAIS (Tabela 3-4, Páginas 228-229; Páginas 230-241)
    # =========================================================================

    # Equipamento de Aventura HdA
    aventura_hda = [
        ("item-abaco", "Ábaco", "T$ 45", 1, "Moldura de madeira com contas deslizantes para cálculos rápidos. Fornece +2 em testes de Ofício (administração/mercador) e Investigação contábil."),
        ("item-ampulheta", "Ampulheta", "T$ 45", 1, "Instrumento de vidro e areia para medição precisa do tempo em testes de perícia e experimentos alquímicos."),
        ("item-aparelho-de-cha", "Aparelho de Chá", "T$ 30", 1, "Bule de porcelana fina e xícaras para cerimônias de chá que concedem +1 em Diplomacia durante o evento."),
        ("item-astrolabio", "Astrolábio", "T$ 90", 1, "Instrumento astronômico de latão que fornece +2 em testes de Navegação e Sobrevivência guiando-se pelas estrelas."),
        ("item-armacao-para-mochila", "Armação para Mochila", "T$ 50", 0, "Estrutura de madeira e tiras acolchoadas que redistribui o peso da mochila, aumentando a capacidade em +2 espaços."),
        ("item-asas-do-texugo", "Asas do Texugo", "T$ 200", 2, "Arnês com asas de lona e hastes de bambu dobráveis que reduz o dano de queda em 6d6."),
        ("item-bainha-adornada", "Bainha Adornada", "T$ 100", 1, "Bainha de couro lavrado com detalhes de prata que concede +1 em testes de Diplomacia quando a arma está embainhada."),
        ("item-bussola", "Bússola", "T$ 45", 1, "Agulha magnética flutuante em caixa de latão que aponta sempre para o Norte de Arton. Concede +2 em Sobrevivência para orientação."),
        ("item-cinto-de-utilidades", "Cinto de Utilidades", "T$ 50", 1, "Cinto com múltiplos bolsos e mosquetões para guardar até 6 itens minúsculos que podem ser sacados como ação livre."),
        ("item-condecoracao-militar", "Condecoração Militar", "T$ —", 1, "Medalha de bravura conferida por uma ordem de cavaleiros ou exército que concede +1 em Nobreza e Intimidação."),
        ("item-dente-falso", "Dente Falso", "T$ 300", 0, "Dente postiço oco para guardar uma dose de veneno, ácido ou gazua miniaturizada indetectável por revistas normais."),
        ("item-diagrama-anatomico", "Diagrama Anatômico", "T$ 75", 1, "Caderno ilustrado com a fisiologia de humanoides e monstros que concede +2 em Cura para cirurgias e primeiros socorros."),
        ("item-espelho-refletor", "Espelho Refletor", "T$ 45", 1, "Espelho parabólico montado em suporte para concentrar feixes de luz ou fazer sinais a até 5km em dias claros."),
        ("item-estetoscopio", "Estetoscópio", "T$ 60", 1, "Tubo auditivo acústico que concede +2 em Percepção para ouvir através de portas e paredes e para testes de Cura."),
        ("item-estrepes-bolsa-para-3m", "Estrepes (bolsa para 3m)", "T$ 5", 1, "Cravos de ferro de quatro pontas que transformam um quadrado de 3m em terreno difícil e causam dano e lentidão a quem passar."),
        ("item-favor-da-pessoa-amada", "Favor da Pessoa Amada", "T$ —", 1, "Lenço perfumado ou fita dada por alguém especial. Uma vez por cena, permite rerrolar um teste de resistência falho."),
        ("item-lampiao-de-foco", "Lampião de Foco", "T$ 15", 1, "Lampião com espelho côncavo que projeta um cone de luz brilhante de 18m em linha reta."),
        ("item-leque", "Leque", "T$ 3", 1, "Leque de seda e varetas de bambu. Concede +1 em testes de Enganação e Diplomacia para ocultar expressões faciais na corte."),
        ("item-livro-de-metodos-anti-nimb", "Livro de Métodos Anti-Nimb", "T$ 100", 1, "Tratado estatístico sobre probabilidade e contenção do caos que concede +1 em testes de resistência contra efeitos de sorte/azar."),
        ("item-lupa", "Lupa", "T$ 30", 1, "Lente convergente de cristal que concede +2 em testes de Investigação e Ladinagem para examinar pistas e detalhes diminutos."),
        ("item-mapa", "Mapa", "T$ 30", 1, "Mapa cartográfico detalhado de uma região de Arton que fornece +2 em testes de Conhecimento e Sobrevivência referentes ao local."),
        ("item-mecanismo-de-mola", "Mecanismo de Mola", "T$ 25", 1, "Mecanismo de liberação rápida sob a manga que ejeta uma arma leve ou poção na mão do usuário como reação."),
        ("item-mochila-discreta", "Mochila Discreta", "T$ 20", 1, "Mochila camuflada com forro duplo que fornece +5 em Ladinagem para ocultar objetos dentro dela."),
        ("item-prancheta", "Prancheta", "T$ 5", 1, "Prancha rígida de madeira com grampo para anotações e desenhos rápidos no campo de batalha."),
        ("item-sinete", "Sinete", "T$ 50", 1, "Anel com carimbo metálico personalizado para lacrar cartas oficiais com cera quente.")
    ]
    for aid, aname, aprice, aspace, adesc in aventura_hda:
        items.append(make_item(aid, aname, "Itens Gerais", "Equipamento de Aventura", "Aventura", aprice, None, None, None, None, None, None, aspace, book, 228, adesc, ["aventura", "utilitário"]))

    # Ferramentas Gerais & Instrumentos Musicais
    ferramentas_hda = [
        ("item-apito-de-caca", "Apito de Caça", "Ferramentas Gerais", "T$ 6", 1, "Apito ultrassônico audível apenas por animais e monstros caninos."),
        ("item-baralho-marcado", "Baralho Marcado", "Ferramentas Gerais", "T$ 15", 1, "Cartas com ranhuras sutis no verso que fornecem +5 em Jogos de Azar com Enganação."),
        ("item-espelho-cirurgico", "Espelho Cirúrgico", "Ferramentas Gerais", "T$ 12", 1, "Espelho côncavo acoplado à cabeça que direciona luz para procedimentos de Cura."),
        ("item-estandarte", "Estandarte", "Ferramentas Gerais", "T$ 15", 1, "Bandeira militar que concede +1 em testes de Vontade para aliados em alcance curto."),
        ("item-estandarte-portatil", "Estandarte Portátil", "Ferramentas Gerais", "T$ 20", 1, "Versão dobrável fixada na armadura do comandante que mantém o benefício de comando em movimento."),
        ("item-molde-pre-fabricado", "Molde Pré-Fabricado", "Ferramentas Gerais", "T$ 500", 1, "Forma metálica de fundição rápida que reduz o tempo de fabricação de itens metálicos pela metade."),
        ("item-clarim-deheoni", "Clarim Deheoni", "Instrumentos Musicais", "T$ 150", 1, "Trombeta militar dourada de Deheon cujo toque marcial inspira coragem a combatentes."),
        ("item-citara-heptatonica", "Cítara Heptatônica", "Instrumentos Musicais", "T$ 250", 1, "Instrumento clássico de sete cordas que harmoniza melodias refinadas para cortesãos."),
        ("item-cornamusa-de-doherimm", "Cornamusa de Doherimm", "Instrumentos Musicais", "T$ 750", 2, "Gaita de fole anã retumbante cujos sons graves ecoam por salões subterrâneos."),
        ("item-flauta-sar-allan", "Flauta Sar-Allan", "Instrumentos Musicais", "T$ 150", 1, "Flauta doce e melodiosa típica dos nômades do Deserto da Perdição."),
        ("item-gaita-de-foles", "Gaita de Foles", "Instrumentos Musicais", "T$ 500", 1, "Instrumento tradicional de tribos das montanhas com som penetrante e inconfundível."),
        ("item-lira-de-casco-de-tartaruga", "Lira de Casco de Tartaruga", "Instrumentos Musicais", "T$ 300", 1, "Feita com a carapaça de quelônios marinhos, emite notas suaves e cristalinas."),
        ("item-marionetes", "Marionetes", "Instrumentos Musicais", "T$ 90", 1, "Bonecos articulados de madeira e fios para encenar peças teatrais que cativam o público."),
        ("item-pandeiro-das-estradas", "Pandeiro das Estradas", "Instrumentos Musicais", "T$ 200", 1, "Pandeiro com platinelas de bronze muito popular entre bardos itinerantes."),
        ("item-tamborete-marcial", "Tamborete Marcial", "Instrumentos Musicais", "T$ 80", 1, "Pequeno tambor amarrado à cintura para marcar o ritmo de marcha de esquadrões."),
        ("item-trombeta-tapistana", "Trombeta Tapistana", "Instrumentos Musicais", "T$ 300", 1, "Trombeta curvada de bronze pesada usada pelas legiões de minotauros."),
        ("item-violino-soprano", "Violino Soprano", "Instrumentos Musicais", "T$ 300", 1, "Violino de afinação aguda e límpida que emociona multidões em concertos.")
    ]
    for fid, fname, fsub, fprice, fspace, fdesc in ferramentas_hda:
        items.append(make_item(fid, fname, "Itens Gerais", fsub, "Ferramenta / Instrumento", fprice, None, None, None, None, None, None, fspace, book, 228, fdesc, ["música", "ferramenta", "arte"]))

    # Vestuário HdA
    vestuario_hda = [
        ("item-avental-de-forja", "Avental de Forja", "T$ 75", 1, "Avental de couro curtido pesado que fornece redução de fogo 2 e +2 em Ofício (armeiro/ferreiro)."),
        ("item-camisolao", "Camisolão", "T$ 12", 1, "Túnica folgada de dormir que proporciona descanso revigorante sem aperto de cintas."),
        ("item-capa-com-dragonas", "Capa com Dragonas", "T$ 50", 1, "Capa militar com insígnias nos ombros que confere +1 em Nobreza e Diplomacia militar."),
        ("item-casaca-de-apetrechos", "Casaca de Apetrechos", "T$ 75", 0, "Casaco com dezenas de compartimentos internos ocultos que aumenta a capacidade de carga vestida em +2 espaços."),
        ("item-chapeu-emplumado", "Chapéu Emplumado", "T$ 50", 1, "Chapéu de abas largas com longas plumas de pássaros exóticos que concede +1 em Atuação e Diplomacia."),
        ("item-elmo-leve", "Elmo Leve", "T$ 15", 1, "Capacete de couro ou metal leve que protege a cabeça sem prejudicar a audição ou visão."),
        ("item-elmo-pesado", "Elmo Pesado", "T$ 200", 1, "Elmo de aço inteiriço com visor articulado que concede +1 na Defesa contra ataques críticos."),
        ("item-jaqueta-de-couro", "Jaqueta de Couro", "T$ 15", 1, "Jaqueta reforçada e estilosa muito usada por pilotos, aventureiros e marinheiros."),
        ("item-luva-de-falcoaria", "Luva de Falcoaria", "T$ 15", 1, "Luva de couro grosso que vai até o cotovelo para pouso seguro de aves de rapina de caça."),
        ("item-luva-magnetica", "Luva Magnética", "T$ 20", 1, "Luva com ímãs integrados na palma que atrai objetos metálicos leves soltos a até 1,5m."),
        ("item-mascara-bucal", "Máscara Bucal", "T$ 3", 1, "Máscara de pano que cobre boca e nariz, fornecendo +2 em Fortitude contra poeira e gases irritantes."),
        ("item-mascara-completa", "Máscara Completa", "T$ 15", 1, "Máscara que cobre todo o rosto, ocultando totalmente a identidade do usuário."),
        ("item-mascara-de-baile", "Máscara de Baile", "T$ 25", 1, "Máscara aristocrática decorada com plumas e veludo para festas de gala e intrigas."),
        ("item-mascara-de-soldador", "Máscara de Soldador", "T$ 50", 1, "Máscara de ferro com visor de vidro escuro que protege contra clarões ofuscantes e calor intenso."),
        ("item-monoculo", "Monóculo", "T$ 50", 1, "Lente única de cristal encaixada no olho que confere +1 em testes de Investigação e Nobreza."),
        ("item-oculos-de-aeronauta", "Óculos de Aeronauta", "T$ 15", 1, "Óculos de couro com lentes de vidro resistentes ao vento para pilotos de balões e montarias voadoras."),
        ("item-palmar", "Palmar", "T$ 12", 1, "Protetor de couro para as palmas das mãos que fornece +1 em Atletismo para escalada e uso de cordas."),
        ("item-peruca", "Peruca", "T$ 20", 1, "Peruca de fios tratados para compor disfarces ou seguir a moda nobre dos salões reais."),
        ("item-rondel", "Rondel", "T$ 150", 1, "Disco de metal decorado preso ao ombro ou peitoral que exibe o brasão heráldico da linhagem."),
        ("item-roupao-elegante", "Roupão Elegante", "T$ 150", 1, "Roupão de seda acetinada usado por cortesãos em aposentos privativos para receber visitas íntimas."),
        ("item-rufo", "Rufo", "T$ 25", 1, "Gola circular pregueada de linho engomado que impõe postura ereta e formalidade na corte."),
        ("item-sapatos-confortaveis", "Sapatos Confortáveis", "T$ 6", 1, "Calçados macios de camurça que evitam bolhas e cansaço em caminhadas urbanas longas."),
        ("item-sapatos-de-salto-alto", "Sapatos de Salto Alto", "T$ 18", 1, "Calçados aristocráticos femininos que aumentam a estatura e o porte em recepções sociais."),
        ("item-veste-acolchoada", "Veste Acolchoada", "T$ 60", 1, "Túnica de algodão acolchoado que pode ser vestida sob armaduras para amortecer impactos contundentes.")
    ]
    for vid, vname, vprice, vspace, vdesc in vestuario_hda:
        items.append(make_item(vid, vname, "Itens Gerais", "Vestuário", "Vestuário", vprice, None, None, None, None, None, None, vspace, book, 228, vdesc, ["vestuário", "moda", "estilo"]))

    # Esotéricos HdA
    items.append(make_item("item-compasso-mistico", "Compasso Místico", "Itens Gerais", "Esotéricos", "Foco Geométrico", "T$ 600", None, None, None, None, None, None, 1, book, 228, 
        "Um compasso articulado de prata e ouro. Ao lançar magias de área (esfera, cone, linha), você pode aumentar ou diminuir a área de efeito em +1,5m.", 
        ["esotérico", "área", "geometria", "mágico"]))

    items.append(make_item("item-flauta-convocadora", "Flauta Convocadora", "Itens Gerais", "Esotéricos", "Foco de Invocação", "T$ 300", None, None, None, None, None, None, 1, book, 228, 
        "Uma flauta de osso gravada com melodias dimensionais. Reduz em -1 PM o custo de magias de convocação de monstros e parceiros.", 
        ["esotérico", "convocação", "invocação", "pm"]))

    items.append(make_item("item-mandala-onirica", "Mandala Onírica", "Itens Gerais", "Esotéricos", "Foco de Ilusão", "T$ 300", None, None, None, None, None, None, 1, book, 228, 
        "Um círculo de fios de seda trançados com penas e cristais que aumenta em +1 a CD de suas magias da escola de Ilusão e Encantamento.", 
        ["esotérico", "ilusão", "encantamento", "cd"]))

    items.append(make_item("item-varinha-armamentista", "Varinha Armamentista", "Itens Gerais", "Esotéricos", "Foco de Combate", "T$ 600", None, None, None, None, None, None, 1, book, 228, 
        "Varinha reforçada com ponta metálica que permite usar o bônus de Ataque Mágico em ataques corpo a corpo com a própria varinha.", 
        ["esotérico", "combate", "mago de batalha"]))

    # Alquímicos HdA
    alquimicos_hda = [
        ("item-acido-concentrado", "Ácido Concentrado", "Alquímicos - Preparados", "T$ 60", "Dose pura de ácido corrosivo que causa 4d4 pontos de dano de ácido e corrói 1 ponto de armadura do alvo."),
        ("item-analgesico", "Analgésico", "Alquímicos - Preparados", "T$ 60", "Tintura que amortece dores, suprimindo condições de abalado e fraco por 1 hora."),
        ("item-estalinho-gury", "Estalinho Gury", "Alquímicos - Preparados", "T$ 30", "Pequeno explosivo de impacto que cria um estampido ensurdecedor, ofuscando e distraindo inimigos adjacentes."),
        ("item-extrato-de-gelo-eterno", "Extrato de Gelo Eterno", "Alquímicos - Preparados", "T$ 60", "Frasco com fluido criogênico que causa 3d6 de dano de frio e congela superfícies."),
        ("item-extrato-de-oxxdon", "Extrato de Oxxdon", "Alquímicos - Preparados", "T$ 180", "Extrato raríssimo que recupera 4d4 pontos de mana instantaneamente ao ser ingerido."),
        ("item-frasco-abissal", "Frasco Abissal", "Alquímicos - Preparados", "T$ 300", "Líquido negro volátil que explode em nuvem de escuridão mágica e dano de trevas."),
        ("item-po-de-cinza", "Pó de Cinza", "Alquímicos - Preparados", "T$ 5", "Cinzas tratadas para apagar pegadas e dificultar rastreamento com Sobrevivência."),
        ("item-po-do-aparecimento", "Pó do Aparecimento", "Alquímicos - Preparados", "T$ 30", "Pó luminoso que revela criaturas e objetos invisíveis em um raio de 3m."),
        ("item-visco-persistente", "Visco Persistente", "Alquímicos - Preparados", "T$ 25", "Cola alquímica viscosa que prende pés e mãos em superfícies por uma cena."),
        ("item-cristal-reflexivo", "Cristal Reflexivo", "Alquímicos - Catalisadores", "T$ 30", "Cristal lapidado que reflete e amplifica feixes luminosos de magias de luz."),
        ("item-essencia-fantasmal", "Essência Fantasmal", "Alquímicos - Catalisadores", "T$ 30", "Fluido ectoplasmático que permite que magias afetem criaturas incorpóreas normalmente."),
        ("item-noz-saltadora", "Noz Saltadora", "Alquímicos - Catalisadores", "T$ 90", "Noz encantada que aumenta o alcance de magias de transmutação e deslocamento."),
        ("item-presa-de-hyninn", "Presa de Hyninn", "Alquímicos - Catalisadores", "T$ 45", "Presa de víbora abençoada que potencializa truques e magias de ilusão."),
        ("item-bolor-hemorragico", "Bolor Hemorrágico", "Alquímicos - Venenos", "T$ 60", "Esporos que entram na corrente sanguínea causando sangramento contínuo (1d8 por rodada)."),
        ("item-fumaca-onirica", "Fumaça Onírica", "Alquímicos - Venenos", "T$ 150", "Gás inalatório que induz alucinações vívidas e paralisia onírica."),
        ("item-gas-moroso", "Gás Moroso", "Alquímicos - Venenos", "T$ 60", "Vapor que reduz o deslocamento da vítima pela metade e impõe -2 em testes de ataque e Defesa."),
        ("item-seiva-necrotica", "Seiva Necrótica", "Alquímicos - Venenos", "T$ 120", "Seiva negra de árvores profanas que drena 2d6 pontos de vida e impede cura mágica por 1 hora.")
    ]
    for alid, alname, alsub, alprice, aldesc in alquimicos_hda:
        items.append(make_item(alid, alname, "Itens Gerais", alsub, "Alquímico", alprice, None, None, None, None, None, None, 0.5, book, 229, aldesc, ["alquimia", alsub.lower()]))

    # 15 Aparatos de Engenhoca (HdA pág 229, 236-238)
    aparatos_hda = [
        ("aparato-captador-de-luz", "Captador de Luz", "T$ 450", "Lentes e prismas que absorvem fótons solares para iluminar ou cegar oponentes."),
        ("aparato-comutador", "Comutador", "T$ 300", "Alavanca seletora de fluxos de energia que alterna os modos de operação da engenhoca sem gastar ações."),
        ("aparato-conversor-alimentador", "Conversor-Alimentador", "T$ 300", "Mecanismo que converte combustível comum ou pólvora em cargas adicionais para a engenhoca."),
        ("aparato-engenho-de-automacao", "Engenho de Automação", "T$ 600", "Mecanismo de relojoaria autônomo que permite acionar a engenhoca com comando verbal."),
        ("aparato-espera-para-melhorias", "Espera para Melhorias", "T$ 150", "Encaixe universal de engrenagens que permite acoplar uma melhoria extra à engenhoca."),
        ("aparato-estabilizador", "Estabilizador", "T$ 900", "Giroscópio pesado que impede que a engenhoca engasgue ou exploda em falhas críticas."),
        ("aparato-estimulador-de-sobrecarga", "Estimulador de Sobrecarga", "T$ 750", "Válvula de pressão que permite dobrar o efeito da engenhoca assumindo risco de quebra."),
        ("aparato-gatilho-de-corda", "Gatilho de Corda", "T$ 1.500", "Corda de alta tensão que aciona a engenhoca como uma reação defensiva instantânea."),
        ("aparato-giroscopio", "Giroscópio", "T$ 450", "Esfera articulada de bronze que mantém o balanço perfeito da engenhoca em qualquer terreno."),
        ("aparato-ligacao-de-convergencia", "Ligação de Convergência", "T$ 300", "Fios condutores de prata que conectam duas engenhocas para ativarem simultaneamente."),
        ("aparato-remontagem-de-portabilidade", "Remontagem de Portabilidade", "T$ 300", "Estrutura retrátil que permite dobrar a engenhoca até o tamanho de um frasco."),
        ("aparato-sequenciador-de-ativacao", "Sequenciador de Ativação", "T$ 600", "Tambor com dentes perfurados que executa uma sequência programada de 3 efeitos consecutivos."),
        ("aparato-sistema-de-refrigeracao", "Sistema de Refrigeração", "T$ 900", "Condensador químico que resfria a máquina imediatamente, prevenindo superaquecimento."),
        ("aparato-supressor-de-seguranca", "Supressor de Segurança", "T$ 300", "Trava de segurança oculta que impede que qualquer outra pessoa além do inventor use a máquina."),
        ("aparato-transformador-mistico", "Transformador Místico", "T$ 600", "Núcleo de quartzo arcano que converte energia mágica ambiente em cargas mecânicas.")
    ]
    for apid, apname, apprice, apdesc in aparatos_hda:
        items.append(make_item(apid, apname, "Itens Gerais", "Aparatos", "Aparato de Engenhoca", apprice, None, None, None, None, None, None, 0, book, 229, apdesc + " (Aparatos acoplados não ocupam espaço; desencaixados ocupam 1 espaço).", ["aparato", "inventor", "engenhoca"]))

    # Alimentação - Pratos Especiais & Bebidas HdA
    pratos_hda = [
        ("item-baga-celeste-cozida", "Baga Celeste Cozida", "Alimentação", "T$ 15", 0, "Fruta cozida com especiarias doces que concede 5 PV temporários e bem-estar."),
        ("item-cozido-de-pimenta", "Cozido de Pimenta", "Alimentação", "T$ 10", 0, "Guisado picante que acelera o metabolismo, fornecendo +1 em testes de Iniciativa por uma cena."),
        ("item-manjar-de-sombras", "Manjar de Sombras", "Alimentação", "T$ 20", 0, "Doce exótico com essências da noite que fornece +2 em testes de Furtividade por uma cena."),
        ("item-baba-de-troll", "Baba de Troll", "Alimentação", "T$ 30", 0.5, "Bebida fermentada densa e forte que acelera a recuperação de PV durante o descanso."),
        ("item-barba-queimada", "Barba Queimada", "Alimentação", "T$ 45", 0.5, "Destilado de pólvora e álcool de cereais consumido por artilheiros que fornece +1 em rolagens de dano."),
        ("item-cerveja-deheoni", "Cerveja Deheoni", "Alimentação", "T$ 15", 0.5, "Cerveja dourada de malte e lúpulo puro de Deheon com sabor equilibrado e reconfortante."),
        ("item-dilinio", "Dilínio", "Alimentação", "T$ 600", 0.5, "Destilado lendário de Mortenstenn no sul com receita esquecida. Concede 10 PV temporários e +2 em testes de Vontade."),
        ("item-grogue-negro", "Grogue Negro", "Alimentação", "T$ 15", 0.5, "Mistura forte de rum, especiarias e raspas de limão favorita de piratas do Mar Negro."),
        ("item-grogue-rubro", "Grogue Rubro", "Alimentação", "T$ 45", 0.5, "Bebida avermelhada picante com pimentas do deserto que concede +1 em testes de Fortitude."),
        ("item-hidromel-uivante", "Hidromel Uivante", "Alimentação", "T$ 21", 0.5, "Hidromel fermentado nas Montanhas Uivantes com mel de abelhas glaciais que fornece resistência a frio 5 por uma cena."),
        ("item-licor-feerico", "Licor Feérico", "Alimentação", "T$ 450", 0.5, "Elixir luminoso produzido em Pondsmânia que concede 5 PM temporários e efeitos visuais mágicos."),
        ("item-sidra-ahleniense", "Sidra Ahleniense", "Alimentação", "T$ 45", 0.5, "Sidra de maçãs nobres fermentada com açúcar que afia a astúcia e concede +2 em Enganação."),
        ("item-vinho-pruss", "Vinho Pruss", "Alimentação", "T$ 60", 0.5, "Vinho encorpado envelhecido em barris de carvalho que fornece +1 em testes de Carisma."),
        ("item-vinho-elfico", "Vinho Élfico", "Alimentação", "T$ 90", 0.5, "Bebida ancestral de néctar floral de Lenórienn de aroma inebriante que restaura +2 PM no descanso.")
    ]
    for prid, prname, prsub, prprice, prspace, prdesc in pratos_hda:
        items.append(make_item(prid, prname, "Itens Gerais", prsub, "Comida e Bebida", prprice, None, None, None, None, None, None, prspace, book, 229, prdesc, ["alimentação", "comida", "bebida"]))

    # Animais & Veículos HdA
    animais_hda = [
        ("item-armadura-de-montaria-leve", "Armadura de Montaria Leve", "T$ 600", 2, "Bardas de couro acolchoado e metal leve que concedem Defesa +2 à montaria sem penalidade de velocidade."),
        ("item-armadura-de-montaria-pesada", "Armadura de Montaria Pesada", "T$ 3.000", 5, "Barda completa de placas de aço para cavalos de guerra que fornece Defesa +5 e RD 2 à montaria."),
        ("item-arreios-namalkahnianos", "Arreios Namalkahnianos", "T$ 50", 1, "Arreios especiais de Namalkah que concedem +2 em testes de Cavalgar e Atletismo para montarias."),
        ("item-caparazao", "Caparazão", "T$ 75", 1, "Manto de tecido nobre bordado com o brasão do cavaleiro que cobre o animal, concedendo +1 em Nobreza."),
        ("item-estribos", "Estribos", "T$ 60", 1, "Estribos de ferro fundido que conferem estabilidade sobre a sela (+2 contra ser derrubado da montaria)."),
        ("item-ornamento", "Ornamento", "T$ 50", 1, "Penachos e broches para arreios que valorizam a montaria em feiras e apresentações aristocráticas."),
        ("item-barcaca", "Barcaça", "T$ 3.000", 0, "Embarcação fluvial ampla com fundo chato projetada para transporte pesado de cargas e tropas em rios calmos."),
        ("item-biga-de-guerra", "Biga de Guerra", "T$ 250", 0, "Carroça ágil de combate de duas rodas com lâminas nos eixos puxada por dois ou quatro cavalos."),
        ("item-dirigivel-goblin", "Dirigível Goblin", "T$ 1.200", 0, "Nave aérea com balão de gás inflamável e motor a vapor barulhento com capacidade para 6 passageiros."),
        ("item-jangada", "Jangada", "T$ 60", 0, "Plataforma flutuante rústica de troncos amarrados e vela triangular para navegação costeira."),
        ("item-veleiro-hda", "Veleiro", "T$ 10.000", 0, "Navio mercante ou de guerra com convés duplo, mastros e velame completo para travessias marítimas.")
    ]
    for anid, anname, anprice, anspace, andesc in animais_hda:
        sub = "Veículos" if "T$ 3.000" in anprice or "T$ 250" in anprice or "T$ 1.200" in anprice or "T$ 60" in anprice or "T$ 10.000" in anprice else "Animais"
        items.append(make_item(anid, anname, "Itens Gerais", sub, sub, anprice, None, None, None, None, None, None, anspace, book, 229, andesc, ["animais", "veículos", "montaria"]))

    # Serviços HdA
    servicos_hda = [
        ("servico-banho-quente", "Banho Quente", "T$ 10", "Disponível em casas de banho e estalagens nobres. Relaxa o corpo e fortalece a imunidade (+1 em testes de Fortitude por um dia)."),
        ("servico-bigode-encerado", "Bigode Encerado", "T$ 20", "Um barbeiro profissional apara e molda barba e bigode com cera fina (+1 em Diplomacia e Enganação por um dia)."),
        ("servico-instrucao-marcial", "Instrução Marcial", "T$ 300", "Treinamento intensivo com um mestre de armas que afia reflexos de combate (+1 em rolagens de dano por uma semana)."),
        ("servico-maquiagem-profissional", "Maquiagem Profissional", "T$ 30", "Aplicação estética de pós e tintas cosméticas de alta qualidade (+1 em perícias baseadas em Carisma)."),
        ("servico-mercenario-iniciante", "Mercenário (Parceiro Iniciante)", "T$ 30 por cena", "Contratação de guerreiro, batedor ou guarda-costas novato como parceiro iniciante por uma cena."),
        ("servico-mercenario-veterano", "Mercenário (Parceiro Veterano)", "T$ 150 por cena", "Contratação de combatente experiente como parceiro veterano por uma cena de combate ou missão."),
        ("servico-mercenario-capangas-iniciantes", "Mercenário (Capangas Iniciantes)", "T$ 90 por cena", "Contratação de um esquadrão de 4 a 6 capangas iniciantes para combate por uma cena."),
        ("servico-mercenario-capangas-veteranos", "Mercenário (Capangas Veteranos)", "T$ 300 por cena", "Contratação de uma unidade de capangas veteranos treinados para ação militar pesada."),
        ("servico-opera", "Ópera", "T$ 200", "Ingresso para espetáculo musical dramático na corte que inspira a mente e concede +1 PM temporário."),
        ("servico-sarau-informativo", "Sarau Informativo", "T$ 150", "Reunião de viajantes e eruditos compartilhando notícias e segredos regionais (+2 em Investigação e Conhecimento).")
    ]
    for sid, sname, sprice, sdesc in servicos_hda:
        items.append(make_item(sid, sname, "Itens Gerais", "Serviços", "Serviço", sprice, None, None, None, None, None, None, 0, book, 229, sdesc, ["serviço", "contratação", "social"]))

    # Capangas HdA (pág 241-242)
    capangas_hda = [
        ("capangas-bando-duyshidakk", "Bando Duyshidakk", "T$ —", "Grupo de combatentes duyshidakk. Iniciante: 5 combatentes (deslocamento 9m, Defesa 15, dano 1d6+1 cada). Veterano: 6 combatentes. Mestre: 7 combatentes (dano 2d4+2)."),
        ("capangas-esqueletos-animados", "Esqueletos Animados", "T$ —", "Mortos-vivos simplificados. Iniciante: 4 esqueletos (deslocamento 9m, Defesa 18, dano 1d6+1 cada). Veterano: 5 esqueletos com RD 5 (corte, frio e perfuração). Mestre: 6 esqueletos (dano 1d8+2)."),
        ("capangas-pelotao-de-infantaria", "Pelotão de Infantaria", "T$ —", "Soldados regulares com equipamento básico. Iniciante: 4 infantes (deslocamento 9m, Defesa 16, dano 2d4+1 cada). Veterano: 5 infantes. Mestre: 6 infantes (Defesa 18)."),
        ("capangas-tripulacao", "Tripulação", "T$ —", "Tripulantes treinados para navegar e combater. Iniciante: 4 marinheiros (deslocamento 9m, Defesa 14, dano 1d6 cada, +1 em Pilotagem). Veterano: 5 marinheiros (+2 em Pilotagem). Mestre: 6 marinheiros (dano 1d8, +5 em Pilotagem)."),
        ("capangas-turba-de-camponeses", "Turba de Camponeses", "T$ —", "Multidão enfurecida armada de foices e forcados. Iniciante: 6 camponeses (deslocamento 9m, Defesa 10, dano 1d6 cada). Veterano: 8 camponeses. Mestre: 10 camponeses (dano 1d6+1)."),
        ("capangas-unidade-de-arqueiros", "Unidade de Arqueiros", "T$ —", "Arqueiros em formação militar que atacam à distância. Iniciante: 4 arqueiros (deslocamento 9m, Defesa 14, dano 1d6 cada em alcance curto). Veterano: 5 arqueiros. Mestre: 6 arqueiros (dano 1d8).")
    ]
    for cid, cname, cprice, cdesc in capangas_hda:
        items.append(make_item(cid, cname, "Itens Gerais", "Capangas", "Capangas", cprice, None, None, None, None, None, None, 0, book, 241, cdesc, ["capangas", "parceiro", "tropas", "combate"]))

    # =========================================================================
    # 4. NOVAS MELHORIAS (Tabela 3-5, Páginas 240-241)
    # =========================================================================
    melhorias_hda = [
        ("melhoria-farpada", "Farpada", "Melhoria de Arma", "+T$ 300", "A lâmina ou ponta possui ganchos perfurantes. Em acertos críticos, deixa a vítima sangrando."),
        ("melhoria-fosforo", "Fósforo", "Melhoria de Arma", "+T$ 300", "Munições revestidas com fósforo alquímico que ofuscam o alvo ao acertar."),
        ("melhoria-guarda", "Guarda", "Melhoria de Arma", "+T$ 300", "Guarda de mão reforçada que concede +1 na Defesa e em testes contra manobras do oponente."),
        ("melhoria-incendiaria", "Incendiária", "Melhoria de Arma", "+T$ 300", "Munição especial que causa dano adicional por fogo e pode colocar o alvo em chamas."),
        ("melhoria-pressurizada", "Pressurizada", "Melhoria de Arma", "+T$ 3.000", "Câmara interna com pistão de ar. Pode ser engatilhada para fornecer +2 no teste de ataque e no dano no próximo golpe."),
        ("melhoria-balistico", "Balístico", "Melhoria de Armadura/Escudo", "+T$ 300", "Mecanismo que projeta fragmentos cortantes durante ataques com escudo, aumentando o dano."),
        ("melhoria-injetora", "Injetora", "Melhoria de Armadura/Escudo", "+T$ 300", "Mecanismo interno na armadura que permite ingerir uma poção ou preparado como ação de movimento."),
        ("melhoria-prudente", "Prudente", "Melhoria de Armadura/Escudo", "+T$ 300", "Ajustes estruturais que minimizam erros do usuário, atenuando os efeitos de falhas críticas."),
        ("melhoria-potencializador", "Potencializador", "Melhoria de Esotérico", "+T$ 3.000", "Gemas místicas amplificadas que aumentam o limite de PM gastável em magias em +2. Pré-requisito: Canalizador."),
        ("melhoria-brasonado", "Brasonado", "Melhoria de Ferramenta/Vestuário", "+T$ 300", "Item adornado com brasões e insígnias que permite usar a perícia correspondente para influenciar atitudes."),
        ("melhoria-usado", "Usado", "Melhoria de Ferramenta/Vestuário", "+T$ 0", "Item amaciado pelo uso prolongado que permite rerrolar um resultado 1 natural em perícia uma vez por dia."),
        ("melhoria-deslumbrante", "Deslumbrante", "Melhoria Geral", "+T$ 3.000", "Acabamento de luxo estonteante que aumenta a CD de suas habilidades baseadas em Carisma em +1.")
    ]
    for mid, mname, msub, mprice, mdesc in melhorias_hda:
        items.append(make_item(mid, mname, "Itens Superiores", "Melhorias", msub, mprice, None, None, None, None, None, None, None, book, 240, mdesc, ["melhoria", "superior", "heróis de arton"]))

    return items
