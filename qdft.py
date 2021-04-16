# https://en.wikipedia.org/wiki/Quantum_Fourier_transform

# author: Konstantinos Dalkafoukis
# qdft
from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys


def applyXgate(num):
    prog = Program()
    counter = 0
    for i in format(num, 'b'):
        if i == '1':
            prog += Program(X(int(counter)))
        counter += 1
    return prog


def getInput(argv):
    number = 0
    qubits = 2
    if (len(argv) == 2 and 2 ** int(argv[0]) > int(argv[1])):
        try:
            qubits = int(argv[0])
            number = int(argv[1])
            print('input')
            print('qubits:', qubits)
            print('number:', number)
        except ValueError:
            pass
    return number, qubits


def qdft(qubits=2, num=1):
    prog = Program()
    prog += applyXgate(num)
    for i in range(qubits):
        prog += Program(H(i))
        counter = 2
        for j in range(i + 1, qubits):
            cphase = CPHASE(2 * np.pi / 2 ** counter, i, j)
            prog += Program(cphase)
            counter = counter + 1
    return prog


def qdft_in_list_of_qubits(qubits=[0, 1, 2], qubit_neigboors=[[1, 2], [0]]):
    prog = Program()
    for qubit in qubits:
        prog += Program(I(qubit))
    for qubit in qubits:
        prog += Program(H(qubit))
        counter = 2
        if(qubit != qubits[len(qubits) - 1]):
            for neighboor in qubit_neigboors[qubit]:
                cphase = CPHASE(2 * np.pi / 2 ** counter, qubit, neighboor)
                prog += Program(cphase)
                counter = counter + 1
    return prog


def main(argv):
    number, qubits = getInput(argv)
    prog = qdft(qubits, number)
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    # print(prob)


if __name__ == "__main__":
    main(sys.argv[1:])
