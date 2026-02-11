#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer ~100 flashcards exhaustives pour chaque cours 
et les injecter dans les fichiers HTML USPN S2
"""

import os
import re

BASE_DIR = "/Users/cyrilwisa/Desktop/diploma/USPN_S2"

# Définition des flashcards pour chaque cours
# ============================================

FLASHCARDS_OBESITE = [
    # I. Définitions
    { "question": "Que signifie HAS ?", "answer": "Haute Autorité de Santé." },
    { "question": "Quelles sont les dates clés de la HAS concernant l'obésité ?", "answer": "2012 : Surpoids et obésité de l'adulte ; 2009 : Obésité ; 2022 : Prise en charge 2e et 3e niveau ; 2023 : Guide du parcours de soins." },
    { "question": "Comment l'OMS définit-elle le surpoids et l'obésité ?", "answer": "Accumulation anormale ou excessive de graisse corporelle qui peut nuire à la santé." },
    { "question": "Quelles sont les trois causes de l'excès pondéral ?", "answer": "Rétention hydrosodée, augmentation des masses musculaires, excès de masse grasse." },
    { "question": "Quelle est la formule de l'IMC ?", "answer": "IMC = poids (kg) / taille² (m)." },
    { "question": "Quelles sont les valeurs normales de l'IMC ?", "answer": "Entre 18,5 et 24,9 kg/m²." },
    { "question": "Quelle est la formule de Lorentz pour le poids idéal ?", "answer": "Poids idéal (kg) = Taille (cm) - 100 - (Taille - 150)/x où x=4 pour homme, x=2 pour femme." },
    { "question": "Quel IMC définit le surpoids ?", "answer": "IMC entre 25,0 et 29,9 kg/m²." },
    { "question": "Quel IMC définit l'obésité de type I (modérée) ?", "answer": "IMC entre 30,0 et 34,9 kg/m²." },
    { "question": "Quel IMC définit l'obésité de type II (sévère) ?", "answer": "IMC entre 35,0 et 39,9 kg/m²." },
    { "question": "Quel IMC définit l'obésité de type III (massive/morbide) ?", "answer": "IMC ≥ 40 kg/m²." },
    { "question": "Quels sont les seuils IMC pour les sujets Sud-Asiatiques ?", "answer": ">23 pour surpoids, >27 pour obésité." },
    { "question": "Quelles méthodes de recherche mesurent précisément la masse grasse ?", "answer": "Plis cutanés, mesures isotopiques, imagerie." },
    { "question": "Quelles méthodes mesurent la masse grasse en services spécialisés ?", "answer": "Impédance électrique, densitométrie, mesures radiologiques." },
    { "question": "Qu'est-ce que la répartition gynoïde ?", "answer": "Répartition en forme de poire, prédominance sous-ombilicale, graisse sous-cutanée sans conséquence métabolique." },
    { "question": "Qu'est-ce que la répartition androïde ?", "answer": "Répartition en forme de pomme, prédominance sus-ombilicale, graisse viscérale associée à des comorbidités." },
    { "question": "Quel est le seuil normal du tour abdominal chez la femme ?", "answer": "Inférieur à 88 cm." },
    { "question": "Quel est le seuil normal du tour abdominal chez l'homme ?", "answer": "Inférieur à 100 cm." },
    { "question": "Où se situe la régulation de la prise alimentaire ?", "answer": "Dans l'hypothalamus, par des noyaux orexigènes et anorexigènes." },
    
    # II. Prévalence
    { "question": "Quelle était la prévalence de l'obésité en France en 2000 ?", "answer": "Au moins 10%." },
    { "question": "Quelle était la prévalence de l'obésité en France en 2010 ?", "answer": "Environ 15%." },
    { "question": "Quelle est la prévalence actuelle de l'obésité en France ?", "answer": "17%." },
    { "question": "Quel pourcentage des adultes français est en surpoids ou obèse ?", "answer": "47%." },
    { "question": "Combien de personnes adultes obèses compte la France ?", "answer": "Près de 8 millions." },
    { "question": "Quel est l'IMC moyen des adultes français ?", "answer": "25,5 kg/m²." },
    { "question": "Quelle est la prévalence de l'obésité massive (IMC>40) ?", "answer": "2%." },
    { "question": "Quel pourcentage d'enfants de 2-7 ans sont obèses ?", "answer": "18%." },
    { "question": "Quel pourcentage d'enfants de 8-17 ans sont obèses ?", "answer": "6%." },
    { "question": "Quels facteurs influencent la prévalence de l'obésité ?", "answer": "L'âge, la région, le niveau socio-professionnel." },
    
    # III. Approche clinique - Évaluation
    { "question": "Quels sont les 6 axes de la prise en charge de l'obésité ?", "answer": "Évaluation médicale/biologique, alimentaire, psycho-sociale, activité physique, dépense énergétique, selon niveau de prise en charge." },
    { "question": "Quelles comorbidités rechercher lors du bilan de l'obésité ?", "answer": "Diabète, HTA, risque cardiovasculaire, pathologies respiratoires, stéatopathie, arthrose, atteinte rénale, cancers." },
    { "question": "Quelles pathologies ont un RR > 3 en cas d'obésité ?", "answer": "Diabète, lithiase vésiculaire, dyslipidémie, insulinorésistance, dyspnée, syndrome d'apnée du sommeil." },
    { "question": "Quelles pathologies ont un RR entre 2 et 3 en cas d'obésité ?", "answer": "Insuffisance coronaire, AVC, HTA, arthrose, hyperuricémie/goutte, stéato-hépatites." },
    { "question": "Quelles pathologies ont un RR entre 1 et 2 en cas d'obésité ?", "answer": "Cancer du sein, de l'endomètre, du colon, de l'oropharynx, infertilité, risque opératoire/obstétrical augmenté." },
    { "question": "Quels gènes sont identifiés dans la prise de poids ?", "answer": "20 gènes, dont mutations de POMC, Proconvertase 1, MC4R." },
    { "question": "Quels sont les syndromes génétiques associés à l'obésité ?", "answer": "Syndrome de Willi-Prader, Bardet-Biedl, Cohen." },
    { "question": "Quels sont les signes du syndrome de Willi-Prader ?", "answer": "Obésité vers 1-2 ans, hypotonie, retard psychomoteur, micropénis." },
    { "question": "Quels sont les signes du syndrome de Bardet-Biedl ?", "answer": "Obésité vers 1-2 ans, rétinite pigmentaire, polydactylie, difficultés cognitives, anomalies génitales et rénales." },
    { "question": "Quelles sont les causes neuro-endocriniennes de l'obésité ?", "answer": "Hypercorticisme (Cushing), obésité hypothalamique, déficit en leptine." },
    
    # Complications
    { "question": "Quel pourcentage des diabétiques sont obèses ?", "answer": "75%." },
    { "question": "Quel est le RR de diabète si IMC > 30 ?", "answer": "RR = 10." },
    { "question": "Quel pourcentage des patients > 40 ans avec obésité sont hypertendus ?", "answer": "80%." },
    { "question": "Quelle est la prévalence de l'hypertrophie ventriculaire gauche si IMC > 30 ?", "answer": "Prévalence x 15." },
    { "question": "Quel pourcentage des patients atteints de SAS sont obèses ?", "answer": "60-70%." },
    { "question": "Quelles pathologies respiratoires sont liées à l'obésité ?", "answer": "Trouble ventilatoire restrictif/obstructif, hypoxémie, syndrome obésité-hypoventilation." },
    { "question": "Qu'est-ce que l'échelle d'Epworth ?", "answer": "Questionnaire évaluant la somnolence dans 8 situations quotidiennes, score 0-3 par situation." },
    { "question": "Quand réaliser une recherche de SAHOS ?", "answer": "IMC ≥ 30 avec signes évocateurs ou HTA résistante ; IMC ≥ 35 même sans symptômes." },
    { "question": "Comment diagnostique-t-on le SAHOS ?", "answer": "Par polygraphie ventilatoire, polysomnographie si doute." },
    { "question": "Quand réaliser des EFR dans l'obésité ?", "answer": "IMC ≥ 30 avec dyspnée de repos ou effort léger ; IMC ≥ 35 avec SAHOS ; IMC ≥ 40." },
    { "question": "Qu'est-ce que la NASH ?", "answer": "Stéato-hépatite non alcoolique, évolution de la stéatose hépatique." },
    { "question": "Quelle est la prévalence de la stéatose hépatique chez les obèses ?", "answer": "57-74%." },
    { "question": "Quel est le RR de gonarthrose en cas d'obésité ?", "answer": "RR de 2 à 6, surtout chez les femmes." },
    { "question": "L'obésité protège-t-elle d'une pathologie ?", "answer": "Oui, de l'ostéoporose." },
    { "question": "Comment dépister la maladie rénale chronique chez l'obèse ?", "answer": "Par estimation du DFG (CKD-EPI) et ratio albuminurie/créatininurie." },
    { "question": "Quel pourcentage des cancers est attribué à l'obésité ?", "answer": "3% chez l'homme, 6% chez la femme." },
    { "question": "Quels cancers ont un lien certain avec l'obésité ?", "answer": "Endomètre, sein, colorectal, rein." },
    { "question": "Quel est le RR de cancer de l'endomètre si IMC > 27 ?", "answer": "RR = 2,7." },
    
    # TCA et évaluation psycho-sociale
    { "question": "Quels sont les 3 grands TCA selon le DSM-5 ?", "answer": "Anorexie mentale, boulimie, accès hyperphagique (Binge-Eating Disorder)." },
    { "question": "Qu'est-ce que le test SCOFF ?", "answer": "Questionnaire de 5 questions pour détecter les TCA, 2 réponses positives = suspicion de TCA." },
    { "question": "Qu'est-ce que le questionnaire CRAC ?", "answer": "Cognitive Restriction Assessment check list, pour évaluer la restriction cognitive." },
    { "question": "Quels éléments psychiques évaluer dans l'obésité ?", "answer": "Troubles de l'humeur, anxiété, image du corps, estime de soi, psycho-traumatismes, addictions, TDAH." },
    { "question": "Qu'est-ce que la restriction cognitive ?", "answer": "Tendance à limiter consciemment la prise alimentaire pour maintenir ou perdre du poids." },
    
    # Activité physique et dépense énergétique
    { "question": "Quel questionnaire évalue l'activité physique ?", "answer": "Le GPAQ (Global Physical Activity Questionnaire)." },
    { "question": "Comment mesure-t-on la dépense énergétique de repos ?", "answer": "Par calorimétrie indirecte ou formule de Harris et Benedict." },
    { "question": "Quelle est la formule de Harris et Benedict pour l'homme ?", "answer": "66,473 + (5,003 × taille) + (13,752 × poids) – (6,755 × âge)." },
    { "question": "Quelle est la formule de Harris et Benedict pour la femme ?", "answer": "655,096 + (1,850 × taille) + (9,563 × poids) – (4,876 × âge)." },
    { "question": "Quelle est la dépense énergétique normale de base ?", "answer": "Femme : 1800 kcal, Homme : 2300 kcal, Grand sportif : 6000 kcal." },
    { "question": "Que provoque un régime très restrictif ?", "answer": "Une chute du métabolisme de base (ex: 1600 à 1300 kcal)." },
    
    # IV. Traitement
    { "question": "Pourquoi les régimes miracles échouent-ils à long terme ?", "answer": "La restriction calorique induit une baisse de la dépense énergétique de base qui ne revient pas à l'état antérieur." },
    { "question": "Quels sont les principes de l'approche diététique conseillée ?", "answer": "Maintenir plaisir alimentaire, retrouver le rythme, adapter apports, diversifier, lutter contre restriction cognitive." },
    { "question": "Quelle activité physique modérée est recommandée ?", "answer": "150 à 300 minutes/semaine d'intensité modérée (effort 5-6/10)." },
    { "question": "Quelle activité physique intense est recommandée ?", "answer": "75 à 150 minutes/semaine d'intensité vigoureuse (effort 7-8/10)." },
    { "question": "Quel renforcement musculaire est recommandé ?", "answer": "Au moins 2 jours/semaine touchant tous les groupes musculaires." },
    { "question": "Qu'est-ce que le Mediator et pourquoi a-t-il été retiré ?", "answer": "Médicament anti-obésité (1976-2009), retiré pour HTAP sévère, proche de l'amphétamine." },
    { "question": "Qu'est-ce que la Sibutramine et pourquoi a-t-elle été retirée ?", "answer": "Inhibiteur de recapture sérotonine/noradrénaline/dopamine, retiré en 2007 pour risque cardiovasculaire." },
    { "question": "Comment fonctionne l'Orlistat (Xenical) ?", "answer": "Inhibiteur des lipases gastro-intestinales, réduit l'absorption des graisses de 30%." },
    { "question": "Que sont les analogues au GLP-1 (AGLP-1) ?", "answer": "Traitements actuels majeurs : anti-diabétiques à faibles doses, anti-obésité à fortes doses." },
    { "question": "Quelles sont les indications du Saxenda (Liraglutide) ?", "answer": "IMC ≥ 30, ou IMC ≥ 27 avec comorbidité (dysglycémie, HTA, dyslipidémie, SAS)." },
    { "question": "Quel est le prix mensuel du Saxenda ?", "answer": "Environ 240 euros/mois (8-10 euros/jour), non remboursé." },
    { "question": "Quels sont les critères d'inclusion pour l'étude Wegovy ?", "answer": "IMC ≥ 40 avec comorbidité (HTA, dyslipidémie, MCV, SAS appareillé), sans alternative thérapeutique." },
    
    # Chirurgie bariatrique
    { "question": "Quelles sont les indications de la chirurgie bariatrique ?", "answer": "IMC ≥ 35 avec comorbidités ou IMC > 40, âge 18-60 ans, échec des traitements conventionnels depuis au moins 1 an." },
    { "question": "Quelles sont les opérations restrictives ?", "answer": "Anneau gastrique, gastroplastie de Mason, anneau de MacLean." },
    { "question": "Quelles sont les opérations malabsorptives ?", "answer": "By-pass bilio-pancréatique (Scopinaro), duodenal switch." },
    { "question": "Quelles sont les opérations mixtes ?", "answer": "By-pass gastrique, by-pass avec transection gastrique." },
    { "question": "En quelle année date l'anneau gastrique ?", "answer": "1986." },
    { "question": "Quel est le principe de l'anneau gastrique ?", "answer": "Création d'une poche de 15-20 ml, anneau gonflable relié à un boîtier sous-cutané." },
    { "question": "Quelles sont les complications de l'anneau gastrique ?", "answer": "Infections, rupture, glissement de boîtier, dilatation de la poche, inefficacité." },
    { "question": "Quel est le principe du by-pass gastrique ?", "answer": "Court-circuitage de l'estomac, duodénum et grêle sans exérèse." },
    { "question": "Quelle est la mortalité du by-pass gastrique ?", "answer": "1,5%." },
    { "question": "Qu'est-ce que le dumping syndrome ?", "answer": "Malaises, sueurs, palpitations, tachycardie, céphalées, nausées par arrivée rapide des aliments." },
    { "question": "Quelles sont les carences nutritionnelles post-chirurgie bariatrique ?", "answer": "Fer, folates, vitamine B12, protéines (<10%)." },
    
    # Messages clés HAS
    { "question": "Quel est le 1er message clé HAS ?", "answer": "Calculer l'IMC, mesurer le tour de taille et suivre annuellement leur évolution." },
    { "question": "Quel est le message HAS sur l'évaluation ?", "answer": "S'appuyer sur une évaluation multidimensionnelle et pluriprofessionnelle." },
    { "question": "Quel est le message HAS sur l'alimentation ?", "answer": "Repérer les perturbations alimentaires et les TCA." },
    { "question": "Quel est le message HAS sur le psychologique ?", "answer": "Évaluer et accompagner les difficultés psychologiques et toute vulnérabilité." },
    { "question": "Quel est le message HAS sur la stigmatisation ?", "answer": "Reconnaître, repérer, prévenir et accompagner toute stigmatisation." },
    { "question": "Quel est le message HAS sur l'ETP ?", "answer": "Proposer une éducation thérapeutique personnalisée dès le diagnostic, la poursuivre, la consolider." },
    { "question": "Quel est le message HAS sur le suivi ?", "answer": "Suivre régulièrement sur plusieurs années (non-complexe) ou à vie (complexe/très complexe)." },
    { "question": "Combien y a-t-il de messages clés HAS sur l'obésité ?", "answer": "14 messages clés." },
    
    # Conclusions
    { "question": "Quels facteurs prendre en compte dans l'obésité ?", "answer": "Facteurs alimentaires, hormonaux et génétiques." },
    { "question": "Quels objectifs thérapeutiques fixer avec le patient ?", "answer": "Objectifs réalistes, répondant à ses besoins, avec accompagnement dans la mise en œuvre." },
    { "question": "Quelle relation entre tabac et IMC ?", "answer": "Tabac + IMC faible ou Non-fumeur + IMC élevé = Risque de mortalité identique." },
]

FLASHCARDS_DYSLIPIDEMIE = [
    # I. Généralités
    { "question": "Quels sont les facteurs influençant les dyslipidémies ?", "answer": "Facteurs génétiques, alimentaires (type d'AG), HTA, diabète, obésité, sédentarité, alcool-tabac." },
    { "question": "Quelle est la 1ère cause de mortalité chez la femme en France ?", "answer": "Les maladies cardiovasculaires et AVC." },
    { "question": "Quelle est la 2ème cause de mortalité chez l'homme en France ?", "answer": "Les maladies cardiovasculaires et AVC." },
    { "question": "Combien de patients hospitalisés pour MCV/AVC en France en 2016 ?", "answer": "Plus d'1 million." },
    { "question": "Quel pourcentage des adultes français sont en surpoids/obésité en 2023 ?", "answer": "47,3% (dont 17% obèses)." },
    { "question": "Qu'est-ce qu'un lipide ?", "answer": "Corps gras présent dans l'alimentation et l'organisme." },
    { "question": "Qu'est-ce qu'un acide gras ?", "answer": "Unité de base des lipides, classé en 3 familles : saturés, monoinsaturés, polyinsaturés." },
    { "question": "Qu'est-ce qu'un triglycéride ?", "answer": "Molécule composée de glycérol et de 3 acides gras." },
    { "question": "Qu'est-ce qu'une lipoprotéine ?", "answer": "Grand complexe de protéines et de lipides (VLDL, IDL, LDL, chylomicrons)." },
    { "question": "Qu'est-ce que la prévention primaire ?", "answer": "Prévention pour éviter la survenue d'un premier évènement cardiovasculaire." },
    { "question": "Qu'est-ce que la prévention secondaire ?", "answer": "Prévention pour éviter la récidive d'un évènement (ex: après un infarctus)." },
    { "question": "Quelle consommation de lipides est conseillée pour un homme de 80 kg ?", "answer": "80 g par jour." },
    { "question": "Quel est le seuil de triglycérides pour la pancréatite aiguë ?", "answer": "10 g/L." },
    { "question": "Quel seuil de LDLc est conseillé après un infarctus ?", "answer": "< 0,55 g/L." },
    
    # II. Sources de lipides
    { "question": "Quelle est la différence entre graisses visibles et cachées ?", "answer": "Visibles : ajoutées (assaisonnement/cuisson) ; Cachées : dans la composition des aliments." },
    { "question": "Quel est l'apport calorique des lipides ?", "answer": "9 kcal/100 g." },
    { "question": "Quel est l'apport calorique de l'alcool ?", "answer": "7 kcal/100 g." },
    { "question": "Quelle est la formule générale des acides gras ?", "answer": "CH3-(CH2)n-COOH." },
    { "question": "Quel est l'effet des AG saturés ?", "answer": "Effet négatif, à restreindre." },
    { "question": "Quel est l'effet des AG monoinsaturés ?", "answer": "Effet intermédiaire." },
    { "question": "Quel est l'effet des AG polyinsaturés ?", "answer": "Effet positif." },
    { "question": "Qu'est-ce qu'un ω3 ?", "answer": "AG polyinsaturé avec double liaison au 3ème carbone." },
    { "question": "Quelles sources animales sont riches en AGS ?", "answer": "Viandes, charcuterie, produits laitiers, fromages." },
    { "question": "Quelles sources sont riches en MIS ?", "answer": "Volailles, huile d'olive, huile de colza." },
    { "question": "Quelles sources sont riches en PIS ω3 ?", "answer": "Poissons, colza, soja, lin, huile de poissons." },
    { "question": "Quelles sources sont riches en PIS ω6 ?", "answer": "Tournesol, maïs, pépin de raisin, soja." },
    { "question": "Quelle huile est riche en tous les types d'AG ?", "answer": "L'huile de noix : riche en PIS, peu de MIS, très peu d'AGS." },
    { "question": "Quel aliment est très riche en cholestérol ?", "answer": "Le beurre (250 mg/100g) et les œufs." },
    { "question": "À quoi sert le cholestérol dans l'organisme ?", "answer": "Synthèse d'acides biliaires, hormones stéroïdes, vitamine D, membranes, digestion." },
    { "question": "Comment sont transportés les lipides alimentaires après absorption ?", "answer": "Par les chylomicrons." },
    { "question": "Quel apport lipidique est recommandé pour 2000 kcal ?", "answer": "35-40% soit environ 70-80g de lipides par jour." },
    { "question": "Quelles sont les recommandations OMS sur l'alcool ?", "answer": "< 30 g/j homme, < 20 g/j femme ; < 10 verres/semaine, max 2/jour + jours sans." },
    { "question": "Quelles sont les conséquences de l'alcool chronique ?", "answer": "Hypertriglycéridémie, atteinte hépatique, pancréatite aiguë/chronique, cancers." },
    
    # III. Exploration des dyslipidémies
    { "question": "Qu'est-ce que l'EAL ?", "answer": "Exploration d'une Anomalie du bilan Lipidique : dosage de cholestérol total, LDLc, TG, HDL." },
    { "question": "Quand prescrit-on généralement un bilan lipidique ?", "answer": "Souvent après 40 ans, à jeun." },
    { "question": "Comment sont classées les dyslipidémies selon Fredrickson ?", "answer": "Classification biochimique selon les lipoprotéines en excès (types I à V)." },
    { "question": "Qu'est-ce qu'une hypercholestérolémie pure de type IIa ?", "answer": "LDLc > 1,60 g/L." },
    { "question": "Quand rechercher une mutation génétique ?", "answer": "Si taux LDLc > 1,9 g/L." },
    { "question": "Qu'est-ce qu'une hypertriglycéridémie pure de type IV ?", "answer": "TG > 1,5 g/L." },
    { "question": "Qu'est-ce qu'une hyperlipidémie mixte ?", "answer": "Association hypercholestérolémie et hypertriglycéridémie (types IIb et III)." },
    
    # Génétique
    { "question": "Quel est le taux de LDLc en mutation homozygote du récepteur LDL ?", "answer": "6-10 g/L." },
    { "question": "À quel âge surviennent les évènements CV en mutation homozygote ?", "answer": "À partir de 10 ans." },
    { "question": "Combien de cas de forme homozygote en France ?", "answer": "200 à 400 cas." },
    { "question": "Quel est le taux de LDLc en mutation hétérozygote ?", "answer": "2-4,5 g/L." },
    { "question": "À quel âge surviennent les évènements CV en mutation hétérozygote ?", "answer": "40-50 ans homme, 50-60 ans femme." },
    { "question": "Quelle est la prévalence de la forme hétérozygote ?", "answer": "1 personne sur 500 (130 000 personnes en France)." },
    
    # IV. Conséquences
    { "question": "Quels dépôts observe-t-on en hypercholestérolémie ?", "answer": "Arc cornéen, xanthélasma, xanthomes tendineux des extenseurs et du tendon d'Achille." },
    { "question": "Qu'est-ce que l'arc cornéen ?", "answer": "Dépôt lipidique autour de la cornée, valeur sémiologique avant 60 ans." },
    { "question": "Qu'est-ce que le xanthélasma ?", "answer": "Dépôt lipidique au-dessus et en-dessous des paupières." },
    { "question": "Quels signes observe-t-on en hypertriglycéridémie ?", "answer": "Syndrome hyperchylomicronémique, hépatomégalie, douleurs abdominales, xanthomatose éruptive, lipémie rétinienne." },
    { "question": "Comment se forme la plaque d'athérome ?", "answer": "Accumulation d'AG provoquant inflammation, puis de LDLc dans les cellules spumeuses de la paroi artérielle." },
    { "question": "Où se forment les plaques d'athérome ?", "answer": "Sur les carotides, coronaires, artères des jambes." },
    { "question": "À partir de quel âge peuvent se former les plaques ?", "answer": "À partir de 10 ans chez certains sujets." },
    { "question": "Qu'est-ce que l'AOMI ?", "answer": "Artériopathie oblitérante des membres inférieurs, causant une ischémie de membre." },
    { "question": "Quelle est l'évolution de la stéatose hépatique ?", "answer": "Stéatose → NASH → Fibrose → Cirrhose → Hépatocarcinome (sur 10-30 ans)." },
    { "question": "À partir de quel taux de TG risque-t-on une pancréatite aiguë ?", "answer": "TG > 10 g/L, surtout si > 30 g/L." },
    { "question": "Quelle est la 3ème cause de pancréatite aiguë ?", "answer": "Les dyslipidémies (après calculs biliaires et alcool)." },
    { "question": "Quelles pathologies causent une hypertriglycéridémie secondaire ?", "answer": "Diabète, obésité androïde, goutte, pathologies rénales, hypothyroïdie, alcoolisme." },
    { "question": "Quels médicaments peuvent causer une hypertriglycéridémie ?", "answer": "Corticoïdes, œstro-progestatifs, diurétiques thiazidiques, β-bloquants, antirétroviraux." },
    
    # V. Prise en charge
    { "question": "Quels sont les FDR cardiovasculaires non modifiables ?", "answer": "ATCD familiaux d'IDM/mort subite (<55 ans père, <65 ans mère), sexe masculin, âge >50 ans H/>60 ans F." },
    { "question": "Quels sont les FDR cardiovasculaires modifiables ?", "answer": "Tabac actif ou arrêté <3 ans, LDLc augmenté, HDLc <0,4 g/L, HTA, diabète, IRC." },
    { "question": "Comment calcule-t-on le risque SCORE ?", "answer": "Tables utilisant âge, sexe, tabac, pression artérielle systolique, ratio CT/HDL." },
    { "question": "Quels sont les niveaux de risque SCORE ?", "answer": "Négligeable <1%, proche de 5%, très élevé >10%." },
    { "question": "Quel LDLc cible si risque <1% ?", "answer": "Jusqu'à 1,16 g/L." },
    { "question": "Quel LDLc cible si risque modéré ?", "answer": "Jusqu'à 1 g/L." },
    { "question": "Quel LDLc cible si risque élevé ?", "answer": "Jusqu'à 0,7 g/L." },
    { "question": "Quel LDLc cible si risque très élevé ?", "answer": "Jusqu'à 0,55 g/L." },
    { "question": "Quel LDLc cible si 1er évènement CV avant 2 ans ?", "answer": "Jusqu'à 0,4 g/L." },
    { "question": "Quelle durée de régime avant traitement médicamenteux ?", "answer": "3 mois de régime diététique bien conduit." },
    { "question": "Quels sont les objectifs diététiques ?", "answer": "Lipides <35% apport calorique, AGS <10%, privilégier MIS, ω3, cholestérol <300 mg/j." },
    
    # VI. Traitements
    { "question": "Comment fonctionnent les statines ?", "answer": "Inhibiteurs de l'HMG-CoA réductase, diminuent production hépatique de cholestérol et VLDL." },
    { "question": "Quelle réduction de LDLc obtient-on avec les statines ?", "answer": "25-60% selon la dose (30% dose modérée, 50% dose élevée)." },
    { "question": "Quels sont les effets secondaires des statines ?", "answer": "Myalgies, rhabdomyolyse." },
    { "question": "Quelles statines ne passent pas par le cytochrome P450 ?", "answer": "Pravastatine (Elisor) et Rosuvastatine (Crestor)." },
    { "question": "Quelles sont les 2 statines les plus efficaces ?", "answer": "Atorvastatine et Rosuvastatine." },
    { "question": "Comment fonctionne l'Ézétimibe ?", "answer": "Inhibiteur spécifique de l'absorption du cholestérol au niveau de l'entérocyte." },
    { "question": "Quelle réduction de LDLc avec Ézétimibe + statine ?", "answer": "15-19% supplémentaires." },
    { "question": "Quand utilise-t-on l'Ézétimibe ?", "answer": "En cas d'échec ou intolérance aux statines, en association ou monothérapie." },
    { "question": "Comment fonctionnent les anti-PCSK9 ?", "answer": "Anticorps antagonisant PCSK9, augmentant les récepteurs au LDLc sur les hépatocytes." },
    { "question": "Quelle réduction de LDLc avec anti-PCSK9 seuls ?", "answer": "60%." },
    { "question": "Quelle réduction de LDLc avec anti-PCSK9 + statine + ézétimibe ?", "answer": "85%." },
    { "question": "Comment fonctionnent les fibrates ?", "answer": "Inhibition de la synthèse hépatique des VLDL via liaison à PPAR alpha." },
    { "question": "Quelle indication principale pour les fibrates ?", "answer": "Hypertriglycéridémie pure en 1ère intention." },
    { "question": "Quelle est l'action de l'acide nicotinique ?", "answer": "Augmente significativement le HDLc (15-20%)." },
    { "question": "Comment fonctionne la Cholestyramine ?", "answer": "Résine échangeuse interrompant le cycle entéro-hépatique, stimulant les récepteurs hépatiques au LDLc." },
    { "question": "Quelle contre-indication pour la Cholestyramine ?", "answer": "L'hypertriglycéridémie." },
    
    # VII. Conclusion
    { "question": "Résumer l'alimentation et le bilan lipidique.", "answer": "L'alimentation apporte cholestérol et AG, le bilan à jeun dose CT, LDLc, TG, HDLc." },
    { "question": "Comment évaluer le risque cardiovasculaire global ?", "answer": "Par les tables SCORE pour décider du traitement diététique puis médicamenteux." },
    { "question": "Quel est le seuil LDLc en très haut risque vasculaire ?", "answer": "< 0,55 g/L (nouveau seuil)." },
    { "question": "Quel est le traitement de 1ère intention des dyslipidémies ?", "answer": "Les statines." },
]

FLASHCARDS_RELATIONS_NUTRITION_SANTE = [
    # II. Épidémiologie des MNT
    { "question": "Qu'est-ce que la prévalence ?", "answer": "Indicateur statique de morbidité : proportion de cas d'une maladie à un instant donné sur la population." },
    { "question": "Qu'est-ce que l'incidence ?", "answer": "Indicateur dynamique de morbidité : nombre de nouveaux cas apparus pendant une période donnée." },
    { "question": "Qu'est-ce que la standardisation ?", "answer": "Méthode permettant de comparer des données en s'affranchissant des effets de la structure d'âge." },
    { "question": "Quelles sont les principales causes de mortalité dans le monde ?", "answer": "Maladies non transmissibles (auparavant 50/50 avec transmissibles)." },
    { "question": "Quel pourcentage des décès en France en 2021 représentent les cancers ?", "answer": "25,7%." },
    { "question": "Quel pourcentage des décès représentent les maladies cardio-neurovasculaires ?", "answer": "20,9%." },
    { "question": "Comment évolue la mortalité par MNT sur le long terme ?", "answer": "Diminution globale, surtout pour les maladies cardio-circulatoires." },
    { "question": "Comment évolue l'incidence du cancer du poumon chez la femme ?", "answer": "En augmentation, due à l'augmentation du tabagisme féminin." },
    { "question": "Comment évolue l'incidence du cancer de la prostate ?", "answer": "En baisse, grâce aux dépistages précoces." },
    { "question": "Quelle est la prévalence globale du diabète en France ?", "answer": "5%." },
    { "question": "Quel pourcentage des adultes français est en surpoids ou obèse ?", "answer": "Plus de 50%." },
    { "question": "Quelle est la position de la France pour l'obésité en Europe ?", "answer": "En dessous de la moyenne européenne." },
    { "question": "Qu'a montré l'étude ESTEBAN 2014-2015 ?", "answer": "Stabilisation de la prévalence du surpoids et de l'obésité." },
    { "question": "Quel impact a eu le Covid-19 sur l'obésité infantile ?", "answer": "Évolution défavorable : les pourcentages ont doublé dans le Val de Marne." },
    
    # Inégalités sociales de santé
    { "question": "Qu'est-ce que les déterminants sociaux de la santé ?", "answer": "Circonstances dans lesquelles les individus naissent, grandissent, vivent, travaillent et vieillissent." },
    { "question": "Qu'est-ce que le gradient social de santé ?", "answer": "L'état de santé varie selon les déterminants sociaux de façon progressive." },
    { "question": "Comment varie l'espérance de vie selon le revenu ?", "answer": "Plus le revenu augmente, plus l'espérance de vie augmente." },
    { "question": "Quelle est la différence d'espérance de vie entre premier et dernier vingtile de revenu ?", "answer": "13,1 ans pour les hommes, 8,3 ans pour les femmes." },
    { "question": "Comment varie la prévalence du surpoids selon l'éducation ?", "answer": "30% si >bac+3, 60% si pas de bac." },
    
    # III. Élaboration des recommandations
    { "question": "Qu'est-ce que l'Evidence-Based Medicine ?", "answer": "Médecine fondée sur les preuves : formuler un problème, rechercher la littérature, évaluer et utiliser les résultats." },
    { "question": "Quels sont les niveaux de preuve scientifique ?", "answer": "4 niveaux du meilleur au plus faible, classant les types d'études." },
    { "question": "Qu'est-ce qu'une méta-analyse ?", "answer": "Analyse combinée de plusieurs études, représentée par un forest plot." },
    { "question": "Qu'est-ce que le risque relatif (RR) ?", "answer": "Rapport entre le risque chez les exposés et chez les non exposés." },
    { "question": "Comment interpréter un RR = 1 ?", "answer": "Pas de lien entre exposition et maladie." },
    { "question": "Comment interpréter un RR < 1 ?", "answer": "L'exposition est un facteur protecteur." },
    { "question": "Comment interpréter un RR > 1 ?", "answer": "L'exposition est un facteur de risque." },
    { "question": "Qu'est-ce que la fraction de risque attribuable ?", "answer": "Proportion des malades exposés dont la maladie peut être attribuée à l'exposition." },
    { "question": "Quelles sont les instances d'expertise en nutrition au niveau national ?", "answer": "ANSES, Santé Publique France." },
    { "question": "Quelles sont les instances internationales en nutrition-cancer ?", "answer": "WCRF (World Cancer Research Fund), IARC." },
    
    # IV. Relations nutrition/maladies cardio-métaboliques
    { "question": "Quelle est la part attribuable aux facteurs alimentaires dans la mortalité MNT ?", "answer": "11%." },
    { "question": "Quelle est la part attribuable à la pression artérielle ?", "answer": "14,8%." },
    { "question": "Quelle est la part attribuable à l'IMC ?", "answer": "8%." },
    { "question": "Quel est le RR de maladie coronaire pour chaque 200g de fruits et légumes ?", "answer": "RR = 0,92 (diminution de 8%)." },
    { "question": "Pourquoi les fruits et légumes protègent-ils du risque CV ?", "answer": "Riches en fibres, vitamines, antioxydants → réduction cholestérol, PA, amélioration fonction vasculaire." },
    { "question": "Quel est le RR de MCV pour 90g de céréales complètes ?", "answer": "RR = 0,78 (diminution de 22%)." },
    { "question": "Pourquoi les céréales complètes protègent-elles ?", "answer": "Riches en fibres, vitamines B et E → activité antioxydante, régulation glycémique." },
    { "question": "Quel est le RR de mortalité CV pour la viande/charcuterie ?", "answer": "RR = 1,23 (augmentation de 23%)." },
    { "question": "Pourquoi la viande/charcuterie augmente-t-elle le risque CV ?", "answer": "Riche en AGS, AG trans, sel → hypercholestérolémie, dysfonction endothéliale, insulinorésistance." },
    { "question": "Quel est le RR de MCV par verre de boisson sucrée ?", "answer": "RR = 1,08 (augmentation de 8%)." },
    { "question": "Pourquoi les boissons sucrées augmentent-elles le risque CV ?", "answer": "Riches en sucres libres → excès énergétique, obésité, insulinorésistance." },
    { "question": "Quels sont les facteurs de risque de diabète de type 2 ?", "answer": "Viande/charcuterie, protéines animales, fast-food, boissons sucrées et édulcorées." },
    { "question": "Quels sont les facteurs de protection du diabète de type 2 ?", "answer": "Céréales complètes, fibres, fruits et légumes." },
    { "question": "Qu'est-ce que la balance énergétique ?", "answer": "Équilibre entrées = sorties ; si entrées > sorties → prise de poids." },
    { "question": "Quels facteurs nutritionnels favorisent l'obésité ?", "answer": "Sédentarité, grignotage, produits haute densité énergétique, boissons sucrées, tailles de portion." },
    
    # V. Relations nutrition/Cancer
    { "question": "Quelles sont les étapes de la cancérogénèse chimique ?", "answer": "Initiation (mutations), promotion (multiplication cellules anormales), progression (métastases)." },
    { "question": "Quels facteurs alimentaires interviennent dans la cancérogénèse ?", "answer": "Ils agissent à tous les niveaux : génétique, épigénétique, métabolique, hormonal, inflammation, microbiote." },
    { "question": "Quels sont les facteurs de risque nutritionnels de cancer ?", "answer": "Alcool, surpoids/obésité, viande rouge/charcuterie, sel, compléments de bêtacarotène." },
    { "question": "Quels sont les facteurs de protection nutritionnels de cancer ?", "answer": "Fruits et légumes, fibres, produits laitiers, activité physique." },
    { "question": "Quels cancers sont liés à l'alcool ?", "answer": "Cancers de la bouche, pharynx, larynx, œsophage, foie, sein, colorectal." },
    { "question": "Quels cancers sont liés au surpoids/obésité ?", "answer": "Cancers de l'œsophage, pancréas, foie, colorectal, sein, endomètre, rein." },
    { "question": "Quels cancers sont liés à la viande rouge/charcuterie ?", "answer": "Cancer colorectal." },
    { "question": "Quels cancers les produits laitiers protègent-ils ?", "answer": "Cancer colorectal." },
    { "question": "Quels cancers l'activité physique protège-t-elle ?", "answer": "Cancers du côlon, sein, endomètre." },
    
    # VI. Déterminants du comportement alimentaire
    { "question": "Quels sont les déterminants environnementaux du comportement alimentaire ?", "answer": "Offre alimentaire, marketing alimentaire, prix des produits." },
    { "question": "Comment se répartissent les fast-foods géographiquement ?", "answer": "Ils se concentrent dans les aires les plus défavorisées." },
    { "question": "Qu'est-ce que la 'marchabilité' de l'environnement ?", "answer": "Présence de trottoirs sécurisés et de commerces de proximité favorisant les déplacements actifs." },
    { "question": "Comment l'environnement 'marchable' influence-t-il la santé ?", "answer": "Plus l'environnement est marchable, plus l'activité physique (notamment la marche) augmente." },
    { "question": "Quels produits représente majoritairement la publicité alimentaire ?", "answer": "Les produits gras, salés, sucrés." },
    { "question": "Comment les tailles de portion influencent-elles la santé ?", "answer": "Les tailles ont augmenté, induisant un risque d'excès calorique et de prise de poids." },
    { "question": "Quels sont les comportements alimentaires des personnes défavorisées ?", "answer": "Moins de fruits/légumes/poisson, plus de produits gras/salés/sucrés, moins d'activité physique." },
    { "question": "Quel est l'objectif des actions de santé publique en nutrition ?", "answer": "Rendre le choix sain le choix simple." },
]

FLASHCARDS_CARYOTYPE = [
    # I. Chromosomes
    { "question": "Qu'est-ce qu'un chromosome à l'état condensé ?", "answer": "Filament d'ADN fortement enroulé et compacté autour des histones." },
    { "question": "Quand étudie-t-on le mieux les chromosomes ?", "answer": "En métaphase de la mitose, en microscopie optique." },
    { "question": "Qu'est-ce que la chromatine ?", "answer": "1 molécule d'ADN (1,8 m) associée à des protéines histones, sous forme de nucléosomes." },
    { "question": "Qu'est-ce qu'un nucléosome ?", "answer": "Octamère d'histones (2H2A, 2H2B, 2H3, 2H4) autour duquel s'enroule l'ADN, structure de base de la chromatine." },
    { "question": "Quelles sont les fonctions du chromosome ?", "answer": "Support de l'information génétique, porte les gènes, répartition égale entre cellules filles." },
    { "question": "Quels sont les 4 stades du cycle cellulaire ?", "answer": "Prophase, métaphase, anaphase, interphase." },
    { "question": "Combien de chromosomes dans un zygote humain normal ?", "answer": "46 chromosomes (diploïde ou euploïde)." },
    { "question": "Quelle est la formule chromosomique d'une fille ?", "answer": "46, XX." },
    { "question": "Quelle est la formule chromosomique d'un garçon ?", "answer": "46, XY." },
    { "question": "Qu'est-ce qu'un autosome ?", "answer": "Un chromosome non sexuel (44 autosomes chez l'humain)." },
    { "question": "Qu'est-ce qu'un gonosome ?", "answer": "Un chromosome sexuel (X ou Y)." },
    { "question": "Qu'est-ce qu'une cellule aneuploïde ?", "answer": "Cellule avec un nombre de chromosomes différent de 46." },
    { "question": "Comment s'obtiennent les bandes G ?", "answer": "Par traitement enzymatique à la trypsine (GTG)." },
    { "question": "Comment s'obtiennent les bandes R ?", "answer": "Par traitement par la chaleur (RHG)." },
    { "question": "Quels sont les critères de classement des chromosomes ?", "answer": "Taille, position du centromère, forme, banding." },
    { "question": "Qu'est-ce que le centromère ?", "answer": "Point d'union des deux chromatides d'un chromosome." },
    { "question": "Qu'est-ce qu'un télomère ?", "answer": "Extrémité d'un chromosome." },
    { "question": "Qu'est-ce que le bras p ?", "answer": "Le bras court d'un chromosome." },
    { "question": "Qu'est-ce que le bras q ?", "answer": "Le bras long d'un chromosome." },
    
    # II. Caryotype - Réalisation
    { "question": "Sur quel type de cellule peut-on établir un caryotype ?", "answer": "Toute cellule nucléée en division." },
    { "question": "Quel prélèvement est le plus simple pour un caryotype ?", "answer": "Sang veineux périphérique (prise de sang)." },
    { "question": "Quel anticoagulant utilise-t-on pour le prélèvement sanguin ?", "answer": "Héparine." },
    { "question": "Qu'est-ce que la phytohémagglutinine ?", "answer": "Lectine mitogène qui provoque la croissance et division des lymphocytes." },
    { "question": "Combien de temps incube-t-on le sang pour un caryotype ?", "answer": "72 heures." },
    { "question": "Comment prélève-t-on le liquide amniotique ?", "answer": "Par amniocentèse, sous contrôle échographique, en conditions stériles." },
    { "question": "Quelle est la couleur normale du liquide amniotique ?", "answer": "Jaune citrin." },
    { "question": "Combien de temps met-on en culture les cellules de liquide amniotique ?", "answer": "6 à 10 jours." },
    { "question": "Quel agent bloque les cellules en métaphase ?", "answer": "La colchicine, poison du fuseau mitotique qui empêche la polymérisation de la tubuline." },
    { "question": "À quoi sert le choc hypotonique ?", "answer": "Gonflermenter les cellules et fragiliser la membrane pour étaler les chromosomes." },
    { "question": "Quel mélange utilise-t-on pour le choc hypotonique ?", "answer": "Chlorure de potassium et eau distillée." },
    { "question": "Quel mélange utilise-t-on pour la fixation ?", "answer": "Acide acétique et éthanol ou méthanol." },
    { "question": "Qu'est-ce qu'un idéogramme ?", "answer": "Schéma modèle servant à vérifier le banding d'un chromosome." },
    
    # Critères de classement
    { "question": "Quelle est la formule du rapport centromérique ?", "answer": "Rc = p/(p + q) × 100." },
    { "question": "Qu'est-ce qu'un chromosome métacentrique ?", "answer": "Chromosome avec bras p et q de même taille, Rc ≈ 50%." },
    { "question": "Quels chromosomes sont métacentriques ?", "answer": "1, 3, 16, 19 et 20." },
    { "question": "Qu'est-ce qu'un chromosome submétacentrique ?", "answer": "Chromosome avec bras p court et q long, Rc < 50%." },
    { "question": "Qu'est-ce qu'un chromosome acrocentrique ?", "answer": "Chromosome avec Rc ≈ 0%, bras courts quasi-inexistants." },
    { "question": "Quels chromosomes sont acrocentriques ?", "answer": "13, 14, 15, 21 et 22." },
    { "question": "Que portent les bras courts des chromosomes acrocentriques ?", "answer": "Des segments impliqués dans la synthèse des ARNr, présents à plusieurs centaines d'exemplaires." },
    { "question": "Qu'est-ce que l'ISCN ?", "answer": "International System for Cytogenetic Nomenclature." },
    { "question": "Quelle est la localisation du gène CFTR ?", "answer": "7q31 (chromosome 7, bras long, région 3, bande 1)." },
    
    # Indications du caryotype
    { "question": "Quelles sont les indications prénatales du caryotype ?", "answer": "Anomalie chromosomique parentale, signes d'appel échographiques, marqueurs sériques >1/250." },
    { "question": "Qu'est-ce que le DPNI ?", "answer": "Diagnostic prénatal non invasif, beaucoup plus sensible et spécifique (proche de 100%)." },
    { "question": "Qu'est-ce que la choriocentèse ?", "answer": "Ponction de villosités choriales, diagnostic précoce dès 12 SA." },
    { "question": "Qu'est-ce que l'amniocentèse ?", "answer": "Ponction de liquide amniotique, réalisée plus tardivement." },
    { "question": "Qu'est-ce que la cordocentèse ?", "answer": "Prélèvement de sang fœtal au cordon, rarement utilisé (risque de fausse couche)." },
    { "question": "Quand est indiqué un caryotype chez l'enfant ?", "answer": "Malformations à la naissance, retard mental, retard de développement." },
    { "question": "Quand est indiqué un caryotype chez l'adolescent ?", "answer": "Anomalies de croissance, retard pubertaire." },
    { "question": "Quand est indiqué un caryotype chez un couple ?", "answer": "Bilan d'infertilité (>2 ans), fausses couches, enfant né avec anomalie chromosomique." },
]

FLASHCARDS_METHODES_ETUDE = [
    # I. Tissus
    { "question": "Quelle est l'étymologie du mot histologie ?", "answer": "Du grec histos (tissus) et logos (science)." },
    { "question": "Qui a créé le mot histologie ?", "answer": "Mayer et Heusinger en Allemagne à la fin du XIXème siècle." },
    { "question": "Qui a fait les premières descriptions histologiques ?", "answer": "Marcelo Malpighi au milieu du 17ème siècle." },
    { "question": "Qui a inventé les premiers microscopes ?", "answer": "Zacharias Janssen en 1590." },
    { "question": "Qu'étudie l'histologie ?", "answer": "Structure, composition, fonctionnement, renouvellement et échanges cellulaires des tissus." },
    { "question": "De quoi sont exclusivement constitués les tissus ?", "answer": "De cellules et de matrice extracellulaire." },
    { "question": "Combien de cellules compte l'organisme humain ?", "answer": "Dizaines de trillions (10^13) de cellules." },
    { "question": "Quel est le premier niveau d'organisation supra-cellulaire ?", "answer": "Les tissus." },
    
    # II. Niveaux d'organisation
    { "question": "Quels sont les niveaux d'organisation du plus simple au plus complexe ?", "answer": "Atomes → Molécules → Organites → Cellules → Tissus → Organes → Systèmes/Appareils." },
    { "question": "Quelle discipline étudie les molécules ?", "answer": "La biochimie." },
    { "question": "Quelle discipline étudie les cellules ?", "answer": "La cytologie ou biologie cellulaire." },
    { "question": "Quelle discipline étudie les organes ?", "answer": "L'anatomie." },
    
    # III. Échelles
    { "question": "Quelle est la limite de résolution de l'œil humain ?", "answer": "0,2 mm = 200 μm." },
    { "question": "Quel est le diamètre d'un atome d'hydrogène ?", "answer": "Environ 0,1 nm = 10^-10 m." },
    { "question": "Quel est le diamètre de la double hélice d'ADN ?", "answer": "2 nm." },
    { "question": "Quelle est la taille d'un chromosome en métaphase ?", "answer": "1 à 10 μm." },
    { "question": "Quelle est la taille des cellules ?", "answer": "5 à 100 μm." },
    { "question": "Combien vaut 1 μm ?", "answer": "1/1000 de mm = 10^-6 m." },
    { "question": "Combien vaut 1 nm ?", "answer": "1/1 000 000 de mm = 10^-9 m." },
    
    # IV. Types de microscope
    { "question": "Quel est le pouvoir séparateur du microscope optique ?", "answer": "0,2 μm = 200 nm." },
    { "question": "Qu'utilise le microscope optique ?", "answer": "Un faisceau lumineux de photons." },
    { "question": "Quel est le pouvoir séparateur du microscope électronique ?", "answer": "0,2 nm." },
    { "question": "Qu'utilise le microscope électronique ?", "answer": "Un faisceau d'électrons." },
    { "question": "Que permet d'observer le microscope électronique ?", "answer": "Les cellules et les organites (mitochondries, REG, ADN, nucléosomes)." },
    
    # V. Étapes de préparation
    { "question": "Qu'est-ce qu'une biopsie ?", "answer": "Fragment d'organe prélevé lors d'une endoscopie." },
    { "question": "Qu'est-ce qu'une pièce opératoire ?", "answer": "Fragment d'organe prélevé lors d'une intervention chirurgicale." },
    { "question": "Quel fixateur utilise-t-on en histologie ?", "answer": "Formol ou paraformaldéhyde." },
    { "question": "Pourquoi fixe-t-on les tissus ?", "answer": "Pour immobiliser les constituants, prévenir l'autolyse et la putréfaction." },
    { "question": "Quelle est la vitesse de pénétration du formol ?", "answer": "1 mm/heure." },
    { "question": "Comment déshydrate-t-on les tissus ?", "answer": "Bains d'alcool de plus en plus concentrés, puis xylène ou toluène." },
    { "question": "Dans quoi inclut-on les tissus ?", "answer": "Dans la paraffine liquide." },
    { "question": "Quelle est l'épaisseur des coupes en microscopie optique ?", "answer": "2 à 5 μm." },
    { "question": "Quel appareil permet de faire des coupes fines ?", "answer": "Le microtome (ou cryostat si tissu congelé)." },
    { "question": "Quelles sont les étapes après la coupe ?", "answer": "Déparaffinage, réhydratation, coloration, montage." },
    
    # Colorations
    { "question": "Quelle est la coloration la plus courante en histologie ?", "answer": "Hématoxyline-Éosine (HE)." },
    { "question": "Qu'est-ce que l'hématoxyline ?", "answer": "Colorant basique se fixant aux acides nucléiques (noyaux et REG en violet)." },
    { "question": "Qu'est-ce que l'éosine ?", "answer": "Colorant acide se fixant aux protéines (cytoplasmes et fibres en rose)." },
    { "question": "Que colore le safran dans le HES ?", "answer": "Les fibres de collagène en jaune." },
    { "question": "Qu'est-ce que le trichrome de Masson ?", "answer": "Coloration identifiant les pathologies musculaires, cardiaques, hépatiques, rénales : cytoplasmes rouge, collagène vert." },
    { "question": "Que colore le Bleu Alcian ?", "answer": "Les mucopolysaccharides acides en bleu." },
    { "question": "Que colore le PAS ?", "answer": "Les glucides, glycogènes, glycoprotéines en rouge pourpre." },
    { "question": "Que colore l'orcéine ?", "answer": "Les fibres élastiques des tissus conjonctifs en gris noir." },
    { "question": "Que colore l'argent ?", "answer": "Les fibres de collagène type III (réticulées) en gris noir." },
    
    # VI. Tissus fondamentaux
    { "question": "Sur quoi repose la classification des tissus ?", "answer": "Sur leur structure et fonction, pas leur origine embryologique." },
    { "question": "Quels sont les 4 groupes de tissus fondamentaux ?", "answer": "Épithélial, conjonctif/soutien, musculaire, nerveux." },
    { "question": "Quelles sont les caractéristiques du tissu épithélial ?", "answer": "Cellules jointives, fonction de revêtement et sécrétion." },
    { "question": "Où trouve-t-on du tissu épithélial ?", "answer": "Épiderme, muqueuses, glandes." },
    { "question": "Quelles sont les caractéristiques du tissu conjonctif ?", "answer": "Cellules non jointives dans un réseau de fibres et substance fondamentale." },
    { "question": "Quelles sont les fonctions du tissu conjonctif ?", "answer": "Contact entre structures, soutien statique, stockage, transport." },
    { "question": "Où trouve-t-on du tissu conjonctif ?", "answer": "Cartilage, os, ligaments, tendons, tissu adipeux, sang." },
    { "question": "Quelles sont les caractéristiques du tissu musculaire ?", "answer": "Cellules contractiles, fonction de mouvement." },
    { "question": "Où trouve-t-on du tissu musculaire ?", "answer": "Muscles squelettiques, cœur, parois vasculaires, organes creux." },
    { "question": "Quelles sont les caractéristiques du tissu nerveux ?", "answer": "Neurones conduisant l'influx, cellules gliales de soutien." },
    { "question": "Quelles sont les fonctions du tissu nerveux ?", "answer": "Recueil, traitement, stockage, envoi d'informations ; commande des fonctions." },
    { "question": "Où trouve-t-on du tissu nerveux ?", "answer": "Cerveau, moelle spinale, nerfs périphériques, organes des sens." },
]

FLASHCARDS_INTRODUCTION_NUTRITION = [
    # I. Introduction
    { "question": "Que disait Hippocrate sur la nutrition ?", "answer": "'Que l'alimentation soit votre première médecine' (460-370 av JC)." },
    { "question": "De quelles maladies une alimentation équilibrée protège-t-elle ?", "answer": "Cancer, maladies cardiovasculaires, ostéoporose, diabète, obésité." },
    
    # II. Démarches scientifiques
    { "question": "Qu'est-ce que le PNNS ?", "answer": "Programme National Nutrition Santé, objectif d'améliorer la santé via la nutrition." },
    { "question": "Que comprend le concept de nutrition du PNNS ?", "answer": "L'alimentation (aliments, comportement) et l'activité physique." },
    { "question": "Qu'est-ce que le CLAN ?", "answer": "Comité de Liaison Alimentation Nutrition, pour surveiller et adapter l'alimentation des malades à l'hôpital." },
    { "question": "Quels marqueurs de dénutrition dose-t-on ?", "answer": "Albumine et pré-albumine sériques." },
    
    # III. Aliments et nutriments
    { "question": "Qu'est-ce qu'un aliment selon l'UE ?", "answer": "Toute substance ou produit destiné à être ingéré par l'être humain (définition 2002)." },
    { "question": "Qu'est-ce qu'un nutriment ?", "answer": "Substance organique ou minérale directement assimilable sans digestion." },
    { "question": "Quels sont les macronutriments ?", "answer": "Glucides, lipides, protéines." },
    { "question": "Quels sont les micronutriments ?", "answer": "Minéraux, oligo-éléments, vitamines." },
    { "question": "Quels sont les minéraux principaux ?", "answer": "Na, Cl, K, Ca, P, Mg." },
    { "question": "Quels sont les oligo-éléments essentiels ?", "answer": "Zn, Fe, Mn, Cu, I, Mo, Cr, Se." },
    { "question": "Quelles sont les vitamines liposolubles ?", "answer": "A, D, E, K." },
    { "question": "Quelles sont les vitamines hydrosolubles ?", "answer": "B et C." },
    { "question": "Pourquoi les micronutriments sont-ils indispensables ?", "answer": "L'organisme ne peut pas les fabriquer ; ils assurent l'assimilation et l'utilisation des macronutriments." },
    { "question": "D'où proviennent les déséquilibres alimentaires ?", "answer": "De l'environnement (disponibilité, climat, tabous) et de l'individu (comportement, activité, génétique)." },
    
    # Étude britannique
    { "question": "Que mesure l'étude britannique de 2008 ?", "answer": "L'impact du mode de vie sur l'espérance de vie (20000 sujets, 45-79 ans, 11 ans)." },
    { "question": "Quels sont les 4 facteurs de risque scorés ?", "answer": "Fumer, >2 verres d'alcool/j, <5 fruits/légumes/j (vit C <50mM/L), <30 min exercice/j." },
    { "question": "Quel est l'intérêt de cette étude ?", "answer": "Première étude quantifiant le bénéfice d'une vie saine en terme de survie." },
    
    # Rôle des nutriments
    { "question": "Quels nutriments sont énergétiques ?", "answer": "Lipides, glucides, acides aminés." },
    { "question": "Quels nutriments ont un rôle structural ?", "answer": "Lipides, glucides, acides aminés, éléments minéraux (Ca, P)." },
    { "question": "Quels nutriments régulent le métabolisme ?", "answer": "Vitamines (cofacteurs enzymatiques), éléments minéraux (pression osmotique), oligo-éléments." },
    { "question": "Comment les métaux se lient-ils aux protéines ?", "answer": "Par liaison ionique (Na, K, Ca) ou de coordination (enzymes métalloprotéinases)." },
    { "question": "Quel est le rôle mécanique des aliments ?", "answer": "Les fibres alimentaires (cellulose) assurent le péristaltisme intestinal." },
    { "question": "Quel est le rôle sensoriel des aliments ?", "answer": "Arômes, colorants, agents de texture influencent l'appétence." },
    
    # IV. L'eau
    { "question": "Pourquoi l'eau est-elle essentielle ?", "answer": "Solvant, réactif pour processus biologiques, échanges osmotiques et thermiques." },
    { "question": "Quels sont les besoins hydriques quotidiens pour 60 kg ?", "answer": "2,8 litres (1-1,5L boissons, 1,2L aliments, 0,3-0,4L production endogène)." },
    { "question": "Que traduit la soif ?", "answer": "Une perte de 3-5% du stock hydrique (phénomène tardif)." },
    { "question": "Quel impact a 2% de perte hydrique ?", "answer": "20% de diminution des capacités physiques." },
    
    # V. Vitamines
    { "question": "Qu'est-ce qu'une vitamine ?", "answer": "Substance nécessaire au métabolisme que l'Homme ne peut pas synthétiser en quantité suffisante." },
    { "question": "Quels sont les besoins journaliers en vitamines ?", "answer": "Du μg à plusieurs mg selon les vitamines." },
    { "question": "Qu'est-ce que l'hypovitaminose ?", "answer": "Apport insuffisant en vitamine." },
    { "question": "Qu'est-ce que l'avitaminose ?", "answer": "Absence de vitamine causant des maladies." },
    { "question": "Quelle maladie cause la carence en vitamine C ?", "answer": "Le scorbut." },
    { "question": "Quelle maladie cause la carence en vitamine D ?", "answer": "Le rachitisme." },
    { "question": "Quelle maladie cause la carence en vitamine B1 ?", "answer": "Le béri-béri." },
    { "question": "Quelles vitamines peuvent être toxiques en excès ?", "answer": "Les vitamines A et D (hypervitaminose)." },
    { "question": "Quelles sont les sources de vitamines B ?", "answer": "Céréales, abats." },
    { "question": "Où trouve-t-on la pro-vitamine A (β-carotène) ?", "answer": "Dans les légumes : carottes, épinards, persil, cresson." },
    { "question": "Où trouve-t-on la vitamine K1 ?", "answer": "Légumes verts (brocolis, choux, épinards, laitue), liée aux chloroplastes." },
    { "question": "D'où vient la vitamine K2 ?", "answer": "De la synthèse intestinale par la flore bactérienne." },
    { "question": "Où trouve-t-on les vitamines E et F ?", "answer": "Dans les graines oléagineuses." },
    { "question": "Où abonde la vitamine C ?", "answer": "Fruits et légumes : agrumes, tomates, poivrons." },
    { "question": "Pourquoi la vitamine D n'est-elle pas vraiment une vitamine ?", "answer": "Elle est synthétisée par l'organisme sous l'effet du soleil, mais pas en quantité suffisante." },
    
    # Scorbut
    { "question": "Comment appelait-on le scorbut ?", "answer": "'La peste des mers' (maladie des marins au long cours)." },
    { "question": "Quand date la première description du scorbut ?", "answer": "1600 av. J.C. (Papyrus d'Ebers)." },
    { "question": "Quels sont les signes du scorbut ?", "answer": "Asthénie, œdème, arthralgie, hémorragies, gingivite, sécheresse cutanée, réouverture de cicatrices." },
    { "question": "Qui a étudié scientifiquement le traitement du scorbut ?", "answer": "James Lind en 1753 (A treatise of Scurvy)." },
    { "question": "Quelles sont les propriétés de la vitamine C ?", "answer": "Très soluble dans l'eau, hydrolyse en solution, oxydation par l'air, photolyse UV, thermolabile." },
    { "question": "Qu'est-ce que l'appertisation ?", "answer": "Mode de conservation préservant la vitamine C, inventé par Nicolas Appert en 1795." },
    { "question": "Quel est le rôle de la vitamine C dans le collagène ?", "answer": "Cofacteur de la Lysyl-hydroxylase et Prolyl-hydroxylase, essentielle au renouvellement du collagène." },
    { "question": "À quoi servent les résidus OH-lysyl et OH-prolyl ?", "answer": "À la stabilité du collagène (liaisons hydrogène)." },
    { "question": "Que se passe-t-il sans vitamine C ?", "answer": "Pas d'hydroxylation → pas de triple hélice de collagène → perte de cohésion du mésenchyme." },
]

# Dictionnaire complet des fichiers et flashcards
FILES_AND_FLASHCARDS = {
    "Nutrition/APP/obe_site_actu.html": FLASHCARDS_OBESITE,
    "Nutrition/APP/dysle_piudemie.html": FLASHCARDS_DYSLIPIDEMIE,
    "Nutrition/APP/app_relations_nutrition_sante.html": FLASHCARDS_RELATIONS_NUTRITION_SANTE,
    "Genetique/SOCLE/caryotype_humain_om.html": FLASHCARDS_CARYOTYPE,
    "Histologie/SOCLE/me_thode_d_e_tude.html": FLASHCARDS_METHODES_ETUDE,
    "Nutrition/SOCLE/1_introduction.html": FLASHCARDS_INTRODUCTION_NUTRITION,
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
    print("🚀 Génération et injection des flashcards USPN S2")
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
