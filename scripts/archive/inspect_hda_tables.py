import re

def inspect_hda():
    with open('scripts/hda_tables_utf8.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    print("===================== HDA TABLES =====================")
    print(txt)

inspect_hda()
