import re

flashcards = [
    ("Pourquoi les art\u00e8res coronaires sont-elles dites \u00ab de type terminal \u00bb ?", "Car elles n\u2019ont pas ou peu d\u2019anastomoses fonctionnelles ; leur obstruction entra\u00eene une isch\u00e9mie puis un infarctus du territoire concern\u00e9."),
    ("Quelle est la cons\u00e9quence d\u2019une obstruction d\u2019une art\u00e8re coronaire ?", "Une isch\u00e9mie myocardique suivie d\u2019un infarctus du myocarde."),
    ("Pourquoi l\u2019infarctus du myocarde est-il si grave ?", "C\u2019est la principale cause de mortalit\u00e9 dans les pays industrialis\u00e9s."),
    ("\u00c0 quel moment du cycle cardiaque les art\u00e8res coronaires se remplissent-elles ?", "Pendant la diastole uniquement."),
    ("Pourquoi les coronaires ne se remplissent-elles pas pendant la systole ?", "La contraction du myocarde comprime les art\u00e8res intra-murales et les cuspides aortiques ouvertes obstruent les ostia coronaires."),
    ("D\u2019o\u00f9 na\u00eet l\u2019art\u00e8re coronaire droite ?", "De l\u2019aorte ascendante, au niveau du flanc ant\u00e9ro-lat\u00e9ral droit."),
    ("Dans quel sinus aortique na\u00eet la coronaire droite ?", "Le sinus de Valsalva ant\u00e9ro-lat\u00e9ral droit."),
    ("Combien de segments distingue-t-on dans l\u2019art\u00e8re coronaire droite ?", "Trois segments."),
    ("D\u00e9crivez le premier segment de la coronaire droite.", "Un segment court allant de l\u2019ostium jusqu\u2019au sillon coronaire droit."),
    ("D\u00e9crivez le deuxi\u00e8me segment de la coronaire droite.", "Un segment vertical cheminant dans le sillon coronaire droit (face ant\u00e9rieure du c\u0153ur)."),
    ("D\u00e9crivez le troisi\u00e8me segment de la coronaire droite.", "Un segment \u00e0 la face inf\u00e9rieure du c\u0153ur, allant jusqu\u2019\u00e0 la croix des sillons."),
    ("Qu\u2019est-ce que la croix des sillons ?", "Le point de rencontre du sillon coronaire, du sillon interventriculaire ant\u00e9rieur et du sillon interventriculaire post\u00e9rieur \u00e0 la face inf\u00e9rieure du c\u0153ur."),
    ("Quels coudes s\u00e9parent les segments de la coronaire droite ?", "Un coude sup\u00e9rieur (entre 1er et 2\u1d49 segments) et un coude inf\u00e9rieur (entre 2\u1d49 et 3\u1d49 segments)."),
    ("Qu\u2019est-ce qu\u2019une coronarographie ?", "Un examen d\u2019imagerie permettant d\u2019opacifier les art\u00e8res coronaires pour d\u00e9tecter d\u2019\u00e9ventuelles obstructions."),
    ("Quelles sont les branches ascendantes principales de la coronaire droite ?", "Les art\u00e8res atriales, dont l\u2019art\u00e8re atriale droite sup\u00e9rieure qui vascularise le n\u0153ud sino-atrial."),
    ("Quelle branche de la coronaire droite vascularise le n\u0153ud sino-atrial ?", "L\u2019art\u00e8re atriale droite sup\u00e9rieure."),
    ("Pourquoi l\u2019art\u00e8re du n\u0153ud sino-atrial est-elle appel\u00e9e \u00ab art\u00e8re du pacemaker \u00bb ?", "Car elle vascularise le n\u0153ud sino-atrial, le pacemaker naturel du c\u0153ur."),
    ("Que vascularisent les branches descendantes de la coronaire droite ?", "Le ventricule droit, sans atteindre le sillon interventriculaire ant\u00e9rieur."),
    ("Qu\u2019est-ce que l\u2019art\u00e8re du c\u00f4ne art\u00e9riel ?", "Une branche de la coronaire droite qui vascularise l\u2019infundibulum pulmonaire (c\u00f4ne art\u00e9riel du ventricule droit)."),
    ("Que vascularise l\u2019art\u00e8re du c\u00f4ne art\u00e9riel ?", "L\u2019infundibulum pulmonaire (voie d\u2019\u00e9jection du ventricule droit vers le tronc pulmonaire)."),
    ("Quelles sont les deux branches terminales de la coronaire droite ?", "Le tronc r\u00e9troventriculaire gauche inf\u00e9rieur et l\u2019art\u00e8re interventriculaire inf\u00e9rieure (post\u00e9rieure)."),
    ("Que vascularise le tronc r\u00e9troventriculaire gauche inf\u00e9rieur ?", "La face inf\u00e9rieure du ventricule gauche, une partie de l\u2019atrium gauche, et le n\u0153ud AV via une art\u00e8re septale."),
    ("Quelle structure le tronc r\u00e9troventriculaire gauche vascularise-t-il via son art\u00e8re septale ?", "Le n\u0153ud atrio-ventriculaire."),
    ("Jusqu\u2019o\u00f9 se prolonge l\u2019art\u00e8re interventriculaire inf\u00e9rieure ?", "Plus ou moins jusqu\u2019\u00e0 l\u2019apex du c\u0153ur."),
    ("D\u2019o\u00f9 na\u00eet l\u2019art\u00e8re coronaire gauche ?", "De l\u2019aorte ascendante, au niveau du flanc ant\u00e9ro-lat\u00e9ral gauche."),
    ("Dans quel sinus aortique na\u00eet la coronaire gauche ?", "Le sinus de Valsalva ant\u00e9ro-lat\u00e9ral gauche."),
    ("Combien de sinus aortiques sont coronaires ?", "Deux : les sinus ant\u00e9rieurs (droit et gauche) sont coronaires."),
    ("Quel sinus aortique est non coronaire ?", "Le sinus post\u00e9rieur."),
    ("Comment s\u2019appelle le tronc initial de la coronaire gauche ?", "Le tronc commun de la coronaire gauche (ou tronc coronaire gauche)."),
    ("En quelles branches principales le tronc coronaire gauche se divise-t-il ?", "L\u2019art\u00e8re interventriculaire ant\u00e9rieure (IVA) et l\u2019art\u00e8re circonflexe."),
    ("Qu\u2019est-ce que l\u2019art\u00e8re circonflexe ?", "Une branche de la coronaire gauche qui chemine dans le sillon atrio-ventriculaire gauche."),
    ("O\u00f9 chemine l\u2019art\u00e8re circonflexe ?", "Dans le sillon atrio-ventriculaire gauche."),
    ("Quelles branches donne l\u2019art\u00e8re circonflexe ?", "Des branches ascendantes pour l\u2019atrium gauche et des branches descendantes marginales pour le ventricule gauche."),
    ("Que vascularisent les branches ascendantes de la circonflexe ?", "L\u2019atrium gauche."),
    ("Que vascularisent les branches descendantes (marginales) de la circonflexe ?", "La paroi lat\u00e9rale du ventricule gauche."),
    ("Qu\u2019est-ce que la dominance cardiaque ?", "Le terme d\u00e9signant quelle coronaire (droite ou gauche) vascularise la face inf\u00e9rieure du c\u0153ur et atteint la croix des sillons."),
    ("Qu\u2019est-ce que la dominance droite ?", "La coronaire droite atteint la croix des sillons et donne le tronc r\u00e9troventriculaire gauche et l\u2019IVP ; c\u2019est la situation la plus fr\u00e9quente."),
    ("Qu\u2019est-ce que la dominance gauche ?", "La circonflexe atteint la croix des sillons et remplace le tronc r\u00e9troventriculaire gauche, parfois m\u00eame l\u2019interventriculaire inf\u00e9rieure."),
    ("Quelle dominance cardiaque est la plus fr\u00e9quente ?", "La dominance droite (environ 85% des cas)."),
    ("Quel est le trajet initial de l\u2019IVA ?", "Elle na\u00eet en arri\u00e8re du tronc pulmonaire, le contourne par la gauche et rejoint le sillon interventriculaire ant\u00e9rieur."),
    ("O\u00f9 chemine l\u2019IVA apr\u00e8s avoir contourn\u00e9 le tronc pulmonaire ?", "Dans le sillon interventriculaire ant\u00e9rieur, en direction de l\u2019apex."),
    ("Jusqu\u2019o\u00f9 descend l\u2019IVA ?", "Jusqu\u2019\u00e0 l\u2019apex du c\u0153ur, et parfois elle se retourne dans le sillon interventriculaire post\u00e9rieur."),
    ("Quelles branches droites l\u2019IVA donne-t-elle ?", "Des branches courtes et fines pour la portion du ventricule droit non vascularis\u00e9e par la coronaire droite."),
    ("Quelles branches gauches l\u2019IVA donne-t-elle ?", "Les art\u00e8res diagonales (2 \u00e0 4) pour la face ant\u00e9rieure du ventricule gauche."),
    ("Que sont les art\u00e8res diagonales ?", "Des branches de l\u2019IVA, au nombre de 2 \u00e0 4, qui vascularisent la face ant\u00e9rieure du ventricule gauche."),
    ("Qu\u2019est-ce que l\u2019art\u00e8re bissectrice ?", "Une art\u00e8re diagonale particuli\u00e8rement volumineuse n\u00e9e d\u2019une bifurcation (ou trifurcation) du tronc commun de la coronaire gauche."),
    ("Quand parle-t-on de trifurcation du tronc coronaire gauche ?", "Lorsque le tronc se divise en trois branches : IVA, circonflexe et art\u00e8re bissectrice."),
    ("Quelles branches septales l\u2019IVA donne-t-elle ?", "Des art\u00e8res septales (perforantes) qui p\u00e9n\u00e8trent le septum interventriculaire."),
    ("Quelle art\u00e8re septale est souvent la plus volumineuse ?", "La deuxi\u00e8me art\u00e8re septale."),
    ("Que vascularise la deuxi\u00e8me art\u00e8re septale ?", "Le trab\u00e9cule septo-marginal, le muscle papillaire ant\u00e9rieur et le faisceau atrio-ventriculaire (His)."),
    ("Quel est le rapport entre la 2\u1d49 art\u00e8re septale et le faisceau de His ?", "La 2\u1d49 art\u00e8re septale vascularise les branches du faisceau de His."),
    ("Quel est le rapport entre la 2\u1d49 art\u00e8re septale et le trab\u00e9cule septo-marginal ?", "La 2\u1d49 art\u00e8re septale vascularise le trab\u00e9cule septo-marginal qui contient la branche droite du faisceau de His."),
    ("Quel est le rapport entre la 2\u1d49 art\u00e8re septale et le muscle papillaire ant\u00e9rieur ?", "Elle vascularise le muscle papillaire ant\u00e9rieur du ventricule droit."),
    ("Qu\u2019est-ce que le sinus veineux coronaire ?", "Le principal collecteur veineux du c\u0153ur, drainant la majorit\u00e9 du sang veineux cardiaque vers l\u2019atrium droit."),
    ("Quelles sont les dimensions du sinus coronaire ?", "Environ 3 cm de long et 12 mm de large."),
    ("O\u00f9 chemine le sinus coronaire ?", "Dans le sillon interventriculaire inf\u00e9rieur gauche (sillon AV gauche) puis s\u2019abouche dans l\u2019atrium droit."),
    ("O\u00f9 le sinus coronaire se jette-t-il ?", "Dans l\u2019atrium droit, pr\u00e8s du septum inter-atrial."),
    ("Qu\u2019est-ce que la grande veine du c\u0153ur ?", "La principale veine cardiaque, qui se jette dans le sinus coronaire."),
    ("Quel est le trajet de la grande veine du c\u0153ur ?", "Elle na\u00eet \u00e0 l\u2019apex, remonte dans le sillon interventriculaire ant\u00e9rieur puis rejoint le sillon atrio-ventriculaire gauche."),
    ("Quelles veines la grande veine du c\u0153ur re\u00e7oit-elle ?", "La veine oblique de Marshall et la veine interventriculaire inf\u00e9rieure."),
    ("Qu\u2019est-ce que la veine de Marshall ?", "La veine oblique de l\u2019atrium gauche, vestige embryonnaire de la veine cave sup\u00e9rieure gauche, se jetant dans le sinus coronaire."),
    ("Qu\u2019est-ce que la petite veine du c\u0153ur ?", "Une veine qui chemine dans le sillon coronaire inf\u00e9rieur droit et se jette dans le sinus coronaire."),
    ("O\u00f9 chemine la petite veine du c\u0153ur ?", "Dans le sillon coronaire inf\u00e9rieur droit."),
    ("Que sont les veines de Galien ?", "Les veines ventriculaires ant\u00e9rieures droites, des petites veines qui se drainent directement dans l\u2019atrium droit."),
    ("O\u00f9 se drainent les veines de Galien ?", "Directement dans l\u2019atrium droit, sans passer par le sinus coronaire."),
    ("Que sont les veines de Th\u00e9b\u00e9sius ?", "Les veines minimes du c\u0153ur (venae cordis minimae) qui se drainent directement dans les cavit\u00e9s cardiaques."),
    ("O\u00f9 se drainent les veines de Th\u00e9b\u00e9sius ?", "Directement dans les cavit\u00e9s cardiaques (atriums et ventricules) \u00e0 travers les parois."),
    ("Quels sont les trois syst\u00e8mes de drainage veineux du c\u0153ur ?", "Le sinus coronaire (principal), les veines de Galien (accessoires) et les veines de Th\u00e9b\u00e9sius (minimes)."),
    ("Quel rapport existe entre la grande veine coronaire et l\u2019IVA ?", "La grande veine coronaire croise l\u2019IVA dans le sillon interventriculaire ant\u00e9rieur avant de rejoindre la circonflexe."),
    ("Quel est le rapport entre l\u2019art\u00e8re circonflexe et le sinus coronaire ?", "Ils cheminent tous deux dans le sillon atrio-ventriculaire gauche, le sinus coronaire \u00e9tant plus post\u00e9rieur."),
    ("Quelle est la premi\u00e8re branche de la coronaire droite ?", "L\u2019art\u00e8re du c\u00f4ne art\u00e9riel (infundibulaire)."),
    ("Pourquoi une l\u00e9sion du tronc commun de la coronaire gauche est-elle particuli\u00e8rement grave ?", "Car elle compromet la vascularisation de l\u2019IVA et de la circonflexe, mena\u00e7ant une grande partie du myocarde."),
    ("Quels sont les territoires vascularis\u00e9s par la coronaire droite en dominance droite ?", "L\u2019atrium droit, le ventricule droit, la face inf\u00e9rieure du ventricule gauche, le n\u0153ud SA et le n\u0153ud AV."),
    ("Quels sont les territoires vascularis\u00e9s par l\u2019IVA ?", "La face ant\u00e9rieure des deux ventricules, l\u2019apex, les deux tiers ant\u00e9rieurs du septum interventriculaire."),
    ("Quels sont les territoires vascularis\u00e9s par l\u2019art\u00e8re circonflexe ?", "L\u2019atrium gauche et la paroi lat\u00e9rale du ventricule gauche."),
    ("Qu\u2019est-ce qu\u2019un infarctus du myocarde ant\u00e9rieur ?", "Un infarctus par occlusion de l\u2019IVA, touchant la face ant\u00e9rieure du ventricule gauche et le septum."),
    ("Qu\u2019est-ce qu\u2019un infarctus du myocarde inf\u00e9rieur ?", "Un infarctus par occlusion de la coronaire droite (ou de la circonflexe), touchant la face inf\u00e9rieure du ventricule gauche."),
    ("Qu\u2019est-ce qu\u2019un infarctus lat\u00e9ral ?", "Un infarctus par occlusion de l\u2019art\u00e8re circonflexe ou d\u2019une diagonale, touchant la paroi lat\u00e9rale du ventricule gauche."),
    ("Quelle art\u00e8re est le plus souvent responsable d\u2019un infarctus ant\u00e9rieur ?", "L\u2019art\u00e8re interventriculaire ant\u00e9rieure (IVA)."),
    ("Quelle art\u00e8re est le plus souvent responsable d\u2019un infarctus inf\u00e9rieur ?", "L\u2019art\u00e8re coronaire droite (en dominance droite)."),
    ("Qu\u2019est-ce que l\u2019ath\u00e9roscl\u00e9rose coronaire ?", "L\u2019accumulation de plaques d\u2019ath\u00e9rome dans la paroi des art\u00e8res coronaires, r\u00e9duisant leur lumi\u00e8re."),
    ("Quel lien existe entre l\u2019ath\u00e9roscl\u00e9rose coronaire et l\u2019infarctus ?", "La rupture d\u2019une plaque d\u2019ath\u00e9rome provoque une thrombose qui obstrue la coronaire, causant l\u2019infarctus."),
    ("Qu\u2019est-ce qu\u2019une angioplastie coronaire ?", "Un geste interventionnel consistant \u00e0 dilater une art\u00e8re coronaire r\u00e9tr\u00e9cie \u00e0 l\u2019aide d\u2019un ballonnet, souvent avec pose d\u2019un stent."),
    ("Qu\u2019est-ce qu\u2019un pontage coronarien ?", "Une intervention chirurgicale cr\u00e9ant un nouveau trajet pour le sang en contournant l\u2019art\u00e8re coronaire obstruée."),
    ("Pourquoi la 1\u00e8re diagonale de l\u2019IVA est-elle cliniquement importante ?", "Car son occlusion peut causer un infarctus ant\u00e9ro-lat\u00e9ral significatif du ventricule gauche."),
    ("Quel est le rapport entre le tronc pulmonaire et l\u2019IVA ?", "L\u2019IVA na\u00eet en arri\u00e8re du tronc pulmonaire et le contourne par la gauche."),
    ("Quelles structures sont visibles en dissection dans le territoire de la coronaire gauche ?", "Le sillon IVA, l\u2019IVA, l\u2019auricule gauche, l\u2019auricule droit, la coronaire droite, le tronc pulmonaire et l\u2019aorte ascendante."),
    ("Quelle est la position relative des deux sinus coronaires par rapport au sinus non coronaire ?", "Les deux sinus coronaires sont ant\u00e9rieurs ; le sinus non coronaire est post\u00e9rieur."),
    ("Que signifie \u00ab art\u00e8re de type terminal \u00bb en termes de perfusion myocardique ?", "Chaque art\u00e8re irrigue un territoire d\u00e9fini sans suppl\u00e9ance efficace par d\u2019autres art\u00e8res en cas d\u2019obstruction."),
    ("Quel est le rapport entre la dominance cardiaque et la vascularisation du n\u0153ud AV ?", "En dominance droite, le n\u0153ud AV est vascularis\u00e9 par la coronaire droite ; en dominance gauche, par la circonflexe."),
    ("O\u00f9 l\u2019IVA peut-elle se retourner apr\u00e8s l\u2019apex ?", "Dans le sillon interventriculaire post\u00e9rieur (wrap-around LAD)."),
    ("Quel est le rapport entre le coude sup\u00e9rieur de la coronaire droite et le sillon coronaire ?", "Le coude sup\u00e9rieur marque l\u2019entr\u00e9e de la coronaire droite dans le sillon coronaire droit."),
    ("Quel est le rapport entre le coude inf\u00e9rieur de la coronaire droite et la face inf\u00e9rieure du c\u0153ur ?", "Le coude inf\u00e9rieur marque le passage de la coronaire droite vers la face inf\u00e9rieure du c\u0153ur."),
    ("Quelle est la principale cause de mortalit\u00e9 dans les pays industrialis\u00e9s en lien avec les coronaires ?", "L\u2019infarctus du myocarde par obstruction d\u2019une art\u00e8re coronaire."),
    ("Quel est le r\u00f4le de la grande veine coronaire dans le retour veineux cardiaque ?", "Elle draine le sang veineux de la face ant\u00e9rieure du c\u0153ur et le conduit vers le sinus coronaire."),
    ("Qu\u2019est-ce que la veine interventriculaire inf\u00e9rieure ?", "Une veine qui chemine dans le sillon interventriculaire post\u00e9rieur et se jette dans la grande veine du c\u0153ur ou le sinus coronaire."),
    ("Combien de diagonales l\u2019IVA donne-t-elle habituellement ?", "De 2 \u00e0 4 art\u00e8res diagonales."),
    ("Quel est le r\u00f4le des art\u00e8res septales dans la vascularisation du c\u0153ur ?", "Elles p\u00e9n\u00e8trent le septum interventriculaire pour vasculariser la cloison entre les ventricules et le syst\u00e8me de conduction."),
    ("Quels facteurs de risque favorisent l\u2019ath\u00e9roscl\u00e9rose coronaire ?", "L\u2019hypercholest\u00e9rol\u00e9mie, le tabagisme, l\u2019hypertension, le diab\u00e8te, l\u2019ob\u00e9sit\u00e9 et la s\u00e9dentarit\u00e9."),
    ("Qu\u2019est-ce qu\u2019un stent coronaire ?", "Un petit dispositif m\u00e9tallique en forme de treillis plac\u00e9 dans une art\u00e8re coronaire pour maintenir sa lumi\u00e8re ouverte apr\u00e8s une angioplastie."),
]

assert len(flashcards) == 100, f"Expected 100 flashcards, got {len(flashcards)}"

# Build JS array
lines = ["const flashcardsData = ["]
for q, a in flashcards:
    lines.append(f"{{ question: '{q}', answer: '{a}' }},")
lines.append("];")
new_data = "\n".join(lines)

# Read file
filepath = "/Users/cyrilwisa/Desktop/diploma/UPEC_LSPS1_S2/Circulation_Respiration/Anatomie/fc5.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace
content = re.sub(r'const flashcardsData\s*=\s*\[.*?\];', new_data, content, flags=re.DOTALL)

# Write
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"fc5.html updated with {len(flashcards)} flashcards")
