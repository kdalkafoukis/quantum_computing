import numpy as np
from scipy.linalg import dft
from pyquil import Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import sys, random
from utils import plotOutput
import getopt, sys

def getNumberOfElements(state):
    numberOfElements = 0
    for elem in state[0]:
        if(elem == 1):
            numberOfElements = numberOfElements + 1
    return numberOfElements

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

def applyOnesToDensityMatrix(density_matrix,numberOfElements, rows):
    for i in range(0, rows):
        sum = 0
        for j in range(0, rows):
            sum = sum + abs(density_matrix[i][j])
        if(sum == 0):
            density_matrix[i][i] = np.sqrt(numberOfElements) 
    return density_matrix

def shiftedState(state):
    rows = len(state[0])

    bitWithFirstOne = 0
    for i in range(rows):
        if(abs(state[0][i]) == 1):
            bitWithFirstOne = i
            break

    number = bitWithFirstOne
    num_bits = bitWithFirstOne
    bits = [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]
    return bits

def generate_density_matrix(state, rows):
    numberOfElements = getNumberOfElements(state)
    flatDft = getFlatDft(numberOfElements)
    density_matrix = state.transpose().dot(state)
    density_matrix = getDensityDft(density_matrix, flatDft, rows)
    density_matrix = applyOnesToDensityMatrix(density_matrix,numberOfElements, rows)
    density_matrix = 1 / np.sqrt(numberOfElements) * density_matrix

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
    return multi_hot_encoder(arr, qubits)

def generateVectorForSet(arr):
    maxArr = max(arr)
    num = closestPowerOf2(maxArr)
    qubitsOfArrayElement = np.log2(num)
    
    qubits = int(qubitsOfArrayElement)
    return multi_hot_encoder(arr, qubits)

def shiftState(state, prog):
    bits = shiftedState(state)

    for position, bit in enumerate(reversed(bits)):
        if(bool(bit)):
            prog += Program(X(position))

def applyDensityMatrix(state, prog):
    rows = len(state[0])
    arr = generate_density_matrix(state, rows)

    definition = DefGate("operator", arr)
    prog += Program(definition)
    operator = definition.get_constructor()

    num_of_qubits = int(np.log2(rows))
    qubits = range(num_of_qubits)
    qbits = [qubit for qubit in reversed(qubits)]
    prog += Program(operator(*qbits))

def closestPowerOf2(value,powerOfTwo=1):
    if(value >= 2 * powerOfTwo):
        return closestPowerOf2(value,2 * powerOfTwo)
    else:
        return 2 * powerOfTwo
    
def getArray():
    return [3, 19, 21, 3, 5, 4, 29]

def getInputArray():
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "i:"
    long_options = ["input="]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        sys.exit(2)
    outputArray = []
    for current_argument, current_value in arguments:
        if current_argument in ("-i", "--input"):
            print (("Enabling input mode (%s)") % (current_value))
            outputArray = [int(x) for x in current_value if x != ',']

    return outputArray

def generateRandomMatrix():
    lengthOfArray = random.randint(1, 16)
    arr = []
    for i in range(lengthOfArray):
        coin = random.randint(0, 1)
        if(coin):
            arr.append(i)
        else:
            arr.append(0)
    return arr

def generateMixedState():
    prog = Program()
    inputArr = getArray()
    state = generateVectorForArray(inputArr)
    # state = generateVectorForSet(inputArr)
    shiftState(state, prog)
    applyDensityMatrix(state, prog)


    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    # plotOutput(prob)
    # print(prob)

    print(wfn)
    
if __name__ == "__main__":
    generateMixedState()
