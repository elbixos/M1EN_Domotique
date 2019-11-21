
import random
import csv
from datetime import datetime, date, time, timedelta

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
        self.energie = []
        #Current time
        self.currentTime = 0
        self.nbWeeks = nbWeeks
        self.nbStepsPerDay = nbStepsPerDay
        self.id = 0
        self.delta = 24 / nbStepsPerDay
        self.name = "P:"+self.behaviourString[self.behaviour]+str(id)
        self.initProfile(self.behaviour)

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
        self.behaviour = behaviour
        self.energie = []
        if self.behaviour == self.RAND:
            for i in range(self.nbStepsPerDay*self.nbWeeks*7):
                self.energie.append(random.random()*self.MaxConso)
        if self.behaviour == self.REGULAR :
            for w in range(nbWeeks):
                for d in range(7):
                    val = random.random()*self.MaxConso # Une valeur differente par jour
                    self.setEnergie(val, w, d, 0, 24)
        if self.behaviour == self.PERIODHOME :
            for w in range(nbWeeks):
                for d in range(5):
                    # Tirage des heures de début et de fin le matin et le soir
                    X = 2
                    self.matinDebut = 6 + ronde(random.random()*2*X-X) # +/- XH autour de 6H
                    self.matinFin = 9 + ronde(random.random()*2*X-X) # +/- XH autour de 9H
                    self.soirDebut = 18 + ronde(random.random()*2*X-X) # +/- XH autour de 18H
                    self.soirFin = 22 + ronde(random.random()*2*X-X) # +/- XH autour de 22H
                    self.val = random.random()*self.MaxConso # Valeur matin
                    self.setEnergie(val, w, d, self.matinDebut,self.matinFin) # Consommation ou production de 6H à 9H
                    self.val = random.random()*self.MaxConso; # Valeur soir
                    self.setEnergie(self.val, w, d, self.soirDebut,self.soirFin) # Consommation ou production de 18H à 22H
                for d in range(2)+4: # Samedi Dimanche
                    self.val = random.random()*self.MaxConso # Une valeur differente par jour
                    for step in range(self.nbStepsPerDay):
                        self.setEnergie(self.val, w, d, 6, 22)
        if self.behaviour == self.PERIODWORK :
            for w in range(self.nbWeeks):
                for d in range(5):
                    self.val = random.random()*self.MaxConso # Valeur matin
                    self.setEnergie(val, w, d, 9,18) #Consommation ou production de 6H à 9H
        if self.behaviour == self.OWN :
            print('A implementer')
        if 	self.behaviour == self.NONE :
            for w in range(nbWeeks):
                for d in range(5):
                    self.setEnergie(0, w, d, 0,24) #Consommation ou production de 6H à 9H

    """ START_DATE doit etre de type datetime"""
    def exportCSV(self, START_DATE, step_size, filename='profile', modelname='ModelProfil'):
        with open(filename, mode='w',newline='') as profile_file:
            fieldnames = ['Date', 'P']
            profile_writer = csv.writer(profile_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #DictWriter(profile_file, fieldnames=fieldnames)
            profile_writer.writerow([modelname])
            #profile_writer.writeheader()
            profile_writer.writerow(fieldnames)
            #profile_writer.writerow('[Profile-%s'%self.behaviourString[self.behaviour]])
            t = 0
            for e in self.energie:
                date = START_DATE + timedelta(minutes=(step_size*t))
                d = '%s' %date.strftime("%Y-%m-%d %H:%M:%S")
                v = '%f' %e
                profile_writer.writerow([d,v])
                t += 1