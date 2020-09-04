import numpy as np
from scipy.linalg import dft
from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.api import local_forest_runtime, WavefunctionSimulator
import numpy as np
import sys

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

def shiftedState(state, rows):
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
    density_matrix = state.transpose().dot(state)
    numberOfElements = getNumberOfElements(state)
    flatDft = getFlatDft(numberOfElements)

    density_matrix = getDensityDft(density_matrix, flatDft, rows)
    density_matrix = applyOnesToDensityMatrix(density_matrix,numberOfElements, rows)
    density_matrix = 1 / np.sqrt(numberOfElements) * density_matrix

    return density_matrix

def generateState(arr):
    state = np.array([[
        0, 1, 1, 1, 
        0, 1, 1, 1, 
    ]], dtype=complex)
    return state

def shiftState(state, rows, prog):
    bits = shiftedState(state, rows)

    for position, bit in enumerate(reversed(bits)):
        if(bool(bit)):
            prog += Program(X(position))

def applyDensityMatrix(state, rows, prog):
    arr = generate_density_matrix(state, rows)

    definition = DefGate("operator", arr)
    prog += Program(definition)
    operator = definition.get_constructor()

    num_of_qubits = int(np.log2(rows))
    qubits = range(num_of_qubits)
    qbits = [qubit for qubit in reversed(qubits)]
    prog += Program(operator(*qbits))

def generateMixedState():
    prog = Program()

    state = generateState([])
    rows = len(state[0])
    shiftState(state, rows, prog)
    applyDensityMatrix(state, rows, prog)

    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()

    print(wfn)
    # print(prob)
    
if __name__ == "__main__":
    generateMixedState()
