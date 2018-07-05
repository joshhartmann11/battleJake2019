import os
import random
import time
import numpy as np
import argparse
from NetworkController.networkController import networkController
from NetworkController.MLP import MLP

DIRECTIONS = {'up':0, 'right':1, 'down':2, 'left':3, 0:'up', 1:'right', 2:'down', 3:'left'}

class StageOne():

    def __init__(self, MLP):
        self.host_id = ""
        self.height = 12
        self.width = 12
        self.nn = MLP([self.height*self.width*5, 1000, 500, 100, 4])

    def board_to_input(self):
        pass


    def train(self, rate, data, n, batchSize):
        for i in range(n):
            k = 0
            while k < batchSize:
                pass
                # Do the thing
            self.nn.backpropigate()



def parse_args():
    pass

if __name__ == "__main__":
    args = parse_args()
    nc = networkController()

    if args.network:
        StageOne(nc.load(args.network))
    else:
        StageOne(MLP(args.layers))

    StageOne.train(args.learningRate, args.dataFolder, args.samples, args.batch)

    print(nc.save(StageOne.mlp))

