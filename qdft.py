# https://en.wikipedia.org/wiki/Quantum_Fourier_transform

# author: Konstantinos Dalkafoukis
# qdft
from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import numpy as np

def qdft(num_of_iterations = 2):
    prog = Program()
    for i in range(num_of_iterations):
        prog += Program(H(i))
        counter = 2
        for j in range(i + 1, num_of_iterations):
            cphase = CPHASE(2 * np.pi / 2 ** counter, i ,j)
            prog += Program(cphase)
            counter = counter + 1
    return prog


def qdft_in_list_of_qubits(qubits = [0,1,2], qubit_neigboors = [[1,2],[0]]):
    prog = Program()
    for qubit in qubits:
        prog += Program(I(qubit))
    for qubit in qubits:
        prog += Program(H(qubit))
        counter = 2
        if(qubit != qubits[len(qubits) - 1]):
            for neighboor in qubit_neigboors[qubit]:
                cphase = CPHASE(2 * np.pi / 2 ** counter, qubit ,neighboor)
                prog += Program(cphase)
                counter = counter + 1
    return prog

def main():
    prog = qdft()
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    # print(prob)


if __name__ == "__main__":
    main()
