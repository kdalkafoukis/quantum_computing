# https://arxiv.org/abs/quant-ph/9607014
# author: Konstantinos Dalkafoukis
from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys
from utils import plotOutput
from generate_mixed_state import getState, generateVectorForArray, closestPowerOf2

def groverCoin(gateName):
    arr = getInput()
    num_of_elements = len(arr)
    initArr  = generateVectorForArray(arr)
    num_of_qubits = int(np.log2(len(initArr[0])))
    sC = np.sqrt(1 / num_of_elements) * initArr
    sCproduct = np.multiply(sC, np.transpose(sC))
    G = 2 * sCproduct - np.identity(2 ** num_of_qubits)
    arr = G
    definition = DefGate(gateName, arr)
    return definition

class Obstacle:
    def __init__(self, qubits, key, gateName):
        rows = 2 ** len(qubits)
        arr = np.zeros((rows, rows), int)

        for row in range(rows):
            diagonal_element = 1
            if(row & 0b0001111 >= key):
                diagonal_element = -1

            arr[row][row] = diagonal_element

        self.obstacle_definition = DefGate(gateName, arr)
        self.qubits = qubits

    def init(self):
        return Program(self.obstacle_definition)

    def iterate(self):
        OBSTACLE = self.obstacle_definition.get_constructor()
        qbits = [qubit for qubit in (self.qubits)]
        # qbits = [qubit for qubit in reversed(self.qubits)]

        return Program(OBSTACLE(*qbits))

def findMinimum(prog):
    arr = getInput()

    lengthOfArr = len(arr)
    qubitsOfPosition = closestPowerOf2(lengthOfArr - 1)
    qubitsOfPosition = int(np.log2(qubitsOfPosition))


    maxArr = max(arr)
    num = closestPowerOf2(maxArr)
    qubitsOfArrayElement = int(np.log2(num))
    qubitsAll = qubitsOfArrayElement + qubitsOfPosition
    qubitsInTotal = range(qubitsAll)
    qubits = [qubit for qubit in reversed(qubitsInTotal)]


    print(qubitsOfArrayElement, qubitsOfPosition, qubitsAll)
    groverCoinDefinition = groverCoin("groverCoin")
    prog += Program(groverCoinDefinition)
    groverCoinOperator = groverCoinDefinition.get_constructor()

    # prog += Program(RZ(np.pi,qubitsOfArrayElement - i - 1))

    # for i in range(1):
    #     print(2 ** (qubitsOfArrayElement - i - 1))
    #     obstacle = Obstacle(qubits,2 ** (qubitsOfArrayElement - i - 1), "obstacle-" + str(i))
    #     prog += obstacle.init()
    #     prog += obstacle.iterate()

    #     prog += Program(groverCoinOperator(*qubits))


    # for i in range(1):
        # prog += Program(RZ(np.pi,i))
        # prog += Program(RZ(np.pi,qubitsOfArrayElement - i - 1))
        # prog += Program(Z(qubitsOfArrayElement - i - 1))
        # prog += Program(groverCoinOperator(*qubits))

    prog += Program(Z(3))
    # prog += Program(groverCoinOperator(*qubits))
    # prog += Program(Z(3))
    # prog += Program(Z(2))
    # prog += Program(groverCoinOperator(*qubits))
    # prog += Program(Z(2))
    # prog += Program(Z(1))
    # prog += Program(groverCoinOperator(*qubits))
    # prog += Program(Z(1))
    # prog += Program(Z(0))
    # prog += Program(groverCoinOperator(*qubits))
    # prog += Program(Z(0))
    return prog

def diffusion_iterations(qubits):
    return ((np.pi / 4) * np.sqrt(2 ** len(qubits))).astype(int)

def getInput():
    return [7, 3, 2, 15, 6, 14, 13]

def main():
    prog = Program()
    arr = getInput()
    prog = getState(prog,arr,'array')
    prog = findMinimum(prog)
    wfn = WavefunctionSimulator().wavefunction(prog)
    print(wfn)
    prob = wfn.get_outcome_probs()
    # plotOutput(prob)


if __name__ == "__main__":
    main()
