# simulator_mosaik.py
"""
Mosaik interface for the models.

"""
import mosaik_api

import simulator

META = {
    'models': {
        'ModelBC': {
            'public': True,
            'params': ['num', 'profile'],
            'attrs': ['num', 'profile'],
        },
    },
}


class SimulatorModelBC(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'BC_'
        self.entities = {}  # Maps EIDs to model indices in self.simulator
        self.models = []  # models list
        self.dataOut = []  # energy exchange
        self.energyexchanged = energyExchange()
        self.inputData = dataIn()

    def init(self, sid, eid_prefix=None):
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, init_val):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            eid = '%s%d' % (self.eid_prefix, i)
            modellocal = ModelBC(nb)
            self.models.append(modellocal)
            self.dataOut.append([])  # Add list for simulation data
            self.entities[eid] = i
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, data):

        # Perform simulation step
        for i, model in enumerate(self.models):
            energy = model.step(data)
            self.dataOut[i].append(energy)

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