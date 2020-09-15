# https://en.wikipedia.org/wiki/Quantum_walk

# author: Konstantinos Dalkafoukis
# random walks on the line
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


def mCoin(num_of_qubits):
    '''
        M Coin
        M_COIN = (
            1  j
            j  1
        )
    '''
    arr = (1/np.sqrt(2)) * np.array([(1, 1j), (1j, 1)], dtype=complex)
    definition = DefGate("m_operator", arr)
    operator = definition.get_constructor()
    return Program(definition, operator(num_of_qubits))


def hadamardCoin(num_of_qubits):
    '''
        Hadamard Coin
        H_COIN = (
            1  1
            1 -1
        )
    '''
    return Program(H(num_of_qubits))


def coin(num_of_qubits):
    return hadamardCoin(num_of_qubits)


def sOperator(qubits):
    '''
        S = |↑><↑|⨂∑|i+1><i| +|↓><↓|⨂∑|i-1><i|
    '''
    rows = 2 ** len(qubits)
    arr = np.zeros((rows, rows), int)

    for row in range(rows):
        if (row < (rows >> 1)):
            column = row + 1
            if(row == (rows >> 1)-1):
                column = 0
            arr[row][column] = 1

        else:
            column = row - 1
            if(row == (rows >> 1)):
                column = rows - 1
            arr[row][column] = 1

    definition = DefGate("s_operator", arr)

    return definition


def getNumOfQubits(num_of_iterations):
    num_of_qubits = num_of_iterations
    length = 2 * num_of_iterations
    i = 0
    while(2 ** i <= length):
        i = i + 1

        num_of_qubits = i
    return num_of_qubits


def random_walks(num_of_iterations):
    # starts from zero and last is the mean of 2** qubits -1
    # so its going like for q=3, |000> = |0>, |111> = |-1> , |001> = |1>
    # |(+)>_max = mean(2**q) -1
    # |(-)>_min = mean(2**q)
    prog = Program()
    num_of_qubits = getNumOfQubits(num_of_iterations)
    # num_of_qubits+1 includes the spin qubit (+1)
    qubits = list(range(num_of_qubits+1))
    definition = sOperator(qubits)
    prog += Program(definition)
    operator = definition.get_constructor()
    qbits = [qubit for qubit in reversed(qubits)]

    initStateIsUpZero = True
    # init state  |y(0)> = |↑>⨂|0>

    for i in range(num_of_iterations):
        prog += coin(num_of_qubits)
        prog += Program(operator(*qbits))
        # if init state  |y(0)> = |↓>⨂|0>
        if(not(initStateIsUpZero)):
            prog += Program(X(num_of_qubits))

    return prog


def main(argv):
    num_of_iterations = parseNumOfIterations(argv)

    prog = random_walks(num_of_iterations)

    wfn = WavefunctionSimulator().wavefunction(prog)

    prob = wfn.get_outcome_probs()

    print(wfn)

    print(prob)


if __name__ == "__main__":
    main(sys.argv[1:])
