#author: Konstantinos Dalkafoukis

from pyquil.quil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator, QVMConnection
from scipy import linalg
import numpy as np

program = Program()
program += Program(H(0), H(1))
# program += Program(I(1))

# program += Program(CNOT(0,1),CNOT(1,0), CNOT(0,1))
# program += Program(PHASE(np.pi / 2, 0))

# operator = 1/2 * (sX(0) * sX(1) + sY(0) * sY(1) + sZ(0) * sZ(1))
# program += exponentiate_commuting_pauli_sum(operator)(np.pi / 2)


operator = 1/4 * (sI() - sZ(0) - sZ(0) + sZ(0) * sZ(1))
program += exponentiate_commuting_pauli_sum(operator)(np.pi / 2)

# operator = 1/2 * (sI(0) + sZ(0))
# theta = np.pi / 4
# program += exponentiate_commuting_pauli_sum(operator)(theta)

# operator = sX(0)
# theta = 2 *np.pi /3 
# program += exponential_map(operator)(theta)

# operator = 1/2 * (sI(1) - sZ(1))
# theta = np.pi / 8
# program += exponentiate_commuting_pauli_sum(operator)(theta)

# operator = sX(1)
# theta = np.pi / 4
# program += exponential_map(operator)(theta)

wfn = WavefunctionSimulator().wavefunction(program)
prob = wfn.get_outcome_probs()

print(wfn)
print(prob)


A = 1 / np.sqrt(3) * np.array([
    # [1, 0, 0, 0],
    # [0, 1, 0, 0],
    # [0, 0, 1, 0],
    # [0, 0, 0, 0],

    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
], dtype=complex)

S = np.array([
    # [1, 0, 0, 0],
    # [0, 1, 0, 0],
    # [0, 0, 1, 0],
    # [0, 0, 0, 0],

    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
], dtype=complex)


# print(S @ A @ np.linalg.inv(S))

# 0 ≤ γ0 < 2π and 0 ≤ β0 < π
gammas =  np.linspace(0, 2* np.pi, 10)
betas =  np.linspace(0, np.pi, 10)

print(gammas)