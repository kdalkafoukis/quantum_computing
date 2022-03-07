import numpy as np

from pyquil import Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import sys
from scipy import linalg
# from utils import testIfArrayIsUnitary

prog = Program()

prog += Program(H(0),H(1))
theta = np.pi/2
operator = 1/2 * (sI() - sZ(0)* sZ(1))
prog += exponentiate_commuting_pauli_sum(operator)(theta)

# # prog += I(0)
# prog += RX(np.pi/4,0)
# # prog += RY(np.pi/2,1)
# # prog += RY(3*np.pi/2,1)
# prog += RY(np.pi/8,1)
# # prog += RY(3*np.pi/4,0)
# prog += RZ(np.pi/2,0)
# # prog += I(0)
# # prog += I(0)

wfn = WavefunctionSimulator().wavefunction(prog)
prob = wfn.get_outcome_probs()
print(wfn)

# 0 ≤ γ0 < 2π and 0 ≤ β0 < π
gammas =  np.linspace(0, 2* np.pi, 10)
betas =  np.linspace(0, np.pi, 10)

print(gammas)