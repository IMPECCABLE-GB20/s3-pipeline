from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
import sys

inpcrd = PDBFile('../../../build/complex.pdb')
prmtop = AmberPrmtopFile('../../../build/complex.prmtop')

system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=0.8*nanometer, constraints=HBonds)
platform = Platform.getPlatformByName('CUDA')
properties = {'Precision': 'mixed'}
#properties = {'Precision': 'mixed', 'DisablePmeStream': '\'true\''}
integrator = LangevinIntegrator(50*kelvin, 5/picosecond, 0.002*picoseconds)
simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
simulation.context.setPositions(inpcrd.positions)
#if inpcrd.boxVectors is not None:
#    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

# Minimization
simulation.minimizeEnergy()
simulation.saveState('eq0.xml')

# Heating from 50 to 300 K
temperature = 50
simulation.reporters.append(StateDataReporter('eq1.log', 2500, step=True, potentialEnergy=True, temperature=True))
for i in range(250):
    simulation.step(100)
    temperature += 1
    integrator.setTemperature(temperature*kelvin)
simulation.step(5000)
simulation.saveState('eq1.xml')

