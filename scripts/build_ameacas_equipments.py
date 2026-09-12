# -*- coding: utf-8 -*-
"""
Gerador Canônico de Equipamentos: Ameaças de Arton (v1.0)
100% completo, exaustivo e fiel às tabelas e páginas do livro oficial.
"""

from equipment_common import make_item

def get_ameacas_equipments():
    book = "Ameaças de Arton (v1.0)"
    items = []

    # =========================================================================
    # 1. NOVAS ARMAS (Tabela 3-1, Página 394; Descrições Páginas 394-395)
    # =========================================================================

    # Armas Simples
    items.append(make_item("arma-porrete", "Porrete", "Armas", "Armas Simples", "Corpo a Corpo / Leve", "T$ 2", "1d6", "x2", "Impacto", "-", None, None, 1, book, 394, 
        "Um bastão de madeira pesada com rebites de metal ou couro trançado no punho. Muito usado por milícias populares, bandidos de rua e capangas.", 
        ["porrete", "simples", "impacto", "milícia"]))

    items.append(make_item("arma-zarabatana", "Zarabatana", "Armas", "Armas Simples", "Ataque à Distância / Uma Mão", "T$ 5", "1d3", "x2", "Perfuração", "Curto", None, None, 1, book, 394, 
        "Pequeno tubo oco usado para disparar dardos com um sopro. Causa dano mínimo, mas é excelente para inocular venenos: a CD para resistir ao veneno dos dardos aumenta em +2.", 
        ["zarabatana", "veneno", "dardo", "sopro"]))

    # Armas Marciais
    items.append(make_item("arma-neko-te", "Neko-te", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 10", "1d4", "19", "Corte", "-", None, None, 1, book, 394, 
        "Garras de aço afiadas presas às pontas dos dedos por tiras de couro. É uma arma ágil que fornece +2 em testes de Ladinagem e Atletismo para escalar.", 
        ["garras", "ninja", "ágil", "escalada", "ladinagem"]))

    items.append(make_item("arma-gladio", "Gládio", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 12", "1d6", "19/x3", "Perfuração", "-", None, None, 1, book, 394, 
        "A espada curta padrão das legiões romanas de Tapista. Possui ponta triangular reforçada feita para estocadas mortais em combate cerrado.", 
        ["tapista", "legião", "estocada", "crítico 19/x3"]))

    items.append(make_item("arma-tetsubo", "Tetsubo", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 20", "1d10", "x2", "Impacto", "-", None, None, 2, book, 394, 
        "Uma versão mais pesada e sofisticada do tacape oriental de Tamu-ra, feita de madeira de lei reforçada com anéis de ferro. É uma arma versátil (+2 para derrubar ou empurrar).", 
        ["tamura", "tacape de ferro", "versátil", "derrubar"]))

    # Armas de Fogo Ameaças
    items.append(make_item("arma-traque", "Traque", "Armas", "Armas de Fogo", "Ataque à Distância / Leve", "T$ 75", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1, book, 394, 
        "Arma de fogo rústica feita com sucata e cano de metal de segunda mão. Se errar um ataque com resultado ímpar no d20, ela fica avariada. Recarregar é uma ação padrão.", 
        ["arma de fogo", "sucata", "barata", "pólvora"]))

    items.append(make_item("arma-arcabuz", "Arcabuz", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos", "T$ 800", "2d10", "19/x3", "Perfuração", "Médio", None, None, 2, book, 394, 
        "Uma arma de fogo longa e pesada com mecanismo de mecha e cano de grosso calibre de impacto devastador.", 
        ["arma de fogo", "arcabuz", "dano pesado", "pólvora"]))

    items.append(make_item("arma-bacamarte", "Bacamarte", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos", "T$ 450", "4d6", "19/x3", "Perfuração", "Especial", None, None, 2, book, 394, 
        "Arma de fogo curta com boca afunilada em sino que dispara uma saraivada de chumbo em cone de 6 metros.", 
        ["arma de fogo", "cone", "área", "chumbo"]))

    # Armas Exóticas
    items.append(make_item("arma-acoite-finntroll", "Açoite Finntroll", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 30", "1d8", "x2", "Corte", "-", None, None, 1, book, 394, 
        "Um chicote biológico feito de tentáculos e lianas carnívoras venenosas cultivadas pelos finntrolls nas profundezas subterrâneas de Trollkyrkja.", 
        ["finntroll", "subterrâneo", "tentáculo", "lianas"]))

    items.append(make_item("arma-espada-vespa", "Espada Vespa", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 75", "2d4", "18", "Corte ou Perfuração", "-", None, None, 1, book, 394, 
        "Feita com ferrões rígidos de vespas gigantes de Galrasia montados em uma haste de osso. É uma arma ágil e pode causar dano de corte ou perfuração.", 
        ["galrasia", "inseto", "ágil", "crítico 18"]))

    items.append(make_item("arma-pistola-punhal", "Pistola-Punhal", "Armas", "Armas Exóticas", "Corpo a Corpo / Ataque à Distância", "T$ 300", "1d4 / 2d6", "19 / 19/x3", "Perfuração", "Curto", None, None, 1, book, 394, 
        "Uma lâmina de punhal fixada sob o cano de uma pistola. Permite desferir um ataque corpo a corpo (1d4 perfuração) ou disparar um tiro de pólvora (2d6 perfuração) com a mesma empunhadura.", 
        ["híbrida", "pistola", "punhal", "fogo e combate"]))

    items.append(make_item("arma-mordida-do-diabo", "Mordida do Diabo", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 30", "1d4", "x2", "Perfuração", "-", None, None, 1, book, 394, 
        "Duas mandíbulas afiadas de ferro com mola potente que prendem a carne da vítima. Ao acertar um ataque, permite iniciar a manobra agarrar como ação livre.", 
        ["mandíbula", "mola", "agarrar", "armadilha"]))

    items.append(make_item("arma-presa-de-serpente", "Presa de Serpente", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 1.000", "1d8", "17", "Corte", "-", None, None, 1, book, 394, 
        "Uma lâmina forjada com presas de serpentes marinhas lendárias de Khubar. É uma arma ágil com margem de ameaça 17 excepcional.", 
        ["khubar", "serpente", "ágil", "crítico 17"]))

    items.append(make_item("arma-lanca-de-fogo", "Lança de Fogo", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos", "T$ 1.000", "1d8 / 4d6", "x3 / x2", "Perfuração / Fogo", "Curto", None, None, 2, book, 394, 
        "Uma lança pesada com um morteiro de pólvora e óleo alquímico na ponta que dispara uma labareda explosiva durante o golpe de investida.", 
        ["lança", "fogo", "pólvora", "explosão"]))

    items.append(make_item("arma-shuriken", "Shuriken", "Armas", "Armas Exóticas", "Ataque à Distância / Leve", "T$ 1", "1d4", "x2", "Perfuração", "Curto", None, None, 0.5, book, 394, 
        "Estrelas metálicas pontiagudas de arremesso. Uma vez por rodada, ao atacar com shuriken, pode gastar 1 PM para fazer um ataque adicional de shuriken contra o mesmo alvo.", 
        ["ninja", "arremesso", "tamura", "ataque extra"]))

    items.append(make_item("arma-arpao", "Arpão", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão", "T$ 30", "1d10", "x3", "Perfuração", "Curto", None, None, 1, book, 394, 
        "Uma grande haste dentada de caça marítima ligada a um cabo de corda. Ao acertar um ataque à distância, prende a criatura permitindo puxá-la com testes de Atletismo.", 
        ["arpão", "marítimo", "prender", "caça"]))

    # =========================================================================
    # 2. NOVAS ARMADURAS & ESCUDOS (Tabela 3-2, Página 395; Páginas 395-396)
    # =========================================================================
    items.append(make_item("armadura-armadura-de-ossos", "Armadura de Ossos", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 120", None, None, None, None, "+3", "-2", 2, book, 395, 
        "Confeccionada com crânios e costelas de monstros unidas por tiras de tendão. Fornece +1 em testes de Intimidação e na CD de seus efeitos de medo.", 
        ["ossos", "medo", "intimidação", "monstro"]))

    items.append(make_item("armadura-veste-de-teia-de-aranha", "Veste de Teia de Aranha", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 3.000", None, None, None, None, "+4", "0", 2, book, 395, 
        "Tecida com seda de aranhas gigantes das cavernas profundas. Extremamente leve e maleável como seda, fornece +5 em testes de Furtividade sem nenhuma penalidade de armadura.", 
        ["teia", "aracnídeo", "furtividade +5", "sem penalidade"]))

    items.append(make_item("armadura-armadura-de-quitina", "Armadura de Quitina", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 350", None, None, None, None, "+7", "-3", 5, book, 395, 
        "Feita com placas de carapaça quitinosa de insetos gigantes dos ermos. Embora seja uma armadura pesada, é muito leve e não reduz o deslocamento do usuário.", 
        ["quitina", "inseto gigante", "pesada", "não reduz deslocamento"]))

    items.append(make_item("armadura-escudo-de-couro", "Escudo de Couro", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 3", None, None, None, None, "+1", "-1", 1, book, 395, 
        "Armação leve de madeira esticando uma membrana flexível de couro de monstro amarrada ao braço. Contra ataques à distância, seu bônus de Defesa aumenta em +2.", 
        ["couro", "leve", "defesa contra projéteis"]))

    # =========================================================================
    # 3. NOVOS ITENS GERAIS (Tabela 3-3, Página 398; Páginas 398-400)
    # =========================================================================

    # Alimentação Monstruosa
    pratos_ameacas = [
        ("item-algravia", "Algravia", "T$ 3", 0, "Doce gelatinoso feito de néctar de flores carnívoras gigantes que acalma a fome por 24 horas."),
        ("item-banquete-de-canceronte", "Banquete de Canceronte", "T$ 36", 0, "Carne nobre de crustáceo colossal cozida com manteiga e ervas que concede RD 2 por uma cena."),
        ("item-coc-au-triz", "Coc-au-triz", "T$ 54", 0, "Prato fino de carne de cocatriz que concede imunidade a efeitos de petrificação e veneno por uma cena."),
        ("item-cozido-de-serpe", "Cozido de Serpe", "T$ 12", 0, "Guisado denso de réptil dracônico que fornece resistência a ácido 5 por uma cena."),
        ("item-gorlogg-ensopado", "Gorlogg Ensopado", "T$ 6", 0, "Ensopado altamente nutritivo de carne de gorlogg. Aumenta a recuperação de PV e PM no próximo descanso em +1 por nível."),
        ("item-omelete-monstruosa", "Omelete Monstruosa", "T$ 3", 0, "Feita com ovos de pragas e feras monstruosas. Concede +2 nas rolagens de dano durante uma cena."),
        ("item-sashimi-de-kraken", "Sashimi de Kraken", "T$ 60", 0, "Fatias nobres de tentáculo de monstro marinho que fornecem 5 PM temporários e +2 em testes de Diplomacia.")
    ]
    for pid, pname, pprice, pspace, pdesc in pratos_ameacas:
        items.append(make_item(pid, pname, "Itens Gerais", "Alimentação", "Comida Monstruosa", pprice, None, None, None, None, None, None, pspace, book, 398, pdesc, ["alimentação", "monstro", "iguaria"]))

    # Animais & Montarias Ameaças
    animais_ameacas = [
        ("item-bulette", "Bulette", "T$ 500", 0, "Fera encouraçada temperamental que escava sob a terra. Pode ser usada como parceiro montaria por guerreiros experientes."),
        ("item-capivara", "Capivara", "T$ 60", 0, "Roedor gigante dócil e afável apreciado como montaria por personagens Pequenos e Minúsculos."),
        ("item-corcel-do-deserto", "Corcel do Deserto", "T$ 150", 0, "Cavalo insetoide das areias do Deserto da Perdição adaptado ao calor extremo (parceiro montaria)."),
        ("item-dromedario", "Dromedário", "T$ 75", 0, "Montaria resistente de uma corcova capaz de viajar dias sem água no deserto e regiões áridas."),
        ("item-elefante", "Elefante", "T$ 1.500", 0, "Paquiderme colossal de grande força de tração e combate capaz de transportar cargas maciças e plataformas."),
        ("item-hiena", "Hiena", "T$ 220", 0, "Predador astuto das savanas que pode ser adestrado como parceiro especial ou montaria para hynne e goblins."),
        ("item-leao", "Leão", "T$ 800", 0, "Grande felino nobre e feroz treinado para aceitar cavaleiros de guerra e desferir botes letais."),
        ("item-rinoceronte", "Rinoceronte", "T$ 600", 0, "Besta colossal com chifre blindado que executa investidas demolidoras contra fortificações."),
        ("item-urso-pardo", "Urso Pardo", "T$ 300", 0, "Predador robusto das florestas frias capaz de lutar bravamente ao lado de seu cavaleiro.")
    ]
    for anid, anname, anprice, anspace, andesc in animais_ameacas:
        items.append(make_item(anid, anname, "Itens Gerais", "Animais", "Montaria Monstruosa", anprice, None, None, None, None, None, None, anspace, book, 398, andesc, ["animais", "montaria", "monstro"]))

    # Equipamento de Aventura & Esotéricos Ameaças
    itens_aventura_ameacas = [
        ("item-caixa-de-voz", "Caixa de Voz", "Equipamento de Aventura", "T$ 50", 1, "Mecanismo complexo com 1d4 cargas que amplifica comandos de voz e gritos de guerra a distâncias imensas."),
        ("item-corda-de-teia", "Corda de Teia", "Equipamento de Aventura", "T$ 100", 1, "Corda tecida com fios pegajosos de aranha gigante com 15m, imune a corte comum e capaz de grudar em superfícies."),
        ("item-dente-de-wisphago", "Dente de Wisphago", "Equipamento de Aventura", "T$ 100", 1, "Amuleto mineralizado de monstro devorador de mana que vibra na presença de ilusões e magia ativa."),
        ("item-ankh-solar", "Ankh Solar", "Esotéricos", "T$ 450", 1, "Símbolo sagrado entalhado em ouro e quartzo solar de Azgher que aumenta o dano de magias de luz e fogo em +1 por dado."),
        ("item-tomo-de-guerra", "Tomo de Guerra", "Esotéricos", "T$ 300", 1, "Grimório encadernado em couro de dragão com anotações de batalha que concede +1 no ataque e dano de armas conjuradas."),
        ("item-tomo-do-rancor", "Tomo do Rancor", "Esotéricos", "T$ 750", 1, "Livro amaldiçoado que armazena a dor do conjurador: ao sofrer dano, sua próxima magia causa dano extra igual à metade do dano sofrido.")
    ]
    for itid, itname, itsub, itprice, itspace, itdesc in itens_aventura_ameacas:
        items.append(make_item(itid, itname, "Itens Gerais", itsub, itsub, itprice, None, None, None, None, None, None, itspace, book, 398, itdesc, ["aventura", "esotérico", "monstro"]))

    # Alquímicos Ameaças (Preparados, Catalisadores, Venenos)
    alquimicos_ameacas = [
        ("item-balsamo-de-drogadora", "Bálsamo de Drogadora", "Alquímicos - Preparados", "T$ 60", "Pasta medicinal de ervas dos povos-trovão que cura 4d4 PV e remove uma condição de fadiga."),
        ("item-bomba-de-fumaca", "Bomba de Fumaça", "Alquímicos - Preparados", "T$ 15", "Gera uma nuvem densa de fumaça escura de 6m de raio que concede camuflagem total por 1d4 rodadas."),
        ("item-elixir-quimerico", "Elixir Quimérico", "Alquímicos - Preparados", "T$ 120", "Poção mutagênica instável que concede visão no escuro e +2 em testes de Percepção por uma cena."),
        ("item-eter-elemental", "Éter Elemental", "Alquímicos - Preparados", "T$ 60", "Fluido volátil que pode ser derramado sobre uma arma para conferir +1d6 de dano elemental por uma cena."),
        ("item-isca-putrefata", "Isca Putrefata", "Alquímicos - Preparados", "T$ 60", "Substância odorífera irresistível que atrai monstros e predadores carnívoros em um raio de 1 km."),
        ("item-lagrima-petrea", "Lágrima Pétrea", "Alquímicos - Preparados", "T$ 30", "Óleo mineral que endurece a pele fornecendo Defesa +2 e resistência a corte e perfuração 2 por uma cena."),
        ("item-oleo-de-baleia", "Óleo de Baleia", "Alquímicos - Preparados", "T$ 30", "Óleo de combustão pura e prolongada que arde debaixo d'água e queima por 12 horas."),
        ("item-oleo-de-besouro", "Óleo de Besouro", "Alquímicos - Preparados", "T$ 50", "Extrato quitinoso espesso que protege armas contra oxidação, ferrugem e ácido por uma semana."),
        ("item-po-azul", "Pó Azul", "Alquímicos - Preparados", "T$ 150", "Pó mineral reluzente que neutraliza efeitos de venenos e toxinas ativas no organismo imediatamente."),
        ("item-corrosivo-mineral", "Corrosivo Mineral", "Alquímicos - Catalisadores", "T$ 150", "Ácido bruto que dissolve minérios e concede +2 no dano de magias de ácido contra construtos."),
        ("item-gelo-extremo", "Gelo Extremo", "Alquímicos - Catalisadores", "T$ 150", "Fragmentos de geada perene que congelam a umidade do ar e aumentam o dano de magias de frio."),
        ("item-pedaco-de-lingua", "Pedaço de Língua", "Alquímicos - Catalisadores", "T$ 30", "Língua preservada de réptil falante que concede +1 na CD de magias de Encantamento."),
        ("item-raio-cristalizado", "Raio Cristalizado", "Alquímicos - Catalisadores", "T$ 150", "Fulgorita criada por relâmpagos mágicos que potencializa arcos elétricos e magias de eletricidade."),
        ("item-esporos-de-cogumelo", "Esporos de Cogumelo", "Alquímicos - Venenos", "T$ 75", "Fungos alucinógenos inalatórios que deixam as vítimas fascinadas e tontas."),
        ("item-peconha-ancia", "Peçonha Anciã", "Alquímicos - Venenos", "T$ 1.800", "Veneno antiquíssimo de dragões e serpes ancestrais (Fortitude CD 28, dano 8d10 de veneno letal)."),
        ("item-peconha-irritante", "Peçonha Irritante", "Alquímicos - Venenos", "T$ 10", "Toxina branda de insetos que causa coceira intensa, impondo -2 em testes de ataque e perícias."),
        ("item-veneno-batraquio", "Veneno Batráquio", "Alquímicos - Venenos", "T$ 30", "Seiva extraída da pele de sapos venenosos que causa dormência e paralisia temporária.")
    ]
    for alid, alname, alsub, alprice, aldesc in alquimicos_ameacas:
        items.append(make_item(alid, alname, "Itens Gerais", alsub, "Alquímico", alprice, None, None, None, None, None, None, 0.5, book, 398, aldesc, ["alquimia", "monstro", alsub.lower()]))

    # Vestuário Ameaças
    vestuario_ameacas = [
        ("item-garra-feroz", "Garra Feroz", "T$ 60", 1, "Garras montadas sobre braceletes de couro que conferem +1 nas rolagens de dano de ataques desarmados."),
        ("item-manto-do-mantor", "Manto do Mantor", "T$ 450", 1, "Manto confeccionado com a pele de uma besta mantor que fornece camuflagem e +2 em Furtividade na escuridão."),
        ("item-manto-pesado", "Manto Pesado", "T$ 10", 1, "Capa grossa de lã e pelo de monstro que protege contra intempéries e frio nos ermos."),
        ("item-sombreiro", "Sombreiro", "T$ 10", 1, "Chapéu de palha de abas gigantescas típico do Deserto da Perdição que protege os olhos do sol escaldante."),
        ("item-traje-selako", "Traje Selako", "T$ 90", 1, "Vestimenta aquática de escamas de tubarão selako que reduz a penalidade de movimento debaixo d'água.")
    ]
    for vid, vname, vprice, vspace, vdesc in vestuario_ameacas:
        items.append(make_item(vid, vname, "Itens Gerais", "Vestuário", "Vestuário Monstruoso", vprice, None, None, None, None, None, None, vspace, book, 398, vdesc, ["vestuário", "monstro", "estilo"]))

    # =========================================================================
    # 4. NOVOS MATERIAIS & MELHORIAS (Tabela 3-4, Páginas 400-401)
    # =========================================================================
    
    # Novas Melhorias Ameaças
    items.append(make_item("melhoria-multifuncional", "Multifuncional", "Itens Superiores", "Melhorias", "Melhoria de Ferramenta/Vestuário", "+T$ 300", None, None, None, None, None, None, None, book, 400, 
        "Aplicada em item que modifica uma perícia: escolha outra perícia que use o mesmo atributo-chave; o item passa a funcionar também para a segunda perícia.", 
        ["melhoria", "multifuncional", "perícia"]))

    items.append(make_item("melhoria-penetrante", "Penetrante", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 3.000", None, None, None, None, None, None, None, book, 400, 
        "A arma possui lâmina ou ponta tratada para perfurar armaduras blindadas. Ignora 5 pontos da redução de dano (RD) do alvo. Pré-requisito: Cruel.", 
        ["melhoria", "arma", "rd", "penetrante"]))

    # Novos Materiais Especiais Ameaças
    materiais_ameacas = [
        ("material-casco-de-monstro", "Casco de Monstro", "Ver Tabela 3-4", "Cascos protetores rígidos de monstros. Arma: conta como arma primitiva. Armadura/Escudo: diminui penalidade de armadura em -1; armaduras pesadas permitem aplicar 1 ponto de Destreza na Defesa. Esotérico: ao lançar magia, recebe RD 5 contra o próximo dano sofrido."),
        ("material-couraca-de-kaiju", "Couraça de Kaiju", "Raro (Não Vendido)", "Escamas colossais de feras gigantes. Arma: dano aumenta em um passo e pode gastar 2 PM para ignorar efeitos redutores como Durão. Armadura/Escudo: concede RD 10/mágico (leves/escudos) ou RD 20/mágico (pesadas). Esotérico: gasta 2 PM para ignorar defesas e evasão de magias de dano."),
        ("material-couro-de-bulette", "Couro de Bulette", "Raro (Não Vendido)", "Couro curtido de bulette escavador. Armadura Leve: fornece deslocamento de escavação (metade do normal) e redução de ácido 5. Armadura Pesada: deslocamento de escavação e redução de ácido 10. Esotérico: rerrola resultados 1 em magias de dano de ácido."),
        ("material-cristal-de-sol", "Cristal de Sol", "Raro (Não Vendido)", "Cristais térmicos armazenadores de calor. Arma: causa +2 de dano por fogo. Armadura/Escudo: rola dois dados e escolhe o melhor em testes de resistência contra frio. Esotérico: ao lançar magia de fogo, pode gastar 1 PM para deixar o alvo em chamas (+1d6)."),
        ("material-lanajuste", "Lanajuste", "Ver Tabela 3-4", "Coral-de-ferro afiadíssimo de Khubar. Arma: ignora penalidades de combate submerso e pode ser usada por devotos de Oceano. Armadura/Escudo: redução de corte (leves/escudos 5; pesadas 10). Esotérico: rerrola resultados 1 em magias de corte."),
        ("material-pena-de-kraken", "Pena de Kraken", "Raro (Não Vendido)", "Material vítreo da concha interna de um kraken. Arma: em acertos críticos, o dano aumenta em dois passos antes de multiplicar. Armadura/Escudo: quando erram ataque contra você, o atacante sofre 5 de dano (leves/escudos) ou 10 de dano (pesadas). Esotérico: bônus numéricos do item aumentam em +1."),
        ("material-prata", "Prata", "Ver Tabela 3-4", "Revestimento nobre de prata que pode ser combinado com um segundo material especial. Arma: causa +2 de dano em espíritos e mortos-vivos e conta como mágica. Armadura/Escudo: redução de dano contra espíritos e mortos-vivos (leves/escudos RD 5; pesadas RD 10)."),
        ("material-espada-de-coral", "Espada de Coral", "+T$ 1.800", "Cimitarra especial feita de lanajuste segundo técnicas da Irmandade dos Pescadores. Além dos benefícios de lanajuste, em acerto crítico deixa a vítima sangrando.")
    ]
    for mid, mname, mprice, mdesc in materiais_ameacas:
        items.append(make_item(mid, mname, "Itens Superiores", "Materiais Especiais", "Material Especial", mprice, None, None, None, None, None, None, None, book, 400, mdesc, ["material especial", "ameaças de arton", "monstro"]))

    return items
