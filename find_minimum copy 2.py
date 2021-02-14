# https://arxiv.org/abs/quant-ph/9607014
# author: Konstantinos Dalkafoukis
from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys
from utils import plotOutput
from generate_mixed_state import getState, generateVectorForArray

def groverCoin(gateName):
    arr = [4,3,5,7]
    length = len(arr)
    num_of_qubits = 6

    initArr  = generateVectorForArray(arr)

    sC = np.sqrt(1 / length) * initArr
    sCproduct = np.multiply(sC, np.transpose(sC))
    G = 2 * sCproduct - np.identity(2 ** num_of_qubits)
    arr = G
    definition = DefGate(gateName, arr)
    print(G)
    return definition

def findMinimum(prog):
    arr = getInput()
    num_of_qubits = 6
    positionQubits = 3
    qubits = range(num_of_qubits)

    groverCoinDefinition = groverCoin("groverCoin")
    prog += Program(groverCoinDefinition)
    groverCoinOperator = groverCoinDefinition.get_constructor()

    positionQubits = 1
    for i in range(positionQubits):
        prog += Program(RZ(np.pi,i))
        prog += Program(groverCoinOperator(5,4,3,2,1,0))
    return prog

def getInput():
    return [2,3,5,7]

def main():
# //////////////////
    prog = Program()
# //////////////////
    arr = getInput()
    prog = getState(prog,arr,'array')
# ////////////////// find minimum
    prog = findMinimum(prog)

# //////////////////
    wfn = WavefunctionSimulator().wavefunction(prog)
    print(wfn)
    prob = wfn.get_outcome_probs()
    # plotOutput(prob)


if __name__ == "__main__":
    main()
