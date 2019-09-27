## Une application Web minimaliste

Pour aller un peu plus loin, nous souhaiterions controler notre
led depuis un ordinateur, ou un téléphone portable, par exemple.

Pour cela, le plus simple est de construire une application Web.

Par exemple, le Raspberry Pi pourrait héberger un **serveur WEB**.
Ce serveur Web proposera des pages permettant de contrôler le matériel.
L'intérêt d'utiliser un serveur Web, est que tous les ordinateurs équipés
d'un **navigateur Web** récent pourront agir sur notre raspberry pi.
C'est nottament le cas de votre smartphone, de votre pc portable (mac, linux, windows) ou de votre tablette...

Voyons donc brièvement ce qu'il nous faut :

### Le serveur web.

Un serveur Web est une application qui écoute le réseau et envoie
des pages HTML à qui les demande.

Quand on tape une **URL** telle que *http://monServeur.gp/toto.html*,
il se passe pas mal de choses, mais pour simplifier :

1. Le réseau trouve l'adresse IP correspondant à l'adresse *monServeur.gp*
2. le navigateur demande au serveur web hébergé à cette adresse le fichier *toto.html*
3. le serveur envoie le code HTML contenu dans cette page
4. Le navigateur affiche ce code HTML

Le serveur le plus utilisé au monde est, sans conteste, **Apache**.
Il est relativement facile d'installer Apache sur un Raspberry.

### Une page HTML de base

Pour écrire des sites Web, on écrit dans un langage, **HTML**,
qui décrit le contenu de la page à afficher.

Voici une page minimaliste
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
    Je suis une page Web minimaliste.
</body>
</html>
```
La première ligne signale que l'on ce document est écrit en... HTML (5).
Puis, on trouve des **balises**, signalées par des < chevrons >.
Ces balises s'ouvrent et se ferment (avec une balise de même nom
mais commençant par un / ).

La balise < html > signale le début d'une page HTML. Elle est fermée à la fin
du document. Toute la page est contenue entre ces deux balises.

On trouve ensuite 2 balises,
- **head** qui contient des informations sur la page (son titre, son encodage...)
- **body** qui contient ce qui s'affichera réellement dans le navigateur

N'ayant pas pour objectif de vous apprendre a faire des pages Web, mais de vous
fournir les notions minimal pour comprendre et faire des choses, cela nous
suffira pour le moment.

Le code complet est ici : [../Sources/minimal.html](../Sources/minimal.html)

### Ou placer sa page

Une page HTML peut etre ouverte par un navigateur directement comme un fichier.
Néanmoins, ce n'est pas ce que nous voulons le plus souvent. Nous voulons
que ce soit le serveur Web qui l'envoie.
Il faut donc placer cette page parmi les fichiers gérés par le serveur.

Dans notre cas, nous allons placer cette page parmi les pages Utilisateurs
(le module *USER_DIR* d'apache). Ce module permet à tous les utilisateurs
d'une machine de disposer d'un répertoire dans leur **home directory** pour
y placer leurs pages WEB.
Ce répertoire est le répertoire *public_html*. il doit être accessible en
lecture.

Dans notre cas, sur le raspberry, l'utilisateur est *pi*.
Nous avons donc crée un repertoire */home/pi/public_html* dans lequel
nous placerons tous nos fichiers (comme *minimal.html*)

Ce fichier est accessible par l'URL suivante :
 *http://IPduRaspberryPi/~pi/minimal.html*

### Une page HTML programmée

Le problème est que nous voulons faire un programme pour interagir avec
le Raspberry Pi. Nous pages ne doivent pas se contenter d'afficher des choses,
elles doivent pouvoir déclencher des actions paramétrables.

Pour cela, nous allons utiliser des pages **PHP**. PHP est un langage de programmation qui nous servira surtout a lancer d'autres programmes, donc
nous ne verrons encore une fois que peu de choses à son propos.

Reprenons l'exemple d'une **requête** du navigateur, mais portant sur une page
php cette fois :

Quand on tape une **URL** telle que *http://monServeur.gp/toto.php*,
il se passe encore plus de choses :

1. Le réseau trouve l'adresse IP correspondant à l'adresse *monServeur.gp*
2. le navigateur demande au serveur web hébergé à cette adresse le fichier *toto.php*
3. Le serveur exécute le code contenu dans le fichier *toto.php*
4. l'execution de ce code génère du code HTML
5. le serveur envoie le code HTML généré
6. Le navigateur affiche ce code HTML

Dans la version proposée ici, le fichier PHP contiendra le même code
HTML que précédemment.
Lorsque certaines opérations doivent être calculées, on bascule
en php avec la balise
```
<?php>
```
qui se ferme avec le code

```
?>
```

Voyons donc le contenu de cette page :
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
    Je suis une page Web minimaliste.
    <?php
    echo "Avec un programme qui s'execute sur le SERVEUR";

    $var1 = 12;
    $var2 = 6;

    echo $var1+$var2;
    ?>
</body>
```

