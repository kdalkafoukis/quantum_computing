#edit: Konstantinos Dalkafoukis

##original code
### Rigetti
#Unsupervised Machine Learning on a Hybrid Quantum Computer
#Johannes Otterbach

#Bay Area Quantum Computing Meetup - YCombinator
#February 1 , 2018
#
from pyquil.quil import Program
from pyquil.gates import H
from pyquil.paulis import sI, sX, sZ, exponentiate_commuting_pauli_sum
# from pyquil.api import QVMConnection
from pyquil.api import WavefunctionSimulator

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

program = init_state_prog + qaoa_ansatz([0., 0.5], [0.75, 1.])
# qvm = QVMConnection()
# qvm.run_and_measure(program, qubits=nodes, trials=10)

wfn = WavefunctionSimulator().wavefunction(program)
prob = wfn.get_outcome_probs()

print(prob)

# import numpy as np
# program = Program()
# gammas =  np.linspace(0, 2* np.pi, 10)
# betas =  np.linspace(0, np.pi, 10)

# for gamma in gammas:
#     for beta in betas:
#         program = init_state_prog + qaoa_ansatz([beta], [gamma])
#         wfn = WavefunctionSimulator().wavefunction(program)
#         prob = wfn.get_outcome_probs()
#         # print(max(prob.values()))
#         values = list(prob.values())
#         values.sort()

#         print('1',max(values))
#         values.remove(max(values))
#         print('2',max(values))