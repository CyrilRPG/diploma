import re

flashcards = [
    ("Quelles sont les trois couches constituant la paroi cardiaque ?", "Le myocarde, l\u2019endocarde et le p\u00e9ricarde."),
    ("De quoi est constitu\u00e9 le myocarde ?", "De faisceaux de cellules musculaires stri\u00e9es contractiles, auriculaires et ventriculaires, ins\u00e9r\u00e9es sur une charpente fibreuse."),
    ("Quel type cellulaire compose le myocarde ?", "Des cellules musculaires stri\u00e9es contractiles (cardiomyocytes)."),
    ("Qu\u2019est-ce que l\u2019endocarde ?", "Un \u00e9pith\u00e9lium qui tapisse l\u2019int\u00e9rieur des cavit\u00e9s cardiaques, en continuit\u00e9 avec l\u2019endoth\u00e9lium des vaisseaux sanguins."),
    ("Avec quelle structure l\u2019endocarde est-il en continuit\u00e9 ?", "Avec l\u2019endoth\u00e9lium des vaisseaux sanguins."),
    ("Quel est le r\u00f4le du p\u00e9ricarde ?", "Enveloppe protectrice du c\u0153ur, il facilite les mouvements cardiaques et fixe le c\u0153ur dans le m\u00e9diastin."),
    ("Sur quoi les cellules musculaires du myocarde s\u2019ins\u00e8rent-elles ?", "Sur la charpente fibreuse du c\u0153ur form\u00e9e par les anneaux valvulaires et les trigones."),
    ("Que forme la charpente fibreuse du c\u0153ur ?", "Quatre anneaux fibreux valvulaires : atrio-ventriculaire droit, atrio-ventriculaire gauche, aortique et pulmonaire."),
    ("Quels sont les quatre anneaux fibreux valvulaires ?", "L\u2019anneau atrio-ventriculaire droit, l\u2019anneau atrio-ventriculaire gauche, l\u2019anneau aortique et l\u2019anneau pulmonaire."),
    ("O\u00f9 est situ\u00e9 l\u2019anneau pulmonaire par rapport \u00e0 l\u2019orifice aortique ?", "En avant et \u00e0 gauche de l\u2019orifice aortique."),
    ("Quel est le r\u00f4le de la charpente fibreuse du c\u0153ur ?", "Servir de squelette d\u2019insertion pour les faisceaux musculaires et les valves, et assurer l\u2019isolation \u00e9lectrique entre atriums et ventricules."),
    ("Quels sont les deux trigones fibreux du c\u0153ur ?", "Le trigone ant\u00e9rieur gauche (aorto-mitral) et le trigone post\u00e9rieur gauche (mitro-tricuspidien)."),
    ("Quel autre nom donne-t-on au trigone ant\u00e9rieur gauche ?", "Le trigone aorto-mitral."),
    ("Quel autre nom donne-t-on au trigone post\u00e9rieur gauche ?", "Le trigone mitro-tricuspidien."),
    ("Quels anneaux le trigone aorto-mitral relie-t-il ?", "Il relie l\u2019anneau aortique et l\u2019anneau mitral (AV gauche)."),
    ("Quels anneaux le trigone mitro-tricuspidien relie-t-il ?", "Il relie l\u2019anneau mitral (AV gauche) et l\u2019anneau tricuspidien (AV droit)."),
    ("Combien de cuspides poss\u00e8de la valve pulmonaire ?", "Trois cuspides : post\u00e9rieure droite, post\u00e9rieure gauche et ant\u00e9rieure."),
    ("Nommez les trois cuspides de la valve pulmonaire.", "La cuspide post\u00e9rieure droite, la cuspide post\u00e9rieure gauche et la cuspide ant\u00e9rieure."),
    ("\u00c0 quel moment du cycle cardiaque la valve pulmonaire s\u2019ouvre-t-elle ?", "Pendant la systole ventriculaire."),
    ("\u00c0 quel moment du cycle cardiaque la valve pulmonaire se ferme-t-elle ?", "Pendant la diastole ventriculaire."),
    ("Quel est le r\u00f4le de la valve pulmonaire ?", "Emp\u00eacher le reflux du sang du tronc pulmonaire vers le ventricule droit lors de la diastole."),
    ("La valve pulmonaire est-elle une valve sigmo\u00efde ou atrio-ventriculaire ?", "C\u2019est une valve sigmo\u00efde (semi-lunaire)."),
    ("Combien de cuspides poss\u00e8de la valve aortique ?", "Trois cuspides : ant\u00e9rieure droite, ant\u00e9rieure gauche et post\u00e9rieure."),
    ("Nommez les trois cuspides de la valve aortique.", "La cuspide ant\u00e9rieure droite (coronaire droite), la cuspide ant\u00e9rieure gauche (coronaire gauche) et la cuspide post\u00e9rieure (non coronaire)."),
    ("La valve aortique est-elle une valve sigmo\u00efde ou atrio-ventriculaire ?", "C\u2019est une valve sigmo\u00efde (semi-lunaire)."),
    ("Quand la valve aortique s\u2019ouvre-t-elle ?", "Pendant la systole ventriculaire, lorsque la pression dans le ventricule gauche d\u00e9passe la pression aortique."),
    ("Quand la valve aortique se ferme-t-elle ?", "Pendant la diastole, lorsque la pression aortique d\u00e9passe la pression ventriculaire gauche."),
    ("Qu\u2019est-ce qu\u2019un sinus aortique ?", "Une dilatation de l\u2019origine de l\u2019aorte situ\u00e9e derri\u00e8re chaque cuspide de la valve aortique."),
    ("Combien de sinus aortiques y a-t-il ?", "Trois sinus aortiques, un derri\u00e8re chaque cuspide."),
    ("Quels sinus aortiques sont dits \u00ab coronaires \u00bb ?", "Les deux sinus ant\u00e9rieurs (droit et gauche) car ils contiennent les ostia des art\u00e8res coronaires."),
    ("Quel sinus aortique est dit \u00ab non coronaire \u00bb ?", "Le sinus post\u00e9rieur, car il ne donne naissance \u00e0 aucune art\u00e8re coronaire."),
    ("Que trouve-t-on au niveau des sinus aortiques coronaires ?", "Les ostia (orifices) des art\u00e8res coronaires droite et gauche."),
    ("\u00c0 quel moment exclusif du cycle cardiaque les art\u00e8res coronaires se remplissent-elles ?", "Uniquement pendant la diastole."),
    ("Pourquoi les coronaires se remplissent-elles en diastole et non en systole ?", "Pendant la systole, la contraction du myocarde comprime les art\u00e8res coronaires intra-murales et la valve aortique ouverte obstrue les ostia coronaires."),
    ("Quel est le r\u00f4le du sinus aortique dans le remplissage coronaire ?", "En diastole, le reflux sanguin remplit les sinus aortiques et pousse le sang dans les ostia coronaires."),
    ("La valve mitrale est-elle une valve sigmo\u00efde ou atrio-ventriculaire ?", "C\u2019est une valve atrio-ventriculaire gauche."),
    ("Quels \u00e9l\u00e9ments composent la valve mitrale ?", "Un anneau fibreux, deux cuspides (ant\u00e9rieure et post\u00e9rieure), des commissures, des cordages tendineux et des piliers (muscles papillaires)."),
    ("Combien de cuspides poss\u00e8de la valve mitrale ?", "Deux cuspides : ant\u00e9rieure et post\u00e9rieure."),
    ("Comment est subdivis\u00e9e la cuspide ant\u00e9rieure de la valve mitrale ?", "En trois segments : A1, A2 et A3."),
    ("Comment est subdivis\u00e9e la cuspide post\u00e9rieure de la valve mitrale ?", "En trois segments : P1, P2 et P3."),
    ("Quelles sont les caract\u00e9ristiques morphologiques de la cuspide ant\u00e9rieure mitrale ?", "Tr\u00e8s mobile, de forme carr\u00e9e, elle occupe un tiers de la circonf\u00e9rence annulaire mais couvre une grande surface."),
    ("Quelles sont les caract\u00e9ristiques de la cuspide post\u00e9rieure mitrale ?", "Arciforme, elle occupe deux tiers de la circonf\u00e9rence annulaire et sert de but\u00e9e \u00e0 la cuspide ant\u00e9rieure lors de la coaptation."),
    ("Quel est le r\u00f4le de la cuspide post\u00e9rieure mitrale par rapport \u00e0 l\u2019ant\u00e9rieure ?", "Elle sert de but\u00e9e \u00e0 la cuspide ant\u00e9rieure pour assurer la coaptation valvulaire."),
    ("Qu\u2019est-ce que la coaptation valvulaire mitrale ?", "La fermeture \u00e9tanche de la valve par contact des bords libres des deux cuspides lors de la systole ventriculaire."),
    ("Que sont les commissures de la valve mitrale ?", "Les zones de jonction entre les cuspides ant\u00e9rieure et post\u00e9rieure, o\u00f9 les feuillets se rejoignent."),
    ("Quelle est la forme de l\u2019anneau fibreux mitral ?", "En forme de D ou de selle (forme en selle de cheval)."),
    ("Comment se modifie l\u2019anneau mitral au cours du cycle cardiaque ?", "Son relief en selle s\u2019accentue pendant la systole ventriculaire."),
    ("Quelles structures vasculaires passent autour de l\u2019anneau mitral ?", "L\u2019art\u00e8re circonflexe et le sinus coronaire."),
    ("Quel rapport anatomique existe entre l\u2019art\u00e8re circonflexe et la valve mitrale ?", "L\u2019art\u00e8re circonflexe chemine dans le sillon atrio-ventriculaire gauche, passant autour de l\u2019anneau mitral."),
    ("Quel rapport anatomique existe entre le sinus coronaire et la valve mitrale ?", "Le sinus coronaire chemine \u00e0 proximit\u00e9 de l\u2019anneau mitral post\u00e9rieur dans le sillon atrio-ventriculaire gauche."),
    ("Pourquoi le rapport entre l\u2019art\u00e8re circonflexe et l\u2019anneau mitral est-il cliniquement important ?", "Lors de la chirurgie mitrale ou de l\u2019annuloplastie, il y a un risque de l\u00e9sion de l\u2019art\u00e8re circonflexe."),
    ("Qu\u2019est-ce que l\u2019appareil sous-valvulaire de la valve mitrale ?", "L\u2019ensemble des cordages tendineux et des muscles papillaires (piliers) qui retiennent les cuspides."),
    ("Quels sont les trois ordres de cordages tendineux de la valve mitrale ?", "Cordages de 1er ordre (bord libre des cuspides), 2\u1d49 ordre (face ventriculaire/corps des cuspides) et 3\u1d49 ordre (base des cuspides)."),
    ("O\u00f9 s\u2019ins\u00e8rent les cordages de 1er ordre ?", "Sur l\u2019extr\u00e9mit\u00e9 distale (bord libre) des cuspides."),
    ("O\u00f9 s\u2019ins\u00e8rent les cordages de 2\u1d49 ordre ?", "Sur le corps (face ventriculaire) des cuspides."),
    ("O\u00f9 s\u2019ins\u00e8rent les cordages de 3\u1d49 ordre ?", "Sur la base des cuspides, pr\u00e8s de l\u2019anneau fibreux."),
    ("Quel est le r\u00f4le des cordages tendineux ?", "Maintenir les cuspides en position et emp\u00eacher leur prolapsus dans l\u2019atrium pendant la systole ventriculaire."),
    ("Combien de muscles papillaires (piliers) poss\u00e8de le ventricule gauche pour la valve mitrale ?", "Deux : le pilier ant\u00e9ro-lat\u00e9ral et le pilier post\u00e9ro-m\u00e9dial."),
    ("Comment les muscles papillaires sont-ils reli\u00e9s aux cuspides mitrales ?", "Par les cordages tendineux ; chaque pilier envoie des cordages aux deux cuspides."),
    ("La valve tricuspide est-elle une valve sigmo\u00efde ou atrio-ventriculaire ?", "C\u2019est une valve atrio-ventriculaire droite."),
    ("Combien de cuspides poss\u00e8de la valve tricuspide ?", "Trois cuspides : ant\u00e9rieure, septale et post\u00e9rieure."),
    ("Nommez les trois cuspides de la valve tricuspide.", "La cuspide ant\u00e9rieure, la cuspide septale et la cuspide post\u00e9rieure."),
    ("Combien de piliers musculaires poss\u00e8de le ventricule droit pour la valve tricuspide ?", "Trois piliers : ant\u00e9rieur, septal et post\u00e9rieur."),
    ("Quelle est la particularit\u00e9 du pilier ant\u00e9rieur de la valve tricuspide ?", "Il est \u00e0 l\u2019origine du trab\u00e9cule septo-marginal (bandelette ansiforme)."),
    ("Quelle est la forme de l\u2019anneau fibreux de la valve tricuspide ?", "Un anneau incomplet en forme de fer \u00e0 cheval, interrompu en post\u00e9ro-lat\u00e9ral."),
    ("Quel est le diam\u00e8tre moyen de l\u2019anneau tricuspide ?", "De 3 \u00e0 4 cm."),
    ("Quelle diff\u00e9rence d\u2019insertion existe entre la valve mitrale et la valve tricuspide ?", "Les cuspides de la valve tricuspide s\u2019ins\u00e8rent un peu plus en distal (vers la pointe) que celles de la valve mitrale."),
    ("Quel est le r\u00f4le de la valve tricuspide ?", "Emp\u00eacher le reflux du sang du ventricule droit vers l\u2019atrium droit pendant la systole ventriculaire."),
    ("Quand la valve tricuspide s\u2019ouvre-t-elle ?", "Pendant la diastole, pour permettre le remplissage du ventricule droit."),
    ("Quand la valve tricuspide se ferme-t-elle ?", "Pendant la systole ventriculaire."),
    ("Pourquoi l\u2019anneau tricuspide est-il dit \u00ab incomplet \u00bb ?", "Car il est interrompu au niveau de la portion post\u00e9ro-lat\u00e9rale o\u00f9 il n\u2019y a pas de tissu fibreux continu."),
    ("Quelles sont les deux cat\u00e9gories de valves cardiaques ?", "Les valves atrio-ventriculaires (mitrale et tricuspide) et les valves sigmo\u00efdes (aortique et pulmonaire)."),
    ("Quelles valves poss\u00e8dent un appareil sous-valvulaire (cordages + piliers) ?", "Les valves atrio-ventriculaires : la valve mitrale et la valve tricuspide."),
    ("Les valves sigmo\u00efdes poss\u00e8dent-elles des cordages tendineux ?", "Non, les valves sigmo\u00efdes (aortique et pulmonaire) n\u2019ont ni cordages ni piliers."),
    ("Comment appelle-t-on les feuillets des valves sigmo\u00efdes ?", "Des cuspides ou valvules semi-lunaires."),
    ("Quelle valve s\u00e9pare l\u2019atrium gauche du ventricule gauche ?", "La valve mitrale."),
    ("Quelle valve s\u00e9pare l\u2019atrium droit du ventricule droit ?", "La valve tricuspide."),
    ("Quelle valve s\u00e9pare le ventricule gauche de l\u2019aorte ?", "La valve aortique."),
    ("Quelle valve s\u00e9pare le ventricule droit du tronc pulmonaire ?", "La valve pulmonaire."),
    ("Quel segment de la cuspide ant\u00e9rieure mitrale est le plus proche de la commissure ant\u00e9ro-lat\u00e9rale ?", "Le segment A1."),
    ("Quel segment de la cuspide ant\u00e9rieure mitrale est central ?", "Le segment A2."),
    ("Quel segment de la cuspide ant\u00e9rieure mitrale est le plus proche de la commissure post\u00e9ro-m\u00e9diale ?", "Le segment A3."),
    ("Comment les segments P1, P2, P3 correspondent-ils aux segments A1, A2, A3 ?", "P1 fait face \u00e0 A1, P2 fait face \u00e0 A2 et P3 fait face \u00e0 A3 lors de la coaptation."),
    ("Qu\u2019est-ce que le prolapsus valvulaire mitral ?", "Le passage d\u2019une ou des deux cuspides au-del\u00e0 du plan de l\u2019anneau mitral dans l\u2019atrium gauche lors de la systole."),
    ("Quelle cons\u00e9quence fonctionnelle entra\u00eene une rupture de cordage mitral ?", "Une insuffisance mitrale par d\u00e9faut de coaptation (r\u00e9gurgitation de sang dans l\u2019atrium gauche)."),
    ("Quelles valves s\u2019ouvrent pendant la systole ventriculaire ?", "Les valves sigmo\u00efdes (aortique et pulmonaire)."),
    ("Quelles valves se ferment pendant la systole ventriculaire ?", "Les valves atrio-ventriculaires (mitrale et tricuspide)."),
    ("Quelles valves s\u2019ouvrent pendant la diastole ventriculaire ?", "Les valves atrio-ventriculaires (mitrale et tricuspide)."),
    ("Quelles valves se ferment pendant la diastole ventriculaire ?", "Les valves sigmo\u00efdes (aortique et pulmonaire)."),
    ("Quel bruit du c\u0153ur correspond \u00e0 la fermeture des valves AV (B1) ?", "Le premier bruit cardiaque (B1), produit par la fermeture des valves mitrale et tricuspide au d\u00e9but de la systole."),
    ("Quel bruit du c\u0153ur correspond \u00e0 la fermeture des valves sigmo\u00efdes (B2) ?", "Le deuxi\u00e8me bruit cardiaque (B2), produit par la fermeture des valves aortique et pulmonaire au d\u00e9but de la diastole."),
    ("Quel est le rapport entre le trigone fibreux et le faisceau de His ?", "Le faisceau de His traverse le trigone fibreux pour passer des atriums aux ventricules, c\u2019est le seul passage \u00e9lectrique."),
    ("Quelle cuspide de la valve aortique est dite \u00ab coronaire droite \u00bb ?", "La cuspide ant\u00e9rieure droite, car le sinus aortique situ\u00e9 derri\u00e8re elle donne naissance \u00e0 l\u2019art\u00e8re coronaire droite."),
    ("Quelle cuspide de la valve aortique est dite \u00ab coronaire gauche \u00bb ?", "La cuspide ant\u00e9rieure gauche, car le sinus aortique situ\u00e9 derri\u00e8re elle donne naissance \u00e0 l\u2019art\u00e8re coronaire gauche."),
    ("Quelle cuspide de la valve aortique est dite \u00ab non coronaire \u00bb ?", "La cuspide post\u00e9rieure, car aucune art\u00e8re coronaire ne na\u00eet du sinus correspondant."),
    ("\u00c0 quoi correspond un r\u00e9tr\u00e9cissement aortique ?", "\u00c0 une st\u00e9nose de la valve aortique limitant l\u2019ouverture des cuspides et g\u00eanant l\u2019\u00e9jection du ventricule gauche."),
    ("\u00c0 quoi correspond une insuffisance mitrale ?", "\u00c0 un d\u00e9faut de coaptation de la valve mitrale entra\u00eenant un reflux de sang du ventricule gauche vers l\u2019atrium gauche en systole."),
    ("Qu\u2019est-ce qu\u2019une endocardite ?", "Une infection de l\u2019endocarde, touchant souvent les valves cardiaques, pouvant provoquer des v\u00e9g\u00e9tations et des destructions valvulaires."),
    ("Quel est le r\u00f4le fonctionnel des muscles papillaires lors de la systole ?", "Ils se contractent en m\u00eame temps que le myocarde pour tendre les cordages et emp\u00eacher le prolapsus des cuspides AV."),
    ("Combien de commissures poss\u00e8de la valve mitrale ?", "Deux commissures : ant\u00e9ro-lat\u00e9rale et post\u00e9ro-m\u00e9diale."),
]

assert len(flashcards) == 100, f"Expected 100 flashcards, got {len(flashcards)}"

# Build JS array
lines = ["const flashcardsData = ["]
for q, a in flashcards:
    lines.append(f"{{ question: '{q}', answer: '{a}' }},")
lines.append("];")
new_data = "\n".join(lines)

# Read file
filepath = "/Users/cyrilwisa/Desktop/diploma/UPEC_LSPS1_S2/Circulation_Respiration/Anatomie/fc7.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace
content = re.sub(r'const flashcardsData\s*=\s*\[.*?\];', new_data, content, flags=re.DOTALL)

# Write
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"fc7.html updated with {len(flashcards)} flashcards")
