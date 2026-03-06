#!/usr/bin/env python3
"""
Generate 7 missing SHS course files for SU_S2:
- 5 Psychologie médicale courses (FC1-FC5)
- 2 Éthique et droit courses (FC3 Principisme, FC4 AMP)
Also updates SU_S2/index.html, favorites.html, and all existing sidebars.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SU_S2_DIR = os.path.join(BASE_DIR, "SU_S2")
SHS_DIR = os.path.join(SU_S2_DIR, "SHS")


def esc(s):
    """Replace straight apostrophes with curly ones for JS strings."""
    return s.replace("'", "\u2019")


# ─── FLASHCARD DATA ─────────────────────────────────────────────────────────

# FC1 Psychologie: Émotion et comportement
PSYCHO_EMOTION = [
    ("Quelle est la définition générale d\u2019une émotion ?", "L\u2019émotion est un état psychologique et physiologique complexe, déclenché par un stimulus, qui implique 3 composantes : subjective (vécu), physiologique (réactions corporelles) et comportementale (expressions)."),
    ("Quelles sont les 3 composantes de l\u2019émotion ?", "1) Composante subjective : le vécu émotionnel (sentiment ressenti)\n2) Composante physiologique : réponses du corps (rythme cardiaque, sudation, cortisol)\n3) Composante comportementale : expressions faciales, postures, actions"),
    ("Qui a étudié les expressions faciales des émotions et quelle est sa thèse ?", "Charles Darwin (1872, L\u2019expression des émotions chez l\u2019homme et les animaux). Thèse : les expressions faciales sont universelles, innées et ont une fonction adaptative issue de l\u2019évolution."),
    ("Quelles sont les 6 émotions de base selon Ekman ?", "Joie, tristesse, colère, peur, dégoût, surprise. Elles sont universelles, reconnues dans toutes les cultures, et associées à des expressions faciales spécifiques."),
    ("Comment peut-on classifier les émotions selon 2 dimensions ?", "1) Valence : agréable (positive) vs désagréable (négative)\n2) Intensité : activation forte (excitation) vs faible (calme)"),
    ("Qu\u2019est-ce que la classification approche/retrait des émotions ?", "Approche : émotions qui poussent à se rapprocher du stimulus (joie, intérêt, colère)\nRetrait : émotions qui poussent à s\u2019éloigner (peur, dégoût, tristesse)"),
    ("Quelle est la théorie périphérique de James-Lange ?", "Les changements corporels précèdent l\u2019émotion. On perçoit un stimulus → réaction physiologique → le cerveau interprète cette réaction comme une émotion. Ex : on tremble d\u2019abord, puis on ressent la peur."),
    ("Quelle est la théorie centrale de Cannon-Bard ?", "L\u2019émotion et la réaction physiologique sont simultanées et indépendantes. Le thalamus envoie un signal en parallèle au cortex (émotion subjective) et au système nerveux autonome (réaction corporelle)."),
    ("Quelle est la théorie cognitive de Schachter-Singer (théorie des 2 facteurs) ?", "L\u2019émotion = activation physiologique + interprétation cognitive du contexte. Une même activation peut donner des émotions différentes selon l\u2019interprétation qu\u2019on en fait."),
    ("Qu\u2019est-ce que les neurones miroirs ?", "Neurones qui s\u2019activent à la fois quand on effectue une action ET quand on observe quelqu\u2019un d\u2019autre effectuer cette même action. Découverts chez le singe par Rizzolatti. Base neurobiologique de l\u2019empathie."),
    ("Quelle est la différence entre empathie et sympathie ?", "Empathie : capacité de comprendre et partager l\u2019état émotionnel d\u2019autrui (se mettre à sa place)\nSympathie : réaction émotionnelle orientée vers l\u2019autre (compassion, désir d\u2019aider) sans nécessairement ressentir la même chose"),
    ("Comment les émotions influencent-elles le comportement ?", "Les émotions orientent les décisions (marqueurs somatiques de Damasio), motivent l\u2019action (fuite, approche), facilitent la communication sociale et la mémorisation des événements importants."),
    ("Pourquoi les expressions faciales ont-elles une fonction adaptative selon Darwin ?", "Elles permettent la communication rapide des états internes entre individus, facilitent la cohésion sociale, alertent du danger et favorisent la survie de l\u2019espèce."),
    ("Quelle critique principale peut-on faire de la théorie de James-Lange ?", "Les réactions physiologiques sont trop lentes et trop similaires entre émotions différentes pour en être la cause. Des patients avec lésions médullaires ressentent quand même des émotions."),
    ("Qu\u2019est-ce que l\u2019expérience d\u2019injection d\u2019adrénaline de Schachter et Singer ?", "Injection d\u2019adrénaline à des sujets : ceux informés de l\u2019effet attribuent leur activation au produit, ceux non informés interprètent leur activation selon le contexte (joyeux ou colérique)."),
    ("Quel rôle joue l\u2019amygdale dans les émotions ?", "L\u2019amygdale est centrale dans le traitement de la peur et des émotions négatives. Elle permet une réponse rapide au danger (voie courte thalamus-amygdale) avant même l\u2019analyse corticale consciente."),
    ("Qu\u2019est-ce que la composante comportementale de l\u2019émotion ?", "L\u2019ensemble des manifestations observables : expressions faciales, postures corporelles, gestes, ton de la voix, actions motrices (fuite, attaque, figement)."),
    ("Comment la culture influence-t-elle l\u2019expression des émotions ?", "Par les règles d\u2019affichage (display rules) : normes sociales dictant quelles émotions montrer ou masquer selon le contexte. Ex : au Japon, masquer les émotions négatives en public."),
    ("Quels sont les effets du stress sur le comportement émotionnel ?", "Le stress chronique altère la régulation émotionnelle, augmente l\u2019irritabilité et l\u2019anxiété, réduit l\u2019empathie et les capacités de contrôle des impulsions."),
    ("Quelle est la valeur adaptative de la peur ?", "La peur active la réponse fight-or-flight (combat ou fuite) via le système nerveux sympathique. Elle prépare l\u2019organisme à réagir face au danger : augmentation du rythme cardiaque, vigilance accrue, mobilisation de l\u2019énergie."),
]

# FC2 Psychologie: Prévention des conduites suicidaires
PSYCHO_SUICIDE = [
    ("Quelle est la définition du suicide selon Durkheim ?", "Tout cas de mort qui résulte directement ou indirectement d\u2019un acte positif ou négatif, accompli par la victime elle-même, et qu\u2019elle savait devoir produire ce résultat."),
    ("Quelle différence entre conduites suicidaires et équivalents suicidaires ?", "Conduites suicidaires : actes visant explicitement la mort (tentative, suicide abouti)\nÉquivalents suicidaires : comportements à risque sans intention suicidaire consciente mais potentiellement mortels (conduite dangereuse, addictions sévères)"),
    ("Quelle différence entre suicidaire, suicidant et suicidé ?", "Suicidaire : personne ayant des idées suicidaires\nSuicidant : personne ayant fait une tentative de suicide\nSuicidé : personne décédée par suicide"),
    ("Combien de suicides et de tentatives par an en France ?", "Environ 10 000 décès par suicide par an (9000 selon les chiffres récents) et environ 200 000 tentatives de suicide par an."),
    ("Quelles sont les différences genrées face au suicide ?", "Les hommes meurent plus par suicide (3 fois plus que les femmes) car ils utilisent des moyens plus létaux.\nLes femmes font plus de tentatives de suicide (3 fois plus que les hommes)."),
    ("Comment le taux de suicide varie-t-il selon l\u2019âge ?", "Le taux augmente avec l\u2019âge, surtout chez les hommes. Les personnes âgées ont le taux le plus élevé. Chez les jeunes (15-24 ans), le suicide est la 2e cause de mortalité."),
    ("Quelles sont les variations régionales du suicide en France ?", "Taux plus élevés dans le Nord et le Nord-Ouest (Bretagne, Normandie, Hauts-de-France). Taux plus faibles dans le Sud (Île-de-France, PACA)."),
    ("Quels sont les 4 facteurs de risque du suicide (4A) ?", "1) Antécédents : de tentative de suicide personnels ou familiaux\n2) Aller mal : pathologie psychiatrique (dépression, troubles bipolaires, schizophrénie, addictions)\n3) Avoir des événements de vie stressants : deuil, rupture, chômage, conflit\n4) Accès aux moyens létaux"),
    ("Quelles pathologies psychiatriques sont les plus associées au suicide ?", "Dépression (risque x30), troubles bipolaires, schizophrénie, troubles de la personnalité (borderline), addictions (alcool, drogues), troubles anxieux sévères."),
    ("Qu\u2019est-ce que la prévention primaire du suicide ?", "Actions visant à réduire l\u2019incidence du suicide dans la population générale : campagnes de sensibilisation, restriction d\u2019accès aux moyens létaux, formation des professionnels, lignes d\u2019écoute."),
    ("Qu\u2019est-ce que la prévention secondaire du suicide ?", "Repérage et prise en charge précoce des personnes à risque : dépistage des idées suicidaires, intervention de crise, évaluation du risque suicidaire, hospitalisation si nécessaire."),
    ("Qu\u2019est-ce que la prévention tertiaire du suicide ?", "Prise en charge après une tentative de suicide : prévention de la récidive, suivi psychologique et psychiatrique, accompagnement social, postvention (soutien aux proches)."),
    ("Qu\u2019est-ce que la grille RUD pour évaluer l\u2019urgence suicidaire ?", "R = Risque (facteurs de risque présents)\nU = Urgence (imminence du passage à l\u2019acte, plan, moyens)\nD = Dangerosité (létalité du moyen envisagé, accessibilité)"),
    ("Quels sont les 3 niveaux d\u2019urgence suicidaire ?", "1) Urgence faible : idées suicidaires sans plan précis, cherche des solutions\n2) Urgence moyenne : plan envisagé mais reporté, ambivalence\n3) Urgence élevée : plan précis, moyen accessible, échéance fixée, grande souffrance, peu d\u2019alternatives"),
    ("Quels sont les principes de la prise en charge d\u2019une crise suicidaire ?", "Créer un lien de confiance, explorer les idées suicidaires (ne pas éviter le sujet), évaluer le niveau d\u2019urgence (RUD), sécuriser l\u2019environnement, orienter vers les soins, ne pas laisser seul."),
    ("Pourquoi est-il important de parler du suicide avec un patient suicidaire ?", "Parler du suicide ne donne pas d\u2019idées suicidaires. Au contraire, cela permet au patient de se sentir écouté, réduit l\u2019isolement et permet une évaluation précise du risque."),
    ("Quels sont les facteurs protecteurs contre le suicide ?", "Soutien social et familial, accès aux soins de santé mentale, sentiment d\u2019appartenance, projets de vie, croyances religieuses/spirituelles, enfants à charge, capacités de résolution de problèmes."),
    ("Qu\u2019est-ce que la postvention ?", "Ensemble des actions mises en place après un suicide pour accompagner l\u2019entourage du défunt (famille, amis, collègues) et prévenir les effets de contagion (cluster suicidaire)."),
    ("Qu\u2019est-ce que l\u2019effet Werther ?", "Phénomène de contagion suicidaire : augmentation des suicides après la médiatisation d\u2019un suicide (particulièrement chez les jeunes). D\u2019où les recommandations de l\u2019OMS aux médias."),
    ("Quel numéro d\u2019appel pour la prévention du suicide en France ?", "Le 3114, numéro national de prévention du suicide, accessible 24h/24, 7j/7, gratuit et confidentiel."),
]

# FC3 Éthique: Principisme et fin de vie
ETHIQUE_PRINCIPISME = [
    ("Quels sont les 4 principes du principisme (Beauchamp et Childress) ?", "1) Non-malfaisance (ne pas nuire)\n2) Bienfaisance (faire le bien du patient)\n3) Autonomie (respect des choix du patient)\n4) Justice (répartition équitable des ressources)"),
    ("Qu\u2019est-ce que la spécification en principisme ?", "Traduire un principe abstrait en règle concrète applicable. Ex : le principe d\u2019autonomie se spécifie en règle du consentement éclairé."),
    ("Qu\u2019est-ce que l\u2019équilibrage (balancing) en principisme ?", "Processus de résolution des conflits entre principes quand ils s\u2019opposent dans un cas concret. Ex : bienfaisance vs autonomie quand un patient refuse un traitement vital."),
    ("Quelle critique pluraliste est faite au principisme ?", "Les 4 principes prétendent à l\u2019universalité mais reflètent des valeurs occidentales libérales. L\u2019autonomie individuelle n\u2019est pas prioritaire dans toutes les cultures."),
    ("Quelle critique universaliste est faite au principisme ?", "Les principes sont trop abstraits et indéterminés, ils ne donnent pas de solution automatique en cas de conflit. On peut les utiliser pour justifier des décisions opposées."),
    ("Quelle critique féministe/éthique du care est faite au principisme ?", "Il néglige la dimension relationnelle du soin, les émotions, la vulnérabilité et les rapports de pouvoir. L\u2019éthique du care met l\u2019accent sur l\u2019attention à autrui et la relation de soin."),
    ("Qu\u2019est-ce que la critique du décisionisme ?", "Le principisme réduit l\u2019éthique à la prise de décision ponctuelle au lieu de considérer le processus global, les dispositions morales du soignant et le contexte institutionnel."),
    ("Qui est Vincent Humbert et quel est son cas ?", "Jeune homme de 20 ans devenu tétraplégique, aveugle et muet après un accident de la route (2000). Il demande le droit de mourir. Sa mère lui administre un barbiturique (2003). Le médecin réanimateur achève le geste."),
    ("Quelles suites judiciaires dans l\u2019affaire Humbert ?", "La mère et le médecin sont poursuivis puis acquittés. L\u2019affaire relance le débat sur la fin de vie et conduit à la loi Leonetti de 2005."),
    ("Qui est Vincent Lambert et quel est son cas ?", "Patient en état végétatif chronique depuis un accident de moto (2008). Conflit familial entre partisans de l\u2019arrêt des traitements et opposants. L\u2019affaire dure de 2013 à 2019 (décès après arrêt des traitements)."),
    ("Quels sont les apports majeurs de la loi Leonetti (2005) ?", "1) Interdiction de l\u2019obstination déraisonnable (acharnement thérapeutique)\n2) Droit du patient de refuser tout traitement\n3) Obligation de soins palliatifs\n4) Procédure collégiale pour les patients inconscients\n5) Directives anticipées (non contraignantes)"),
    ("Quels sont les apports de la loi Claeys-Leonetti (2016) ?", "1) Sédation Profonde et Continue Jusqu\u2019au Décès (SPCJD) pour les patients en fin de vie\n2) Directives anticipées devenues contraignantes\n3) Personne de confiance renforcée\n4) Nutrition et hydratation artificielles = traitements (peuvent être arrêtés)"),
    ("Qu\u2019est-ce que la SPCJD ?", "Sédation Profonde et Continue jusqu\u2019au Décès : altération profonde et continue de la conscience jusqu\u2019au décès, associée à l\u2019arrêt de l\u2019ensemble des traitements de maintien en vie, y compris nutrition et hydratation."),
    ("Dans quels cas la SPCJD peut-elle être mise en place ?", "1) Patient en phase terminale avec souffrance réfractaire aux traitements\n2) Patient en fin de vie décidant d\u2019arrêter un traitement vital\n3) Patient hors d\u2019état d\u2019exprimer sa volonté : décision collégiale si obstination déraisonnable"),
    ("Qu\u2019est-ce que le projet de loi sur l\u2019aide active à mourir (2024-2025) ?", "Projet permettant sous conditions strictes une aide active à mourir pour les patients majeurs, capables de discernement, atteints d\u2019affection grave et incurable avec pronostic vital engagé à court/moyen terme et souffrance réfractaire."),
    ("Quels sont les modèles étrangers d\u2019aide à mourir ?", "Pays-Bas/Belgique : euthanasie active légale (acte du médecin)\nSuisse : suicide assisté (le patient s\u2019administre lui-même le produit)\nOregon (USA) : Death with Dignity Act (suicide assisté)\nCanada : aide médicale à mourir (AMAD)"),
    ("Qu\u2019est-ce que la doctrine du double effet (Thomas d\u2019Aquin) ?", "Doctrine morale permettant de justifier un acte ayant un effet bon recherché et un effet mauvais prévu mais non voulu. Ex : administrer des antalgiques puissants sachant que cela peut accélérer le décès."),
    ("Quelles sont les 4 conditions cumulatives du double effet ?", "1) L\u2019acte en lui-même est bon ou moralement indifférent\n2) L\u2019effet mauvais n\u2019est pas voulu, seulement prévu et toléré\n3) L\u2019effet bon n\u2019est pas produit par l\u2019effet mauvais (qui n\u2019est pas un moyen)\n4) Proportionnalité entre l\u2019effet bon visé et l\u2019effet mauvais toléré"),
    ("Quelle différence entre euthanasie et SPCJD ?", "Euthanasie : acte provoquant intentionnellement la mort (injection létale)\nSPCJD : sédation profonde + arrêt des traitements vitaux → la mort survient naturellement. L\u2019intention est de soulager, pas de tuer."),
    ("Qu\u2019est-ce que les directives anticipées ?", "Document écrit par lequel une personne majeure exprime ses volontés relatives à sa fin de vie (traitements à poursuivre, limiter ou arrêter). Depuis 2016 : s\u2019imposent au médecin sauf urgence vitale ou inappropriation manifeste."),
]

# FC3 Psychologie: Les représentations du corps
PSYCHO_CORPS = [
    ("Qu\u2019est-ce que le dualisme platonico-cartésien ?", "Séparation radicale entre l\u2019âme (ou l\u2019esprit) et le corps. Platon : le corps est le tombeau de l\u2019âme. Descartes : res cogitans (substance pensante) vs res extensa (substance étendue). Le corps est une machine."),
    ("Qu\u2019est-ce que le monisme de Spinoza ?", "Il n\u2019y a qu\u2019une seule substance (Dieu/Nature) dont corps et esprit sont deux attributs. Corps et pensée sont parallèles, indissociables. Pas de supériorité de l\u2019esprit sur le corps."),
    ("Qu\u2019est-ce que la thèse de l\u2019homme-machine (La Mettrie, 1747) ?", "Le corps humain est intégralement une machine, y compris le cerveau et la pensée. Position matérialiste radicale : la pensée est un produit de la matière cérébrale."),
    ("Qu\u2019est-ce que l\u2019homme neuronal (Jean-Pierre Changeux) ?", "Thèse contemporaine : l\u2019homme se réduit à son cerveau. La conscience, les émotions et la pensée sont des phénomènes neuronaux. Forme moderne de matérialisme réductionniste."),
    ("Quel rapport Nietzsche entretient-il avec le corps ?", "Nietzsche réhabilite le corps comme \u201cgrande raison\u201d face à la \u201cpetite raison\u201d de la conscience. Le corps vivant est la source de la volonté de puissance et de la connaissance. Renversement du platonisme."),
    ("Qu\u2019est-ce que la distinction Körper/Leib chez Husserl ?", "Körper : le corps-objet, le corps physique et matériel, observable de l\u2019extérieur\nLeib : le corps-vécu, le corps propre, le corps comme siège de la subjectivité et de l\u2019expérience"),
    ("Quelle est la conception du corps chez Merleau-Ponty ?", "Le corps est le medium fondamental de notre rapport au monde. Il n\u2019est ni pur objet ni pure conscience. C\u2019est par le corps propre que nous percevons, agissons et existons dans le monde."),
    ("Qu\u2019est-ce que la phénoménologie du visage chez Levinas ?", "Le visage d\u2019autrui est une épiphanie éthique : il me convoque à la responsabilité. Le visage est nu, vulnérable, et m\u2019interdit de tuer. Fondement de l\u2019éthique comme philosophie première."),
    ("Qu\u2019est-ce que le constructivisme social appliqué au corps ?", "Le corps n\u2019est pas seulement biologique mais aussi construit socialement : les normes culturelles définissent ce qu\u2019est un corps normal, beau, sain, masculin/féminin, valide/handicapé."),
    ("Comment l\u2019image du corps s\u2019est-elle transformée dans la modernité ?", "Le corps est devenu objet de consommation, de performance et de transformation (chirurgie esthétique, sport, tatouages). Tension entre corps naturel et corps artificialisé."),
    ("Qu\u2019est-ce que le corps fantasmé ?", "Représentation imaginaire du corps, influencée par les idéaux culturels (beauté, minceur, performance). Décalage entre le corps réel et le corps idéalisé, source de souffrance psychique (troubles alimentaires, dysmorphophobie)."),
    ("Comment la différence sociale des sexes est-elle construite selon le cours ?", "La distinction masculin/féminin n\u2019est pas seulement biologique mais aussi socialement construite. Les rôles de genre, les comportements attendus et les représentations corporelles varient selon les cultures et les époques."),
    ("Qu\u2019est-ce que la déconstruction du genre appliquée au corps ?", "Remise en question de la binarité homme/femme comme catégorie naturelle. Le genre est une performance sociale (Butler). Le corps est un lieu de normes imposées que l\u2019on peut déconstruire."),
    ("Comment le racisme et le handicap interrogent-ils les représentations du corps ?", "Le racisme assigne des corps à des catégories hiérarchisées (races). Le handicap révèle les normes du corps \u201cvalide\u201d comme construction sociale. Les deux montrent que le corps est un lieu de pouvoir et de discrimination."),
    ("Pourquoi le dualisme corps/esprit est-il problématique en médecine ?", "Il conduit à traiter le corps comme une machine à réparer en ignorant le vécu du patient. La médecine psychosomatique montre que corps et psychisme interagissent constamment."),
    ("Quel est l\u2019intérêt de la phénoménologie pour la pratique médicale ?", "Elle invite à considérer le patient non comme un corps-objet à examiner mais comme un sujet incarné avec un vécu. Le corps malade est un corps-vécu, pas seulement un organisme dysfonctionnel."),
    ("Qu\u2019est-ce que le dualisme moderne en médecine ?", "Persistance de la séparation corps/esprit dans la pratique médicale : spécialités somatiques vs psychiatrie, médecine du corps vs médecine de l\u2019esprit. La médecine holistique tente de dépasser cette dichotomie."),
    ("Comment Descartes justifie-t-il que le corps est une machine ?", "Par l\u2019analogie avec les automates : le corps fonctionne comme une horloge selon des lois mécaniques. Seule l\u2019âme pensante (glande pinéale) distingue l\u2019homme de la machine."),
    ("Qu\u2019est-ce que le schéma corporel ?", "Représentation inconsciente et dynamique du corps dans l\u2019espace. Il permet la coordination motrice et la proprioception. Se distingue de l\u2019image du corps (représentation consciente et affective)."),
    ("Comment la sociologie aborde-t-elle le corps ?", "Le corps est socialement façonné : techniques du corps (Mauss), habitus corporel (Bourdieu), discipline des corps (Foucault). Le corps est un lieu d\u2019inscription des normes sociales et du pouvoir."),
]

# FC4 Psychologie: Stress et psycho-traumatisme
PSYCHO_STRESS = [
    ("Quelle est la définition du stress ?", "Le stress se définit par l\u2019ensemble des réponses de l\u2019organisme soumis à des contraintes/pressions de la part de l\u2019environnement. Ces contraintes sont non spécifiques et entraînent la sécrétion d\u2019hormones de stress (adrénaline, cortisol)."),
    ("Quelle différence entre stress et anxiété ?", "Le stress est une réponse à une contrainte externe de l\u2019environnement.\nL\u2019anxiété est un phénomène interne où le cerveau se fait du souci sans contrainte externe nécessairement présente."),
    ("Qu\u2019est-ce que la réaction de stress ?", "Ensemble de processus biologiques et psychologiques mis en œuvre par l\u2019organisme pour s\u2019adapter à un agent perturbateur. Phénomène indispensable à la survie, permettant de s\u2019adapter aux contraintes hostiles."),
    ("Qui est Hans Selye et qu\u2019a-t-il décrit ?", "Hans Selye (1956) a décrit le Syndrome Général d\u2019Adaptation (SGA) en 3 phases : 1) Phase d\u2019alarme, 2) Phase de résistance, 3) Phase d\u2019épuisement."),
    ("Quelles sont les 3 phases du Syndrome Général d\u2019Adaptation (Selye) ?", "1) Alarme : mobilisation des ressources (adrénaline, noradrénaline) → fight or flight\n2) Résistance : maintien de l\u2019effort d\u2019adaptation (cortisol) → l\u2019organisme résiste\n3) Épuisement : si le stress persiste, effondrement des capacités d\u2019adaptation"),
    ("Quels sont les 2 grands axes neuro-hormonaux du stress ?", "1) Axe sympatho-adrénergique : réponse rapide (adrénaline, noradrénaline) → augmentation FC, TA, vigilance\n2) Axe corticotrope (HPA) : réponse plus lente (CRH → ACTH → cortisol) → mobilisation de l\u2019énergie"),
    ("Quelles sont les conséquences psychologiques du stress chronique ?", "Anxiété, irritabilité, troubles du sommeil, difficultés de concentration, dépression, burn-out, troubles de la mémoire, retrait social, addictions (alcool, tabac)."),
    ("Quelles sont les conséquences physiques du stress chronique ?", "Troubles cardiovasculaires (HTA, infarctus), immuno-suppression, troubles digestifs (ulcères), troubles musculo-squelettiques, céphalées, dermatoses, troubles hormonaux."),
    ("Quelles interventions sont possibles pour gérer le stress ?", "Relaxation et respiration, activité physique régulière, gestion cognitive (restructuration), soutien social, évitement des psychostimulants (café, alcool, drogues), psychothérapie (TCC)."),
    ("Qu\u2019est-ce qu\u2019un psycho-traumatisme ?", "Événement soudain et violent qui menace l\u2019intégrité physique ou psychique d\u2019un individu (ou d\u2019un témoin). Il provoque un effroi et dépasse les capacités d\u2019adaptation du sujet."),
    ("Quels types d\u2019événements peuvent être traumatogènes ?", "Agressions (violences, viols), accidents graves, catastrophes naturelles, attentats, guerre, mort violente d\u2019un proche, annonce d\u2019un diagnostic grave."),
    ("Qu\u2019est-ce que l\u2019État de Stress Post-Traumatique (ESPT) ?", "Trouble survenant après un psycho-traumatisme, caractérisé par : reviviscences (flashbacks, cauchemars), évitement des rappels, hyperactivation neurovégétative, altérations cognitives et de l\u2019humeur."),
    ("Quels sont les symptômes de reviviscence dans l\u2019ESPT ?", "Flashbacks (revivre l\u2019événement comme s\u2019il se reproduisait), cauchemars répétitifs, détresse intense face aux stimuli rappelant l\u2019événement, réactions physiologiques aux rappels."),
    ("Qu\u2019est-ce que l\u2019état de stress aigu ?", "Réaction dans les heures/jours suivant le traumatisme (jusqu\u2019à 1 mois). Symptômes dissociatifs (déréalisation, dépersonnalisation), reviviscences, évitement, hyperactivation. Si persiste > 1 mois → ESPT."),
    ("Quels traitements sont utilisés pour l\u2019ESPT ?", "1) Psychothérapie : TCC (thérapie d\u2019exposition) et EMDR (Eye Movement Desensitization and Reprocessing)\n2) Pharmacologie : antidépresseurs (paroxétine, sertraline) dans les cas sévères\n3) Blocage de la reconsolidation mnésique (propranolol)"),
    ("Qu\u2019est-ce que l\u2019EMDR ?", "Eye Movement Desensitization and Reprocessing : le sujet revit l\u2019événement traumatisant dans un environnement sécurisé en faisant des mouvements oculaires répétés. Permet de couper la partie émotionnelle du souvenir."),
    ("Qu\u2019est-ce que le blocage de la reconsolidation mnésique ?", "Technique basée sur le fait qu\u2019un souvenir remémoré redevient instable et doit être reconsolidé. En utilisant du propranolol (bétabloquant) pendant la remémoration, on peut atténuer la charge émotionnelle du souvenir traumatique."),
    ("Quels sont les facteurs de risque d\u2019ESPT ?", "Intensité et durée du traumatisme, antécédents psychiatriques, isolement social, absence de soutien après l\u2019événement, dissociation péri-traumatique, traumatismes antérieurs."),
    ("Quelles complications peuvent survenir avec un ESPT non traité ?", "Dépression, addictions (alcool, drogues), troubles anxieux, isolement social, difficultés professionnelles, risque suicidaire augmenté."),
    ("Qu\u2019est-ce que la dissociation péri-traumatique ?", "État de conscience altéré pendant l\u2019événement traumatique : sentiment d\u2019irréalité, de détachement de soi, perception ralentie du temps. C\u2019est un facteur de risque majeur de développer un ESPT."),
]

# FC4 Éthique: Progrès techniques et AMP
ETHIQUE_AMP = [
    ("Qu\u2019est-ce que l\u2019AMP (Assistance Médicale à la Procréation) ?", "Ensemble des pratiques cliniques et biologiques permettant la conception in vitro, la conservation des gamètes et embryons, le transfert d\u2019embryon et l\u2019insémination artificielle."),
    ("Quelles sont les principales causes d\u2019infertilité féminine ?", "1) Âge avancé (cause majeure après 35 ans)\n2) Troubles de l\u2019ovulation (SOPK, anovulation)\n3) Facteur tubo-péritonéal (trompes bouchées : IST, endométriose)\n4) Facteurs utérins (fibromes, adénomyose, synéchies)"),
    ("Quelles sont les principales causes d\u2019infertilité masculine ?", "1) Causes obstructives (canaux déférents bloqués, agénésie)\n2) Causes non obstructives (microdélétions Y, cryptorchidie, varicocèle)\n3) Causes mécaniques/sexuelles (troubles érection/éjaculation)\n4) Toxiques (cannabis, tabac, alcool, chaleur)"),
    ("Quelle est la répartition des causes d\u2019infertilité dans un couple ?", "30% d\u2019origine masculine, 30% d\u2019origine féminine, 30% d\u2019origine mixte, 10% idiopathique (cause inconnue)."),
    ("Comment évolue le stock ovocytaire au cours de la vie ?", "6 millions à 6 mois in utero → 1 million à la naissance → 400 000 à la puberté → 0 à la ménopause (~51 ans). Déclin qualitatif : 70% normaux à 30 ans vs 30% à 40 ans."),
    ("Qui sont Louise Brown et Amandine ?", "Louise Brown : 1er bébé mondial conçu par FIV (25 juillet 1978, UK, équipe Edwards et Steptoe)\nAmandine : 1er bébé français par FIV (24 février 1982, équipe Testart et Frydman, hôpital Antoine-Béclère)"),
    ("Qu\u2019est-ce que l\u2019ICSI ?", "Injection Intra-Cytoplasmique de Spermatozoïde : micro-injection d\u2019un seul spermatozoïde directement dans l\u2019ovocyte. Indiquée pour les infertilités masculines sévères. 1er enfant né en 1992 (Belgique)."),
    ("Qu\u2019est-ce que la vitrification ovocytaire et embryonnaire ?", "Technique de congélation ultra-rapide (-196°C) empêchant la formation de cristaux. Autorisée en France depuis 2011. Amélioration de la survie : passage de 60% à 90% à la décongélation."),
    ("Quels sont les apports majeurs de la loi de bioéthique de 2021 pour l\u2019AMP ?", "1) Extension aux couples de femmes et femmes seules\n2) Autoconservation sociétale de gamètes (sans motif médical)\n3) Fin de l\u2019anonymat du donneur (accès à 18 ans)\n4) Double don autorisé"),
    ("Quelles sont les limites d\u2019âge pour l\u2019AMP en France (décret 2021) ?", "Femme : ponction ovocytaire jusqu\u2019à la veille de 43 ans, insémination/transfert jusqu\u2019à la veille de 45 ans\nHomme : recueil de sperme jusqu\u2019à la veille de 60 ans"),
    ("Qu\u2019est-ce que l\u2019insémination artificielle ?", "Technique la plus simple : optimisation de la rencontre des gamètes dans la trompe. Stimulation ovarienne légère + monitorage + préparation du sperme le jour de l\u2019ovulation. Pas d\u2019insémination post-mortem."),
    ("Quelle différence entre FIV classique et ICSI ?", "FIV classique : 10 000-60 000 spermatozoïdes placés autour de l\u2019ovocyte, le spermatozoïde pénètre seul. Nécessite NSMI > 1M.\nICSI : injection directe d\u2019un seul spermatozoïde dans l\u2019ovocyte. Pour infertilités masculines sévères."),
    ("Quels sont les stades du développement embryonnaire en laboratoire ?", "J1 : Zygote (2 pronucléi)\nJ2 : 4 cellules\nJ3 : 8 cellules\nJ5 : Blastocyste (masse cellulaire interne = futur fœtus + trophectoderme = futur placenta). Stade privilégié pour le transfert (~46% de réussite)."),
    ("Qu\u2019est-ce que la politique du Single Embryo Transfer ?", "Transfert d\u2019un seul embryon à la fois pour éviter les grossesses multiples (risques de prématurité). A permis de réduire les jumeaux de 8% (2020) à 5% (2023)."),
    ("Quels sont les chiffres clés de l\u2019AMP en France (2023) ?", "~25 000 enfants/an par AMP (3% des naissances), ~70 000 ponctions ovocytaires/an. TEC : 48%, Insémination : 21%, ICSI : 21%, FIV classique : 10%. Taux d\u2019accouchement par transfert : ~25%."),
    ("Qu\u2019est-ce que le DPI (Diagnostic Préimplantatoire) ?", "Analyse génétique de cellules prélevées sur l\u2019embryon in vitro pour éviter la transmission d\u2019une maladie génétique grave incurable (ex : mucoviscidose, Huntington). Autorisé depuis 1994, 6 centres en France."),
    ("Quelles sont les 3 options pour les embryons surnuméraires en fin de projet parental ?", "1) Don à un autre couple ou femme non mariée\n2) Don à la recherche scientifique\n3) Arrêt de la conservation"),
    ("Qu\u2019est-ce que la préservation de fertilité ?", "Conservation de gamètes ou tissus germinaux pour préserver la capacité reproductive. Médicale (avant cancer, endométriose) ou sociétale (sans motif médical, par choix personnel). La France rembourse les deux à 100%."),
    ("Quels sont les débats éthiques pour la future loi de bioéthique (2028) ?", "1) DPI-A (criblage chromosomique sans maladie connue)\n2) AMP post-mortem (transfert d\u2019embryons après décès du conjoint)\n3) Méthode ROPA (couples de femmes : une donne les ovocytes, l\u2019autre porte)\n4) Impact de l\u2019IA sur la santé"),
    ("Qu\u2019est-ce que la Reconnaissance Conjointe Anticipée (RCA) ?", "Obligation pour les couples de femmes ayant recours à l\u2019AMP de signer devant notaire une reconnaissance conjointe anticipée avant la conception, pour établir la double filiation dès la naissance."),
]

# FC5 Psychologie: Développement affectif et intellectuel
PSYCHO_DEVELOPPEMENT = [
    ("Comment Piaget définit-il l\u2019intelligence ?", "Capacité d\u2019un individu à s\u2019adapter à son environnement. Elle dépend de données innées (développement du système nerveux) et des expériences acquises. Elle est associée à la motricité et à l\u2019affectivité."),
    ("Quelles sont les opérations intellectuelles sous-tendues par l\u2019intelligence ?", "Organisation de la perception, organisation mnésique, raisonnement, planification des actions, capacités d\u2019apprentissage, argumentation et échanges sociaux, vitesse de traitement cognitif."),
    ("Qui a créé le premier test d\u2019intelligence et dans quel contexte ?", "Alfred Binet et Théodore Simon, fin du 19e siècle, commandé par l\u2019Éducation nationale pour repérer les enfants en difficulté scolaire après la loi Jules Ferry sur l\u2019obligation scolaire."),
    ("Comment calcule-t-on le QI selon Binet et Simon ?", "QI = (Âge mental / Âge réel) × 100\nÂge mental = performance moyenne aux 6 épreuves comparée aux classes d\u2019âge\nQI = 100 → intelligence moyenne. Cette méthode est toujours utilisée."),
    ("Qu\u2019est-ce que le test de Wechsler (WISC/WAIS) ?", "Test de QI moderne basé sur la loi normale. Moyenne fixée à 100, écart-type à 15. Retard < 70, surdouance (HPI) > 130. WISC : 6-16 ans, WAIS : adultes (>16 ans), WPPSI : 4-6 ans."),
    ("Qu\u2019est-ce que le facteur G en psychologie ?", "Facteur général d\u2019intelligence : degré de corrélation entre les variations interindividuelles aux différentes épreuves. Montre que l\u2019intelligence est hétérogène mais repose sur un facteur commun. Bons tests : facteur G ≥ 0.6-0.7."),
    ("Quels facteurs influencent les différences individuelles de QI ?", "1) Altérations cérébrales organiques (prématurité)\n2) Environnement familial (stimulations, sécurité affective)\n3) Milieu socio-économique (surtout QI verbal)\n4) Facteurs génétiques (50-60% de variance génétique, 40-50% environnementale)"),
    ("Pourquoi ne peut-on pas comparer le QI entre cultures ?", "Les tests sont conçus dans un contexte culturel spécifique. L\u2019intelligence se construit dans l\u2019équilibre inné/acquis, et l\u2019acquis est toujours culturel. Il n\u2019existe pas de mesure transculturelle de l\u2019intelligence."),
    ("Quels sont les types de développement : phylogénèse, ontogénèse, épigénèse ?", "Phylogénèse : évolution des espèces\nOntogénèse : développement d\u2019un individu à partir de son patrimoine génétique\nÉpigénèse : façonnement de l\u2019individu par ses interactions avec l\u2019environnement (avec marquage ADN transmissible)"),
    ("Qu\u2019est-ce que l\u2019assimilation selon Piaget ?", "Incorporation d\u2019éléments du milieu à la structure de l\u2019individu. Ex : à force d\u2019entendre les phonèmes de sa langue, des aires cérébrales se déterminent et contraignent la voix."),
    ("Qu\u2019est-ce que l\u2019accommodation selon Piaget ?", "Modifications de la structure de l\u2019individu pour s\u2019adapter aux modifications du milieu. Ex : l\u2019apprentissage de la lecture crée une zone d\u2019identification des mots dans le cerveau (recyclage neuronal)."),
    ("Quels sont les 4 stades du développement de l\u2019intelligence selon Piaget ?", "1) Sensori-moteur (0-2 ans)\n2) Préopératoire (2-6 ans)\n3) Opérations concrètes (7-11 ans)\n4) Opérations formelles (12-16 ans)"),
    ("Que caractérise le stade sensori-moteur (0-2 ans) ?", "Intelligence basée sur le concret et l\u2019immédiat : perceptions et schèmes d\u2019action motrice. Réactions circulaires (primaires, secondaires, tertiaires). Acquisition de la permanence de l\u2019objet vers 18 mois."),
    ("Que caractérise le stade préopératoire (2-6 ans) ?", "Fonction symbolique (imitation, jeu, dessin, langage). Pensée prélogique : animisme (objets vivants), finalisme, artificialisme, réalisme, égocentrisme, dominance du perceptif."),
    ("Que caractérise le stade des opérations concrètes (7-11 ans) ?", "Réversibilité logique, conservation de la matière/poids/volume. Apprentissages nécessaires à la pensée rationnelle. Capacité de lecture (besoin d\u2019invariants). Début de l\u2019école primaire dans tous les pays."),
    ("Que caractérise le stade des opérations formelles (12-16 ans) ?", "Pensée formelle : pensée sur la pensée. Raisonnement hypothético-déductif. Mathématiques abstraites, philosophie. Capacité de conceptualisation et d\u2019abstraction."),
    ("Qu\u2019est-ce que la théorie de l\u2019attachement de Bowlby ?", "Il existe un besoin primaire et inné d\u2019attachement, aussi fondamental que se nourrir. C\u2019est un instinct phylogénétiquement programmé pour maintenir la proximité avec la figure d\u2019attachement. S\u2019oppose à Freud."),
    ("Qu\u2019est-ce que la dépression anaclitique décrite par Spitz ?", "Dépression chez les bébés séparés de leur mère de façon prolongée (en orphelinat). L\u2019enfant devient amorphe, apathique. La mortalité en orphelinat sans soins maternels atteignait 70%."),
    ("Quelles sont les 3 étapes de la séparation selon Spitz ?", "1) Détresse (protestation, pleurs)\n2) Découragement (retrait, passivité)\n3) Indifférence (détachement émotionnel)\nMais si la mère revient, l\u2019enfant peut récupérer."),
    ("Qu\u2019est-ce que l\u2019attachement sécure vs insécure (Ainsworth) ?", "Sécure : sentiment de sécurité interne, confiance de base, exploration confiante du monde\nInsécure : anxiété, difficulté relationnelle à l\u2019âge adulte, souvent lié à des interactions précoces défaillantes"),
]

# ─── COURSE DEFINITIONS ────────────────────────────────────────────────────

COURSES = [
    # Psychologie médicale (5)
    {
        "filename": "psycho_emotion_comportement.html",
        "title_h1": "SHS - Psychologie médicale",
        "title_h2": "Émotion et comportement (FC1)",
        "page_title": "Diploma Santé - Émotion et comportement",
        "flashcards": PSYCHO_EMOTION,
    },
    {
        "filename": "psycho_prevention_suicidaires.html",
        "title_h1": "SHS - Psychologie médicale",
        "title_h2": "Prévention des conduites suicidaires (FC2)",
        "page_title": "Diploma Santé - Prévention des conduites suicidaires",
        "flashcards": PSYCHO_SUICIDE,
    },
    {
        "filename": "psycho_representations_corps.html",
        "title_h1": "SHS - Psychologie médicale",
        "title_h2": "Les représentations du corps (FC3)",
        "page_title": "Diploma Santé - Les représentations du corps",
        "flashcards": PSYCHO_CORPS,
    },
    {
        "filename": "psycho_stress_psychotraumatisme.html",
        "title_h1": "SHS - Psychologie médicale",
        "title_h2": "Stress et psycho-traumatisme (FC4)",
        "page_title": "Diploma Santé - Stress et psycho-traumatisme",
        "flashcards": PSYCHO_STRESS,
    },
    {
        "filename": "psycho_developpement_affectif.html",
        "title_h1": "SHS - Psychologie médicale",
        "title_h2": "Développement affectif et intellectuel (FC5)",
        "page_title": "Diploma Santé - Développement affectif et intellectuel",
        "flashcards": PSYCHO_DEVELOPPEMENT,
    },
    # Éthique et droit (2)
    {
        "filename": "principisme_fin_de_vie.html",
        "title_h1": "SHS - Éthique et droit",
        "title_h2": "Principisme et fin de vie (FC3)",
        "page_title": "Diploma Santé - Principisme et fin de vie",
        "flashcards": ETHIQUE_PRINCIPISME,
    },
    {
        "filename": "progres_techniques_amp.html",
        "title_h1": "SHS - Éthique et droit",
        "title_h2": "Progrès techniques et AMP (FC4)",
        "page_title": "Diploma Santé - Progrès techniques et AMP",
        "flashcards": ETHIQUE_AMP,
    },
]

# ─── SIDEBAR ────────────────────────────────────────────────────────────────

# Full sidebar for SU_S2 (from course files, uses ../ prefix)
SIDEBAR_COURSE = '''							<nav id="menu">
								<header class="major">
									<h2>Menu</h2>
								</header>
								<ul>
									<li><a href="../index.html">Accueil</a></li>
									<li><a href="../favorites.html">Favoris</a></li>
									<li>
										<span class="opener">Physiologie</span>
										<ul>
											<li><a href="../Physiologie/fc1.html">Introduction a la physiologie cardio-vasculaire</a></li>
											<li><a href="../Physiologie/fc2.html">Adaptation de l\u2019apport d\u2019oxygène</a></li>
											<li><a href="../Physiologie/fc3.html">Organisation du système cardiovasculaire</a></li>
											<li><a href="../Physiologie/fc4.html">Adaptations à l\u2019effort</a></li>
											<li><a href="../Physiologie/fc5.html">Introduction à la neurophysiologie</a></li>
											<li><a href="../Physiologie/fc6.html">Adaptation rénale</a></li>
											<li><a href="../Physiologie/fc7.html">Bilan de l\u2019eau</a></li>
											<li><a href="../Physiologie/fc8.html">Contrôle de la croissance</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">Anatomie</span>
										<ul>
											<li><a href="../Anatomie/tete_cou.html">Tête et cou</a></li>
											<li><a href="../Anatomie/petit_bassin.html">Le petit bassin</a></li>
											<li><a href="../Anatomie/odontologie.html">Odontologie</a></li>
											<li><a href="../Anatomie/appareil_reproducteur.html">Appareil reproducteur</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">Biophysique</span>
										<ul>
											<li><a href="../Biophysique/fc1.html">Physique pour la biophysique</a></li>
											<li><a href="../Biophysique/fc2.html">Solutions et transport</a></li>
											<li><a href="../Biophysique/fc3.html">Compartiments liquidiens</a></li>
											<li><a href="../Biophysique/fc4.html">Transfert electrodiffusif</a></li>
											<li><a href="../Biophysique/fc5.html">Potentiel de membrane</a></li>
											<li><a href="../Biophysique/fc6.html">ECG</a></li>
											<li><a href="../Biophysique/fc7.html">Acide base</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">Pharmacologie</span>
										<ul>
											<li><a href="../Pharmacologie/fc1.html">Introduction à la pharmacologie</a></li>
											<li><a href="../Pharmacologie/fc2.html">Règles de prescription</a></li>
											<li><a href="../Pharmacologie/fc3.html">Les phases de développement clinique</a></li>
											<li><a href="../Pharmacologie/fc4.html">Encadrement réglementaire de la recherche clinique</a></li>
											<li><a href="../Pharmacologie/fc5.html">Pharmacocinétique descriptive (FC5)</a></li>
											<li><a href="../Pharmacologie/fc6.html">Pharmacodynamie</a></li>
											<li><a href="../Pharmacologie/fc7.html">Pharmscocinétique quantitative</a></li>
											<li><a href="../Pharmacologie/fc8.html">Causes pharmacocinétiques de variabilité</a></li>
											<li><a href="../Pharmacologie/fc9.html">Cibles et mécanismes d\u2019actions</a></li>
											<li><a href="../Pharmacologie/fc10.html">Iatrogénie</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">Biostatistiques</span>
										<ul>
											<li><a href="../Biostatistiques/fc1.html">Probabilité</a></li>
											<li><a href="../Biostatistiques/fc2.html">Tests diagnostiques</a></li>
											<li><a href="../Biostatistiques/fc3.html">Variables aléatoires</a></li>
											<li><a href="../Biostatistiques/fc4.html">Distribution usuelles</a></li>
											<li><a href="../Biostatistiques/fc5.html">Échantillon, population et théorème central</a></li>
											<li><a href="../Biostatistiques/fc6.html">Théorie des tests et degré de signification</a></li>
											<li><a href="../Biostatistiques/fc7.html">Test de comparaison</a></li>
											<li><a href="../Biostatistiques/fc8.html">X2</a></li>
											<li><a href="../Biostatistiques/fc9.html">Principaux types d\u2019études</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">UEDS Biologie</span>
										<ul>
											<li><a href="../UEDS_Biologie/fc1.html">Acides aminés</a></li>
											<li><a href="../UEDS_Biologie/fc2_1.html">Enzymologie (FC2.1)</a></li>
											<li><a href="../UEDS_Biologie/fc2_2.html">Enzymologie (FC2.2)</a></li>
											<li><a href="../UEDS_Biologie/fc3_1.html">Glucides (FC3.1)</a></li>
											<li><a href="../UEDS_Biologie/fc3_2.html">Glucides (FC3.2)</a></li>
											<li><a href="../UEDS_Biologie/fc4.html">Réplication procaryote</a></li>
											<li><a href="../UEDS_Biologie/fc5.html">Transcription</a></li>
											<li><a href="../UEDS_Biologie/fc6.html">Analyse cellulaire et moléculaire</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">UEDL IGHL</span>
										<ul>
											<li><a href="../UEDL_IGHL/fc1.html">La syntaxe</a></li>
											<li><a href="../UEDL_IGHL/fc2.html">Morphologie</a></li>
											<li><a href="../UEDL_IGHL/fc3.html">Introduction à l\u2019histoire de la langue</a></li>
											<li><a href="../UEDL_IGHL/fc4.html">Ancien français</a></li>
											<li><a href="../UEDL_IGHL/fc5.html">Le moyen français</a></li>
											<li><a href="../UEDL_IGHL/fc6.html">Français classique, post classique et moderne</a></li>
											<li><a href="../UEDL_IGHL/fc7.html">Les voyelles</a></li>
											<li><a href="../UEDL_IGHL/fc8.html">Les consonnes</a></li>
											<li><a href="../UEDL_IGHL/fc9.html">Le groupe nominal</a></li>
											<li><a href="../UEDL_IGHL/fc10.html">Le groupe verbal et le système pronominal</a></li>
											<li><a href="../UEDL_IGHL/fc11.html">Lexicologie historique</a></li>
											<li><a href="../UEDL_IGHL/fc12.html">Sémantique historique</a></li>
											<li><a href="../UEDL_IGHL/fc13.html">Dialectologie gallo-romane</a></li>
										</ul>
									</li>
									<li>
										<span class="opener">SHS</span>
										<ul>
											<li>
												<span class="opener">Santé numérique</span>
												<ul>
													<li><a href="../SHS/definition_acteurs_strategies.html">Définition, acteurs et stratégies nationales</a></li>
													<li><a href="../SHS/outils_pratiques_numeriques.html">Outils et pratiques numériques en santé</a></li>
													<li><a href="../SHS/traitement_donnees_sante.html">Traitement des données de santé</a></li>
												</ul>
											</li>
											<li>
												<span class="opener">Éthique et droit</span>
												<ul>
													<li><a href="../SHS/introduction_droit_sante.html">Introduction au droit de la santé</a></li>
													<li><a href="../SHS/introduction_ethique_medicale.html">Introduction à l\u2019éthique médicale (FC2)</a></li>
													<li><a href="../SHS/principisme_fin_de_vie.html">Principisme et fin de vie (FC3)</a></li>
													<li><a href="../SHS/progres_techniques_amp.html">Progrès techniques et AMP (FC4)</a></li>
												</ul>
											</li>
											<li>
												<span class="opener">Psychologie médicale</span>
												<ul>
													<li><a href="../SHS/psycho_emotion_comportement.html">Émotion et comportement (FC1)</a></li>
													<li><a href="../SHS/psycho_prevention_suicidaires.html">Prévention des conduites suicidaires (FC2)</a></li>
													<li><a href="../SHS/psycho_representations_corps.html">Les représentations du corps (FC3)</a></li>
													<li><a href="../SHS/psycho_stress_psychotraumatisme.html">Stress et psycho-traumatisme (FC4)</a></li>
													<li><a href="../SHS/psycho_developpement_affectif.html">Développement affectif et intellectuel (FC5)</a></li>
												</ul>
											</li>
										</ul>
									</li>
								</ul>
							</nav>'''

# Index sidebar (uses ./ prefix for SHS, direct paths for others)
SIDEBAR_INDEX = SIDEBAR_COURSE.replace('../', '')


def get_html_template(course):
    """Generate full HTML for a course file."""
    flashcards_js = "[\n"
    for q, a in course["flashcards"]:
        q_escaped = q.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        a_escaped = a.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        flashcards_js += f'  {{ question: "{q_escaped}", answer: "{a_escaped}" }},\n'
    flashcards_js += "]"

    return f'''<!DOCTYPE HTML>
<html>
<head>
<title>{course["page_title"]}</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../../images/diploma.jpeg" />
    <script src="../../assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<!-- Wrapper -->
<div id="wrapper">

<!-- Main -->
<div id="main">
<div class="inner">

<!-- Header -->
<header id="header">
<a href="../../index.html" class="logo"><strong>Diploma Santé</strong>- Plateforme de Flashcards</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
        <li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<!-- Content -->
<section>
<header class="main"><div class="header-left"><h1>{course["title_h1"]}</h1><h2>{course["title_h2"]}</h2></div><span class="image main"><img src="../../images/banner.png" alt="" /></span></header>

\t\t\t\t\t<style>  /* Header minimal avec contrôles accessibles */
  #header {{ padding: 1rem 0; margin-bottom: 0.5rem; }}
  header.main {{ margin-top: 1.5rem !important; margin-bottom: 0.8rem !important; padding-bottom: 0.5rem !important; display: flex; align-items: center; gap: 2rem; }}
  header.main .header-left h1, header.main .header-left h2 {{ flex: 1; margin: 0 !important; }}
  header.main h1 {{ font-size: 2em !important; line-height: 1.3 !important; }}
  header.main h2 {{ font-size: 1.3em !important; color: #7f888f !important; }}
  header.main .header-left {{ flex: 1; display: flex; flex-direction: column; }}
  .image.main {{ flex: 1; max-height: none !important; overflow: visible !important; margin: 0 !important; display: flex; align-items: center; justify-content: center; }}
  .image.main img {{ width: 100% !important; height: auto !important; max-height: 120px !important; object-fit: contain !important; object-position: center; }}
  section {{ padding-top: 0 !important; }}
  .progress-container {{ width: 100%; max-width: 1000px; height: 20px; background-color: #eee; border-radius: 10px; overflow: hidden; margin: 0 auto 1rem; border: 1px solid #ddd; }}
  .progress-bar {{ height: 100%; background-color: #00aeef; width: 0%; transition: width 0.3s; }}
  .flashcards-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2rem; min-height: calc(100vh - 250px); padding: 1rem 0; }}
  .flashcard {{ width: 100%; max-width: 1000px; height: calc(100vh - 340px); min-height: 450px; perspective: 1500px; cursor: pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }}
  .flashcard-inner {{ position: relative; width: 100%; height: 100%; border-radius: 20px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25); background-color: white; transition: transform 0.6s; overflow: visible; transform-style: preserve-3d; }}
  .flashcard.show-answer .flashcard-inner {{ transform: rotateY(180deg); }}
  .flashcard-front, .flashcard-back {{ position: absolute; width: 100%; height: 100%; border-radius: 20px; backface-visibility: hidden; display: flex; justify-content: center; align-items: center; padding: 3rem; font-size: 2rem; text-align: center; }}
  .flashcard-front {{ background-color: white; color: #333; box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.15); }}
  .flashcard-back {{ background-color: #73C3EC; color: white; overflow: visible; transform: rotateY(180deg); box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.5); font-size: 2.2rem; text-shadow: 0 0 4px rgba(255, 255, 255, 0.3); }}
  .flashcard-button {{ margin-top: 1rem; display: flex; justify-content: center; align-items: center; gap: 1rem; width: 100%; flex-wrap: wrap; }}
  .check-icon, .cross-icon, .favorite-icon {{ display: none; position: absolute; cursor: pointer; z-index: 1000; transition: all 0.3s; opacity: 0.8; pointer-events: auto; }}
  .check-icon {{ top: 30px; left: 30px; width: 45px; height: 45px; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); color: #888; font-size: 20px; }}
  .cross-icon {{ top: 30px; right: 30px; stroke: #888; width: 45px; height: 45px; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); }}
  body.dark-mode .check-icon, body.dark-mode .cross-icon {{ background: rgba(50, 50, 50, 0.95); color: #fff; stroke: #fff; }}
  .favorite-icon {{ bottom: 15px; left: 50%; transform: translateX(-50%); fill: #888; width: 30px; height: 30px; }}
  .favorite-icon.active {{ fill: #ffd700; }}
  .flashcard.show-answer .check-icon, .flashcard.show-answer .cross-icon, .flashcard.show-answer .favorite-icon {{ display: flex !important; }}
  .slide-left {{ animation: slideLeft 0.4s forwards; }}
  .slide-right {{ animation: slideRight 0.4s forwards; }}
  @keyframes slideLeft {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(-100%); opacity: 0; }} }}
  @keyframes slideRight {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(100%); opacity: 0; }} }}
  body.dark-mode .flashcard-front {{ background-color: #2d3436; color: #e2e8f0; }}
  body.dark-mode .flashcard-inner {{ background-color: #2d3436; }}
  body.dark-mode .progress-container {{ background-color: #34495e; border-color: #4a5568; }}
  @media screen and (max-width: 768px) {{ .flashcard {{ width: 95vw; height: calc(100vh - 180px); min-height: 450px; }} }}
</style>

</head>
<body>
<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>
 <div class="flashcards-container" id="flashcards"></div>

 <script>

const flashcardsData = {flashcards_js};

const container = document.getElementById("flashcards");
const progressBar = document.getElementById("progressBar");
const originalData = [...flashcardsData];
let flashcards = [...originalData];
const pageId = location.pathname.split("/").pop().replace(".html","");
const progressKey = "progress_" + pageId;
let currentIndex = parseInt(localStorage.getItem(progressKey)) || 0;
if (currentIndex >= originalData.length) {{ currentIndex = 0; localStorage.setItem(progressKey, currentIndex); }}

function updateProgress() {{
  const total = originalData.length;
  const progress = Math.min(currentIndex / total, 1);
  progressBar.style.width = (progress * 100) + "%";
}}

function showFlashcard(index) {{
  container.innerHTML = "";
  if (index >= flashcards.length) {{
    container.innerHTML = '<p style="text-align:center; font-size:1.5rem;">Bravo ! Vous avez terminé toutes les flashcards ! 🎉</p>';
    progressBar.style.width = "100%";
    localStorage.setItem("completed_" + pageId, "true");
    return;
  }}
  const fc = flashcards[index];
  const card = document.createElement("div");
  card.className = "flashcard";
  card.innerHTML = `
    <div class="flashcard-inner">
      <div class="flashcard-front"><span>${{fc.question}}</span></div>
      <div class="flashcard-back"><span>${{fc.answer.replace(/\\n/g, '<br>')}}</span></div>
      <div class="check-icon" title="Je savais">&#10004;</div>
      <svg class="cross-icon" title="Je ne savais pas" viewBox="0 0 24 24"><line x1="4" y1="4" x2="20" y2="20" stroke-width="3"/><line x1="20" y1="4" x2="4" y2="20" stroke-width="3"/></svg>
      <svg class="favorite-icon" title="Ajouter aux favoris" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
    </div>
  `;
  container.appendChild(card);
  card.querySelector(".flashcard-inner").addEventListener("click", function(e) {{
    if (!e.target.closest('.check-icon') && !e.target.closest('.cross-icon') && !e.target.closest('.favorite-icon')) {{
      card.classList.toggle("show-answer");
    }}
  }});
  card.querySelector(".check-icon").addEventListener("click", function(e) {{
    e.stopPropagation();
    card.querySelector(".flashcard-inner").classList.add("slide-right");
    setTimeout(() => {{ currentIndex++; localStorage.setItem(progressKey, currentIndex); updateProgress(); showFlashcard(currentIndex); }}, 400);
  }});
  card.querySelector(".cross-icon").addEventListener("click", function(e) {{
    e.stopPropagation();
    card.querySelector(".flashcard-inner").classList.add("slide-left");
    flashcards.push(fc);
    setTimeout(() => {{ currentIndex++; localStorage.setItem(progressKey, currentIndex); updateProgress(); showFlashcard(currentIndex); }}, 400);
  }});
  const favIcon = card.querySelector(".favorite-icon");
  const favKey = "fav_" + pageId + "_" + index;
  if (localStorage.getItem(favKey) === "true") favIcon.classList.add("active");
  favIcon.addEventListener("click", function(e) {{
    e.stopPropagation();
    const isActive = favIcon.classList.toggle("active");
    localStorage.setItem(favKey, isActive);
  }});
  updateProgress();
}}

showFlashcard(currentIndex);
</script>

</section>
</div>
</div>

<!-- Sidebar -->
<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>
{SIDEBAR_COURSE}

<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<!-- Scripts -->
<script src="../../assets/js/jquery.min.js"></script>
<script src="../../assets/js/browser.min.js"></script>
<script src="../../assets/js/breakpoints.min.js"></script>
<script src="../../assets/js/util.js"></script>
<script src="../../assets/js/main.js"></script>
<script src="../../assets/js/darkmode.js"></script>
<script src="../../assets/js/favorites.js"></script>

</body>
</html>'''


def generate_course_files():
    """Generate all 7 course HTML files."""
    os.makedirs(SHS_DIR, exist_ok=True)
    total_flashcards = 0
    for course in COURSES:
        filepath = os.path.join(SHS_DIR, course["filename"])
        html = get_html_template(course)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        n = len(course["flashcards"])
        total_flashcards += n
        print(f"  Created {course['filename']} ({n} flashcards)")
    print(f"\nTotal: {len(COURSES)} files, {total_flashcards} flashcards")


def update_existing_sidebars():
    """Update sidebar in all existing SU_S2 HTML files."""
    count = 0
    for root, dirs, files in os.walk(SU_S2_DIR):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = os.path.join(root, fname)
            # Skip newly created files (they already have the right sidebar)
            if fname in [c["filename"] for c in COURSES]:
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if '<nav id="menu">' not in content:
                continue

            # Determine prefix based on file location
            rel_path = os.path.relpath(filepath, SU_S2_DIR)
            depth = rel_path.count(os.sep)

            if depth == 0:
                # Files in SU_S2/ root (index.html, favorites.html)
                new_sidebar = SIDEBAR_INDEX
            else:
                # Files in subdirectories (SHS/, Physiologie/, etc.)
                new_sidebar = SIDEBAR_COURSE

            # Replace the nav block
            pattern = r'<nav id="menu">.*?</nav>'
            new_content = re.sub(pattern, new_sidebar, content, flags=re.DOTALL)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1

    print(f"Updated sidebar in {count} existing files")


def update_index():
    """Update SU_S2/index.html: add Psychologie médicale card and update COURSE_PATHS."""
    index_path = os.path.join(SU_S2_DIR, "index.html")
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add Psychologie médicale card before </div></section>
    psycho_card = '''										<article>
											<span class="icon solid fa-brain"></span>
											<div class="content">
												<h3>SHS - Psychologie médicale</h3>
												<ul class="actions">
													<li><a href="SHS/psycho_emotion_comportement.html" class="button big">Commencer</a></li>
												</ul>
											</div>
										</article>'''

    # Insert before the closing </div></section> (after last article)
    content = content.replace(
        '''									</div>
								</section>''',
        psycho_card + '''
									</div>
								</section>'''
    )

    # Update COURSE_PATHS to include new courses
    old_paths_end = "'SHS/introduction_droit_sante.html', 'SHS/introduction_ethique_medicale.html'"
    new_paths_end = """'SHS/introduction_droit_sante.html', 'SHS/introduction_ethique_medicale.html',
				'SHS/principisme_fin_de_vie.html', 'SHS/progres_techniques_amp.html',
				'SHS/psycho_emotion_comportement.html', 'SHS/psycho_prevention_suicidaires.html',
				'SHS/psycho_representations_corps.html', 'SHS/psycho_stress_psychotraumatisme.html',
				'SHS/psycho_developpement_affectif.html'"""
    content = content.replace(old_paths_end, new_paths_end)

    # Update total count comment
    content = content.replace("// 62", "// 69")

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated SU_S2/index.html (new card + 7 course paths)")


def main():
    print("=== Generating SU S2 SHS additions ===\n")

    print("1. Generating 7 course files...")
    generate_course_files()

    print("\n2. Updating existing sidebars...")
    update_existing_sidebars()

    print("\n3. Updating index.html...")
    update_index()

    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
