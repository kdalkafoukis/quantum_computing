# https://arxiv.org/pdf/quant-ph/9605043.pdf
# https://en.wikipedia.org/wiki/Grover%27s_algorithm

# author: Konstantinos Dalkafoukis
from pyquil import Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys


class Obstacle:
    def __init__(self, qubits, key):
        rows = 2 ** len(qubits)
        arr = np.zeros((rows, rows), int)

        for row in range(rows):
            diagonal_element = 1
            if(row == key):
                diagonal_element = -1

            arr[row][row] = diagonal_element

        self.obstacle_definition = DefGate("OBSTACLE", arr)
        self.qubits = qubits

    def init(self):
        return Program(self.obstacle_definition)

    def iterate(self):
        OBSTACLE = self.obstacle_definition.get_constructor()
        qbits = [qubit for qubit in reversed(self.qubits)]
        return Program(OBSTACLE(*qbits))


class GroversDiffusionOperator:
    def __init__(self, qubits):
        rows = 2 ** len(qubits)
        arr = np.zeros((rows, rows), int)

        arr = 2 / rows * \
            np.ones((rows, rows), int) - np.identity(rows)

        self.diffusion_operator_definition = DefGate("DIFFUSION_OPERATOR", arr)
        self.qubits = qubits

    def init(self):
        return Program(self.diffusion_operator_definition)

    def iterate(self):
        DIFFUSION_OPERATOR = self.diffusion_operator_definition.get_constructor()
        qbits = [qubit for qubit in reversed(self.qubits)]
        return Program(DIFFUSION_OPERATOR(*qbits))


def equalSuperPosition(qubits):
    prog = Program()
    for i in qubits:
        prog += Program(H(qubits[i]))
    return prog


def diffusion_iterations(qubits):
    return ((np.pi / 4) * np.sqrt(2 ** len(qubits))).astype(int)


def obstacle(qubits):
    prog = Program()
    num_of_qubits = len(qubits)
    num_of_qubits_minus_one = num_of_qubits - 1
    gate = Z(num_of_qubits_minus_one)
    for i in range(num_of_qubits_minus_one):
        gate = gate.controlled(i)
    prog += Program(gate)
    return prog


def flipQubits(qubits, key):
    prog = Program()
    num_of_qubits = len(qubits)
    counter = 0
    key_in_binary = '{:0{:d}b}'.format(key, num_of_qubits)
    for bit in reversed(key_in_binary):
        if bit == "0":
            prog += Program(X(counter))
        counter += 1
    return prog


def groversAlgorithmSingleKeySimulation(qubits, key):
    prog = Program()
    prog += equalSuperPosition(qubits)
    grovers_diffusion_operator = GroversDiffusionOperator(qubits)
    prog += grovers_diffusion_operator.init()
    iterations = diffusion_iterations(qubits)
    for _ in range(iterations):
        prog += obstacle(qubits)
        prog += grovers_diffusion_operator.iterate()

    prog += flipQubits(qubits, key)
    return prog


def groversAlgorithm(qubits, key):
    prog = Program()
    prog += equalSuperPosition(qubits)

    obstacle = Obstacle(qubits, key)
    prog += obstacle.init()

    grovers_diffusion_operator = GroversDiffusionOperator(qubits)
    prog += grovers_diffusion_operator.init()

    iterations = diffusion_iterations(qubits)
    for _ in range(iterations):
        prog += obstacle.iterate()
        prog += grovers_diffusion_operator.iterate()

    return prog


def getNumOfQubitsAndSearchKey(argv):
    num_of_qubits = 3
    key = 5
    if (len(argv) >= 2):
        try:
            argv0 = int(argv[0])
            argv1 = int(argv[1])
            if(argv[0] in argv and argv[1] in argv and 2 ** argv0 > argv1):
                num_of_qubits = argv0
                key = argv1

        except ValueError:
            pass

    return num_of_qubits, key


def main(argv):
    num_of_qubits, key = getNumOfQubitsAndSearchKey(argv)

    qubits = range(num_of_qubits)

    prog = groversAlgorithm(qubits, key)
    # prog = groversAlgorithmSingleKeySimulation(qubits, key)

    wfn = WavefunctionSimulator().wavefunction(prog)
    print(wfn)


if __name__ == "__main__":
    main(sys.argv[1:])
