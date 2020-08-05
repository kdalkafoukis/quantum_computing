import numpy as np

H = np.array(
    [
        [1, 1],
        [1,-1]
    ]
)

def arrayToBinaryString(arr):
    return "01001100"
    # return "01001100"
    # return "11" 
    # return "00011011" + ''.join(reversed("00011011"))


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
    a = np.kron(H, H)
    for number in range(2,int(np.log2(rows))-1):
        a = np.kron(H, a)
    a = np.kron(a,np.array([[1,1],[1,1]]))
    return a
def multiplyHadamardWithStateArray(a,b):
    return np.multiply(a,b)

def generate_density_matrix(state, numberOfElements):
    rows = len(state)
    arr = np.zeros((rows, rows), int)
    fillFirstTwoLines(arr)
    fillRestOfLines(arr)
    hadamardGate = generateHadamardGate(arr)
    arr = multiplyHadamardWithStateArray(arr,hadamardGate)
    print(arr,numberOfElements)
    arr = np.sqrt(1 / numberOfElements) * arr
    print(testIfArrayIsUnitary(arr))

    print(arr,numberOfElements)


def testIfArrayIsUnitary(arr):
    '''
    U U* = U* U= I
    '''
    
    arr_conjugate_transpose = np.conjugate(arr)
    arr_conjugate_transpose = np.transpose(arr_conjugate_transpose)
    arrMultArrTransConj = arr.dot(arr_conjugate_transpose)
    arrMultArrTransConj = np.absolute(arrMultArrTransConj)
    arrMultArrTransConj = np.rint(arrMultArrTransConj)
    
    identityMatrix = np.identity(arr.shape[0])
    # print(arrMultArrTransConj)

    if(np.array_equal(arrMultArrTransConj,identityMatrix)):
        return True
    else:
        return False

if __name__ == "__main__":
    arr = [3,4,6]
    numberOfElements = len(arr)
    state = arrayToBinaryString(arr)
    generate_density_matrix(state, numberOfElements)
