#!/usr/bin/env python3
"""
Script to fix navigation menus in all USPN_S2 HTML files.
Ensures all files have the complete, standardized menu.
"""

import os
import re
from pathlib import Path

# Base directory
BASE_DIR = Path("/Users/cyrilwisa/Desktop/diploma/USPN_S2")

# Complete menu template for course files (../../ prefix)
COMPLETE_MENU_COURSE = '''<nav id="menu">
							<header class="major">
								<h2>Menu</h2>
							</header>
										<ul>
											<li><a href="../../index.html">Accueil</a></li>
											<li><a href="../../favorites.html">Favoris</a></li>
											<li>
												<span class="opener">Génétique</span>
												<ul>
													<li>
														<span class="opener">SOCLE</span>
														<ul>
															<li><a href="../../Genetique/SOCLE/caryotype_humain_om.html">Caryotype humain</a></li>
															<li><a href="../../Genetique/SOCLE/modes_de_transmission.html">Modes de transmission</a></li>
														</ul>
													</li>
													<li>
														<span class="opener">APP</span>
														<ul>
															<li><a href="../../Genetique/APP/anomalies_de_caryotype_om.html">Anomalies du caryotype</a></li>
															<li><a href="../../Genetique/APP/diagnostic_pre_natal_et_diagnostique_pre_implanmatoire.html">Diagnostic prénatal et préimplantatoire</a></li>
														</ul>
													</li>
												</ul>
											</li>
											<li>
												<span class="opener">Histologie</span>
												<ul>
													<li>
														<span class="opener">SOCLE</span>
														<ul>
															<li><a href="../../Histologie/SOCLE/me_thode_d_e_tude.html">Méthodes d'étude</a></li>
															<li><a href="../../Histologie/SOCLE/1_tissu_e_phitelial.html">Tissu épithélial</a></li>
															<li><a href="../../Histologie/SOCLE/2_tissus_e_phitelial.html">Tissu épithélial (suite)</a></li>
															<li><a href="../../Histologie/SOCLE/1_tissus_conjonctif.html">Tissu conjonctif</a></li>
															<li><a href="../../Histologie/SOCLE/2_tissus_conjonctif.html">Tissu conjonctif (cellules)</a></li>
															<li><a href="../../Histologie/SOCLE/3_tissus_conjonctif.html">Tissu conjonctif (MEC)</a></li>
															<li><a href="../../Histologie/SOCLE/1_tissus_cartilagineux.html">Tissu cartilagineux</a></li>
															<li><a href="../../Histologie/SOCLE/2_tissus_osseux.html">Tissu osseux</a></li>
															<li><a href="../../Histologie/SOCLE/1_tissus_musculaire.html">Tissu musculaire</a></li>
															<li><a href="../../Histologie/SOCLE/2_leiomyocyte.html">Léiomyocyte</a></li>
															<li><a href="../../Histologie/SOCLE/tissus_nerveux.html">Tissu nerveux</a></li>
														</ul>
													</li>
													<li>
														<span class="opener">APP</span>
														<ul>
															<li><a href="../../Histologie/APP/ephitelium_glandulaires.html">Épithéliums glandulaires</a></li>
															<li><a href="../../Histologie/APP/tissus_conjonctif.html">Tissu conjonctif</a></li>
															<li><a href="../../Histologie/APP/2_tissus_squelettique.html">Tissu squelettique</a></li>
															<li><a href="../../Histologie/APP/tissus_musculaire_cardiaque.html">Tissu musculaire cardiaque</a></li>
															<li><a href="../../Histologie/APP/app_parenchyme_nerveux.html">Parenchyme nerveux</a></li>
														</ul>
													</li>
													<li>
														<span class="opener">APP SPE</span>
														<ul>
															<li><a href="../../Histologie/APP_SPE/1_appareil_cardio.html">Appareil cardiovasculaire</a></li>
															<li><a href="../../Histologie/APP_SPE/2_appareil_cardiovasculaire.html">Appareil cardiovasculaire (suite)</a></li>
															<li><a href="../../Histologie/APP_SPE/appareil_urinaire.html">Appareil urinaire</a></li>
														</ul>
													</li>
												</ul>
											</li>
											<li>
												<span class="opener">Nutrition</span>
												<ul>
													<li>
														<span class="opener">SOCLE</span>
														<ul>
															<li><a href="../../Nutrition/SOCLE/1_introduction.html">Introduction à la nutrition</a></li>
															<li><a href="../../Nutrition/SOCLE/me_tabolisme_glucides.html">Métabolisme des glucides</a></li>
															<li><a href="../../Nutrition/SOCLE/me_tabolisme_lipidique.html">Métabolisme lipidique</a></li>
															<li><a href="../../Nutrition/SOCLE/1_e_tabolisme_des_acides_amine_s.html">Métabolisme des acides aminés</a></li>
															<li><a href="../../Nutrition/SOCLE/2_e_tabolisme_des_acides_amine_s.html">Métabolisme des acides aminés (suite)</a></li>
															<li><a href="../../Nutrition/SOCLE/substrats_e_nerge_tique.html">Substrats énergétiques</a></li>
														</ul>
													</li>
													<li>
														<span class="opener">APP</span>
														<ul>
															<li><a href="../../Nutrition/APP/app_relations_nutrition_sante.html">Relations nutrition-santé</a></li>
															<li><a href="../../Nutrition/APP/approfondissement_introduction_au_diabe_te.html">Introduction au diabète</a></li>
															<li><a href="../../Nutrition/APP/dysle_piudemie.html">Dyslipidémie</a></li>
															<li><a href="../../Nutrition/APP/obe_site_actu.html">Obésité</a></li>
														</ul>
													</li>
												</ul>
											</li>
											<li>
												<span class="opener">Embryologie</span>
												<ul>
													<li>
														<span class="opener">SOCLE</span>
														<ul>
															<li><a href="../../Embryologie/SOCLE/introduction.html">Introduction</a></li>
															<li><a href="../../Embryologie/SOCLE/gametogenese.html">Gamétogenèse</a></li>
															<li><a href="../../Embryologie/SOCLE/fecondation.html">Fécondation</a></li>
															<li><a href="../../Embryologie/SOCLE/premiere_deuxieme_semaine.html">Semaines 1 et 2</a></li>
															<li><a href="../../Embryologie/SOCLE/troisieme_quatrieme_semaine.html">Semaines 3 et 4</a></li>
														</ul>
													</li>
													<li>
														<span class="opener">APP</span>
														<ul>
															<li><a href="../../Embryologie/APP/1ere_semaine_developpement.html">1ère semaine de développement</a></li>
															<li><a href="../../Embryologie/APP/2eme_semaine_developpement.html">2ème semaine de développement</a></li>
															<li><a href="../../Embryologie/APP/3eme_semaine_developpement.html">3ème semaine de développement</a></li>
															<li><a href="../../Embryologie/APP/4eme_semaine_developpement.html">4ème semaine de développement</a></li>
														</ul>
													</li>
													<li>
														<span class="opener">APP SPE</span>
														<ul>
															<li><a href="../../Embryologie/APP_SPE/appareil_cardiovasculaire.html">Appareil cardiovasculaire</a></li>
															<li><a href="../../Embryologie/APP_SPE/voies_aeriennes_sup.html">Voies aériennes supérieures</a></li>
															<li><a href="../../Embryologie/APP_SPE/voies_aeriennes_profondes.html">Voies aériennes profondes</a></li>
															<li><a href="../../Embryologie/APP_SPE/appareil_urinaire.html">Appareil urinaire</a></li>
														</ul>
													</li>
												</ul>
											</li>
										</ul>
						</nav>'''


def find_html_files():
    """Find all HTML files in course directories (not index.html or favorites.html)."""
    html_files = []
    for matiere in ['Genetique', 'Histologie', 'Nutrition', 'Embryologie']:
        matiere_dir = BASE_DIR / matiere
        if matiere_dir.exists():
            for subcat in ['SOCLE', 'APP', 'APP_SPE']:
                subcat_dir = matiere_dir / subcat
                if subcat_dir.exists():
                    for html_file in subcat_dir.glob('*.html'):
                        html_files.append(html_file)
    return html_files


def update_menu(file_path):
    """Update the menu in a single HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the nav menu section
    # Pattern to match from <nav id="menu"> to </nav>
    pattern = r'<nav id="menu">.*?</nav>'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, COMPLETE_MENU_COURSE, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    return False


def main():
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files to process")
    
    updated = 0
    for file_path in html_files:
        if update_menu(file_path):
            updated += 1
            print(f"Updated: {file_path.relative_to(BASE_DIR)}")
        else:
            print(f"Skipped (no change): {file_path.relative_to(BASE_DIR)}")
    
    print(f"\nTotal updated: {updated}/{len(html_files)}")


if __name__ == "__main__":
    main()
