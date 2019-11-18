# simulator_mosaik.py
"""
Mosaik interface for the example simulator.

"""
import mosaik_api
import simulator

META = {
    'models': {
        'ExampleModel': {
            'public': True,
            'params': ['num'],
            'attrs': ['num'],
        },
    },
}
