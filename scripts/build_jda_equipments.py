# -*- coding: utf-8 -*-
"""
Gerador Canônico de Equipamentos: Tormenta20 - Jogo do Ano (v1.3)
100% completo, exaustivo e fiel às tabelas e páginas do livro oficial.
"""

from equipment_common import make_item

def get_jda_equipments():
    book = "Tormenta20 - Jogo do Ano (v1.3)"
    items = []

    # =========================================================================
    # 1. ARMAS (Tabela 3-3, Páginas 144-145; Descrições Páginas 146-151)
    # =========================================================================
    
    # Armas Simples - Corpo a Corpo - Leves
    items.append(make_item("arma-adaga", "Adaga", "Armas", "Armas Simples", "Corpo a Corpo / Leve", "T$ 2", "1d4", "19", "Perfuração", "Curto", None, None, 1, book, 146, 
        "Esta faca afiada é usada por muitos habitantes adultos do Reinado, embora seja favorita de ladrões e assassinos, por ser facilmente escondida (fornece +5 em testes de Ladinagem para ocultá-la). Quando ataca com uma adaga, você pode usar sua Destreza em vez de Força nos testes de ataque. Uma adaga pode ser arremessada.", 
        ["faca", "acuidade", "arremesso", "ladinagem", "ocultável"]))
        
    items.append(make_item("arma-ataque-desarmado", "Ataque Desarmado", "Armas", "Armas Simples", "Corpo a Corpo / Leve", "T$ 0", "1d3", "x2", "Impacto", "-", None, None, 0, book, 144, 
        "Um soco, chute, cabeçada ou qualquer outro golpe desferido com o próprio corpo. Um ataque desarmado causa dano não letal. Um personagem treinado em Luta pode causar dano letal ou não letal sem penalidades. Você não pode aplicar melhorias ou encantos a ataques desarmados, a menos que esteja usando uma manopla.", 
        ["soco", "chute", "não letal", "desarmado"]))

    items.append(make_item("arma-espada-curta", "Espada Curta", "Armas", "Armas Simples", "Corpo a Corpo / Leve", "T$ 10", "1d6", "19", "Perfuração", "-", None, None, 1, book, 147, 
        "O tipo mais comum de espada, usada por guardas ou como arma secundária de guerreiros.", 
        ["espada", "leve", "guarda"]))

    items.append(make_item("arma-foice", "Foice", "Armas", "Armas Simples", "Corpo a Corpo / Leve", "T$ 4", "1d6", "x3", "Corte", "-", None, None, 1, book, 147, 
        "Uma ferramenta agrícola com lâmina curva montada em um cabo de madeira curto. Causa dano crítico triplo.", 
        ["agrícola", "crítico x3", "camponês"]))

    # Armas Simples - Corpo a Corpo - Uma Mão
    items.append(make_item("arma-clava", "Clava", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão", "T$ 0", "1d6", "x2", "Impacto", "-", None, None, 1, book, 147, 
        "Um pedaço de madeira empunhado como arma, geralmente usado por bárbaros ou criaturas brutais — ou como arma improvisada, como um galho de árvore ou pedaço de mobília. Sendo fácil de conseguir, seu preço é zero.", 
        ["madeira", "porrete", "grátis", "improvisada"]))

    items.append(make_item("arma-lanca", "Lança", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão", "T$ 2", "1d6", "x2", "Perfuração", "Curto", None, None, 1, book, 148, 
        "Uma haste de madeira com uma ponta afiada de ferro ou pedra. Pode ser arremessada.", 
        ["haste", "arremesso", "infantaria"]))

    items.append(make_item("arma-maca", "Maça", "Armas", "Armas Simples", "Corpo a Corpo / Uma Mão", "T$ 12", "1d8", "x2", "Impacto", "-", None, None, 1, book, 148, 
        "Um bastão de madeira ou metal com uma cabeça pesada e flangeada na ponta. Muito utilizada por clérigos que fazem votos de não derramar sangue cortando carne.", 
        ["bastão", "impacto", "clérigo"]))

    # Armas Simples - Corpo a Corpo - Duas Mãos
    items.append(make_item("arma-bordao", "Bordão", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos", "T$ 0", "1d6/1d6", "x2", "Impacto", "-", None, None, 2, book, 147, 
        "Um cajado apreciado por viajantes e camponeses por sua praticidade e fácil acesso (seu preço é zero). O bordão é uma arma dupla.", 
        ["cajado", "dupla", "grátis", "viajante"]))

    items.append(make_item("arma-pique", "Pique", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos", "T$ 2", "1d8", "x2", "Perfuração", "-", None, None, 2, book, 148, 
        "Uma lança muito longa (entre 3 e 4,5m). O pique é uma arma alongada. Uma arma alongada dobra o seu alcance natural, mas não permite que você ataque um inimigo adjacente.", 
        ["haste longa", "alongada", "alcance"]) )

    items.append(make_item("arma-tacape", "Tacape", "Armas", "Armas Simples", "Corpo a Corpo / Duas Mãos", "T$ 0", "1d10", "x2", "Impacto", "-", None, None, 2, book, 148, 
        "Um tronco ou galho pesado e irregular, usado com as duas mãos por humanoides primitivos ou brutais.", 
        ["tronco", "grátis", "brutal", "duas mãos"]))

    # Armas Simples - Ataque à Distância - Uma Mão
    items.append(make_item("arma-azagaia", "Azagaia", "Armas", "Armas Simples", "Ataque à Distância / Uma Mão", "T$ 1", "1d6", "x2", "Perfuração", "Médio", None, None, 1, book, 146, 
        "Uma lança flexível própria para arremesso.", 
        ["lança de arremesso", "arremesso", "distância"]))

    items.append(make_item("arma-besta-leve", "Besta Leve", "Armas", "Armas Simples", "Ataque à Distância / Uma Mão", "T$ 35", "1d8", "19", "Perfuração", "Médio", None, None, 1, book, 146, 
        "Uma arma de disparo mecânica feita de um arco montado sobre uma coronha. Recarregar uma besta leve é uma ação de movimento.", 
        ["besta", "disparo", "mecanismo"]))

    # Armas Simples - Ataque à Distância - Duas Mãos
    items.append(make_item("arma-funda", "Funda", "Armas", "Armas Simples", "Ataque à Distância / Duas Mãos", "T$ 0", "1d4", "x2", "Impacto", "Médio", None, None, 1, book, 147, 
        "Uma tira de couro usada para lançar pedras com força e velocidade surpreendentes. Ao usar uma funda, você aplica seu modificador de Força às rolagens de dano. Recarregar uma funda com uma pedra é uma ação de movimento.", 
        ["estilingue", "força no dano", "pedras", "grátis"]))

    items.append(make_item("arma-arco-curto", "Arco Curto", "Armas", "Armas Simples", "Ataque à Distância / Duas Mãos", "T$ 30", "1d6", "x3", "Perfuração", "Médio", None, None, 2, book, 146, 
        "Um arco pequeno, ideal para caçadas em florestas fechadas ou para atirar a cavalo.", 
        ["arco", "disparo", "caça"]))

    # Armas Marciais - Corpo a Corpo - Leves
    items.append(make_item("arma-machadinha", "Machadinha", "Armas", "Armas Marciais", "Corpo a Corpo / Leve", "T$ 6", "1d6", "x3", "Corte", "Curto", None, None, 1, book, 148, 
        "Um machado de cabo curto, próprio para combate rápido corpo a corpo ou para ser arremessado.", 
        ["machado", "arremesso", "crítico x3"]))

    # Armas Marciais - Corpo a Corpo - Uma Mão
    items.append(make_item("arma-cimitarra", "Cimitarra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 15", "1d6", "18", "Corte", "-", None, None, 1, book, 147, 
        "Uma espada com lâmina curva, muito popular no Deserto da Perdição. Quando ataca com uma cimitarra, você pode usar sua Destreza em vez de Força nos testes de ataque.", 
        ["espada curva", "acuidade", "crítico 18"]))

    items.append(make_item("arma-espada-longa", "Espada Longa", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 15", "1d8", "19", "Corte", "-", None, None, 1, book, 147, 
        "A arma tradicional de soldados e cavaleiros artonianos. Uma lâmina reta de dois gumes com cabo para uma mão.", 
        ["espada", "cavaleiro", "soldado"]))

    items.append(make_item("arma-florete", "Florete", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 20", "1d6", "18", "Perfuração", "-", None, None, 1, book, 147, 
        "Uma espada fina e flexível, própria para estocadas. Quando ataca com um florete, você pode usar sua Destreza em vez de Força nos testes de ataque.", 
        ["estocada", "acuidade", "esgrima", "crítico 18"]))

    items.append(make_item("arma-machado-de-batalha", "Machado de Batalha", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 10", "1d8", "x3", "Corte", "-", None, None, 1, book, 148, 
        "A arma favorita dos anões, um machado de lâmina larga forjado para combate.", 
        ["machado", "anão", "crítico x3"]))

    items.append(make_item("arma-mangual", "Mangual", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 8", "1d8", "x2", "Impacto", "-", None, None, 1, book, 148, 
        "Uma haste de madeira ligada por uma corrente a uma bola de ferro com cravos. O mangual é uma arma versátil. Uma arma versátil fornece +2 em testes para desarmar e derrubar.", 
        ["corrente", "versátil", "desarmar", "derrubar"]))

    items.append(make_item("arma-martelo-de-guerra", "Martelo de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 12", "1d8", "x3", "Impacto", "-", None, None, 1, book, 148, 
        "Um martelo pesado de metal, com uma ponta na extremidade oposta à cabeça, capaz de esmagar armaduras de placas.", 
        ["martelo", "impacto", "crítico x3"]))

    items.append(make_item("arma-picareta", "Picareta", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 8", "1d6", "x4", "Perfuração", "-", None, None, 1, book, 148, 
        "Uma ferramenta de mineração adaptada para combate, dotada de uma ponta de aço muito afiada capaz de infligir ferimentos letais.", 
        ["mineração", "crítico x4", "perfurante"]))

    items.append(make_item("arma-tridente", "Tridente", "Armas", "Armas Marciais", "Corpo a Corpo / Uma Mão", "T$ 15", "1d8", "x2", "Perfuração", "Curto", None, None, 1, book, 148, 
        "Uma lança com três pontas de ferro, muito usada por pescadores, marinheiros e devotos de Oceano. Pode ser arremessada.", 
        ["tridente", "oceano", "arremesso"]))

    # Armas Marciais - Corpo a Corpo - Duas Mãos
    items.append(make_item("arma-alabarda", "Alabarda", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 10", "1d10", "x3", "Corte/perfuração", "-", None, None, 2, book, 146, 
        "Uma longa haste de madeira terminando em uma lâmina de machado encimada por uma ponta de lança. A alabarda é uma arma alongada.", 
        ["haste", "alongada", "crítico x3", "infantaria"]))

    items.append(make_item("arma-alfange", "Alfange", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 75", "2d4", "18", "Corte", "-", None, None, 2, book, 146, 
        "Uma espada larga de lâmina muito curva, usada com as duas mãos para desferir golpes cortantes devastadores.", 
        ["espada curva", "duas mãos", "crítico 18"]))

    items.append(make_item("arma-gadanho", "Gadanho", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 18", "2d4", "x4", "Corte", "-", None, None, 2, book, 148, 
        "Uma versão de guerra da foice camponesa, com uma lâmina longa e curvada montada perpendicularmente no topo de uma haste de duas mãos.", 
        ["foice de guerra", "crítico x4", "duas mãos"]))

    items.append(make_item("arma-lanca-montada", "Lança Montada", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 10", "1d8", "x3", "Perfuração", "-", None, None, 2, book, 148, 
        "Feita para combate a cavalo, tem um guarda-mão largo e ponta afiada. Causa dano dobrado quando usada em investida montada.", 
        ["justa", "montaria", "investida montada", "crítico x3"]))

    items.append(make_item("arma-machado-de-guerra", "Machado de Guerra", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 20", "1d12", "x3", "Corte", "-", None, None, 2, book, 148, 
        "Um machado imenso com duas lâminas pesadas, forjado para desmembrar oponentes com facilidade.", 
        ["machado pesado", "crítico x3", "duas mãos"]))

    items.append(make_item("arma-marreta", "Marreta", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 20", "3d4", "x2", "Impacto", "-", None, None, 2, book, 148, 
        "Um martelo colossal com cabeça pesada de ferro e cabo longo de madeira, capaz de esmagar armaduras e ossos.", 
        ["martelo colossal", "esmagar", "duas mãos"]))

    items.append(make_item("arma-montante", "Montante", "Armas", "Armas Marciais", "Corpo a Corpo / Duas Mãos", "T$ 50", "2d6", "19", "Corte", "-", None, None, 2, book, 148, 
        "A maior das espadas tradicionais, medindo até 1,8m de comprimento, com lâmina reta de corte formidável.", 
        ["espada de duas mãos", "espadão", "duas mãos"]))

    # Armas Marciais - Ataque à Distância - Duas Mãos
    items.append(make_item("arma-arco-longo", "Arco Longo", "Armas", "Armas Marciais", "Ataque à Distância / Duas Mãos", "T$ 100", "1d8", "x3", "Perfuração", "Médio", None, None, 2, book, 146, 
        "Um arco de grande estatura feito de madeira nobre e flexível. Ao disparar um arco longo, você aplica seu modificador de Força às rolagens de dano.", 
        ["arco potente", "força no dano", "disparo", "crítico x3"]))

    items.append(make_item("arma-besta-pesada", "Besta Pesada", "Armas", "Armas Marciais", "Ataque à Distância / Duas Mãos", "T$ 50", "1d12", "19", "Perfuração", "Médio", None, None, 2, book, 146, 
        "Uma versão reforçada da besta, feita de madeira de lei e aço. Recarregar uma besta pesada é uma ação padrão.", 
        ["besta pesada", "disparo", "dano pesado"]))

    # Armas Exóticas - Corpo a Corpo - Uma Mão
    items.append(make_item("arma-chicote", "Chicote", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 2", "1d3", "x2", "Corte", "-", None, None, 1, book, 147, 
        "Uma tira longa de couro trançado terminando em pontas afiadas. O chicote é uma arma ágil, versátil e alongada que permite atacar alvos adjacentes.", 
        ["couro", "ágil", "versátil", "alongada", "acuidade"]))

    items.append(make_item("arma-espada-bastarda", "Espada Bastarda", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 35", "1d10/1d12", "19", "Corte", "-", None, None, 1, book, 147, 
        "Maior que a espada longa e menor que o montante. Pode ser usada com uma mão (1d10) ou com as duas mãos (1d12).", 
        ["espada e meia", "versátil", "uma ou duas mãos"]))

    items.append(make_item("arma-katana", "Katana", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 100", "1d8/1d10", "19", "Corte", "-", None, None, 1, book, 148, 
        "A tradicional espada dos samurais de Tamu-ra, com lâmina curva de aço dobrado. É uma arma ágil e pode ser empunhada com uma (1d8) ou duas mãos (1d10).", 
        ["tamura", "samurai", "ágil", "acuidade"]))

    items.append(make_item("arma-machado-anao", "Machado Anão", "Armas", "Armas Exóticas", "Corpo a Corpo / Uma Mão", "T$ 30", "1d10", "x3", "Corte", "-", None, None, 1, book, 148, 
        "Forjado com técnicas secretas de Doherimm, este machado de guerra pesado pode ser empunhado com apenas uma mão por um guerreiro treinado.", 
        ["doherimm", "anão", "crítico x3"]))

    # Armas Exóticas - Corpo a Corpo - Duas Mãos
    items.append(make_item("arma-corrente-de-espinhos", "Corrente de Espinhos", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos", "T$ 25", "2d4/2d4", "19", "Corte", "-", None, None, 2, book, 147, 
        "Uma corrente de ferro de 2,5m coberta de lâminas e pontas afiadas. É uma arma ágil, dupla e versátil.", 
        ["corrente", "ágil", "dupla", "versátil", "acuidade"]))

    items.append(make_item("arma-machado-taurico", "Machado Táurico", "Armas", "Armas Exóticas", "Corpo a Corpo / Duas Mãos", "T$ 50", "2d8", "x3", "Corte", "-", None, None, 2, book, 148, 
        "A arma colossal favorita dos minotauros de Tapista, com lâminas enormes que exigem força formidável.", 
        ["minotauro", "tapista", "dano maciço", "crítico x3"]))

    # Armas Exóticas - Ataque à Distância - Uma Mão
    items.append(make_item("arma-rede", "Rede", "Armas", "Armas Exóticas", "Ataque à Distância / Uma Mão", "T$ 20", "-", "-", "-", "Curto", None, None, 1, book, 148, 
        "Uma rede com chumbadas nas pontas. Ao acertar um ataque com uma rede, o alvo fica enredado. Para se libertar, a criatura precisa gastar uma ação padrão e passar num teste de Acrobacia ou Atletismo (CD 20).", 
        ["enredar", "imobilizar", "captura"]))

    # Armas de Fogo
    items.append(make_item("arma-pistola", "Pistola", "Armas", "Armas de Fogo", "Ataque à Distância / Leve", "T$ 250", "2d6", "19/x3", "Perfuração", "Curto", None, None, 1, book, 148, 
        "Uma arma de fogo de cano curto operada por pólvora e pederneira. Recarregar uma pistola é uma ação padrão.", 
        ["pólvora", "arma de fogo", "crítico x3"]))

    items.append(make_item("arma-mosquete", "Mosquete", "Armas", "Armas de Fogo", "Ataque à Distância / Duas Mãos", "T$ 500", "2d8", "19/x3", "Perfuração", "Médio", None, None, 2, book, 148, 
        "Uma arma de fogo longa com cano raiado e grande poder de parada. Recarregar um mosquete é uma ação padrão.", 
        ["pólvora", "arma de fogo", "alcance médio", "crítico x3"]))

    # =========================================================================
    # 2. MUNIÇÕES (Tabela 3-4, Página 151)
    # =========================================================================
    items.append(make_item("municao-balas", "Balas", "Munições", "Munição de Arma de Fogo", "Munição", "T$ 20", "-", "-", "Perfuração", "-", None, None, 1, book, 151, 
        "Uma bolsa com 20 balas (pequenas esferas de chumbo) e pólvora. Usadas em pistolas e mosquetes. Recarregar uma arma de fogo é uma ação padrão.", 
        ["projéteis", "pólvora", "balas", "chumbo"]))

    items.append(make_item("municao-flechas", "Flechas", "Munições", "Munição de Arco", "Munição", "T$ 1", "-", "-", "Perfuração", "-", None, None, 1, book, 151, 
        "Uma aljava com 20 flechas, hastes de madeira com ponta metálica e penas para estabilizar o voo. Recarregar um arco com uma flecha é uma ação livre.", 
        ["projéteis", "arco", "flechas", "aljava"]))

    items.append(make_item("municao-pedras", "Pedras", "Munições", "Munição de Funda", "Munição", "T$ 0,5", "-", "-", "Impacto", "-", None, None, 1, book, 151, 
        "Um saco de couro com 20 pedras polidas. Recarregar uma funda com uma pedra é uma ação de movimento.", 
        ["funda", "pedras", "projéteis"]))

    items.append(make_item("municao-virotes", "Virotes", "Munições", "Munição de Besta", "Munição", "T$ 2", "-", "-", "Perfuração", "-", None, None, 1, book, 151, 
        "Uma aljava com 20 setas de madeira com ponta metálica pesada para bestas. Recarregar uma besta leve é uma ação de movimento; já recarregar uma besta pesada é uma ação padrão.", 
        ["besta", "virotes", "setas", "aljava"]))

    # =========================================================================
    # 3. ARMADURAS & ESCUDOS (Tabela 3-5, Página 153; Descrições Páginas 152-154)
    # =========================================================================
    items.append(make_item("armadura-armadura-acolchoada", "Armadura Acolchoada", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 5", None, None, None, None, "+1", "0", 2, book, 152, 
        "Mais grossa que uma roupa comum, esta armadura é feita de várias camadas de tecido acolchoado com lã ou algodão.", 
        ["leve", "tecido", "sem penalidade"]))

    items.append(make_item("armadura-armadura-de-couro", "Armadura de Couro", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 20", None, None, None, None, "+2", "0", 2, book, 152, 
        "O peitoral desta armadura é feito de couro curtido em óleo para endurecer, enquanto o resto é feito de couro flexível.", 
        ["couro", "leve", "sem penalidade"]))

    items.append(make_item("armadura-couro-batido", "Couro Batido", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 35", None, None, None, None, "+3", "-1", 2, book, 152, 
        "Versão mais pesada da armadura de couro, reforçada com rebites de metal.", 
        ["couro", "rebites", "leve"]))

    items.append(make_item("armadura-gibao-de-peles", "Gibão de Peles", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 25", None, None, None, None, "+4", "-3", 2, book, 152, 
        "Usada por bárbaros e povos primitivos, consiste em várias camadas de peles de animais sobrepostas.", 
        ["peles", "bárbaro", "leve"]))

    items.append(make_item("armadura-couraca", "Couraça", "Armaduras e Escudos", "Armaduras Leves", "Armadura Leve", "T$ 500", None, None, None, None, "+5", "-4", 2, book, 152, 
        "Uma peça de metal inteiriça que protege o tronco do usuário, acompanhada de perneiras e braçadeiras de couro leve.", 
        ["metal", "peitoral", "melhor armadura leve"]))

    items.append(make_item("armadura-brunea", "Brunea", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 50", None, None, None, None, "+5", "-2", 5, book, 152, 
        "Um colete de couro coberto com pequenas placas de metal sobrepostas, como escamas de um peixe.", 
        ["pesada", "escamas", "econômica"]))

    items.append(make_item("armadura-cota-de-malha", "Cota de Malha", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 150", None, None, None, None, "+6", "-2", 5, book, 152, 
        "Feita de anéis de aço entrelaçados, cobre o tronco, braços e pernas, acompanhada por um capuz de malha.", 
        ["malha", "anéis", "pesada"]))

    items.append(make_item("armadura-loriga-segmentada", "Loriga Segmentada", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 250", None, None, None, None, "+7", "-3", 5, book, 152, 
        "Composta de tiras horizontais de metal rebitadas em tiras de couro, muito comum entre legionários táuricos.", 
        ["tiras", "tapista", "pesada"]))

    items.append(make_item("armadura-meia-armadura", "Meia Armadura", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 600", None, None, None, None, "+8", "-4", 5, book, 152, 
        "Combina placas de metal nas áreas vitais (tronco, ombros, pernas) com cota de malha e couro nas articulações.", 
        ["placas", "malha", "pesada"]))

    items.append(make_item("armadura-armadura-completa", "Armadura Completa", "Armaduras e Escudos", "Armaduras Pesadas", "Armadura Pesada", "T$ 3.000", None, None, None, None, "+10", "-5", 5, book, 152, 
        "A armadura máxima do cavaleiro: placas de aço moldadas que cobrem o corpo inteiro, feitas sob medida e acompanhadas de elmo, manoplas e grevas.", 
        ["placas completas", "cavaleiro", "pesada", "máxima"]))

    items.append(make_item("armadura-escudo-leve", "Escudo Leve", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 5", None, None, None, None, "+1", "-1", 1, book, 154, 
        "Um escudo pequeno de madeira ou couro reforçado preso ao antebraço, permitindo carregar um objeto na mão (mas não empunhar uma arma).", 
        ["madeira", "antebraço", "escudo"]))

    items.append(make_item("armadura-escudo-pesado", "Escudo Pesado", "Armaduras e Escudos", "Escudos", "Escudo", "T$ 15", None, None, None, None, "+2", "-2", 2, book, 154, 
        "Um grande escudo de aço ou madeira reforçada com ferro. Precisa ser empunhado com uma das mãos com firmeza.", 
        ["metal", "aço", "proteção", "escudo"]))

    # =========================================================================
    # 4. ITENS GERAIS (Tabela 3-6, Páginas 156-157; Descrições Páginas 157-162)
    # =========================================================================

    # Equipamento de Aventura
    items.append(make_item("item-agua-benta", "Água Benta", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 10", None, None, "Sagrado", "Curto", None, None, 0.5, book, 157, 
        "Água abençoada por clérigos de deuses bondosos. Um frasco de água benta pode ser arremessado em alcance curto como um ataque à distância. Causa 2d6 pontos de dano de luz em mortos-vivos e espíritos.", 
        ["luz", "morto-vivo", "arremesso", "sagrado"]))

    items.append(make_item("item-algemas", "Algemas", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 15", None, None, None, None, None, None, 1, book, 157, 
        "Algemas de ferro forjado para prender as mãos ou pés de uma criatura Média. Abrir algemas sem a chave exige um teste de Ladinagem (CD 20); escapar delas exige Acrobacia (CD 25) e quebrar exige Atletismo (CD 25).", 
        ["ferro", "prender", "ladinagem"]))

    items.append(make_item("item-arpeu", "Arpéu", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 5", None, None, None, None, None, None, 1, book, 157, 
        "Um gancho de ferro de quatro pontas próprio para ser amarrado a uma corda e lançado para fixação em muros ou árvores.", 
        ["gancho", "escalada", "corda"]))

    items.append(make_item("item-bandoleira-de-pocoes", "Bandoleira de Poções", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 20", None, None, None, None, None, None, 1, book, 157, 
        "Um cinto de couro com compartimentos acolchoados para frascos. Permite sacar itens alquímicos e poções nela armazenados (máximo de 4) como uma ação livre.", 
        ["cinto", "poções", "saque rápido"]))

    items.append(make_item("item-barraca", "Barraca", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 10", None, None, None, None, None, None, 1, book, 157, 
        "Uma tenda de lona resistente capaz de abrigar duas pessoas e seus equipamentos contra chuva e intempéries.", 
        ["tenda", "acampamento", "abrigo"]))

    items.append(make_item("item-corda", "Corda", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 1", None, None, None, None, None, None, 1, book, 157, 
        "Uma corda de cânhamo resistente com 15m de comprimento. Fornece +2 em testes de Atletismo para escalar quando amarrada.", 
        ["cânhamo", "escalada", "amarrar"]))

    items.append(make_item("item-espelho", "Espelho", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 10", None, None, None, None, None, None, 1, book, 157, 
        "Um pequeno espelho de aço polido. Útil para espiar esquinas sem se expor ou para fazer sinais luminosos a distância.", 
        ["aço", "reflexo", "espionagem"]))

    items.append(make_item("item-lampiao", "Lampião", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 7", None, None, None, None, None, None, 1, book, 157, 
        "Uma lanterna fechada com paredes de vidro e aletas metálicas. Ilumina um raio de 9m por 6 horas com uma dose de óleo.", 
        ["iluminação", "óleo", "lanterna"]))

    items.append(make_item("item-mochila", "Mochila", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 2", None, None, None, None, None, None, 0, book, 157, 
        "Uma mochila de couro resistente que aumenta sua capacidade de carga em +2 espaços.", 
        ["capacidade de carga", "bolsa", "armazenamento"]))

    items.append(make_item("item-mochila-de-aventureiro", "Mochila de Aventureiro", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 50", None, None, None, None, None, None, 0, book, 157, 
        "Uma mochila espaçosa, com diversos compartimentos e tiras reforçadas. Aumenta sua capacidade de carga em +5 espaços.", 
        ["capacidade de carga", "aventureiro", "carga reforçada"]))

    items.append(make_item("item-oleo", "Óleo", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 0,1", None, None, None, None, None, None, 0.5, book, 157, 
        "Um frasco com óleo mineral combustível suficiente para manter um lampião aceso por 6 horas, ou para ser espalhado no chão.", 
        ["combustível", "lampião", "fogo"]))

    items.append(make_item("item-organizador-de-pergaminhos", "Organizador de Pergaminhos", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 25", None, None, None, None, None, None, 1, book, 157, 
        "Um estojo cilíndrico rígido de couro impermeável. Permite guardar até 6 pergaminhos e sacá-los como ação livre.", 
        ["pergaminhos", "estojo", "saque rápido"]))

    items.append(make_item("item-pe-de-cabra", "Pé de Cabra", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 2", None, None, None, None, None, None, 1, book, 157, 
        "Uma barra de ferro achatada em uma das pontas. Fornece +2 em testes de Atletismo e Força para arrombar portas e baús.", 
        ["ferro", "alavanca", "arrombamento"]))

    items.append(make_item("item-saco-de-dormir", "Saco de Dormir", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 1", None, None, None, None, None, None, 1, book, 157, 
        "Um acolchoado de lã e lona impermeável para dormir confortavelmente ao relento sem penalidade de descanso.", 
        ["descanso", "acampamento", "sono"]))

    items.append(make_item("item-simbolo-sagrado", "Símbolo Sagrado", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 5", None, None, None, None, None, None, 1, book, 157, 
        "Um medalhão de madeira ou metal com o símbolo de sua divindade. Quando empunhado ou vestido por um devoto, concede +1 em testes de resistência.", 
        ["divindade", "fé", "resistência", "clérigo"]))

    items.append(make_item("item-tocha", "Tocha", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 0,1", "1d4", "x2", "Impacto/Fogo", "-", None, None, 1, book, 157, 
        "Um bastão de madeira com estopa embebida em piche. Ilumina um raio de 9m por uma cena e pode ser usada como arma simples leve.", 
        ["fogo", "iluminação", "arma leve"]))

    items.append(make_item("item-vara-de-madeira-3m", "Vara de Madeira (3m)", "Itens Gerais", "Equipamento de Aventura", "Aventura", "T$ 0,2", None, None, None, None, None, None, 1, book, 157, 
        "Uma haste de madeira com 3 metros de comprimento. Útil para testar armadilhas e acionar mecanismos a distância segura.", 
        ["haste", "armadilhas", "exploração"]))

    # Ferramentas
    items.append(make_item("item-alaude-elfico", "Alaúde Élfico", "Itens Gerais", "Ferramentas", "Instrumento Musical", "T$ 300", None, None, None, None, None, None, 1, book, 158, 
        "Feito com madeira de troncos élficos de Lenórienn, produz acordes harmoniosos e cristalinos. Concede +2 em testes de Atuação com música e reduz o custo de habilidades de música bárdica em -1 PM.", 
        ["bardo", "música", "atuação", "élfico"]))

    items.append(make_item("item-colecao-de-livros", "Coleção de Livros", "Itens Gerais", "Ferramentas", "Ferramenta de Estudo", "T$ 75", None, None, None, None, None, None, 1, book, 158, 
        "Um conjunto de tomos e manuscritos sobre assuntos específicos. Fornece +2 em testes de Conhecimento, Guerra, Misticismo, Nobreza ou Religião (definido ao comprar).", 
        ["livros", "estudo", "conhecimento", "erudição"]))

    items.append(make_item("item-equipamento-de-viagem", "Equipamento de Viagem", "Itens Gerais", "Ferramentas", "Utensílio de Viagem", "T$ 10", None, None, None, None, None, None, 1, book, 158, 
        "Inclui cantil, panelas pequenas, talheres de madeira e pederneira. Necessário para evitar penalidades em testes de Sobrevivência em viagens.", 
        ["viagem", "sobrevivência", "utensílios"]))

    items.append(make_item("item-estojo-de-disfarces", "Estojo de Disfarces", "Itens Gerais", "Ferramentas", "Ferramenta de Ofício", "T$ 50", None, None, None, None, None, None, 1, book, 158, 
        "Contém perucas postiças, maquiagem teatral, próteses de cera e tintas para pele. Permite usar a perícia Enganação para criar disfarces convincentes.", 
        ["disfarce", "enganação", "maquiagem"]))

    items.append(make_item("item-flauta-mistica", "Flauta Mística", "Itens Gerais", "Ferramentas", "Instrumento Musical", "T$ 150", None, None, None, None, None, None, 1, book, 158, 
        "Uma flauta entalhada com runas arcanas que ressoam com a mana ambiente. Concede +1 na CD de suas magias que possuem componentes verbais.", 
        ["música", "magia", "bardo", "flauta"]))

    items.append(make_item("item-gazua", "Gazua", "Itens Gerais", "Ferramentas", "Ferramenta de Ladinagem", "T$ 5", None, None, None, None, None, None, 1, book, 158, 
        "Gazuas e ganchos de arame para abrir fechaduras. Necessário para abrir fechaduras com Ladinagem sem penalidade de -5.", 
        ["fechaduras", "ladinagem", "arrombamento"]))

    items.append(make_item("item-instrumentos-de-oficio", "Instrumentos de <ofício>", "Itens Gerais", "Ferramentas", "Ferramenta de Ofício", "T$ 30", None, None, None, None, None, None, 1, book, 158, 
        "Conjunto completo de ferramentas apropriadas para exercer um determinado Ofício (alquimia, armeiro, carpintaria, etc.). Sem instrumentos, você sofre -5 no teste.", 
        ["ofício", "trabalho", "fabricação"]))

    items.append(make_item("item-instrumento-musical", "Instrumento Musical", "Itens Gerais", "Ferramentas", "Instrumento Musical", "T$ 35", None, None, None, None, None, None, 1, book, 158, 
        "Um instrumento comum como tambor, flauta doce, pandeiro ou violino. Necessário para usar habilidades de Atuação musical.", 
        ["música", "atuação", "bardo"]))

    items.append(make_item("item-luneta", "Luneta", "Itens Gerais", "Ferramentas", "Ferramenta Óptica", "T$ 100", None, None, None, None, None, None, 1, book, 158, 
        "Um tubo com lentes de cristal polido que aproxima objetos distantes. Fornece +5 em testes de Percepção para observar a longas distâncias.", 
        ["óptica", "percepção", "visão"]))

    items.append(make_item("item-maleta-de-medicamentos", "Maleta de Medicamentos", "Itens Gerais", "Ferramentas", "Ferramenta de Cura", "T$ 50", None, None, None, None, None, None, 1, book, 158, 
        "Faixas esterilizadas, bisturis, pinças, agulhas e unguentos calmantes. Necessário para usar Primeiros Socorros e Cuidados Médicos na perícia Cura sem penalidade.", 
        ["cura", "medicina", "primeiros socorros"]))

    items.append(make_item("item-sela", "Sela", "Itens Gerais", "Ferramentas", "Acessório de Montaria", "T$ 20", None, None, None, None, None, None, 1, book, 158, 
        "Uma sela de couro com estribos ajustáveis montada sobre o dorso de um animal. Necessária para cavalgar sem penalidades em Cavalgar/Pilotagem.", 
        ["montaria", "cavalo", "cavalgar"]))

    items.append(make_item("item-tambor-das-profundezas", "Tambor das Profundezas", "Itens Gerais", "Ferramentas", "Instrumento Musical", "T$ 80", None, None, None, None, None, None, 1, book, 158, 
        "Um tambor de guerra feito de madeira densa e couro de trobo, com batidas retumbantes que reverberam por quilômetros.", 
        ["guerra", "tambor", "bardo", "atuação"]))

    # Vestuário
    items.append(make_item("item-andrajos-de-aldeao", "Andrajos de Aldeão", "Itens Gerais", "Vestuário", "Traje", "T$ 1", None, None, None, None, None, None, 1, book, 158, 
        "Roupas gastas, manchadas e remendadas típicas de camponeses paupérrimos. Concede +2 em testes de Enganação e Furtividade para se misturar a multidões de plebeus.", 
        ["camponês", "disfarce", "humilde"]))

    items.append(make_item("item-bandana", "Bandana", "Itens Gerais", "Vestuário", "Acessório de Cabeça", "T$ 5", None, None, None, None, None, None, 1, book, 158, 
        "Um lenço de tecido colorido amarrado na cabeça ou no pescoço. Muito popular entre marinheiros e piratas do Mar Negro.", 
        ["pirata", "estilo", "acessório"]))

    items.append(make_item("item-botas-reforcadas", "Botas Reforçadas", "Itens Gerais", "Vestuário", "Calçado", "T$ 20", None, None, None, None, None, None, 1, book, 158, 
        "Botas de cano alto feitas de couro espesso com solado reforçado de madeira ou ferro. Concede +1 em testes de Fortitude em marchas prolongadas.", 
        ["botas", "marcha", "resistência"]))

    items.append(make_item("item-camisa-bufante", "Camisa Bufante", "Itens Gerais", "Vestuário", "Traje", "T$ 25", None, None, None, None, None, None, 1, book, 158, 
        "Camisa de linho fino com mangas amplas e gola elegante, muito apreciada por duelistas, nobres e piratas galantes.", 
        ["elegante", "duelista", "nobreza"]))

    items.append(make_item("item-capa-esvoacante", "Capa Esvoaçante", "Itens Gerais", "Vestuário", "Capa", "T$ 25", None, None, None, None, None, None, 1, book, 158, 
        "Uma capa de tecido leve e corte dramático que ondula com o vento, adicionando elegância aos movimentos do herói.", 
        ["capa", "estilo", "teatral"]))

    items.append(make_item("item-capa-pesada", "Capa Pesada", "Itens Gerais", "Vestuário", "Capa", "T$ 15", None, None, None, None, None, None, 1, book, 158, 
        "Feita de lã grossa forrada com pele, mantém o usuário aquecido e fornece +2 em testes de Fortitude contra efeitos de frio extremo.", 
        ["frio", "inverno", "resistência", "capa"]))

    items.append(make_item("item-casaco-longo", "Casaco Longo", "Itens Gerais", "Vestuário", "Traje", "T$ 20", None, None, None, None, None, None, 1, book, 158, 
        "Sobretudo de couro ou tecido pesado que desce até os tornozelos, protegendo contra o vento e poeira da estrada.", 
        ["sobretudo", "viagem", "proteção"]))

    items.append(make_item("item-chapeu-arcano", "Chapéu Arcano", "Itens Gerais", "Vestuário", "Acessório de Cabeça", "T$ 50", None, None, None, None, None, None, 1, book, 158, 
        "O clássico chapéu pontudo e cônico favorito de magos e ilusionistas, bordado com fios de prata e constelações.", 
        ["arcano", "mago", "chapéu"]))

    items.append(make_item("item-enfeite-de-elmo", "Enfeite de Elmo", "Itens Gerais", "Vestuário", "Acessório de Armadura", "T$ 15", None, None, None, None, None, None, 1, book, 158, 
        "Penachos coloridos, asas de bronze ou cristas esculpidas instaladas no elmo para indicar patente ou impressionar oponentes.", 
        ["elmo", "cavaleiro", "intimidação"]))

    items.append(make_item("item-farrapos-de-ermitao", "Farrapos de Ermitão", "Itens Gerais", "Vestuário", "Traje", "T$ 1", None, None, None, None, None, None, 1, book, 158, 
        "Vestimentas grosseiras feitas de trapos e cordas desfiadas usadas por anacoretas e eremitas nos ermos.", 
        ["eremita", "humilde", "ermos"]))

    items.append(make_item("item-gorro-de-ervas", "Gorro de Ervas", "Itens Gerais", "Vestuário", "Acessório de Cabeça", "T$ 75", None, None, None, None, None, None, 1, book, 158, 
        "Um gorro forrado internamente com ervas aromáticas e calmantes que clareiam a mente do usuário, concedendo +1 em testes de Vontade.", 
        ["ervas", "mente", "vontade"]))

    items.append(make_item("item-luva-de-pelica", "Luva de Pelica", "Itens Gerais", "Vestuário", "Acessório de Mão", "T$ 5", None, None, None, None, None, None, 1, book, 158, 
        "Luvas feitas de couro de cabra finíssimo e macio que não tiram a sensibilidade das pontas dos dedos.", 
        ["couro fino", "elegância", "mão"]))

    items.append(make_item("item-manopla", "Manopla", "Itens Gerais", "Vestuário", "Acessório de Armadura", "T$ 10", None, None, None, None, None, None, 1, book, 158, 
        "Uma luva articulada de placas de aço forjado. Permite desferir ataques desarmados causando dano letal e receber melhorias e encantos de armas.", 
        ["luva de metal", "ataque desarmado letal", "melhorias"]))

    items.append(make_item("item-manto-camuflado", "Manto Camuflado", "Itens Gerais", "Vestuário", "Capa", "T$ 12", None, None, None, None, None, None, 1, book, 158, 
        "Um manto tingido com padrões específicos para um bioma (floresta, deserto, neve). Fornece +2 em Furtividade no terreno correspondente.", 
        ["camuflagem", "furtividade", "terreno"]))

    items.append(make_item("item-manto-eclesiastico", "Manto Eclesiástico", "Itens Gerais", "Vestuário", "Traje Religioso", "T$ 20", None, None, None, None, None, None, 1, book, 158, 
        "Manto cerimonial bordado com os dogmas e insígnias sagradas de uma divindade do Panteão.", 
        ["clérigo", "religião", "sagrado"]))

    items.append(make_item("item-robe-mistico", "Robe Místico", "Itens Gerais", "Vestuário", "Traje Arcano", "T$ 50", None, None, None, None, None, None, 1, book, 158, 
        "Túnica ampla confeccionada em veludo de seda especial, confortável para canalizar energias místicas sem interferir nos gestos arcanos.", 
        ["arcano", "mago", "misticismo"]))

    items.append(make_item("item-sapatos-de-camurca", "Sapatos de Camurça", "Itens Gerais", "Vestuário", "Calçado", "T$ 8", None, None, None, None, None, None, 1, book, 158, 
        "Calçados com solado macio que amortecem os passos, fornecendo +1 em testes de Furtividade em pisos lisos.", 
        ["calçado", "furtividade", "silêncio"]))

    items.append(make_item("item-tabardo", "Tabardo", "Itens Gerais", "Vestuário", "Traje Militar", "T$ 10", None, None, None, None, None, None, 1, book, 158, 
        "Uma sobreveste sem mangas aberta nas laterais estampando o brasão militar de um lorde, guilda ou ordem de cavaleiros.", 
        ["brasão", "nobreza", "militar"]))

    items.append(make_item("item-traje-da-corte", "Traje da Corte", "Itens Gerais", "Vestuário", "Traje Aristocrático", "T$ 100", None, None, None, None, None, None, 1, book, 158, 
        "Roupas luxuosas de tecidos importados e fios de ouro. Concede +1 em testes de Diplomacia e Nobreza em eventos aristocráticos.", 
        ["luxo", "nobreza", "corte", "diplomacia"]))

    items.append(make_item("item-traje-de-viajante", "Traje de Viajante", "Itens Gerais", "Vestuário", "Traje Comum", "T$ 10", None, None, None, None, None, None, 0, book, 158, 
        "Camisa de linho, calças de lã resistente, botas de couro e cinto. É a roupa padrão vestida por aventureiros (não ocupa espaço vestida).", 
        ["roupa padrão", "viagem", "conforto"]))

    items.append(make_item("item-veste-de-seda", "Veste de Seda", "Itens Gerais", "Vestuário", "Traje Fino", "T$ 25", None, None, None, None, None, None, 1, book, 158, 
        "Uma túnica fina e lustrosa tecida com fios de bicho-da-seda do sul, leve e agradável ao toque.", 
        ["seda", "luxo", "nobre"]))

    # Esotéricos
    items.append(make_item("item-bolsa-de-po", "Bolsa de Pó", "Itens Gerais", "Esotéricos", "Catalisador Mágico", "T$ 300", None, None, None, None, None, None, 1, book, 159, 
        "Uma bolsa de couro contendo cinzas vulcânicas, pó de ossos e gemas moídas. Quando lança uma magia através dela, o alcance aumenta em um passo.", 
        ["esotérico", "magia", "alcance ampliado"]))

    items.append(make_item("item-cajado-arcano", "Cajado Arcano", "Itens Gerais", "Esotéricos", "Foco Arcano", "T$ 1.000", None, None, None, None, None, None, 2, book, 159, 
        "Um longo bastão entalhado em carvalho antigo com ponta de cristal puro. Concede +1 na CD de suas magias e pode ser usado como bordão em combate.", 
        ["esotérico", "cajado", "cd de magias", "mago"]))

    items.append(make_item("item-cetro-elemental", "Cetro Elemental", "Itens Gerais", "Esotéricos", "Foco Elemental", "T$ 750", None, None, None, None, None, None, 1, book, 159, 
        "Um bastão curto adornado com fragmentos elementais. Quando você lança uma magia que causa dano elemental (fogo, frio, eletricidade ou ácido), ela causa +2 pontos de dano por dado de dano.", 
        ["esotérico", "elementos", "dano mágico", "cetro"]))

    items.append(make_item("item-costela-de-lich", "Costela de Lich", "Itens Gerais", "Esotéricos", "Foco Necromântico", "T$ 300", None, None, None, None, None, None, 1, book, 159, 
        "O osso petrificado de um necromante lendário. Suas magias de Necromancia custam -1 PM (mínimo 1 PM).", 
        ["esotérico", "necromancia", "osso", "pm"]))

    items.append(make_item("item-dedo-de-ente", "Dedo de Ente", "Itens Gerais", "Esotéricos", "Foco da Natureza", "T$ 200", None, None, None, None, None, None, 1, book, 159, 
        "Um galho vivo arrancado de um guardião vegetal ancestral. Suas magias de Ilusão e Encantamento têm sua CD aumentada em +1.", 
        ["esotérico", "druida", "natureza", "ilusão"]))

    items.append(make_item("item-luva-de-ferro", "Luva de Ferro", "Itens Gerais", "Esotéricos", "Foco de Convocação", "T$ 150", None, None, None, None, None, None, 1, book, 159, 
        "Uma luva de metal gravada com sigilos arcanos. Criaturas conjuradas por você através desta luva recebem +1 em testes de ataque e na Defesa.", 
        ["esotérico", "convocação", "invocador"]))

    items.append(make_item("item-medalhao-de-prata", "Medalhão de Prata", "Itens Gerais", "Esotéricos", "Foco Divino", "T$ 750", None, None, None, None, None, None, 1, book, 159, 
        "Um medalhão de prata polida gravado com runas protetoras. Concede +1 em todos os testes de resistência contra magias e habilidades mágicas.", 
        ["esotérico", "prata", "resistência a magias"]))

    items.append(make_item("item-orbe-cristalino", "Orbe Cristalino", "Itens Gerais", "Esotéricos", "Foco de Adivinhação", "T$ 750", None, None, None, None, None, None, 1, book, 159, 
        "Uma esfera translúcida de quartzo puro. Permite que você pague +1 PM ao lançar uma magia para rolar novamente um dado de dano dela.", 
        ["esotérico", "cristal", "orbe", "adivinhação"]))

    items.append(make_item("item-tomo-hermetico", "Tomo Hermético", "Itens Gerais", "Esotéricos", "Grimório Especial", "T$ 1.500", None, None, None, None, None, None, 1, book, 159, 
        "Um livro grosso repleto de anotações complexas e teoremas místicos. Permite que você prepare uma magia adicional de qualquer círculo que possa lançar.", 
        ["esotérico", "grimório", "magia extra", "mago"]))

    items.append(make_item("item-varinha-arcana", "Varinha Arcana", "Itens Gerais", "Esotéricos", "Foco Básico", "T$ 100", None, None, None, None, None, None, 1, book, 159, 
        "Uma haste de madeira nobre polida de 30cm com ponta afunilada, muito comum entre aprendizes da Academia Arcana.", 
        ["esotérico", "varinha", "mago", "foco básico"]))

    # Alquímicos - Preparados
    items.append(make_item("item-acido", "Ácido", "Itens Gerais", "Alquímicos - Preparados", "Alquímico de Combate", "T$ 10", "2d4", "-", "Ácido", "Curto", None, None, 0.5, book, 160, 
        "Um frasco com líquido corrosivo que pode ser arremessado em alcance curto como ataque à distância. Causa 2d4 pontos de dano de ácido.", 
        ["alquimia", "ácido", "corrosivo", "arremesso"]))

    items.append(make_item("item-balsamo-restaurador", "Bálsamo Restaurador", "Itens Gerais", "Alquímicos - Preparados", "Alquímico Curativo", "T$ 10", None, None, None, None, None, None, 0.5, book, 160, 
        "Uma pasta medicinal de ervas maceradas. Aplicar como ação padrão recupera 2d4 pontos de vida do usuário.", 
        ["cura", "alquimia", "pv", "recuperação"]))

    items.append(make_item("item-bomba", "Bomba", "Itens Gerais", "Alquímicos - Preparados", "Alquímico Explosivo", "T$ 50", "6d6", "-", "Fogo e Impacto", "Curto", None, None, 0.5, book, 160, 
        "Um vaso de cerâmica cheio de pólvora com pavio curto. Ao ser arremessada, explode em uma área de 3m de raio causando 6d6 de dano (Reflexos CD 15 reduz à metade).", 
        ["explosão", "alquimia", "área", "bomba"]))

    items.append(make_item("item-cosmetico", "Cosmético", "Itens Gerais", "Alquímicos - Preparados", "Alquímico Social", "T$ 30", None, None, None, None, None, None, 0.5, book, 160, 
        "Pó aromático e cremes finos que realçam a beleza e o magnetismo pessoal. Fornece +1 em testes de perícias baseadas em Carisma durante uma cena.", 
        ["carisma", "beleza", "diplomacia", "alquimia"]))

    items.append(make_item("item-elixir-do-amor", "Elixir do Amor", "Itens Gerais", "Alquímicos - Preparados", "Alquímico Mental", "T$ 100", None, None, None, None, None, None, 0.5, book, 160, 
        "Uma poção rosada adocicada. Uma criatura que ingira este líquido fica sob efeito similar ao da magia Enfeitiçar (Vontade CD 15 anula).", 
        ["sedução", "enfeitiçar", "alquimia"]))

    items.append(make_item("item-essencia-de-mana", "Essência de Mana", "Itens Gerais", "Alquímicos - Preparados", "Alquímico de Mana", "T$ 50", None, None, None, None, None, None, 0.5, book, 160, 
        "Um líquido azul reluzente que restaura as energias místicas do corpo. Beber recupera 1d4+1 pontos de mana.", 
        ["mana", "pm", "alquimia", "recuperação"]))

    items.append(make_item("item-fogo-alquimico", "Fogo Alquímico", "Itens Gerais", "Alquímicos - Preparados", "Alquímico de Combate", "T$ 10", "1d6", "-", "Fogo", "Curto", None, None, 0.5, book, 160, 
        "Uma substância volátil que entra em ignição em contato com o ar. Causa 1d6 de dano de fogo e deixa o alvo em chamas (1d6 por rodada, Reflexos CD 15 apaga).", 
        ["fogo", "chamas", "alquimia", "arremesso"]))

    items.append(make_item("item-po-do-desaparecimento", "Pó do Desaparecimento", "Itens Gerais", "Alquímicos - Preparados", "Alquímico de Furtividade", "T$ 100", None, None, None, None, None, None, 0.5, book, 160, 
        "Jogar este pó sobre si como uma ação padrão deixa você invisível por 1d4 rodadas (como na magia Invisibilidade).", 
        ["invisibilidade", "furtividade", "alquimia"]))

    # Alquímicos - Catalisadores
    catalisadores_jda = [
        ("item-baga-de-fogo", "Baga-de-fogo", "T$ 30", "Gera calor intenso ao ser triturada. Aumenta dano de fogo em +1 por dado."),
        ("item-dente-de-dragao", "Dente-de-dragão", "T$ 45", "Dente fóssil de réptil dracônico. Concede +1 na CD de magias de dano."),
        ("item-essencia-abissal", "Essência abissal", "T$ 150", "Óleo extraído de criaturas extraplanares. Converte o dano de magias para trevas."),
        ("item-liquen-lilas", "Líquen lilás", "T$ 30", "Fungo bioluminescente das profundezas. Aumenta a duração de magias de luz em uma cena."),
        ("item-musgo-purpura", "Musgo púrpura", "T$ 45", "Musgo raro que potencializa venenos e efeitos necróticos."),
        ("item-ossos-de-monstro", "Ossos de monstro", "T$ 45", "Ossos triturados de bestas temíveis. Concede +2 no dano de magias de impacto."),
        ("item-po-de-cristal", "Pó de cristal", "T$ 30", "Pó finíssimo de quartzo. Permite que magias de área tenham seu raio aumentado em +1,5m."),
        ("item-po-de-giz", "Pó de giz", "T$ 30", "Giz purificado com sais minerais. Aumenta a duração de magias de proteção."),
        ("item-ramo-verdejante", "Ramo verdejante", "T$ 45", "Ramo florido colhido sob luar de Allihanna. Magias de cura curam +1 ponto por dado."),
        ("item-saco-de-sal", "Saco de sal", "T$ 45", "Sal bento extraído de minas sagradas. Afasta espíritos e protege contra magias profanas."),
        ("item-seixo-de-ambar", "Seixo de âmbar", "T$ 30", "Resina fóssil carregada com energia estática. Concede +1 no dano de eletricidade."),
        ("item-terra-de-cemiterio", "Terra de cemitério", "T$ 30", "Solo profano de tumbas esquecidas. Concede +1 PV temporário por criatura afetada por magia de Necromancia.")
    ]
    for cid, cname, cprice, cdesc in catalisadores_jda:
        items.append(make_item(cid, cname, "Itens Gerais", "Alquímicos - Catalisadores", "Catalisador Alquímico", cprice, None, None, None, None, None, None, 0.5, book, 160, cdesc, ["catalisador", "alquimia", "magia"]))

    # Alquímicos - Venenos
    venenos_jda = [
        ("item-beladona", "Beladona", "T$ 1.500", "Extremamente letal. Ingestão: Fortitude CD 25, dano 6d12 de veneno e paralisia."),
        ("item-bruma-sonolenta", "Bruma sonolenta", "T$ 150", "Gás inodoro. Inalação: Fortitude CD 15, deixa o alvo inconsciente por 1d4 horas."),
        ("item-cicuta", "Cicuta", "T$ 60", "Extrato vegetal comum. Ingestão: Fortitude CD 15, dano 2d6 de veneno e enfraquecimento."),
        ("item-essencia-de-sombra", "Essência de sombra", "T$ 100", "Líquido escuro como piche. Contato: Fortitude CD 18, impõe -2 em Força e Destreza."),
        ("item-nevoa-toxica", "Névoa tóxica", "T$ 30", "Pó volátil. Inalação: Fortitude CD 12, deixa a vítima enjoada por 1d4 rodadas."),
        ("item-peconha-comum", "Peçonha comum", "T$ 15", "Veneno de víboras e escorpiões pequenos. Ferimento: Fortitude CD 12, dano 1d6 de veneno."),
        ("item-peconha-concentrada", "Peçonha concentrada", "T$ 90", "Dose refinada e pura de peçonha. Ferimento: Fortitude CD 15, dano 2d8 de veneno."),
        ("item-peconha-potente", "Peçonha potente", "T$ 600", "Extrato de serpentes gigantes e monstros peçonhentos. Ferimento: Fortitude CD 20, dano 4d10 de veneno."),
        ("item-po-de-lich", "Pó de lich", "T$ 3.000", "Cinzas de cadáveres reanimados. Contato/Inalação: Fortitude CD 30, dano 10d10 de trevas."),
        ("item-riso-de-nimb", "Riso de Nimb", "T$ 150", "Extrato de fungos alucinógenos. Ingestão: Fortitude CD 15, deixa a vítima confusa por 1d6 rodadas.")
    ]
    for vid, vname, vprice, vdesc in venenos_jda:
        items.append(make_item(vid, vname, "Itens Gerais", "Alquímicos - Venenos", "Veneno", vprice, None, None, "Veneno", None, None, None, 0.5, book, 160, vdesc, ["veneno", "toxina", "alquimia"]))

    # Alimentação
    alimentos_jda = [
        ("item-batata-valkariana", "Batata valkariana", "T$ 2", "Batata assada com ervas e queijo típico de Valkaria. Fornece +1 em testes de Fortitude por uma cena."),
        ("item-gorad-quente", "Gorad quente", "T$ 18", "Bebida achocolatada e encorpada de origem anã que aquece o espírito e restaura +1 PM durante o descanso."),
        ("item-macarrao-de-yuvalin", "Macarrão de Yuvalin", "T$ 6", "Massa densa e calórica consumida pelos mineiros de Yuvalin. Fornece +1 em rolagens de dano por uma cena."),
        ("item-prato-do-aventureiro", "Prato do aventureiro", "T$ 1", "Prato simples com arroz, feijão ou lentilha, toucinho e legumes cozidos."),
        ("item-racao-de-viagem-por-dia", "Ração de viagem (por dia)", "T$ 0,5", "Carne seca, queijo duro, frutas desidratadas e biscoitos próprios para longas expedições."),
        ("item-refeicao-comum", "Refeição comum", "T$ 0,3", "Pão rústico, caldo ralo e pedaço de queijo em tavernas simples de vilarejos."),
        ("item-sopa-de-peixe", "Sopa de peixe", "T$ 1", "Caldo quente de peixes da costa com ervas e raízes marítimas.")
    ]
    for aid, aname, aprice, adesc in alimentos_jda:
        items.append(make_item(aid, aname, "Itens Gerais", "Alimentação", "Comida", aprice, None, None, None, None, None, None, 0.5, book, 161, adesc, ["alimentação", "comida", "taverna"]))

    # Animais & Montarias
    animais_jda = [
        ("item-alforje", "Alforje", "T$ 30", 0, "Bolsas de couro acopladas à sela que aumentam a carga da montaria em +5 espaços."),
        ("item-cao-de-caca", "Cão de caça", "T$ 150", 0, "Cão treinado para rastrear presas e alertar sobre perigos no acampamento (parceiro ajudante em Percepção e Sobrevivência)."),
        ("item-cavalo", "Cavalo", "T$ 75", 0, "Montaria robusta e dócil para viagens terrestres (deslocamento 12m)."),
        ("item-cavalo-de-guerra", "Cavalo de guerra", "T$ 400", 0, "Cavalo forte treinado para combate com armaduras e investidas militares (parceiro montaria veterano)."),
        ("item-estabulo-por-dia", "Estábulo (por dia)", "T$ 0,1", 0, "Acomodação, água limpa e feno para um animal em uma estalagem ou feira."),
        ("item-ponei", "Pônei", "T$ 5", 0, "Animal de montaria e carga ideal para personagens Pequenos como hynne e goblins."),
        ("item-ponei-de-guerra", "Pônei de guerra", "T$ 30", 0, "Pônei treinado para guerreiros hynne e anões montados."),
        ("item-trobo", "Trobo", "T$ 60", 0, "Grande ave corredora nativa do Reinado, rústica e adaptável para tração e montaria.")
    ]
    for anid, anname, anprice, anspace, andesc in animais_jda:
        items.append(make_item(anid, anname, "Itens Gerais", "Animais", "Montaria e Acessório", anprice, None, None, None, None, None, None, anspace, book, 162, andesc, ["animais", "montaria", "viagem"]))

    # Veículos
    veiculos_jda = [
        ("item-balao-goblin", "Balão goblin", "T$ 200", 0, "Engenhoca voadora instável operada por ar quente e hélices movidas a manivela."),
        ("item-carroca", "Carroça", "T$ 150", 0, "Veículo rústico de duas rodas puxado por um ou dois animais de tração."),
        ("item-carruagem", "Carruagem", "T$ 500", 0, "Veículo de quatro rodas fechado e acolchoado com molas de aço para nobres e personalidades."),
        ("item-canoa", "Canoa", "T$ 70", 0, "Embarcação leve de madeira para navegação em rios calmos e lagos."),
        ("item-veleiro", "Veleiro", "T$ 10.000", 0, "Grande navio de madeira com mastros e velas para singrar oceanos e mares abertos.")
    ]
    for vid, vname, vprice, vspace, vdesc in veiculos_jda:
        items.append(make_item(vid, vname, "Itens Gerais", "Veículos", "Veículo", vprice, None, None, None, None, None, None, vspace, book, 162, vdesc, ["veículos", "transporte", "viagem"]))

    # Serviços
    servicos_jda = [
        ("servico-estadia-comum", "Estadia Comum", "T$ 0,5", "Quarto coletivo em estalagem com colchão de palha e cobertor rústico."),
        ("servico-estadia-confortavel", "Estadia Confortável", "T$ 4", "Quarto individual em estalagem conceituada, com cama macia, banho e café."),
        ("servico-estadia-luxuosa", "Estadia Luxuosa", "T$ 20", "Suíte em hotel nobre com criados particulares, banho perfumado e refeições gourmet."),
        ("servico-conducao-terrestre", "Condução Terrestre", "T$ 0,5 por km", "Passagem de diligência ou comboio de carroças em estradas pavimentadas."),
        ("servico-conducao-maritima", "Condução Marítima", "T$ 0,1 por km", "Passagem de convés em navios mercantes e veleiros de cabotagem."),
        ("servico-conducao-aerea", "Condução Aérea", "T$ 10 por km", "Voo fretado em balões goblins ou criaturas aladas domesticadas."),
        ("servico-curandeiro", "Curandeiro", "T$ 5", "Tratamento de ferimentos e doenças comuns com ervas e conhecimentos médicos."),
        ("servico-magia-1-circulo", "Serviço de Magia (1º Círculo)", "T$ 10", "Contratação de um arcanista ou clérigo para conjurar uma magia de 1º círculo."),
        ("servico-magia-2-circulo", "Serviço de Magia (2º Círculo)", "T$ 90", "Contratação de conjurador para lançar uma magia de 2º círculo em benefício do contratante."),
        ("servico-magia-3-circulo", "Serviço de Magia (3º Círculo)", "T$ 360", "Contratação de poderoso conjurador para realizar um feitiço de 3º círculo."),
        ("servico-mensageiro", "Mensageiro", "T$ 0,5 por km", "Envio expresso de cartas e encomendas lacradas através de estafetas e pombos-correio.")
    ]
    for sid, sname, sprice, sdesc in servicos_jda:
        items.append(make_item(sid, sname, "Itens Gerais", "Serviços", "Serviço", sprice, None, None, None, None, None, None, 0, book, 162, sdesc, ["serviço", "estadia", "condução", "magia"]))

    # =========================================================================
    # 5. MELHORIAS & MATERIAIS ESPECIAIS (Tabelas 3-8 & 3-9, Páginas 165-172)
    # =========================================================================

    # Melhorias para Armas
    items.append(make_item("melhoria-certeira", "Certeira", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "A arma é forjada com balanceamento perfeito para cortes e estocadas. Fornece +1 nos testes de ataque.", 
        ["melhoria", "arma", "ataque"]))

    items.append(make_item("melhoria-pungente", "Pungente", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "Temperada diversas vezes para adquirir o fio ou equilíbrio perfeito, a arma fornece +2 nos testes de ataque. Pré-requisito: Certeira.", 
        ["melhoria", "arma", "ataque +2"]))

    items.append(make_item("melhoria-cruel", "Cruel", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Lâmina serrilhada ou pontas brutais aumentam o poder lesivo da arma. Concede +1 nas rolagens de dano.", 
        ["melhoria", "arma", "dano"]))

    items.append(make_item("melhoria-atroz", "Atroz", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "A arma é excepcionalmente cruel e devastadora ao dilacerar carne e osso. Fornece +2 nas rolagens de dano. Pré-requisito: Cruel.", 
        ["melhoria", "arma", "dano +2"]))

    items.append(make_item("melhoria-equilibrada", "Equilibrada", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Forjada com centro de gravidade impecável, facilitando fintas e manobras. Fornece +2 em testes de manobras (desarmar, quebrar, derrubar, empurrar).", 
        ["melhoria", "arma", "manobras"]))

    items.append(make_item("melhoria-harmonizada-arma", "Harmonizada (Arma)", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "Banhada em óleos alquímicos que sintonizam a lâmina à aura de combate do usuário. Escolha uma habilidade ativada com ataque/agredir que custe PM: seu custo é reduzido em -1 PM. Pré-requisito: outra melhoria.", 
        ["melhoria", "arma", "redução de pm"]))

    items.append(make_item("melhoria-injecao-alquimica", "Injeção Alquímica", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Um compartimento interno na arma libera um preparado alquímico ou água benta automaticamente no alvo em caso de acerto (capacidade para 2 doses).", 
        ["melhoria", "arma", "alquimia", "injeção"]))

    items.append(make_item("melhoria-macica", "Maciça", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Feita com material de altíssima densidade. O multiplicador de crítico da arma aumenta em +1 (ex: x2 vira x3). Não pode ser maciça e precisa.", 
        ["melhoria", "arma", "crítico"]))

    items.append(make_item("melhoria-mira-telescopica", "Mira Telescópica", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Lentes ajustadas sobre o topo de armas de disparo (exceto fundas). Aumenta o alcance da arma em uma categoria e o alcance de Ataque Furtivo para médio.", 
        ["melhoria", "disparo", "alcance", "ataque furtivo"]))

    items.append(make_item("melhoria-precisa", "Precisa", "Itens Superiores", "Melhorias", "Melhoria de Arma", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "O fio e a geometria do gume foram trabalhados para encontrar brechas mortais na defesa. A margem de ameaça aumenta em +1 (ex: 19 vira 18). Não pode ser precisa e maciça.", 
        ["melhoria", "arma", "margem de ameaça"]))

    # Melhorias para Armaduras e Escudos
    items.append(make_item("melhoria-ajustada", "Ajustada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Ajustada ergonomicamente para permitir mobilidade e agilidade ao usuário. Reduz a penalidade de armadura do item em -1.", 
        ["melhoria", "armadura", "escudo", "penalidade"]))

    items.append(make_item("melhoria-sob-medida", "Sob Medida", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "Forjada e lapidada meticulosamente para as medidas exatas de um guerreiro específico. Reduz a penalidade de armadura em -2 para esse usuário. Pré-requisito: Ajustada.", 
        ["melhoria", "armadura", "escudo", "penalidade -2"]))

    items.append(make_item("melhoria-delicada", "Delicada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Leve e com articulações finas, permite aplicar 1 ponto adicional da sua Destreza no bônus de Defesa da armadura.", 
        ["melhoria", "armadura", "destreza"]))

    items.append(make_item("melhoria-espinhosa-armadura", "Espinhosa (Armadura)", "Itens Superiores", "Melhorias", "Melhoria de Armadura", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Coberta de cravos pontiagudos de aço. Ao agarrar ou ser agarrado por uma criatura, causa dano de perfuração igual à sua Força na hora e a cada rodada mantida.", 
        ["melhoria", "armadura", "agarrar", "espinhos"]))

    items.append(make_item("melhoria-espinhoso-escudo", "Espinhoso (Escudo)", "Itens Superiores", "Melhorias", "Melhoria de Escudo", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "O escudo possui lâminas ou um espigão central reforçado. Aumenta o dano de um ataque com escudo em um passo.", 
        ["melhoria", "escudo", "dano de ataque"]))

    items.append(make_item("melhoria-polida", "Polida", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Metal com acabamento espelhado reluzente. Em ambientes iluminados, concede +5 na Defesa na primeira rodada de combate ofuscando os oponentes.", 
        ["melhoria", "armadura", "escudo", "ofuscar", "defesa"]))

    items.append(make_item("melhoria-reforcada", "Reforçada", "Itens Superiores", "Melhorias", "Melhoria de Armadura/Escudo", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Camadas extras de aço e reforços estruturais. O bônus na Defesa aumenta em +1, mas a penalidade de armadura também aumenta em +1.", 
        ["melhoria", "armadura", "escudo", "defesa +1"]))

    items.append(make_item("melhoria-selada", "Selada", "Itens Superiores", "Melhorias", "Melhoria de Armadura", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "As juntas e placas de metal são blindadas e herméticas. Fornece +1 em todos os testes de resistência (apenas em armaduras pesadas).", 
        ["melhoria", "armadura pesada", "resistência"]))

    # Melhorias para Esotéricos
    items.append(make_item("melhoria-canalizador", "Canalizador", "Itens Superiores", "Melhorias", "Melhoria de Esotérico", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Gemas especiais no foco místico aumentam a vazão de energia. O limite de PM que você pode gastar em magias aumenta em +1.", 
        ["melhoria", "esotérico", "limite de pm"]))

    items.append(make_item("melhoria-energetico", "Energético", "Itens Superiores", "Melhorias", "Melhoria de Esotérico", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Catalisadores alquímicos no esotérico potencializam energias mágicas. Suas magias que causam dano causam +1d6 de dano adicional do mesmo tipo.", 
        ["melhoria", "esotérico", "dano mágico"]))

    items.append(make_item("melhoria-harmonizado-esoterico", "Harmonizado (Esotérico)", "Itens Superiores", "Melhorias", "Melhoria de Esotérico", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "Sintonizado com os padrões mentais de uma magia escolhida. O custo dessa magia diminui em -1 PM (mínimo 1 PM).", 
        ["melhoria", "esotérico", "redução de pm"]))

    items.append(make_item("melhoria-poderoso", "Poderoso", "Itens Superiores", "Melhorias", "Melhoria de Esotérico", "+T$ 3.000", None, None, None, None, None, None, None, book, 165, 
        "Gravações arcanas de alta complexidade. A CD para resistir a todas as suas magias aumenta em +1.", 
        ["melhoria", "esotérico", "cd de magias"]))

    items.append(make_item("melhoria-vigilante", "Vigilante", "Itens Superiores", "Melhorias", "Melhoria de Esotérico", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "O item usa parte da mana passiva do conjurador para projetar um campo defletor invisível. Fornece +2 na Defesa.", 
        ["melhoria", "esotérico", "defesa"]))

    # Melhorias Gerais / Ferramentas / Vestuário
    items.append(make_item("melhoria-aprimorado", "Aprimorado", "Itens Superiores", "Melhorias", "Melhoria de Ferramenta/Vestuário", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Confeccionado com maestria de materiais nobres. Fornece +1 em testes de perícia com o item.", 
        ["melhoria", "perícia", "ferramenta", "vestuário"]))

    items.append(make_item("melhoria-banhado-a-ouro", "Banhado a Ouro", "Itens Superiores", "Melhorias", "Melhoria Geral", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Revestido com folheados brilhantes de ouro puro. Fornece +2 em testes de Diplomacia.", 
        ["melhoria", "diplomacia", "ouro", "luxo"]))

    items.append(make_item("melhoria-cravejado-de-gemas", "Cravejado de Gemas", "Itens Superiores", "Melhorias", "Melhoria Geral", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Incrustado com pedras preciosas fascinantes. Fornece +2 em testes de Enganação.", 
        ["melhoria", "enganação", "gemas", "luxo"]))

    items.append(make_item("melhoria-discreto", "Discreto", "Itens Superiores", "Melhorias", "Melhoria Geral", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Projetado de maneira compacta e dissimulada. O item ocupa -1 espaço (mínimo 0) e concede +5 em testes de Ladinagem para ser ocultado.", 
        ["melhoria", "espaço reduzido", "ladinagem", "ocultar"]))

    items.append(make_item("melhoria-macabro", "Macabro", "Itens Superiores", "Melhorias", "Melhoria Geral", "+T$ 300", None, None, None, None, None, None, None, book, 165, 
        "Decorado com crânios, ossos entalhados e sangue seco. Fornece +2 em Intimidação, mas impõe -2 em Diplomacia.", 
        ["melhoria", "intimidação", "medo"]))

    # Materiais Especiais JdA
    items.append(make_item("material-aco-rubi", "Aço-Rubi", "Itens Superiores", "Materiais Especiais", "Material Especial", "Ver Tabela 3-9", None, None, None, None, None, None, None, book, 166, 
        "Vidro avermelhado duro como aço minerado das profundezas da Tormenta por anões. Arma: ignora 10 pontos de RD e imunidade a crítico de lefeu. Armadura/Escudo: chance de ignorar dano extra de acerto crítico e ataque furtivo (leves/escudos 25%, pesadas 50%). Esotérico: magias que causam dano ignoram 10 de RD e imunidades de lefeu.", 
        ["material especial", "aço-rubi", "tormenta", "rd"]))

    items.append(make_item("material-adamante", "Adamante", "Itens Superiores", "Materiais Especiais", "Material Especial", "Ver Tabela 3-9", None, None, None, None, None, None, None, book, 166, 
        "Metal meteórico escuro, fosco e hiperdenso. Arma: aumenta o dano em um passo. Armadura/Escudo: fornece redução de dano (leves/escudos RD 2; pesadas RD 5). Esotérico: ao lançar magia de dano, pode gastar +1 PM para rerrolar resultados 1 de dano.", 
        ["material especial", "adamante", "dano", "rd"]))

    items.append(make_item("material-gelo-eterno", "Gelo Eterno", "Itens Superiores", "Materiais Especiais", "Material Especial", "Ver Tabela 3-9", None, None, None, None, None, None, None, book, 166, 
        "Gelo mineral extraído das Montanhas Uivantes que jamais derrete. Arma: causa +2 de dano por frio. Armadura/Escudo: redução de fogo (leves/escudos 5; pesadas 10). Esotérico: ao lançar magia de frio, pode rerrolar resultados 1 de dano.", 
        ["material especial", "gelo eterno", "frio", "fogo"]))

    items.append(make_item("material-madeira-tollon", "Madeira Tollon", "Itens Superiores", "Materiais Especiais", "Material Especial", "Ver Tabela 3-9", None, None, None, None, None, None, None, book, 166, 
        "Madeira negra nobre e mágica de Tollon (apenas armas de madeira, escudos leves e esotéricos). Arma: conta como mágica e reduz custo de habilidades ativadas com ataque/agredir em -1 PM. Escudo e Esotérico: fornece Resistência a Magia +2.", 
        ["material especial", "madeira tollon", "mágico", "resistência a magia"]))

    items.append(make_item("material-materia-vermelha", "Matéria Vermelha", "Itens Superiores", "Materiais Especiais", "Material Especial", "Ver Tabela 3-9", None, None, None, None, None, None, None, book, 166, 
        "Partes orgânicas e carapaças lefeu. Impõe -2 em Carisma (exceto Intimidação). Arma: causa +1d6 de dano extra, mas o usuário perde 1 PV por acerto (lefou/lefeu imunes). Armadura/Escudo: concede chance de falha em ataques contra o usuário (10% leves/escudos, 25% pesadas). Esotérico: você e inimigos em alcance curto sofrem -2 em testes de resistência contra magias.", 
        ["material especial", "matéria vermelha", "tormenta", "lefou"]))

    items.append(make_item("material-mitral", "Mitral", "Itens Superiores", "Materiais Especiais", "Material Especial", "Ver Tabela 3-9", None, None, None, None, None, None, None, book, 166, 
        "Metal prateado ultra-leve e brilhante. O item ocupa -1 espaço (mínimo 1). Arma: margem de ameaça aumenta em +1. Armadura/Escudo: diminui penalidade de armadura em -2; armaduras pesadas de mitral permitem aplicar até +2 da Destreza na Defesa. Esotérico: permite pagar +2 PM para aumentar a CD da magia em +2.", 
        ["material especial", "mitral", "leve", "margem de ameaça"]))

    return items
