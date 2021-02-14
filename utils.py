import matplotlib.pyplot as plt

def plotOutput(prob):
    keys = []
    values = []
    threshold = 0.02
    for key, value in prob.items():
        if(value > threshold):
            values.append(value)
            keys.append(key)

    plt.bar(keys, values)
    plt.ylabel('probability')
    plt.show()
