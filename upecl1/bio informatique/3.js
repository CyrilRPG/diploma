{ question: 'Quels sont les trois types de séquences biologiques comparées en bio-informatique ?', answer: 'Les séquences d’ADN, d’ARN et d’acides aminés.', },

{ question: 'Combien d’éléments différents composent l’ADN/ARN et les protéines ?', answer: 'ADN/ARN : 4 bases ; protéines : 20 acides aminés.', },

{ question: 'Que permet l’étude comparative des séquences ?', answer: 'D’obtenir des informations importantes sur leur fonction.', },

{ question: 'Pourquoi deux séquences similaires ont-elles probablement la même fonction ?', answer: 'Parce qu’elles sont composées des mêmes éléments dans le même ordre.', },

{ question: 'Quel est le principe d’un alignement de séquences ?', answer: 'Superposer deux séquences pour comparer leurs résidus.', },

{ question: 'Comment appelle-t-on deux nucléotides égaux à la même position lors d’un alignement ?', answer: 'Des nucléotides conservés.', },

{ question: 'Qu’est-ce qu’une substitution au cours de l’évolution ?', answer: 'Une base remplacée par une autre base.', },

{ question: 'Qu’est-ce qu’un gap dans un alignement ?', answer: 'Un trou dans la séquence dû à une insertion ou une délétion.', },

{ question: 'Comment calcule-t-on un pourcentage d’identité entre deux séquences ?', answer: 'Nombre d’identités divisé par la longueur de l’alignement × 100.', },

{ question: 'Quel est l’intérêt d’insérer des gaps dans un alignement ?', answer: 'Améliorer la conservation et augmenter le score d’alignement.', },

{ question: 'Quels sont les scores d’alignement possibles dans une approche simple ?', answer: '1 pour une identité, 0 sinon ; ou -1 pour substitution/gap.', },

{ question: 'Qu’est-ce que mesure un score de similarité ?', answer: 'La ressemblance entre deux séquences.', },

{ question: 'Qu’est-ce que mesure un score de divergence ?', answer: 'Les différences entre deux séquences.', },

{ question: 'Quel est l’objectif d’un algorithme d’alignement ?', answer: 'Trouver l’alignement ayant le meilleur score.', },

{ question: 'Que compare une matrice de substitution ?', answer: 'La similarité entre deux acides aminés.', },

{ question: 'Pourquoi Gly → Cys est-il un changement délétère ?', answer: 'Parce que leurs propriétés physico-chimiques sont très différentes.', },

{ question: 'Pourquoi Ile → Leu conserve-t-il souvent la fonction ?', answer: 'Car ces acides aminés sont similaires.', },

{ question: 'Qui a développé la première matrice de substitution ?', answer: 'Margaret Dayhoff.', },

{ question: 'Sur quoi reposent les matrices PAM ?', answer: 'Sur les mutations ponctuelles acceptées au cours de l’évolution.', },

{ question: 'Que mesure une matrice PAM0 ?', answer: 'Uniquement les identités (score 1 ou 0).', },

{ question: 'Quel peptide est le plus proche du peptide 1 dans l’exemple donné ?', answer: 'Le peptide 2 (score 27 vs -32).', },

{ question: 'Qu’est-ce que la matrice BLOSUM 62 ?', answer: 'Une matrice de substitution très utilisée pour les alignements.', },

{ question: 'Pourquoi existe-t-il un nombre énorme d’alignements possibles pour deux séquences ?', answer: 'Parce qu’il existe 2ⁿ manières d’aligner deux séquences de longueur totale n.', },

{ question: 'Qu’est-ce que la programmation dynamique ?', answer: 'Une méthode qui résout un problème en le décomposant en sous-problèmes.', },

{ question: 'Pourquoi utilise-t-on la programmation dynamique pour les alignements ?', answer: 'Pour éviter d’examiner toutes les solutions possibles.', },

{ question: 'Quelle est la différence entre une recherche globale et une recherche locale ?', answer: 'Globale : score sur toute la longueur ; locale : recherche d’un domaine spécifique.', },

{ question: 'Quel est l’intérêt d’un alignement local ?', answer: 'Détecter des régions fortement similaires entre protéines différentes.', },

{ question: 'Qu’est-ce que BLAST ?', answer: 'Un outil en ligne permettant de rechercher des régions similaires entre séquences.', },

{ question: 'BLAST compare-t-il toute une base de données ?', answer: 'Non, il sélectionne d’abord un sous-ensemble pertinent.', },

{ question: 'Que fournit BLAST pour chaque alignement ?', answer: 'Un score et une évaluation statistique.', },

{ question: 'Quel type de fichier peut être entré dans BLAST ?', answer: 'Une séquence brute ou une séquence au format FASTA.', },

{ question: 'Que permet de cocher l’option “score pour toutes les séquences similaires” ?', answer: 'D’obtenir le score pour chaque séquence similaire dans la base.', },

{ question: 'Que renseigne BLAST dans ses résultats ?', answer: 'Score, pourcentage d’identité, couverture de la séquence, E-value.', },

{ question: 'Quel seuil doit respecter l’E-value pour indiquer un alignement fiable ?', answer: 'Elle doit être inférieure à 1.', },

{ question: 'À quoi servent les graphiques de résultats BLAST ?', answer: 'À visualiser les alignements selon un code couleur.', },

{ question: 'Que signifie une zone rouge dans le graphique BLAST ?', answer: 'Un alignement de score maximal.', },

{ question: 'Que peut-on voir dans les détails d’un alignement BLAST ?', answer: 'Identités, substitutions, gaps et scores basés sur BLOSUM62.', },
