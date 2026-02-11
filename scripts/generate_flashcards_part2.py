#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer ~100 flashcards - Partie 2 (Histologie et Métabolisme AA)
"""

import os
import re

BASE_DIR = "/Users/cyrilwisa/Desktop/diploma/USPN_S2"

# =============================================================================
# FLASHCARDS APPAREIL CARDIOVASCULAIRE
# =============================================================================
FLASHCARDS_APPAREIL_CARDIO = [
    # I. Introduction
    { "question": "Quel est le rôle de l'appareil cardiovasculaire ?", "answer": "Assurer la circulation du sang pour l'apport d'O2 et nutriments, l'élimination des déchets." },
    { "question": "Quels sont les constituants de l'appareil cardiovasculaire ?", "answer": "Le cœur (pompe), les artères, les veines, les capillaires." },
    { "question": "Qu'est-ce que la grande circulation ?", "answer": "Circulation systémique : cœur gauche → tissus → cœur droit." },
    { "question": "Qu'est-ce que la petite circulation ?", "answer": "Circulation pulmonaire : cœur droit → poumons → cœur gauche." },
    { "question": "Quelle est la structure générale de la paroi vasculaire ?", "answer": "Trois tuniques concentriques : intima, média, adventice." },
    
    # II. Les tuniques vasculaires
    { "question": "Qu'est-ce que l'intima ?", "answer": "Tunique interne en contact avec le sang, constituée de l'endothélium et de la couche sous-endothéliale." },
    { "question": "Qu'est-ce que l'endothélium ?", "answer": "Épithélium simple pavimenteux (cellules aplaties avec noyau en saillie), reposant sur une lame basale." },
    { "question": "Quels sont les rôles de l'endothélium ?", "answer": "Barrière semi-perméable, régulation vasomotricité, anti-coagulation, synthèse de substances vasoactives." },
    { "question": "Que contient la couche sous-endothéliale ?", "answer": "Tissu conjonctif lâche avec fibres de collagène, élastiques, et quelques fibres musculaires lisses." },
    { "question": "Qu'est-ce que la média ?", "answer": "Tunique moyenne la plus épaisse, constituée de cellules musculaires lisses, fibres élastiques et collagène." },
    { "question": "Quel est le rôle de la média ?", "answer": "Assurer l'élasticité (fibres élastiques) et la vasomotricité (fibres musculaires lisses)." },
    { "question": "Qu'est-ce que l'adventice ?", "answer": "Tunique externe de tissu conjonctif fibreux dense, contenant nerfs et vasa vasorum." },
    { "question": "Que sont les vasa vasorum ?", "answer": "Petits vaisseaux sanguins irriguant la paroi des gros vaisseaux." },
    { "question": "Qu'est-ce que la limitante élastique interne (LEI) ?", "answer": "Lame élastique festonnée séparant l'intima de la média, avec fenestrations." },
    { "question": "Qu'est-ce que la limitante élastique externe (LEE) ?", "answer": "Lame élastique séparant la média de l'adventice, moins bien définie que la LEI." },
    
    # III. Les artères
    { "question": "Quels sont les deux types d'artères ?", "answer": "Artères élastiques (gros calibre) et artères musculaires (moyen et petit calibre)." },
    { "question": "Citez des exemples d'artères élastiques.", "answer": "Aorte, tronc brachio-céphalique, carotides, sous-clavières, iliaques, pulmonaires." },
    { "question": "Quel est le diamètre des artères élastiques ?", "answer": "De 25 mm (aorte à l'origine) à 10 mm." },
    { "question": "Comment est l'intima des artères élastiques ?", "answer": "Épaisse avec endothélium, couche sous-endothéliale bien développée (tissu conjonctif, fibres musculaires lisses)." },
    { "question": "Comment est la média des artères élastiques ?", "answer": "Très épaisse avec unités lamellaires (lames élastiques fenêtrées + cellules musculaires lisses)." },
    { "question": "Combien de lames élastiques compte l'aorte ?", "answer": "40 à 70 lames élastiques concentriques." },
    { "question": "Quel est le rôle des artères élastiques ?", "answer": "Amortir l'onde systolique et transformer un flux discontinu en flux continu." },
    { "question": "Qu'est-ce qu'une artère musculaire ?", "answer": "Artère de distribution avec média riche en cellules musculaires lisses." },
    { "question": "Quel est le diamètre des artères musculaires ?", "answer": "De 1 mm à 10 mm." },
    { "question": "Comment est l'intima des artères musculaires ?", "answer": "Mince avec LEI bien visible, festonnée et réfringente." },
    { "question": "Comment est la média des artères musculaires ?", "answer": "Épaisse, constituée de cellules musculaires lisses en couches concentriques (5 à 40 couches)." },
    { "question": "Quel est le rôle des artères musculaires ?", "answer": "Distribuer le sang aux organes et réguler la pression par vasomotricité." },
    
    # IV. Les artérioles
    { "question": "Quel est le diamètre des artérioles ?", "answer": "Inférieur à 1 mm (jusqu'à 30 μm pour les métartérioles)." },
    { "question": "Quelle est la structure de la paroi artériolaire ?", "answer": "Endothélium + 1 à 3 couches de cellules musculaires lisses, peu d'adventice." },
    { "question": "Quel est le rôle des artérioles ?", "answer": "Vaisseaux de résistance régulant la pression artérielle." },
    { "question": "Qu'est-ce qu'une métartériole ?", "answer": "Artériole terminale à paroi discontinue de cellules musculaires lisses (sphincters précapillaires)." },
    
    # V. Les capillaires
    { "question": "Quelles sont les dimensions des capillaires ?", "answer": "Diamètre 7-10 μm, longueur 0,5-1 mm." },
    { "question": "Quelle est la structure de la paroi capillaire ?", "answer": "Endothélium seul avec lame basale, pas de média ni d'adventice." },
    { "question": "Quels sont les 3 types de capillaires ?", "answer": "Capillaires continus, fenêtrés, discontinus (sinusoïdes)." },
    { "question": "Où trouve-t-on les capillaires continus ?", "answer": "Muscles, tissu nerveux, tissu conjonctif, poumons." },
    { "question": "Qu'est-ce qu'un capillaire fenêtré ?", "answer": "Capillaire avec des pores (fenestrations) de 50-80 nm, obturés ou non par un diaphragme." },
    { "question": "Où trouve-t-on les capillaires fenêtrés ?", "answer": "Glandes endocrines, tube digestif, rein (glomérule)." },
    { "question": "Qu'est-ce qu'un capillaire sinusoïde ?", "answer": "Capillaire discontinu avec orifices larges et lame basale discontinue." },
    { "question": "Où trouve-t-on les sinusoïdes ?", "answer": "Foie, rate, moelle osseuse." },
    { "question": "Qu'est-ce qu'un péricyte ?", "answer": "Cellule contractile entourant les capillaires, impliquée dans la régulation du flux sanguin." },
    
    # VI. Les veines
    { "question": "Quels sont les 3 types de veines ?", "answer": "Veinules, veines de moyen calibre, veines de gros calibre." },
    { "question": "Quel est le diamètre des veinules ?", "answer": "10 à 200 μm (veinules postcapillaires: 10-50 μm, veinules musculaires: 50-200 μm)." },
    { "question": "Quelle est la fonction des veinules postcapillaires ?", "answer": "Site privilégié des échanges et de la diapédèse leucocytaire." },
    { "question": "Quel est le diamètre des veines de moyen calibre ?", "answer": "1 à 10 mm." },
    { "question": "Comment est la paroi des veines de moyen calibre ?", "answer": "Fine avec intima mince, média peu développée, adventice épaisse." },
    { "question": "Que possèdent les veines des membres inférieurs ?", "answer": "Des valvules anti-reflux (replis de l'intima)." },
    { "question": "Comment est la paroi des veines de gros calibre ?", "answer": "Intima mince, média peu développée, adventice très épaisse avec fibres musculaires lisses longitudinales." },
    { "question": "Citez des exemples de veines de gros calibre.", "answer": "Veines caves supérieure et inférieure, veines jugulaires, veine porte." },
    
    # VII. Structures particulières
    { "question": "Qu'est-ce qu'un glomus artério-veineux ?", "answer": "Anastomose artério-veineuse sans capillaires, régulant la température (doigts, orteils, lèvres)." },
    { "question": "Qu'est-ce qu'un sinus veineux ?", "answer": "Veine à paroi fine sans cellules musculaires, enchâssée dans un tissu (ex: sinus dure-mère)." },
    { "question": "Qu'est-ce qu'un système porte ?", "answer": "Système veineux interposé entre deux réseaux capillaires (ex: système porte hépatique)." },
    { "question": "Qu'est-ce qu'un corps caverneux ?", "answer": "Réseau de sinus veineux anastomosés entourés de tissu conjonctif et fibres musculaires lisses." },
    
    # VIII. Vaisseaux lymphatiques
    { "question": "Quel est le rôle du système lymphatique ?", "answer": "Drainage de la lymphe et transport des lipides absorbés par l'intestin." },
    { "question": "Quelle est la structure des capillaires lymphatiques ?", "answer": "Endothélium discontinu sans lame basale, jonctions ouvertes, filaments d'ancrage au collagène." },
    { "question": "Où commencent les capillaires lymphatiques ?", "answer": "En cul-de-sac dans les tissus." },
    { "question": "Quelle est la structure des vaisseaux lymphatiques ?", "answer": "Paroi mince avec média peu développée, nombreuses valvules." },
    { "question": "Où se draine le canal thoracique ?", "answer": "Dans la veine sous-clavière gauche." },
    
    # IX. Le cœur
    { "question": "Quelles sont les 3 tuniques du cœur ?", "answer": "Endocarde, myocarde, épicarde." },
    { "question": "Qu'est-ce que l'endocarde ?", "answer": "Tunique interne comparable à l'intima vasculaire (endothélium + tissu sous-endothélial)." },
    { "question": "De quoi est formé le myocarde ?", "answer": "Tissu musculaire strié cardiaque avec cardiomyocytes connectés par disques intercalaires." },
    { "question": "Quelle est l'épaisseur du myocarde ventriculaire gauche ?", "answer": "10-15 mm (3 fois plus épais que le droit)." },
    { "question": "Qu'est-ce que l'épicarde ?", "answer": "Feuillet viscéral du péricarde séreux, recouvert de mésothélium." },
    { "question": "De quoi est constitué le squelette fibreux du cœur ?", "answer": "Tissu conjonctif dense formant les anneaux fibreux valvulaires et les trigones." },
    { "question": "Quel est le rôle du squelette fibreux ?", "answer": "Isoler électriquement les oreillettes des ventricules et servir d'insertion aux valves." },
    { "question": "Quelle est la structure des valves cardiaques ?", "answer": "Replis d'endocarde avec une charpente de tissu conjonctif dense." },
    { "question": "Qu'est-ce que le tissu nodal ?", "answer": "Système cardionecteur générant et propageant l'activité électrique (pacemaker)." },
    { "question": "Quels sont les éléments du tissu nodal ?", "answer": "Nœud sino-atrial (Keith et Flack), nœud atrio-ventriculaire (Aschoff-Tawara), faisceau de His, réseau de Purkinje." },
    { "question": "Où se situe le nœud sinusal ?", "answer": "À la jonction entre la veine cave supérieure et l'oreillette droite." },
    { "question": "Quelle est la fréquence intrinsèque du nœud sinusal ?", "answer": "70-80 battements par minute." },
    { "question": "Que sont les cellules de Purkinje ?", "answer": "Cardiomyocytes modifiés de grande taille transmettant l'excitation aux cardiomyocytes contractiles." },
    
    # Pathologies
    { "question": "Qu'est-ce que l'athérosclérose ?", "answer": "Dépôt de lipides (plaques d'athérome) dans l'intima des artères élastiques et musculaires." },
    { "question": "Qu'est-ce qu'un anévrisme ?", "answer": "Dilatation localisée de la paroi artérielle par altération de la média." },
    { "question": "Qu'est-ce qu'une varice ?", "answer": "Dilatation permanente d'une veine superficielle avec insuffisance valvulaire." },
    { "question": "Qu'est-ce qu'une phlébite ?", "answer": "Inflammation de la paroi veineuse, souvent associée à une thrombose." },
]

# =============================================================================
# FLASHCARDS MÉTABOLISME DES ACIDES AMINÉS
# =============================================================================
FLASHCARDS_METABOLISME_AA = [
    # I. Introduction
    { "question": "Combien d'AA protéinogènes existe-t-il ?", "answer": "20 acides aminés standards incorporés dans les protéines." },
    { "question": "Qu'est-ce qu'un acide aminé indispensable ?", "answer": "AA que l'organisme ne peut pas synthétiser, devant être apporté par l'alimentation." },
    { "question": "Quels sont les 8 AA indispensables chez l'adulte ?", "answer": "Isoleucine, Leucine, Lysine, Méthionine, Phénylalanine, Thréonine, Tryptophane, Valine." },
    { "question": "Quels sont les 2 AA indispensables supplémentaires chez l'enfant ?", "answer": "Arginine et Histidine." },
    { "question": "Comment retenir les AA indispensables ?", "answer": "'Le très lyrique Tristan fait vachement méditer Iseult' (Leu, Thr, Lys, Trp, Phe, Val, Met, Ile)." },
    { "question": "Quelles sont les fonctions des AA ?", "answer": "Synthèse protéique, production d'énergie, précurseurs de molécules bioactives." },
    { "question": "Quel est le pool d'AA libre de l'organisme ?", "answer": "70 g, dont 1/4 dans le plasma." },
    { "question": "Comment varie le pool d'AA libre ?", "answer": "Peu de variations grâce au foie qui régule l'homéostasie des AA." },
    
    # II. Sources et devenir des AA
    { "question": "Quelles sont les 3 sources d'AA pour le pool libre ?", "answer": "Alimentation (digestion protéique), synthèse de novo, catabolisme des protéines endogènes." },
    { "question": "Quels sont les 3 devenirs des AA du pool libre ?", "answer": "Synthèse protéique, catabolisme oxydatif, synthèse de molécules dérivées." },
    { "question": "Quel est le turnover protéique quotidien ?", "answer": "300-400 g de protéines sont synthétisées et dégradées chaque jour." },
    { "question": "Quelle est la demie-vie de l'hémoglobine ?", "answer": "120 jours." },
    { "question": "Quelle est la demie-vie du collagène ?", "answer": "300 jours." },
    { "question": "Quelle est la demie-vie de l'ornithine décarboxylase ?", "answer": "11 minutes (la plus courte)." },
    
    # III. Digestion et absorption
    { "question": "Quelles enzymes digèrent les protéines dans l'estomac ?", "answer": "Pepsine (et HCl pour dénaturation)." },
    { "question": "Quelles enzymes pancréatiques digèrent les protéines ?", "answer": "Trypsine, chymotrypsine, élastase, carboxypeptidases A et B." },
    { "question": "Quelles enzymes intestinales complètent la digestion ?", "answer": "Aminopeptidases et dipeptidases de la bordure en brosse." },
    { "question": "Sous quelle forme les produits de digestion sont-ils absorbés ?", "answer": "AA libres, dipeptides et tripeptides." },
    { "question": "Comment sont transportés les AA dans l'entérocyte ?", "answer": "Par des transporteurs spécifiques couplés au Na+ (cotransport actif secondaire)." },
    { "question": "Combien de transporteurs d'AA existe-t-il ?", "answer": "Au moins 7 transporteurs avec spécificité de groupe." },
    { "question": "Comment les dipeptides sont-ils absorbés ?", "answer": "Par le transporteur PepT1, couplé au gradient de H+." },
    
    # IV. Catabolisme des AA
    { "question": "Quels sont les produits du catabolisme des AA ?", "answer": "NH4+ (ammoniaque), squelette carboné, CO2, H2O, énergie." },
    { "question": "Pourquoi l'ammoniaque est-il toxique ?", "answer": "Il est neurotoxique et doit être éliminé sous forme d'urée." },
    { "question": "Comment s'appellent les réactions de transfert du groupement aminé ?", "answer": "Transaminations, catalysées par des aminotransférases." },
    { "question": "Quel est le coenzyme des aminotransférases ?", "answer": "Le phosphate de pyridoxal (PLP), forme active de la vitamine B6." },
    { "question": "Quelles sont les 2 aminotransférases les plus importantes ?", "answer": "ASAT (GOT) et ALAT (GPT)." },
    { "question": "Quel AA reçoit le groupement aminé lors des transaminations ?", "answer": "L'α-cétoglutarate qui devient glutamate." },
    { "question": "Qu'est-ce que la désamination oxydative ?", "answer": "Libération de NH4+ à partir du glutamate par la glutamate déshydrogénase." },
    { "question": "Où a lieu principalement la désamination oxydative ?", "answer": "Dans le foie (mitochondries)." },
    { "question": "Quel est le destin de l'ammoniaque hépatique ?", "answer": "Incorporation dans l'urée (cycle de l'urée)." },
    { "question": "Qu'est-ce que l'uréogenèse ?", "answer": "Cycle de l'urée : synthèse de l'urée à partir de 2 NH4+ et du CO2." },
    { "question": "Où se déroule le cycle de l'urée ?", "answer": "Dans les hépatocytes (mitochondrie et cytosol)." },
    { "question": "Quelle est la formule de l'urée ?", "answer": "CO(NH2)2, contenant 2 atomes d'azote." },
    { "question": "Quelle enzyme initie le cycle de l'urée ?", "answer": "La carbamyl-phosphate synthétase I (CPS I), mitochondriale." },
    { "question": "Quels sont les intermédiaires du cycle de l'urée ?", "answer": "Carbamyl-phosphate, citrulline, argininosuccinate, arginine, ornithine." },
    { "question": "Quelle enzyme produit l'urée ?", "answer": "L'arginase, qui hydrolyse l'arginine en urée + ornithine." },
    { "question": "Comment les tissus périphériques éliminent-ils l'ammoniaque ?", "answer": "Par la glutamine synthétase : glutamate + NH4+ → glutamine." },
    { "question": "Quel est le rôle de la glutamine ?", "answer": "Transport non toxique de l'ammoniaque vers le foie et les reins." },
    { "question": "Quel est le destin de la glutamine rénale ?", "answer": "Libération de NH4+ excrété dans l'urine (régulation acido-basique)." },
    
    # V. Squelettes carbonés
    { "question": "Qu'est-ce qu'un AA glucoformateur ?", "answer": "AA dont le squelette carboné peut être converti en glucose (néoglucogenèse)." },
    { "question": "Qu'est-ce qu'un AA cétoformateur ?", "answer": "AA dont le squelette carboné donne des corps cétoniques (acétyl-CoA)." },
    { "question": "Combien d'AA sont uniquement glucoformateurs ?", "answer": "14 AA sont strictement glucoformateurs." },
    { "question": "Quels AA sont uniquement cétoformateurs ?", "answer": "Leucine et Lysine." },
    { "question": "Quels AA sont à la fois gluco- et cétoformateurs ?", "answer": "Isoleucine, Phénylalanine, Tryptophane, Tyrosine." },
    { "question": "Quels intermédiaires proviennent du catabolisme des AA ?", "answer": "Pyruvate, acétyl-CoA, α-cétoglutarate, succinyl-CoA, fumarate, oxaloacétate." },
    
    # VI. Synthèse de molécules dérivées
    { "question": "Quels neurotransmetteurs dérivent des AA ?", "answer": "Sérotonine (Trp), dopamine et catécholamines (Tyr), GABA (Glu), histamine (His)." },
    { "question": "De quel AA dérive la sérotonine ?", "answer": "Du tryptophane, via le 5-hydroxytryptophane." },
    { "question": "De quel AA dérivent les catécholamines ?", "answer": "De la tyrosine : dopamine → noradrénaline → adrénaline." },
    { "question": "De quel AA dérive le monoxyde d'azote (NO) ?", "answer": "De l'arginine, par la NO synthase." },
    { "question": "De quel AA dérive la créatine ?", "answer": "De l'arginine, la glycine et la méthionine." },
    { "question": "Qu'est-ce que la créatine ?", "answer": "Réservoir d'énergie musculaire sous forme de phosphocréatine." },
    { "question": "De quoi dérivent les bases puriques et pyrimidiques ?", "answer": "Glutamine, glycine, aspartate fournissent les atomes du cycle." },
    { "question": "De quoi dérive l'hème ?", "answer": "De la glycine et du succinyl-CoA." },
    { "question": "Qu'est-ce que le glutathion ?", "answer": "Tripeptide antioxydant (Glu-Cys-Gly) protégeant les cellules du stress oxydatif." },
    { "question": "Qu'est-ce que la mélanine ?", "answer": "Pigment cutané dérivé de la tyrosine." },
    { "question": "Qu'est-ce que la mélatonine ?", "answer": "Hormone du sommeil dérivée du tryptophane." },
    { "question": "Qu'est-ce que les hormones thyroïdiennes ?", "answer": "T3 et T4, dérivées de la tyrosine iodée." },
    
    # VII. Régulation du métabolisme
    { "question": "Comment varie le métabolisme des AA selon l'état nutritionnel ?", "answer": "À jeun : catabolisme accru ; en période post-prandiale : synthèse protéique favorisée." },
    { "question": "Quel est l'effet de l'insuline sur le métabolisme des AA ?", "answer": "Favorise la captation des AA et la synthèse protéique." },
    { "question": "Quel est l'effet du glucagon sur le métabolisme des AA ?", "answer": "Favorise le catabolisme des AA et l'uréogenèse." },
    { "question": "Quel est l'effet du cortisol sur le métabolisme des AA ?", "answer": "Stimule la protéolyse musculaire et la néoglucogenèse hépatique." },
    
    # VIII. Pathologies
    { "question": "Qu'est-ce que la phénylcétonurie ?", "answer": "Déficit en phénylalanine hydroxylase → accumulation de phénylalanine → retard mental si non traité." },
    { "question": "Quel est le traitement de la phénylcétonurie ?", "answer": "Régime pauvre en phénylalanine dès la naissance." },
    { "question": "Qu'est-ce que l'albinisme ?", "answer": "Déficit en tyrosinase → absence de mélanine." },
    { "question": "Qu'est-ce que l'homocystinurie ?", "answer": "Déficit enzymatique du métabolisme de la méthionine → risques thrombotiques et oculaires." },
    { "question": "Qu'est-ce que la maladie du sirop d'érable ?", "answer": "Déficit en complexe BCKDH → accumulation d'AA branchés → odeur de sirop d'érable des urines." },
    { "question": "Qu'est-ce que l'hyperammoniémie ?", "answer": "Élévation de l'ammoniaque sanguin par déficit du cycle de l'urée → encéphalopathie." },
]

# =============================================================================
# FLASHCARDS PARENCHYME NERVEUX
# =============================================================================
FLASHCARDS_PARENCHYME_NERVEUX = [
    # I. Introduction
    { "question": "Qu'est-ce que le tissu nerveux ?", "answer": "Tissu spécialisé dans la réception, la conduction et la transmission de l'influx nerveux." },
    { "question": "Quels sont les 2 types de cellules du tissu nerveux ?", "answer": "Les neurones et les cellules gliales (névroglie)." },
    { "question": "Qu'est-ce que la substance grise ?", "answer": "Zones contenant les corps cellulaires des neurones." },
    { "question": "Qu'est-ce que la substance blanche ?", "answer": "Zones contenant les axones myélinisés." },
    { "question": "Quelle est l'origine embryologique du tissu nerveux ?", "answer": "L'ectoderme (tube neural et crête neurale)." },
    
    # II. Le neurone
    { "question": "Quelles sont les 3 parties d'un neurone ?", "answer": "Corps cellulaire (péricaryon), dendrites, axone." },
    { "question": "Qu'est-ce que le péricaryon ?", "answer": "Corps cellulaire du neurone contenant le noyau et les organites." },
    { "question": "Quelle est la particularité du noyau du neurone ?", "answer": "Grand, clair, euchromatique avec nucléole proéminent." },
    { "question": "Qu'est-ce que les corps de Nissl ?", "answer": "Amas de réticulum endoplasmique granuleux (REG) intensément colorés au crésyl violet." },
    { "question": "Que traduit l'abondance des corps de Nissl ?", "answer": "Une synthèse protéique intense (environ 10% des protéines renouvelées chaque jour)." },
    { "question": "Qu'est-ce que le cône d'implantation ?", "answer": "Zone d'émergence de l'axone, dépourvue de corps de Nissl." },
    { "question": "Qu'est-ce qu'une dendrite ?", "answer": "Prolongement récepteur du neurone, court, ramifié, contenant des corps de Nissl." },
    { "question": "Qu'est-ce qu'un axone ?", "answer": "Prolongement unique, long, fin, transmettant l'influx vers les terminaisons synaptiques." },
    { "question": "Qu'est-ce que le transport axonal antérograde ?", "answer": "Transport du corps cellulaire vers la terminaison axonale (kinésines)." },
    { "question": "Qu'est-ce que le transport axonal rétrograde ?", "answer": "Transport de la terminaison vers le corps cellulaire (dynéines)." },
    { "question": "Qu'est-ce qu'un bouton synaptique ?", "answer": "Terminaison axonale contenant les vésicules de neurotransmetteurs." },
    
    # Classification des neurones
    { "question": "Qu'est-ce qu'un neurone unipolaire ?", "answer": "Neurone avec un seul prolongement (rare chez l'adulte)." },
    { "question": "Qu'est-ce qu'un neurone bipolaire ?", "answer": "Neurone avec 2 prolongements opposés (rétine, oreille interne, muqueuse olfactive)." },
    { "question": "Qu'est-ce qu'un neurone pseudo-unipolaire ?", "answer": "Neurone sensitif avec un seul prolongement qui se divise en T (ganglions spinaux)." },
    { "question": "Qu'est-ce qu'un neurone multipolaire ?", "answer": "Neurone avec nombreuses dendrites et un axone (majorité des neurones)." },
    { "question": "Qu'est-ce qu'une cellule de Purkinje ?", "answer": "Grand neurone multipolaire du cortex cérébelleux avec arborisation dendritique complexe." },
    { "question": "Qu'est-ce qu'une cellule pyramidale ?", "answer": "Neurone du cortex cérébral avec corps triangulaire et dendrite apicale." },
    
    # III. La névroglie centrale
    { "question": "Combien de cellules gliales pour un neurone ?", "answer": "10 à 50 cellules gliales pour 1 neurone." },
    { "question": "Quels sont les types de cellules gliales du SNC ?", "answer": "Astrocytes, oligodendrocytes, cellules épendymaires, microglie." },
    { "question": "Qu'est-ce qu'un astrocyte ?", "answer": "Cellule gliale étoilée avec prolongements péri-vasculaires (pieds astrocytaires)." },
    { "question": "Quels sont les 2 types d'astrocytes ?", "answer": "Astrocytes protoplasmiques (substance grise) et fibreux (substance blanche)." },
    { "question": "Quelles sont les fonctions des astrocytes ?", "answer": "Soutien, barrière hémato-encéphalique, nutrition, régulation ionique, cicatrisation." },
    { "question": "Qu'est-ce que la barrière hémato-encéphalique ?", "answer": "Barrière formée par l'endothélium capillaire et les pieds astrocytaires, contrôlant les échanges." },
    { "question": "Qu'est-ce qu'un oligodendrocyte ?", "answer": "Cellule gliale formant la myéline du SNC (un oligodendrocyte myélinise plusieurs axones)." },
    { "question": "Qu'est-ce que les cellules épendymaires ?", "answer": "Cellules épithéliales bordant les ventricules cérébraux et le canal de l'épendyme." },
    { "question": "Quels sont les 3 types de cellules épendymaires ?", "answer": "Épendymocytes, tanycytes, cellules des plexus choroïdes." },
    { "question": "Quel est le rôle des plexus choroïdes ?", "answer": "Sécrétion du liquide céphalo-rachidien (LCR)." },
    { "question": "Qu'est-ce que la microglie ?", "answer": "Macrophages résidents du SNC, d'origine mésenchymateuse." },
    { "question": "Quel est le rôle de la microglie ?", "answer": "Défense immunitaire, phagocytose des débris cellulaires." },
    
    # IV. La névroglie périphérique
    { "question": "Quelles cellules constituent la névroglie périphérique ?", "answer": "Cellules de Schwann et cellules satellites." },
    { "question": "Qu'est-ce qu'une cellule de Schwann ?", "answer": "Cellule gliale entourant les axones périphériques (une cellule = un internode)." },
    { "question": "Quelle est la différence entre fibres myélinisées et amyéliniques ?", "answer": "Myélinisées : axone entouré de gaine de myéline ; amyéliniques : axones en gouttières (fibres de Remak)." },
    { "question": "Qu'est-ce que les cellules satellites ?", "answer": "Cellules gliales entourant les corps des neurones dans les ganglions." },
    
    # V. La myéline
    { "question": "Qu'est-ce que la myéline ?", "answer": "Gaine lipidique entourant les axones, formée par enroulement de la membrane des cellules gliales." },
    { "question": "Quelle est la composition de la myéline ?", "answer": "70% lipides (cholestérol, phospholipides, glycolipides), 30% protéines." },
    { "question": "Qu'est-ce qu'un nœud de Ranvier ?", "answer": "Interruption de la gaine de myéline entre deux cellules de Schwann ou oligodendrocytes." },
    { "question": "Qu'est-ce que la conduction saltatoire ?", "answer": "Propagation rapide de l'influx nerveux de nœud de Ranvier en nœud de Ranvier." },
    { "question": "Quelle est la vitesse de conduction des fibres myélinisées ?", "answer": "Jusqu'à 120 m/s (contre 0,5-2 m/s pour les fibres amyéliniques)." },
    { "question": "Qu'est-ce qu'un internode ?", "answer": "Segment de myéline entre deux nœuds de Ranvier (0,3 à 1,5 mm)." },
    
    # VI. Les synapses
    { "question": "Qu'est-ce qu'une synapse ?", "answer": "Zone de contact fonctionnel entre deux neurones ou entre un neurone et une cellule effectrice." },
    { "question": "Quels sont les 2 types de synapses ?", "answer": "Synapses chimiques (neurotransmetteurs) et électriques (jonctions gap)." },
    { "question": "Quels sont les 3 éléments d'une synapse chimique ?", "answer": "Élément présynaptique (bouton), fente synaptique (20-30 nm), élément postsynaptique." },
    { "question": "Que contient le bouton présynaptique ?", "answer": "Vésicules synaptiques, mitochondries, cytosquelette." },
    { "question": "Comment sont libérés les neurotransmetteurs ?", "answer": "Par exocytose Ca2+-dépendante des vésicules synaptiques." },
    { "question": "Qu'est-ce qu'une synapse excitatrice ?", "answer": "Synapse provoquant une dépolarisation du neurone postsynaptique (asymétrique, type I de Gray)." },
    { "question": "Qu'est-ce qu'une synapse inhibitrice ?", "answer": "Synapse provoquant une hyperpolarisation (symétrique, type II de Gray)." },
    { "question": "Quels sont les types de synapses selon leur localisation ?", "answer": "Axo-dendritique, axo-somatique, axo-axonique, dendro-dendritique." },
    { "question": "Qu'est-ce qu'une plaque motrice ?", "answer": "Synapse neuro-musculaire entre un motoneurone et une fibre musculaire striée." },
    
    # VII. Nerfs périphériques
    { "question": "Comment est organisé un nerf périphérique ?", "answer": "Axones en faisceaux entourés d'endonèvre, périnèvre (fascicule), épinèvre (nerf entier)." },
    { "question": "Qu'est-ce que l'endonèvre ?", "answer": "Tissu conjonctif lâche entourant chaque fibre nerveuse." },
    { "question": "Qu'est-ce que le périnèvre ?", "answer": "Gaine de cellules épithélioïdes entourant un fascicule nerveux (barrière hémato-nerveuse)." },
    { "question": "Qu'est-ce que l'épinèvre ?", "answer": "Tissu conjonctif dense entourant l'ensemble du nerf." },
    
    # VIII. Ganglions nerveux
    { "question": "Quels sont les types de ganglions nerveux ?", "answer": "Ganglions sensitifs (cérébro-spinaux) et ganglions végétatifs (autonomes)." },
    { "question": "Qu'est-ce qu'un ganglion spinal ?", "answer": "Ganglion contenant les corps cellulaires des neurones sensitifs (pseudo-unipolaires)." },
    { "question": "Qu'est-ce qu'un ganglion sympathique ?", "answer": "Ganglion végétatif avec neurones multipolaires et synapses intrinsèques." },
]

# =============================================================================
# FLASHCARDS TISSUS CONJONCTIFS
# =============================================================================
FLASHCARDS_TISSUS_CONJONCTIFS = [
    # I. Introduction
    { "question": "Quelle est l'origine embryologique des tissus conjonctifs ?", "answer": "Le mésenchyme, issu du mésoblaste." },
    { "question": "Quels sont les constituants des tissus conjonctifs ?", "answer": "Cellules, fibres et substance fondamentale (matrice extracellulaire)." },
    { "question": "Quelles sont les fonctions des tissus conjonctifs ?", "answer": "Soutien, nutrition, défense, réparation, stockage." },
    { "question": "Quels sont les types de tissus conjonctifs ?", "answer": "Lâche, dense (orienté/non orienté), réticulé, adipeux, muqueux." },
    
    # II. Cellules du tissu conjonctif
    { "question": "Quelles sont les cellules résidentes du tissu conjonctif ?", "answer": "Fibroblastes, adipocytes, mastocytes, macrophages." },
    { "question": "Quelles sont les cellules migratrices du tissu conjonctif ?", "answer": "Lymphocytes, plasmocytes, polynucléaires, monocytes." },
    { "question": "Qu'est-ce qu'un fibroblaste ?", "answer": "Cellule fusiforme synthétisant les fibres et la substance fondamentale." },
    { "question": "Quelle est la forme inactive du fibroblaste ?", "answer": "Le fibrocyte, cellule quiescente pouvant être réactivée." },
    { "question": "Qu'est-ce qu'un myofibroblaste ?", "answer": "Fibroblaste contractile avec filaments d'actine, impliqué dans la cicatrisation." },
    { "question": "Qu'est-ce qu'un macrophage ?", "answer": "Cellule phagocytaire dérivée du monocyte sanguin (système mononucléé phagocytaire)." },
    { "question": "Quels sont les autres noms des macrophages selon leur localisation ?", "answer": "Cellules de Kupffer (foie), microglie (SNC), ostéoclastes (os), cellules de Langerhans (peau)." },
    { "question": "Quelles sont les fonctions des macrophages ?", "answer": "Phagocytose, présentation d'antigène, sécrétion de cytokines." },
    { "question": "Qu'est-ce qu'un mastocyte ?", "answer": "Cellule contenant des granulations métachromatiques (histamine, héparine)." },
    { "question": "Quelle coloration révèle les mastocytes ?", "answer": "Bleu de toluidine (métachromasie : violet au lieu de bleu)." },
    { "question": "Quel est le rôle des mastocytes ?", "answer": "Réactions allergiques (IgE), inflammation, coagulation locale." },
    { "question": "Qu'est-ce qu'un plasmocyte ?", "answer": "Lymphocyte B différencié sécrétant des immunoglobulines (anticorps)." },
    { "question": "Quelle est la morphologie caractéristique du plasmocyte ?", "answer": "Noyau excentré, chromatine en 'rayon de roue', cytoplasme basophile (REG abondant)." },
    
    # III. Fibres du tissu conjonctif
    { "question": "Quels sont les 3 types de fibres conjonctives ?", "answer": "Fibres de collagène, fibres élastiques, fibres réticulées." },
    { "question": "Qu'est-ce que le collagène ?", "answer": "Protéine fibreuse la plus abondante de l'organisme (30% des protéines totales)." },
    { "question": "Quelle est la structure du collagène ?", "answer": "Triple hélice de 3 chaînes α, organisées en fibrilles puis en fibres." },
    { "question": "Quels sont les principaux types de collagène ?", "answer": "Type I (os, tendon, derme), II (cartilage), III (réticuline), IV (lames basales)." },
    { "question": "Comment synthétise-t-on le collagène ?", "answer": "Procollagène dans le REG → modifications (hydroxylation, glycosylation) → sécrétion → assemblage extracellulaire." },
    { "question": "Quels AA sont hydroxylés dans le collagène ?", "answer": "Proline et lysine (hydroxyproline, hydroxylysine) par des hydroxylases vitamine C-dépendantes." },
    { "question": "Qu'est-ce que les fibres élastiques ?", "answer": "Fibres extensibles composées d'élastine entourée de microfibrilles (fibrilline)." },
    { "question": "Où trouve-t-on des fibres élastiques ?", "answer": "Paroi des artères, poumons, peau, ligaments." },
    { "question": "Comment colore-t-on les fibres élastiques ?", "answer": "Par l'orcéine ou la résorcine-fuchsine." },
    { "question": "Qu'est-ce que les fibres réticulées ?", "answer": "Fibres fines de collagène type III, formant des réseaux." },
    { "question": "Où trouve-t-on des fibres réticulées ?", "answer": "Stroma des organes lymphoïdes, autour des cellules (fibres péricellulaires)." },
    { "question": "Comment colore-t-on les fibres réticulées ?", "answer": "Par imprégnation argentique (fibres argyrophiles)." },
    
    # IV. Substance fondamentale
    { "question": "Qu'est-ce que la substance fondamentale ?", "answer": "Gel hydraté transparent remplissant l'espace entre cellules et fibres." },
    { "question": "Quels sont les constituants de la substance fondamentale ?", "answer": "Eau, sels, glycosaminoglycanes (GAG), protéoglycanes, glycoprotéines." },
    { "question": "Qu'est-ce qu'un glycosaminoglycane (GAG) ?", "answer": "Polysaccharide formé d'unités disaccharidiques répétées, fortement hydrophile." },
    { "question": "Quels sont les principaux GAG ?", "answer": "Acide hyaluronique, chondroïtine-sulfate, héparane-sulfate, kératane-sulfate." },
    { "question": "Qu'est-ce qu'un protéoglycane ?", "answer": "Protéine axiale sur laquelle sont greffés des GAG." },
    { "question": "Qu'est-ce qu'un agrécane ?", "answer": "Protéoglycane du cartilage formant des agrégats avec l'acide hyaluronique." },
    { "question": "Quelles glycoprotéines adhésives trouve-t-on ?", "answer": "Fibronectine, laminine, entactine." },
    { "question": "Quel est le rôle de la fibronectine ?", "answer": "Adhésion cellule-matrice, migration cellulaire, cicatrisation." },
    { "question": "Où trouve-t-on la laminine ?", "answer": "Dans les lames basales." },
    
    # V. Types de tissus conjonctifs
    { "question": "Qu'est-ce que le tissu conjonctif lâche ?", "answer": "TC aréolaire avec peu de fibres, beaucoup de substance fondamentale et de cellules." },
    { "question": "Où trouve-t-on le tissu conjonctif lâche ?", "answer": "Chorion des muqueuses, tissu sous-cutané, autour des vaisseaux et nerfs." },
    { "question": "Qu'est-ce que le tissu conjonctif dense non orienté ?", "answer": "TC riche en fibres de collagène entrecroisées (derme, capsules d'organes)." },
    { "question": "Qu'est-ce que le tissu conjonctif dense orienté ?", "answer": "TC avec fibres parallèles (tendons, ligaments, aponévroses)." },
    { "question": "Qu'est-ce que le tissu réticulé ?", "answer": "TC avec réseau de fibres réticulées et cellules réticulaires (organes lymphoïdes)." },
    { "question": "Qu'est-ce que le tissu muqueux ?", "answer": "TC embryonnaire riche en substance fondamentale (gelée de Wharton du cordon ombilical)." },
    
    # VI. Tissu adipeux
    { "question": "Quels sont les 2 types de tissu adipeux ?", "answer": "Tissu adipeux blanc (uniloculaire) et brun (multiloculaire)." },
    { "question": "Quelle est la structure d'un adipocyte blanc ?", "answer": "Grande cellule (100-150 μm) avec une vacuole lipidique unique, noyau périphérique aplati." },
    { "question": "Quelles sont les fonctions du tissu adipeux blanc ?", "answer": "Réserve énergétique, isolation thermique, protection mécanique, fonction endocrine." },
    { "question": "Quelles hormones sécrète le tissu adipeux blanc ?", "answer": "Leptine, adiponectine, résistine, œstrogènes." },
    { "question": "Quelle est la structure d'un adipocyte brun ?", "answer": "Cellule plus petite avec multiples vacuoles lipidiques, nombreuses mitochondries." },
    { "question": "Quelle est la fonction du tissu adipeux brun ?", "answer": "Thermogenèse (production de chaleur) grâce à la protéine découplante UCP1." },
    { "question": "Où trouve-t-on le tissu adipeux brun ?", "answer": "Chez le nouveau-né (interscapulaire) ; traces chez l'adulte." },
    
    # VII. Lames basales
    { "question": "Qu'est-ce qu'une lame basale ?", "answer": "Structure extracellulaire fine sous les épithéliums et autour de certaines cellules." },
    { "question": "Quelles sont les couches de la lame basale en ME ?", "answer": "Lamina lucida (claire), lamina densa (dense aux électrons)." },
    { "question": "Quels sont les composants de la lame basale ?", "answer": "Collagène IV, laminine, entactine, héparane-sulfate." },
    { "question": "Quelles sont les fonctions de la lame basale ?", "answer": "Support, filtration, compartimentation, polarité cellulaire, régénération." },
    { "question": "Qu'est-ce qu'une membrane basale ?", "answer": "Lame basale + lame réticulée (fibres réticulées) en microscopie optique." },
    { "question": "Comment colore-t-on la membrane basale ?", "answer": "Par le PAS (positive) ou l'imprégnation argentique." },
]

# =============================================================================
# FLASHCARDS TISSU MUSCULAIRE CARDIAQUE
# =============================================================================
FLASHCARDS_TISSU_MUSCULAIRE_CARDIAQUE = [
    # I. Introduction
    { "question": "Quels sont les 3 types de tissu musculaire ?", "answer": "Musculaire strié squelettique, strié cardiaque, lisse." },
    { "question": "Quelles sont les propriétés du tissu musculaire cardiaque ?", "answer": "Strié, contractile, automatique (rythmogène), involontaire." },
    { "question": "Où trouve-t-on le tissu musculaire cardiaque ?", "answer": "Uniquement dans le myocarde (paroi du cœur)." },
    
    # II. Le cardiomyocyte
    { "question": "Qu'est-ce qu'un cardiomyocyte ?", "answer": "Cellule musculaire cardiaque (cellule myocardique)." },
    { "question": "Quelle est la forme d'un cardiomyocyte ?", "answer": "Cellule cylindrique bifurquée (ramifiée) avec 1 ou 2 noyaux centraux." },
    { "question": "Quelles sont les dimensions d'un cardiomyocyte ?", "answer": "100-150 μm de long, 10-20 μm de diamètre." },
    { "question": "Pourquoi le cardiomyocyte est-il strié ?", "answer": "Présence de myofibrilles organisées en sarcomères." },
    { "question": "Qu'est-ce qu'un sarcomère ?", "answer": "Unité contractile entre deux stries Z, contenant filaments fins et épais." },
    { "question": "Que sont les filaments fins ?", "answer": "Filaments d'actine avec tropomyosine et troponine." },
    { "question": "Que sont les filaments épais ?", "answer": "Filaments de myosine avec têtes ATPasiques." },
    { "question": "Qu'est-ce que la bande A ?", "answer": "Bande sombre contenant les filaments de myosine (et partiellement les filaments d'actine)." },
    { "question": "Qu'est-ce que la bande I ?", "answer": "Bande claire contenant uniquement les filaments d'actine." },
    { "question": "Qu'est-ce que la bande H ?", "answer": "Zone centrale de la bande A contenant uniquement la myosine." },
    { "question": "Qu'est-ce que la strie Z ?", "answer": "Ligne de jonction des filaments d'actine (limite du sarcomère)." },
    { "question": "Qu'est-ce que la strie M ?", "answer": "Ligne centrale du sarcomère (milieu de la bande H)." },
    { "question": "Pourquoi les cardiomyocytes sont-ils riches en mitochondries ?", "answer": "Pour la production d'ATP nécessaire aux contractions continues." },
    { "question": "Quel pourcentage du volume cellulaire occupent les mitochondries ?", "answer": "30-40% du volume cellulaire." },
    { "question": "Qu'est-ce que le réticulum sarcoplasmique ?", "answer": "Réticulum endoplasmique lisse stockant le Ca2+." },
    { "question": "Qu'est-ce qu'un tubule T ?", "answer": "Invagination du sarcolemme au niveau des stries Z permettant la propagation du potentiel d'action." },
    { "question": "Qu'est-ce qu'une diade ?", "answer": "Association d'un tubule T et d'une citerne du RS." },
    { "question": "Quelle est la particularité des tubules T cardiaques ?", "answer": "Situés au niveau des stries Z (pas des jonctions A-I comme le muscle squelettique)." },
    
    # III. Disques intercalaires
    { "question": "Qu'est-ce qu'un disque intercalaire ?", "answer": "Zone de jonction entre deux cardiomyocytes adjacents, au niveau des stries Z." },
    { "question": "Quels sont les 3 types de jonctions des disques intercalaires ?", "answer": "Fascia adherens (zonula adherens), desmosomes, jonctions gap." },
    { "question": "Quel est le rôle du fascia adherens ?", "answer": "Ancrage des filaments d'actine (myofibrilles) entre cellules adjacentes." },
    { "question": "Quel est le rôle des desmosomes cardiaques ?", "answer": "Jonctions d'ancrage résistant aux forces de traction." },
    { "question": "Quel est le rôle des jonctions gap cardiaques ?", "answer": "Couplage électrique : propagation du potentiel d'action entre cellules." },
    { "question": "Qu'est-ce qu'un connexon ?", "answer": "Canal formé par 6 connexines, constituant les jonctions gap." },
    { "question": "Pourquoi le cœur fonctionne-t-il comme un syncytium ?", "answer": "Les jonctions gap permettent la contraction synchrone de toutes les cellules." },
    
    # IV. Contraction cardiaque
    { "question": "Quel est le mécanisme de la contraction cardiaque ?", "answer": "Glissement des filaments d'actine sur la myosine (théorie du glissement)." },
    { "question": "Quel ion déclenche la contraction ?", "answer": "Le calcium (Ca2+)." },
    { "question": "Qu'est-ce que le couplage excitation-contraction ?", "answer": "Transformation du signal électrique en contraction mécanique." },
    { "question": "D'où provient le Ca2+ de la contraction cardiaque ?", "answer": "Entrée de Ca2+ extracellulaire (tubules T) + libération du RS (calcium-induced calcium release)." },
    { "question": "Quel est le rôle de la troponine C ?", "answer": "Fixation du Ca2+, permettant le démasquage des sites de liaison actine-myosine." },
    { "question": "Comment se termine la contraction ?", "answer": "Recaptage du Ca2+ par SERCA (pompe du RS) et expulsion par NCX." },
    { "question": "Qu'est-ce que SERCA ?", "answer": "Sarco/Endoplasmic Reticulum Ca2+-ATPase, pompe recaptant le Ca2+ dans le RS." },
    
    # V. Tissu nodal
    { "question": "Qu'est-ce que le tissu nodal ?", "answer": "Tissu cardiaque spécialisé dans la genèse et la conduction de l'influx (cardiomyocytes modifiés)." },
    { "question": "Quels sont les éléments du tissu nodal ?", "answer": "Nœud sinusal, nœud atrio-ventriculaire, faisceau de His, branches, réseau de Purkinje." },
    { "question": "Où se situe le nœud sinusal ?", "answer": "À la jonction VCS-oreillette droite (pacemaker naturel)." },
    { "question": "Quelle est la fréquence intrinsèque du nœud sinusal ?", "answer": "70-80 bpm." },
    { "question": "Quelle est la fréquence intrinsèque du nœud AV ?", "answer": "40-60 bpm." },
    { "question": "Quelle est la fréquence intrinsèque du faisceau de His ?", "answer": "30-40 bpm." },
    { "question": "Quelles sont les caractéristiques des cellules nodales ?", "answer": "Plus petites, pâles, pauvres en myofibrilles, sans tubules T, riches en glycogène." },
    { "question": "Qu'est-ce qu'une cellule de Purkinje ?", "answer": "Grande cellule du réseau de conduction, riche en glycogène, reliée par jonctions gap." },
    { "question": "Comment reconnaît-on les cellules de Purkinje en microscopie ?", "answer": "Grandes cellules pâles, vacuolées (glycogène), pauvres en myofibrilles." },
    
    # VI. Innervation et vascularisation
    { "question": "Quelle est l'innervation du cœur ?", "answer": "Système nerveux autonome : sympathique (accélérateur) et parasympathique (freinateur)." },
    { "question": "Quel nerf apporte l'innervation parasympathique au cœur ?", "answer": "Le nerf vague (X)." },
    { "question": "Quel est l'effet du sympathique sur le cœur ?", "answer": "Effet chronotrope +, inotrope +, dromotrope + (accélération, force, conduction)." },
    { "question": "Quel est l'effet du parasympathique sur le cœur ?", "answer": "Effet chronotrope -, dromotrope - (ralentissement, conduction diminuée)." },
    { "question": "Comment est vascularisé le myocarde ?", "answer": "Par les artères coronaires (gauche et droite) issues de l'aorte." },
    
    # VII. Régénération et pathologies
    { "question": "Le cardiomyocyte peut-il se diviser ?", "answer": "Non (ou très peu), c'est une cellule post-mitotique." },
    { "question": "Comment se répare le myocarde après un infarctus ?", "answer": "Par fibrose cicatricielle (tissu conjonctif), pas par régénération." },
    { "question": "Qu'est-ce que l'hypertrophie cardiaque ?", "answer": "Augmentation de taille des cardiomyocytes (pas du nombre) en réponse à une surcharge." },
    { "question": "Qu'est-ce qu'une cardiomyopathie ?", "answer": "Maladie primitive du muscle cardiaque (hypertrophique, dilatée, restrictive)." },
    { "question": "Qu'est-ce qu'une myocardite ?", "answer": "Inflammation du myocarde, souvent virale." },
]

# =============================================================================
# FLASHCARDS TISSUS SQUELETTIQUES
# =============================================================================
FLASHCARDS_TISSUS_SQUELETTIQUES = [
    # I. Introduction
    { "question": "Quels sont les tissus squelettiques ?", "answer": "Tissu cartilagineux et tissu osseux." },
    { "question": "Quelle est l'origine embryologique des tissus squelettiques ?", "answer": "Le mésenchyme (mésoblaste)." },
    { "question": "Quelle est la caractéristique commune des tissus squelettiques ?", "answer": "Matrice extracellulaire solide (rigide ou semi-rigide)." },
    
    # II. Tissu cartilagineux
    { "question": "Quelles sont les propriétés du cartilage ?", "answer": "Résistant, souple, élastique, avasculaire." },
    { "question": "Quels sont les constituants du cartilage ?", "answer": "Chondrocytes et matrice cartilagineuse." },
    { "question": "Qu'est-ce qu'un chondrocyte ?", "answer": "Cellule du cartilage, située dans une logette (chondroplaste)." },
    { "question": "Quelle est la forme des chondrocytes ?", "answer": "Sphérique (avec noyau rond, cytoplasme basophile riche en REG)." },
    { "question": "Qu'est-ce qu'un groupe isogénique ?", "answer": "Ensemble de chondrocytes issus de la même cellule mère, regroupés dans une même lacune." },
    { "question": "Qu'est-ce que la matrice territoriale ?", "answer": "Zone de matrice entourant immédiatement un groupe isogénique (basophile)." },
    { "question": "Qu'est-ce que la matrice interterritoriale ?", "answer": "Zone de matrice entre les territoires (moins basophile)." },
    { "question": "Que contient la matrice cartilagineuse ?", "answer": "Collagène (II principalement), protéoglycanes (agrécanes), glycoprotéines, eau." },
    { "question": "Pourquoi le cartilage est-il avasculaire ?", "answer": "La matrice dense empêche la pénétration des vaisseaux." },
    { "question": "Comment se nourrit le cartilage ?", "answer": "Par diffusion à partir du périchondre ou du liquide synovial." },
    { "question": "Qu'est-ce que le périchondre ?", "answer": "Gaine de tissu conjonctif entourant le cartilage (sauf cartilage articulaire)." },
    { "question": "Quelles sont les couches du périchondre ?", "answer": "Couche fibreuse externe (fibroblastes), couche chondrogène interne (chondroblastes)." },
    
    # Types de cartilage
    { "question": "Quels sont les 3 types de cartilage ?", "answer": "Cartilage hyalin, élastique, fibreux (fibrocartilage)." },
    { "question": "Qu'est-ce que le cartilage hyalin ?", "answer": "Cartilage le plus répandu, aspect translucide, riche en collagène II." },
    { "question": "Où trouve-t-on du cartilage hyalin ?", "answer": "Cartilages articulaires, costaux, respiratoires (trachée, bronches), nasaux." },
    { "question": "Qu'est-ce que le cartilage élastique ?", "answer": "Cartilage contenant des fibres élastiques en plus du collagène II." },
    { "question": "Où trouve-t-on du cartilage élastique ?", "answer": "Pavillon de l'oreille, conduit auditif, épiglotte, trompe d'Eustache." },
    { "question": "Comment colore-t-on le cartilage élastique ?", "answer": "Par l'orcéine ou la résorcine-fuchsine (fibres élastiques)." },
    { "question": "Qu'est-ce que le fibrocartilage ?", "answer": "Cartilage riche en fibres de collagène I organisées en faisceaux." },
    { "question": "Où trouve-t-on du fibrocartilage ?", "answer": "Disques intervertébraux, ménisques, symphyse pubienne, insertion des tendons." },
    { "question": "Quelle est la particularité du fibrocartilage ?", "answer": "Pas de périchondre, résistant aux compressions et cisaillements." },
    
    # III. Tissu osseux
    { "question": "Quelles sont les propriétés du tissu osseux ?", "answer": "Rigide, solide, vascularisé, innervé, en remodelage permanent." },
    { "question": "Quelles sont les fonctions du tissu osseux ?", "answer": "Soutien, protection, mouvement, réserve minérale (Ca, P), hématopoïèse (moelle)." },
    { "question": "Quels sont les constituants du tissu osseux ?", "answer": "Cellules (ostéoblastes, ostéocytes, ostéoclastes) et matrice osseuse." },
    { "question": "Qu'est-ce qu'un ostéoblaste ?", "answer": "Cellule synthétisant la matrice osseuse (ostéoïde)." },
    { "question": "Où se situent les ostéoblastes ?", "answer": "En surface du tissu osseux, formant des couches de cellules cubiques." },
    { "question": "Qu'est-ce qu'un ostéocyte ?", "answer": "Ostéoblaste emprisonné dans la matrice minéralisée, dans une ostéoplaste." },
    { "question": "Quelle est la morphologie de l'ostéocyte ?", "answer": "Cellule étoilée avec prolongements dans des canalicules reliés par jonctions gap." },
    { "question": "Quel est le rôle des ostéocytes ?", "answer": "Maintien de la matrice, mécanoréception, régulation du remodelage." },
    { "question": "Qu'est-ce qu'un ostéoclaste ?", "answer": "Grande cellule multinucléée résorbant la matrice osseuse." },
    { "question": "Quelle est l'origine de l'ostéoclaste ?", "answer": "Fusion de précurseurs monocytaires (lignée monocyte-macrophage)." },
    { "question": "Comment fonctionne l'ostéoclaste ?", "answer": "Bordure en brosse sécrétant HCl (dissolution minérale) et enzymes (digestion organique)." },
    { "question": "Qu'est-ce qu'une lacune de Howship ?", "answer": "Dépression creusée par un ostéoclaste dans la matrice osseuse." },
    
    # Matrice osseuse
    { "question": "Quelle est la composition de la matrice osseuse ?", "answer": "35% matrice organique, 65% matrice minérale." },
    { "question": "Que contient la matrice organique ?", "answer": "Collagène I (90%), ostéocalcine, ostéopontine, ostéonectine, GAG." },
    { "question": "Que contient la matrice minérale ?", "answer": "Cristaux d'hydroxyapatite Ca10(PO4)6(OH)2." },
    { "question": "Qu'est-ce que l'ostéoïde ?", "answer": "Matrice organique non minéralisée, sécrétée par les ostéoblastes." },
    { "question": "Comment se fait la minéralisation ?", "answer": "Dépôt de cristaux d'hydroxyapatite sur les fibres de collagène." },
    
    # Types d'os
    { "question": "Quels sont les 2 types d'os selon la structure ?", "answer": "Os compact (cortical) et os spongieux (trabéculaire)." },
    { "question": "Où trouve-t-on l'os compact ?", "answer": "Diaphyse des os longs, couche externe de tous les os." },
    { "question": "Où trouve-t-on l'os spongieux ?", "answer": "Épiphyses des os longs, intérieur des os courts et plats." },
    { "question": "Qu'est-ce qu'un ostéon ?", "answer": "Unité structurale de l'os compact (système de Havers)." },
    { "question": "Comment est organisé un ostéon ?", "answer": "Canal de Havers central + lamelles concentriques + ostéocytes dans leurs lacunes." },
    { "question": "Qu'est-ce qu'un canal de Havers ?", "answer": "Canal central de l'ostéon contenant vaisseaux et nerfs." },
    { "question": "Qu'est-ce qu'un canal de Volkmann ?", "answer": "Canal transversal reliant les canaux de Havers entre eux." },
    { "question": "Que sont les lamelles interstitielles ?", "answer": "Restes d'anciens ostéons entre les ostéons actuels." },
    { "question": "Que sont les travées osseuses ?", "answer": "Lamelles de l'os spongieux délimitant des cavités médullaires." },
    
    # Enveloppes osseuses
    { "question": "Qu'est-ce que le périoste ?", "answer": "Membrane conjonctive vascularisée recouvrant l'os (sauf surfaces articulaires)." },
    { "question": "Quelles sont les couches du périoste ?", "answer": "Couche fibreuse externe, couche ostéogène interne (cellules ostéoprogénitrices)." },
    { "question": "Qu'est-ce que l'endoste ?", "answer": "Fine couche de cellules bordant les cavités médullaires et les canaux de Havers." },
    
    # Ossification
    { "question": "Quels sont les 2 modes d'ossification ?", "answer": "Ossification endoconjonctive (de membrane) et endochondrale." },
    { "question": "Qu'est-ce que l'ossification de membrane ?", "answer": "Formation d'os directement à partir du mésenchyme (os du crâne, mandibule)." },
    { "question": "Qu'est-ce que l'ossification endochondrale ?", "answer": "Formation d'os sur une maquette cartilagineuse (os longs, vertèbres)." },
    { "question": "Où se situe le cartilage de conjugaison ?", "answer": "Entre l'épiphyse et la diaphyse, responsable de la croissance en longueur." },
    { "question": "Quelles sont les zones du cartilage de conjugaison ?", "answer": "Zone de réserve, prolifération, hypertrophie, calcification, ossification." },
    
    # Remodelage
    { "question": "Qu'est-ce que le remodelage osseux ?", "answer": "Équilibre continu entre résorption (ostéoclastes) et formation (ostéoblastes)." },
    { "question": "À quoi sert le remodelage osseux ?", "answer": "Maintien de la masse osseuse, réparation des microfissures, adaptation mécanique." },
    { "question": "Qu'est-ce que l'ostéoporose ?", "answer": "Déséquilibre du remodelage avec perte de masse osseuse (résorption > formation)." },
    { "question": "Comment la PTH agit-elle sur l'os ?", "answer": "Stimule indirectement les ostéoclastes → augmente la calcémie." },
    { "question": "Comment la calcitonine agit-elle sur l'os ?", "answer": "Inhibe directement les ostéoclastes → diminue la calcémie." },
]

# Dictionnaire des fichiers et flashcards
FILES_AND_FLASHCARDS = {
    "Histologie/APP_SPE/1_appareil_cardio.html": FLASHCARDS_APPAREIL_CARDIO,
    "Nutrition/SOCLE/1_e_tabolisme_des_acides_amine_s.html": FLASHCARDS_METABOLISME_AA,
    "Histologie/APP/app_parenchyme_nerveux.html": FLASHCARDS_PARENCHYME_NERVEUX,
    "Histologie/SOCLE/3_tissus_conjonctif.html": FLASHCARDS_TISSUS_CONJONCTIFS,
    "Histologie/APP/tissus_musculaire_cardiaque.html": FLASHCARDS_TISSU_MUSCULAIRE_CARDIAQUE,
    "Histologie/APP/2_tissus_squelettique.html": FLASHCARDS_TISSUS_SQUELETTIQUES,
}

def format_flashcards_js(flashcards):
    """Formatte la liste de flashcards en JavaScript."""
    lines = ["["]
    for fc in flashcards:
        q = fc["question"].replace("'", "\\'").replace('"', '\\"')
        a = fc["answer"].replace("'", "\\'").replace('"', '\\"')
        lines.append(f"{{ question: '{q}', answer: '{a}', }},")
    lines.append("]")
    return "\n".join(lines)

def update_html_file(filepath, flashcards):
    """Remplace les flashcards dans un fichier HTML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver et remplacer le tableau flashcardsData
    pattern = r'const flashcardsData =\s*\[[\s\S]*?\];'
    
    new_data = "const flashcardsData =\n" + format_flashcards_js(flashcards) + ";"
    
    new_content, count = re.subn(pattern, new_data, content)
    
    if count == 0:
        print(f"  ⚠️ Pattern non trouvé dans {filepath}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    import os
    print("🚀 Génération et injection des flashcards - Partie 2 (Histologie & Métabolisme)")
    print("=" * 60)
    
    for rel_path, flashcards in FILES_AND_FLASHCARDS.items():
        filepath = os.path.join(BASE_DIR, rel_path)
        print(f"\n📁 {rel_path}")
        print(f"   Flashcards à injecter: {len(flashcards)}")
        
        if not os.path.exists(filepath):
            print(f"   ❌ Fichier non trouvé!")
            continue
        
        success = update_html_file(filepath, flashcards)
        if success:
            print(f"   ✅ {len(flashcards)} flashcards injectées avec succès")
        else:
            print(f"   ❌ Échec de l'injection")
    
    print("\n" + "=" * 60)
    print("✨ Terminé!")

if __name__ == "__main__":
    main()
