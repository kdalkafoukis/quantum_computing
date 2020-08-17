# gates

# I = np.array(
#     [
#         [1, 0],
#         [0, 1]
#     ]
# )

# X = np.array(
#     [
#         [0, 1],
#         [1, 0]
#     ]
# )

# H = np.array(
#     [
#         [1, 1],
#         [1,-1]
#     ]
# )

# O = np.array(
#     [
#         [0, 0],
#         [0, 0]
#     ]
# )

# states
# return "00000111"
# return "00001110"
# return "00011100"
# return "00111000"
# return "01110000"
# return "11100000"

# return "00001101"
# return "00011001"
# return "00110001"
# return "01100001"
# return "11000001"
# return "00001011"
# return "00010011"
# return "00100011"
# return "01000011"

# 1st
# 00000111
#  default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# a) algorith
# generateHadamardGate
# A[1][4] = -1
# A[3][6] = 1
# A[7][2] = 1
# A[5][0] = -1

# b) algorithm
# no generateHadamardGate
# A[1][4] = -1
# A[2][7] = -1
# A[5][0] = -1
# A[6][3] = -1

# 2nd
# 00001110
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# a) algorith
# generateHadamardGate

# b) algorithm
# no generateHadamardGate

# A[2][4] = -1
# A[3][5] = -1
# A[6][0] = -1
# A[7][1] = -1

# 3rd
# 00011100
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]
# no generateHadamardGate
# A[1][2] = -1 
# A[2][1] = -1
# A[5][6] = -1
# A[6][5] = -1

# 4th
# 00111000
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# a) algorithm
# generateHadamardGate
# A[7][3] = 1
# A[6][2] = 1
# A[2][6] = 1
# A[3][7] = 1

# b) algorithm
# no generateHadamardGate
# A[2][6] = -1
# A[3][7] = -1
# A[6][2] = -1
# A[7][3] = -1

# 5th
# 01110000
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]
# no generateHadamardGate
# A[1][0] = -1 
# A[2][3] = -1
# A[5][4] = -1
# A[6][7] = -1

# 6th
# 11100000
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# a) algorith
# generateHadamardGate

# b) algorithm
# no generateHadamardGate
# A[2][0] = -1
# A[3][1] = -1
# A[6][4] = -1
# A[7][5] = -1


# 7th
# 00001101
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate
# A[1][6] = -1
# A[2][5] = -1
# A[5][2] = -1
# A[6][1] = -1

# 8th
# 00011001
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate
# A[1][6] = -1
# A[3][4] = -1
# A[5][2] = -1
# A[7][0] = -1
# A[4][7] = -1
# A[5][6] = -1
# A[6][5] = -1
# A[7][4] = -1


# 9th
# 00110001
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate
# A[4][7] = -1
# A[5][6] = -1
# A[6][5] = -1
# A[7][4] = -1

# 10th
# 01100001
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate

# A[1][3] = -1
# A[3][1] = -1
# A[4][6] = -1
# A[6][4] = -1

# A[4][3] = -1
# A[5][2] = -1
# A[6][1] = -1
# A[7][0] = -1


# 11th
# 00001011
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate

# A[2][6] = -1
# A[3][7] = -1
# A[6][2] = -1
# A[7][3] = -1

# 12th
# 00010011
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate

# A[3][0] = -1
# A[1][2] = -1
# A[4][7] = -1
# A[6][5] = -1

# 13th
# 00100011
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate
# A[2][0] = -1
# A[3][1] = -1
# A[4][6] = -1
# A[5][7] = -1

# 14th
# 01000011
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]

# no generateHadamardGate
# A[1][0] = -1
# A[3][2] = -1
# A[4][5] = -1
# A[6][7] = -1

# 15th
# 10000011
# default, [0,0,0,0, 0,1,1,0, 1,0,0,1, 1,1,1,-1]
# no generateHadamardGate

# A[2][2] = -1
# A[3][3] = -1
# A[6][6] = -1
# A[7][7] = -1