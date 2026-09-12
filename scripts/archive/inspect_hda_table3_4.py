def inspect_hda_table3_4():
    with open('scripts/hda_tables_utf8.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    p = txt.find("Tabela 3-4: Itens Gerais")
    p_end = txt.find("Tabela 3-5: Novas Melhorias")
    print(txt[p:p_end])

inspect_hda_table3_4()
