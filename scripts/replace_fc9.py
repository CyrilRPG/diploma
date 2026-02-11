import re

flashcards = [
    ("Quelles sont les deux grandes consid\u00e9rations motivant le d\u00e9veloppement d\u2019un nouveau m\u00e9dicament ?", "Une consid\u00e9ration m\u00e9dicale (progr\u00e8s th\u00e9rapeutique) et une consid\u00e9ration \u00e9conomique (rentabilit\u00e9, march\u00e9)."),
    ("Que recouvre la consid\u00e9ration m\u00e9dicale dans le d\u00e9veloppement d\u2019un m\u00e9dicament ?", "Le progr\u00e8s th\u00e9rapeutique : absence de strat\u00e9gie pharmacologique, traitements insuffisamment efficaces, am\u00e9lioration des traitements existants."),
    ("Que recouvre la consid\u00e9ration \u00e9conomique dans le d\u00e9veloppement d\u2019un m\u00e9dicament ?", "La rentabilit\u00e9 pour l\u2019industrie pharmaceutique, l\u2019importance du march\u00e9 et la concurrence."),
    ("Quels motifs m\u00e9dicaux justifient la cr\u00e9ation d\u2019un nouveau m\u00e9dicament ?", "L\u2019absence de strat\u00e9gie pharmacologique, les traitements insuffisamment efficaces et l\u2019am\u00e9lioration des traitements existants."),
    ("Quels objectifs d\u2019am\u00e9lioration peut-on viser lors du d\u00e9veloppement d\u2019un m\u00e9dicament ?", "Augmenter l\u2019efficacit\u00e9, r\u00e9duire les effets ind\u00e9sirables, \u00e9viter certaines interactions m\u00e9dicamenteuses, am\u00e9liorer la biodisponibilit\u00e9."),
    ("Qu\u2019est-ce qu\u2019un analogue de m\u00e9dicament connu ou \u00ab me-too drug \u00bb ?", "Un m\u00e9dicament inspir\u00e9 d\u2019une classe th\u00e9rapeutique existante, modifi\u00e9 chimiquement pour \u00eatre brevetable."),
    ("Quel est l\u2019objectif principal des analogues de m\u00e9dicaments (me-too drugs) ?", "Am\u00e9liorer la s\u00e9lectivit\u00e9, r\u00e9duire les effets secondaires, augmenter la biodisponibilit\u00e9 ou \u00e9viter les interactions."),
    ("Sur quel principe repose la conception d\u2019un analogue ?", "Sur la relation structure-activit\u00e9 d\u2019une classe de m\u00e9dicaments d\u00e9j\u00e0 connue."),
    ("Qu\u2019est-ce que la relation structure-activit\u00e9 ?", "Le lien entre la structure chimique d\u2019une mol\u00e9cule et son activit\u00e9 pharmacologique, permettant d\u2019optimiser de nouveaux compos\u00e9s."),
    ("Pourquoi un analogue doit-il \u00eatre brevetable ?", "Pour garantir la propri\u00e9t\u00e9 intellectuelle et la rentabilit\u00e9 de l\u2019investissement en recherche et d\u00e9veloppement."),
    ("Pourquoi les industriels d\u00e9veloppent-ils de nombreux me-too drugs ?", "Pour obtenir des parts de march\u00e9 importantes, surtout pour les traitements chroniques \u00e0 forte consommation."),
    ("Donnez un exemple de classe de m\u00e9dicaments ayant g\u00e9n\u00e9r\u00e9 de nombreux analogues.", "Les statines, inhibiteurs de l\u2019HMG-CoA r\u00e9ductase."),
    ("Quelle est la cible pharmacologique des statines ?", "L\u2019enzyme HMG-CoA r\u00e9ductase, cl\u00e9 de la synth\u00e8se du cholest\u00e9rol."),
    ("Donnez un exemple d\u2019analogue parmi les antagonistes des r\u00e9cepteurs AT1 de l\u2019angiotensine II.", "Le telmisartan, analogue du losartan."),
    ("Quel est le chef de file des antagonistes des r\u00e9cepteurs AT1 ?", "Le losartan."),
    ("Quelle est la cible des antagonistes AT1 (sartans) ?", "Les r\u00e9cepteurs AT1 de l\u2019angiotensine II, impliqu\u00e9s dans la vasoconstriction."),
    ("Comment la p\u00e9nicilline a-t-elle \u00e9t\u00e9 d\u00e9couverte ?", "Par hasard, en 1928, par Alexander Fleming qui a observ\u00e9 qu\u2019un champignon inhibait la croissance bact\u00e9rienne."),
    ("Qui a d\u00e9couvert la p\u00e9nicilline et en quelle ann\u00e9e ?", "Alexander Fleming en 1928."),
    ("Quel champignon est \u00e0 l\u2019origine de la p\u00e9nicilline ?", "Penicillium notatum."),
    ("Quelle bact\u00e9rie \u00e9tait cultiv\u00e9e sur la bo\u00eete de P\u00e9tri de Fleming lors de la d\u00e9couverte de la p\u00e9nicilline ?", "Staphylococcus aureus."),
    ("Qu\u2019a observ\u00e9 Fleming sur sa bo\u00eete de P\u00e9tri contamin\u00e9e ?", "Une zone d\u2019inhibition de la croissance de S. aureus autour de la colonie de Penicillium notatum."),
    ("Quel est le principe g\u00e9n\u00e9ral de la d\u00e9couverte fortuite de m\u00e9dicaments ?", "Un \u00e9v\u00e9nement ou une observation inattendue d\u00e9clenche la recherche d\u2019une nouvelle mol\u00e9cule active."),
    ("Qu\u2019est-ce que l\u2019exploitation des effets ind\u00e9sirables d\u2019un m\u00e9dicament ?", "Utiliser un effet secondaire observ\u00e9 comme nouvelle indication th\u00e9rapeutique."),
    ("Quelle \u00e9tait l\u2019indication initiale du minoxidil ?", "Antihypertenseur."),
    ("Quel effet ind\u00e9sirable du minoxidil a \u00e9t\u00e9 exploit\u00e9 ?", "L\u2019hypertrichose (pousse excessive des poils)."),
    ("Quelle nouvelle indication th\u00e9rapeutique a \u00e9t\u00e9 d\u00e9velopp\u00e9e \u00e0 partir de l\u2019hypertrichose du minoxidil ?", "Le traitement de la calvitie (alopécie)."),
    ("D\u00e9crivez le parcours du minoxidil de l\u2019indication initiale \u00e0 la nouvelle indication.", "Antihypertenseur \u2192 effet ind\u00e9sirable d\u2019hypertrichose \u2192 exploitation pour traiter la calvitie."),
    ("Qui a d\u00e9couvert les propri\u00e9t\u00e9s hypoglyc\u00e9miantes des sulfamides ?", "Marcel Jambon en 1942."),
    ("En quelle ann\u00e9e Marcel Jambon a-t-il observ\u00e9 les effets hypoglyc\u00e9miants des sulfamides ?", "En 1942."),
    ("Quelle \u00e9tait l\u2019indication initiale des sulfamides avant la d\u00e9couverte de leur effet hypoglyc\u00e9miant ?", "Antibact\u00e9riens (sulfamides antibact\u00e9riens)."),
    ("Quel effet ind\u00e9sirable des sulfamides antibact\u00e9riens a \u00e9t\u00e9 exploit\u00e9 ?", "L\u2019hypoglyc\u00e9mie."),
    ("Quelle classe de m\u00e9dicaments est n\u00e9e de l\u2019exploitation des effets hypoglyc\u00e9miants des sulfamides ?", "Les antidiab\u00e9tiques de type sulfamides hypoglyc\u00e9miants (sulfonylur\u00e9es)."),
    ("D\u00e9crivez le parcours des sulfamides de l\u2019indication initiale \u00e0 la nouvelle.", "Sulfamides antibact\u00e9riens \u2192 observation d\u2019hypoglyc\u00e9mies \u2192 d\u00e9veloppement d\u2019antidiab\u00e9tiques sulfamides."),
    ("Qu\u2019est-ce que la d\u00e9couverte d\u2019une nouvelle propri\u00e9t\u00e9 d\u2019un m\u00e9dicament existant ?", "Apr\u00e8s la commercialisation, on d\u00e9couvre une propri\u00e9t\u00e9 pharmacologique in\u00e9dite exploitable dans une autre pathologie."),
    ("Quelle \u00e9tait l\u2019indication initiale de la ciclosporine ?", "Immunosuppresseur utilis\u00e9 en pr\u00e9vention du rejet de greffe d\u2019organe."),
    ("Quelle nouvelle propri\u00e9t\u00e9 de la ciclosporine a \u00e9t\u00e9 d\u00e9couverte apr\u00e8s sa commercialisation ?", "Sa capacit\u00e9 \u00e0 moduler la mort cellulaire, r\u00e9duisant les l\u00e9sions tissulaires."),
    ("Dans quelles situations la propri\u00e9t\u00e9 de modulation de la mort cellulaire de la ciclosporine est-elle int\u00e9ressante ?", "Dans l\u2019infarctus du myocarde et l\u2019arr\u00eat cardiaque, pour limiter les l\u00e9sions tissulaires."),
    ("D\u00e9crivez le parcours de la ciclosporine de l\u2019indication initiale aux nouvelles propri\u00e9t\u00e9s.", "Immunosuppresseur pour greffe \u2192 d\u00e9couverte de la modulation de la mort cellulaire \u2192 potentiel dans l\u2019infarctus et l\u2019arr\u00eat cardiaque."),
    ("Pourquoi continue-t-on la recherche apr\u00e8s l\u2019AMM d\u2019un m\u00e9dicament ?", "Pour surveiller la pharmacovigilance, d\u00e9couvrir de nouvelles propri\u00e9t\u00e9s, de nouvelles indications ou de nouvelles cibles."),
    ("Qu\u2019est-ce que l\u2019exploitation de la non-s\u00e9lectivit\u00e9 d\u2019un m\u00e9dicament ?", "Utiliser une propri\u00e9t\u00e9 pharmacologique d\u2019un m\u00e9dicament dans une pathologie diff\u00e9rente de l\u2019indication initiale."),
    ("Quelle \u00e9tait l\u2019indication initiale des IEC ?", "Le traitement de l\u2019hypertension art\u00e9rielle (HTA)."),
    ("Quelle nouvelle indication a \u00e9t\u00e9 d\u00e9couverte pour les IEC gr\u00e2ce \u00e0 la non-s\u00e9lectivit\u00e9 ?", "Le traitement de l\u2019insuffisance cardiaque."),
    ("Donnez l\u2019exemple de parcours des IEC de l\u2019HTA \u00e0 l\u2019insuffisance cardiaque.", "IEC initialement pour l\u2019HTA \u2192 propri\u00e9t\u00e9s b\u00e9n\u00e9fiques d\u00e9couvertes dans l\u2019insuffisance cardiaque \u2192 nouvelle indication."),
    ("Quelle \u00e9tait l\u2019indication initiale des inhibiteurs de la PDE5 (sild\u00e9nafil) ?", "Le traitement de l\u2019insuffisance \u00e9rectile."),
    ("Quelle nouvelle indication a \u00e9t\u00e9 d\u00e9couverte pour les inhibiteurs de la PDE5 ?", "Le traitement de l\u2019hypertension art\u00e9rielle pulmonaire (HTAP)."),
    ("Quelle autre application potentielle des inhibiteurs de la PDE5 est \u00e0 l\u2019\u00e9tude ?", "La myopathie de Duchenne."),
    ("D\u00e9crivez le parcours du sild\u00e9nafil (inhibiteur PDE5) \u00e0 travers ses diff\u00e9rentes indications.", "Insuffisance \u00e9rectile \u2192 HTAP \u2192 potentiel dans la myopathie de Duchenne."),
    ("Pourquoi l\u2019inhibition d\u2019une m\u00eame enzyme peut-elle \u00eatre utile dans diff\u00e9rentes pathologies ?", "Parce que certaines cibles enzymatiques sont ubiquitaires et impliqu\u00e9es dans plusieurs processus physiologiques."),
    ("Qu\u2019est-ce que la conception fond\u00e9e sur la connaissance de processus biologiques ?", "Identifier un processus biologique impliqu\u00e9 dans une pathologie, puis concevoir une mol\u00e9cule ciblant une \u00e9tape cl\u00e9 de ce processus."),
    ("Quel est le principe de la conception rationnelle d\u2019un m\u00e9dicament ?", "Conna\u00eetre la cible pharmacologique et les m\u00e9canismes biologiques pour concevoir une mol\u00e9cule adapt\u00e9e."),
    ("Quel processus biologique a \u00e9t\u00e9 cibl\u00e9 pour d\u00e9velopper les premiers IEC ?", "Le syst\u00e8me r\u00e9nine-angiotensine, plus pr\u00e9cis\u00e9ment la conversion de l\u2019angiotensine I en angiotensine II."),
    ("Quel est le r\u00f4le de l\u2019angiotensine II dans la r\u00e9gulation vasculaire ?", "C\u2019est un puissant vasoconstricteur qui augmente la pression art\u00e9rielle."),
    ("Quel \u00e9tait l\u2019objectif du d\u00e9veloppement des premiers IEC ?", "R\u00e9duire l\u2019action vasoconstrictrice de l\u2019angiotensine II pour traiter l\u2019hypertension art\u00e9rielle."),
    ("Quelles sont les deux strat\u00e9gies possibles pour emp\u00eacher la vasoconstriction li\u00e9e \u00e0 l\u2019angiotensine II ?", "Inhiber la synth\u00e8se de l\u2019angiotensine II (IEC) ou antagoniser ses r\u00e9cepteurs (sartans/ARA II)."),
    ("Qu\u2019est-ce qu\u2019un IEC ?", "Un inhibiteur de l\u2019enzyme de conversion de l\u2019angiotensine, qui bloque la transformation de l\u2019angiotensine I en angiotensine II."),
    ("Qu\u2019est-ce qu\u2019un ARA II (sartan) ?", "Un antagoniste des r\u00e9cepteurs AT1 de l\u2019angiotensine II, qui bloque l\u2019action de l\u2019angiotensine II sur ses r\u00e9cepteurs."),
    ("Quelle d\u00e9couverte a permis de d\u00e9velopper les premiers IEC ?", "L\u2019observation qu\u2019un venin de serpent inhibait l\u2019enzyme de conversion de l\u2019angiotensine."),
    ("De quel animal provient le venin ayant inspir\u00e9 les IEC ?", "Du serpent (Bothrops jararaca, vip\u00e8re br\u00e9silienne)."),
    ("Comment le venin de serpent a-t-il conduit au d\u00e9veloppement des IEC ?", "Le venin contenait un peptide inhibant l\u2019enzyme de conversion, ce qui a inspir\u00e9 la synth\u00e8se de mol\u00e9cules analogues."),
    ("Quelle est la diff\u00e9rence entre la strat\u00e9gie IEC et la strat\u00e9gie sartan ?", "L\u2019IEC inhibe l\u2019enzyme qui produit l\u2019angiotensine II, le sartan bloque le r\u00e9cepteur AT1 sur lequel l\u2019angiotensine II agit."),
    ("Quelles sont les principales m\u00e9thodes d\u2019identification d\u2019un m\u00e9dicament ?", "Les analogues (me-too drugs), le hasard, l\u2019exploitation des effets ind\u00e9sirables, la d\u00e9couverte de nouvelles propri\u00e9t\u00e9s, la non-s\u00e9lectivit\u00e9, et la conception rationnelle."),
    ("Citez les six grandes approches de conception et d\u2019identification d\u2019un m\u00e9dicament.", "1) Analogues, 2) Hasard, 3) Exploitation des effets ind\u00e9sirables, 4) Nouvelle propri\u00e9t\u00e9 d\u2019un m\u00e9dicament existant, 5) Non-s\u00e9lectivit\u00e9, 6) Conception fond\u00e9e sur un processus biologique."),
    ("Qu\u2019est-ce que le criblage pharmacologique (screening) ?", "La m\u00e9thode syst\u00e9matique de test d\u2019un grand nombre de mol\u00e9cules sur une cible biologique pour identifier des candidats m\u00e9dicaments."),
    ("Quelle diff\u00e9rence y a-t-il entre une d\u00e9couverte par hasard et une conception rationnelle ?", "Le hasard repose sur une observation impr\u00e9vue, la conception rationnelle part d\u2019une connaissance pr\u00e9alable du m\u00e9canisme physiopathologique."),
    ("Qu\u2019est-ce qu\u2019un chef de file pharmacologique ?", "La premi\u00e8re mol\u00e9cule d\u2019une classe th\u00e9rapeutique servant de r\u00e9f\u00e9rence pour le d\u00e9veloppement d\u2019analogues."),
    ("Pourquoi d\u00e9veloppe-t-on des analogues plut\u00f4t que de rester sur le chef de file ?", "Pour am\u00e9liorer la s\u00e9lectivit\u00e9, r\u00e9duire les effets secondaires, optimiser la pharmacocin\u00e9tique et contourner les brevets."),
    ("Qu\u2019est-ce que la biodisponibilit\u00e9 d\u2019un m\u00e9dicament ?", "La fraction de la dose administr\u00e9e qui atteint la circulation syst\u00e9mique sous forme inchang\u00e9e."),
    ("Pourquoi cherche-t-on \u00e0 am\u00e9liorer la biodisponibilit\u00e9 d\u2019un analogue ?", "Pour augmenter la quantit\u00e9 de principe actif atteignant la cible et r\u00e9duire les doses n\u00e9cessaires."),
    ("Quel est le lien entre les statines et l\u2019HMG-CoA r\u00e9ductase ?", "Les statines sont des inhibiteurs comp\u00e9titifs de l\u2019HMG-CoA r\u00e9ductase, enzyme limitante de la synth\u00e8se du cholest\u00e9rol."),
    ("Pourquoi le march\u00e9 des statines est-il si important pour l\u2019industrie ?", "L\u2019hypercholest\u00e9rol\u00e9mie est une pathologie chronique fr\u00e9quente n\u00e9cessitant un traitement au long cours, repr\u00e9sentant un march\u00e9 consid\u00e9rable."),
    ("Quelle est la diff\u00e9rence entre un IEC et un antagoniste des r\u00e9cepteurs AT1 en termes de m\u00e9canisme ?", "L\u2019IEC emp\u00eache la formation de l\u2019angiotensine II ; l\u2019antagoniste AT1 bloque l\u2019action de l\u2019angiotensine II d\u00e9j\u00e0 form\u00e9e."),
    ("Pourquoi le telmisartan a-t-il \u00e9t\u00e9 d\u00e9velopp\u00e9 comme analogue du losartan ?", "Pour am\u00e9liorer la s\u00e9lectivit\u00e9 pour le r\u00e9cepteur AT1, la dur\u00e9e d\u2019action et le profil pharmacocin\u00e9tique."),
    ("Qu\u2019est-ce que la pharmacovigilance ?", "La surveillance des effets ind\u00e9sirables des m\u00e9dicaments apr\u00e8s leur mise sur le march\u00e9."),
    ("Quel lien existe entre la pharmacovigilance et la d\u00e9couverte de nouvelles indications ?", "La pharmacovigilance peut r\u00e9v\u00e9ler des effets inattendus exploitables comme nouvelles indications th\u00e9rapeutiques."),
    ("Qu\u2019est-ce qu\u2019une AMM ?", "L\u2019Autorisation de Mise sur le March\u00e9, n\u00e9cessaire \u00e0 la commercialisation d\u2019un m\u00e9dicament."),
    ("Pourquoi la recherche continue-t-elle apr\u00e8s l\u2019obtention de l\u2019AMM ?", "Pour d\u00e9couvrir de nouvelles propri\u00e9t\u00e9s, \u00e9tendre les indications, surveiller les effets ind\u00e9sirables rares et identifier de nouvelles cibles."),
    ("Qu\u2019est-ce qu\u2019un repositionnement de m\u00e9dicament (drug repurposing) ?", "L\u2019utilisation d\u2019un m\u00e9dicament d\u00e9j\u00e0 approuv\u00e9 pour une indication diff\u00e9rente de celle initialement pr\u00e9vue."),
    ("Donnez un exemple de repositionnement de m\u00e9dicament.", "Le sild\u00e9nafil (Viagra), initialement \u00e9tudi\u00e9 pour l\u2019angor, repositionn\u00e9 dans l\u2019insuffisance \u00e9rectile puis l\u2019HTAP."),
    ("Qu\u2019est-ce que l\u2019enzyme de conversion de l\u2019angiotensine (ECA) ?", "Une enzyme qui convertit l\u2019angiotensine I inactive en angiotensine II vasoconstrictrice active."),
    ("Quel est le substrat de l\u2019enzyme de conversion ?", "L\u2019angiotensine I."),
    ("Quel est le produit de l\u2019enzyme de conversion ?", "L\u2019angiotensine II, un puissant vasoconstricteur."),
    ("Que se passe-t-il lorsqu\u2019on inhibe l\u2019enzyme de conversion ?", "La production d\u2019angiotensine II diminue, entra\u00eenant une vasodilatation et une baisse de la pression art\u00e9rielle."),
    ("Qu\u2019est-ce que le syst\u00e8me r\u00e9nine-angiotensine-aldost\u00e9rone (SRAA) ?", "Un syst\u00e8me hormonal r\u00e9gulant la pression art\u00e9rielle et l\u2019\u00e9quilibre hydrosod\u00e9, impliquant r\u00e9nine, angiotensine et aldost\u00e9rone."),
    ("Pourquoi la d\u00e9couverte de la p\u00e9nicilline est-elle un exemple majeur de d\u00e9couverte par hasard ?", "Car Fleming ne cherchait pas un antibiotique ; il a remarqu\u00e9 par accident l\u2019inhibition bact\u00e9rienne par un champignon contaminant."),
    ("Quelle est l\u2019importance clinique de la p\u00e9nicilline ?", "C\u2019est le premier antibiotique d\u00e9couvert, r\u00e9volutionnant le traitement des infections bact\u00e9riennes."),
    ("Quel est le m\u00e9canisme d\u2019action de la ciclosporine comme immunosuppresseur ?", "Elle inhibe la calcineurine, bloquant l\u2019activation des lymphocytes T et la production d\u2019interleukine-2."),
    ("Dans quel type de greffe la ciclosporine est-elle principalement utilis\u00e9e ?", "Dans la greffe d\u2019organe solide (rein, foie, c\u0153ur) pour pr\u00e9venir le rejet."),
    ("Qu\u2019est-ce que la s\u00e9lectivit\u00e9 d\u2019un m\u00e9dicament ?", "La capacit\u00e9 d\u2019un m\u00e9dicament \u00e0 agir pr\u00e9f\u00e9rentiellement sur une cible pharmacologique donn\u00e9e, limitant les effets sur d\u2019autres cibles."),
    ("Pourquoi la non-s\u00e9lectivit\u00e9 peut-elle \u00eatre b\u00e9n\u00e9fique ?", "Car elle permet de d\u00e9couvrir des applications dans d\u2019autres pathologies o\u00f9 la m\u00eame cible est impliqu\u00e9e."),
    ("Qu\u2019est-ce que la PDE5 ?", "La phosphodiest\u00e9rase de type 5, une enzyme qui d\u00e9grade le GMPc, impliqu\u00e9e dans la relaxation des muscles lisses vasculaires."),
    ("Comment le sild\u00e9nafil agit-il sur la PDE5 ?", "Il inhibe la PDE5, emp\u00eachant la d\u00e9gradation du GMPc, ce qui favorise la vasodilatation."),
    ("Pourquoi l\u2019inhibition de la PDE5 est-elle utile dans l\u2019HTAP ?", "Car la vasodilatation pulmonaire r\u00e9duit la r\u00e9sistance vasculaire pulmonaire et am\u00e9liore la fonction cardiaque droite."),
    ("Pourquoi l\u2019inhibition de la PDE5 est-elle \u00e9tudi\u00e9e dans la myopathie de Duchenne ?", "Car elle pourrait am\u00e9liorer la perfusion musculaire et r\u00e9duire la fibrose dans les muscles dystrophiques."),
    ("Quel est l\u2019avantage \u00e9conomique d\u2019un repositionnement de m\u00e9dicament ?", "Le m\u00e9dicament a d\u00e9j\u00e0 pass\u00e9 les \u00e9tapes de s\u00e9curit\u00e9, r\u00e9duisant le co\u00fbt et la dur\u00e9e du d\u00e9veloppement pour la nouvelle indication."),
    ("Quelle est la diff\u00e9rence entre un effet ind\u00e9sirable et un effet secondaire ?", "L\u2019effet ind\u00e9sirable est tout effet non souhait\u00e9 ; l\u2019effet secondaire est un effet pharmacologique accessoire, pas forc\u00e9ment n\u00e9gatif."),
    ("Comment l\u2019hypertrichose du minoxidil est-elle pass\u00e9e d\u2019effet ind\u00e9sirable \u00e0 indication ?", "L\u2019observation syst\u00e9matique de repousse capillaire chez les patients hypertendus trait\u00e9s a conduit \u00e0 son d\u00e9veloppement topique contre la calvitie."),
    ("Qu\u2019est-ce qu\u2019une cible th\u00e9rapeutique ?", "Une mol\u00e9cule biologique (enzyme, r\u00e9cepteur, canal ionique, transporteur) sur laquelle un m\u00e9dicament agit pour produire son effet."),
    ("Quel type de cible est l\u2019HMG-CoA r\u00e9ductase ?", "C\u2019est une enzyme."),
    ("Quel type de cible est le r\u00e9cepteur AT1 ?", "C\u2019est un r\u00e9cepteur membranaire coupl\u00e9 aux prot\u00e9ines G."),
    ("Quel est l\u2019int\u00e9r\u00eat de conna\u00eetre le m\u00e9canisme physiopathologique pour concevoir un m\u00e9dicament ?", "Il permet d\u2019identifier des cibles pr\u00e9cises et de concevoir des mol\u00e9cules sp\u00e9cifiques, augmentant l\u2019efficacit\u00e9 et r\u00e9duisant les effets secondaires."),
]

assert len(flashcards) == 100, f"Expected 100 flashcards, got {len(flashcards)}"

# Build JS array
lines = ["const flashcardsData = ["]
for q, a in flashcards:
    lines.append(f"{{ question: '{q}', answer: '{a}' }},")
lines.append("];")
new_data = "\n".join(lines)

# Read file
filepath = "/Users/cyrilwisa/Desktop/diploma/UPEC_LSPS1_S2/ICM/fc9.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace
content = re.sub(r'const flashcardsData\s*=\s*\[.*?\];', new_data, content, flags=re.DOTALL)

# Write
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"fc9.html updated with {len(flashcards)} flashcards")
