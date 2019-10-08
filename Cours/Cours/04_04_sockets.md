
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
