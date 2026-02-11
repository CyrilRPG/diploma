import re

flashcards = [
    ("Qu\u2019est-ce que le tissu cardionecteur ?", "Le tissu nodal, un tissu cardiaque sp\u00e9cialis\u00e9 qui donne naissance et conduit les impulsions \u00e9lectriques du c\u0153ur."),
    ("Quel est le r\u00f4le du tissu cardionecteur ?", "Provoquer la contraction myocardique par une d\u00e9polarisation automatique et rythmique, et coordonner les contractions des cavit\u00e9s."),
    ("Qu\u2019est-ce que la d\u00e9polarisation automatique rythmique ?", "La capacit\u00e9 du tissu nodal \u00e0 g\u00e9n\u00e9rer spontan\u00e9ment des potentiels d\u2019action sans stimulation externe."),
    ("Comment le tissu cardionecteur coordonne-t-il les contractions cardiaques ?", "Il assure la contraction s\u00e9quentielle : d\u2019abord les atriums qui remplissent les ventricules, puis les ventricules qui \u00e9jectent le sang."),
    ("Quelles sont les principales structures du tissu nodal ?", "Le n\u0153ud sino-atrial, le n\u0153ud atrio-ventriculaire, les voies internodales et le faisceau de His avec ses branches."),
    ("Qui a d\u00e9couvert le n\u0153ud sino-atrial ?", "Keith et Flack."),
    ("O\u00f9 est situ\u00e9 le n\u0153ud sino-atrial ?", "Dans la paroi post\u00e9rieure de l\u2019atrium droit, dans l\u2019\u00e9paisseur du sillon terminal."),
    ("Dans quelle cavit\u00e9 cardiaque se trouve le n\u0153ud sino-atrial ?", "Dans l\u2019atrium droit."),
    ("Quel est le rythme spontan\u00e9 de d\u00e9polarisation du n\u0153ud sino-atrial ?", "Environ 70 battements par minute."),
    ("Pourquoi le n\u0153ud sino-atrial impose-t-il le rythme cardiaque ?", "Parce que c\u2019est le centre dont la d\u00e9polarisation automatique est la plus rapide, il impose son rythme aux autres structures."),
    ("Quel autre nom donne-t-on au n\u0153ud sino-atrial ?", "Le pacemaker naturel du c\u0153ur (centre d\u2019automatisme primaire)."),
    ("Quelles connexions le n\u0153ud sino-atrial re\u00e7oit-il ?", "Les aff\u00e9rences du plexus cardiaque."),
    ("Par quoi le rythme du n\u0153ud sino-atrial est-il modul\u00e9 ?", "Par le syst\u00e8me nerveux sympathique et le syst\u00e8me nerveux parasympathique."),
    ("Quel est l\u2019effet du sympathique sur le n\u0153ud sino-atrial ?", "Il acc\u00e9l\u00e8re la fr\u00e9quence cardiaque (effet chronotrope positif)."),
    ("Quel est l\u2019effet du parasympathique sur le n\u0153ud sino-atrial ?", "Il ralentit la fr\u00e9quence cardiaque (effet chronotrope n\u00e9gatif)."),
    ("Quels facteurs modulent l\u2019activit\u00e9 du syst\u00e8me sympathique et parasympathique sur le c\u0153ur ?", "La douleur, l\u2019\u00e9motion, l\u2019activit\u00e9 physique et le stress."),
    ("Qu\u2019est-ce que le plexus cardiaque ?", "Un r\u00e9seau de fibres nerveuses sympathiques et parasympathiques qui innerve le c\u0153ur et module son activit\u00e9."),
    ("Qui a d\u00e9couvert le n\u0153ud atrio-ventriculaire ?", "Aschoff et Tawara."),
    ("O\u00f9 est situ\u00e9 le n\u0153ud atrio-ventriculaire ?", "Dans le septum inter-atrial, \u00e0 proximit\u00e9 de la cuspide septale de la valve mitrale et de l\u2019orifice du sinus coronaire."),
    ("Dans quel triangle anatomique se trouve le n\u0153ud AV ?", "Dans le triangle de Koch."),
    ("Qu\u2019est-ce que le triangle de Koch ?", "Un rep\u00e8re anatomique d\u00e9limit\u00e9 par le tendon de Todaro, l\u2019anneau tricuspide (cuspide septale) et l\u2019orifice du sinus coronaire, contenant le n\u0153ud AV."),
    ("Quel est le rythme spontan\u00e9 de d\u00e9polarisation du n\u0153ud atrio-ventriculaire ?", "Environ 30 battements par minute."),
    ("Pourquoi le n\u0153ud AV est-il un centre d\u2019automatisme secondaire ?", "Car son rythme propre (30/min) est plus lent que celui du n\u0153ud sino-atrial (70/min) ; il ne s\u2019exprime que si le n\u0153ud SA d\u00e9faille."),
    ("Quel est le r\u00f4le du n\u0153ud AV dans la conduction ?", "Il re\u00e7oit la d\u00e9polarisation atriale et la transmet aux ventricules via le faisceau de His, avec un l\u00e9ger retard."),
    ("Pourquoi le d\u00e9lai de conduction au n\u0153ud AV est-il important ?", "Il permet aux atriums de finir leur contraction et de remplir compl\u00e8tement les ventricules avant la systole ventriculaire."),
    ("Combien de voies de conduction internodales relient le n\u0153ud SA au n\u0153ud AV ?", "Trois voies : ant\u00e9rieure, moyenne et post\u00e9rieure."),
    ("Quel est le trajet de la voie internodale ant\u00e9rieure ?", "Elle passe lat\u00e9ralement \u00e0 l\u2019orifice de la veine cave sup\u00e9rieure, traverse le toit de l\u2019atrium droit, puis descend dans le septum inter-atrial vers le n\u0153ud AV."),
    ("Par o\u00f9 passe la voie internodale ant\u00e9rieure par rapport \u00e0 la VCS ?", "Lat\u00e9ralement \u00e0 l\u2019orifice de la veine cave sup\u00e9rieure."),
    ("Quel est le trajet de la voie internodale moyenne ?", "Elle passe en arri\u00e8re de la veine cave sup\u00e9rieure, traverse la partie moyenne du septum inter-atrial au-dessus de la fosse ovale, et rejoint le n\u0153ud AV."),
    ("Quel est le rapport de la voie internodale moyenne avec la fosse ovale ?", "Elle passe au-dessus de la fosse ovale dans le septum inter-atrial."),
    ("Quel est le trajet de la voie internodale post\u00e9rieure ?", "Elle suit le sillon terminal et rejoint le n\u0153ud AV."),
    ("Quelle structure anatomique la voie internodale post\u00e9rieure longe-t-elle ?", "Le sillon terminal."),
    ("Quel est le r\u00f4le des voies internodales ?", "Conduire l\u2019onde de d\u00e9polarisation du n\u0153ud sino-atrial au n\u0153ud atrio-ventriculaire \u00e0 travers l\u2019atrium droit."),
    ("O\u00f9 na\u00eet la contraction atriale ?", "Au n\u0153ud sino-atrial, puis elle se propage par les voies internodales et la paroi atriale."),
    ("Qu\u2019est-ce que le faisceau de His ?", "Le faisceau atrio-ventriculaire qui propage l\u2019onde de d\u00e9polarisation des atriums vers les ventricules."),
    ("Quel est le trajet du tronc du faisceau de His ?", "Il se dirige en avant, longe le bord inf\u00e9rieur du septum membraneux interventriculaire, puis atteint le sommet du septum intermusculaire."),
    ("Quel rapport le faisceau de His a-t-il avec le septum membraneux ?", "Il longe le bord inf\u00e9rieur du septum membraneux interventriculaire."),
    ("Le faisceau de His est-il la seule connexion \u00e9lectrique entre atriums et ventricules ?", "Oui, c\u2019est la seule voie de conduction physiologique traversant la charpente fibreuse."),
    ("En combien de branches le faisceau de His se divise-t-il ?", "En deux branches : une branche droite et une branche gauche."),
    ("Quel est le trajet de la branche droite du faisceau de His ?", "Elle s\u2019incline vers le bas, p\u00e9n\u00e8tre le trab\u00e9cule septo-marginal et se termine au muscle papillaire ant\u00e9rieur de la valve tricuspide."),
    ("Quelle structure le faisceau de His emprunte-t-il pour atteindre le ventricule droit ?", "Le trab\u00e9cule septo-marginal (bandelette ansiforme)."),
    ("O\u00f9 se termine la branche droite du faisceau de His ?", "Au muscle papillaire ant\u00e9rieur de la valve tricuspide."),
    ("Combien de muscles papillaires la branche droite innerve-t-elle ?", "Les trois muscles papillaires du ventricule droit (ant\u00e9rieur, septal et post\u00e9rieur)."),
    ("Quel est le trajet de la branche gauche du faisceau de His ?", "Elle passe en avant du septum membraneux et se dirige vers les muscles papillaires ant\u00e9rieur et post\u00e9rieur du ventricule gauche."),
    ("Par o\u00f9 passe la branche gauche par rapport au septum membraneux ?", "En avant du septum membraneux."),
    ("Vers quels muscles papillaires la branche gauche se dirige-t-elle ?", "Vers les muscles papillaires ant\u00e9rieur et post\u00e9rieur du ventricule gauche."),
    ("Qu\u2019est-ce que le r\u00e9seau de Purkinje ?", "Les ramifications terminales des branches du faisceau de His qui se distribuent dans la paroi des ventricules pour assurer une d\u00e9polarisation homog\u00e8ne."),
    ("Quel est l\u2019ordre de d\u00e9polarisation du c\u0153ur ?", "N\u0153ud SA \u2192 atriums (voies internodales) \u2192 n\u0153ud AV \u2192 faisceau de His \u2192 branches droite et gauche \u2192 r\u00e9seau de Purkinje \u2192 ventricules."),
    ("Quelle art\u00e8re vascularise le n\u0153ud atrio-ventriculaire ?", "Le tronc r\u00e9troventriculaire gauche (branche terminale de la coronaire droite)."),
    ("D\u2019o\u00f9 provient le tronc r\u00e9troventriculaire gauche ?", "C\u2019est une branche terminale de l\u2019art\u00e8re coronaire droite."),
    ("Quelles art\u00e8res vascularisent les branches du faisceau de His ?", "Les art\u00e8res septales, en particulier la deuxi\u00e8me art\u00e8re septale."),
    ("Quelle art\u00e8re septale est la plus importante pour le faisceau de His ?", "La deuxi\u00e8me art\u00e8re septale, qui est souvent la plus volumineuse."),
    ("D\u2019o\u00f9 naissent les art\u00e8res septales ?", "De l\u2019art\u00e8re interventriculaire ant\u00e9rieure (IVA), branche de la coronaire gauche."),
    ("Pourquoi la vascularisation du tissu de conduction est-elle cliniquement importante ?", "Car une isch\u00e9mie de ces art\u00e8res peut provoquer des troubles de la conduction (blocs cardiaques)."),
    ("Qu\u2019est-ce qu\u2019un bloc sino-atrial ?", "Un trouble de la conduction o\u00f9 l\u2019influx du n\u0153ud SA ne se propage pas correctement aux atriums."),
    ("Qu\u2019est-ce qu\u2019un bloc atrio-ventriculaire ?", "Un trouble de la conduction o\u00f9 la transmission de l\u2019influx du n\u0153ud AV aux ventricules est ralentie ou interrompue."),
    ("Quels sont les trois degr\u00e9s de bloc atrio-ventriculaire ?", "BAV 1er degr\u00e9 (allongement PR), 2\u1d49 degr\u00e9 (conduction intermittente) et 3\u1d49 degr\u00e9 (dissociation compl\u00e8te atrio-ventriculaire)."),
    ("Que se passe-t-il en cas de BAV complet (3\u1d49 degr\u00e9) ?", "Aucun influx atrial n\u2019est transmis aux ventricules ; les ventricules battent \u00e0 leur rythme propre (30/min via n\u0153ud AV ou plus lent)."),
    ("Qu\u2019est-ce que le rythme d\u2019\u00e9chappement jonctionnel ?", "Un rythme de secours g\u00e9n\u00e9r\u00e9 par le n\u0153ud AV ou le faisceau de His lorsque le n\u0153ud SA d\u00e9faille, \u00e0 environ 30-40/min."),
    ("Qu\u2019est-ce que le sillon terminal ?", "Un sillon sur la face externe de l\u2019atrium droit, rep\u00e8re du n\u0153ud sino-atrial et de la voie internodale post\u00e9rieure."),
    ("Quel est le rapport entre la fosse ovale et le syst\u00e8me de conduction ?", "La voie internodale moyenne passe au-dessus de la fosse ovale dans le septum inter-atrial."),
    ("Quel est le rapport entre la cuspide septale de la valve mitrale et le n\u0153ud AV ?", "Le n\u0153ud AV est situ\u00e9 \u00e0 proximit\u00e9 de la cuspide septale de la valve mitrale."),
    ("Quel est le rapport entre le sinus coronaire et le n\u0153ud AV ?", "Le n\u0153ud AV est situ\u00e9 \u00e0 proximit\u00e9 de l\u2019orifice du sinus coronaire, formant un sommet du triangle de Koch."),
    ("Qu\u2019est-ce que le trab\u00e9cule septo-marginal ?", "Une band\u00e9e musculaire traversant le ventricule droit du septum \u00e0 la paroi libre, contenant la branche droite du faisceau de His."),
    ("Quel est le r\u00f4le du trab\u00e9cule septo-marginal dans la conduction ?", "Il transporte la branche droite du faisceau de His vers le muscle papillaire ant\u00e9rieur du ventricule droit."),
    ("Pourquoi dit-on que le n\u0153ud SA est le centre d\u2019automatisme le plus rapide ?", "Car sa fr\u00e9quence intrins\u00e8que (70/min) est sup\u00e9rieure \u00e0 celle du n\u0153ud AV (30/min) et du faisceau de His (20/min)."),
    ("Quelle est la fr\u00e9quence intrins\u00e8que approximative du faisceau de His ?", "Environ 20 battements par minute."),
    ("Quel est le m\u00e9canisme de la hi\u00e9rarchie des centres d\u2019automatisme ?", "Le centre le plus rapide supprime l\u2019automatisme des centres plus lents par un m\u00e9canisme d\u2019overdrive suppression."),
    ("Qu\u2019est-ce que l\u2019overdrive suppression ?", "Le ph\u00e9nom\u00e8ne par lequel un centre d\u2019automatisme rapide emp\u00eache les centres plus lents de s\u2019exprimer en les d\u00e9polarisant avant qu\u2019ils n\u2019atteignent leur seuil."),
    ("Quel nerf transporte les fibres parasympathiques vers le c\u0153ur ?", "Le nerf vague (X\u1d49 paire cr\u00e2nienne)."),
    ("Quelles fibres sympathiques innervent le c\u0153ur ?", "Les fibres post-ganglionnaires issues des ganglions cervicaux et thoraciques sup\u00e9rieurs de la cha\u00eene sympathique."),
    ("Qu\u2019est-ce que l\u2019effet chronotrope ?", "L\u2019effet sur la fr\u00e9quence cardiaque : positif (acc\u00e9l\u00e9ration) ou n\u00e9gatif (ralentissement)."),
    ("Qu\u2019est-ce que l\u2019effet dromotrope ?", "L\u2019effet sur la vitesse de conduction dans le tissu nodal : positif (acc\u00e9l\u00e9ration) ou n\u00e9gatif (ralentissement)."),
    ("Qu\u2019est-ce que l\u2019effet bathmotrope ?", "L\u2019effet sur l\u2019excitabilit\u00e9 du myocarde : positif (augmentation) ou n\u00e9gatif (diminution)."),
    ("Le sympathique a-t-il un effet chronotrope positif ou n\u00e9gatif ?", "Positif : il acc\u00e9l\u00e8re la fr\u00e9quence cardiaque."),
    ("Le parasympathique a-t-il un effet chronotrope positif ou n\u00e9gatif ?", "N\u00e9gatif : il ralentit la fr\u00e9quence cardiaque."),
    ("Le sympathique a-t-il un effet dromotrope positif ou n\u00e9gatif ?", "Positif : il acc\u00e9l\u00e8re la conduction dans le tissu nodal."),
    ("Le parasympathique a-t-il un effet dromotrope positif ou n\u00e9gatif ?", "N\u00e9gatif : il ralentit la conduction, notamment au n\u0153ud AV."),
    ("Qu\u2019est-ce qu\u2019un pacemaker artificiel ?", "Un dispositif \u00e9lectronique implant\u00e9 qui g\u00e9n\u00e8re des impulsions \u00e9lectriques pour stimuler le c\u0153ur lorsque le syst\u00e8me de conduction est d\u00e9faillant."),
    ("Dans quelle situation implante-t-on un pacemaker ?", "En cas de bradycardie symptomatique ou de bloc atrio-ventriculaire de haut degr\u00e9 ne r\u00e9pondant pas au traitement m\u00e9dical."),
    ("Quel est le rapport entre le septum membraneux et le faisceau de His ?", "Le faisceau de His longe le bord inf\u00e9rieur du septum membraneux interventriculaire, zona fragile en chirurgie."),
    ("Pourquoi le faisceau de His est-il vuln\u00e9rable lors de la chirurgie cardiaque ?", "Car il chemine dans une zone anatomique exigu\u00eb pr\u00e8s du septum membraneux et peut \u00eatre l\u00e9s\u00e9 lors d\u2019interventions valvulaires."),
    ("Qu\u2019est-ce que le sommet du septum intermusculaire ?", "La jonction entre le septum membraneux et le septum musculaire interventriculaire, o\u00f9 le faisceau de His se divise."),
    ("Quelle est la cons\u00e9quence d\u2019une l\u00e9sion de la branche droite du faisceau de His ?", "Un bloc de branche droit, avec retard d\u2019activation du ventricule droit visible sur l\u2019ECG."),
    ("Quelle est la cons\u00e9quence d\u2019une l\u00e9sion de la branche gauche du faisceau de His ?", "Un bloc de branche gauche, avec retard d\u2019activation du ventricule gauche visible sur l\u2019ECG."),
    ("Quel rep\u00e8re anatomique d\u00e9limite le triangle de Koch en bas ?", "L\u2019anneau tricuspide au niveau de la cuspide septale."),
    ("Quel rep\u00e8re anatomique d\u00e9limite le triangle de Koch en haut et en arri\u00e8re ?", "Le tendon de Todaro."),
    ("Quel rep\u00e8re anatomique d\u00e9limite le triangle de Koch en bas et en arri\u00e8re ?", "L\u2019orifice du sinus coronaire."),
    ("Quel est l\u2019int\u00e9r\u00eat clinique du triangle de Koch ?", "C\u2019est le rep\u00e8re chirurgical pour localiser le n\u0153ud AV et \u00e9viter de le l\u00e9ser lors des interventions."),
    ("Qu\u2019est-ce qu\u2019un rythme sinusal normal ?", "Un rythme cardiaque dont l\u2019origine est le n\u0153ud sino-atrial, avec une fr\u00e9quence de 60 \u00e0 100/min chez l\u2019adulte au repos."),
    ("Que se passe-t-il si le n\u0153ud sino-atrial cesse de fonctionner ?", "Le n\u0153ud AV prend le relais comme pacemaker, imposant un rythme d\u2019environ 30-40/min (rythme d\u2019\u00e9chappement jonctionnel)."),
    ("Quelle veine cave est en rapport \u00e9troit avec le n\u0153ud SA et les voies internodales ?", "La veine cave sup\u00e9rieure."),
    ("Quel est le rapport entre les voies internodales ant\u00e9rieure et moyenne avec la VCS ?", "La voie ant\u00e9rieure passe lat\u00e9ralement \u00e0 la VCS, la voie moyenne passe en arri\u00e8re de la VCS."),
    ("Quelle est la particularit\u00e9 fonctionnelle des cellules du tissu nodal par rapport aux cardiomyocytes contractiles ?", "Les cellules nodales ont une d\u00e9polarisation diastolique lente spontan\u00e9e (automatisme) alors que les cardiomyocytes ont un potentiel de repos stable."),
    ("Par quelle art\u00e8re le n\u0153ud sino-atrial est-il principalement vascularis\u00e9 ?", "L\u2019art\u00e8re atriale droite sup\u00e9rieure (branche de la coronaire droite, ou parfois de la circonflexe)."),
    ("Quelle cons\u00e9quence clinique entra\u00eene une isch\u00e9mie de l\u2019art\u00e8re du n\u0153ud SA ?", "Une dysfonction sinusale (maladie du sinus) avec bradycardie ou pauses sinusales."),
    ("Quelle cons\u00e9quence clinique entra\u00eene une isch\u00e9mie du tronc r\u00e9troventriculaire gauche ?", "Un bloc atrio-ventriculaire par atteinte de la vascularisation du n\u0153ud AV."),
    ("Comment le septum membraneux se situe-t-il par rapport au faisceau de His ?", "Le faisceau de His longe son bord inf\u00e9rieur, ce qui en fait une zone \u00e0 risque lors des interventions sur le septum."),
    ("Quel est le neurotransmetteur du syst\u00e8me parasympathique agissant sur le c\u0153ur ?", "L\u2019ac\u00e9tylcholine, agissant sur les r\u00e9cepteurs muscariniques M2."),
    ("Quel est le neurotransmetteur du syst\u00e8me sympathique agissant sur le c\u0153ur ?", "La noradr\u00e9naline (et l\u2019adr\u00e9naline circulante), agissant sur les r\u00e9cepteurs b\u00eata-1 adr\u00e9nergiques."),
]

assert len(flashcards) == 100, f"Expected 100 flashcards, got {len(flashcards)}"

# Build JS array
lines = ["const flashcardsData = ["]
for q, a in flashcards:
    lines.append(f"{{ question: '{q}', answer: '{a}' }},")
lines.append("];")
new_data = "\n".join(lines)

# Read file
filepath = "/Users/cyrilwisa/Desktop/diploma/UPEC_LSPS1_S2/Circulation_Respiration/Anatomie/fc6.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace
content = re.sub(r'const flashcardsData\s*=\s*\[.*?\];', new_data, content, flags=re.DOTALL)

# Write
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"fc6.html updated with {len(flashcards)} flashcards")
