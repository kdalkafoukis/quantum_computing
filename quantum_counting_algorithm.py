# https://en.wikipedia.org/wiki/Quantum_counting_algorithm

# author: Konstantinos Dalkafoukis
# Quantum counting algorithm
from pyquil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys
from pyquil.quil import DefGate
from utils import plotOutput
import math


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


def controlUnitary(p, n, num_of_solutions):
    prog = Program()
    obstacleDef = getObstacle(range(n, n + p), range(num_of_solutions))
    prog += Program(obstacleDef)
    diffOperatorDef = getDiffOperator(range(n, n + p))
    prog += Program(diffOperatorDef)
    obstacle = obstacleDef.get_constructor()
    diffOperator = diffOperatorDef.get_constructor()

    qbits = [qubit for qubit in reversed(range(n, n + p))]
    for qubit in range(n):
        for _ in range(2 ** qubit):
            prog += Program(obstacle(*qbits))
            prog += Program(diffOperator(*qbits).controlled(qubit))
    return prog


def phase_estimation(p, n, num_of_solutions):
    prog = Program()
    prog += applyHadamard(p, n)
    prog += controlUnitary(p, n, num_of_solutions)
    prog += qft_dagger(n)
    return prog


def getInput(argv):
    p = 4
    n = 4
    num_of_solutions = 5
    if (len(argv) == 3):
        try:
            p = int(argv[0])
            n = int(argv[1])
            num_of_solutions = int(argv[2])
        except ValueError:
            pass
    return p, n, num_of_solutions


def filterProb(prob, p):
    newProb = {}
    for key, value in prob.items():
        k = key[:p:]
        if k not in newProb:
            newProb[k] = value
        else:
            newProb[k] += value
    return newProb


def calculate_M(measured_int, t, n):
    """For Processing Output of Quantum Counting"""
    # Calculate Theta
    theta = (measured_int/(2**t))*math.pi*2
    print("Theta = %.5f" % theta)
    # Calculate No. of Solutions
    N = 2**n
    M = N * (math.sin(theta/2)**2)
    print("No. of Solutions = %.1f" % (N-M))


def main(argv):
    p, n, num_of_solutions = getInput(argv)
    prog = phase_estimation(p, n, num_of_solutions)
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print('p:', p)
    print('n:', n)
    print('num_of_solutions:', num_of_solutions)
    # print('wfn:', wfn)
    newProb = filterProb(prob, p)
    plotOutput(newProb, 0.01)
    # plotOutput(prob, 0.01)
    print(prog)
    # calculate_M(3, p, n)


if __name__ == "__main__":
    main(sys.argv[1:])
