import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))



class NeuralNetwork:
    def __init__(self, x):
        self.input      = x
        self.weights1   = 2*np.random.rand(self.input.shape[1],10) - 1
        self.weights2   = 2*np.random.rand(10,1) - 1            
        self.output     = int()

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))
        self.output = int(float(self.output>0.5))
