#!/usr/bin/env python3
"""
Corrections finales USPN_S2.
"""
import os
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

# Corrections finales
EXACT_REPLACEMENTS = [
    # Nutrition métabolisme acides aminés
    ("1. étabolisme des acides aminés", "Métabolisme des acides aminés"),
    ("1 étabolisme des acides aminés", "Métabolisme des acides aminés"),
    ("2 étabolisme des acides aminés", "Métabolisme des acides aminés (suite)"),
    
    # Double s
    ("énergétiquess", "énergétiques"),
    
    # h2 headers corrections
    ("SOCLE - 1. étabolisme des acides aminés", "SOCLE - Métabolisme des acides aminés"),
    ("SOCLE - 1 étabolisme des acides aminés", "SOCLE - Métabolisme des acides aminés"),
    ("SOCLE - 2 étabolisme des acides aminés", "SOCLE - Métabolisme des acides aminés (suite)"),
    ("SOCLE - 1 e tabolisme des acides amine s", "SOCLE - Métabolisme des acides aminés"),
    ("SOCLE - 2 e tabolisme des acides amine s", "SOCLE - Métabolisme des acides aminés (suite)"),
]

def normalize_nfd(s):
    return unicodedata.normalize('NFD', s)

def normalize_nfc(s):
    return unicodedata.normalize('NFC', s)

def fix_all_files():
    fixed_count = 0
    
    for root_dir, dirs, files in os.walk(USPN_S2_ROOT):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = Path(root_dir) / filename
            content = filepath.read_text(encoding='utf-8')
            original = content
            
            for old_text, new_text in EXACT_REPLACEMENTS:
                old_nfd = normalize_nfd(old_text)
                old_nfc = normalize_nfc(old_text)
                new_nfc = normalize_nfc(new_text)
                
                content = content.replace(old_nfd, new_nfc)
                content = content.replace(old_nfc, new_nfc)
            
            if content != original:
                filepath.write_text(content, encoding='utf-8')
                fixed_count += 1
                print(f"✓ Corrigé: {filepath.relative_to(ROOT)}")
    
    print(f"\n=== {fixed_count} fichiers corrigés ===")

if __name__ == "__main__":
    fix_all_files()
