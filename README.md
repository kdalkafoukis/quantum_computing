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

### Grover's algorithm

##### args

- 1st arg: number of qubits
- 2nd arg: key to be found
- run for eg. qubits=3 and key=0 `python grovers_algorithm.py 3 0`
