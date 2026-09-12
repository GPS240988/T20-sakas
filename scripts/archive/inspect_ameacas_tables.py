def inspect_ameacas():
    with open('scripts/ameacas_tables_utf8.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    print("===================== AMEACAS TABLES =====================")
    print(txt)

inspect_ameacas()
