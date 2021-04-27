# quantum_computing

Experimental repository

# Quil

- https://github.com/rigetti/pyquil
- https://arxiv.org/abs/1608.03355
- https://pyquil.readthedocs.io/en/stable/start.html
- https://buildmedia.readthedocs.org/media/pdf/pyquil/latest/pyquil.pdf

### two consoles

### CONSOLE 1

`qvm -S`

### CONSOLE 2

`quilc -S`

### quantum random walk on the line

##### args

- 1st arg: number of iterations
- run for eg. two iterations `python random_walks_on_the_line.py 2`

### quantum random walk on the qube

##### args

- 1st arg: number of iterations
- run for eg. two iterations `python random_walks_on_the_cube.py 2`

### Grover's algorithm

##### args

- 1st arg: number of qubits
- 2nd arg: key to be found
- run for eg. qubits=3 and key=0 `python grovers_algorithm.py 3 0`

### Generate superposition state algorithm

run  
`python generate_superposition_state.py`  
to test see the array `[3, 19, 21, 3, 5, 4, 29]`

expected result: `(0.377964473+0j)|00000011> + (0.377964473+0j)|00110011> + (0.377964473+0j)|01010101> + (0.377964473+0j)|01100011> + (0.377964473+0j)|10000101> + (0.377964473+0j)|10100100> + (0.377964473+0j)|11011101>`

first 3 qubits are the position of the element  
last 5 ones are for the value of the array element

### Phase estimation algorithm

##### args

- 1st arg: number of qubits for approximation
- 2nd arg: theta to be approximated
- run for eg. qubits=3 and theta=1/4 `python grovers_algorithm.py 3 1/4`

### Alternate Minimum Algorithm

run `python finding_minimum.py`

note: works for a subset of possible cases

'''
The current design of the algorithm requires that the number of binary numbers with
first digit 0 should be strictly less than the number of binary numbers with first digit 1
'''

### Quantum state preparation

`python quantum_state_preparation.py`

##### results

```
input arr:  [0.17320508075688773, 0.2645751311064591, 0.3872983346207417, 0.22360679774997896, 0.31622776601683794, 0.5477225575051661, 0.4472135954999579, 0.31622776601683794]

wave function:  (0.1732050808+0j)|000> + (0.2645751311+0j)|001> + (0.3872983346+0j)|010> + (0.2236067977+0j)|011> + + (0.316227766+0j)|100> + (0.5477225575+0j)|101> + (0.4472135955+0j)|110> + (0.316227766+0j)|111>
```
