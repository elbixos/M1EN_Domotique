# Smartgrids TP1

Dans ce TP, nous allons prendre en main le simulateur de Smartgrids, pour essayer de mettre un peu de smart dedans...

Toute l'installation doit déja être faite,
et la démonstration de mosaik doit fonctionner.

## Les éléments d'une simulation

Dans une simulation, nous allons avoir différentes **entités**
placées dans la grille. Voyons un peu les entités en présence.

### Les entités correspondant à des objets physiques

Nous avons plusieurs types d'acteurs.

#### Les entités de base :

##### Les **Profils**

Tout d'abord, nous avons des acteurs "aveugles"
- des Consommateurs aveugles, qui demandent à consommer sans se préoccuper de ce que veut le réseau.
- des Producteurs aveugles, qui produisent sans se préoccuper de ce que veut le réseau.

Pour rendre la chose plus réaliste et plus répétable, l'activité de ces acteurs est stockée dans un fichier de **profil**.
Nous avons ainsi un fichier [../Sources/ModelSimple/data/profileC.csv](../Sources/ModelSimple/data/profileC.csv) correspondant à une consommation standard, et un fichier [../Sources/ModelSimple/profileP.csv](../Sources/ModelSimple/data/profileP.csv) correspondant à une production spécifique.

##### La **Batterie**
C'est une entité capable de stocker une certaine quantité d'énergie, et de la restituer à la demande.

#### Le **Dispatcher**

Dans notre réseau, c'est cet élément qui connecte entre eux les entitées pour leur fournir de l'énergie.
Il a pour objectif de collecter toutes les Consommation demandées,
toutes les Production proposées et de mesurer l'écart entre les deux.

#### Le **ConsomActor**

Ce sera l'objet de notre étude :
C'est un sous réseau qui a un certain **profil de consommation**,
un certain **profil de production** ainsi qu'une **batterie**.

Cette entité est donc connectée à trois entités de base :
- un consommateur aveugle
- un producteur aveugle
- une batterie

Le ConsomActor devra être en mesure de choisir des stratégies
- pour fournir l'energie à son consommateur,
- utiliser l'énergie de son producteur

Il pourra pour cela :
- charger ou décharger sa batterie
- demander ou donner de l'énergie à son Dispatcher.

### L'entité de visualisation.

Nous souhaitons de plus visualiser l'activité de chacune de ces entités lors de la simulation. La visualisation se fait à l'aide d'un navigateur web.
Pour cela, nous disposons d'une autre entité, (*webvis*) dans notre code, à laquelle chaque entité est connectée pour lui transmettre les informations concernant son activité.

## Premier programme

Pour débuter, commencons par regarder le contenu
du fichier [../Sources/ModelSimple/TP1_0.py](../Sources/ModelSimple/TP1_0.py).

### Objectifs

Nous allons créer un réseau simplissime, contenant
- 1 Dispatcher.
- 1 Consommateur aveugle, dont le profil est déterministe.
- 1 Producteur aveugle, dont le profil est déterministe.

### Les imports
Voici le tout début du programme, qui importe les modules nécessaires.

```python
# demo_1.py
import mosaik
import mosaik.util
import webbrowser
import random

from mosaik.util import connect_randomly, connect_many_to_one
```
### La configuration de la simulation
Puis quelques éléments de configuration
```python
# Sim config. and other parameters
SIM_CONFIG = {
    'SimulateurModels': {
        'python': 'simulateurModeles:simulateur',
    },
    'Dispatcher': {
        'python': 'simulateurDispatcher:SDispatcher',
    },
    'WebVis': {
        'cmd': 'mosaik-web -s 0.0.0.0:8000 %(addr)s',
    },
    'Collector': {
        'cmd': 'python collector.py %(addr)s',
    },
    'CSV': {
        'python': 'mosaik_csv:CSV',
    },
    'DB': {
        'cmd': 'mosaik-hdf5 %(addr)s',
    },

}
START = '2014-01-01 00:00:00'
END = 31 * 24 * 3600  # 10 minutes
PROFILE_P = 'data/profileP.csv'
PROFILE_C = 'data/profileC.csv'
```

