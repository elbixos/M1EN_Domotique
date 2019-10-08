
### Définitions et formalisation

Au cours de ces expériences, nous avons finalement mis en place la plupart
des outils utilisés en domotique réelle :

- un serveur en charge de centraliser les opérations :
c'est notre Raspberry pi hébergeant le serveur Web

- un logiciel capable de recevoir les commandes des utilisateurs
(c'est le serveur Web)

- des objets distants connectés sur lesquels le serveur envoie des commandes
(c'est notre second Raspberry Pi)

Pour la communication entre le serveur et les objets connectés, nous avons en fait défini un **protocole**.
Ce protocole de communication définit comment sont faites les communications
et de quoi elles sont composées.



Notre protocole à nous :
- s'appuie sur le wifi (ou le filaire) : des sockets **TCP**
- ne prévoit que deux commandes : *eteind* ou *clignote*. Dans le cas de cette
dernière commande, celle ci doit aussi spécifier à quelle fréquence l'objet
doit clignoter, sous la forme d'une chaine de caractères telle que :
*clignote 0.5*
- l'objet connecté ne répond rien au serveur, qui ne sait jamais dans quel
état est l'objet qu'il gère.

### Améliorations et variantes possibles

Pour améliorer, on pourrait envisager plusieurs pistes :
- Donner de nouvelles possibilités aux objets, comme allumer une led avec une
  intensité variable ou encore utiliser autre chose que des Led...
- chaque objet peut signaler au serveur son état (ce qui permettrait
  d'afficher quelles leds sont allumées ou clignotent...)
- Les objets sont découverts automatiquement quand ils arrivent sur le réseau.
- Les objets fournissent eux même la liste des commandes qu'ils supportent,
le serveur adapte ses formulaires à cette liste.

Notre architecture, certes simple, est néanmoins très flexible et permet
de nombreuses variantes.

- les objets ne sont pas forcément hébergés sur un Raspberry Pi (qui est un peu cher pour cela). Un *arduino nano* équipé d'un *ESP8266* à 0.66 euros pourrait faire l'affaire (à vrai dire, l'ESP8266 tout seul ferait l'affaire)
- les objets ne sont pas forcément programmés en Python. N'importe quel langage acceptant les sockets peut faire l'affaire (tous... C, Java, ...)
- de même, le programme qui se connecte sur les objets peut être écrit
en n'importe quel langage (même directement en PHP)

### Solutions grand public

Il existe de nombreuses solutions grand public pour faire de la domotique.
Toutes s'appuient sur les notions vues précédemment.

Elles se distinguent par :
- leur prix
- la qualité de leur interface de controle (leur serveur Web)
- les protocoles gérés (**Z-Wave**, **Bluetooth**,...)
- les équipements qu'elles peuvent gérer

Une des plus utilisées et qui soit liée au monde du libre est **Jeedom**.
Nous verrons sans doute en TP comment l'utiliser sur des appareils
plus complexes qu'une LED.
