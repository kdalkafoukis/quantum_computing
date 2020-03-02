# https://en.wikipedia.org/wiki/Quantum_walk

# author: Konstantinos Dalkafoukis
# random walks on the cube
from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys


def parseNumOfIterations(argv):
    num_of_iterations = 1
    if (len(argv) >= 1):
        try:
            argv0 = int(argv[0])
            if(argv[0] in argv):
                num_of_iterations = argv0

        except ValueError:
            pass

    return num_of_iterations


def coin():
    '''
    |0> = |00> |1> = |01> |2> = |10> |3> = |11>
    coin = 1/sqrt(3)(|1> + |2> + |3>)
    '''
    arr = np.sqrt(1 / 3) * np.array([
        [0,  1,  1,  1],
        [1, -1,  1,  0],
        [1,  1,  0, -1],
        [1,  0, -1,  1]
    ], dtype=complex)

    definition = DefGate("coin", arr)
    return definition


def sOperator(qubits, operator):
    '''
    |0> = |00> |1> = |01> |2> = |10> |3> = |11>
        |0><0|⨂∑|i><i| +
    S = |1><1|⨂∑|adj_vertex1_of_i><i| +
        |2><2|⨂∑|adj_vertex2_of_i><i| +
        |3><3|⨂∑|adj_vertex3_of_i><i|
    '''

    # adjMatrix = np.array([
    #     [0, 1, 1, 0, 1, 0, 0, 0],
    #     [1, 0, 0, 1, 0, 1, 0, 0],
    #     [1, 0, 0, 1, 0, 0, 1, 0],
    #     [0, 1, 1, 0, 0, 0, 0, 1],
    #     [1, 0, 0, 0, 0, 1, 1, 0],
    #     [0, 1, 0, 0, 1, 0, 0, 1],
    #     [0, 0, 1, 0, 1, 0, 0, 1],
    #     [0, 0, 0, 1, 0, 1, 1, 0]
    # ], dtype=complex)

    arr1 = np.identity(8, dtype=complex)

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

    rows = 2 ** len(qubits)
    ar = np.zeros((rows, rows), complex)
    for i in range(8):
        for j in range(8):
            ar[i][j] = arr1[i][j]
            ar[i+8][j+8] = arr2[i][j]
            ar[i+16][j+16] = arr3[i][j]
            ar[i+24][j+24] = arr4[i][j]

    definition = DefGate(operator, ar)
    return definition


def random_walks(num_of_iterations=1):
    prog = Program()

    num_of_qubits = 5
    qubits = range(num_of_qubits)

    definition = sOperator(qubits, "sOperator")
    prog += Program(definition)
    operator = definition.get_constructor()
    qbits = [qubit for qubit in reversed(qubits)]

    coinDefinition = coin()
    prog += Program(coinDefinition)
    coinOperator = coinDefinition.get_constructor()

    prog += Program(coinOperator(3, 4))
    prog += Program(operator(*qbits))

    return prog


def main(argv):
    num_of_iterations = parseNumOfIterations(argv)
    prog = random_walks(num_of_iterations)
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    # print(prob)


if __name__ == "__main__":
    main(sys.argv[1:])
