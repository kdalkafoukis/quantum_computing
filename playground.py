import numpy as np
arr = np.array([[1, -4]])

prod = arr * arr.transpose()
print(prod)
'''
[
a -b* c -d*
b a*  d c*
e -f* g -h*
f e*  h g*
] 

[
    1 -1
    1  1
]

1 -1 1 -1
1  1 1  1
1 -1 1 -1
1  1 1  1
'''