### Le Main
Vient ensuite la fonction **main** qui contiend notre programme principal.

```python
def main():

    random.seed(23)
    # Create World
    world = mosaik.World(SIM_CONFIG)
```
Ici, nous venons de figer la graine aléatoire (à 23) pour que la simulation soit identique à chaque lancement.

#### Simulateurs en charge des entités.
Créons maintenant quelques simulateurs pour nos entités.

```python
    # Start simulators
    factoryDispatcher = world.start('Dispatcher')
    factoryProfileP = world.start('CSV', sim_start=START, datafile=PROFILE_P)
    factoryProfileC = world.start('CSV', sim_start=START, datafile=PROFILE_C)
```
 Ces éléments ne sont pas les entités, mais les simulateurs qui les gèrent. Ainsi, le *factoryDispatcher* sera en charge des *Dispatcher*.

#### Les entités
A partir de ces simulateurs (les *factory*), nous pouvons créer
des entités. Créons donc un *Dispatcher*, un *Consommateur Aveugle* et un *Producteur Aveugle*

```python
entiteDispatcher = factoryDispatcher.ModelDispatcher()

#creation des noeuds
entitePP = factoryProfileP.ModelProfil()  # .create(1)
entitePC = factoryProfileC.ModelProfil()  # .create(1)
```

#### Connection des entités entre elles

Connectons tout ce monde là comme il faut.
- La puissance (**P**) fournie par le Producteur **entitePP**
est connectée à la production en entrée **Iproduction** du Dispatcher **entiteDispatcher**.
- La puissance (**P**) demandée par le Consommateur **entitePC**
est connectée à la consommation en entrée **Iconsommation** du Dispatcher **entiteDispatcher**.


```python
world.connect(entitePP, entiteDispatcher, ('P', 'Iproduction'))
world.connect(entitePC, entiteDispatcher, ('P', 'Iconsommation'))
```
A chaque étape, le Dispatcher calculera son équilibre (**Oequilibre**) résultant de la différence entre production et consommation.


#### Visualisation

