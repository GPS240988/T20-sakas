# -*- coding: utf-8 -*-
import os
import shutil

archive_dir = "scripts/archive"
os.makedirs(archive_dir, exist_ok=True)

# List of active, reliable production files to KEEP in scripts/
keep_files = {
    # Core Compilers & Quality Assurance
    "compile_all_categories.py",
    "remove_version_suffixes.py",
    "inspect_descriptions_quality.py",

    # Verbatim Text Source Text Files (Official raw chapters)
    "raw_jda_equip_text.txt",
    "raw_hda_equip_text.txt",
    "raw_ameacas_equip_text.txt",

    # Equipment Canonical Builders & Verbatim Injectors
    "build_canonical_verbatim_equipments.py",
    "fix_remaining_literal_descriptions.py",
    "build_jda_equipments.py",
    "build_hda_equipments.py",
    "build_ameacas_equipments.py",
    "fix_4_weapons.py",
    "fix_ameacas_weapons.py",

    # Base Reusable Category Extractors (For Spells, Powers, Monsters, etc.)
    "extract_all_spells.py",
    "extract_all_powers.py",
    "extract_all_monsters.py",
    "extract_all_origins.py",
    "extract_t20_conditions.py",
    "extract_treasures.py",

    # This script
    "organize_scripts.py"
}

moved_count = 0
for filename in os.listdir("scripts"):
    filepath = os.path.join("scripts", filename)
    
    # Skip directories and files in keep list
    if os.path.isdir(filepath):
        continue
    
    if filename not in keep_files:
        dest_path = os.path.join(archive_dir, filename)
        shutil.move(filepath, dest_path)
        print(f"Archived: {filename}")
        moved_count += 1

print(f"\n=======================================================")
print(f"Organização concluída! {moved_count} arquivos arquivados em '{archive_dir}'.")
print(f"Total de scripts ativos e confiáveis mantidos: {len(keep_files) - 1}")
print("=======================================================\n")
