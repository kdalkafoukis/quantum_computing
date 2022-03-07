# https://en.wikipedia.org/wiki/Shor%27s_algorithm

# author: Konstantinos Dalkafoukis
# Shor's algorithm
from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
import numpy as np
from qdft import qdft
from random import randrange

def shors_algorithm():
    prog = Program()
    prog += qdft()

    # step1
    N = 16
    a = randrange(1,N)

    q = N.bit_length()
    print(q)
    # step2
    gcd = np.gcd(a, N)
    # step2
    if (gcd == 1):
        pass
    else:
        print('then this number is a nontrivial factor of {\displaystyle N}N')
    # ////////////
    # Q = round(N /2)
    # for i in range(Q):
    #     prog += Program(H(i))

    # prog += Program(X(1),X(0))
    # for i in range(num_of_iterations):
    #     prog += Program(H(i))
    #     counter = 2
    #     for j in range(i + 1, num_of_iterations):
    #         phase = 2 * np.pi / 2 ** counter
    #         cphase = CPHASE(phase, i ,j)
    #         prog += Program(cphase)
    #         counter = counter + 1
    return prog

def main():
    prog = shors_algorithm()
    wfn = WavefunctionSimulator().wavefunction(prog)
    prob = wfn.get_outcome_probs()
    # print(wfn)
    print(prob)


if __name__ == "__main__":
    main()
