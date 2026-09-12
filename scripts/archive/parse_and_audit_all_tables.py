import re
import json

def audit_file(filename, book_name):
    print(f"\n{'='*20} AUDITING {book_name} ({filename}) {'='*20}")
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    pages = text.split("="*30)
    print(f"Total pages in dump: {len(pages)}")
    
    # Find all table markers
    for p in pages:
        if "PDF PAGE" in p:
            header = p.split('\n')[0].strip()
            for line in p.split('\n'):
                if "Tabela " in line or "TABELA " in line:
                    print(f"{header} -> {line.strip()}")

audit_file("scripts/jda_equip_full_dump.txt", "Tormenta20 JdA")
audit_file("scripts/hda_equip_full_dump.txt", "Heróis de Arton")
audit_file("scripts/ameacas_equip_full_dump.txt", "Ameaças de Arton")
