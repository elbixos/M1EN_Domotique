
### Définitions et formalisation

#### Serveur et Objets connectés.

Au cours de ces expériences, nous avons finalement mis en place la plupart
des outils utilisés en domotique réelle :

- un serveur en charge de centraliser les opérations :
c'est notre Raspberry pi hébergeant le serveur Web.

- un logiciel capable de recevoir les commandes des utilisateurs
(c'est le serveur Web)

- des objets distants connectés sur lesquels le serveur envoie des commandes
(c'est notre second Raspberry Pi)

#### Protocole de communication

Pour la communication entre le serveur et les objets connectés, nous avons en fait défini un **protocole**.
Ce protocole de communication définit comment sont faites les communications
et de quoi elles sont composées.

Notre protocole est composé de plusieurs couches (je vais simplifier éhontément)

- une **couche application** : qui définit quelles commandes sont possibles.
Dans notre cas :
    - il n'y a que deux commandes dans le sens serveur -> objet : *eteind* ou *clignote*. Dans le cas de cette
    dernière commande, celle ci doit aussi spécifier à quelle fréquence l'objet
    doit clignoter, sous la forme d'une chaine de caractères telle que :
    *clignote 0.5*
    - l'objet connecté ne répond rien au serveur, qui ne sait jamais dans quel
    état est l'objet qu'il gère.

- ces commandes sont envoyées par le biais de la **couche Réseau**. Pour nous,
ce sont les sockets **TCP**. Celles ci s'assurent que les données sont bien envoyées et réceptionnées. A chaque envoi, l'envoyeur recoit par exemple des accusés de réception du recepteur. Les commandes de l'application sont donc encapsulées dans un message plus complexe comprenant des échanges entre les deux entités en contact.

- Ces échanges sont effectués via une **couche physique** sur laquelle circulent réellement les messages. Dans notre cas, il peut s'agir d'echanges par des **cables réseaux** ou du **wifi**. Ceci est complètement invisible pour nous
car pris en charge par la couche Réseau.

#### Améliorations et variantes possibles

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

### Quelques protocoles utilisés en domotique

Ces protocoles se distinguent essentiellement par :
- les commandes permises par la couche application
- la couche physique de transmission


#### Protocole Z-Wave
(repompé sur [https://fr.wikipedia.org/wiki/Z-Wave](https://fr.wikipedia.org/wiki/Z-Wave) )

Z-Wave communique en utilisant une technologie radio de faible puissance dans la bande de fréquence de 868 MHz. Ces échanges consomment beaucoup moins que
le wifi, qui est prévu pour des échanges haut débit.
La portée des échanges est évaluée à 50m.

Pour communiquer, deux périphériques doivent être « inclus » dans le même réseau Z-Wave. Z Wave peut connecter jusqu'a 232 appareils dans un même réseau.

Un intérêt notable de Z-Wave est la capacité, pour un équipement, à servir de relais vers d'autres points. Ainsi, on peut mailler un batiment d'objet qui serviront de relais vers le serveur (en plus de leur fonction domotique)

Z-Wave permet de préciser le type d'équipement avec la notion de classes (exemples : interrupteur binaire, capteur binaire, capteur multi-niveaux, moteur multi-niveaux, thermostat, alarme, ...).

Ainsi, les équipements s'enregistrent auprès du serveur en précisant leur classe, ce qui permet au serveur de proposer des interfaces adaptées à l'utilisateur.

#### Autres protocoles
on trouve aussi :
- Enocean
- ZigBee
- 6LoWPAN
- Chacon DIO

Pour certains de ces protocoles (Enocean, Chacon DIO),
le serveur centralisé n'est pas nécessaire.
On peut ainsi connecter un interrupteur à une lampe sans avoir
besoin de serveur centralisé pour régler les actions à effectuer.
