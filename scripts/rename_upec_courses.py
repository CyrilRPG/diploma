#!/usr/bin/env python3
"""Rename all UPEC_LSPS1_S2 course titles based on fiches originales."""

import os
import re
from pathlib import Path

BASE = Path("/Users/cyrilwisa/Desktop/diploma/UPEC_LSPS1_S2")

# Mapping: href_suffix -> (old_menu_title, new_title)
# The href_suffix is the path portion that uniquely identifies each course
COURSES = {
    # ICM
    "ICM/fc1.html": ("Cours 1 - Le médicament", "Généralités sur les médicaments (partie 1)"),
    "ICM/fc1_2.html": ("Cours 1.2 - Le médicament (suite)", "Généralités sur les médicaments (partie 2)"),
    "ICM/fc2.html": ("Cours 2", "Interaction ligand-récepteur"),
    "ICM/fc3.html": ("Cours 3", "Voies de signalisation"),
    "ICM/fc4.html": ("Cours 4", "Pharmacométrie"),
    "ICM/fc5.html": ("Cours 5", "Étapes pharmacocinétiques"),
    "ICM/fc6_1.html": ("Cours 6.1", "Paramètres pharmacocinétiques"),
    "ICM/fc6_2.html": ("Cours 6.2", "Pharmacocinétique et formes galéniques"),
    "ICM/fc7.html": ("Cours 7", "Pharmacocinétique et prescription"),
    "ICM/fc8.html": ("Cours 8", "Variabilité de la réponse au médicament"),
    "ICM/fc9.html": ("Cours 9", "Conception et identification du médicament"),
    "ICM/fc10.html": ("Cours 10", "Développement pré-clinique"),
    "ICM/fc11.html": ("Cours 11", "Développement clinique"),
    "ICM/fc12.html": ("Cours 12", "Structure et régulation du médicament"),
    "ICM/fc13.html": ("Cours 13", "Générique et biosimilaire"),
    "ICM/fc14.html": ("Cours 14", "Circuits de dispensation des médicaments"),
    "ICM/fc15.html": ("Cours 15", "Iatrogénie"),
    
    # Bio-informatique
    "Bio_Informatique/fc1.html": ("Cours 1 - Introduction à la bio-informatique", "Introduction à la bio-informatique"),
    "Bio_Informatique/fc2.html": ("Cours 2", "Bases de données bio-informatiques"),
    "Bio_Informatique/fc3.html": ("Cours 3", "Comparaison de séquences"),
    
    # Circulation Respiration - Anatomie
    "Circulation_Respiration/Anatomie/fc1.html": ("Cours 1", "Introduction sur l'appareil cardiovasculaire"),
    "Circulation_Respiration/Anatomie/fc2.html": ("Cours 2", "Cœur, aspects extérieurs"),
    "Circulation_Respiration/Anatomie/fc3.html": ("Cours 3", "Cœur droit et cœur gauche"),
    "Circulation_Respiration/Anatomie/fc4.html": ("Cours 4", "Péricarde"),
    "Circulation_Respiration/Anatomie/fc5.html": ("Cours 5", "Artères et veines coronaires"),
    "Circulation_Respiration/Anatomie/fc6.html": ("Cours 6", "Innervation du cœur"),
    "Circulation_Respiration/Anatomie/fc7.html": ("Cours 7", "Structure du cœur et valves cardiaques"),
    "Circulation_Respiration/Anatomie/fc8.html": ("Cours 8", "Principales artères du corps"),
    "Circulation_Respiration/Anatomie/fc9.html": ("Cours 9", "Coupes du cœur"),
    "Circulation_Respiration/Anatomie/fc10.html": ("Cours 10", "Anatomie de l'appareil respiratoire"),
    
    # Circulation Respiration - Physiologie
    "Circulation_Respiration/Physiologie/fc1.html": ("Cours 1", "Voies aériennes et transports gazeux"),
    "Circulation_Respiration/Physiologie/fc2.html": ("Cours 2", "Équilibre acide-base"),
    "Circulation_Respiration/Physiologie/fc3.html": ("Cours 3", "Cellule musculaire cardiaque"),
    "Circulation_Respiration/Physiologie/fc4.html": ("Cours 4", "ECG et cœur"),
    "Circulation_Respiration/Physiologie/fc5.html": ("Cours 5", "Pression artérielle"),
    "Circulation_Respiration/Physiologie/fc6.html": ("Cours 6", "Régulation de la pression artérielle"),
    "Circulation_Respiration/Physiologie/fc7.html": ("Cours 7", "Le cycle cardiaque"),
    
    # Régulation Neuroendocrienne - Anatomie
    "Regulation_Neuroendocrienne/Anatomie/fc1.html": ("Cours 1", "Anatomie générale du système nerveux"),
    "Regulation_Neuroendocrienne/Anatomie/fc2.html": ("Cours 2", "Neurone"),
    "Regulation_Neuroendocrienne/Anatomie/fc3.html": ("Cours 3", "Schéma général des réseaux neuronaux"),
    "Regulation_Neuroendocrienne/Anatomie/fc4.html": ("Cours 4", "Système nerveux végétatif ou autonome"),
    "Regulation_Neuroendocrienne/Anatomie/fc5.html": ("Cours 5", "Sécrétion hormonale"),
    "Regulation_Neuroendocrienne/Anatomie/fc6.html": ("Cours 6", "Anatomie digestive simplifiée"),
    
    # Régulation Neuroendocrienne - Physiologie
    "Regulation_Neuroendocrienne/Physiologie/fc1.html": ("Cours 1", "Fonction digestive"),
    "Regulation_Neuroendocrienne/Physiologie/fc2.html": ("Cours 2", "Fonctions hépatiques"),
    "Regulation_Neuroendocrienne/Physiologie/fc3.html": ("Cours 3", "Fonctions pancréatiques"),
    "Regulation_Neuroendocrienne/Physiologie/fc4.html": ("Cours 4", "Rôle de l'intestin grêle et du colon"),
    "Regulation_Neuroendocrienne/Physiologie/fc5.html": ("Cours 5", "Diabète"),
    "Regulation_Neuroendocrienne/Physiologie/fc6.html": ("Cours 6", "Hypothalamus, faim et satiété"),
    
    # Squelette Motricité - Anatomie
    "Squelette_Motricite/Anatomie/fc1.html": ("Cours 1", "Les os du crâne"),
    "Squelette_Motricite/Anatomie/fc2.html": ("Cours 2", "Os de la face"),
    "Squelette_Motricite/Anatomie/fc3.html": ("Cours 3", "Cavités de la face"),
    "Squelette_Motricite/Anatomie/fc4.html": ("Cours 4", "Membre supérieur"),
    "Squelette_Motricite/Anatomie/fc5.html": ("Cours 5", "Ceinture scapulaire"),
    "Squelette_Motricite/Anatomie/fc6.html": ("Cours 6", "Bras"),
    
    # Squelette Motricité - Activité physique
    "Squelette_Motricite/Activite_Physique/fc1.html": ("Cours 1", "Connaissances générales sur l'activité physique"),
    "Squelette_Motricite/Activite_Physique/fc2.html": ("Cours 2", "Adaptations cardiaques à l'exercice"),
    "Squelette_Motricite/Activite_Physique/fc3.html": ("Cours 3", "Adaptations respiratoires à l'exercice"),
    "Squelette_Motricite/Activite_Physique/fc4.html": ("Cours 4", "Adaptations hormonales à l'exercice"),
    
    # Squelette Motricité - Situations de handicap
    "Squelette_Motricite/Situations_Handicap/fc1.html": ("Cours 1", "Réadaptation"),
    "Squelette_Motricite/Situations_Handicap/fc2.html": ("Cours 2", "Moyens de compensation"),
    
    # Squelette Motricité - Physiologie
    "Squelette_Motricite/Physiologie/fc1.html": ("Cours 1", "Biomécanique de la force musculaire"),
    "Squelette_Motricite/Physiologie/fc2.html": ("Cours 2", "Excitation-contraction"),
}


def update_all_files():
    """Update titles in all HTML files."""
    html_files = list(BASE.rglob("*.html"))
    updated_count = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1) Replace menu link titles: match href containing the course path + old title
        for href_suffix, (old_title, new_title) in COURSES.items():
            # Menu links can have various prefix depths (../ or ../../)
            # Match pattern: href="<any_prefix>HREF_SUFFIX">OLD_TITLE</a>
            pattern = re.compile(
                r'(href="[^"]*' + re.escape(href_suffix) + r'">)' + re.escape(old_title) + r'(</a>)'
            )
            content = pattern.sub(r'\g<1>' + new_title + r'\2', content)
        
        # 2) Replace <h2> header title on the course's own page
        # Determine which course this file is
        rel = html_file.relative_to(BASE)
        rel_str = str(rel)
        if rel_str in COURSES:
            old_title, new_title = COURSES[rel_str]
            content = content.replace(f"<h2>{old_title}</h2>", f"<h2>{new_title}</h2>")
        
        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"Updated: {rel_str}")
    
    print(f"\nTotal updated: {updated_count}/{len(html_files)}")


if __name__ == "__main__":
    update_all_files()
