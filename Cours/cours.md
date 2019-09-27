
# Cours Programmation et Objets Connectés

# Auteur : Vincent Pagé : <vincent.page@univ-antilles.fr>


## Introduction

Dans ce cours, nous verrons donc comment aborder la programmation des Objets
Connectés.

Pour la définition, j'ai, sans scrupules, repompé ce qui se dit ici :
[http://www.smartgrids-cre.fr/index.php?p=objets-connectes-definition](http://www.smartgrids-cre.fr/index.php?p=objets-connectes-definition).

Donc, tel quel :

```
Un objet connecté est un objet physique équipé de capteurs ou d’une puce qui
lui permettent de transcender son usage initial pour proposer de nouveaux
services. Il s’agit d’un matériel électronique capable de communiquer avec un
ordinateur, un smartphone ou une tablette via un réseau sans fil (Wi-Fi,
Bluetooth, réseaux de téléphonie mobile, réseau radio à longue portée de type
Sigfox ou LoRa, etc.), qui le relie à Internet ou à un réseau local.

On distingue communément deux grands groupes d’objets connectés :

    - les objets destinés à la collecte et l’analyse de données, dont la
    mission principale est de collecter et transmettre des informations ;

    - les objets qui répondent à une logique de contrôle-commande et
    permettent de déclencher une action à distance.

Les capteurs installés sur ces objets connectés sont plus ou moins
intelligents, selon qu’ils intègrent ou non eux-mêmes des algorithmes
d’analyse de données, et qu’ils soient pour certains auto-adaptatifs.

Sortie en 2003, la lampe DAL connectée en Wi-Fi est le premier objet connecté
de l’histoire. Selon ses créateurs, elle s’est vendue à une cinquantaine
d’exemplaires. Grâce à ses 9 LED, elle pouvait s’allumer de différentes
couleurs en fonction de différents événements liés à la météo, la situation
boursière, la pollution, les alertes Google ou encore des « envois de messages
de couleurs » par SMS ou courriel.
```

Dans la pratique, on voit donc qu'un objet connecté, c'est avant tout :

- un circuit électronique
- dont les actions sont programmables
- qui peut dialoguer sur un réseau (local ou global)

A terme, lors des Travaux Pratiques, nous souhaiterions mettre en place
un équipement dans les salles de TP permettant de contrôler

- la clim
- l'éclairage
- des brasseurs d'air

Tout ceci serait contrôlable depuis un **smartphone**, via un serveur.
Le serveur serait, lui, hébergé sur un **raspberry**.

Si certains de ces mots vous échappent pour le moment, ce n'est pas grave,
on va voir cela calmement.

Mais pour faire tout cela, il va nous falloir quelques notions, et pour
commencer, quelques notions sur les **circuits électroniques programmables**.

___
Vous pouvez repartir vers le [Sommaire](99_sommaire.md)

___
### Introduction aux cartes Arduino

Avant même de faire des objets connectés, il faudrait donc pouvoir programmer
des circuits électroniques. Pour avoir une idée de choses qui nécessitent une des circuits electroniques programmables, considérez un peu :

- la barrière d'entrée de l'université
- un distributeur automatique de boissons.

Ce sont des objets qui ne sont pas forcément connectés, mais dans lequel
on doit effectuer des actions spécifiques lorsque certains évenements se
produisent dans le bon ordre (faire tomber une cochonnerie sucrée lorsque
l'on a mis de l'argent et qu'on a appuyé sur le bon bouton. Accessoirement,
il faut aussi calculer la monnaie à rendre, puis la rendre
(ou blinder la machine contre les coups de genoux)).

Pour faire tout cela, la solution la moins cher consiste
à intégrer dans votre circuit électronique une **carte electronique programmable**. Il en existe énormément de type, de prix très variables.
(ici, je vous mettrais une liste non exhaustive).

Dans le domaine du DIY (Do It Yourself), ce qu'on appelerait sans doute en français le domaine du "je bricole moi même mes trucs de geek", une carte a,
au cours des dernières années, obtenue beaucoup de succès : les cartes
**Arduino**.

#### Les cartes Arduino

Ci dessous, une photo de l'Arduino Uno, très pratique pour les enseignements.
![L'arduino Uno](Arduino_Uno.jpg)

En soi, elle n'ont rien de mieux que les autres, simplements, leurs plans
sont **open source**, copiables, et il existe une documentation très vaste
concernant leur utilisation par des novices.

Cette carte comporte, comme toutes les cartes programmables :

- Un microprocesseur (qui executera le programme)
- une alimentation
- une horloge (qui cadence le programme)
- des broches permettant d'interagir avec le matériel (les boutons, les moteurs, les capteurs ou les lumières)


L'idée est donc de concevoir un programme, qui va prendre en charge
les différents cas qui peuvent se présenter au matériel et déclencher
les évênements voulus.

#### Le logiciel Arduino

Ce programme, dans le cas des cartes Arduino (et très souvent sauf pour
certaines cartes récentes permettant de taper directement le code sur la
carte), est concu sur un ordinateur, pourvu d'un logiciel permettant
de charger ensuite le programme sur la carte.

Lorsque la carte est mise sous tension, ce programme s'éxecute (et on peut
acheter un Mars. Ou un Snickers).

Ce logiciel permettant de préparer son programme et de le charger sur la carte
est également **Open Source** et gratuit dans le cas des cartes Arduino,
ce qui a contribué à leur succès.

Ci dessous, un exemple du logiciel Arduino, permettant de dialoguer avec
l'ensemble des cartes de la famille :
![Logiciel Arduino](arduinoLogiciel.png)

#### Le premier programme

L'équivalent des programmes de type **helloWorld** en électronique
consiste à faire clignoter une diode LED.

Je ne vais pas m'apesantir sur le sujet de la programmation Arduino, car nous
basculeront assez vite sur des Raspberry Pi, mais on retrouve néanmoins de
nombreux points communs entre les programmes sur ces deux types de matériel.

Un programme Arduino est souvent écrit dans un langage proche du **langage C**.
Il comporte deux parties :

- une fonction **setup** qui s'exécute une fois lorsque la carte est mise sous
tension.
- Lorsque le **setup** est terminé, c'est la fonction **loop** qui s'exécute juste en boucle, indéfinimement tant que la carte est sous tension.

Pour faire clignoter une led, il faudrait :

- préparer le circuit electronique (je vais ajouter un schéma un jour)
- brancher ce circuit sur une des broches de la carte (disons la broche 4 par
  exemple)

Le **setup** consisterait a dire : je vais utiliser la broche 4 comme **broche de sortie**

La **loop** pourrait consister a dire :

1. Je met la broche 4 à 5V (a l'état **HAUT**)
2. J'attends un peu (disons une seconde ou 1000 ms)
3. Je met la broche 4 à 0V (a l'état **BAS**)
4. J'attends un peu (disons une seconde ou 1000 ms)

Tout ceci se retrouve dans le programme qui suit :

```c
int brocheLed = 4

// the setup function runs once when you press reset or power the board
void setup() {
  // La broche 4 sera utilisée en SORTIE
  pinMode(brocheLed, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(brocheLed, HIGH);  // Allume la diode
  delay(1000);                    // Attend 1s
  digitalWrite(brocheLed, LOW);   // Eteint la diode
  delay(1000);                    // attend une seconde
}
```
Le programme complet est disponible ici :
[../Sources/Blink.ino](../Sources/Blink.ino)
### Raspberry Pi, premiers pas

Ici, je vais vous présenter les Raspberry,
et toujours faire un premier programme (qui fera aussi clignoter une diode)

#### Présentation des Raspberry Pi

Raspberry Pi est une fondation (originaire du Royaume Uni), qui développe
des ordinateurs tenant sur une seule carte, de taille très réduite.
Du coup, on dit souvent que les Raspberry Pi sont sont des **nano-ordinateurs**.
Du coup, un raspberry pi est avant tout... un ordinateur.

Ci desous, le logo des raspberry pi, une célèbre framboise :

![logo Raspberry Pi](RaspberryPiLogo.png)

Par rapport a ses grands frères comme les PC, il offre de nombreux avantages
pour travailler avec des objets connectés :
- Ils sont petits.
- Ils sont peu cher.
- Ils consomment très peu d'énergie.
- Ils ont des broches pour interagir avec le matériel (comme les cartes
  Arduino vues précédemment)

En revanche, ils sont relativement peu puissants, ce qui nous empecherait de
faire tourner des gros jeux vidéos dessus. Mais leur puissance est tout à fait
adaptée à de nombreux usages.

Il en existe de nombreuses versions. En TP, nous utiliserons la version *3B*
qui offre l'avantage d'intégrer nativement **le wifi**, **le bluetooth**.
Actuellement, il existe un **raspberry 4**, un peu plus cher et un peu plus
puissant.

Comme tout ordinateur, le raspberry pi a besoin d'un **disque dur**, qui est
dans ce cas une carte **micro SD**.
Le raspberry pi a également besoin d'un système d'exploitation qui est, le plus
souvent, un système **Linux**, dans sa variante **Raspbian**, dérivée de la
distribution Linux **Debian**. Ce système d'exploitation, ainsi que tous les
fichiers que vous pourriez créer ou télécharger seront stockés sur la carte
micro SD.

La version du Raspberry Pi que je vous ai présentée en cours est équipée d'un systeme de
fenêtrage qui permet d'interagir avec lui  avec une souris comme pour tout
ordinateur classique ces jours ci (nous verrons dans un autre cours qu'on peut
s'en passer).

J'ai donc branché sur un **clavier usb**, une **souris usb** et un
**écran HDMI** directement sur le raspberry. L'alimentation est en 5V sur un
port **micro USB**. Dans ce premier cours, nous avons utilisé le powerbank

Lorsque le raspberry pi est configuré pour cela, lorsqu'on le met sous tension,
l'ordinateur **boote**, puis vous propose un écran de connection.
Le login par défaut est **pi**, son mot de passe est **raspberry**.

d'un de vos camarades, vu que j'avais oublié mon alim...
![raspberry login](raspberryLogin.jpg)

Ceci permet alors d'accéder au bureau, géré par un logiciel nommé **pixel**.

![pixeldesk](pixeldesk.jpg)

Nous sommes donc en présence d'un véritable ordinateur fonctionnel, permettant
notamment de programmer dans toutes sortes de langages (C, java, python...).

#### Premier programme en Python

Dans notre cas, nous utiliserons Python que nous pouvons lancer pour le moment
avec son environnement de développement.

![idle](hello_world_idle.jpg)

A gauche, la console ou s'éxecute le programme, à droite, le programme python.
(Pour exécuter un programme dans ce contexte, appuyer sur la touche F5)

Comme précédemment, nous souhaitons faire clignoter une LED, branchée
sur une broche du raspberry. Voyons calmement ce programme.

Tout d'abord, il faut choisir une broche sur laquelle brancher la LED.
Pour cela, il faut disposer du plan
des broches (le **pinout**) qui est présenté ci dessous

![pinout Raspberry](raspberryPinout.jpg)

On peut voir que les broches sont numérotées de 1 à 40. Par exemple, les
broches 2 et 4 sont a 5V. Les broches 6 et 9 sont a la masse. La broche 8 est
une broche d'interaction nommée *GPIO14*. **GPIO** est l'acronyme de *General
Purpose Input Output*, ce qui signifie "Broches d'entrées / sorties à usage
général".

Un programme qui veut utiliser une de ces broches devra donc la désigner,
soit par son numéro physique sur la carte (la broche 8), soit par le numéro
qui compose son nom de GPIO (14).

Voici le schéma de montage complet. La masse est prise sur la broche physique 6, la broche physique 8 est utilisée pour l'anode (positif) de la LED.

![schema LED](blinkingLED.jpg)

Voyons donc le programme complet, qui suit exactement celui que nous avions
fait pour l'arduino avec quelques petites modifications :

1. On specifie quelle broche est utilisée

2. Puis indéfinimement

  1. On allume la diode
  2. On attend 1s
  3. On eteind la diode
  4. On attend une seconde.


Tout d'abord, il faut dire à python que nous souhaitons utiliser la fonction
*sleep* qui permet de mettre en pause le programme (pour attendre une
seconde). Cette fonction est disponible dans le **module** *time*, que notre
programme doit importer avec la ligne qui suit :

```python
import time
```

A partir de cette ligne, la fonction *sleep* pourrait être appelée
en tapant :
```python
time.sleep(1)
```

Par ailleurs, notre programme doit utiliser les broches.
Pour cela, on **importe le module RPi.GPIO**  qui va nous fournir
les outils pour cela, comme par exemple la fonction *setup* qui permet
de dire qu'une broche va être utilisée en entrée ou en sortie.
On pourait donc importer le module *RPi.GPIO* comme nous l'avons fait pour
le module *time*, mais il faudrait alors apppeler la fonction *setup* comme
suit :
```python
RPi.GPIO.setup(.....)
```
Pour simplifier un peu notre programme, nous allons donc importer le module
*RPi.GPIO* en lui donnant un alias (ici *GPIO*) comme suit.
```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
```
Si je veux utiliser la fonction *setup*, je taperais maintenant :
```python
GPIO.setup(.....)
```
Donc pour le moment, nous avons seulement importé nos deux modules
et notre programme ne contient que deux lignes :
```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function
```

Ajoutons deux lignes pour lui dire que nous utilisons la broche physique 8,
(aussi appelée GPIO14) comme broche de sortie. On commence par dire au
programme que nous utilisons la numérotation physique des broches (pas son
numéro de GPIO)

```python
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
```
Puis on désigne la broche 8 comme broche de sortie :
```python
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
```

Ces deux lignes constituent l'équivalent de ce qui se trouvait dans la fonction *setup* du programme Arduino.

Pour la suite, notre programme doit tourner en boucle indéfiniment,
ce que l'on va faire ici avec une boucle *while*, contenant les 4 étapes
(allume / attend / Eteint / attend)

```python
while True: # Run forever
    GPIO.output(8, GPIO.HIGH) # Turn on
    time.sleep(1)             # Sleep for 1 second
    GPIO.output(8, GPIO.LOW)  # Turn off
    time.sleep(1)             # Sleep for 1 second
```

Le programme complet figure ci dessous.
Il est également téléchargeable dans le répertoire [Sources](../Sources/)
de ce site. Il s'agit du fichier [blinkBoard.py](../Sources/blinkBoard.py).

```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function

GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

while True: # Run forever
    GPIO.output(8, GPIO.HIGH) # Turn on
    time.sleep(1)                  # Sleep for 1 second
    GPIO.output(8, GPIO.LOW)  # Turn off
    time.sleep(1)
```

On peut alors lancer ce programme et constater avec plaisir que notre diode
clignote. Elle ne s'arrêtera jamais. Pour stopper le programme, il faut
demander au système d'exploitation de l'arrêter, ce que l'on ferait en
appuyant sur **CTRL** et **C** simultanément (noté **CTRL C**)

Pour raffiner un petit peu, j'aurais tendance à définir une variable
pour contenir le numéro de la broche de la diode (si je veux modifier,
ce sera plus simple). Mon programme deviendrait :

```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function


GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering

ledpin = 8
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

while True: # Run forever
    GPIO.output(ledpin, GPIO.HIGH) # Turn on
    time.sleep(1)                  # Sleep for 1 second
    GPIO.output(ledpin, GPIO.LOW)  # Turn off
    time.sleep(1)
```

Par ailleurs, j'aurais aussi tendance a définir une variable pour contrôler
la durée totale d'un cycle (ici, 2 secondes) ce qui me permettrait de faire
clignoter ma diode plus ou moins vite. La diode reste allumée la moitié
d'un cycle puis éteinte la moitié d'un cycle. Mon programme deviendrait :

```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function


GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering

ledpin = 8
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

dureeCycle = 2 # En secondes

while True: # Run forever
    GPIO.output(ledpin, GPIO.HIGH) # Turn on
    time.sleep(dureeCycle * 0.5 )                  # Sleep for 1 second
    GPIO.output(ledpin, GPIO.LOW)  # Turn off
    time.sleep(dureeCycle * 0.5)
```

Notons enfin que notre programme utilise la broche 8. En fait, il a demandé
le contrôle de cette broche au Raspberry (qui lui donne de bon coeur).
En revanche, il faudrait que quand le programme s'interromp, il libère toutes
les broches utilisées. Ceci pourrait être fait avec la fonction *GPIO.cleanup()*.

Le problème est qu'il faudrait faire ceci quand notre programme s'arrete, et il ne s'arretera que quand on l'interromppra avec **CTRL C**.
On va donc dire au programme : Tourne indéfiniment, et si une interruption
de type CTRL C arrive, libère les broches.

Le programme complet serait alors, disponible ici : [blinkBoardClean.py](../Sources/blinkBoardClean.py)

```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function

GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering

ledpin = 8
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

dureeCycle = 2 # En secondes
try:    
    while True: # Run forever
        GPIO.output(ledpin, GPIO.HIGH) # Turn on
        time.sleep(dureeCycle * 0.5 )                  # Sleep for 1 second
        GPIO.output(ledpin, GPIO.LOW)  # Turn off
        time.sleep(dureeCycle * 0.5)

except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
```

Et voila !
## Connection au Raspberry en SSH

Pour aller un peu plus loin avec le Raspberry Pi, il va nous falloir
nous intéresser un peu au monde Linux, de façon à interagir avec lui à travers
un terminal (à la fin de ce cours, nous le ferons depuis un autre ordinateur).

Du coup, il me faut vous raconter deux ou trois choses sur Linux / Unix :

### Organisation des fichiers sous Linux

Tout d'abot, il nous faut comprendre comment est organisé l'**arborescence des fichiers** sous Linux.

Dans le monde Linux, tous les fichiers de l'ordinateur sont stockés dans un seul arbre. La **racine** de cette arborescence est notée **/**
Tous les autres fichiers sont quelque part à l'intérieur de cette racine.

A la racine, on trouve des sous répertoires, comme :

- */home/* qui contient les comptes de tous les utilisateurs (sauf un...)
- */etc/* qui contient des fichiers de configuration.
- */bin/* qui contient la plupart des programmes executables.
- ...

Ces répertoires peuvent contenir des sours répertoires et/ou des fichiers.

Enfin, dans chaque répertoire, on trouve deux autres sous répertoires :
- *.* qui désigne le répertoire lui même
- *..* qui désigne le répertoire parent. Par exemple */home/vpage/..**
est en fait */home/*


De plus, Linux permet, depuis toujours, à plusieurs utilisateurs de partager
le même ordinateur.

Chaque utilisateur est caractérisé par son *login* et il se connecte sur la machine par l'intermédiaire de son login et de son *mot de passe*. Chaque utilisateur dispose d'un répertoire personnel, appelé **home directory**,
stocké dans */home/* et qui contiendra tous ses fichiers.

Par exemple, si mon login est *vpage*, mon repertoire personnel sera (le plus
souvent) : */home/vpage*, dans lequel je pourrais créer des sous répertoires
pour ranger mes programmes, mes images...

Enfin, il existe un utilisateur spécial : **root** qui dispose des
droits d'administration (certains utilisateurs auront le droit de passer
momentanément **root** pour effectuer ces actions, nous reviendrons la dessus plus loin). Dans une distribution *Debian* comme celle qui tourne sur nos Raspberry Pi, cet utilisateur ne se connecte jamais directement.

Pour l'utilisation de Linux avec un gestionnaire d'écran, pas besoin de cours,
tout est a peu près intuitif. Vous aurez les mêmes façon d'interagir avec
l'ordinateur qu'avec les autres Systèmes d'exploitation (Windows, Mac Os) et le
même temps d'acclimatation à l'interface.

Néanmoins, il est très fréquent que certaines opérations doivent être faites
en **ligne de commande**, dans un terminal. Voyons donc le minimum vital pour
survivre en ligne de commande.

### La ligne de commande Bash

Quand on se trouve face à un terminal, on voit ce genre de choses :

![terminal](terminal.png)

On tape ses commandes sur la ligne qui clignote (le **prompt**).
Ce **prompt** donne en général quelques informations :

1. Dans l'image, l'utilisateur a pour login *vpage*
2. l'ordinateur sur lequel je travaille s'appelle *braquo*
3. je suis actuellement dans le répertoire */home/vpage/Documents/Cours/Refonte2018* . Ce répertoire est appelé **répertoire courant**.

Évidemment, si je me déplace dans l'arborescence, le répertoire
courant change... Le répertoire courant est le répertoire ou je suis
actuellement.

#### Les commandes les plus usuelles

Vite fait, quelques commandes utiles :


- **pwd** (path of working directory) affiche le chemin du répertoire courant)


- **ls** (list) : affiche les répertoires et les fichiers d'un répertoire)
On peut ainsi taper :
  - *ls* : cela liste les fichiers du répertoire courant.
  - *ls /home/vpage/* : cela liste les fichiers du répertoire /home/vpage/

- **cd** (change directory) ; permet de changer de répertoire.
On peut ainsi taper :

  - *cd /home/vpage/Document* pour aller dans le répertoire
  */home/vpage/document*
  - *cd monRepertoire* pour aller dans le sous repertoire *monRepertoire* du
  répertoire courant.
  - *cd ..* (répertoire parent)
  - *cd ~* (home directory)

- **mkdir** (make directory) : créer un répertoire. la commande *mkdir Truc*
va créer un répertoire nommé *Truc* dans le répertoire courant

- **rm** (remove) : effacer des fichiers, des dossiers.
On pourra taper les commandes :
  - *rm toto* : pour effacer le fichier *toto* du répertoire courant.
  - *rm -r monRep* : pour effacer le répertoire *monRep* du répertoire courant.

- **cp** (copy) : fait une copie du fichier. par exemple, *cp toto.txt sauvegarde.txt* fait une copie du fichier *toto.txt* du répertoire courant, et
la sauve sous le nom *sauvegarde.txt*, toujours dans le répertoire courant.

Pour toutes ces opérations, n'oubliez pas, comme vu en cours, qu'il est souvent
inutile de taper le nom complet des commandes, des fichiers ou des répertoires.
La touche < TAB > vous permet de demander la **complétion** des noms, ce qui
permet de gagner beaucoup de temps (et de ne pas faire d'erreurs).

#### Les commandes d'administration

Certaines commandes ne peuvent être executée que par **root**.
C'est par exemple le cas de la commande *raspi-config* qui permet
de modifier des paramètres primordiaux du Raspberry Pi.

Dans les distributions Debian, cela se fait de la façon suivante :
Si vous êtes un utilisateur de type **administrateur**, au lieu
de taper la commande
```
raspi-config
```
vous taperiez
```
sudo raspi-config
```

la commande **sudo** demande ici de lancer la commande *raspi-config* en tant
que **root**.
Le terminal vous demandera d'entrer votre mot de passe pour s'assurer
que c'est bien vous qui faîtes cette demande.


#### Editeurs de texte dans le terminal.

On peut aussi, depuis le terminal, lancer des programmes en les appelant par
leur nom. Dans un contexte de programmation en python, il nous faudra par
exemple lancer

1. un **editeur de texte** pour écrire notre programme (*toto.py*).
2. l’interpréteur python pour exécuter ce programme.

Il en existe de multiples. En voici trois :

- *vi* : très efficace, mais sa prise en main est délicate.
- *emacs* : pas moins efficace, prise en main un peu plus facile.
- *nano* : basique mais facile d'utilisation.

Si vous débutez, je vous conseille *nano* le temps de vous familiariser avec
votre terminal. Vous pourrez toujours vous intéresser à *vi* ou *Emacs* le
jour où vous aurez compris ce que cela apporte (en gros, un gain de temps sur
toutes vos opérations).

Mettons que je sois dans mon **home directory**, et que je veuille y créer un
chemin *M1/Prog/* dans lequel ranger un fichier **blink.py** puis le lancer,
voici la liste des commandes :

```bash
mkdir M1
mkdir M1/Prog
cd M1/Prog
nano blink.py
python blink.py
```

Avec cela, on doit pouvoir survivre pour la suite.
Notre objectif étant de nous connecter à un Raspberry Pi via le réseau
wifi, je vais devoir vous raconter deux ou trois choses sur les réseaux.

### Un peu de réseau.

Comme vous le savez sans doute, les ordinateurs discutent sur le réseau par
l'intermédiaire de **cartes réseaux** qui peuvent être filaire ou wifi.
Chaque carte est identifiée par un numéro, le **numéro IP**.
Mettons que je veuille discuter avec mon Raspberry Pi en wifi, il me faut
connaître le numéro IP de sa carte réseau wifi.

Pour cela, je vais taper dans un terminal du Raspberry Pi la commande
```
ifconfig
```
qui me donnera un résultat tel que le suivant (obtenu non pas sur un raspberry
mais sur mon pc...)

![ifconfig](ifconfig.png)

Dans cette réponse, je vois 4 interface réseaux, nommément :
- docker0
- enp2s0
- lo
- wlp9s0b1

celle qui commence par w est la carte wifi.
son numéro IP est **192.168.1.12**

### SSH

Je veux donc me connecter sur le Raspberry Pi depuis un autre ordinateur.
Pour cela, je vais utiliser le protocole **SSH** qui va me permettre
d'obtenir un terminal ouvert sur le Raspberry Pi.

pour utiliser **SSH**, il vous faut 2 choses :
- Un **client ssh** sur mon PC.
- Un **serveur ssh** sur le Raspberry pi (qui va accepter la connection)

Le Raspberry du cours est configuré pour avoir un serveur ssh fonctionnel.
(sinon, cela se fait grâce à la commande *raspi-config*)

Mon Pc linux dispose d'un client ssh. Sur une machine windows, on peut utiliser
par exemple le logiciel *Putty* qui fournit un client.


Mon objectif étant de me connecter, en tant qu'utilisateur *pi* sur le
Raspberry Pi dont j'ai trouvé l'adresse IP tout à l'heure : *192.168.1.12*.
La commande sera :
```bash
ssh pi@192.168.1.12
```

Après avoir entré notre mot de passe, nous disposons d'un terminal,
sur le Raspberry Pi permettant de lancer nos programmes qui font clignoter
nos LED...
## PWM sur un Raspberry Pi

### Raspberry Pi : des broches Numériques.

Au cours du premier cours, nous avions vu comment allumer et éteindre une LED.
Il est temps de clarifier un peu les choses pour aller plus loin et voir
ce qu'il est possible de faire ou pas avec les Raspberry Pi.

Tout d'abord, je vous avais signalé que les broches du Raspberry peuvent
être à l'état HAUT ou Bas. Ce sont des broches **numériques**.

Formalisons un peu cela : le Raspberry est alimenté en 5V.
Ses broches fonctionnent en **3.3 V**. L'état HAUT est donc une tension
de 3.3V, l'état BAS, une tension de 0V.

Qu'est ce que cela implique ?
Il n'y a pas de broche analogique sur un Raspberry Pi.
On peut donc lire ou écrire des
valeurs *0* ou *1*, mais en aucun cas *0.5*.

A vrai dire, si on applique 0.2V sur une broche d'entrée, le Raspberry la lira
comme un état BAS. Si on applique 2.8V, il lira un état HAUT)

De ce fait, il semble impossible d'allumer une lampe avec une intensité
variable sur un Raspberry, la lampe ne pouvant être que Allumée ou Eteinte.

### PWM : principe

Pour y arriver néanmoins, on va utiliser une feinte, dite **PWM** pour *Pulse Width Modulation*.

Lorsque l'on fixe l'état HAUT d'une broche, cela signifie que,
durant un cycle, de durée spécifique, l'état de la broche est HAUT.
Si l'on souhaite envoyer moitié moins de puissance à la broche,
on peut simplement mettre cette broche à l'état HAUT durant la moitié
du cycle.

Si la durée du cycle est très faible, on ne pourra pas voir que la lampe
s'allume puis s’éteint, on ne verra qu'une lampe allumée avec une intensité
plus faible.

Dans le cas d'un moteur, même principe permettrait de faire varier la vitesse
du moteur...

Voici une image représentant ces cycles, empruntée ici [https://www.mbtechworks.com/projects/raspberry-pi-pwm.html](https://www.mbtechworks.com/projects/raspberry-pi-pwm.html)

![duty cycle](pwm-duty-cycle.jpg)

La proportion de temps au cours d'un cycle pendant lequel la broche est
allumée est appelée **Duty Cycle**.


### PWM : programmes Python

#### Premier programme

Commençons par allumer une diode avec une valeur de duty cycle fixée par une
variable. Le programme commence comme précédemment.

```python
import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.

ledpin = 8


GPIO.setup(ledpin, GPIO.OUT)  # Set GPIO pin 12 to output mode.
```

Puis, nous demandons un objet PWM pour gérer la broche de la led.
Au passage, nous fixons la fréquence des cycles à 100 Hz (donc la durée d'un
cycle à 0.01s)

```python

freq = 100 # en Hz
pwm = GPIO.PWM(ledpin, freq)   # Initialize PWM on pwmPin 100Hz frequency
```

On fixe ensuite la valeur du duty cycle en fonction des besoins. Cette valeur
peut fluctuer entre 0 (HAUT 0% du cycle) et 100 (HAUT 100% du cycle).

```python
dc = 50
pwm.ChangeDutyCycle(dc)
```

Avec ceci, votre diode s'allume moins fortement qu'avec le programme du cours
précédent.
Le code complet de ce programme est ici :
[../Sources/BlinkPwm01.py](../Sources/BlinkPwm01.py)

En mixant ce principe avec nos compétences de programmation,
nous pouvons faire de nombreuses choses.

#### Demander à l'utilisateur de choisir une intensité

pour cela, il suffit de faire une boucle dans laquelle on demande à
l'utilisateur quelle intensité il souhaite, puis de fixer le duty cycle
à cette valeur. Tant que l'utilisateur n'aura pas entré de nouvelle
valeur, ce duty cycle ne change pas.

```python
while True :
    print ("entrez l'intensité souhaitée")
    dc = int (input() )
    pwm.ChangeDutyCycle(dc)
```

Le code complet de ce programme est ici :
[../Sources/BlinkPwm02.py](../Sources/BlinkPwm02.py)

#### Faire croitre l'intensité d'une led

Encore une fois, c'est relativement simple, il faut une variable qui croit
à chaque tour de boucle, puis on atteint 0.1 seconde avant de changer la valeur
du duty cycle. Si la valeur du Duty cycle passe au dessus de 100, on la
contraint à rester à 100.

```python
dc = 0

while True :
    print ("duty cycle",dc)
    pwm.ChangeDutyCycle(dc)

    dc+= 1

    if dc > 100:
      dc = 100

    time.sleep(0.1)
```

Le code complet de ce programme est ici :
[../Sources/BlinkPwm02.py](../Sources/BlinkPwm03.py)

#### la led qui s'allume et s'eteint progressivement

Même principe mais quand le duty cycle arrive a 100, il faut redescendre.
Quand il arrivera à 0, il faudra remonter.

Nous avons vu en cours que cela nécessitait une nouvelle variable
(ici *step*) qui contienne la direction actuelle (monte ou descend)
lorsqu'on arrive a une limite, on inverse la direction.


```python
dc = 0
step = +1

while True :
    print ("duty cycle",dc)
    pwm.ChangeDutyCycle(dc)
    dc+= step

    if dc >= 100 or dc <= 0:
      step *= -1

    time.sleep(0.1)

```

Le code complet de ce programme est ici :
[../Sources/BlinkPwm02.py](../Sources/BlinkPwm03.py)

C'est tout pour le cours 2.
## Une application Web minimaliste
## Quelques liens externes concernant python.

Le problème quand on enseigne l'informatique (ou quoi que ce soit d'autre), est d'adapter son discours a son public. Ce que je propose dans ce cours est un kit de survie pour l'algorithmique et la programmation utile pour tout ingénieur.

J'y fais d'énormes raccourcis.
Si vous souhaitez aller un peu plus loin voici quelques liens que j'ai glané sur internet.

### Un tutoriel pour se former :

Si vous souhaitez des informations plus détaillées, d'autres exemples, des exercices à faire, voici
 [un tutoriel](https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python)
 Je vous conseille de faire tout le début, vous pourrez vous arrêter quand vous voudrez.

### Le tutoriel officiel :
Vous voulez quelque chose de plus rigoureux, toujours sous forme de tutoriel ? Voici [un autre tutoriel](https://docs.python.org/fr/3/tutorial/index.html)
Il est bien aussi, mais il suppose souvent que vous travaillez sous Linux et/ou que vous ayez quelques bases en informatique...

### Un cours :
Vous souhaitez un gros pdf avec tout ce qu'on peut vouloir savoir sur python ? Voici [un gros cours](https://inforef.be/swi/download/apprendre_python3_5.pdf)
J'aurais tendance à louer son côté très complet, tout en lui reprochant de ne pas être ...synthétique...  

### Autres ressources
Si vous trouvez d'autres ressources utiles, n'hésitez pas à m'en faire part, je pourrais les ajouter...
