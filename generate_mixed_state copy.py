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

H = np.array(
    [
        [1, 1],
        [1,-1]
    ]
)


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
            arr[1][i + 0] = 1
            # arr[1][i + 0] = -1

            arr[1][i + 1] = 0
        elif(twoDigits == "10"):
            arr[0][i + 0] = 1
            arr[0][i + 1] = 0
            arr[1][i + 0] = 0
            arr[1][i + 1] = 1
            # arr[1][i + 1] = -1

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
    return "00011001"
    # return "00011011" + ''.join(reversed("00011011"))

def generate_density_matrix(state, numberOfElements):
    rows = len(state)
    A = np.zeros((rows, rows), int)
    fillFirstTwoLines(A)
    fillRestOfLines(A)

    # ///////// to be removed or replaced
    hadamardGate = generateHadamardGate(A)
    A = multiplyHadamardWithStateArray(A,hadamardGate)
    # /////////

    # ///////// dont remove
    # A[1][6] = -1
    # A[3][4] = -1
    # A[5][2] = -1
    # A[7][0] = -1
    # A[4][7] = -1
    # A[5][6] = -1
    # A[6][5] = -1
    # A[7][4] = -1
    # /////////

    # /////////
    print("array A")
    print(A)
    A = np.sqrt(1 / numberOfElements) * A
    # print("U * U -1 transpose")
    # print(testIfArrayIsUnitary(A))
    # /////////
    # /////////
    # grschmidt = gram_schmidt(A)
    # # grschmidt = np.absolute(grschmidt)
    # # grschmidt = np.rint(grschmidt)
    # print(grschmidt)
    # print(testIfArrayIsUnitary(gram_schmidt(A)))
    # /////////

    testarr = np.array([[1, 1, 1, 0, 0, 0, 0, 0]], dtype=complex)

    testarr = testarr.transpose().dot(testarr)

    df = dft(3)
    for i in range(0,3):
        for j in range(0,3):
            testarr[i][j] = df[i][j]

    for i in range(3,8):
        testarr[i][i] = np.sqrt(3) 
    testarr = 1 / np.sqrt(3) * testarr
    # print(testarr)
    print(testIfArrayIsUnitary(testarr))
    # B = np.sqrt(numberOfElements) * A
    # B = A.dot(A)
    # # print(B)
    # iden = 1/ 3 * np.identity(8)
    # res = np.linalg.solve(B, iden)
    # print(res)
    # print(testIfArrayIsUnitary(res))
    # print(np.linalg.eig(A))
    # //////////////////
    # T, Z = schur(A)
    # print(testIfArrayIsUnitary(T))
    # print(T)
    # ////////////////////

    # U = np.identity(A.shape[0]) + np.pi / 1j * A2
    # print(U)
    # print(testIfArrayIsUnitary(U))

    # a = np.multiply(dft(8),A)
    # a = (np.exp((-2 * np.pi * 1j)/ numberOfElements) / np.exp((-2 * np.pi * 1j)/ 8) )* a
    # print(a)
    # print(testIfArrayIsUnitary(a))

    # ////////////////////
    # q, r = generateQR(A)
    # print(r)
    # print(testIfArrayIsUnitary(q))
    # ////////////////////


if __name__ == "__main__":
    arr = [3,4,6]
    numberOfElements = len(arr)
    state = arrayToBinaryString(arr)
    generate_density_matrix(state, numberOfElements)
