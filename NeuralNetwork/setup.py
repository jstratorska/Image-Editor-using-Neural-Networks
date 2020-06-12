from NeuralNetwork.model import NeuralNetwork
from DataPreprocess.read_sketches import read_sketch_data
from DataPreprocess.read_data import find_files, read_data_one
from DataPreprocess.preprocess import to_json_file
from DataPreprocess.draw_sketches import draw
from DataPreprocess.gradients import save_gradients
import numpy as np

def setup():

    objects = ['airplane', 'apple', 'banana', 'bicycle', 'bird']
    folders = ['train', 'test']
    path = "Data\\"

    for i in range (len(folders)):
        for j in range(len(objects)):
            if not find_files(path + "json\\" + folders[i] + "\\" + objects[j] + "*"):
                to_json_file(objects[j])
            if not find_files(path + "sketches\\" + folders[i] + "\\" + objects[j] + "\\*"):
                data = read_data_one(folders[i], objects[j])
                draw(data, folders[i], objects[j])

    print("Finished transforming\nTraining begins")

    input, length = read_sketch_data("train")
    networks = []
    weights = []
    bias = []
    number_of_iterations = 3000
    learning_rate = 0.01
    already_saved = find_files(path + "gradients\\*")
    for i in range (5):  
        networks.append(NeuralNetwork(input, i)) 
        if not already_saved:
            Y = np.zeros(length)
            Y [200*i : 200* (i+1)] = 1
            Y.reshape(1, -1)             
            networks[i].train_model(Y, number_of_iterations, learning_rate) 
            weights.append(np.array(networks[i].weights.reshape(1, -1)))
            bias.append(networks[i].bias) 
    if not already_saved:
        save_gradients(weights, bias)
    return networks