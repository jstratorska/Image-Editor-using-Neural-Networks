import numpy as np
import math
from DataPreprocess.gradients import read_gradients

class NeuralNetwork:

    def __init__(self, input, i):
        self.input = input
        # The matrix input with m * n size
        self.m , self.n = input.shape
        self.initialize(self.m, i)

    def initialize(self, dimension, i):
        data = read_gradients()
        if not data.empty:
            self.weights = np.array(data['weights'][i]).reshape(-1, 1)
            self.bias = data['bias'][i]
        else:
            self.weights = np.zeros(shape = (dimension, 1))
            self.bias = 0

    # Sigmoid's function
    def activation(self, x):
        return 1 / (1 + np.exp(-x))

    def forward_propagation(self):
        activation_matrix = self.activation(np.dot(self.weights.T, self.input) + self.bias)
        return activation_matrix

    def back_propagation(self, expected_output, activation_matrix):
        weights_der = (1 / self.n) * np.dot(self.input, (activation_matrix - expected_output).T)        
        bias_der = (1 / self.n) * np.sum(activation_matrix - expected_output)
        return weights_der, bias_der

    def predict(self):
        prediction = np.zeros((1, self.n))
        activation_matrix = self.activation(np.dot(self.weights.T, self.input) + self.bias)
        for i in range(activation_matrix.shape[1]):
            if activation_matrix [0, i] > 0.5:
                prediction[0, i] = 1
            else:
                prediction[0, i] = 0
        return prediction

    def optimize_cost (self, expected_output, rate, iterations):
        for i in range(iterations):
            activation_matrix = self.forward_propagation()
            weights_der, bias_der = self.back_propagation(expected_output, activation_matrix)
            self.weights -= rate * weights_der 
            self.bias -= rate * bias_der
        return weights_der, bias_der

    def train_model(self, expected_output, iterations, rate):
        self.optimize_cost (expected_output, rate, iterations)
        prediction = self.predict()
        print("The accuracy for the train data is " + str(self.calculate_accuracy(prediction, expected_output)) + "%" )

    def calculate_accuracy(self, prediction, expected_output):
        return 100 - np.mean(np.abs(prediction - expected_output) * 100)

    def predict_value(self, input, i):
        test_Network = NeuralNetwork(input, i)
        test_Network.weights = self.weights.reshape(input.shape[0], 1)
        test_Network.bias = self.bias
        return test_Network.predict()

    def test_value(self, input, expected_output):
        prediction = self.predict_value(input, 0)
        print("The accuracy for the test data is " + str(self.calculate_accuracy(prediction, expected_output))+ "%")