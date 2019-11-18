# simulator_mosaik.py
"""
Mosaik interface for the models.

"""
import mosaik_api

import simulator

# Sim config. and other parameters
SIM_CONFIG = {
    'ModelBC': {
        'python': 'simulatorModelBC:SimulatorModelBC',
    },
    'Collector': {
        'cmd': 'python collector.py %(addr)s',
    },
}
END = 10 * 60  # 10 minutes



def main():
    random.seed(23)
    world = mosaik.World(sim_config)
    create_scenario(world)
    webbrowser.open('http://localhost:8000')
    world.run(until=END)  # As fast as possilbe
    # world.run(until=END, rt_factor=1/60)  # Real-time 1min -> 1sec

def Generateur():
    while

def create_scenario(world):
    # Start simulators
    pypower = world.start('ModelBC')

    # Instantiate models
    grid = pypower.Grid(gridfile=GRID_FILE).children
    profile = []
    for i in range(1000):
        profile.append(randint(0, 100))
    BCInstance = ModelBC(1, profile)

    # Connect entities
    connect_buildings_to_grid(world, BCInstance, grid)
  #  connect_randomly(world, pvs, [e for e in grid if 'node' in e.eid], 'P')

    # Database
    #db = world.start('DB', step_size=60, duration=END)
    #hdf5 = db.Database(filename='demo.hdf5')
    #connect_many_to_one(world, houses, hdf5, 'P_out')
    #connect_many_to_one(world, pvs, hdf5, 'P')

    #nodes = [e for e in grid if e.type in ('RefBus, PQBus')]
    #connect_many_to_one(world, nodes, hdf5, 'P', 'Q', 'Vl', 'Vm', 'Va')

    #branches = [e for e in grid if e.type in ('Transformer', 'Branch')]
    #connect_many_to_one(world, branches, hdf5,
    #                    'P_from', 'Q_from', 'P_to', 'P_from')

    # Web visualization
    webvis = world.start('WebVis', start_date=START, step_size=60)
    webvis.set_config(ignore_types=['Topology', 'BCInstances', 'Grid',
                                    'Database'])
    vis_topo = webvis.Topology()

    connect_many_to_one(world, nodes, vis_topo, 'P', 'Vm')
    webvis.set_etypes({
        'RefBus': {
            'cls': 'refbus',
            'attr': 'P',
            'unit': 'P [W]',
            'default': 0,
            'min': 0,
            'max': 30000,
        },
        'PQBus': {
            'cls': 'pqbus',
            'attr': 'Vm',
            'unit': 'U [V]',
            'default': 230,
            'min': 0.99 * 230,
            'max': 1.01 * 230,
        },
    })

    connect_many_to_one(world, houses, vis_topo, 'P_out')
    webvis.set_etypes({
        'House': {
            'cls': 'load',
            'attr': 'P_out',
            'unit': 'P [W]',
            'default': 0,
            'min': 0,
            'max': 3000,
        },
    })

    connect_many_to_one(world, pvs, vis_topo, 'P')
    webvis.set_etypes({
        'PV': {
            'cls': 'gen',
            'attr': 'P',
            'unit': 'P [W]',
            'default': 0,
            'min': -10000,
            'max': 0,
        },
    })


def connect_buildings_to_grid(world, houses, grid):
    buses = filter(lambda e: e.type == 'PQBus', grid)
    buses = {b.eid.split('-')[1]: b for b in buses}
    house_data = world.get_data(houses, 'node_id')
    for house in houses:
        node_id = house_data[house]['node_id']
        world.connect(house, buses[node_id], ('P_out', 'P'))


if __name__ == '__main__':
    main()
