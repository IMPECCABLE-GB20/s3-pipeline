from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
import sys

prmtop = AmberPrmtopFile('../../../build/complex.prmtop')
system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=0.8*nanometer, constraints=HBonds)
platform = Platform.getPlatformByName('CUDA')
properties = {'Precision': 'mixed'}
#properties = {'Precision': 'mixed', 'DisablePmeStream': '\'true\''}
integrator = LangevinIntegrator(300*kelvin, 5/picosecond, 0.002*picoseconds)
system.addForce(MonteCarloBarostat(1.01325*bar, 300*kelvin, 25))
simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
simulation.loadState('../equilibration/eq1.xml')

simulation.reporters.append(DCDReporter('sim1.dcd', 50000))
simulation.reporters.append(StateDataReporter('sim1.log', 10000, step=True, potentialEnergy=True, temperature=True))

# Simulation
simulation.step(2500000)
simulation.saveState('sim1.xml')

