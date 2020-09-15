import numpy as np
from scipy.linalg import orth, polar, dft, schur
from scipy import linalg
from utils import allCombinations, testIfArrayIsUnitary, gram_schmidt

testArray = np.array(
    [
        [1,  0,  0,  0,  0,  0,  1,  1],
        [0,  1,  0,  0,  0,  0,  1, -1],
        [0,  0,  1,  0,  0,  0,  0, 0],
        [0,  0,  0,  1,  0,  0,  0, 0],
        
        [0,  0,  0,  0,  1,  0,  0, 0],
        [0,  0,  0,  0,  0,  1,  0, 0],
        [1,  1,  0,  0,  0,  0,  1,  0],
        [1, -1,  0,  0,  0,  0,  0,  1],
    ]
)

H = np.array([[1, 1],[1,-1]])


def fillFirstTwoLines(arr):
    rows = len(arr)
    for i in range(0,rows,2):
        twoDigits = state[i:i + 2]
        if(twoDigits == "00"):
            arr[0][i + 0] = 0
            arr[0][i + 1] = 0
            arr[1][i + 0] = 0
            arr[1][i + 1] = 0
        elif(twoDigits == "01"):
            arr[0][i + 0] = 0
            arr[0][i + 1] = 1
            arr[1][i + 0] = -1
            arr[1][i + 1] = 0
        elif(twoDigits == "10"):
            arr[0][i + 0] = 1
            arr[0][i + 1] = 0
            arr[1][i + 0] = 0
            arr[1][i + 1] = 1
        elif(twoDigits == "11"):
            arr[0][i + 0] = 1
            arr[0][i + 1] = 1
            arr[1][i + 0] = 1
            arr[1][i + 1] = -1 
    

def fillRestOfLines(arr):
    rows = len(arr)
    for number in range(1,int(np.log2(rows))):
        sizeOfArray = 2 ** number        
        counter =  0
        for k in range(0,rows,sizeOfArray):
            for i in range(sizeOfArray):
                for j in range(sizeOfArray):
                    if(counter % 2 == 0):
                        column = min(j + k + sizeOfArray,rows - 1)
                    else:
                        column = max(j + k - sizeOfArray,0)
                    arr[i + sizeOfArray][column] = arr[i][j + k]
            counter =  counter + 1


def generateHadamardGate(arr):
    rows = len(arr)
    a = np.kron(H,H)
    for number in range(2,int(np.log2(rows))-1):
        a = np.kron(H, a)
    a = np.kron(a,np.array([[1,1],[1,1]]))
    return a

def multiplyHadamardWithStateArray(a,b):
    return np.multiply(a,b)

def generateQR(A):
    q, r = np.linalg.qr(A)
    # print(q)
    # print(r)
    return q, r

def arrayToBinaryString(arr):
    # return "0100"
    return "11100000"
    # return "00011011" + ''.join(reversed("00011011"))

def mappingMatrix(rows, moving_number = 0):
    mapping_matrix = np.zeros((rows,rows))
    for i in range(0,rows,2):
        mapping_matrix[i][(i + moving_number) % rows] = 1
        mapping_matrix[(i + 1) % rows ][(i + 1 + moving_number) % rows] = 1
        mapping_matrix[i][(i + moving_number + 1) % rows] = 1
        mapping_matrix[(i + 1) % rows ][(i  + moving_number) % rows] = 1



    return mapping_matrix

# def fillRestOfLines(arr):
#     rows = len(arr)
#     temp = np.array([[0, 0],[0, 0]],int)
#     for i in range(0,rows,2):
#         twoDigits = state[i:i + 2]
#         if(twoDigits == "00"):
#             temp = np.array([[0, 0], [0, 0]],int)
#         elif(twoDigits == "01"):
#             temp = np.array([[0, 1], [-1, 0]],int)
#         elif(twoDigits == "10"):
#             temp = np.array([[1, 0], [0, 1]],int)
#         elif(twoDigits == "11"):
#             temp = np.array([[1, 1], [1, -1]],int)
        
#         qubits = int(np.log2(rows))
#         a = 0
#         # mapping_matrix = mappingMatrix(rows, 1)
#         # print(mapping_matrix)
#         for qubit in range(qubits):
#             if (qubit == 0):
#                 mapping_matrix = mappingMatrix(rows,0)

#             else:
#                 mapping_matrix = mappingMatrix(rows, 2 ** qubit)

#             print(mapping_matrix)
#             # a = np.kron(mappingMatrix(rows, 2 ** qubit), temp)
        
            
def generate_density_matrix(state, numberOfElements):
    rows = len(state)
    A = np.zeros((rows, rows), int)
    fillFirstTwoLines(A)
    fillRestOfLines(A)

    # ///////// to be removed or replaced
    # hadamardGate = generateHadamardGate(A)
    # A = multiplyHadamardWithStateArray(A,hadamardGate)
    # /////////

    A[2][0] = -1
    A[3][1] = -1
    A[6][4] = -1
    A[7][5] = -1

    Xgate = np.array([[0,1],[1,0]])
    negXgate = np.array([[0,1],[-1,0]])
    Zgate = np.array([[1,0],[0,-1]])
    Igate = np.array([[1,0],[0, 1]])
    H = np.array([[1, 1],[1, -1]])
    # ///////////////////////////////////
    a1 = np.kron(Xgate, Igate)
    a1 = np.kron(Igate, a1)

    # Xgate or negXgate, Igate or Zgate
    a2 = np.kron(Igate, negXgate)
    a2 = np.kron(Zgate, a2)
    # print(a2)
    a3 = np.kron(negXgate, H)
    a3 = np.kron(negXgate, a3)

    a4= np.kron(Igate, H)
    a4 = np.kron(Xgate, a4)
    print(a2 + a3 + a4 + a1)
    # print((1/np.sqrt(4))* (1j*a1 + a2 + a3))
    print(testIfArrayIsUnitary((1/np.sqrt(6))* (a2 + a3 + a4 + a1)))
    # ///////////////////////////////////

    # /////////
    # print("array A")
    # print(A)
    # print(testIfArrayIsUnitary(A))
    # A = np.sqrt(1 / numberOfElements) * A

def whatever(A,rows):
    for i in range(len(A)):
        # print(A[i])
        sum = 0
        for j in range(0, rows):
            sum = sum + abs(A[i][j])
        print(sum)

if __name__ == "__main__":
    arr = [3,4,6]
    numberOfElements = len(arr)
    state = arrayToBinaryString(arr)
    generate_density_matrix(state, numberOfElements)
