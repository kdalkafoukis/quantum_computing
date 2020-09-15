import numpy as np
from scipy.linalg import dft
from pyquil import Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import sys, random

def getFlatDft(numberOfElements):
    dftArr = dft(numberOfElements)
    flatDft = []
    for i in range(0,numberOfElements):
        for j in range(0,numberOfElements):
            flatDft.append(dftArr[i][j])
    return flatDft

def getDensityDft(density_matrix, flatDft, rows):
    counter = 0
    for i in range(0,rows):
        for j in range(0,rows):
            if(density_matrix[i][j] != 0):
                density_matrix[i][j] = flatDft[counter]
                counter = counter + 1
    return density_matrix

def applyOnesToDensityMatrix(density_matrix, arr, rows):
    for i in range(len(arr), rows):
        density_matrix[i][i] = np.sqrt(len(arr)) 
    return density_matrix

def generate_density_matrix(inputArr, state, rows):
    density_matrix = state.transpose().dot(state)
    flatDft = getFlatDft(len(inputArr))

    density_matrix = getDensityDft(density_matrix, flatDft, rows)
    density_matrix = applyOnesToDensityMatrix(density_matrix, inputArr, rows)
    density_matrix = 1 / np.sqrt(len(inputArr)) * density_matrix
    return density_matrix

def multi_hot_encoder(arr, qubits):
    state = np.zeros((2** qubits),complex)
    for i in arr:
        state[i] = 1
    state = np.array([state],complex)
    return state

def generateVectorForArray(arr):
    lengthOfArr = len(arr)
    qubitsOfPosition = closestPowerOf2(lengthOfArr)
    qubitsOfPosition = np.log2(qubitsOfPosition)

    maxArr = max(arr)
    num = closestPowerOf2(maxArr)
    qubitsOfArrayElement = np.log2(num)

    for i in range(len(arr)):
        bstr = np.uint64(i)  << np.uint64(qubitsOfArrayElement)
        bstr = bstr + np.uint64(arr[i]) 
        arr[i]= int(bstr)
    
    qubits = int(qubitsOfPosition + qubitsOfArrayElement)
    return multi_hot_encoder(arr, qubits), qubits

def generateVectorForSet(arr):
    maxArr = max(arr)
    num = closestPowerOf2(maxArr)
    qubitsOfArrayElement = np.log2(num)
    
    qubits = int(qubitsOfArrayElement)
    return multi_hot_encoder(arr, qubits), qubits

def intializeQuantumState(state, number, prog):
    bits = [(number >> bit) & 1 for bit in range(number - 1, -1, -1)]
    for position, bit in enumerate(reversed(bits)):
        if(bool(bit)):
            prog += Program(X(position))

def applyDensityMatrix(inputArr, numOfQubits, state, prog):

    rows = 2 ** numOfQubits
    array = generate_density_matrix(inputArr, state, rows)
    print(array)

    definition = DefGate("operator", array)
    prog += Program(definition)
    operator = definition.get_constructor()

    num_of_qubits = int(np.log2(rows))
    qubits = range(num_of_qubits)
    qbits = [qubit for qubit in reversed(qubits)]
    prog += Program(operator(*qbits))

def closestPowerOf2(value,powerOfTwo=1):
    if(value > 2 * powerOfTwo):
        return closestPowerOf2(value,2 * powerOfTwo)
    else:
        return 2 * powerOfTwo
    
def someArray():
    return [3, 5, 4]

def getInputArray(argv):
    return someArray()

def readInputArray(argv):
    return np.fromstring(argv[0],dtype=int,sep=', ')

def generateRandomArray(num):
    lengthOfArray = random.randint(1, num)
    arr = []
    for i in range(lengthOfArray):
        coin = random.randint(0, 1)
        if(coin):
            arr.append(i)
        else:
            arr.append(0)
    return arr

def generateState(argv):
    prog = Program()
    inputArr = getInputArray(argv)
    # state, numOfQubits = generateVectorForArray(inputArr)
    state, numOfQubits = generateVectorForSet(inputArr)

    intializeQuantumState(state, numOfQubits, prog)
    applyDensityMatrix(inputArr, numOfQubits, state, prog)

    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()

    print(wfn)
    # print(prob)
    
if __name__ == "__main__":
    generateState(sys.argv[1:])
