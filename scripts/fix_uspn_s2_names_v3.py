#!/usr/bin/env python3
"""
Script pour corriger les noms dans les fichiers USPN_S2.
Gère les problèmes d'encodage Unicode NFD/NFC.
"""
import os
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

# Corrections finales
EXACT_REPLACEMENTS = [
    # Histologie
    ("1 Tissu éphitelial", "Tissu épithélial"),
    ("2 Tissus éphitelial", "Tissu épithélial (suite)"),
    ("Méthode d étude", "Méthodes d'étude"),
    
    # Nutrition APP
    ("App Relations nutrition-santé", "Relations nutrition-santé"),
    ("Approfondissement introduction au diabète", "Introduction au diabète"),
    ("Dyslépiudemie", "Dyslipidémie"),
    ("Obésité ACTU", "Obésité"),
    
    # Nutrition SOCLE
    ("Métabolisme glucides", "Métabolisme des glucides"),
    ("Substrats énergétique", "Substrats énergétiques"),
]

def normalize_nfd(s):
    """Normalise en NFD (décomposé)"""
    return unicodedata.normalize('NFD', s)

def normalize_nfc(s):
    """Normalise en NFC (composé)"""
    return unicodedata.normalize('NFC', s)

def fix_all_files():
    """Corrige tous les fichiers HTML USPN_S2."""
    fixed_count = 0
    
    for root_dir, dirs, files in os.walk(USPN_S2_ROOT):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = Path(root_dir) / filename
            content = filepath.read_text(encoding='utf-8')
            original = content
            
            for old_text, new_text in EXACT_REPLACEMENTS:
                # Essayer les deux formes de normalisation
                old_nfd = normalize_nfd(old_text)
                old_nfc = normalize_nfc(old_text)
                new_nfc = normalize_nfc(new_text)
                
                # Remplacer dans le contenu
                content = content.replace(old_nfd, new_nfc)
                content = content.replace(old_nfc, new_nfc)
            
            if content != original:
                filepath.write_text(content, encoding='utf-8')
                fixed_count += 1
                print(f"✓ Corrigé: {filepath.relative_to(ROOT)}")
    
    print(f"\n=== {fixed_count} fichiers corrigés ===")

if __name__ == "__main__":
    fix_all_files()
