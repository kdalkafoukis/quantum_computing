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

def TestSpecificArray():
    arr = np.array([1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1])
    createUnitary(arr)


def testAllCombinations():
    numberOfUnitaries = 0

    number = 8
    bitsNumber = 2 ** number
    for bit in range(1, bitsNumber):
        bits = [(bit >> b) & 1 for b in range(number - 1, -1, -1)]
        inputArr = np.array(bits)
        numberOfUnitaries += createUnitary(inputArr)

    print(numberOfUnitaries)


def createUnitary(inputArr):
    numberOfUnitaries = 0
    bit = np.packbits(inputArr)

    isArrayIsUnitary = False
    for numberOfMutations in range(5): 
        u = getUnitary(inputArr, numberOfMutations)
        if(testIfArrayIsUnitary(u)):
            isArrayIsUnitary = True
            numberOfUnitaries = 1
            # print(numberOfUnitaries, numberOfMutations)
            break
    if(not isArrayIsUnitary):
        print('bit: ', bit)
    return numberOfUnitaries

 

def getNewColumn(i, counter, column, prevColumn, lengthOfArr):
    new_column = 0
    if (i == 0):
        new_column = counter + prevColumn
    elif(i == 1):
        new_column = - counter + prevColumn
    elif(i == 2):
        new_column = counter + column
    elif(i == 3):
        new_column = - counter + column

    # elif(i == 4):
    #     new_column = counter + 2 * column
    # elif(i == 5):
    #     new_column = - counter + 2 * column
    # elif(i == 6):
    #     new_column = counter + 2 * prevColumn
    # elif(i == 7):
    #     new_column = - counter + 2 * prevColumn


    # # elif(i == 8):
    # #     new_column = counter + 3 * column
    # # elif(i == 9):
    # #     new_column = - counter + 3 * column
    # # elif(i == 10):
    # #     new_column = counter + 3 * prevColumn
    # # elif(i == 11):
    # #     new_column = - counter + 3 * prevColumn


    # # # elif(i == 12):
    # # #     new_column = counter + 4 * column
    # # # elif(i == 13):
    # # #     new_column = - counter + 4 * column
    # # # elif(i == 14):
    # # #     new_column = counter + 4 * prevColumn
    # # # elif(i == 15):
    # # #     new_column = - counter + 4 * prevColumn


    # # # elif(i == 16):
    # # #     new_column = counter + 5 * column
    # # # elif(i == 17):
    # # #     new_column = - counter + 5 * column
    # # # elif(i == 18):
    # # #     new_column = counter + 5 * prevColumn
    # # # elif(i == 19):
    # # #     new_column = - counter + 5 * prevColumn

    
    # # # elif(i == 20):
    # # #     new_column = counter + 6 * column
    # # # elif(i == 21):
    # # #     new_column = - counter + 6 * column
    # # # elif(i == 22):
    # # #     new_column = counter + 6 * prevColumn
    # # # elif(i == 23):
    # # #     new_column = - counter + 6 * prevColumn

    # # # elif(i == 24):
    # # #     new_column = counter + 7 * column
    # # # elif(i == 25):
    # # #     new_column = - counter + 7 * column
    # # # elif(i == 27):
    # # #     new_column = counter + 7 * prevColumn
    # # # elif(i == 27):
    # # #     new_column = - counter + 7 * prevColumn

    # elif(i == 28):
    #     new_column = counter + 8 * column
    # elif(i == 29):
    #     new_column = - counter + 8 * column
    # elif(i == 30):
    #     new_column = counter + 8 * prevColumn
    # elif(i == 31):
    #     new_column = - counter + 8 * prevColumn
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

def main():
    # TestSpecificArray()
    testAllCombinations()

if __name__ == "__main__":
    main()

######################################################## 
# wfn = WavefunctionSimulator().wavefunction(prog)
# prob = wfn.get_outcome_probs()
# print(wfn)