Ce code doit être clair si l'on sait que :
- les variables commencent par un signe $ en php.
- *echo* est l'équivalent en PHP de *print* en python

Le code complet est ici : [../Sources/minimal.php](../Sources/minimal.php)

Encore une fois, on place ce fichier dans */home/pi/public_html*
et ce fichier est accessible par l'URL suivante :
 *http://IPduRaspberryPi/~pi/minimal.php*

**ATTENTION** : sur le Raspberry Pi, il faut veiller à avoir :

1. installé le module PHP pour apache
2. autorisé les USER DIR a utiliser php

### Lancement d'un programme Python par le serveur web

Notre serveur web peut executer des commandes, par l'intermédiaire
de PHP. Nous pourrions donc directement interagir avec les broches du
Raspberry Pi en PHP.
Mais je considère que Python vous sera plus utile et nous savons
déja faire des choses en Python, donc nous pouvons reformuler :

Nous voudrions donc un faire un programme en PHP qui lance, sur le serveur,
un programme Python (qui va gérer la LED)

Imaginons ce programme Python :
```python
print ("Je suis le programme python")

print ("je calcule un truc...")
a = 5
b = 8

print (a+b)
```

Le code complet est ici : [../Sources/test.py](../Sources/test.py)

Il est possible de le lancer depuis PHP, avec ce code :

```python
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
<?php

echo "<p>Je suis le script php. j'appelle un script
python et voici ce que celui écrit : </p>";

echo "<hr>";

$command = escapeshellcmd('python3 test.py');
$output = shell_exec($command);
echo "<p>";
echo $output;
echo "</p>";
?>
</body>
</html>
```
Le code complet est ici : [../Sources/phpLaunchPython.php](../Sources/phpLaunchPython.php)

Encore une fois, on place ce fichier dans */home/pi/public_html*
et ce fichier est accessible par l'URL suivante :
 *http://IPduRaspberryPi/~pi/phpLaunchPython.php*
## Application à la gestion des LED

### Allumage d'une Led pendant 1s

En remplacant le programme *test.py* par un programme qui allume une led
pendant une seconde, nous devrions avoir notre première gestion de matériel
depuis un site web.

Voici un programme python qui allume une LED pendant une seconde :
```python
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function

GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

GPIO.output(8, GPIO.HIGH) # Turn on
time.sleep(1)                  # Sleep for 1 second

GPIO.output(8, GPIO.LOW)  # Turn off

GPIO.cleanup()       # clean up GPIO on CTRL+C exit
```

Le code complet est ici : [../Sources/turnOn1s.py](../Sources/turnOn1s.py).

On appelle ce programme depuis une page php dont voici le code :

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
<?php

echo "<p>Je suis le script php. j'appelle un script
python et voici ce que celui écrit : </p>";

echo "<hr>";

$command = escapeshellcmd('python3 turnOn1s.py');
$output = shell_exec($command);
echo "<p>";
echo $output;
echo "</p>";
?>
</body>
```

Le code complet est ici : [../Sources/startLed.php](../Sources/startLed.php)

Encore une fois, on place ce fichier dans */home/pi/public_html*
et ce fichier est accessible par l'URL suivante :
 *http://IPduRaspberryPi/~pi/StartLed.php*

 Et cela doit allumer la LED !

 ### Rendons cela plus propre.

 Pour une application de domotique, il faudra sans doute des boutons
 de réglages, puis un bouton sur lequel cliquer pour envoyer les commandes.
 Tout ceci est fait en **HTML** avec des formulaires.

 Notre premier formulaire ne comportera qu'un bouton permettant
 de lancer la commande.

on ajouterait dans une page HTML les lignes suivantes
```html
<form action="traitement.php" method="post">
  <button type="submit">Envoyer le message</button>
</form>
```
Ceci crée un formulaire qui va appeler le fichier *traitement.php*
lorsque l'on clique sur le bouton.
Comme lorsque l'on clique, je veux en fait appeler le fichier PHP
qui lance le programme python qui allume la led, je modifie un peu
ce code en

```html
<form action="startLed.php" method="post">
  <button type="submit">Envoyer le message</button>
</form>
```

Voici le code complet de la page
[../Sources/startForm.php](../Sources/startForm.php)

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
  <form action="startLed.php" method="post">
    <button type="submit">Envoyer le message</button>
  </form>
</body>
</html>
```

 ### Rendons cela plus encore propre.

 c'est un peu dommage que lorsque l'on clique sur le bouton,
 on parte sur une nouvelle page.
 Nous allons donc modifier un peu le code pour rester
 toujours sur la meme page.

 Un peu d'explications sur $ \_\_POST $

 ### Rendons cela joli !

 On fera des CSS pour améliorer l'aspect visuel.

___
Vous pouvez repartir vers le [Sommaire](99_sommaire.md)

___
