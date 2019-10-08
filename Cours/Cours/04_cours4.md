## Amélioration de la gestion des LED

### Introduction

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

### Code PHP

Reprenons le code précédent vu auparavant, que l'on adapte
puisque son nom est *useLed.php* et qu'il appelle le fichier
python *clientLed.py*. J'ai également ajouté un titre de niveau 1
dans la page page (Gestion de Led)

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
  <h1> Gestion de LED </h1>
  <form action="useLed.php" method="post">
    <button type="submit" id="submit" name="submit">Allumer</button>
  </form>

  <?php
  if (isset($_POST["submit"])){
      $command = escapeshellcmd('python3 clientLed.py');
      $output = shell_exec($command);

      echo "<p>";
      echo $output;
      echo </p>
  }
  ?>
</body>
</html>
```

Ajoutons dans le formulaire un champ pour la fréquence :

- On ajoute un paragraphe pour bien séparer les champs. Ceci grâce à la balise \<p\>,
- on ajoute un label pour écrire "Fréquence" devant le champ.
- on ajoute le champ *freq* pour que l'utilisateur puisse entrer
un nombre.

Voici le code du formulaire, qui remplace l'ancien :

```
<form action="useLed.php" method="post">

  <p>
    <label for="freq">Fréquence</label>
    <input type="number" name="freq" id="freq" />
 </p>
   <button type="submit" id="submit" name="submit">Clignoter</button>

</form>

```

On vérifie que l'affichage fonctionne :

![gestion Led 1](gestionLed1.png)


Ajoutons que le script Php doit récupérer la valeur de la fréquence
qu'il recoit du formulaire, et la transmettre au programme python qu'il lance.

Pour récuperer cette valeur, on regarde dans *\$_POST*
```
$frequence = $_POST["submit"]
```

Pour transmettre cela au programme python qu'on lance,
il faut que la commande devienne :
```
python3 clientLed.py $frequence
```

je vais changer les simples guillemets du programme précédent
par des doubles, ce qui va permettre a PHP de remplacer *\$frequence*
par sa valeur
```
<?php

