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

def sOperator(qubits, operator):
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

    arr1 = np.identity(8)

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
            ar[i][j] = arr2[i][j]
            ar[i+8][j+8] = arr3[i][j]
            ar[i+16][j+16] = arr4[i][j]
            ar[i+24][j+24] = arr1[i][j]

    definition = DefGate(operator, ar)
    return definition

def dft(gateName):
    '''
    https://en.wikipedia.org/wiki/DFT_matrix
    '''
    fftEl = 1/2 - 1j* np.sqrt(3)/2
    # A = np.sqrt(1 / 3) * np.array([
    #     [   np.sqrt(3),  0,  0, 0],
    #     [   0, fftEl ** 1, fftEl ** 2, fftEl ** 3],
    #     [   0, fftEl ** 2, -fftEl ** 4, fftEl ** 6],
    #     [   0, fftEl ** 3, fftEl ** 6, fftEl ** 9],
    # ], dtype=complex)
    A = np.sqrt(1 / 3) * np.array([
        [   1,  1,  1, 0],
        [   1, -fftEl ** 1,  fftEl ** 2, 0],
        [  -1, -fftEl ** 2, -fftEl ** 4, 0],
        [   0,  0 , 0, np.sqrt(3)],
    ], dtype=complex)
    arr = A
    definition = DefGate(gateName, arr)
    return definition

def groverCoin(gateName):
    sC = np.sqrt(1 / 3) * np.array([[1,1,1,0]])
    sCproduct = np.multiply(sC, np.transpose(sC))
    G = 2 * sCproduct - np.identity(4)
    arr = G
    definition = DefGate(gateName, arr)
    return definition

def random_walks(num_of_iterations=1):
    prog = Program()

    num_of_qubits = 5
    qubits = range(num_of_qubits)

    definition = sOperator(qubits, "sOperator")
    prog += Program(definition)
    operator = definition.get_constructor()
    qbits = [qubit for qubit in reversed(qubits)]

    coinDefinition = dft("coin")
    prog += Program(coinDefinition)
    coinOperator = coinDefinition.get_constructor()

    groverCoinDefinition = groverCoin("groverCoin")
    prog += Program(groverCoinDefinition)
    groverCoinOperator = groverCoinDefinition.get_constructor()

    for i in range(num_of_iterations):
        prog += Program(coinOperator(3,4))
        # prog += Program(groverCoinOperator(3,4))
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
