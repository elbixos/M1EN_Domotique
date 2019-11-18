# simulator_mosaik.py
"""
Mosaik interface for the example simulator.

"""
import mosaik_api

META = {
    'models': {
        'ModelOdC': {
            'public': True,
            'params': [''],
            'attrs': ['Iequilibre', 'Oconsommation'],
        },
        'ModelBC': {
            'public': True,
            'params': [''],
            'attrs': ['Oconsommation'],
        },
        'ModelBP': {
            'public': True,
            'params': [''],
            'attrs': ['Oproduction'],
        },
        'ModelCA': {
            'public': True,
            'params': [''],
            'attrs': ['Iequilibre', 'Iproduction','Iconsommation','Icharge','Ocharge','Oproduction', 'Oconsommation'],
        },
        'Batterie': {
            'public': True,
            'params': [''],
            'attrs': ['Ocharge', 'Icharge'],
        }

    },
}

import random

class ModelCA:
    def __init__(self):
        self.Iequilibre = 0
        self.Oproduction = 0
        self.Oconsommation = 0
        self.Iproduction = 0
        self.Iconsommation = 0
        self.Icharge = 0
        self.Ocharge = 0



    def step(self, time):
        """Perform a simulation step by adding *delta* to *val*."""
        diff = self.Iproduction-self.Iconsommation
        if diff <0 : #Trop de consommation
            if -diff<self.Icharge: # il y a plus de batterie que d energie necessaire
                diff = 0 #plus d energie necessaire
                self.Ocharge = diff #on decharge la batterie de diff (negatif)
            else: #il y a moins de batterie que d energie necessaire
                diff = diff+self.Icharge #on reduit l'energie necessaire
                self.Ocharge = -self.Icharge # on décharge toute la batterie
            self.Oconsommation = -diff # on consomme le restant sur le reseau
            self.Oproduction = 0
        else: #trop de production
            self.Oconsommation = 0 #on ne consomme rien sur le reseau
            if self.Iequilibre>0: #si le reseau n'a pas besoin d energie
                self.Ocharge = diff # on charge la batterie
            else: #si le reseau a besoin d energie
                self.Ocharge = 0 #on ne charge pas la batterie
            self.Oproduction = diff-self.Ocharge #on envoie sur le reseau ce qu il reste (0 ou diff)


        #print('ModeleBC Step - Iequilibre : %f - Oconsommation : %f' %(Iequilibre, self.Oconsommation))

class Batterie:
    def __init__(self):
        self.Icharge = 0
        self.Ocharge = 0


    def step(self, time):
        """Perform a simulation step by adding *delta* to *val*."""
        self.Ocharge = max(self.Ocharge+self.Icharge, 0)
        #print('ModeleBat Step - Iequilibre : %f - Oconsommation : %f' %(Iequilibre, self.Oconsommation))


class ModelBC:
    def __init__(self,start=0, datafile=None):
        self.Oconsommation = 0


    def step(self, time):
        """Perform a simulation step by adding *delta* to *val*."""
        self.Oconsommation = random.random()
        #print('ModeleBC Step - Iequilibre : %f - Oconsommation : %f' %(Iequilibre, self.Oconsommation))


class ModelBP:
    def __init__(self,start=0,datafile=None):
        self.Oproduction = 0


    def step(self, time):
        """Perform a simulation step by adding *delta* to *val*."""
        self.Oproduction = random.random()
        #print('ModeleBC Step - Iequilibre : %f - Oproduction : %f' %(Iequilibre, self.Oproduction))


class ModelOdC:
    def __init__(self):
        self.Iequilibre = 0
        self.Oconsommation = 0


    def step(self, time):
        """Perform a simulation step by adding *delta* to *val*."""
        if self.Iequilibre >= 0:
            self.Oconsommation = random.random()
        #print('ModeleOdC Step - Iequilibre : %f - Oconsommation : %f' %(Iequilibre, self.Oconsommation))


class simulateur(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META) # ou super().__init__(META) ou mosaik_api.Simulator.__init__(META)
        self.entites = []
        self.entities = {}
        self.eid_prefix = 'Model_'

    def init(self, sid, eid_prefix=None):
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.entities)
        entities = []
        print('On cree %d %s' % (num,model))
        for i in range(next_eid, next_eid + num):
            if model == 'ModelOdC':
                eid = '%s%s%d' % (self.eid_prefix, 'OdC',i)
                entite = ModelOdC()
            if model == 'ModelBC':
                eid = '%s%s%d' % (self.eid_prefix, 'BC', i)
                entite = ModelBC()
            if model == 'ModelBP':
                eid = '%s%s%d' % (self.eid_prefix, 'BP', i)
                entite = ModelBP()
            if model == 'ModelCA':
                eid = '%s%s%d' % (self.eid_prefix, 'CA', i)
                entite = ModelCA()
            if model == 'Batterie':
                eid = '%s%s%d' % (self.eid_prefix, 'BAT', i)
                entite = Batterie()

            self.entites.append(entite)
            self.entities[eid] = i
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs):
        # Get inputs
        if inputs != {}:
            for eid, attrs in inputs.items():
                #eid : id de l'entite destination concernee
                model_idx = self.entities[eid]
                Iequilibre = Iconsommation = Iproduction = Icharge = 0
                for attr, values in attrs.items(): #attr : l'attribut, values : les valeurs sous la forme liste de ('src':val)
                    if attr=='Iequilibre':
                        self.entites[model_idx].Iequilibre = sum(values.values()) # a priori il n'y a qu'une seule valeur provenant du dispatcher
                    if attr == 'Iconsommation':
                        self.entites[model_idx].Iconsommation = sum(values.values())
                    if attr == 'Iproduction':
                        self.entites[model_idx].Iproduction = sum(values.values())
                    if attr == 'Icharge':
                        self.entites[model_idx].Icharge = sum(values.values())
                    #print('Simulateur ODC Step %d - Src : %s - val : %f' %(time,values.keys,Iequilibre))
                self.entites[model_idx].step(time)
        else:
            for entite in self.entites:
                entite.step(time)

        return time + 60  # Step size is 1 minute

    def get_data(self, outputs):
        print('Outputs:%s' %outputs)
        models = self.entites
        data = {}
        for eid, attrs in outputs.items():
            model_idx = self.entities[eid]
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ModelCA']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                # Get model.val or model.delta:
                data[eid][attr] = getattr(models[model_idx], attr)

        return data
