import numpy as np
import sys
import os
print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))
from NetworkController.networkController import networkController
from NetworkController.MLP import MLP
from NetworkController import json2Input

DIRECTIONS = {'up':0, 'right':1, 'down':2, 'left':3, 0:'up', 1:'right', 2:'down', 3:'left'}

class Jake2019():

    def __init__(self, fittedNetwork):
        nc = networkController()
        if isinstance(fittedNetwork, str):
            self.mlp = nc.load(fittedNetwork)
        else:
            self.mlp = fittedNetwork

    def output_to_direction(self, output):
        output = output.tolist()[0]
        print(output)
        maxVal = max(output)
        print(maxVal)
        location = output.index(maxVal)
        return DIRECTIONS[location]

    def get_network_input(self, data):
        return json2Input.encode_input_vector(data)

    def propigate_input(self, input):
        return self.mlp.propigate(input, allLayers=False)

    def move(self, data):
        inputVec = self.get_network_input(data)
        outputVec = self.propigate_input(inputVec)
        print("*"*50)
        print(outputVec)
        choice = self.output_to_direction(outputVec)
        print(choice)
        print("*"*50)
        return {"move": choice}
