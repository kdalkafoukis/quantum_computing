# https://arxiv.org/pdf/2008.01511.pdf


# author: Konstantinos Dalkafoukis
# A divide-and-conquer algorithm for quantum state preparation
from pyquil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys


def index(qubit, qubits, i):
    prog = Program()
    key_in_binary = '{:0{:d}b}'.format(2 ** qubit - 1 - i, qubit)
    for controlled_bit in range(qubit):
        if key_in_binary[controlled_bit] == '1':
            prog += Program(X(qubits - 1 - controlled_bit))
    return prog


def construct_circuit(angles, qubits):
    prog = Program()
    counter = 0
    for qubit in range(qubits):
        for i in range(2 ** qubit):
            gate = RY(angles[counter], qubits - 1 - qubit)
            prog += index(qubit, qubits, i)
            for controlled_bit in range(qubit):
                gate = gate.controlled(qubits - 1 - controlled_bit)
            prog += Program(gate)
            prog += index(qubit, qubits, i)
            counter += 1
    return prog


def calclulate_angles(arr):
    new_arr = []
    length_new_arr = int(len(arr) / 2)
    angles = []
    if len(arr) > 1:
        for i in range(length_new_arr):
            new_arr.append(np.sqrt(np.square(arr[2 * i]) +
                                   np.square(arr[2 * i + 1])))
        inner_angles = calclulate_angles(new_arr)
        for i in range(length_new_arr):
            if new_arr[i] != 0:
                temp = 2 * np.arcsin(arr[2 * i + 1] / new_arr[i])
                if arr[2 * i] > 0:
                    angles.append(temp)
                else:
                    angles.append(2 * np.pi - temp)
            else:
                angles.append(0)
        angles = inner_angles + angles
    return angles


def quantum_state_preparation(arr):
    prog = Program()
    angles = calclulate_angles(arr)
    qubits = int(np.log2(len(arr)))
    prog += construct_circuit(angles, qubits)
    return prog


def getInput(argv):
    inputArr = [0.03, 0.07, 0.15, 0.05, 0.1, 0.3, 0.2, 0.1]
    if len(argv) == 1 and argv[0] in argv:
        arr = argv[0].split(',')
        arr = list(map(lambda x: x.split('/'), arr))
        arr = [int(x[0]) / int(x[1]) if len(x) == 2 else 0 for x in arr]
        try:
            inputArr = arr
        except ValueError:
            pass
    inputArr = list(map(lambda x: np.sqrt(x), inputArr))
    return inputArr


def main(argv):
    arr = getInput(argv)
    prog = quantum_state_preparation(arr)
    wfn = WavefunctionSimulator().wavefunction(prog)
    # prob = wfn.get_outcome_probs()
    print('input arr: ', arr)
    print()
    print('wave function: ', wfn)


if __name__ == "__main__":
    main(sys.argv[1:])
