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
