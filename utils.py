import numpy as np
from scipy.linalg import orth

# A = np.array(
#     [
#         [1, 0],
#         [0, 1]
#     ]
# )

# A = np.sqrt(1/4) *  np.array(
#     [
#         [1, 1, 1, 1],
#         [1,-1, 1,-1],
#         [1, 1,-1,-1],
#         [1,-1,-1, 1],
#     ]
# )

# A = np.sqrt(1/2) *  np.array(
#     [
#         [0, 1, 1, 0],
#         [1, 0, 0, 1],
#         [1, 0, 0,-1],
#         [0,-1, 1, 0],
#     ]
# )

# steps for changing hadamard probabilities 
# swap 2, 4 
# diagonal 0
# sqrt(1/4) -> sqrt(1/3)
# A[element][(element+0)% (8 -1)] = 0


# A = np.sqrt(1/8) *  np.array(
#     [
#         [1, 1, 1, 1, 1, 1, 1, 1],
#         [1,-1, 1,-1, 1,-1, 1,-1],
#         [1, 1,-1,-1, 1, 1,-1,-1],
#         [1,-1,-1, 1, 1,-1,-1, 1],
#         [1, 1, 1, 1,-1,-1,-1,-1],
#         [1,-1, 1,-1,-1, 1,-1, 1],
#         [1, 1,-1,-1,-1,-1, 1, 1],
#         [1,-1,-1, 1,-1, 1, 1,-1],
#     ]
# )

def testIfArrayIsUnitary(arr):
    '''
    U U* = U* U= I
    '''
    
    arr_conjugate_transpose = np.conjugate(arr)
    arr_conjugate_transpose = np.transpose(arr_conjugate_transpose)
    # arr_conjugate_transpose = np.matrix(arr).getH()
    arrMultArrTransConj = arr.dot(arr_conjugate_transpose)
    arrMultArrTransConj = np.absolute(arrMultArrTransConj)
    arrMultArrTransConj = np.rint(arrMultArrTransConj)
    
    identityMatrix = np.identity(arr.shape[0])

    # print(arrMultArrTransConj)

    if(np.array_equal(arrMultArrTransConj,identityMatrix)):
        return True
    else:
        return False


def closestPowerOf2(value,powerOfTwo=1):
    if(value > 2 * powerOfTwo):
        return closestPowerOf2(value,2 * powerOfTwo)
    else:
        return 2 * powerOfTwo
     

def DensityArrayFromRowVector(arr):
    '''
    create density matrix from row vector 
    for creating mixed quantum states

    eg. |𝜓⟩ = 𝛼0|111⟩ + 𝛼1|101⟩ + 𝛼2|010⟩ + 𝛼3|001⟩
    '''

    '''
    eg. |𝜓⟩ = 𝛼0|111⟩|0⟩ + 𝛼1|101⟩|1⟩ + 𝛼2|010⟩|2⟩ + 𝛼3|001⟩|3⟩

    '''

    vectorLength = len(arr)
    multiplicationFactor = 1 / np.sqrt(vectorLength)

    rows = closestPowerOf2(vectorLength)

    densityMatrix = np.zeros((rows, rows), int)
    for elem in range(vectorLength):
        densityMatrix[0][arr[elem]] = 1

    pass

def mixedState(densityMatrix):
    '''
    mixed_state = densityMatrix * |0..0⟩
    '''
    pass

def rvs(dim=3):
     random_state = np.random
     H = np.eye(dim)
     D = np.ones((dim,))
     for n in range(1, dim):
         x = random_state.normal(size=(dim-n+1,))
         D[n-1] = np.sign(x[0])
         x[0] -= D[n-1]*np.sqrt((x*x).sum())
         # Householder transformation
         Hx = (np.eye(dim-n+1) - 2.*np.outer(x, x)/(x*x).sum())
         mat = np.eye(dim)
         mat[n-1:, n-1:] = Hx
         H = np.dot(H, mat)
         # Fix the last sign such that the determinant is 1
     D[-1] = (-1)**(1-(dim % 2))*D.prod()
     # Equivalent to np.dot(np.diag(D), H) but faster, apparently
     H = (D*H.T).T
     return H

def allCombinations(A, lengthOfSqrMatrix):
    for i in range(lengthOfSqrMatrix):
        for j in range(i + 1, lengthOfSqrMatrix):
            # print(i,j)
            # B = np.copy(A)
            # temp = B[i][j]
            # B[i][j] = B[j][i]
            # B[j][i] = temp    
            # print(B)
            temp = A[i][j]
            A[i][j] = A[j][i]
            A[j][i] = temp    
            unitary = testIfArrayIsUnitary(A)
            if(testIfArrayIsUnitary(A)):
                return (i,j)
                break

    return None

def allCombinations2(A, lengthOfSqrMatrix):
    for i in range(lengthOfSqrMatrix):
        for j in range(i + 1, lengthOfSqrMatrix):
            # print(i,j)
            # B = np.copy(A)
            # temp = B[i][j]
            # B[i][j] = B[j][i]
            # B[j][i] = temp    
            # print(B)
            temp = A[i][j]
            A[i][j] = A[j][i]
            A[j][i] = temp    
            unitary = testIfArrayIsUnitary(A)
            if(testIfArrayIsUnitary(A)):
                return (i,j)
                break

    return None

if __name__ == "__main__":
    A = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1,-1, 1,-1, 1,-1, 1,-1],
            [1, 1,-1,-1, 1, 1,-1,-1],
            [1,-1,-1, 1, 1,-1,-1, 1],
            [1, 1, 1, 1,-1,-1,-1,-1],
            [1,-1, 1,-1,-1, 1,-1, 1],
            [1, 1,-1,-1,-1,-1, 1, 1],
            [1,-1,-1, 1,-1, 1, 1,-1],
        ]
    )
    length = 8
    A = np.sqrt(1/7) *  A
    for element in range(length):
        A[element][(element+0)% length] = 0 
        # A[element][(element+1)% length]= 0
        # A[element][(element+2)% length]= 0
        # A[element][(element+3)% length]= 0
        # A[element][(element+4)% length]= 0        
        # A[element][(element+5)% length]= 0
        # A[element][(element+6)% length]= 0
        # A[element][(element+7)% length]= 0

    print(np.sqrt(7) * A)

    if(testIfArrayIsUnitary(A)):
        print(True)
    else:
        print(allCombinations(A, length))
    # unitary = testIfArrayIsUnitary(A)
    # print(unitary)

    A =  [0b111, 0b101, 0b010, 0b001, 0b110]
    densityMatrix = DensityArrayFromRowVector(A)


    pass
