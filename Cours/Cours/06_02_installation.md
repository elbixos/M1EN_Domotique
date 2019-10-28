## Installation de mosaik et des simulateurs

### Creation d'un environnement virtuel

```
python3 -m venv venv
venv\Script\activate
```

### Installation des packages dans cet environnement

```
pip install mosaik numpy scipy h5py
```

### Recupération des Sources

```
git clone https://git@bitbucket.org/mosaik/mosaik-demo.git
```

### Installation des packages supplémentaires
```
cd mosaik-demo/
pip install -r requirements.txt
```

### lancement de la démo
```
python demo.py
```
Pour visualiser la démonstration, le programme demo.py crée un serveur Web
qui écoute le port 8000 en local. Vous pouvez donc observer la démo en cours
avec votre navigateur à l'adresse [http://localhost:8000/](http://localhost:8000/)

Vous devriez voir quelque chose comme ceci :
![demo mosaik](demoMosaik.png)
