import pypdf
import re

def search_pdf(pdf_path, terms):
    r = pypdf.PdfReader(pdf_path)
    print(f"\n==========================================")
    print(f"BUSCANDO EM: {pdf_path}")
    print(f"Total de Páginas no PDF: {len(r.pages)}")
    print(f"==========================================")
    
    for idx, page in enumerate(r.pages):
        text = page.extract_text()
        pdf_page = idx + 1
        for term in terms:
            if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
                # Tenta capturar o número de página impresso no texto
                # Em T20 o número da página costuma aparecer em linhas isoladas como '142', '146', etc.
                p_matches = re.findall(r'(?:^|\n)\s*(\d{1,3})\s*(?:\n|$)', text)
                printed_page = p_matches[-1] if p_matches else f"~{pdf_page}"
                first_line = text.strip().split('\n')[0] if text.strip() else ""
                print(f"[PDF Pág {pdf_page:03d} | Livro Pág {printed_page}] Termo: '{term}' -> {first_line[:60]}")

# 1. Jogo do Ano
search_pdf("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf", [
    "Tabela 3-3", "Tabela 3-4", "Tabela 3-5", "Tabela 3-6", "Tabela 3-8", "Capítulo 3", "Armas Simples", "Munições", "Armaduras", "Itens Gerais", "Melhorias"
])

# 2. Heróis de Arton
search_pdf("T20-Herois-de-Arton-v1-1_compressed.pdf", [
    "Tabela 3-1", "Tabela 3-2", "Tabela 3-3", "Tabela 3-4", "Tabela 3-5", "Capangas", "Veículos", "Arsenal dos Heróis"
])

# 3. Ameaças de Arton
search_pdf("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf", [
    "Bazar Monstruoso", "Tabela 3-1", "Tabela 3-2", "Tabela 3-3", "Tabela 3-4", "Tabela 3-5"
])
