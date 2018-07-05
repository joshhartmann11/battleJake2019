import os
import random
import time
import numpy as np

DIRECTIONS = {'up':0, 'right':1, 'down':2, 'left':3, 0:'up', 1:'right', 2:'down', 3:'left'}

class NetworkFitting():

    def __init__(self, data):
        self.host_id = ""
        self.height = 12
        self.width = 12
        self.nn = MLP([self.height*self.width*5, 1000, 500, 100, 4])

    def board_to_input(self):
        pass
        
    
    def train(self, data, choice):
        input = np.array(board_to_input(data))
        output = [0, 0, 0, 0]
        output[DIRECTIONS[choice]] = 1
        output = np.array(output)
        
        