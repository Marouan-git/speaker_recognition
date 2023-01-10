# Speaker_recognition

L'objectif de cette application est de mettre en place un système d'identification par reconnaissance vocale. 
L'idée est d'empêcher l'usurpation d'identité (accès à des informations confidentielles, des lieux à accès restreints...) avec une méthode non intrusive et ergonomique.

Pour illustrer ce système d'identification vocale, 3 classes sont distinguées :
- "aissa" : désigne une personne dont l'accès est autorisé.
- "marouan" : désigne une autre personne dont l'accès est autorisé.
- "autre" : désigne tout autre personne dont l'accès n'est pas autorisé.

## Améliorations possibles

Les résultats globaux sont assez bons (88% accuracy, 97% recall pour classe "autre"). Néanmoins, des améliorations sont possibles pour rendre le système encore plus fiable et plus ergonomique :
- Les précisions pour les classes "Aissa" et "Marouan" sont respectivement de 87% et 83%. Cela signifie qu'il y a 3 chances sur 10 pour que quelqu'un réussisse à usurper l'identité d'Aissa et Marouan. Il faudrait améliorer cette métrique pour diminuer les chances d'usurpation d'identité.
- Le recall pour la classe "Aissa" est de 76%, contre 84% pour la classe "Marouan". On peut éventuellement améliorer le recall pour la classe Aissa afin qu'il est moins besoin de répéter pour pouvoir s'identifier.
- Le recall pour la classe "autre" (c'est-à-dire les personnes non autorisées) est de 97%, ce qui est un très bon résultat, mais il est peut-être possible de passer à 100% (ou du moins augmenter encore le recall) pour fiabiliser davantage le système.
- La méthode pour s'identifier sur l'application nécessite d'avoir un fichier wav déjà enregistré ou d'enregistrer un vocal via un voice recorder et charger le fichier dans l'application.
Il est préférable de pouvoir enregistrer directement l'audio via l'application (plus ergonomique).

## Solutions d'amélioration envisagées

### Pour les 3 premiers points d'amélioration (amélioration des métriques)
Le modèle actuel utilisé est un modèle de machine learning Random Forest.

Considérant que la représentation de l'audio en spectrogramme se rapproche de celle d'une image, on peut émettre l'hypothèse qu'un algorithme de deep learning avec une architecture CNN permettra d'avoir une meilleure extraction des caractéristiques du son et donc une meilleure discrimination (et potentiellement une amélioration des métriques de classification).

Comme le deep learning nécessite en général une grande quantité de données d'entrainement (ce que nous ne possédons pas) pour extraire les caractéristiques discriminantes, il parait judicieux de faire du transfer learning en utilisant des algorithmes déjà entrainés sur un grand volume de données audio. En effet, ces algorithmes déjà entrainés sont capables d'extraire les caractéristiques haut niveau d'un audio, il suffira d'ajouter des couches externes à entrainer avec les audios enregistrés pour les 3 classes "aissa", "marouan" et "autre".

D'après ce papier de recherche (https://www.mdpi.com/2224-2708/10/4/72), VGGish et YAMNet sont les algorithmes donnant les meilleurs résultats pour de la classification d'audios. VGGish est très légèrement meilleur, mais YAMNet semble être plus utilisé (100k vs 10k téléchargements sur tensorflow hub) et il semble y avoir davantage de documentation montrant comment l'utiliser. C'est pourquoi il sera choisi pour le transfer learning.

On considérera que l'amélioration est significative si les métriques augmentent de 5%, sauf pour le recall de la classe "autre" dont la valeur est déjà très élevée.

Charge de travail estimée : 1 jour et demi

### Pour le dernier point d'amélioration (amélioration de l'interface)
Utiliser un outil javascript pour enregistrer directement un audio sur l'application.
L'interface javascript MediaRecorder permet de faire cela assez facilement. Il faudra cependant récupérer le fichier audio enregistré et l'envoyer au serveur via une requête ajax.

Charge de travail estimée : 1/2 jour
