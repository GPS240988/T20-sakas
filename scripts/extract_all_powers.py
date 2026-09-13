# -*- coding: utf-8 -*-
"""
Extractor canónico del grupo PODERES para Tormenta20 (T20 Sakas).

Lee el texto verbatim de los PDFs de los libros y consolida TODOS los poderes
del grupo "Poder" con el texto EXACTO tal como aparece en el libro (sin
alteración ni interpretación), siguiendo el patrón de extracción de magias.

Fuentes (se excluyen las Distinções, formato narrativo aparte):
  - Tormenta20 - Jogo do Ano (v1.3): Combate, Destino, Magia, Concedidos, da Tormenta
  - T20 Heróis de Arton (v1.1):      Novos Poderes (Combate/Destino/Magia/Tormenta),
                                     Raça y Grupo
"""
import json
import os
import re

DUMP_JDA = "scripts/tmp_dump/jda_poderes_130_143.txt"
DUMP_HEROIS = "scripts/tmp_dump/herois_poderes_80_97.txt"
OUT = "data/categories/poderes.json"

# ---------------------------------------------------------------------------
# Sección determinada por PÁGINA IMPRESA (por el libro entrelaza descripciones
# con páginas-tabla de resumen; "TABLE"/"SKIP" se descartan).
# ---------------------------------------------------------------------------
PAGE_SECTIONS = {
    "JDA": {
        130: "Combate", 131: "Combate", 132: "TABLE", 133: "TABLE",
        134: "Combate", 135: "Combate", 136: "Destino", 137: "Destino",
        138: "Concedidos", 139: "Concedidos", 140: "Concedidos",
        141: "Concedidos", 142: "Tormenta", 143: "Tormenta",
    },
    "HEROIS": {
        80: "Combate", 81: "Combate", 82: "Destino", 83: "TABLE",
        84: "Magia", 85: "Tormenta", 86: "Raça", 87: "TABLE",
        88: "Raça", 89: "Raça", 90: "Raça", 91: "Raça", 92: "Raça",
        93: "Raça", 94: "Grupo", 95: "Grupo", 96: "Grupo", 97: "Grupo",
    },
}

SECTION_NAME_MAP = {
    "Combate": ("Poderes de Combate", "Combate", "none"),
    "Destino": ("Poderes de Destino", "Destino", "none"),
    "Magia": ("Poderes de Magia", "Magia", "none"),
    "Concedidos": ("Poderes Concedidos", "Concedido", "deidad"),
    "Tormenta": ("Poderes da Tormenta", "Tormenta", "none"),
    "Aprimoramiento": ("Poderes de Magia", "Magia", "none"),
    "Raça": ("Poderes de Raça", "Raça", "raza"),
    "Grupo": ("Poderes de Grupo", "Grupo", "none"),
}

SECTION_TITLE_MAP = {
    "poderes de combate": "Combate",
    "poderes de destino": "Destino",
    "poderes de magia": "Magia",
    "poderes concedidos": "Concedidos",
    "poderes da tormenta": "Tormenta",
    "poderes de aprimoramento": "Aprimoramiento",
    "poderes de raça": "Raça",
    "poderes de raza": "Raça",
    "podéres de grupo": "Grupo",
    "poderes de grupo": "Grupo",
}


def _norm_key(s):
    s = s.lower()
    for _a, _b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('à','a'),
                   ('è','e'),('ç','c'),('ã','a'),('õ','o'),('ñ','n')]:
        s = s.replace(_a, _b)
    return " ".join(s.split())


SECTION_TITLE_NORM = {_norm_key(k): v for k, v in SECTION_TITLE_MAP.items()}

BOOK_META = {
    "JDA": {"book": "Tormenta20 - Jogo do Ano", "version": "v1.3"},
    "HEROIS": {"book": "Heróis de Arton", "version": "v1.1"},
}


def looks_like_table_header(line):
    s = line.strip()
    if not s or s.endswith('.'):
        return False
    low = _norm_key(s)
    return (low.startswith("tabela ")
            or low in ("poder pre-requisitos", "poder prerequisitos")
            or low.startswith("poder pre-requisitos"))
