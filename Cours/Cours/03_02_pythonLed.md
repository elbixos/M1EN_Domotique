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

```html
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
 **Mais en fait non...**


 ### Quelques problèmes rencontrés.
En fait, nous avons eu plusieurs problèmes à régler.

#### Problèmes de permissions


Quand un navigateur demande une page *PHP* au serveur web du Raspberry Pi,
c'est bien le serveur (apache) qui exécute le code PHP sur le Raspberry Pi.
Dans le monde Linux, ce serveur est un utilisateur spécifique.
Dans le cas de la Raspbian, cet utilisateur s'appelle *www-data*.
Cet utilisateur a le droit de faire des choses, mais pas d'autres.

##### Droits d'accès aux fichiers php et python

Par exemple, le serveur ne peut pas fouiller dans tous les fichiers sauf si vous
lui donnez explicitement l'autorisation de le faire).

Notez que le code du programme *startLed.php* a été crée par un autre utilisateur
(*pi*) et est stocké dans le répertoire de celui ci.
il faut donc s'assurer que
1. *www-data* a le droit de traverser le répertoire */home/pi* (pour accéder
  à */home/pi/public_html*)
2. *www-data* a le droit de traverser *~/public_html* pour accéder au fichier *startLed.php*
3. *www-data* a le droit de lire le fichier *startLed.php*
4. *www-data* a le droit de lire le fichier *turnOn1s.py*

il suffit de lancer la commande
```
ls -alh ~/public_html
```

Vous devriez voir quelque chose comme ceci
(je dois ajouter l'image, je n'ai pas mon pc avec moi)
dans lequel on peut observer :


1. que tous les utilisateurs peuvent traverser */home/pi* (c'est le répertoire *..*)
2. que tous les utilisateurs peuvent traverse *~/public_html*
(c'est le répertoire *.*)
3. que tous les utilisateurs peuvent lire le fichier *startLed.php*
4. que tous les utilisateurs peuvent lire le fichier *turnOn1s.py*

Dans le cas du cours, ceci n'était pas le problème.

##### Droits d'accès aux GPIO

Par défaut, tous les utilisateurs n'ont pas le droit d'accès aux GPIO
(les broches du Raspberry). Il faut donc autoriser l'utilisateur *www-data*
à pouvoir manipuler ces broches.

Pour cela, linux utilise la notion de **groupes d'utilisateurs**.
Le groupe *gpio* à le droit d'utiliser les GPIO.
Il nous faut donc intégrer *www-data* au groupe *gpio*.
Ceci se fait avec cette commande.

```
sudo usermod -a -G gpio www-data
```

on peut vérifier les groupes de l'utilisateurs *www-data* en tapant
```
groups www-data
```

Enfin, il peut falloir redémarrer le serveur apache.
```
sudo /etc/init.d/apache2 restart
```

##### Des problèmes d'accents

Pour une raison pas très claire, il est apparu que le python, lancé par
*www-data* avait des soucis avec les accents dans le code (même dans les
  commentaires)
En première solution, j'ai supprimé les accents dans le code

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

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
  <form action="startLed.php" method="post">
    <button type="submit" id="submit" name="submit">Envoyer le message</button>
  </form>
</body>
</html>
```

### Rendons cela plus encore propre.

c'est un peu dommage que lorsque l'on clique sur le bouton,
on parte sur une nouvelle page.
Nous allons donc modifier un peu le code pour rester
toujours sur la même page.
Notre formulaire va tenir dans la page *startForm2.php*
et son traitement sera fait aussi par le fichier *startForm2.php*.
Pour cela, on modifie un peu le code précédent
```html
  <form action="startForm2.php" method="post">
```

Puis, il faut distinguer deux cas :
1. l'utilisateur arrive sur la page sans cliquer
(on lui afficher juste le formulaire)
2. l'utilisateur arrive sur la page parcequ'il a cliqué : on lui affiche le formulaire ET on allume la LED.

Pour faire cela, il vous faut quelques explications sur $ \_\_POST $.
Cette variable contient les données envoyée par le formulaire.
Ce formulaire ne contient qu'une donnée, associée au bouton *submit*.
La donnée associée au bouton submit est contenue dans *$\_POST["submit"]*

- Si on arrive sur la page sans cliquer, cette variable est non définie.
- Si on arrive sur la page en ayant cliqué, cette variable est la chaine de
caractères vide.

On peut donc écrire facilement le code suivant :
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
  <form action="startForm2.php" method="post">
    <button type="submit" id="submit" name="submit">Allumer</button>
  </form>

  <?php
  if (isset($_POST["submit"])){
      $command = escapeshellcmd('python3 turnOn1s.py');
      $output = shell_exec($command);
  }
  ?>
</body>
</html>
```

Voici le code complet de la page
[../Sources/startForm2.php](../Sources/startForm2.php)
