import numpy as np
import pandas as pd

def save_gradients(weights, bias):
    file = open("Data\\gradients\\gradients.json","w+")
    file.write("[\n")
    for i in range(len(bias)):
        file.write('{"weights": ')
        with np.printoptions(threshold=np.inf):
            file.write(np.array2string(weights[i], separator = ","))
        file.write(',\n"bias":' + str(bias[i]) + '}')
        if i != len(bias) - 1:
            file.write(",\n")
    file.write('\n]')
    file.close()

def read_gradients():
    try:
        data = pd.read_json("Data\\gradients\\gradients.json")
        return data
    except:
        return pd.DataFrame()