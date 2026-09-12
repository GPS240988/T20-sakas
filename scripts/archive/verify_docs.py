import pymupdf
import re
import json

def get_page_text(doc, page_num):
    # page_num is 1-indexed PDF page
    return doc[page_num - 1].get_text()

jda_doc = pymupdf.open("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf")
hda_doc = pymupdf.open("T20-Herois-de-Arton-v1-1_compressed.pdf")
ameacas_doc = pymupdf.open("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf")

print("JDA total pages:", len(jda_doc))
print("HDA total pages:", len(hda_doc))
print("Ameacas total pages:", len(ameacas_doc))
