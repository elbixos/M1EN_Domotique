# models.py
"""
This module contains a simple example simulator.

"""
import random


class dataIn:
    """Input Data for each node (element/model)"""
    def __init__(self):
        self.equilibre = 0
        self.reportPerc = 0
        self.byingPrice = 0
        self.sellingPrice = 0

class Profile:
    """ Comportement  aléatoire """
    RAND = 0
    """ Comportement périodique type habitation(soir / matin) """
    PERIODHOME = 1
    """ Comportement périodique type boulot(journée) """
    PERIODWORK = 2
    """ Comportement régulier par jour """
    REGULAR = 3
    """ Comportement spécifique """
    OWN = 4
    """ Aucun profil """
    NONE = 5
    """ Faible producteur / consommateur """
    low = 0
    """ Gros producteur / consommateur """
    high = 1

    behaviourString = ["Rand", "PeriodHome", "PeriodWork", "Regular", "Own"]

    def __init__(self, nbWeeks = 1, nbStepsPerDay = 24, behaviour=NONE):
        #Niveau de consommation ou de production
        self.level = 0
        self.behaviour = behaviour
        #Consomation max
        self.MaxConso = 10
        # Energie evolution
        self.energy = []
        #Current time
        self.currentTime = 0
        self.nbWeeks = nbWeeks
        self.nbStepsPerDay = nbStepsPerDay
        self.id = 0
        self.delta = 24 / nbStepsPerDay
        self.name = "P:"+behaviourString[behaviour]+str(id)
        initProfile()

    """
    val : valeur a mettre
    day : le jour de la simulation (commence à 0)
    HDebut : heure de debut
    HFin : heure de fin"""
    def setEnergie(self, val, week, day, HDebut, HFin):
        nbstep = floor(HFin/self.delta)-ceil(HDebut/self.delta)+1
        for step in range(nbstep)+ceil(HDebut/self.delta):
            energie[week * 7 * this.nbStepsPerDay + day * this.nbStepsPerDay + step] = val

    def initProfile(self, behaviour):
        if behaviour == RAND :
            for i in range(self.nbStepsPerDay*self.nbWeeks):
                energie[i] = random()*Self.MaxConso
        if behaviour == REGULAR :
            for w in range(nbWeeks):
                for d in range(7):
                    val = random()*MaxConso # Une valeur differente par jour
                    setEnergie(val, w, d, 0, 24)
        if bahaviour == PERIODHOME :
            for w in range(nbWeeks):
                for d in range(5):
                    # Tirage des heures de début et de fin le matin et le soir
                    X = 2
                    matinDebut = 6 + ronde(random()*2*X-X) # +/- XH autour de 6H
                    matinFin = 9 + ronde(random()*2*X-X) # +/- XH autour de 9H
                    soirDebut = 18 + ronde(random()*2*X-X) # +/- XH autour de 18H
                    soirFin = 22 + ronde(random()*2*X-X) # +/- XH autour de 22H
                    val = random()*MaxConso # Valeur matin
                    setEnergie(val, w, d, matinDebut,matinFin) # Consommation ou production de 6H à 9H
                    val = random()*MaxConso; # Valeur soir
                    setEnergie(val, w, d, soirDebut,soirFin) # Consommation ou production de 18H à 22H
                for d in range(2)+4: # Samedi Dimanche
                    val = random()*MaxConso # Une valeur differente par jour
                    for step in range(nbStepsPerDay):
                        setEnergie(val, w, d, 6, 22)
        if behaviour == PERIODWORK :
            for w in range(nbWeeks):
                for d in range(5):
                    val = random()*MaxConso # Valeur matin
                    setEnergie(val, w, d, 9,18) #Consommation ou production de 6H à 9H
        if behaviour == OWN :
            print 'A implementer'
        if 	bahaviour == NONE :
            for w in range(nbWeeks):
                for d in range(5):
                    setEnergie(0, w, d, 0,24) #Consommation ou production de 6H à 9H

class energyExchange:
    """Energy exchanged between network and node (element/model)"""
    def __init__(self):
        self.consumption = 0
        self.production = 0

class Model:
    """Model base class"""
    def __init(self, num, profile=[]):
        self.profile = profile   # Consumtion/Production profil [t,val(t)]
        self.num = num
        self.time = 0

class ModelBC(Model):
    """Blind Consummer"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        if empty(profile):
            energy.consumption = random.random()
        else:
            energy.consumption = self.profile[time]  # random.random()
        energy.production = 0
        self.time += 1
        return energy


class ModelBP(Model):
    """Blind Producer"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        if empty(profile):
            energy.production = random.random()
        else:
            energy.production = self.profile[self.time]  # random.random()
        energy.consumption = 0
        self.time += 1
        return energy

class ModelOdC(Model):
    """ On Demand Consumer"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        # Add Code here
        if data.Equilibre > 0:
            if empty(profile):
                energy.production = random.random()
            else:
                energy.production = self.profile[self.time]  # random.random()

        self.time += 1
        return energy

class ModelOdP(Model):
    """ On Demand Producer"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        # Add Code here
        time += 1
        return energy

class ModelSC(Model):
    """ Smart consumer, effacement + report"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        # Add Code here
        time += 1
        return energy

class ModelBBP(Model):
    """ Battery Best Price"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        # Add Code here
        time += 1
        return energy


class ModelCA(Model):
    """ CunsumActor, you are free"""

    def __init__(self, num, profile=[]):
        Model.__init__(self, num, profile)

    def step(self, data):
        """Perform a simulation"""
        energy = energyExchange()
        # Add Code here
        time += 1
        return energy


class SimulatorBC(object):
    """Simulates a number of ``Model`` models and collects some data."""

    def __init__(self):
        self.models = []
        self.data = []

    def add_model(self, nb):
        """Create an instances of ``Model`` with *init_val*."""
        model = ModelBC(nb)
        self.models.append(model)
        self.data.append([])  # Add list for simulation data

    def step(self, deltas=None):
        """Set new model inputs from *deltas* to the models and perform a
        simulatino step.

        *deltas* is a dictionary that maps model indices to new delta values
        for the model.

        """
        if deltas:
            # Set new deltas to model instances
            for idx, delta in deltas.items():
                self.models[idx].delta = delta
        data = dataIn()

        # Step models and collect data
        for i, model in enumerate(self.models):
            energy = model.step(data)
            print('{2}-P:{0},C={1}'.format(energy.production, energy.consumption, model.num))
            self.data[i].append([model.num, energy.consumption, energy.production])


if __name__ == '__main__':
    # This is how the simulator could be used:
    sim = Simulator()
    for i in range(5):
        sim.add_model(i)
    sim.step()

    sim.step({0: 23, 1: 42})
    print('Simulation finished with data:')
    for i, inst in enumerate(sim.data):
        print('%d: %s' % (i, inst))
