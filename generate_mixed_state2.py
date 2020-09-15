import numpy as np
from scipy.linalg import orth, polar, dft, schur
from scipy import linalg
from utils import allCombinations, testIfArrayIsUnitary, gram_schmidt

def arrayToBinaryString(arr):
    return "11110001"
    # return "00011011" + ''.join(reversed("00011011"))

def generateAll8bitNumbers():
    arr = []
    for i in range(2 ** 8):
        arr.append('{:08b}\n'.format(i))          
    return arr

def randomArray():
    arr = []
    for i in range(2 ** 8):
        arr.append('{:08b}\n'.format(i))          
    return arr

def generate_density_matrix(state):
    rows = len(state)

    Xgate = np.array([[0,1],[1,0]])
    negXgate = np.array([[0,1],[-1,0]])
    Zgate = np.array([[1,0],[0,-1]])
    Igate = np.array([[1,0],[0, 1]])
    H = np.array([[1, 1],[1, 1]])
    # H = np.array([[1, 1],[1, -1]])
    ZeroGate = np.array([[0,0],[0,0]])

    transition1 = [Igate, Zgate]
    transition2 = [Xgate, negXgate]
    counter = 0
    arr = np.zeros((rows, rows))

    for i in range(0,rows,2):
        twoDigits = state[i:i + 2]
        gate = []
        if(twoDigits == "00"):
            gate = [ZeroGate]
        elif(twoDigits == "01"):
            gate = [Xgate, negXgate]
        elif(twoDigits == "10"):
            gate = [Zgate, Igate]
        elif(twoDigits == "11"):
            gate = [H]

        a = np.zeros((rows, rows))
        if(counter == 0):
            a = np.kron(transition1[0], gate[0])
            a = np.kron(transition1[0], a)
        elif(counter == 1):
            a = np.kron(transition2[0], gate[0])
            a = np.kron(transition1[0], a)
        elif(counter == 2):
            a= np.kron(transition1[0], gate[0])
            a = np.kron(transition2[0], a)      
        elif(counter == 3):
            a = np.kron(transition2[0], gate[0])
            a = np.kron(transition2[0], a)
        counter += 1
        arr = arr + a

    # arr = arr + 1j * arr 
    # print(arr)
    # print(linalg.lu( arr))
    # arr = 1/np.sqrt(5) * arr
    # print(testIfArrayIsUnitary(arr))

    arr_conjugate_transpose = np.conjugate(arr)
    arr_conjugate_transpose = np.transpose(arr_conjugate_transpose)
    # arr_conjugate_transpose = np.matrix(arr).getH()
    arrMultArrTransConj = arr.dot(arr_conjugate_transpose)
    arrMultArrTransConj = arrMultArrTransConj
    # arrMultArrTransConj = np.rint(arrMultArrTransConj)
    # print(arrMultArrTransConj)

    # print(testIfArrayIsUnitary(gram_schmidt(arr)))
    arrMultArrTransConj = np.transpose(arrMultArrTransConj)
    inverse = linalg.solve(arrMultArrTransConj, np.identity(8))
    arr= arr.dot(inverse)
    # arr= inverse.dot(arr)
    arr = np.rint(arr)
    print(1/np.sqrt(5)  * inverse)
    print(testIfArrayIsUnitary(arr))

    # s, v, d = np.linalg.svd(arr)
    # q, r = np.linalg.qr(arr)
    # l = linalg.schur(arr)
    # print(linalg.lu( arr))
    # print(testIfArrayIsUnitary(l[0]))
    # print(q)
    # print(linalg.eig(arr))
    # print(linalg.solve(arrMultArrTransConj, np.identity(8)))
   
    # print(np.linalg.eig(arrMultArrTransConj), np.identity(8))
    # print(np.linalg.eigh(arr))
    # print(linalg.orth((1/np.sqrt(5)) * arr))
    # print(np.linalg.qr(arr))
    # print(arr)
    # print(testIfArrayIsUnitary(arr))
    # ///////////////////////////////////
    # a1 = np.kron(Xgate, Igate)
    # a1 = np.kron(Igate, a1)
    # # Xgate or negXgate, Igate or Zgate
    # a2 = np.kron(Igate, negXgate)
    # a2 = np.kron(Zgate, a2)
    # # print(a2)
    # a3 = np.kron(negXgate, H)
    # a3 = np.kron(negXgate, a3)

    # a4= np.kron(Igate, H)
    # a4 = np.kron(Xgate, a4)
    # print(a2 + a3 + a4 + a1)
    # # print((1/np.sqrt(4))* (1j*a1 + a2 + a3))
    # print(testIfArrayIsUnitary((1/np.sqrt(6))* (a2 + a3 + a4 + a1)))

if __name__ == "__main__":
    arr = [3,4,6]
    numberOfElements = len(arr)
    strings = generateAll8bitNumbers()
    # for state in strings:
        # generate_density_matrix(state)
    state = arrayToBinaryString(arr)
    generate_density_matrix(state)
