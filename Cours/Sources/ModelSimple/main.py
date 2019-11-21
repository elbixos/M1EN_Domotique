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
NB_DISPATCHER = 4

def main():

    random.seed(23)
    # Create World
    world = mosaik.World(SIM_CONFIG)

    # Start simulators
    factoryModeles = world.start('SimulateurModels')
    factoryBat = world.start('SimulateurModels')
    factoryDispatcher = world.start('Dispatcher')
    factoryProfileP = world.start('CSV', sim_start=START, datafile=PROFILE_P)
    factoryProfileC = world.start('CSV', sim_start=START, datafile=PROFILE_C)
    webvis = world.start('WebVis', start_date=START, step_size=60)
    webvis.set_config(ignore_types=['Topology', 'ResidentialLoads', 'Grid', 'Database'])
    vis_topo = webvis.Topology()

    # Instantiate models
    print("instanciation Dispatcher")
    entitesDispatcher = factoryDispatcher.ModelDispatcher.create(NB_DISPATCHER)
    connect_many_to_one(world, entitesDispatcher, vis_topo, 'Oequilibre')

    for dispatcher in entitesDispatcher:
        #creation des noeuds
        entiteCA = factoryModeles.ModelCA()
        batterie = factoryBat.Batterie()
        entitePP = factoryProfileP.ModelProfil()  # .create(1)
        entitePC = factoryProfileC.ModelProfil()  # .create(1)
        entiteBC = factoryModeles.ModelBC()
        entiteBP = factoryModeles.ModelBP()
        # Connection des noeuds
        # Un CA est compose d'une batterie, d'un systeme de production et de consommation
        world.connect(entitePP, entiteCA, ('P', 'Iproduction'))
        world.connect(entitePC, entiteCA, ('P', 'Iconsommation'))
        world.connect(batterie, entiteCA, ('Ocharge', 'Icharge'))
        world.connect(entiteCA, batterie, ('Ocharge', 'Icharge'), time_shifted=True, initial_data={'Ocharge': 10})
        # On connecte au dispatcher, un CA, un BP, un BC
        world.connect(entiteCA, dispatcher, ('Oconsommation','Iconsommation'))
        world.connect(dispatcher, entiteCA, ('Oequilibre','Iequilibre'), time_shifted=True, initial_data={'Oequilibre': 0})
        world.connect(entiteBC, dispatcher, ('Oconsommation', 'Iconsommation'))
        world.connect(entiteBP, dispatcher, ('Oproduction', 'Iproduction'))
        # On connecte les noeuds a la visualisation web
        world.connect(entiteBC, vis_topo, 'Oconsommation')
        world.connect(entiteBP, vis_topo, 'Oproduction')
        world.connect(entitePP, vis_topo, 'P')
        world.connect(entitePC, vis_topo, 'P')
        world.connect(batterie, vis_topo, 'Ocharge')
        world.connect(entiteCA, vis_topo, 'Oconsommation')

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
        'ModelProfil': {
            'cls': 'load',
            'attr': 'P',
            'unit': 'P.',
            'default': 0,
            'min': -1000,
            'max': 1000,
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
    webvis.set_etypes({
        'ModelBC': {
            'cls': 'load',
            'attr': 'Oconsommation',
            'unit': 'Conso.',
            'default': 0,
            'min': 0,
            'max': 100,
        }, })
    webvis.set_etypes({
        'ModelBP': {
            'cls': 'load',
            'attr': 'Oproduction',
            'unit': 'Prod.',
            'default': 0,
            'min': 0,
            'max': 3000,
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

    webbrowser.open('http://localhost:8000')
    # Run simulation
    world.run(until=END)
    #world.run(until=END, rt_factor=1 / 60)

if __name__ == '__main__':
    print("Main")
    main()
