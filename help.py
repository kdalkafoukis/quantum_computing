from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys
from generate_mixed_state import generate_density_matrix, shiftedState

prog = Program()

state = np.array([[
    0, 1, 1, 1, 
    0, 1, 0, 1, 
]], dtype=complex)

rows = len(state[0])

arr = generate_density_matrix(state, rows)
bits = shiftedState(state, rows)

for position, bit in enumerate(reversed(bits)):
    if(bool(bit)):
        prog += Program(X(position))

definition = DefGate("operator", arr)
prog += Program(definition)
operator = definition.get_constructor()

num_of_qubits = int(np.log2(rows))
qubits = range(num_of_qubits)
qbits = [qubit for qubit in reversed(qubits)]
prog += Program(operator(*qbits))

wfn = WavefunctionSimulator().wavefunction(prog)
prob = wfn.get_outcome_probs()

print(wfn)
# print(prob)
