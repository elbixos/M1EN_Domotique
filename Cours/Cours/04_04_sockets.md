
### Les Sockets

Ce que nous avons fait auparavant est une partie du programme
*serverLed.py* qui gère la led.
Il s'agit maintenant pour un autre programme (*clientLed.py*) de signaler
au programme *serverLed* qu'il faut qu'il change la fréquence.

Pour établir une communication entre deux programmes, nous pouvons utiliser
les **sockets** qui sont un moyen assez général pour deux programmes,
de discuter (éventuellement à travers le réseau).

Je ferais l'explication sous peu, mais en attendant :

Le code complet du client python est ici : [../Sources/clientLed.py](../Sources/clientLed.py)

Le code complet du serveur python est ici : [../Sources/serverLed.py](../Sources/serverLed.py)

# Ajoutons un moyen d'eteindre la led

Il suffit d'ajouter un ordre possible au client...
L'ordre d'extinction. Lorsque le serveur recoit cet
ordre, il eteint la LED.

Il va falloir aussi modifier la page PHP
pour permettre d'envoyer l'ordre.
Ceci peut être fait en ajoutant un autre bouton submit
au formulaire.
On aura
- un bouton de type submit, nommé "clignote" qui devra déclencher le clignotement
- un bouton de type submit, nommé "eteindre" qui devra déclencher l'extinction

Voici le nouveau formulaire :
```
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
```

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
