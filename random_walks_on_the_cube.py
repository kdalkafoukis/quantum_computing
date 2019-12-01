# https://en.wikipedia.org/wiki/Quantum_walk

# author: Konstantinos Dalkafoukis
# random walks on the cube
from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys


def coin():
    prog = Program()

    num_of_qubits = 2
    qubits = range(num_of_qubits)

    arr = np.sqrt(1/3) * np.array([
        [0,  1,  1,  1],
        [1, -1,  1,  0],
        [1,  1,  0, -1],
        [1,  0, -1,  1]
    ], dtype=complex)

    definition = DefGate("coin", arr)
    prog += Program(definition)
    operator = definition.get_constructor()
    qbits = [qubit for qubit in reversed(qubits)]
    prog += Program(operator(*qbits))
    return prog


def sOperator():
    '''
        |1> = |01>
        |2> = |10>
        |3> = |11>
        S = |1><1|⨂∑|adj_vertex1_of_i><i| +
            |2><2|⨂∑|adj_vertex2_of_i><i| +
            |3><3|⨂∑|adj_vertex3_of_i><i|
    '''
    prog = Program()

    adjMatrix = np.array([
        [0, 1, 1, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 0]
    ], dtype=complex)

    arr = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]
    ], dtype=complex)

    arr2 = np.array([
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0]
    ], dtype=complex)

    arr3 = np.array([
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0]
    ], dtype=complex)

    arr4 = np.array([
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0]
    ], dtype=complex)

    num_of_qubits = 5
    qubits = range(num_of_qubits)

    rows = 2 ** len(qubits)
    ar = np.zeros((rows, rows), int)

    for i in range(8):
        for j in range(8):
            ar[i][j] = arr[i][j]

    for i in range(8, 16):
        for j in range(8, 16):
            ar[i][j] = arr2[i % 8][j % 8]

    for i in range(16, 24):
        for j in range(16, 24):
            ar[i][j] = arr3[i % 8][j % 8]

    for i in range(24, 32):
        for j in range(24, 32):
            ar[i][j] = arr4[i % 8][j % 8]

    definition = DefGate("sOperator", ar)
    prog += Program(definition)
    operator = definition.get_constructor()
    qbits = [qubit for qubit in qubits]
    prog += Program(operator(*qbits))
    return prog


def random_walks():
    prog = Program()

    for i in range(1):
        prog += coin()
        prog += sOperator()

    return prog


def main(argv):
    prog = random_walks()
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    print(prob)


if __name__ == "__main__":
    main(sys.argv[1:])
