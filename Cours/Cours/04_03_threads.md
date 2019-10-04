### Clignotement.

Oublions un instant le serveur web et  voyons comment faire clignoter proprement.
Comme je n'ai pas de Raspberry sous la main, je vais simuler avec un
programme qui affiche des choses.

L'idée du clignotement est la suivante :

```
import time

clignote = True
while clignote:
  print ("allume")
  time.sleep(1)
  print ("eteint")
  time.sleep(1)
```

Si l'on veut prendre en compte une valeur passée
de fréquence, cela deviendrait :

```
import time

freq = 1 # en Hz
t = 1/freq

clignote = True

while clignote:
  print ("allume")
  time.sleep(t/2)
  print ("eteint")
  time.sleep(t/2)
```

Disons que l'on veuille changer la fréquence quand l'utilisateur
tape une nouvelle valeur au clavier...
cette partie du code serait :

```
print("Entrez la fréquence")
freq = float(input());
```

Le problème est que je ne peux pas intégrer ces lignes dans la boucle :
l'attente de l'utilisateur bloque le clignotement.
Inversement, les *sleep* du clignotement pourraient empécher la réception des
arrivées de demande de changement de fréquence (pas dans le cas du clavier,
mais si cela venait du réseau, oui)

Le code qui suit **ne permet donc pas** de clignoter :
```
import time

freq = 1 # en Hz
t = 1/freq

clignote = True

while clignote:
  print ("allume")
  time.sleep(t/2)
  print ("eteint")
  time.sleep(t/2)

  print("Entrez la fréquence")
  freq = float(input());
```

Notre programme doit donc avoir deux parties :
- une qui clignote
- une qui attend.

Pour cela, nous allons utiliser des **Threads**

### Les Threads

Bon, on va dire que ce sont presque des processus qui s'exécutent
parallèlement dans un programme.

Commencons par créer une fonction qui clignote.
Cette fonction utilise les **variables globales** suivantes :
- clignote (boolean)
- freq (un float)

```
def clignoter():
  while clignote:
      t = 1/freq
      print ("allume")
      time.sleep(t/2)
      print ("eteint")
      time.sleep(t/2)
```

Mon programme principal va alors créer un thread
qui exécute cette fonction *clignoter*.
Le programme principal reste donc libre de faire autre chose...

On définit le thread à créer comme suit :
```
monThread = threading.Thread(target=clignoter)
```
On le lance comme cela.
```
monThread.start()
```

Voici donc un premier programme complet,
qui clignote, tout en affichant d'autres choses.

```
# -*- coding: utf-8 -*-
import time
import threading

def clignoter():
  while clignote:
      t = 1/freq
      print ("allume")
      time.sleep(t/2)
      print ("eteint")
      time.sleep(t/2)


freq = 0.5 # en Hz
clignote = True

monThread = threading.Thread(target=clignoter)
monThread.start()

while True:
     print("pg principal")
     time.sleep(2)
```

Ne lancez pas ce programme, vous auriez du mal a arrêter le thread...
Ajoutons donc quelques lignes pour que tout s'arrête proprement si on appuie
sur CTRL + C... Il suffit que si le programme principal s'arrête, la variable
*clignote* passe à *False*. Ainsi, la boucle du thread s’arrêtera et le thread
se terminera avec la fonction *clignoter*.

Voici le code du programme principal seul :

```
freq = 0.5 # en Hz
clignote = True

try:

    monThread = threading.Thread(target=clignoter)
    monThread.start()

    while True:
        print("pg principal")
        time.sleep(2)

except (KeyboardInterrupt, SystemExit):
    clignote = False
```

Il ne reste plus qu'a prendre en compte les choix de l'utilisateur,
c'est facile. Voici le code du programme complet :
```
# -*- coding: utf-8 -*-
import time
import threading

def clignoter():
  while clignote:
      t = 1/freq
      print ("allume")
      time.sleep(t/2)
      print ("eteint")
      time.sleep(t/2)

  print("j'arrete de clignoter")

freq = 0.5 # en Hz
clignote = True

try:

    monThread = threading.Thread(target=clignoter)
    monThread.start()

    while True:
         print("pg principal")
         print ("entrez la frequence souhaitee")
         freq = float(input())

except (KeyboardInterrupt, SystemExit):
    clignote = False
    print ("je sors du programme principal")
```

### Modification pour intégrer les Leds

On transforme ceci un petit peu...
Il suffit d'injecter le code de cligntement des leds dans notre fonction.
On pourrait faire ceci :
```
def clignoter():
  broche = 8
  GPIO.setmode(GPIO.BOARD)  
  GPIO.setup(broche, GPIO.OUT, initial=GPIO.LOW)

  while clignote:
      t = 1/freq

      GPIO.output(broche, GPIO.HIGH) # Turn on
      time.sleep(t/2)

      GPIO.output(broche, GPIO.LOW)  # Turn off
      time.sleep(t/2)

  print("j'arrete de clignoter")
```

Une remarque néanmoins :
Je souhaite que le numéro de broche soit choisi par le programme principal
(car potentiellement, je voudrais en faire clignoter plusieurs en meme temps).

C'est aussi le programme principal qui définira que cette broche est une broche
de sortie.

Je pourrais faire de broche une variable globale mais c'est moche
(et rendrait difficile d'en faire clignoter plusieurs en meme temps)

Je vais donc passer ce numéro de broche à ma fonction clignoter, qui devient :

```
def clignoter(broche):
  GPIO.setmode(GPIO.BOARD)  
  GPIO.setup(broche, GPIO.OUT, initial=GPIO.LOW)

  while clignote:
      t = 1/freq

      GPIO.output(broche, GPIO.HIGH) # Turn on
      time.sleep(t/2)

      GPIO.output(broche, GPIO.LOW)  # Turn off
      time.sleep(t/2)

  print("j'arrete de clignoter")
```

Il s'agit maintenant, pour le programme principal, de creer un thread
qui execute la fonction *clignoter* en lui passant le numéro de broche
comme argument.
Dans mon programme principal, je vais donc trouver ceci :

```
ledpin = 8
GPIO.setmode(GPIO.BOARD)                        # Use physical pin numbering
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)

try:

    monThread = threading.Thread(target=clignoter, args=(ledpin,))
    monThread.start()
```

Au final, voici le code complet :

```python
# -*- coding: utf-8 -*-
import time
import threading
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library


def clignoter(broche):

  while clignote:
      t = 1/freq

      GPIO.output(broche, GPIO.HIGH) # Turn on
      time.sleep(t/2)

      GPIO.output(broche, GPIO.LOW)  # Turn off
      time.sleep(t/2)

  print("j'arrete de clignoter")

freq = 0.5 # en Hz
clignote = True

ledpin = 8
GPIO.setmode(GPIO.BOARD)                        # Use physical pin numbering
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)

try:

    monThread = threading.Thread(target=clignoter, args=(ledpin,))
    monThread.start()

    while True:
         print("pg principal")
         print ("entrez la frequence souhaitee")
         freq = float(input())

except (KeyboardInterrupt, SystemExit):
    clignote = False
```

Le code complet du fichier PHP est ici : [../Sources/blinkLedThread.py](../Sources/blinkLedThread.py)
