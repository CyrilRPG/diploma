{ question: 'Que signifie l’acronyme ADME ?', answer: 'Absorption, Distribution, Métabolisme, Excrétion.', },
{ question: 'Pourquoi quantifier les étapes ADME ?', answer: 'Pour définir le comportement pharmacocinétique des médicaments via des paramètres spécifiques.', },
{ question: 'Comment détermine-t-on les paramètres pharmacocinétiques ?', answer: 'À l’aide de procédés et de calculs mathématiques.', },

{ question: 'Quel paramètre caractérise une administration intraveineuse concernant l’absorption ?', answer: 'La concentration extrapolée au temps 0, appelée C0.', },
{ question: 'Comment évoluent les concentrations plasmatiques après injection intraveineuse ?', answer: 'Elles décroissent de façon exponentielle en reflétant distribution et élimination.', },

{ question: 'Que représente Cmax ?', answer: 'La concentration maximale atteinte après administration orale.', },
{ question: 'Que représente Tmax ?', answer: 'Le temps nécessaire pour atteindre Cmax.', },
{ question: 'Que traduit un Tmax court ?', answer: 'Une absorption rapide.', },
{ question: 'Que traduit une Cmax faible avec Tmax allongé ?', answer: 'Une absorption lente.', },
{ question: 'Qu’est-ce que la Surface Sous Courbe (SSC) ?', answer: 'L’aire sous la courbe concentration–temps, reflétant l’imprégnation du médicament.', },

{ question: 'Qu’est-ce que la biodisponibilité absolue F ?', answer: 'La fraction de dose atteignant la circulation générale et la vitesse à laquelle cela survient.', },
{ question: 'Quels paramètres conditionnent F ?', answer: 'La quantité absorbée (f) et la quantité éliminée par effet de premier passage (E).', },
{ question: 'Qu’est-ce que f ?', answer: 'La fraction absorbée, comprise entre 0 et 1.', },
{ question: 'Qu’est-ce que E ?', answer: 'La fraction éliminée par effet de premier passage hépatique.', },
{ question: 'Qu’est-ce que F’ ?', answer: 'La fraction échappant à l’effet de premier passage hépatique.', },
{ question: 'Quelle est la formule reliant F’, E et F ?', answer: 'F’ = 1 - E et F = f × F’.', },

{ question: 'Quelle est la biodisponibilité en intraveineux ?', answer: '100%.', },
{ question: 'Que signifie une biodisponibilité orale F = 30 % ?', answer: 'Faible biodisponibilité, avec 70 % détruits lors du premier passage.', },
{ question: 'Comment détermine-t-on F expérimentalement ?', answer: 'En comparant la SSC après voie orale et la SSC après voie intraveineuse.', },

{ question: 'Qu’est-ce que la biodisponibilité relative ?', answer: 'La comparaison entre deux formes pharmaceutiques d’un même médicament.', },
{ question: 'Qu’est-ce que la bioéquivalence ?', answer: 'Deux formes galéniques donnant la même SSC et les mêmes effets.', },

{ question: 'Qu’est-ce que le volume de distribution Vd ?', answer: 'Le volume théorique dans lequel le médicament se répartit pour être à la même concentration que dans le plasma.', },
{ question: 'Comment interpréter un Vd élevé ?', answer: 'Distribution intense dans les tissus.', },
{ question: 'Comment interpréter un Vd faible ?', answer: 'Faible diffusion tissulaire, médicament restant majoritairement dans le plasma.', },
{ question: 'Quelle est la formule du Vd initial ?', answer: 'Vd = Dose / C0.', },
{ question: 'Quelle est la formule du Vd apparent ?', answer: 'Vd = (t1/2 × ClT) / 0,7.', },

{ question: 'Qu’est-ce que fb et fu ?', answer: 'fb est la fraction liée aux protéines, fu la fraction libre.', },
{ question: 'À partir de quel seuil considère-t-on qu’un médicament est fortement lié ?', answer: 'Lorsque fb > 90%.', },
{ question: 'Comment calcule-t-on fu ?', answer: 'fu = 100 - fb.', },

{ question: 'Qu’est-ce que la clairance totale ClT ?', answer: 'La capacité d’épuration de l’organisme pour un médicament.', },
{ question: 'Comment s’exprime la clairance ?', answer: 'En volume de sang ou plasma épuré par unité de temps (L/h ou mL/min).', },
{ question: 'Quelles sont les formules de ClT ?', answer: 'Par voie IV : ClT = Dose / SSC ; par voie orale : ClT = (Dose / SSC) × F.', },
{ question: 'Comment s’exprime la clairance totale selon les organes ?', answer: 'ClT = ClR + ClH.', },

{ question: 'Qu’est-ce que fe ?', answer: 'La fraction de médicament éliminée sous forme inchangée dans les urines.', },
{ question: 'Quelle est la formule de la clairance rénale ?', answer: 'ClR = fe × ClT.', },
{ question: 'Que signifie fe = 1 ?', answer: 'Élimination urinaire totale.', },
{ question: 'Quelle est la formule de la clairance de filtration glomérulaire ?', answer: 'Clf = fu × DFG.', },
{ question: 'Que conclure si ClR = Clf ?', answer: 'Le médicament est éliminé uniquement par filtration glomérulaire.', },
{ question: 'Que conclure si ClR < Clf ?', answer: 'Réabsorption tubulaire prédominante.', },
{ question: 'Que conclure si ClR > Clf ?', answer: 'Sécrétion tubulaire prédominante.', },

{ question: 'Quels éléments influencent la clairance hépatique ?', answer: 'Débit sanguin hépatique QH, fixation protéique, clairance intrinsèque Cli.', },
{ question: 'Qu’est-ce que la clairance intrinsèque Cli ?', answer: 'La capacité maximale des hépatocytes à éliminer un médicament.', },

{ question: 'Qu’indique un coefficient d’extraction EH > 0,7 ?', answer: 'ClH proche de QH, médicaments flux-dépendants, fort effet de premier passage.', },
{ question: 'Qu’indique un coefficient d’extraction EH < 0,3 ?', answer: 'ClH ≈ fu × Cli, médicaments flux-indépendants et sensibles aux variations enzymatiques.', },

{ question: 'Qu’est-ce que la demi-vie t1/2 ?', answer: 'Le temps nécessaire pour que la concentration sanguine diminue de moitié.', },
{ question: 'Combien de demi-vies sont nécessaires pour éliminer presque tout le médicament ?', answer: 'Environ 5 demi-vies.', },
{ question: 'Combien de demi-vies pour atteindre l’état d’équilibre ?', answer: 'Environ 5 également.', },

{ question: 'Qu’est-ce qu’une pharmacocinétique linéaire ?', answer: 'Une situation où SSC et Cmax sont proportionnelles à la dose administrée.', },
{ question: 'Qu’est-ce que cela implique pour la clairance ?', answer: 'Elle est constante, quel que soit la dose.', },
{ question: 'Quels médicaments sont les plus faciles à prescrire ?', answer: 'Les médicaments à cinétique linéaire.', },
{ question: 'Pourquoi un médicament non linéaire est-il difficile à manier ?', answer: 'Car les concentrations varient de manière imprévisible en cas de modification posologique.', },
{ question: 'Quel exemple de médicament présente une cinétique non linéaire ?', answer: 'La phénytoïne, à cause de la saturation de son métabolisme.', },
