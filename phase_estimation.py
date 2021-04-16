# https://en.wikipedia.org/wiki/Quantum_phase_estimation_algorithm

# author: Konstantinos Dalkafoukis
# Quantum phase estimation
from pyquil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys


def qft_dagger(num_of_iterations):
    prog = Program()
    for qubit in range(num_of_iterations//2):
        prog += Program(SWAP(qubit, num_of_iterations - qubit-1))
    for i in range(num_of_iterations):
        for j in range(i):
            cphase = CPHASE(-1 * np.pi / 2**(i-j), j, i)
            prog += Program(cphase)
        prog += Program(H(i))
    return prog


def applyHadamard(n):
    prog = Program()
    for qubit in range(n):
        prog += Program(H(qubit))
    return prog


def controlUnitary(n, theta):
    prog = Program()
    for qubit in range(n):
        for _ in range(2 ** qubit):
            prog += Program(PHASE(theta, n).controlled(qubit))
    return prog


def phase_estimation(theta, n):
    prog = Program()
    prog += Program(X(n))
    prog += applyHadamard(n)
    prog += controlUnitary(n, theta)
    prog += qft_dagger(n)
    return prog


def caclulatePhase(prob, n):
    maximum_value = -1
    maximum_key = -1
    for key, value in prob.items():
        if (value > maximum_value):
            maximum_value = value
            maximum_key = key
    maximum_key = maximum_key[1:]
    return int(maximum_key, 2) / 2 ** n


def getInput(argv):
    qubits = 3
    theta = 1 / 4
    if (len(argv) >= 2):
        try:
            temp = argv[1].strip().split('/')
            temp = list(map(lambda x: int(x), temp))
            if len(temp) == 2:
                theta = temp[0] / temp[1]
                qubits = int(argv[0])
        except ValueError:
            pass
    return qubits, theta


def main(argv):
    qubits, theta = getInput(argv)
    angle = 2 * np.pi * theta
    prog = phase_estimation(angle, qubits)
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    approximatedTheta = caclulatePhase(prob, qubits)
    print('qubits:', qubits)
    print('theta:', theta)
    print('approximated theta:', approximatedTheta)


if __name__ == "__main__":
    main(sys.argv[1:])
