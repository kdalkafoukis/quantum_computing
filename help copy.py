import numpy as np

from pyquil import get_qc, Program
from pyquil.quil import DefGate
from pyquil.gates import *
from pyquil.paulis import *
from pyquil.api import WavefunctionSimulator
import numpy as np
import sys
from scipy import linalg
from utils import testIfArrayIsUnitary

# A = np.mat('[1 3 2]')
# print("hello", A)
prog = Program()

arr = np.array(
    [
        [1,  1],
        [1, -1]
    ]
)

# sigma =  sX(0) * sY(1) * sZ(2)
# theta = prog.declare('theta', 'REAL')
# prog += exponential_map(sigma)(theta)

# definition = DefGate("h", arr)
# prog += Program(definition)
# operator = definition.get_constructor()
# prog += Program(I(0),X(1))
# prog += exponentiate(sZ(0))

# prog += exponentiate(sX(0))


# prog += exponentiate(sY(0))
# ///////////////////
# sigma =  -1* sI(0) * sX(1)

# prog += exponentiate(sigma)

# prog += Program(Z(0),X(1))

# num = 

# def prepare_initial_state(prog):
#     for i in range(0, num):
#         prog += Program(H(prog))
#     return prog

# prog +=prepare_initial_state(prog)

# state = 1 / np.sqrt(3) * np.array([[1, 1, 1, 0]])

from scipy.sparse import csgraph
########################################################
######################################################## 0
# state = np.array([
#     [1, 1, 1, 0],
#     [0, 1, 1, 1],
#     [1, 0, 1, 1],
#     [1, 1, 0, 1],
# ])
# state = 1/ np.sqrt(3) * state
# doubleH = np.kron(arr,arr)
# u = np.multiply(doubleH,state)
# print("u",u)
# testIfArrayIsUnitary(u)

state = np.array([
    [0, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
])

state = 1/ np.sqrt(2) * state
doubleH = np.kron(arr,arr)
u = np.multiply(doubleH,state)
print("u",u)
print(testIfArrayIsUnitary(u))

# state = np.array([
#     [1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1],
#     [1, 1, 0, 1, 1, 1, 1, 1],
#     [1, 1, 1, 0, 1, 1, 1, 1],
#     [1, 1, 1, 1, 0, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 0, 1],
# ])
# state = 1/ np.sqrt(7) * state
# doubleH = np.kron(arr,arr) 
# doubleH = np.kron(arr,doubleH) 

# u = np.multiply(doubleH,state)

# print("u",np.sqrt(7) * u)
# print(testIfArrayIsUnitary(u))

######################################################## 0
########################################################
######################################################## 1
# laplacian = np.array([
#     [3, -1, -1, -1],
#     [-1, 3, -1, -1],
#     [-1, -1, 3, -1],
#     [0, -1, -1, 3],
# ])

# laplacian = 1/ 3 * laplacian

# k = 3
# L =  k * np.identity(4) - laplacian
# # laplacian = csgraph.laplacian(state, normed=False)
# print(laplacian)

# print(np.dot(L.transpose(),L))
# print(L)
######################################################## 1
########################################################
######################################################## 2
# state = np.dot(state,state)
# s = (2 * np.identity(4) - dot)
# s = linalg.inv(state)
# print(s)

# print(linalg.eig(state))
# print(linalg.eig(1/ 3 * state))
# s = linalg.solve(state, np.identity(4))
# print(s)
######################################################## 2
########################################################
######################################################## 3

# state = np.dot(state,state)
# # s = linalg.inv(state)
# # print(s)
# a1, a2 = linalg.eig(state)
# print(3 * a1)
# print(a2)

######################################################## 3
########################################################
# wfn = WavefunctionSimulator().wavefunction(prog)
# prob = wfn.get_outcome_probs()
# print(wfn)
