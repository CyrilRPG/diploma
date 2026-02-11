#!/usr/bin/env python3
"""Regenerate flashcards for courses with <40 flashcards in UPEC_LSPS1_S2."""

import os
import re

BASE = "/Users/cyrilwisa/Desktop/diploma/UPEC_LSPS1_S2"

def replace_flashcards(filepath, flashcards):
    """Replace flashcardsData in an HTML file with new flashcard array."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Build JS array string
    entries = []
    for q, a in flashcards:
        # Escape single quotes in French text with curly apostrophe
        q = q.replace("'", "\u2019")
        a = a.replace("'", "\u2019")
        entries.append(f"{{ question: '{q}', answer: '{a}' }}")
    
    js_array = ",\n".join(entries)
    
    # Replace the flashcardsData block
    pattern = r"const flashcardsData\s*=\s*\[.*?\];"
    replacement = f"const flashcardsData = [\n{js_array}\n];"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"  WARNING: No replacement made in {filepath}")
        return False
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


# ============================================================
# COURSE 1: Coupes du cœur (fc9.html) - Circulation_Respiration/Anatomie
# ============================================================
COUPES_COEUR = [
    ("Qu'est-ce que le médiastin ?", "Zone située entre les deux poumons contenant la masse cardiaque, les gros vaisseaux et les conduits traversant les régions cervicale, thoracique et abdominale."),
    ("Par quelle vertèbre passe la première coupe du cœur ?", "La 8ème vertèbre thoracique (T8)."),
    ("Que contient le médiastin ?", "La masse cardiaque, les gros vaisseaux allant et venant du cœur, et les conduits traversant les régions cervicale, thoracique et abdominale."),
    ("Quel type de coupe est la 2ème coupe du cœur ?", "Une coupe sagittale."),
    ("Par quoi passe la 3ème coupe du cœur ?", "Par le petit axe du cœur."),
    ("Quelle observation fait-on sur la 3ème coupe du cœur concernant les ventricules ?", "Les parois du ventricule gauche sont épaisses comparées à celles du ventricule droit."),
    ("Pourquoi le ventricule gauche a-t-il des parois plus épaisses que le ventricule droit ?", "Car il doit éjecter le sang dans la circulation systémique à haute pression, tandis que le ventricule droit éjecte dans la circulation pulmonaire à basse pression."),
    ("Quels sont les 2 stades du cycle cardiaque visibles sur la 4ème coupe ?", "La systole (contraction du muscle) et la diastole (remplissage des ventricules)."),
    ("Qu'est-ce que la systole ?", "La phase du cycle cardiaque où le muscle cardiaque se contracte pour éjecter le sang."),
    ("Qu'est-ce que la diastole ?", "La phase du cycle cardiaque où les ventricules se remplissent de sang."),
    ("Quelle observation fait-on sur la 4ème coupe concernant les valves ?", "Il existe un décalage entre la valve tricuspide et la valve mitrale : la valve tricuspide est un peu plus apicale."),
    ("Qu'est-ce qu'une position apicale pour une valve ?", "Une position plus proche de la pointe (apex) du cœur."),
    ("Quelles séquences d'IRM dynamique sont réalisées ?", "Des séquences passant par T8 et par le petit axe du cœur."),
    ("À quoi servent les séquences d'IRM dynamique du cœur ?", "À visualiser le cœur en mouvement, observer la contraction et le remplissage des cavités cardiaques."),
    ("Quel est le rapport entre l'épaisseur des parois ventriculaires et la pression exercée ?", "Plus la pression que doit exercer un ventricule est élevée, plus ses parois sont épaisses."),
    ("Quelle est la pression systolique normale dans le ventricule gauche ?", "Environ 120 mmHg."),
    ("Quelle est la pression systolique normale dans le ventricule droit ?", "Environ 25 mmHg."),
    ("Comment appelle-t-on la cloison entre les deux ventricules ?", "Le septum interventriculaire."),
    ("Quelle est l'orientation générale du cœur dans le thorax ?", "Le cœur est orienté en avant, à gauche et en bas, avec l'apex dirigé vers la gauche."),
    ("Combien de cavités possède le cœur ?", "4 cavités : 2 atriums (oreillettes) et 2 ventricules."),
    ("Qu'est-ce que l'apex du cœur ?", "La pointe du cœur, formée par le ventricule gauche, dirigée vers la gauche et en bas."),
    ("Qu'est-ce que la base du cœur ?", "La face postérieure du cœur, formée principalement par les atriums."),
    ("Quel est le plan de coupe le plus utilisé en échocardiographie ?", "Le plan petit axe (coupe transversale perpendiculaire au grand axe du cœur)."),
    ("Qu'observe-t-on en coupe petit axe au niveau des ventricules ?", "Le ventricule gauche apparaît circulaire avec des parois épaisses, et le ventricule droit en forme de croissant avec des parois fines."),
    ("Que sépare le septum interatrial ?", "Les deux atriums (oreillettes) droit et gauche."),
    ("Que sépare le septum interventriculaire ?", "Les deux ventricules droit et gauche."),
    ("Quels sont les gros vaisseaux qui partent du cœur ?", "L'aorte (du ventricule gauche) et le tronc pulmonaire (du ventricule droit)."),
    ("Quels sont les gros vaisseaux qui arrivent au cœur ?", "Les veines caves supérieure et inférieure (dans l'atrium droit) et les 4 veines pulmonaires (dans l'atrium gauche)."),
    ("Comment visualise-t-on les coupes du cœur en imagerie ?", "Par échocardiographie, IRM cardiaque, scanner cardiaque."),
    ("Qu'est-ce que le sillon interventriculaire antérieur ?", "Le sillon situé sur la face antérieure du cœur qui sépare les deux ventricules."),
    ("Qu'est-ce que le sillon coronaire ?", "Le sillon qui sépare les atriums des ventricules, contenant les artères et veines coronaires."),
    ("Quelle face du cœur est en contact avec le diaphragme ?", "La face inférieure (diaphragmatique)."),
    ("Quelle face du cœur est en contact avec le sternum ?", "La face antérieure (sterno-costale)."),
    ("Quelle valve sépare l'atrium droit du ventricule droit ?", "La valve tricuspide."),
    ("Quelle valve sépare l'atrium gauche du ventricule gauche ?", "La valve mitrale (bicuspide)."),
    ("Quelle valve se trouve à la sortie du ventricule droit ?", "La valve pulmonaire."),
    ("Quelle valve se trouve à la sortie du ventricule gauche ?", "La valve aortique."),
    ("Comment circule le sang dans le cœur droit ?", "VCS/VCI → atrium droit → valve tricuspide → ventricule droit → valve pulmonaire → tronc pulmonaire."),
    ("Comment circule le sang dans le cœur gauche ?", "Veines pulmonaires → atrium gauche → valve mitrale → ventricule gauche → valve aortique → aorte."),
    ("Quel est le rôle du cœur droit ?", "Propulser le sang désoxygéné vers les poumons via la circulation pulmonaire."),
    ("Quel est le rôle du cœur gauche ?", "Propulser le sang oxygéné vers l'ensemble de l'organisme via la circulation systémique."),
    ("Qu'est-ce qu'une coupe 4 cavités ?", "Une coupe passant par les 4 cavités cardiaques, montrant les 2 atriums et les 2 ventricules simultanément."),
    ("En coupe 4 cavités, quel ventricule est le plus proche de l'apex ?", "Le ventricule gauche."),
    ("Quel est le rapport entre le cœur et le poumon gauche ?", "Le cœur crée une empreinte cardiaque sur la face médiale du poumon gauche."),
    ("Quelles structures médiastinales sont visibles sur une coupe passant par T8 ?", "Le cœur, l'aorte descendante, l'œsophage, les poumons."),
    ("Comment distingue-t-on le ventricule droit du gauche en imagerie ?", "Le VD a une paroi fine et contient le trabécule septo-marginal ; le VG a une paroi épaisse et un aspect plus lisse."),
    ("Qu'est-ce que le trabécule septo-marginal ?", "Une bande musculaire dans le ventricule droit reliant le septum à la paroi libre."),
    ("Quels muscles papillaires trouve-t-on dans le ventricule droit ?", "3 muscles papillaires : antérieur, postérieur et septal."),
    ("Quels muscles papillaires trouve-t-on dans le ventricule gauche ?", "2 muscles papillaires : antéro-latéral et postéro-médial."),
    ("Quel est l'épaisseur normale de la paroi du ventricule gauche ?", "Environ 10-12 mm en diastole."),
    ("Quel est l'épaisseur normale de la paroi du ventricule droit ?", "Environ 3-5 mm."),
    ("En coupe petit axe, comment apparaît le septum interventriculaire ?", "Comme une cloison convexe vers le ventricule droit (bombant dans le VD)."),
    ("Qu'est-ce que la fraction d'éjection ?", "Le pourcentage de sang éjecté du ventricule à chaque systole (normale : 55-70% pour le VG)."),
    ("Que se passe-t-il pendant la systole auriculaire ?", "Les atriums se contractent, achevant le remplissage des ventricules (contribution de 20-30%)."),
    ("Que se passe-t-il pendant la systole ventriculaire ?", "Les ventricules se contractent, les valves AV se ferment, les valves sigmoïdes s'ouvrent et le sang est éjecté."),
    ("Que se passe-t-il pendant la diastole ventriculaire ?", "Les ventricules se relâchent, les valves sigmoïdes se ferment et les ventricules se remplissent passivement."),
    ("En IRM cardiaque, quelle séquence permet de visualiser le mouvement du cœur ?", "Les séquences ciné en mode SSFP (steady-state free precession)."),
    ("Qu'est-ce que la contraction isovolumétrique ?", "Phase de la systole où la pression ventriculaire augmente sans changement de volume (toutes les valves sont fermées)."),
    ("Qu'est-ce que la relaxation isovolumétrique ?", "Phase de la diastole où la pression ventriculaire diminue sans changement de volume (toutes les valves sont fermées)."),
    ("Comment appelle-t-on le volume de sang éjecté à chaque battement ?", "Le volume d'éjection systolique (VES), normalement 70-80 mL."),
    ("Comment calcule-t-on le débit cardiaque ?", "Débit cardiaque = fréquence cardiaque × volume d'éjection systolique (environ 5 L/min au repos)."),
    ("Qu'est-ce que le volume télédiastolique (VTD) ?", "Le volume de sang dans le ventricule à la fin de la diastole (environ 120 mL pour le VG)."),
    ("Qu'est-ce que le volume télésystolique (VTS) ?", "Le volume de sang résiduel dans le ventricule à la fin de la systole (environ 50 mL pour le VG)."),
    ("Quelle est la formule du volume d'éjection systolique ?", "VES = VTD - VTS."),
    ("Quelle est la formule de la fraction d'éjection ?", "FE = (VES / VTD) × 100."),
    ("En coupe grand axe, quelles structures sont bien visibles ?", "Le ventricule gauche, l'atrium gauche, la valve mitrale et l'aorte ascendante."),
    ("Qu'est-ce que le péricarde visible en coupe ?", "L'enveloppe fibro-séreuse qui entoure le cœur, apparaissant comme une fine ligne hyperéchogène."),
    ("Quel rôle joue le septum dans la fonction cardiaque ?", "Il participe à la contraction des deux ventricules et maintient la séparation entre les circulations pulmonaire et systémique."),
    ("Quelle pathologie résulte d'un défaut du septum interventriculaire ?", "La communication interventriculaire (CIV), permettant un shunt gauche-droit."),
    ("Quelle pathologie résulte d'un défaut du septum interatrial ?", "La communication interatriale (CIA), permettant un passage de sang entre les oreillettes."),
    ("Qu'est-ce que le foramen ovale ?", "Une communication entre les deux atriums présente chez le fœtus, normalement fermée après la naissance."),
    ("Qu'est-ce qu'un foramen ovale perméable ?", "La persistance d'une communication entre les deux atriums après la naissance (présent chez ~25% de la population adulte)."),
    ("Comment le sang fœtal contourne-t-il les poumons ?", "Par le foramen ovale (sang de la VCI vers l'atrium gauche) et le canal artériel (tronc pulmonaire vers l'aorte)."),
    ("Qu'est-ce que le canal artériel ?", "Une communication fœtale entre le tronc pulmonaire et l'aorte, qui se ferme normalement après la naissance."),
    ("Comment s'appelle le ligament résiduel du canal artériel ?", "Le ligament artériel."),
    ("Quel examen de première intention permet d'étudier les coupes du cœur ?", "L'échocardiographie transthoracique (ETT)."),
    ("Quelles sont les incidences standard en échocardiographie ?", "Parasternale grand axe, parasternale petit axe, apicale 4 cavités, apicale 2 cavités, sous-costale."),
    ("En coupe parasternale grand axe, quelles structures sont visibles ?", "VG, VD, atrium gauche, valve mitrale, valve aortique, aorte ascendante, septum interventriculaire."),
    ("En coupe apicale 4 cavités, comment distingue-t-on les ventricules ?", "Le VD est plus trabéculé et la valve tricuspide s'insère plus apicalement que la valve mitrale."),
    ("Quel est l'intérêt des coupes cardiaques en pratique clinique ?", "Évaluer la fonction ventriculaire, rechercher des valvulopathies, mesurer les dimensions des cavités, détecter des anomalies structurelles."),
    ("Qu'est-ce qu'une hypertrophie ventriculaire gauche ?", "Un épaississement anormal de la paroi du VG (>12 mm en diastole), souvent lié à l'HTA ou à une sténose aortique."),
    ("Qu'est-ce qu'une dilatation ventriculaire ?", "Une augmentation anormale du volume d'une cavité cardiaque, souvent liée à une insuffisance valvulaire ou une cardiomyopathie."),
    ("Quel est le rapport normal entre VD et VG en coupe apicale ?", "Le rapport VD/VG est normalement < 0.6 (le VD est plus petit que le VG)."),
    ("Que signifie un rapport VD/VG > 1 ?", "Une dilatation du ventricule droit, pouvant évoquer une embolie pulmonaire ou une HTAP."),
    ("Qu'est-ce que le TAPSE en échocardiographie ?", "Le déplacement systolique du plan de l'anneau tricuspide, reflet de la fonction systolique du VD (normal > 17 mm)."),
    ("Comment mesure-t-on la fraction d'éjection du VG en pratique ?", "Par la méthode de Simpson biplan en échocardiographie, ou par IRM cardiaque."),
    ("Qu'est-ce que la méthode de Simpson biplan ?", "Une méthode de calcul du volume ventriculaire basée sur le tracé des contours endocardiques en coupes apicales 4 et 2 cavités."),
    ("Qu'est-ce que la cardiomyopathie hypertrophique ?", "Une maladie génétique caractérisée par un épaississement asymétrique du myocarde, principalement le septum."),
    ("Qu'est-ce qu'un épanchement péricardique visible en coupe ?", "Un espace anéchogène (noir) entre le péricarde viscéral et pariétal, témoignant de liquide dans la cavité péricardique."),
    ("Quelles sont les limites du médiastin ?", "En haut : orifice supérieur du thorax ; en bas : diaphragme ; latéralement : plèvres médiastinales ; en avant : sternum ; en arrière : colonne vertébrale."),
    ("Qu'est-ce que le médiastin antérieur ?", "La portion du médiastin située en avant du péricarde, contenant du tissu adipeux et le thymus."),
    ("Qu'est-ce que le médiastin postérieur ?", "La portion du médiastin située en arrière du péricarde, contenant l'aorte thoracique descendante, l'œsophage et le canal thoracique."),
    ("Qu'est-ce que le médiastin moyen ?", "La portion du médiastin contenant le cœur et le péricarde."),
    ("Quel est le volume cardiaque normal ?", "Environ 700-800 mL chez l'homme adulte, occupant environ la taille du poing fermé."),
    ("Quel est le poids normal du cœur ?", "Environ 250-350 g chez l'adulte."),
    ("Où se projette le cœur sur la paroi thoracique ?", "Du 2ème au 5ème espace intercostal, entre le bord droit du sternum et la ligne médioclaviculaire gauche."),
    ("À quoi correspond le choc de pointe ?", "L'impact de l'apex du VG contre la paroi thoracique, palpable au 5ème espace intercostal gauche sur la ligne médioclaviculaire."),
    ("Quel est le rôle de l'IRM cardiaque par rapport à l'échocardiographie ?", "L'IRM offre une meilleure résolution spatiale, une visualisation complète du myocarde et permet la caractérisation tissulaire (fibrose, œdème)."),
    ("Quelles pathologies peut-on diagnostiquer grâce aux coupes cardiaques ?", "Cardiopathies congénitales, valvulopathies, cardiomyopathies, insuffisance cardiaque, péricardites, tumeurs cardiaques."),
]

# ============================================================
# COURSE 2: Interaction ligand-récepteur (fc2.html) - ICM
# ============================================================
INTERACTION_LIGAND = [
    ("Qu'est-ce qu'un ligand en pharmacologie ?", "Une molécule capable de se lier à une ou plusieurs cibles déterminées pour produire un effet pharmacologique."),
    ("Que se passe-t-il lors de l'interaction ligand-récepteur ?", "Le ligand (principe actif) rencontre sa cible, s'y lie, ce qui déclenche une cascade d'événements menant à une réponse biologique = effet pharmacologique."),
    ("Quelles sont les deux types de conséquences d'une liaison ligand-récepteur ?", "L'effet pharmacologique recherché (base de l'effet thérapeutique) et l'effet délétère (base des effets indésirables ou toxiques)."),
    ("Qu'est-ce qu'un effet pharmacologique recherché ?", "L'effet bénéfique sur la pathologie, constituant la base de l'effet thérapeutique du médicament."),
    ("Qu'est-ce qu'un effet délétère en pharmacologie ?", "Un effet qui constitue la base des effets indésirables, secondaires ou toxiques du médicament."),
    ("Quels sont les deux résultats possibles de l'interaction ligand-récepteur ?", "L'activation de la cible (mimant l'effet d'une molécule endogène) ou l'inhibition de la cible (réduisant l'activité du système ciblé)."),
    ("Qu'est-ce que l'activation d'une cible par un ligand ?", "Le ligand mime tout ou partie de l'effet d'une molécule endogène qui se lie physiologiquement à cette cible."),
    ("Qu'est-ce que l'inhibition d'une cible par un ligand ?", "Le ligand réduit l'activité du système ciblé et empêche l'action des molécules endogènes."),
    ("Qu'est-ce qu'une molécule endogène ?", "Une molécule produite naturellement par l'organisme (ex : adrénaline, dopamine, sérotonine)."),
    ("Qu'est-ce qu'une molécule exogène ?", "Une molécule qui n'existe pas dans l'organisme, le plus souvent issue de la synthèse chimique."),
    ("Donnez un exemple de molécule endogène utilisée comme médicament.", "L'adrénaline : médiateur endogène qui peut être administré par voie IV en injection exogène."),
    ("D'où proviennent la majorité des médicaments ?", "Ce sont des molécules exogènes issues de la synthèse chimique, capables d'interagir avec des cibles endogènes."),
    ("Qu'est-ce qu'un second messager ?", "Une molécule endogène synthétisée ou libérée suite à l'interaction ligand-récepteur, qui transmet et amplifie le message du ligand dans la cellule."),
    ("Quel est le rôle des seconds messagers ?", "Porter le message du ligand à l'intérieur de la cellule et servir d'amplificateurs (un ligand induit la libération de nombreux seconds messagers)."),
    ("Qu'est-ce que la constante de dissociation (Kd) ?", "La constante mesurant l'intensité de la liaison ligand-récepteur : plus le Kd est petit, plus la liaison est forte."),
    ("Comment interprète-t-on un Kd faible ?", "Un Kd faible signifie une affinité élevée du ligand pour le récepteur (liaison forte)."),
    ("Comment interprète-t-on un Kd élevé ?", "Un Kd élevé signifie une affinité faible du ligand pour le récepteur (liaison faible)."),
    ("Quelle est la différence entre spécificité et sélectivité ?", "La spécificité est l'interaction unique entre un ligand et un récepteur (clé-serrure), la sélectivité est la préférence de liaison du ligand pour certains récepteurs basée sur l'affinité."),
    ("Comment définit-on la spécificité d'un ligand ?", "C'est le caractère unique de l'interaction ligand-récepteur, comme une clé avec sa serrure. Elle est indépendante du nombre de cibles."),
    ("Comment définit-on la sélectivité d'un ligand ?", "C'est la préférence de liaison d'un ligand pour un ou plusieurs récepteurs, basée sur l'affinité différentielle pour ces cibles."),
    ("Un ligand peut-il interagir avec plusieurs récepteurs ?", "Oui, souvent un même ligand interagit avec plusieurs récepteurs. Chaque liaison est spécifique, mais la sélectivité dépend de l'affinité."),
    ("Qu'est-ce que la théorie de l'occupation des récepteurs ?", "Plus la quantité de médicament administrée est grande, plus le nombre de récepteurs occupés augmente, entraînant une augmentation de l'intensité de l'effet."),
    ("La spécificité dépend-elle de la dose ?", "Non, la spécificité reste la même quelle que soit la dose, car elle dépend de la nature intrinsèque de l'interaction ligand-cible."),
    ("La sélectivité dépend-elle de la dose ?", "Oui, la sélectivité est modifiée par la dose. Augmenter la dose peut entraîner une perte de sélectivité."),
    ("Que se passe-t-il quand le différentiel d'affinité entre récepteurs est très grand ?", "La sélectivité est peu affectée par l'augmentation de dose, le ligand reste préférentiellement sur le récepteur de haute affinité."),
    ("Que se passe-t-il quand le différentiel d'affinité entre récepteurs est faible ?", "Augmenter la dose entraîne une perte de sélectivité : le ligand se fixe de plus en plus sur les récepteurs secondaires."),
    ("Quelle est la conséquence clinique d'une perte de sélectivité ?", "L'apparition d'effets indésirables liés à la fixation du ligand sur des récepteurs non ciblés."),
    ("Qu'est-ce qu'un agoniste ?", "Un ligand qui se fixe sur un récepteur et l'active, reproduisant l'effet de la molécule endogène."),
    ("Qu'est-ce qu'un antagoniste ?", "Un ligand qui se fixe sur un récepteur sans l'activer, bloquant l'action des agonistes endogènes ou exogènes."),
    ("Qu'est-ce qu'un agoniste partiel ?", "Un ligand qui active le récepteur mais ne peut pas produire l'effet maximal, même à forte concentration."),
    ("Qu'est-ce qu'un agoniste complet ?", "Un ligand capable de produire l'effet maximal en occupant tous les récepteurs disponibles."),
    ("Qu'est-ce qu'un agoniste inverse ?", "Un ligand qui se fixe sur un récepteur constitutivement actif et diminue son activité basale."),
    ("Comment l'affinité influence-t-elle l'effet thérapeutique ?", "Plus l'affinité d'un médicament pour sa cible est forte (Kd faible), plus il est efficace à faible dose."),
    ("Qu'est-ce que la puissance d'un médicament ?", "La capacité d'un médicament à produire un effet à faible dose. Plus la dose nécessaire est faible, plus le médicament est puissant."),
    ("Qu'est-ce que l'efficacité d'un médicament ?", "L'intensité maximale de l'effet qu'un médicament peut produire (Emax), indépendamment de la dose utilisée."),
    ("Quelle est la relation entre dose et effet ?", "L'effet augmente avec la dose selon une courbe sigmoïde, jusqu'à atteindre un plateau correspondant à l'effet maximal."),
    ("Pourquoi l'effet d'un médicament atteint-il un plateau ?", "Car le nombre de récepteurs disponibles est limité, ou les voies de signalisation intracellulaires sont saturées."),
    ("Qu'est-ce que la DE50 ?", "La dose efficace 50% : la dose provoquant la moitié de l'effet maximal du médicament."),
    ("Qu'est-ce que la CE50 ?", "La concentration efficace 50% : la concentration provoquant la moitié de l'effet maximal (utilisée in vitro)."),
    ("Qu'est-ce qu'une courbe dose-réponse ?", "La représentation graphique de la relation entre la dose d'un médicament et l'intensité de l'effet produit."),
    ("Pourquoi utilise-t-on des coordonnées semi-logarithmiques ?", "Pour transformer la courbe dose-réponse en sigmoïde, facilitant la détermination de DE50 et Emax."),
    ("Qu'est-ce qu'une liaison réversible ligand-récepteur ?", "Une liaison où le ligand peut se dissocier du récepteur, permettant un équilibre entre forme libre et complexe ligand-récepteur."),
    ("Qu'est-ce qu'une liaison irréversible ligand-récepteur ?", "Une liaison permanente où le ligand ne se dissocie pas du récepteur, bloquant définitivement la cible."),
    ("Comment l'augmentation de dose affecte-t-elle la fixation sur les récepteurs ?", "Elle augmente le nombre de récepteurs occupés et peut entraîner une fixation sur des récepteurs secondaires (perte de sélectivité)."),
    ("Qu'est-ce que la pharmacodynamie ?", "L'étude de l'effet des médicaments sur l'organisme (ce que le médicament fait au corps)."),
    ("Qu'est-ce que la pharmacocinétique ?", "L'étude du devenir du médicament dans l'organisme : absorption, distribution, métabolisme, élimination (ce que le corps fait au médicament)."),
    ("Qu'est-ce qu'un récepteur en pharmacologie ?", "Une macromolécule cellulaire (protéine) capable de reconnaître et de lier un ligand de manière spécifique, déclenchant une réponse cellulaire."),
    ("Où peuvent se situer les récepteurs ?", "À la surface des cellules (récepteurs membranaires) ou à l'intérieur des cellules (récepteurs intracellulaires/nucléaires)."),
    ("Quels sont les principaux types de récepteurs membranaires ?", "Les récepteurs couplés aux protéines G (RCPG), les récepteurs-canaux ioniques, les récepteurs à activité enzymatique (tyrosine kinase)."),
    ("Qu'est-ce qu'un récepteur couplé aux protéines G (RCPG) ?", "Un récepteur à 7 domaines transmembranaires qui, une fois activé, active une protéine G intracellulaire déclenchant une cascade de signalisation."),
    ("Qu'est-ce qu'un récepteur-canal ionique ?", "Un récepteur qui, lorsqu'il est activé par un ligand, ouvre un canal permettant le passage d'ions à travers la membrane."),
    ("Qu'est-ce qu'un récepteur à activité tyrosine kinase ?", "Un récepteur dont l'activation entraîne la phosphorylation de protéines intracellulaires sur des résidus tyrosine."),
    ("Qu'est-ce qu'un récepteur nucléaire ?", "Un récepteur intracellulaire qui, une fois activé par son ligand, agit comme facteur de transcription modifiant l'expression des gènes."),
    ("Donnez des exemples de seconds messagers.", "AMPc, GMPc, IP3, DAG, Ca2+."),
    ("Qu'est-ce que l'AMPc ?", "L'adénosine monophosphate cyclique, un second messager produit par l'adénylate cyclase suite à l'activation d'un RCPG."),
    ("Quel rôle joue le calcium comme second messager ?", "Le Ca2+ intracellulaire active de nombreuses enzymes (kinases, phosphatases) et participe à la contraction musculaire, la sécrétion et l'exocytose."),
    ("Qu'est-ce que la transduction du signal ?", "L'ensemble des mécanismes par lesquels la liaison d'un ligand à son récepteur est convertie en réponse cellulaire."),
    ("Qu'est-ce que l'amplification du signal ?", "Le phénomène par lequel un seul ligand, via les seconds messagers, active un grand nombre de molécules effectrices dans la cellule."),
    ("Qu'est-ce que la désensibilisation d'un récepteur ?", "La diminution de la réponse d'un récepteur malgré la présence continue du ligand (tolérance pharmacodynamique)."),
    ("Qu'est-ce que la régulation à la baisse (down-regulation) ?", "La diminution du nombre de récepteurs à la surface cellulaire après une exposition prolongée à un agoniste."),
    ("Qu'est-ce que la régulation à la hausse (up-regulation) ?", "L'augmentation du nombre de récepteurs après une exposition prolongée à un antagoniste."),
    ("Qu'est-ce que l'index thérapeutique ?", "Le rapport entre la dose toxique 50% (DT50) et la dose efficace 50% (DE50). Plus il est grand, plus le médicament est sûr."),
    ("Qu'est-ce que la marge thérapeutique ?", "L'intervalle entre la concentration minimale efficace et la concentration minimale toxique d'un médicament."),
    ("Un médicament à marge thérapeutique étroite nécessite-t-il une surveillance particulière ?", "Oui, car de faibles variations de dose peuvent entraîner soit une inefficacité soit une toxicité."),
    ("Citez des exemples de médicaments à marge thérapeutique étroite.", "Anticoagulants anti-vitamine K (warfarine), antiépileptiques (phénytoïne), digitaliques (digoxine), lithium, théophylline."),
    ("Qu'est-ce que la relation structure-activité ?", "L'étude du lien entre la structure chimique d'une molécule et son activité pharmacologique, permettant de concevoir de nouveaux médicaments."),
    ("Comment la modification structurale d'un ligand peut-elle affecter son activité ?", "Elle peut modifier l'affinité, la sélectivité, la puissance, l'efficacité ou les propriétés pharmacocinétiques."),
    ("Qu'est-ce que le phénomène de tolérance ?", "La nécessité d'augmenter progressivement la dose d'un médicament pour obtenir le même effet thérapeutique."),
    ("Qu'est-ce que la tachyphylaxie ?", "Une forme rapide de tolérance qui s'installe après quelques administrations seulement."),
    ("Comment la densité de récepteurs influence-t-elle l'effet d'un médicament ?", "Plus il y a de récepteurs disponibles, plus l'effet potentiel est important (récepteurs de réserve)."),
    ("Qu'est-ce qu'un récepteur de réserve ?", "Des récepteurs qui ne sont pas nécessaires pour obtenir l'effet maximal. L'Emax peut être atteint sans occuper 100% des récepteurs."),
    ("Comment mesure-t-on l'affinité d'un ligand pour un récepteur ?", "Par des études de liaison (binding) utilisant des ligands radiomarqués et la détermination du Kd."),
    ("Qu'est-ce qu'une étude de binding ?", "Une expérience in vitro utilisant un ligand radiomarqué pour mesurer l'affinité et le nombre de sites de liaison d'un récepteur."),
    ("Qu'est-ce que la liaison spécifique ?", "La liaison du ligand à son récepteur cible, saturable et déplaçable par un excès de ligand non marqué."),
    ("Qu'est-ce que la liaison non spécifique ?", "La liaison du ligand à des sites non récepteurs, non saturable et proportionnelle à la concentration."),
    ("Qu'est-ce qu'un ligand allostérique ?", "Un ligand qui se fixe sur un site différent du site orthostérique (site de liaison de l'agoniste endogène), modulant la réponse du récepteur."),
    ("Qu'est-ce que le site orthostérique ?", "Le site principal de liaison du ligand endogène sur un récepteur."),
    ("Qu'est-ce qu'un modulateur allostérique positif ?", "Un ligand qui augmente l'affinité ou l'efficacité de l'agoniste endogène en se fixant sur le site allostérique."),
    ("Qu'est-ce qu'un modulateur allostérique négatif ?", "Un ligand qui diminue l'affinité ou l'efficacité de l'agoniste endogène en se fixant sur le site allostérique."),
    ("Qu'est-ce que l'activité constitutive d'un récepteur ?", "L'activité basale d'un récepteur en l'absence de tout ligand, pouvant générer un signal intracellulaire minimal."),
    ("Qu'est-ce que l'efficacité intrinsèque ?", "La capacité d'un ligand à activer un récepteur une fois lié. Un agoniste complet a une efficacité maximale, un antagoniste a une efficacité nulle."),
    ("Quelle est la différence entre affinité et efficacité intrinsèque ?", "L'affinité mesure la force de liaison au récepteur (Kd), l'efficacité intrinsèque mesure la capacité à activer le récepteur une fois lié."),
    ("Comment un médicament peut-il avoir une forte affinité mais pas d'effet ?", "C'est le cas d'un antagoniste : il se fixe fortement au récepteur (forte affinité) mais ne l'active pas (efficacité intrinsèque nulle)."),
    ("Qu'est-ce que l'effet placebo ?", "Un effet thérapeutique observé après administration d'un traitement dépourvu de principe actif, lié à des mécanismes psychologiques et neurobiologiques."),
    ("Qu'est-ce que l'effet nocebo ?", "L'apparition d'effets indésirables après administration d'un traitement inactif, liée aux attentes négatives du patient."),
    ("Pourquoi compare-t-on un médicament à un placebo dans les essais cliniques ?", "Pour distinguer l'effet pharmacologique réel du médicament de l'effet placebo."),
    ("Qu'est-ce que la fenêtre thérapeutique ?", "La zone de concentrations plasmatiques comprise entre le seuil d'efficacité et le seuil de toxicité."),
    ("Qu'est-ce qu'un effet dose-dépendant ?", "Un effet dont l'intensité augmente proportionnellement à la dose administrée."),
    ("Qu'est-ce qu'un antagoniste fonctionnel ?", "Un ligand qui produit un effet opposé à celui d'un agoniste mais en agissant sur un récepteur ou une voie différente."),
    ("Qu'est-ce que la synergie additive ?", "L'effet combiné de deux médicaments est égal à la somme de leurs effets individuels."),
    ("Qu'est-ce que la potentialisation ?", "Un médicament augmente l'effet d'un autre au-delà de la simple addition."),
    ("Qu'est-ce que le polymorphisme des récepteurs ?", "Les variations génétiques des récepteurs entre individus, pouvant entraîner des différences de réponse aux médicaments."),
    ("Comment le polymorphisme génétique influence-t-il la pharmacologie ?", "Il peut modifier l'affinité des récepteurs pour les ligands, l'efficacité de la transduction du signal, ou le métabolisme des médicaments."),
]

# Due to size constraints, I'll define remaining courses inline
# Let me write all courses and execute

COURSES_DATA = {
    "Circulation_Respiration/Anatomie/fc9.html": COUPES_COEUR,
    "ICM/fc2.html": INTERACTION_LIGAND,
}

# I'll generate the remaining 14 courses now
