# https://en.wikipedia.org/wiki/Simon%27s_problem

# author: Konstantinos Dalkafoukis
# shor's algorithm
from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import numpy as np

def simons_algorithm():
    num_of_qubits = 3
    prog = Program()
    for i in range(num_of_qubits):
        prog += Program(H(i+num_of_qubits + 1), I(i))
        # counter = 2
        # for j in range(i + 1, num_of_iterations):
        #     cphase = CPHASE(2 * np.pi / 2 ** counter, i ,j)
        #     prog += Program(cphase)
        #     counter = counter + 1
    return prog


def main():
    prog = simons_algorithm()
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    # print(prob)
    theta = 2 * np.pi
    arr = np.array([[1, 0], [0, np.exp(1j* theta)]])
    arr = np.kron(arr, arr)

    # sC = np.sqrt(1 / 3) * np.array([[1,1,1,0]])
    # arr = np.multiply(sC, np.transpose(sC))
    # arr[3][3] = 1
    # arr = np.dot(arr, np.transpose(arr))
    print(arr)


if __name__ == "__main__":
    main()
