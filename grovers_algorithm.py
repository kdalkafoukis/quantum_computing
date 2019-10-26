# https://arxiv.org/pdf/quant-ph/9605043.pdf
# https://en.wikipedia.org/wiki/Grover%27s_algorithm

from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np


def obstacle(qubits, key):
    prog = Program()

    rows = 2 ** len(qubits)
    arr = np.zeros((rows, rows), int)

    for row in range(rows):
        diagonal_element = 1
        if(row == key):
            diagonal_element = -1

        arr[row][row] = diagonal_element

    obstacle_definition = DefGate("OBSTACLE", arr)
    OBSTACLE = obstacle_definition.get_constructor()
    prog += Program(obstacle_definition)

    qbits = [qubit for qubit in reversed(qubits)]

    prog += Program(OBSTACLE(*qbits))

    return prog


def grovers_diffusion_operator(qubits):
    prog = Program()

    rows = 2 ** len(qubits)
    arr = 2 / 2**len(qubits) * \
        np.ones((rows, rows), int) - np.identity(rows)

    diffusion_operator_definition = DefGate("DIFFUSION_OPERATOR", arr)
    DIFFUSION_OPERATOR = diffusion_operator_definition.get_constructor()
    prog += Program(diffusion_operator_definition)

    qbits = [qubit for qubit in reversed(qubits)]

    prog += Program(DIFFUSION_OPERATOR(*qbits))

    return prog


def equalSuperPosition(qubits):
    prog = Program()
    for i in qubits:
        prog += Program(H(qubits[i]))
    return prog


def groversAlgorithm(qubits, key):
    prog = Program()
    prog += equalSuperPosition(qubits)
    prog += obstacle(qubits, key)
    prog += grovers_diffusion_operator(qubits)
    return prog


def run():
    num_of_qubits = 3
    qubits = range(num_of_qubits)
    key = 5

    prog = groversAlgorithm(qubits, key)

    wfn = WavefunctionSimulator().wavefunction(prog)
    print(wfn)


run()