Créons maintenant l'entité de visualisation
et récupérons sa topologie (c'est comme cà...)

```python
   webvis = world.start('WebVis', start_date=START, step_size=60)
   webvis.set_config(ignore_types=['Topology', 'ResidentialLoads', 'Grid', 'Database'])
   vis_topo = webvis.Topology()
```

Puis connectons nos entités à la visualisation.

```python
# On connecte les noeuds a la visualisation web
world.connect(entiteDispatcher, vis_topo, 'Oequilibre')
world.connect(entitePP, vis_topo, 'P')
world.connect(entitePC, vis_topo, 'P')
```

Enfin, il faut spécifier, pour la visualisation, quels sont les attributs a visualiser. Par exemple, pour les profils, on regarde l'attribut **P** de puissance (consommée ou produite)

```python
webvis.set_etypes({
    'ModelProfil': {
        'cls': 'load',
        'attr': 'P',
        'unit': 'P.',
        'default': 0,
        'min': -1000,
        'max': 1000,
    }, })
```
Pour les Dispatchers, on observe l'équilibre
```python
webvis.set_etypes({
    'ModelDispatcher': {
        'cls': 'load',
        'attr': 'Oequilibre',
        'unit': 'Equ.',
        'default': 0,
        'min': -3000,
        'max': 3000,
    },})
```

Enfin, on ouvre le navigateur pour observer la visualisation Web et on lance la simulation comme suit :
```python

    webbrowser.open('http://localhost:8000')
    # Run simulation
    world.run(until=END)
```

Ceci devrait vous donner quelque chose comme ceci (et nous sommes contents).

![image TP1_0](TP1_0.png)

## Second programme

Copiez le code de *TP1_0.py* dans un second fichier (*TP1_1.py*) dans lequel nous allons travailler.

### Objectifs

Nous allons créer un réseau un peu plus complexe, contenant
- 1 Dispatcher.
- 1 ConsomActeur relié à :
    - 1 Consommateur aveugle, dont le profil est déterministe.
    - 1 Producteur aveugle, dont le profil est déterministe.
    - 1 Batterie controlable

Il s'agira ici de définir une stratégie pour notre ConsomActor, lui permettant
de réguler sa consommation, et de voir ce qu'il se passe pour le Dispatcher.

### Récupération des factoryModels.

A partir du programme précédent, nous disposons déja des factoryModels
correspondant à :
- 1 consommateur Aveugle
- 1 producteur Aveugle
- 1 Dispatcher

Il nous manque les factorymodels correspondant aux :
- ConsomActeur
- Batterie

Il va donc falloir ajouter les lignes suivantes à notre programme
(je vous laisse trouver où...)

L'ensemble des modèles des entités standard (comme le ConsomActor ou la batterie)
est dans un fichier nommé *SimulateurModels.py*. Pour des raisons pratiques,
nous allons créer 2 factorymodels pour creer respectivement nos 2 types d'entités.

```python
factoryModeles = world.start('SimulateurModels')
factoryBat = world.start('SimulateurModels')
```

#### Les entités

Demandons donc à chaque factorymodel de nous créer une entité.
Comme précédemment, voici les lignes à insérer, à vous de comprendre
pourquoi, et où !

On demande un ConsomActor à *factoryModeles* et une Batterie à *factoryBat*

```python
entiteCA = factoryModeles.ModelCA()
batterie = factoryBat.Batterie()
```

#### Connection des entités entre elles

Ca se complique. Il faut connecter :
- le profil de consommation au ConsomActor
- le profil de production au ConsomActor
- la batterie au ConsomActor

```python
world.connect(entitePP, entiteCA, ('P', 'Iproduction'))
world.connect(entitePC, entiteCA, ('P', 'Iconsommation'))
world.connect(batterie, entiteCA, ('Ocharge', 'Icharge'))
```

A chaque étape de la simulation, la batterie va envoyer au ConsomActor sa charge (Ocharge pour la batterie. Le ConsomActor recoit cette information dans Icharge).

Le ConsomActor devant commander la charge de la batterie,
on le connecte également à la batterie.
Son coefficient Ocharge correspond à son ordre à la batterie, que celle si recoit sur son propre Icharge... Si ce chiffre est positif, il demande à la batterie de se charger de la quantité correspondante.
Si ce chiffre est négatif, il demande à la batterie de se décharger de cette quantité.

```python
world.connect(entiteCA, batterie, ('Ocharge', 'Icharge'), time_shifted=True, initial_data={'Ocharge': 10})
```

Enfin, nous pouvons connecter le ConsomActor au Dispatcher.
Le ConsomActor doit préciser sa consommation au Dispatcher.
Dans l'autre sens, le Dispatcher doit préciser l'équilibre qu'il
à atteint au ConsomActor pour que celui ci puisse s'y adapter s'il le souhaite.

```python
world.connect(entiteCA, entiteDispatcher, ('Oconsommation','Iconsommation'),('Oproduction','Iproduction'))
world.connect(entiteDispatcher, entiteCA, ('Oequilibre','Iequilibre'), time_shifted=True, initial_data={'Oequilibre': 0})


```

#### Visualisation

Enfin, on connecte tout le monde à la visualisation

```python
world.connect(entiteDispatcher, vis_topo, 'Oequilibre')
world.connect(entiteCA, vis_topo, 'Oconsommation')
world.connect(entitePP, vis_topo, 'P')
world.connect(entitePC, vis_topo, 'P')
world.connect(batterie, vis_topo, 'Ocharge')
```

Et on paramètre les visualisations qui manquent :
```python
webvis.set_etypes({
    'Batterie': {
        'cls': 'load',
        'attr': 'Ocharge',
        'unit': 'Charge',
        'default': 0,
        'min': 0,
        'max': 100,
    }, })
webvis.set_etypes({
    'ModelCA': {
        'cls': 'load',
        'attr': 'Oconsommation',
        'unit': 'Conso.',
        'default': 0,
        'min': 0,
        'max': 100,
    }, })
```

Si on lance cette simulation, on obtient quelque chose comme ceci :
![visu TP1_1](TP1_1.png)

Bon... je teste et on verra après pour définir la stratégie du ConsomActor...
