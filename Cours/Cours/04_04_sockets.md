
### Les Sockets

Ce que nous avons fait auparavant est une partie du programme
*serverLed.py* qui gère la led.
Il s'agit maintenant pour un autre programme (*clientLed.py*) de signaler
au programme *serverLed* qu'il faut qu'il change la fréquence.

Pour établir une communication entre deux programmes, nous pouvons utiliser
les **sockets** qui sont un moyen assez général pour deux programmes,
de discuter (éventuellement à travers le réseau).

Je ferais l'explication sous peu, mais en attendant :

Le code complet du client PHP est ici : [../Sources/clientLed.py](../Sources/clientLed.py)

Le code complet du serveur PHP est ici : [../Sources/serverLed.py](../Sources/serverLed.py)
