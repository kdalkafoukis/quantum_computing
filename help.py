import numpy as np

from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import sys
from scipy import linalg
from utils import testIfArrayIsUnitary
from scipy.sparse import csgraph


def main():
    A = np.array([
        # [1, 0,-1, 1],
        # [0, 1,-1,-1],
        # [1,-1, 0,-1],
        # [1, 1, 1, 0],

        [ 1,  0, 1,  1],
        [ 0, -1,  1, -1],
        [ 1,  1, -0, -1],
        [ 1, -1, -1,  0]

        # [1, 0,-1, 1],
        # [0, 1,-1,-1],
        # [1,-1, 1, 0],
        # [1, 1, 0, 1],

    ])

    diag = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],

        # [0, 0, 0, 1],
        # [0, 0, 1, 0],
        # [0, -1, 0, 0],
        # [1, 0, 0, 0],
    ])
    res = A 
    # res = diag @ A
    # res = A @ diag
    # print(res)
    res = 1 /np.sqrt(3) * res

    # print(res)

    # print(res @ res.transpose())
    # print(testIfArrayIsUnitary(res))



if __name__ == "__main__":
    main()

######################################################## 
prog = Program()

operator = sZ(0)
# prog += exponentiate(operator)

# prog += I(0)
prog += RX(np.pi/4,0)
# prog += RY(np.pi/2,1)
# prog += RY(3*np.pi/2,1)
prog += RY(np.pi/8,1)
# prog += RY(3*np.pi/4,0)
prog += RZ(np.pi/2,0)
# prog += I(0)
# prog += I(0)

wfn = WavefunctionSimulator().wavefunction(prog)
prob = wfn.get_outcome_probs()
print(wfn)