# https://arxiv.org/pdf/1411.4028.pdf
# https://arxiv.org/pdf/1805.03265.pdf

# optimal angles for 
# https://arxiv.org/pdf/1706.02998.pdf

# author: Konstantinos Dalkafoukis


from pyquil.quil import Program
from pyquil.gates import H
from pyquil.paulis import sI, sX, sZ, exponentiate_commuting_pauli_sum
# from pyquil.api import QVMConnection
from pyquil.api import WavefunctionSimulator
import numpy as np

graph = [(0, 1), (1, 2), (2, 3), (3, 0)]
nodes = range(4)

init_state_prog = sum([H(i) for i in nodes], Program())
h_cost = -0.5 * sum(sI(nodes[0]) - sZ(i) * sZ(j) for i, j in graph)
h_driver = -1. * sum(sX(i) for i in nodes)

def qaoa_ansatz(betas, gammas):   
    return sum([
        exponentiate_commuting_pauli_sum(h_cost)(g) + 
        exponentiate_commuting_pauli_sum(h_driver)(b) 
        for g, b in zip(gammas, betas)], Program())


beta1 = np.pi / 8
gamma1 = np.pi / 4

betas = [beta1]
gammas = [gamma1]

betas = [beta1, beta1, beta1]
gammas = [gamma1, gamma1, gamma1]
program = init_state_prog + qaoa_ansatz(betas, gammas)

# betas = [0.1978 * np.pi, 0.1044 * np.pi]
# gammas = [0.3956 * np.pi, 0.3022 * np.pi]
# program = init_state_prog + qaoa_ansatz(betas, gammas)

wfn = WavefunctionSimulator().wavefunction(program)
prob = wfn.get_outcome_probs()

print(prob)

# qvm = QVMConnection()
# qvm.run_and_measure(program, qubits=nodes, trials=10)

# p    r    F∗/n    γ1     β1     γ2     β2     γ3     β3     γ4     β4     γ5     β5
# 1   3/4   -1/2  0.1250
# 2   5/6   -2/3  0.2052 0.1026
# 3   7/8   -3/4  0.2268 0.1888 0.0918
# 4   9/10  -4/5  0.2357 0.2161 0.1791 0.0850
# 5  11/12  -5/6  0.2403 0.2282 0.2094 0.1724 0.0802
# 6  13/14  -6/7  0.3035 0.1639 0.2506 0.2835 0.0794 0.2409
# 7  15/16  -7/8  0.2303 0.1623 0.3468 0.2690 0.1042 0.2397 0.1599
# 8  17/18  -8/9  0.2445 0.1638 0.2839 0.3484 0.1539 0.1530 0.2581 0.1291
# 9  19/20  -9/10 0.1929 0.1648 0.3307 0.3016 0.1551 0.2538 0.2174 0.1089 0.3117
# 10 21/22 -10/11 0.2208 0.1374 0.3098 0.2974 0.2702 0.1205 0.3148 0.1904 0.1423 0.2572