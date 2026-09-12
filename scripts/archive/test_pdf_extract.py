from pypdf import PdfReader
import sys

reader = PdfReader("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf")
print("Total pages in JDA:", len(reader.pages))

# In JDA, book page 142 is PDF page 148 (index 147)
# Let's inspect pages 146 to 170 (PDF index 145 to 170)
for pno in range(147, 165):
    text = reader.pages[pno].extract_text()
    first_lines = text.split("\n")[:5]
    print(f"--- PDF Page {pno+1} (Book Pág ~{pno+1-6}) ---")
    print("\n".join(first_lines))
