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

def findMinimum(prog):
    arr = getInput()

    lengthOfArr = len(arr)
    qubitsOfPosition = closestPowerOf2(lengthOfArr)
    qubitsOfPosition = int(np.log2(qubitsOfPosition))


    maxArr = max(arr)
    num = closestPowerOf2(maxArr)
    qubitsOfArrayElement = np.log2(num)
    
    qubitsInTotal = int(qubitsOfArrayElement + qubitsOfPosition)
    qubits = range(qubitsInTotal)

    print(qubits, qubitsOfPosition)
    groverCoinDefinition = groverCoin("groverCoin")
    prog += Program(groverCoinDefinition)
    groverCoinOperator = groverCoinDefinition.get_constructor()

    for i in range(qubitsOfPosition):
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
