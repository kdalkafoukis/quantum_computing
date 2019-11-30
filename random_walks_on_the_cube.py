# https://en.wikipedia.org/wiki/Quantum_walk

# author: Konstantinos Dalkafoukis
# random walks on the cube
from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys


def coin(qubits):
    prog = Program()

    arr = np.sqrt(1/3) * np.array([
        [0, 1, 1, 1],
        [1, -1, 1, 0],
        [1, 1, 0, -1],
        [1, 0, -1, 1]
    ], dtype=complex)

    definition = DefGate("operator", arr)
    prog += Program(definition)
    operator = definition.get_constructor()
    qbits = [qubit for qubit in reversed(qubits)]
    prog += Program(operator(*qbits))
    return prog


def random_walks():
    prog = Program()

    num_of_qubits = 2
    qubits = range(num_of_qubits)

    prog += coin(qubits)
    return prog


def main(argv):
    prog = random_walks()
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    print(prob)


if __name__ == "__main__":
    main(sys.argv[1:])
