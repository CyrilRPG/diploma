#!/usr/bin/env python3
"""
Script pour réorganiser le menu USPN S2:
- SOCLE avant APP et APP SPE
- Cours dans un ordre logique/pédagogique
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

def generate_menu_html(rel_prefix):
    """
    Génère le HTML du menu avec l'ordre correct.
    rel_prefix: préfixe pour les chemins relatifs (ex: "../../" ou "../" ou "")
    """
    
    # Structure du menu avec ordre correct
    # Format: (nom_fichier, titre_affiché)
    
    menu_structure = {
        "Génétique": {
            "SOCLE": [
                ("Genetique/SOCLE/caryotype_humain_om.html", "Caryotype humain"),
                ("Genetique/SOCLE/modes_de_transmission.html", "Modes de transmission"),
            ],
            "APP": [
                ("Genetique/APP/anomalies_de_caryotype_om.html", "Anomalies du caryotype"),
                ("Genetique/APP/diagnostic_pre_natal_et_diagnostique_pre_implanmatoire.html", "Diagnostic prénatal et préimplantatoire"),
            ],
        },
        "Histologie": {
            "SOCLE": [
                ("Histologie/SOCLE/me_thode_d_e_tude.html", "Méthodes d'étude"),
                ("Histologie/SOCLE/1_tissu_e_phitelial.html", "Tissu épithélial"),
                ("Histologie/SOCLE/2_tissus_e_phitelial.html", "Tissu épithélial (suite)"),
                ("Histologie/SOCLE/1_tissus_conjonctif.html", "Tissu conjonctif"),
                ("Histologie/SOCLE/2_tissus_conjonctif.html", "Tissu conjonctif (cellules)"),
                ("Histologie/SOCLE/3_tissus_conjonctif.html", "Tissu conjonctif (MEC)"),
                ("Histologie/SOCLE/1_tissus_cartilagineux.html", "Tissu cartilagineux"),
                ("Histologie/SOCLE/2_tissus_osseux.html", "Tissu osseux"),
                ("Histologie/SOCLE/1_tissus_musculaire.html", "Tissu musculaire"),
                ("Histologie/SOCLE/2_leiomyocyte.html", "Léiomyocyte"),
                ("Histologie/SOCLE/tissus_nerveux.html", "Tissu nerveux"),
            ],
            "APP": [
                ("Histologie/APP/ephitelium_glandulaires.html", "Épithéliums glandulaires"),
                ("Histologie/APP/tissus_conjonctif.html", "Tissu conjonctif"),
                ("Histologie/APP/2_tissus_squelettique.html", "Tissu squelettique"),
                ("Histologie/APP/tissus_musculaire_cardiaque.html", "Tissu musculaire cardiaque"),
                ("Histologie/APP/app_parenchyme_nerveux.html", "Parenchyme nerveux"),
            ],
            "APP SPE": [
                ("Histologie/APP_SPE/1_appareil_cardio.html", "Appareil cardiovasculaire"),
                ("Histologie/APP_SPE/2_appareil_cardiovasculaire.html", "Appareil cardiovasculaire (suite)"),
                ("Histologie/APP_SPE/appareil_urinaire.html", "Appareil urinaire"),
            ],
        },
        "Nutrition": {
            "SOCLE": [
                ("Nutrition/SOCLE/1_introduction.html", "Introduction à la nutrition"),
                ("Nutrition/SOCLE/me_tabolisme_glucides.html", "Métabolisme des glucides"),
                ("Nutrition/SOCLE/me_tabolisme_lipidique.html", "Métabolisme lipidique"),
                ("Nutrition/SOCLE/1_e_tabolisme_des_acides_amine_s.html", "Métabolisme des acides aminés"),
                ("Nutrition/SOCLE/2_e_tabolisme_des_acides_amine_s.html", "Métabolisme des acides aminés (suite)"),
                ("Nutrition/SOCLE/substrats_e_nerge_tique.html", "Substrats énergétiques"),
            ],
            "APP": [
                ("Nutrition/APP/app_relations_nutrition_sante.html", "Relations nutrition-santé"),
                ("Nutrition/APP/approfondissement_introduction_au_diabe_te.html", "Introduction au diabète"),
                ("Nutrition/APP/dysle_piudemie.html", "Dyslipidémie"),
                ("Nutrition/APP/obe_site_actu.html", "Obésité"),
            ],
        },
        "Embryologie": {
            "SOCLE": [],
            "APP": [],
            "APP SPE": [],
        },
    }
    
    html = []
    html.append('\t\t\t\t\t\t\t\t\t\t<ul>')
    html.append(f'\t\t\t\t\t\t\t\t\t\t\t<li><a href="{rel_prefix}index.html">Accueil</a></li>')
    html.append(f'\t\t\t\t\t\t\t\t\t\t\t<li><a href="{rel_prefix}favorites.html">Favoris</a></li>')
    
    for subject, categories in menu_structure.items():
        html.append('\t\t\t\t\t\t\t\t\t\t\t<li>')
        html.append(f'\t\t\t\t\t\t\t\t\t\t\t\t<span class="opener">{subject}</span>')
        html.append('\t\t\t\t\t\t\t\t\t\t\t\t<ul>')
        
        # Ordre: SOCLE, APP, APP SPE
        category_order = ["SOCLE", "APP", "APP SPE"]
        for cat in category_order:
            if cat not in categories:
                continue
            courses = categories[cat]
            
            html.append('\t\t\t\t\t\t\t\t\t\t\t\t\t<li>')
            html.append(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t<span class="opener">{cat}</span>')
            html.append('\t\t\t\t\t\t\t\t\t\t\t\t\t\t<ul>')
            
            if courses:
                for path, title in courses:
                    html.append(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="{rel_prefix}{path}">{title}</a></li>')
            else:
                html.append('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<!-- Aucun cours pour l\'instant -->')
            
            html.append('\t\t\t\t\t\t\t\t\t\t\t\t\t\t</ul>')
            html.append('\t\t\t\t\t\t\t\t\t\t\t\t\t</li>')
        
        html.append('\t\t\t\t\t\t\t\t\t\t\t\t</ul>')
        html.append('\t\t\t\t\t\t\t\t\t\t\t</li>')
    
    html.append('\t\t\t\t\t\t\t\t\t\t</ul>')
    
    return '\n'.join(html)


def get_relative_prefix(filepath):
    """Calcule le préfixe relatif pour les liens depuis un fichier."""
    rel = filepath.relative_to(USPN_S2_ROOT)
    depth = len(rel.parts) - 1  # -1 pour le fichier lui-même
    
    if depth == 0:
        return ""
    else:
        return "../" * depth


def fix_menu_in_file(filepath):
    """Remplace le menu dans un fichier HTML."""
    content = filepath.read_text(encoding='utf-8')
    
    # Calculer le préfixe relatif
    rel_prefix = get_relative_prefix(filepath)
    
    # Générer le nouveau menu
    new_menu = generate_menu_html(rel_prefix)
    
    # Pattern pour trouver l'ancien menu (de <ul> après Menu jusqu'à </ul> avant </nav>)
    pattern = r'(<nav id="menu">\s*<header class="major">\s*<h2>Menu</h2>\s*</header>\s*)\n\t*<ul>.*?</ul>(\s*</nav>)'
    
    replacement = r'\1\n' + new_menu + r'\2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        return True
    return False


def main():
    fixed_count = 0
    
    for root, dirs, files in os.walk(USPN_S2_ROOT):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = Path(root) / filename
            print(f"Traitement de {filepath.relative_to(ROOT)}...")
            
            if fix_menu_in_file(filepath):
                fixed_count += 1
                print(f"  ✓ Corrigé")
            else:
                print(f"  - Pas de changement")
    
    print(f"\n=== {fixed_count} fichiers corrigés ===")


if __name__ == "__main__":
    main()
