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

