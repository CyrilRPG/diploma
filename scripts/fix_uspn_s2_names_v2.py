#!/usr/bin/env python3
"""
Script pour corriger les noms restants dans les fichiers USPN_S2.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

# Corrections finales exactes
EXACT_REPLACEMENTS = [
    # Histologie
    (">1 Tissu éphitelial<", ">Tissu épithélial<"),
    (">2 Tissus éphitelial<", ">Tissu épithélial (suite)<"),
    (">Méthode d étude<", ">Méthodes d'étude<"),
    
    # Nutrition APP
    (">App Relations nutrition-santé<", ">Relations nutrition-santé<"),
    (">Approfondissement introduction au diabète<", ">Introduction au diabète<"),
    (">Dyslépiudemie<", ">Dyslipidémie<"),
    (">Obésité ACTU<", ">Obésité<"),
    
    # Nutrition SOCLE
    (">Métabolisme glucides<", ">Métabolisme des glucides<"),
    (">Substrats énergétique<", ">Substrats énergétiques<"),
    
    # h2 headers
    ("<h2>SOCLE - Métabolisme glucides</h2>", "<h2>SOCLE - Métabolisme des glucides</h2>"),
    ("<h2>SOCLE - Substrats énergétique</h2>", "<h2>SOCLE - Substrats énergétiques</h2>"),
    ("<h2>APP - Dyslépiudemie</h2>", "<h2>APP - Dyslipidémie</h2>"),
    ("<h2>APP - Obésité ACTU</h2>", "<h2>APP - Obésité</h2>"),
    ("<h2>APP - App Relations nutrition-santé</h2>", "<h2>APP - Relations nutrition-santé</h2>"),
    ("<h2>APP - Approfondissement introduction au diabète</h2>", "<h2>APP - Introduction au diabète</h2>"),
    ("<h2>SOCLE - 1 Tissu éphitelial</h2>", "<h2>SOCLE - Tissu épithélial</h2>"),
    ("<h2>SOCLE - 2 Tissus éphitelial</h2>", "<h2>SOCLE - Tissu épithélial (suite)</h2>"),
    ("<h2>SOCLE - Méthode d étude</h2>", "<h2>SOCLE - Méthodes d'étude</h2>"),
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
