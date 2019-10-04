## Amélioration de la gestion des LED

Ici, nous voulons que l'on puisse, par exemple,
faire clignoter une diode avec une fréquence définie.

Le problème est le suivant :
Nos programmes précédents allumaient la diode une seconde
puis s’arrêtaient.

Ici, le programme python qui pilote la diode doit :
- tourner en permanence (et faire clignoter)
- écouter le serveur web à l'écoute d'une nouvelle consigne.

Notre programme python va donc se comporter comme un **serveur**
(un logiciel qui tourne en permanence). Ce serveur sera le programme *serverLed.py*

Il faudra que le serveur web **contacte** le serveur
en tant que **client** pour envoyer ses consignes.

Pour rester le plus possible en Python, le nouveau mécanisme va
être le suivant :
quand on clique sur le bouton :
1. on appelle le formulaire *useLed.php*.
2. celui ci lance un programme python : *clientLed.py*
3. *clientLed.py* contacte *serverLed.py* pour lui donner ses consignes
4. *serverLed.py* actualise le comportement de la LED.

De fait, le programme *useLed.php* pourrait directement contacter
le programme *serverLed.py* mais j'ai souhaité que PHP ne fasse
que lancer du python.

Ceci nécessite deux ou trois nouvelles petites choses,
telles que des **sockets** et des **threads**...
Mais avant cela, préparons le fichier Php
