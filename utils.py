import matplotlib.pyplot as plt


def plotOutput(prob, accuracy=0):
    keys = []
    values = []
    threshold = accuracy
    for key, value in prob.items():
        if(value > threshold):
            values.append(value)
            keys.append(key)

    plt.bar(keys, values)
    plt.ylabel('probability')
    plt.show()
