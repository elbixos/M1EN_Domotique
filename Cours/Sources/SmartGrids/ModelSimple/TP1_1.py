# demo_1.py
import mosaik
import mosaik.util
import webbrowser
import random

from mosaik.util import connect_randomly, connect_many_to_one


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

def main():

    random.seed(23)
    # Create World
    world = mosaik.World(SIM_CONFIG)

    # Start simulators
    factoryDispatcher = world.start('Dispatcher')
    factoryProfileP = world.start('CSV', sim_start=START, datafile=PROFILE_P)
    factoryProfileC = world.start('CSV', sim_start=START, datafile=PROFILE_C)
    factoryModeles = world.start('SimulateurModels')
    factoryBat = world.start('SimulateurModels')

    # Instantiate models
    print("instanciation Dispatcher")
    entiteDispatcher = factoryDispatcher.ModelDispatcher()


    #creation des noeuds
    entiteCA = factoryModeles.ModelCA()
    batterie = factoryBat.Batterie()
    entitePP = factoryProfileP.ModelProfil()  # .create(1)
    entitePC = factoryProfileC.ModelProfil()  # .create(1)

    world.connect(entitePP, entiteCA, ('P', 'Iproduction'))
    world.connect(entitePC, entiteCA, ('P', 'Iconsommation'))
    world.connect(batterie, entiteCA, ('Ocharge', 'Icharge'))
    world.connect(entiteCA, batterie, ('Ocharge', 'Icharge'), time_shifted=True, initial_data={'Ocharge': 10})

    world.connect(entiteCA, entiteDispatcher, ('Oconsommation','Iconsommation'))
    world.connect(entiteDispatcher, entiteCA, ('Oequilibre','Iequilibre'), time_shifted=True, initial_data={'Oequilibre': 0})

    webvis = world.start('WebVis', start_date=START, step_size=60)
    webvis.set_config(ignore_types=['Topology', 'ResidentialLoads', 'Grid', 'Database'])
    vis_topo = webvis.Topology()

    # On connecte les noeuds a la visualisation web
    world.connect(entiteDispatcher, vis_topo, 'Oequilibre')
    world.connect(entiteCA, vis_topo, 'Oconsommation')
    world.connect(entitePP, vis_topo, 'P')
    world.connect(entitePC, vis_topo, 'P')
    world.connect(batterie, vis_topo, 'Ocharge')

    webvis.set_etypes({
        'ModelProfil': {
            'cls': 'load',
            'attr': 'P',
            'unit': 'P.',
            'default': 0,
            'min': -1000,
            'max': 1000,
        }, })
    webvis.set_etypes({
        'ModelDispatcher': {
            'cls': 'load',
            'attr': 'Oequilibre',
            'unit': 'Equ.',
            'default': 0,
            'min': -3000,
            'max': 3000,
        },})
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

    webbrowser.open('http://localhost:8000')
    # Run simulation
    world.run(until=END)
    #world.run(until=END, rt_factor=1 / 60)

if __name__ == '__main__':
    print("Main")
    main()
