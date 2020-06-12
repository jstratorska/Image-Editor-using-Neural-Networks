from NeuralNetwork.model import NeuralNetwork
from DataPreprocess.read_sketches import read_sketch_data
import numpy as np

# input, Y = read_sketch_data("train")
# # print(input.shape)
# t = NeuralNetwork(input)
# t.train_model(Y, 3000, 0.01)

# test_input, test_Y = read_sketch_data("test")
# # print(type(test_input))
# # print(test_Y.shape)
# # prediction = t.test_value(test_input[:, 0])
# # print(prediction)
# # print("train accuracy: {} %".format(100 - np.mean(np.abs(prediction - test_Y[0])) * 100))
# t.test_value(test_input, test_Y)

input, length = read_sketch_data("train")
test_input, length = read_sketch_data("test")
objects =  ['airplane', 'apple', 'banana', 'bicycle', 'bird']
num = 3000
rate = 0.01
print( "For " + str(num) + " iterations and " + str(rate) + " for the learning rate we get the following accuracy for the train and test data")
for i in range(1,5):
    # print("---------------------------\nThe prediction for the object " + objects[i] + " is ")
    Y = np.zeros(length)
    Y [i *200:200*(i+1)] = 1
    t = NeuralNetwork(input)
    t.train_model(Y, num, rate)
    Y = np.zeros(length)
    Y [200*i:(i+1)*200] = 1
    Y.reshape(1, -1) 
    t.test_value(test_input, Y)


