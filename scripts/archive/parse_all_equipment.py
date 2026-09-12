import re
import json

def clean_text(t):
    t = t.replace("\x00", "")
    # replace common encoding artifacts if any
    t = t.replace("", "")
    t = re.sub(r'\s+', ' ', t).strip()
    return t

with open("scripts/jda_equip_dump.txt", encoding="utf-8") as f:
    jda_raw = f.read()

with open("scripts/hda_equip_dump.txt", encoding="utf-8") as f:
    hda_raw = f.read()

with open("scripts/ameacas_equip_dump.txt", encoding="utf-8") as f:
    ameacas_raw = f.read()

print("JDA raw length:", len(jda_raw))
print("HDA raw length:", len(hda_raw))
print("Ameacas raw length:", len(ameacas_raw))
