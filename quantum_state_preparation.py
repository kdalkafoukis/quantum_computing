# https://arxiv.org/pdf/2008.01511.pdf


# author: Konstantinos Dalkafoukis
# A divide-and-conquer algorithm for quantum state preparation
from pyquil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys


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
    print(angles)
    return prog


def getInput(argv):
    # inputArr = [1/3, 1/3, 1/3, 0]
    inputArr = [0.03, 0.07, 0.15, 0.05, 0.1, 0.3, 0.2, 0.1]
    inputArr = list(map(lambda x: np.sqrt(x), inputArr))
    return inputArr


def main(argv):
    arr = getInput(argv)
    prog = quantum_state_preparation(arr)
    wfn = WavefunctionSimulator().wavefunction(prog)
    # prob = wfn.get_outcome_probs()
    print(wfn)


if __name__ == "__main__":
    main(sys.argv[1:])