# ---------------------------------------------------------------------------
# Heurística de detección de NOMBRES de poder
# ---------------------------------------------------------------------------
_SENTENCE_LEADS = (
    "quando ", "você ", "uma ", "se vle ", "escolha ", "todos los ", "todos os ",
    "sempre que ", "no final ", "cada ", "a presença ", "se você ", "en este ",
    "os ", "as ", "ao ", "membros ", "algu s ", "contudo ", "após ", "então ",
    "toda ", "efeitos ", "para cada ", "busque ", "este ", "estes ", "como ",
    "sua ", "tu ", "seu ", "sobre ", "quando você ", "sofre ", "quando faz ",
    "capítulo ", "escolhendo poderes gerais", "grupos de poderes",
    "campeões de arton", "um inexpugn", "poder pré-requisitos", "tabela ",
    "nivel benefício", "nível benefício", "benefício cd", "poderes  de ", "87 cap", "86 cap",
    "85 cap", "89 cap", "90 cap", "92 cap", "93", "91",
)
_POWER_NAME_RE = re.compile(r"^[A-ZÁÉÍÓÚÀ-ÜÑ][A-Za-z0-9áéíóúà-ÿñü'’“”—, \-\"]*$")


def looks_like_power_name(line):
    s = line.strip()
    if not s or len(s) > 40:
        return False
    if s.endswith(('.', ':', ';', ',', '?', '!')):
        return False
    if not _POWER_NAME_RE.match(s):
        return False
    low = _norm_key(s)
    if "pre-requisito" in low:
        return False
    if re.fullmatch(r'[\d\s–—-]+', s):
        return False
    _HARD_NOISE = (
        "capítulo dois", "capítulo 1", "capítulo ", "grupos de poderes",
        "escolhendo poderes gerais", "campeões de arton", "um inexpugn",
        "poder pré-requisitos", "tabela 1", "benefício cd",
        "nivel benefício", "nível benefício",
        "perícias & poderes", "poderes gerais", "o dilema do jogador",
    )
    if s.lower().startswith(_HARD_NOISE):
        return False
    if low.startswith(_SENTENCE_LEADS) and len(s) > 25:
        return False
    words = [w for w in re.split(r'\s+', s) if w]
    if not words:
        return False
    if len(words) == 1:
        w0 = words[0].rstrip('.,')
        return bool(w0 and w0[0].isupper() and not w0.isupper() and len(w0) > 2)
    caps = sum(1 for w in words if w and w[0].isupper() and not w.isupper() and len(w) > 1)
    return caps >= 2


def split_trailing(line):
    s = line.strip()
    words = [w for w in line.split() if w]
    if not words:
        return s, ""
    trail_words = []
    i = len(words) - 1
    while i >= 0:
        bare = words[i].strip(" ,;")
        if not bare:
            i -= 1
            continue
        if bare[0].isupper() and len(bare) > 1 and bare.lower() not in ("de", "da", "do", "las", "los"):
            trail_words.insert(0, words[i])
            i -= 1
        elif trail_words and _norm_key(bare) in ("ou", "y", "o", "e", ","):
            trail_words.insert(0, words[i])
            i -= 1
        else:
            break
    if not trail_words:
        return s, ""
    name = " ".join(words[:len(words) - len(trail_words)]).strip().rstrip(",").strip()
    tail = " ".join(trail_words).strip()
    if not name:
        return s, ""
    return name, tail


# ---------------------------------------------------------------------------
# Utilidades de limpieza técnica (no alteran el texto del libro)
# ---------------------------------------------------------------------------
def join_lines(lines):
    txt = " ".join(lines)
    txt = txt.replace("\u00a0", " ")
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()


