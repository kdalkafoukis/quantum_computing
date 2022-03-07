
# https://core.ac.uk/download/pdf/214315115.pdf
# https://arxiv.org/abs/quant-ph/9607014

# Alternate Minimum Algorithm
# implementation: pyquil
# author: Konstantinos Dalkafoukis

from pyquil import Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys
from generate_superposition_state import getSuperPositionState, multi_hot_encoder, getNumberOfQubitsOfPositionAndOfArray
from utils import plotOutput


class Obstacle:
    def __init__(self, qubits, inputArr, i, name):
        rows = 2 ** qubits
        arr = np.identity(rows, int)
        counter = 0
        for elem in reversed(['{:0{:d}b}'.format(el, qubits) for el in inputArr]):
            if elem[i] == "0":
                arr[counter][counter] = -1
            counter += 1
        self.obstacle_definition = DefGate(name, arr)
        self.qubits = range(qubits)

    def init(self):
        return Program(self.obstacle_definition)

    def iterate(self):
        OBSTACLE = self.obstacle_definition.get_constructor()
        qbits = [qubit for qubit in reversed(self.qubits)]
        return Program(OBSTACLE(*qbits))


class GroversDiffusionOperator:
    def __init__(self, qubits, inputArr):
        arr = multi_hot_encoder(inputArr, qubits)
        sC = np.sqrt(1 / len(inputArr)) * np.array(arr)
        sCproduct = np.multiply(sC, np.transpose(sC))
        G = 2 * sCproduct - np.identity(2 ** qubits)
        arr = G
        self.diffusion_operator_definition = DefGate("DIFFUSION_OPERATOR", arr)
        self.qubits = range(qubits)

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


def find_minimum(inputArr):
    # extra hack, needs better software engineering together with generate_superposition state
    arr = inputArr.copy()
    prog = getSuperPositionState(inputArr)
    qubitsOfPosition, qubitsOfArrayElement = getNumberOfQubitsOfPositionAndOfArray(
        arr)

    qubitsOfPosition = int(qubitsOfPosition)
    qubitsOfArrayElement = int(qubitsOfArrayElement)
    qubits = qubitsOfPosition + qubitsOfArrayElement
    grovers_diffusion_operator = GroversDiffusionOperator(qubits, inputArr)
    prog += grovers_diffusion_operator.init()

    for i in range(qubitsOfArrayElement):
        obstacle = Obstacle(qubitsOfArrayElement, arr,
                            i, 'OBSTACLE-{}'.format(i))
        prog += obstacle.init()
        prog += obstacle.iterate()
        prog += grovers_diffusion_operator.iterate()
        prog += obstacle.iterate()
        for j in range(qubitsOfArrayElement):
            prog += Program(RZ(2 * np.pi, j))
    return prog


# def getArray(argv):
#     inputArr = [7, 5, 2, 1, 6]
#     if len(argv) == 1 and argv[0] in argv:
#         arr = [int(x) for x in argv[0] if x != ',']
#         try:
#             inputArr = arr
#         except ValueError:
#             pass
#     return inputArr


def main(argv):
    inputArr = [7, 5, 2, 1, 6]
    prog = find_minimum(inputArr)
    wfn = WavefunctionSimulator().wavefunction(prog)
    print(wfn)
    prob = wfn.get_outcome_probs()
    plotOutput(prob)


if __name__ == "__main__":
    main(sys.argv[1:])
