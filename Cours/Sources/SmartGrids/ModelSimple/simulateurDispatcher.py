# simulator_mosaik.py
"""
Mosaik interface for the example simulator.

"""
import mosaik_api




META = {
    'models': {
        'ModelDispatcher': {
            'public': True,
            'params': [''],
            'attrs': ['Oequilibre', 'Iproduction','Iconsommation'],
        },
    },
}

class ModelDispatcher:
    def __init__(self):
        self.Oequilibre = 0
        self.Iproduction = 0
        self.Iconsommation = 0

    def step(self, time):
        """Perform a simulation step by adding *delta* to *val*."""
        self.Oequilibre = self.Iproduction-self.Iconsommation
        #print("youhou")
        #print('ModeleDispatcher Step - Oequilibre : %f - Iconsommation : %f' %(self.Oequilibre, Iconsommation))


class SDispatcher(mosaik_api.Simulator):
    def __init__(self):
        mosaik_api.Simulator.__init__(self, META) # ou super().__init__(META) ou mosaik_api.Simulator.__init__(META)
        self.entites = []
        self.entities = {}
        self.eid_prefix = 'Dispatcher_'

    def init(self, sid, eid_prefix=None):
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.entities)
        entities = []
        print('On cree %d %s' % (num,model))
        for i in range(next_eid, next_eid + num):
            eid = '%s%d' % (self.eid_prefix, i)
            entite = ModelDispatcher()
            self.entites.append(entite)
            self.entities[eid] = i
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs):
        # Get inputs
        deltas = {}

        if inputs != {}:
            for eid, attrs in inputs.items():
                #eid : id de l'entite concernee
                model_idx = self.entities[eid]
                self.entites[model_idx].Iproduction = 0
                self.entites[model_idx].Iconsommation = 0
                for attr, values in attrs.items(): #attr : l'attribut, values : les valeurs sous la forme liste de ('src':val)
                    # a priori deux tours de boucles un pour la conso un pour la production
                    if attr=="Iconsommation":
                        self.entites[model_idx].Iconsommation = sum(values.values()) # somme les consommations des elements
                    if attr=="Iproduction":
                        self.entites[model_idx].Iproduction = sum(values.values()) # somme les productions des elements
                    #print('Dispatcher Step %d attr:%s - Src/val : %s '   %(time,attr,values))
                self.entites[model_idx].step(time)

        #for model in self.entites:
        #    model.Oequilibre = model.Iproduction - model.Iconsommation
            #model.Oequilibre = 0

        return time + 60  # Step size is 1 minute

    def get_data(self, outputs):
        models = self.entites
        data = {}
        for eid, attrs in outputs.items():
            model_idx = self.entities[eid]
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ModelDispatcher']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                # Get model.val or model.delta:
                data[eid][attr] = getattr(models[model_idx], attr)

        return data
