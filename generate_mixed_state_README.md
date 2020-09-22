# Generate quantum state in superposition from an array of numbers

## Description
Given an array of numbers we want to generate this state in a quantum computer.  

The array can represent an array with the first qubits being the position qubits coming
from the number of elements and the position bits in the array and the rest qubits being are the value of the number.

It could solve the same problem for sets by removing position qubits.
The 

It's state preparation for problems such as searching problems, finding the minimum and many other problems and subproblems.

## example

### input

- python array with positive numbers `[3, 8, 5, 15, 2]`

### output 

- `(0.4472135955+0j)|0000011> + (0.4472135955+0j)|0011000> + (0.4472135955+0j)|0100101> + (0.4472135955+0j)|0111111> + (0.4472135955+0j)|1000010>`

- the first 3 bits are the position bits  
- the other 4 bits are for the number value

## architecture

1. handling input
2. generate the classical vector state from formatted input
3. intialize quantum state  
4. create unitary operator to transform the initial state  
5. handling output

### 1. handling input

get input from the user in python array form
the array has positive numbers
eg. `A =` `[3, 8, 5, 15, 2]`

### 2. generate the classical vector state from formatted input

generate the state combining position and value element

- position_qubits: find the log2(x) of the closest power of two from the number of elements in the array  
`position_qubits = log2(closest_power(lengthOf(A)) = log2(closest_power(5)) = log2(8) = 3 `
- value_qubits: find the log2(x) of the closest power of maximum of the elemnts in the array  
`value_qubits = log2(closest_power(maxOf(A)) = log2(closest_power(15)) = log2(16) = 4 `  
- combined_number: shift position bits by value qubits and add both of them and create new array  
`number of combined qubits = position_qubits + combined_number = 7 `

```
A=loop(A): a[i] = (i <<  position_qubits) + a[i]

A = [
    (0 << 4) + 3 = 000 0000 + 000 0011 = 3,
    (1 << 4) + 8 = 001 0000 + 000 1000 = 24,
    (2 << 4) + 5 = 010 0000 + 000 0101 = 7,
    (3 << 4) + 15 = 011 0000 + 000 1111 = 63,
    (4 << 4) + 2 = 100 0000 + 000 0010 = 65
]
```

- one_hot_vector: zeros in length equal to the power of combined_number and ones to the index of the number from the combined numbers

```
Vector = emptyVectorOfSize(2powerof(combined_number)) + loop(A): emptyVectorOfSize(A[i]) = 1) 

Vector = [0, 0, 0, 1, 0, 0, 0, 1, ...1, ...1, ...1, ...0]
```

### 3. intialize quantum state  

get min from the vector
shift quantum state from |0...0> to |f(x) = min(Vector), x belongs to [0,1]...x, x belongs to [0,1]>  
```
minOf(Vector) = 3
|000 0000> = |000 0011>
```
### 4. create unitary operator to transform the initial state  
calculate the dft with size the number of elements in the array
DFT = DFT(number_of_elements)
calculate the flat version of the array by transforming the k x k array to a (k x k) x 1 array
flatDFT = flatMap(DFT)

| y > = |one_hot_vector>

calculate the outer product of the one_hot_vector `|y><y|`

A = | y > < y |
loop through the outer product array and apply the flatDFT to the non zero elements
B = elementbyElementMultiply(flatDFT * A)

then apply ones to the diagonal elements that the the sum of the columns it's zero to 
make it almost unitary

Ualmost = B + diagonalWithZerosInNonZeroColumns
As last step devide the array with the sqrt of number_of_elements to make it unitary

U = 1 / np.sqrt(numberOfElements) * Ualmost


### 5. handling output

print the quantum state on the console

