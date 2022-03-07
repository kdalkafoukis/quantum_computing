# author: Konstantinos Dalkafoukis
# max k colorability

from pyquil.quil import Program
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import QVMConnection
from pyquil.api import WavefunctionSimulator
from utils import plotOutput

program = Program()

colours = 3
edges = [(0, 1), (1, 2), (2, 0)]
vertices = 3
# edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
# vertices = 4
qubits = range(vertices * colours)
num_of_edges = len(edges)

init_state_prog = Program(X(0),X(4), X(8))

h_cost = colours * num_of_edges * sI()
for u, v in edges:
    for i in range(colours):
        h_cost -= sZ(u * colours + i) * sZ(v * colours + i)
h_cost = 1 / 4 * h_cost

h_driver = 0
for vertice in range(vertices):
    for k in range(colours):
        h_driver -= sX(vertice * colours + k) * sX(vertice * colours + (k+1) % colours) + sY(vertice * colours + k) * sY(vertice * colours + (k+1) % colours)
# h_driver = 1 / colours * h_driver

def qaoa_ansatz(betas, gammas):   
    return sum([
        exponentiate_commuting_pauli_sum(h_cost)(g) + 
        exponentiate_commuting_pauli_sum(h_driver)(b) 
        for g, b in zip(gammas, betas)], Program())


# 0 ≤ γ0 < 2π and 0 ≤ β0 < π

# beta1 = np.pi / 4
# gamma1 = np.pi / 16
# beta1 = np.pi / 3
# gamma1 = np.pi / 5
# betas = [beta1]
# gammas = [gamma1]
# # betas = [beta1, beta1, beta1]
# # gammas = [gamma1, gamma1, gamma1]

# program += init_state_prog + qaoa_ansatz(betas, gammas)
# wfn = WavefunctionSimulator().wavefunction(program)
# prob = wfn.get_outcome_probs()

# m_v = -1
# m_k = -1
# for key, val in prob.items():
#     if (val > 0.01):
#         print(key, val)
#     if val > m_v:
#         m_v = val
#         m_k = key

# print(m_v, m_k)      
# print(max(prob.values()))


gammas =  np.linspace(0, 2* np.pi, 10)
betas =  np.linspace(0, np.pi, 10)

program = Program()

for gamma in gammas:
    for beta in betas:
        program = init_state_prog + qaoa_ansatz([beta], [gamma])
        wfn = WavefunctionSimulator().wavefunction(program)
        prob = wfn.get_outcome_probs()
        # print(max(prob.values()))
        values = list(prob.values())
        values.sort()

        print('1',max(values))
        values.remove(max(values))
        print('2',max(values))

        # print(values[:5])
