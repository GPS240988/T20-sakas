import pypdf

def extract_to_file(pdf_path, pages_dict, out_file):
    reader = pypdf.PdfReader(pdf_path)
    with open(out_file, 'w', encoding='utf-8') as f:
        for title, page_nums in pages_dict.items():
            f.write(f"\n{'='*25} {title} {'='*25}\n")
            for p in page_nums:
                f.write(f"\n--- PDF Page {p} ---\n")
                txt = reader.pages[p].extract_text()
                f.write(txt or '')
                f.write("\n")

print("Extracting JDA tables...")
extract_to_file("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf", {
    "Tabela 3-3 Armas": [149, 150],
    "Tabela 3-4 Municoes": [156],
    "Tabela 3-5 Armaduras e Escudos": [158],
    "Tabela 3-6 Itens Gerais": [161, 162],
    "Tabela 3-8 Melhorias e 3-9 Materiais": [170, 171, 172]
}, "scripts/jda_tables_utf8.txt")

print("Extracting HDA tables...")
extract_to_file("T20-Herois-de-Arton-v1-1_compressed.pdf", {
    "HDA Tabela 3-1 Armas": [219, 220],
    "HDA Tabela 3-3 Armaduras e Escudos": [225],
    "HDA Tabela 3-4 Itens Gerais": [229, 230],
    "HDA Tabela 3-5 Novas Melhorias": [241, 242]
}, "scripts/hda_tables_utf8.txt")

print("Extracting Ameacas tables...")
extract_to_file("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf", {
    "Ameacas Tabela 3-1 Armas e 3-2 Armaduras": [395, 396],
    "Ameacas Tabela 3-3 Itens Gerais": [399, 400],
    "Ameacas Tabela 3-4 Materiais": [401]
}, "scripts/ameacas_tables_utf8.txt")

print("All tables extracted successfully in UTF-8!")