def sanitize_desc(t):
    t = t.replace('\x00', '')
    t = re.sub(r'\s+([,.;:])', r'\1', t)
    t = re.sub(r'\s+e\s*$', '', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def slugify_name(name):
    s = name.lower()
    for a, b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('à','a'),
                 ('è','e'),('ì','i'),('ò','o'),('ù','u'),('â','a'),('ê','e'),
                 ('î','i'),('ô','o'),('û','u'),('ã','a'),('õ','o'),('ñ','n'),
                 ('ç','c'),('ü','u'),('–','-'),('—','-'),('/','-'),('’',"'"),
                 ('‘',"'"),('“','"'),('”','"')]:
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9\'\- ]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    return f"poder-{s}"
# ---------------------------------------------------------------------------
# Extracción página por página
# ---------------------------------------------------------------------------
def extract(dump_path, book_key):
    with open(dump_path, "r", encoding="utf-8") as fd:
        raw = fd.read()

    pages = []
    for line in raw.split("\n"):
        pm = re.match(r'^=+ PAGE_INDEX_(\d+) \(printed (\d+)\)', line.strip())
        if pm:
            pages.append({"printed": int(pm.group(2)), "lines": []})
        elif pages:
            pages[-1]["lines"].append(line.strip())

    powers = []
    section = None
    current = None
    in_table = False
    page_map = PAGE_SECTIONS[book_key]

    def flush():
        nonlocal current
        if current and current.get("desc_lines"):
            powers.append(current)
        current = None

    for page in pages:
        printed = page["printed"]
        default_sec = page_map.get(printed)
        if default_sec in ("TABLE", "SKIP"):
            flush()
            continue
        in_table = False
        if default_sec is not None:
            section = SECTION_NAME_MAP[default_sec]

        for line in page["lines"]:
            s = line.strip()
            lowk = _norm_key(s)

            if lowk in SECTION_TITLE_NORM:
                flush()
                section = SECTION_NAME_MAP[SECTION_TITLE_NORM[lowk]]
                in_table = False
                continue
            if looks_like_table_header(line):
                in_table = True
                continue
            if in_table or not s:
                continue

            if section and looks_like_power_name(s):
                flush()
                subcat, ptype, trailer = section
                name = s
                trail = ""
                if trailer in ("deidad", "raza"):
                    _, trail = split_trailing(s)
                    if not trail:
                        trail = ""
                current = {"_section": subcat, "_type": ptype,
                           "name": name, "trail": trail,
                           "_page": page["printed"], "desc_lines": []}
                continue

            if current is not None:
                current["desc_lines"].append(s)

    flush()

    out = []
    for p in powers:
        desc = sanitize_desc(join_lines(p["desc_lines"]))
        if not desc:
            continue
        name = p["name"].rstrip(",").strip()
        if not name:
            continue
        trail = p.get("trail", "")
        trails = [t.strip().rstrip(",") for t in re.split(r'[,/]|\s+e\s+|\s+y\s+|\s+ou\s+', trail) if t.strip()]
        requirements = []
        deity = None

        req = re.search(r'Pr[ée]-?requisito[s]?\s*:\s*(.*)$', desc, re.IGNORECASE | re.MULTILINE)
        if req:
            req_text = sanitize_desc(req.group(1).strip().rstrip('.'))
            parts = [x.strip().rstrip('.').strip() for x
                     in re.split(r'[,;]|\s+e\s+|\s+y\s+|\s+ou\s+|\.', req_text) if x.strip()]
            requirements = [re.sub(r'\s+', ' ', x) for x in parts]

        type_ = p["_type"]
        if type_ == "Concedido":
            deity = "; ".join(trails) if trails else None
            if deity:
                requirements = [f"Devoto de {deity}"] + [r for r in requirements
                                                          if not r.lower().startswith("devoto")]
        elif type_ == "Raça":
            requirements = trails + requirements

        meta = BOOK_META[book_key]
        subcat = p["_section"]
        out.append({
            "id": slugify_name(name),
            "name": name,
            "category": "poder",
            "subcategory": subcat,
            "powerType": type_,
            "requirements": requirements,
            "cost": None,
            "deity": deity,
            "summary": f"{type_}. {desc[:90]}{'...' if len(desc) > 90 else ''}",
            "description": desc,
            "sources": [{
                "book": meta["book"],
                "page": p.get("_page"),
                "section": f"Poderes: {subcat}",
                "version": meta["version"]
            }],
            "tags": ["poder", name.lower(), type_.lower(), subcat.lower()] + [r.lower() for r in requirements]
        })
    return out


def main():
    all_powers = extract(DUMP_JDA, "JDA") + extract(DUMP_HEROIS, "HEROIS")
    by_id = {}
    for p in all_powers:
        pid = p["id"]
        if pid in by_id:
            for src in p["sources"]:
                if src not in by_id[pid]["sources"]:
                    by_id[pid]["sources"].append(src)
        else:
            by_id[pid] = p
    result = list(by_id.values())
    result.sort(key=lambda x: (x["subcategory"], x["name"].lower()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Total poderes consolidados: {len(result)}")
    by_sub = {}
    for p in result:
        by_sub[p["subcategory"]] = by_sub.get(p["subcategory"], 0) + 1
    for k in sorted(by_sub):
        print(f"  * {k}: {by_sub[k]}")


if __name__ == "__main__":
    main()