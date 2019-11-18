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
    factoryModeles = world.start('SimulateurModels')
    factoryBat = world.start('SimulateurModels')
    factoryDispatcher = world.start('Dispatcher')
    factoryDispatcher2 = world.start('Dispatcher')
    #pypower = world.start('PyPower', step_size=15 * 60)

    # Instantiate models
    print("instanciation OdC")
    entiteOdC = factoryModeles.ModelOdC()
    print("instanciation BC")
    entiteBC = factoryModeles.ModelBC()
    print("instanciation BP")
    entiteBP = factoryModeles.ModelBP()
    print("instanciation CA")
    entiteCA = factoryModeles.ModelCA()
    print("instanciation Bat")
    batterie = factoryBat.Batterie()
    print("instanciation Profile")
    profileP = world.start('CSV', sim_start=START, datafile=PROFILE_P)
    profileC = world.start('CSV', sim_start=START, datafile=PROFILE_C)
    entitePP = profileP.ModelProfil() #.create(1)
    entitePC = profileC.ModelProfil() #.create(1)
    print("instanciation Dispatcher")
    entiteDispatcher = factoryDispatcher.ModelDispatcher()
    entiteDispatcher2 = factoryDispatcher2.ModelDispatcher()


    # Connect entities
    world.connect(entiteOdC, entiteDispatcher, ('Oconsommation','Iconsommation'))
    world.connect(entiteDispatcher, entiteOdC, ('Oequilibre','Iequilibre'), time_shifted=True, initial_data={'Oequilibre': 0})
    world.connect(entiteBC, entiteDispatcher, ('Oconsommation', 'Iconsommation'))
    world.connect(entiteBP, entiteDispatcher, ('Oproduction', 'Iproduction'))

    world.connect(entiteCA, entiteDispatcher2, ('Oproduction', 'Iproduction'), ('Oconsommation', 'Iconsommation'))
    world.connect(entitePP, entiteCA, ('P', 'Iproduction'))
    world.connect(entitePC, entiteCA, ('P', 'Iconsommation'))

    world.connect(batterie, entiteCA, ('Ocharge', 'Icharge'))
    world.connect(entiteCA, batterie, ('Ocharge', 'Icharge'), time_shifted=True, initial_data={'Ocharge': 10})

    #world.connect(entiteDispatcher, entiteDispatcher2)

    # Create more entities
    entitesOdC = factoryModeles.ModelOdC.create(10)
    # Instantiate models
    #grid = pypower.Grid(gridfile=GRID_FILE).children

    connect_many_to_one(world, entitesOdC, entiteDispatcher2,  ('Oconsommation', 'Iconsommation'))
    for entite in entitesOdC:
        world.connect(entiteDispatcher2, entite, ('Oequilibre','Iequilibre'), time_shifted=True, initial_data={'Oequilibre': 0})

    #factoryMonitor = world.start('Collector')
    #monitor = factoryMonitor.Monitor()

    #mosaik.util.connect_many_to_one(world, entitesBC, monitor, 'Oconsommation', 'Oproduction')

    webvis = world.start('WebVis', start_date=START, step_size=60)
    webvis.set_config(ignore_types=['Topology', 'ResidentialLoads', 'Grid', 'Database'])
    vis_topo = webvis.Topology()

    world.connect(entiteOdC, vis_topo, 'Oconsommation')
    world.connect(entiteBC, vis_topo, 'Oconsommation')
    world.connect(entiteBP, vis_topo, 'Oproduction')
    world.connect(entitePP, vis_topo, 'P')
    world.connect(entitePC, vis_topo, 'P')
    world.connect(batterie, vis_topo, 'Ocharge')
    world.connect(entiteCA, vis_topo, 'Oconsommation')
    connect_many_to_one(world, entitesOdC, vis_topo, 'Oconsommation')
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
            'max': 3000,
        }, })
    webvis.set_etypes({
        'ModelOdC': {
            'cls': 'load',
            'attr': 'Oconsommation',
            'unit': 'Conso.',
            'default': 0,
            'min': 0,
            'max': 3000,
        }, })

    webvis.set_etypes({
        'ModelBC': {
            'cls': 'load',
            'attr': 'Oconsommation',
            'unit': 'Conso.',
            'default': 0,
            'min': 0,
            'max': 3000,
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

    world.connect(entiteDispatcher, vis_topo, 'Oequilibre')
    world.connect(entiteDispatcher2, vis_topo, 'Oequilibre')
    webvis.set_etypes({
        'ModelDispatcher': {
            'cls': 'gen',
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
    main()
