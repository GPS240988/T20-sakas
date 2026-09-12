import json
import re

def inspect_jda():
    with open('scripts/jda_tables_utf8.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    print("===================== JDA TABELA 3-6 (ITENS GERAIS) =====================")
    p = txt.find("Tabela 3-6: Itens Gerais")
    p_end = txt.find("Tabela 3-8: Melhorias")
    print(txt[p:p_end])

inspect_jda()
