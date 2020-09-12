import numpy as np

from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys
from scipy import linalg
from utils import testIfArrayIsUnitary
from scipy.sparse import csgraph

prog = Program()

H = np.array(
    [
        [1,  1],
        [1, -1]
    ]
)

def generateHadamardGate(rows):
    a = np.kron(H,H)
    for number in range(2,int(np.log2(rows))):
        a = np.kron(H, a)
    return a

def getNumOfOnes(arr):
    numOfOnes = 0 
    for elem in arr:
        if(elem == 1):
            numOfOnes += 1
    return numOfOnes

def getInput():
    arr = np.array([1, 1, 1, 1, 0, 0, 0, 1, ])
    return arr

def main():
    bitsNumber = 2 ** 8
    for bit in range(1, bitsNumber):
        bits = np.array(bit, dtype=np.uint8)
        inputArr = np.unpackbits(bits, axis=0)
        for numberOfMutations in range(4): 
            u = getUnitary(inputArr, numberOfMutations)
            if(testIfArrayIsUnitary(u)):
                print(bit, numberOfMutations)
                break

def getNewColumn(i, counter, column, prevColumn, lengthOfArr):
    new_column = 0
    if (i == 0):
        new_column = counter + prevColumn
    elif(i ==1):
        new_column = counter - prevColumn
    elif(i ==2):
        new_column = counter + column
    elif(i ==3):
        new_column = counter - column

    new_column = new_column % lengthOfArr
    return new_column

def getUnitary(inputArr, numOfSolution = 0):
    lengthOfArr = len(inputArr)
    numOfOnes = getNumOfOnes(inputArr)
    state = np.ones((lengthOfArr, lengthOfArr))

    for column in range(lengthOfArr):
        if(inputArr[column] == 0):
            counter = 0
            prevColumn = column
            for row in range(lengthOfArr):
                new_column = getNewColumn(numOfSolution, counter, column, prevColumn, lengthOfArr)
                state[row][new_column] = 0
                counter += 1 
                prevColumn = new_column

    hadamard = generateHadamardGate(lengthOfArr)
    u = np.multiply(hadamard,state)
    u = 1 / np.sqrt(numOfOnes) * u
    return u 
    ######################################################## 1

    # wfn = WavefunctionSimulator().wavefunction(prog)
    # prob = wfn.get_outcome_probs()
    # print(wfn)

if __name__ == "__main__":
    main()