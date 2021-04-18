
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
    def __init__(self, qubits, keys, name):
        rows = 2 ** qubits
        arr = np.zeros((rows, rows), int)
        for row in range(rows):
            diagonal_element = 1
            if(row in keys):
                diagonal_element = -1

            arr[row][row] = diagonal_element

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
        print('inputArr', inputArr)
        arr = multi_hot_encoder(inputArr, qubits)
        rows = len(arr[0])
        print('rows', rows)
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

    grovers_diffusion_operator = GroversDiffusionOperator(
        qubitsOfPosition + qubitsOfPosition, inputArr)
    prog += grovers_diffusion_operator.init()

    obstacle = Obstacle(qubitsOfArrayElement, [
                        1, 2], 'OBSTACLE-{}'.format(0))
    prog += obstacle.init()
    prog += obstacle.iterate()
    prog += grovers_diffusion_operator.iterate()
    prog += obstacle.iterate()
    for i in range(3):
        prog += Program(RZ(2 * np.pi, i))

    obstacle = Obstacle(qubitsOfArrayElement, [
                        1, 5], 'OBSTACLE-{}'.format(1))
    prog += obstacle.init()
    prog += obstacle.iterate()
    prog += grovers_diffusion_operator.iterate()
    prog += obstacle.iterate()
    for i in range(3):
        prog += Program(RZ(2 * np.pi, i))
    return prog


def main():
    inputArr = [7, 5, 2, 1, 6]
    prog = find_minimum(inputArr)
    wfn = WavefunctionSimulator().wavefunction(prog)
    print(wfn)
    # prob = wfn.get_outcome_probs()
    # plotOutput(prob)


if __name__ == "__main__":
    main()
