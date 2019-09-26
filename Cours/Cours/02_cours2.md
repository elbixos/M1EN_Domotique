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

___
Vous pouvez repartir vers le [Sommaire](99_sommaire.md)

___
