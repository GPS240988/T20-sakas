import pypdf

def extract_text_range(pdf_path, pages_dict):
    reader = pypdf.PdfReader(pdf_path)
    for title, page_nums in pages_dict.items():
        print(f"\n{'='*25} {title} {'='*25}")
        for p in page_nums:
            print(f"--- PDF Page {p} ---")
            txt = reader.pages[p].extract_text()
            print(txt)

print("=== 1. JDA TABLES ===")
extract_text_range("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf", {
    "Tabela 3-3 Armas": [149, 150],
    "Tabela 3-4 Munições": [156],
    "Tabela 3-5 Armaduras & Escudos": [158],
    "Tabela 3-6 Itens Gerais": [161, 162],
    "Tabela 3-8 Melhorias & 3-9 Materiais": [170, 171, 172]
})

print("\n=== 2. HDA TABLES ===")
extract_text_range("T20-Herois-de-Arton-v1-1_compressed.pdf", {
    "HDA Tabela 3-1 Armas": [219, 220],
    "HDA Tabela 3-3 Armaduras & Escudos": [225],
    "HDA Tabela 3-4 Itens Gerais": [229, 230],
    "HDA Tabela 3-5 Novas Melhorias": [241, 242]
})

print("\n=== 3. AMEACAS TABLES ===")
extract_text_range("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf", {
    "Ameacas Tabela 3-1 Armas & 3-2 Armaduras": [395, 396],
    "Ameacas Tabela 3-3 Itens Gerais": [399, 400],
    "Ameacas Tabela 3-4 Materiais": [401]
})
