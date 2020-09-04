from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys
from generate_mixed_state import generate_density_matrix

prog = Program()

arr = generate_density_matrix()
definition = DefGate("operator", arr)
prog += Program(definition)
operator = definition.get_constructor()

prog += Program(operator(2,1,0))

wfn = WavefunctionSimulator().wavefunction(prog)
prob = wfn.get_outcome_probs()

print(wfn)
print(prob)
