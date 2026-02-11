#!/usr/bin/env python3
"""
Script pour corriger les noms restants dans les fichiers USPN_S2.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

# Corrections finales exactes pour les liens du menu
EXACT_REPLACEMENTS = [
    # Format: (ancien texte exact, nouveau texte)
    (">1 Tissu éphitelial<", ">Tissu épithélial<"),
    (">2 Tissus éphitelial<", ">Tissu épithélial (suite)<"),
    (">1 Tissu éphitélial<", ">Tissu épithélial<"),
    (">2 Tissus éphitélial<", ">Tissu épithélial (suite)<"),
    (">Méthode d étude<", ">Méthodes d'étude<"),
    (">App Relations nutrition-santé<", ">Relations nutrition-santé<"),
    (">Approfondissement introduction au diabète<", ">Introduction au diabète<"),
    (">Dyslépiudemie<", ">Dyslipidémie<"),
    (">Obésité ACTU<", ">Obésité<"),
    (">Obésité actu<", ">Obésité<"),
    (">1. étabolisme des acides aminés<", ">Métabolisme des acides aminés<"),
    (">1 étabolisme des acides aminés<", ">Métabolisme des acides aminés<"),
    (">2 étabolisme des acides aminés<", ">Métabolisme des acides aminés (suite)<"),
    (">Métabolisme glucides<", ">Métabolisme des glucides<"),
    (">Substrats énergétique<", ">Substrats énergétiques<"),
    # Pour les h2
    ("SOCLE - 1 tissu e phitelial", "SOCLE - Tissu épithélial"),
    ("SOCLE - 2 tissus e phitelial", "SOCLE - Tissu épithélial (suite)"),
    ("SOCLE - Me thode d e tude", "SOCLE - Méthodes d'étude"),
    ("APP - App relations nutrition sante", "APP - Relations nutrition-santé"),
    ("APP - Approfondissement introduction au diabe te", "APP - Introduction au diabète"),
    ("APP - Dysle piudemie", "APP - Dyslipidémie"),
    ("APP - Obe site actu", "APP - Obésité"),
    ("SOCLE - 1 e tabolisme des acides amine s", "SOCLE - Métabolisme des acides aminés"),
    ("SOCLE - 2 e tabolisme des acides amine s", "SOCLE - Métabolisme des acides aminés (suite)"),
    ("SOCLE - Me tabolisme glucides", "SOCLE - Métabolisme des glucides"),
    ("SOCLE - Substrats e nerge tique", "SOCLE - Substrats énergétiques"),
    ("SOCLE - 1 Introduction", "SOCLE - Introduction à la nutrition"),
    ("SOCLE - 1 introduction", "SOCLE - Introduction à la nutrition"),
    ("SOCLE - Me tabolisme lipidique", "SOCLE - Métabolisme lipidique"),
    # Corrections supplémentaires
    (">1 tissus conjonctif<", ">Tissu conjonctif<"),
    (">1 Tissus conjonctif<", ">Tissu conjonctif<"),
]

def fix_all_files():
    """Corrige tous les fichiers HTML USPN_S2."""
    fixed_count = 0
    
    for root, dirs, files in os.walk(USPN_S2_ROOT):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = Path(root) / filename
            content = filepath.read_text(encoding='utf-8')
            original = content
            
            for old_text, new_text in EXACT_REPLACEMENTS:
                content = content.replace(old_text, new_text)
            
            if content != original:
                filepath.write_text(content, encoding='utf-8')
                fixed_count += 1
                print(f"✓ Corrigé: {filepath.relative_to(ROOT)}")
    
    print(f"\n=== {fixed_count} fichiers corrigés ===")

if __name__ == "__main__":
    fix_all_files()
