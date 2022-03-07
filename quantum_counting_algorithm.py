# https://en.wikipedia.org/wiki/Quantum_counting_algorithm

# author: Konstantinos Dalkafoukis
# Quantum phase estimation
from pyquil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys
from pyquil.quil import DefGate
from utils import plotOutput


def getObstacle(qubits, keys):
    rows = 2 ** len(qubits)
    arr = np.zeros((rows, rows), int)
    for row in range(rows):
        diagonal_element = 1
        if(row in keys):
            diagonal_element = -1

        arr[row][row] = diagonal_element

    obstacle_definition = DefGate("OBSTACLE", arr)
    return obstacle_definition


def getDiffOperator(qubits):
    rows = 2 ** len(qubits)
    arr = np.zeros((rows, rows), int)

    arr = 2 / rows * \
        np.ones((rows, rows), int) - np.identity(rows)

    diffusion_operator_definition = DefGate("DIFFUSION_OPERATOR", arr)
    return diffusion_operator_definition


def qft_dagger(num_of_iterations):
    prog = Program()
    for qubit in range(num_of_iterations//2):
        prog += Program(SWAP(qubit, num_of_iterations - qubit-1))
    for i in range(num_of_iterations):
        for j in range(i):
            cphase = CPHASE(-1 * np.pi / 2**(i-j), j, i)
            prog += Program(cphase)
        prog += Program(H(i))
    return prog


def applyHadamard(p, n):
    prog = Program()
    for qubit in range(p + n):
        prog += Program(H(qubit))
    return prog


def controlUnitary(p, n):
    prog = Program()
    num_of_solutions = 3
    obstacleDef = getObstacle(range(n, n + p), range(num_of_solutions))
    prog += Program(obstacleDef)
    diffOperatorDef = getDiffOperator(range(n, n + p))
    prog += Program(diffOperatorDef)
    obstacle = obstacleDef.get_constructor()
    diffOperator = diffOperatorDef.get_constructor()

    # qbits = [qubit for qubit in reversed(range(n, n + p))]
    qbits = [qubit for qubit in range(n, n + p)]
    for qubit in range(n):
        for _ in range(2 ** qubit):
            prog += Program(obstacle(*qbits))
            prog += Program(diffOperator(*qbits).controlled(qubit))
    return prog


def phase_estimation(p, n):
    prog = Program()
    prog += applyHadamard(p, n)
    prog += controlUnitary(p, n)
    prog += qft_dagger(n)
    return prog


def getInput(argv):
    p = 4
    n = 4
    if (len(argv) == 2):
        try:
            p = int(argv[0])
            n = int(argv[1])
        except ValueError:
            pass
    return p, n


def filterProb(prob):
    newProb = {}
    return


def main(argv):
    p, n = getInput(argv)
    prog = phase_estimation(p, n)
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print('p:', p)
    print('n:', n)
    # print('wfn:', wfn)
    newProb = filterProb(prob)
    plotOutput(newProb, 0.02)


if __name__ == "__main__":
    main(sys.argv[1:])