if (isset($_POST["submit"])){
    $frequence = $_POST["submit"];

    $command = escapeshellcmd("python3 clientLed.py $frequence");
    $output = shell_exec($command);
```

Pour vérifier, on va faire un programme python *clientLed.py* tout bête qui
affiche la valeur du paramètre avec lequel il est lancé.

```
import sys

freq = sys.argv[1]
print ("Je suis python, vous voulez une fréquence de :", freq)
```

Ceci nous permettra d'avoir ce type de choses :

![gestion Led 2](gestionLed2.png)
### Un peu de style.

Rendons ceci plus joli : on va utiliser les Feuilles de styles (CSS) pour
améliorer visuellement notre formulaire.
C'est une bonne habitude de mettre les instructions de style dans
un fichier séparé du code HTML. Ce fichier s'appellera ici *styleM1.css*

Commencons par dire, dans le fichier PHP, que le navigateur doit récuperer
ce fichier pour la mise en page. Ceci se fait dans la balise *head*,
en ajoutant la ligne suivante :

```
 <link rel="stylesheet" href="styleM1.css" />
```

Je n'ai pas l'intention ici de faire un cours complet sur les CSS (c'est long),
juste de vous en apprendre quelques notions.
Dans un fichier css, on veut définir des **instructions de style** appliquer à certains **éléments** de la page HTML.

Les éléments sont choisis avec un **sélecteur**, comme par exemple le nom d'une
balise. Puis on définit la **valeur** d'une **propriété** pour ce sélécteur.

Par exemple : Si je veux mettre un fond noir sur toute ma page,
je dois selectionner la balise *body*, et donner à la propriété
*background-color* la valeur *black* (ou *#000000*).
Dans mon CSS, j'écrirais :
```
body
{
    background-color: black;  /* Le fond de la page sera noir */
}
```
En bricolant un peu (et en repompant des styles sur le net), on arrive à ceci :

![gestion Led CSS](gestionLedCSS.png)


Le code complet du fichier PHP est ici : [../Sources/useLed.php](../Sources/useLed.php)


Le code complet du fichier css est ici : [../Sources/styleM1.css](../Sources/styleM1.css)
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

## Les Sockets

### Principes : IP et ports

Ce que nous avons fait auparavant est une partie du programme
*serverLed.py* qui gère la led.
Il s'agit maintenant pour un autre programme (*clientLed.py*) de signaler
au programme *serverLed* qu'il faut qu'il change la fréquence.

Pour établir une communication entre deux programmes, nous pouvons utiliser
les **sockets** qui sont un moyen assez général de communiquer pour deux programmes, le plus souvent à travers le réseau.

Un programme qui tourne sur une machine, peut écouter les requêtes du réseau
en utilisant une interface réseau de cette machine (une carte réseau).
Comme plusieurs applications peuvent avoir besoin du réseau en même temps,
les communications seront associées à un numéro de port permettant de les trier.

Ainsi, la destination d'une communication est caractérisée par deux nombres :
- Le numéro IP de la machine hote (d'une de ses interfaces réseau)
- Le numéro de port associé à l'application.

Un certain nombre de numéro de ports ont une application associée par défaut.
Par exemple, si je contacte :
- la machine 192.168.1.17 sur le port 80, c'est son serveur web qui répondra (sans doute)
- la machine 192.168.1.17 sur le port 22, c'est son serveur ssh qui répondra (sans doute)
- la machine 192.168.1.17 sur le port 443, c'est son serveur web qui répondra en connexion sécurisée, https. (sans doute)

Le numéro de port est compris entre 0 et 65535 (il y en a donc un certain nombre !) et les numéros entre 0 et 1023 sont réservés par le système. On peut les utiliser, mais ce n'est pas une très bonne idée.

### premier serveur

Notre programme *serverLed.py* doit donc réquisitionner un port réseau
de la machine sur laquelle il tourne. J'ai choisi le port 10000.

Notre programme *serverLed.py* devra donc faire les choses suivantes.

Pour importer les modules utiles :

```python
import socket
import sys
```

Pour créer un objet *sock* gérant les connections
```python
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Pour attacher cette socket à un port :
```python
# Bind the socket to the port
server_address = ('', 10000)
print ('je démarre sur : ',server_address)
sock.bind(server_address)
```

Puis on dit au serveur de commencer à écouter (une seule connection
pour simplifier) :
```python
# Listen for incoming connections
sock.listen(1)
print ("waiting")
```

On va le mettre en attente d'une connection, ce qui va bloquer
le programme jusqu'à ce que quelqu'un se connecte :
```python
print 'waiting for a connection')
connection, client_address = sock.accept()
```

Si l'on passe cette ligne, on dispose d'une *connection* vers le client,
dont l'adresse est indiquée dans *client_adress*
Cette connection va nous permettre d'envoyer (*send*) et de recevoir (*recv*)
des informations.

Dans notre cas, pour simplifier, on va recevoir un paquet de données en provenance du client (de longueur max 256), transformée en chaine de charactere
de type utf8...

```python
data = connection.recv(256).decode("Utf8")
print ('received ', data)
```

Enfin, on pourra fermer la connection :
```
connection.close()
```

Voici donc le code de notre premier serveur :

```python
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10000)
print ('starting up on',server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print ("waiting")

print ('waiting for a connection')
connection, client_address = sock.accept()

print ('connection from', client_address)

data = connection.recv(256)
print ('received ',data)

connection.close()
```

Le code complet du serveur python est ici : [../Sources/server1.py](../Sources/server1.py)

### premier client

Le client doit lui aussi créer une socket,
```python
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Puis, il connecte sa socket au serveur
```python
# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print ('connecting to', server_address)
sock.connect(server_address)
```

Puis il peut envoyer des informations au serveur (ou en recevoir)
```python
message = 'hey, je parle dans une socket.'
print ('sending ' message)
sock.sendall(message)
```

Enfin, quand il a fini, il ferme la connection
```python
print ('closing socket')
sock.close()
```

Soit le programme complet suivant :
```python
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print ('connecting to', server_address)
sock.connect(server_address)

message = '99'
print ('sending ' message)
sock.sendall(message)

print ('closing socket')
sock.close()
```

Le code complet du client python est ici : [../Sources/client1.py](../Sources/client1.py)


### tests et améliorations

Le problème est que notre serveur s'arrete dès la fin de la première
connection. On voudrait que lorsqu'une connection se termine, il se remette
en attente d'une nouvelle...

Le code deviendrait :
```python
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 10000)
print ('starting up on',server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print ("waiting")

while True:
    print ('waiting for a connection')
    connection, client_address = sock.accept()

    print ('connection from', client_address)

    data = connection.recv(256)
    print ('received ',data)

    connection.close()
```
Le code complet du serveur python est ici : [../Sources/server2.py](../Sources/server2.py)

### Client : envoi du message de gestion de LED

Notre client est simple :
On le lance avec une ligne comme
```
python3 clientLed.py 3
```
qui indique la fréquence à laquelle faire clignoter la led.
Et il doit envoyer le message "clignote 3" au serveur.

Le code est le suivant :

```python
import socket
import sys

freq = sys.argv[1] # pour recuperer l'argument de frequence'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("127.0.0.1", 10000)
print ('connecting to port ', server_address)
sock.connect(server_address)

# Ici, j'ai ajoute un block try catch pour capter les problemes.
try:

    # Send data
    message = "clignote "+str(freq)
    print ('sending ', message)
    sock.sendall(message.encode("Utf8"))

except Exception as ex:
    print (ex)

finally:
    print ('closing socket')
    sock.close()
```

Le code complet du client python est ici : [../Sources/clientLed.py](../Sources/clientLed.py)

### Serveur : Ajoutons de quoi gérer la LED
Je ne fais ici que mixer la partie Socket avec la partie
Threads vue auparavant.

La seule nouveauté consistera a éclater le message reçu (par exemple,
"clignote 3" en deux parties :
- la chaine "clignote" qui est un ordre
- la fréquence 3 qui doit être convertie en float.


Ce découpage de chaine de caractère sera fait par la fonction *split*.
On aura donc quelque chose comme :
```python
data = connection.recv(256).decode("Utf8")

dataSplit = data.split()
ordre = dataSplit[0]
freq = float(dataSplit[1]) # en Hz
```

Voici le code complet du serveur :

```python
import socket
import sys


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

ledpin = 8
GPIO.setmode(GPIO.BOARD)                        # Use physical pin numbering
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)
clignote = False

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ("127.0.0.1", 10000)
print ('starting up on port',server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print ("waiting")

while True:
  print ('waiting for a connection')
  connection, client_address = sock.accept()

  try:
    print ('connection from', client_address)

    data = connection.recv(256).decode("Utf8")
    print ('received ', data)

    dataSplit = data.split()
    ordre = dataSplit[0]
    print(ordre)
    freq = float(dataSplit[1]) # en Hz
    print ("frequence", freq)

    if clignote == False :
        clignote = True

        monThread = threading.Thread(target=clignoter, args=(ledpin,))
        monThread.start()

  except Exception as ex:
    print (ex)
    clignote = False
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

  finally:

    # Clean up the connection
    connection.close()
```

Le code complet du serveur python est ici : [../Sources/serverLed.py](../Sources/serverLed.py)

### Ajoutons un moyen d'éteindre la led

Il suffit d'ajouter un ordre possible au client...
L'ordre d'extinction. Lorsque le serveur recoit cet
ordre, il éteint la LED.

Il va falloir aussi modifier la page PHP
pour permettre d'envoyer l'ordre.
Ceci peut être fait en ajoutant un autre bouton submit
au formulaire.
On aura
- un bouton de type submit, nommé "clignote" qui devra déclencher le clignotement
- un bouton de type submit, nommé "eteindre" qui devra déclencher l'extinction

Voici le nouveau formulaire :
```html
<form action="useLed.php" method="post">

  <p>
    <label for="freq">Fréquence</label>
    <input type="number" name="freq" id="freq" />
 </p>
   <button type="submit" id="clignote" name="clignote">Clignoter</button>
   <button type="submit" id="eteindre" name="eteindre">Eteindre</button>

</form>
```
Ensuite, si l'utilisateur a cliqué sur "Clignote"
le script php va lancer la commande
```
python3 clientLed2.py clignote $frequence
```
Si l'utilisateur a cliqué sur "Eteindre", le script php va lancer
```
python3 clientLed2.py eteindre
```

Pour cela, le code php est maintenant :
```
<?php
  if (isset($_POST["clignote"]) || isset($_POST["eteindre"])){
	   if (isset($_POST["clignote"])){
        $frequence = $_POST["freq"];
	      $command = escapeshellcmd("python3 clientLed2.py clignote $frequence");
        $output = shell_exec($command);
	   }
     else {
          $command = escapeshellcmd("python3 clientLed2.py eteind");
     }

     echo "<p>";
	   echo "commande envoyee :";
	   echo $command;

     $output = shell_exec($command);
     echo $output;
     echo "</p>";
  }
?>
```

Le client python doit simplement relayer la commande au serveur.
Son code n'a pas changé

Le serveur python à un peu changé dans la gestion de la commande reçue.
Lors de la réception de la commande du client, voici le code :
```python
    data = connection.recv(256).decode("Utf8")
    print ('received ', data)

    dataSplit = data.split()
    ordre = dataSplit[0]
    print(ordre)
    if ordre == "clignote":
        print ("demande de clignotement")
        freq = float(dataSplit[1]) # en Hz
        print ("frequence", freq)

        if clignote == False :
            clignote = True

            monThread = threading.Thread(target=clignoter, args=(ledpin,))
            monThread.start()
    else :
        print ("demande d'extinction")
        clignote = False
        GPIO.output(ledpin, GPIO.LOW)  # Turn off
```
Tout ceci se comprend plus ou moins aisément...

Le code complet du script php est ici :
[../Sources/useLed2.php](../Sources/useLed2.php)

Le code complet du client python est ici : [../Sources/clientLed.py](../Sources/clientLed2.py)

Le code complet du serveur python est ici : [../Sources/serverLed.py](../Sources/serverLed2py)

### Déportons le serveur sur une autre machine

Les sockets nous permettent de placer notre serveur qui fait clignoter
la led sur une autre machine que celle qui gère le serveur Web.
Il suffit de changer le numéro IP de la machine à contacter par le client.

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

___
Vous pouvez repartir vers le [Sommaire](99_sommaire.md)

___
