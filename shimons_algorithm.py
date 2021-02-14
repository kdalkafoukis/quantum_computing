# https://en.wikipedia.org/wiki/Simon%27s_problem

# author: Konstantinos Dalkafoukis
# shor's algorithm
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


def main():
    prog = qdft(2)
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    print(wfn)
    print(prob)


if __name__ == "__main__":
    main()
