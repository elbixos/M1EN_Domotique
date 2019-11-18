# simulator_mosaik.py
"""
Mosaik interface for the models.

"""
import mosaik_api

import simulator

# Sim config. and other parameters
SIM_CONFIG = {
    'simulatorModels': {
        'python': 'simulatorModels:simulatorModels',
    },
    'Collector': {
        'cmd': 'python collector.py %(addr)s',
    },
}
END = 10 * 60  # 10 minutes

META = {
    'models': {
        'ModelBC': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
        'ModelBP': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
        'ModelSC': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
        'ModelCA': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
        'ModelOdC': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
        'ModelOdP': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
        'ModelBBP': {
            'public': True,
            'params': ['eid', 'profile'],
            'attrs': ['inputs', 'outputs','eid','profile'],
        },
    },
}


class SimulatorModels(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        # self.simulator = simulator.Simulator()
        self.eid_prefix = 'M_'
        self.entities = {}  # Maps EIDs to model indices in self.simulator
        self.models = []  # models list


    def init(self, sid, eid_prefix=None):
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    # num : nombre d'elements a creer
    # model : type d'element a creer
    # profile : le profile energetique de l'element
    def create(self, num, model, profile):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            eid = '%s%d' % (self.eid_prefix, i)
            modellocal = ModelBC(i)
            self.models.append(modellocal)
            self.dataOut.append([])  # Add list for simulation data
            self.entities[eid] = i
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs):
        # Get inputs
        deltas = {}
        for eid, attrs in inputs.items():
            for attr, values in attrs.items():
                model_idx = self.entities[eid]
                new_delta = sum(values.values())
                deltas[model_idx] = new_delta

        # Perform simulation step
        self.simulator.step(deltas)

        return time + 60  # Step size is 1 minute

    def get_data(self, outputs):
        models = self.simulator.models
        data = {}
        for eid, attrs in outputs.items():
            model_idx = self.entities[eid]
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ExampleModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                # Get model.val or model.delta:
                data[eid][attr] = getattr(models[model_idx], attr)

        return data


def main():
    return mosaik_api.start_simulation(ExampleSim())


if __name__ == '__main__':
    main()