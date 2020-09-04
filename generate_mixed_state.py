import numpy as np
from scipy.linalg import orth, polar, dft, schur
from scipy import linalg
from utils import allCombinations, testIfArrayIsUnitary, gram_schmidt

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

# def getFlatDft(numberOfElements):
#     numberOfElements = numberOfElements + 1
#     dftArr = dft(numberOfElements)
#     flatDft = []
#     for i in range(1,numberOfElements):
#         for j in range(1,numberOfElements):
#             flatDft.append(dftArr[i][j])
#     return flatDft

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
    # print(flatDft)

    density_matrix = getDensityDft(density_matrix, flatDft, rows)
    density_matrix = applyOnesToDensityMatrix(density_matrix,numberOfElements, rows)

    density_matrix = 1 / np.sqrt(numberOfElements) * density_matrix
    # print(density_matrix)
    # print(testIfArrayIsUnitary(density_matrix))
    return density_matrix


if __name__ == "__main__":
    generate_density_matrix()
