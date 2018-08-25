import os
import random
import time
import json
import numpy as np
import argparse
from NetworkController.networkController import networkController
from NetworkController.MLP import MLP
from NetworkController.MLP_debug import MLP_debug

DIRECTIONS = {'up':0, 'right':1, 'down':2, 'left':3, 0:'up', 1:'right', 2:'down', 3:'left'}
DATA_FOLDER = "/home/joshhartmann/Documents/Programming/Python/Battle Snake/BattleSnake2019/Training/stage1/input_stage1"

class StageOne():

    def __init__(self, neuralNet, data, networkName=None, verbose=False, save=True):

        self.nc = networkController()

        if isinstance(neuralNet, str):
            neuralNet = self.nc.load(neuralNet)
        elif not isinstance(neuralNet, MLP):
            raise OSError("Input neural network is not a MLP object")

        if not os.path.isdir(data):
            raise OSError("{} is not a folder".format(data))

        self.save = save
        self.verbose = verbose
        self.dataFolder = data
        self.nn = neuralNet
        if self.save:
            self.nnName = self.nc.save(self.nn)

    def _pprint(self, msg):
        if self.verbose:
            print("[{0} StageOne]: {1}".format(time.strftime("%Y-%m-%d %H:%M"), msg))

    def get_input_output(self):
        randomFile = random.choice(os.listdir(self.dataFolder))
        with open(os.path.join(self.dataFolder, randomFile), "r") as inFile:
            fileContents = inFile.read()
        fileContents = json.loads(fileContents)
        input = fileContents["input"]
        output = fileContents["output"]
        #print("Output Act: " + str(output))
        #print("Training File: " + str(randomFile))
        return np.matrix(input), np.matrix(output)

    def _train_sprint(self, batchSize, lMul, lRate):
        inputs = []
        outputs = []
        for i in range(batchSize):
            inp, out = self.get_input_output()
            inputs.append(inp)
            outputs.append(out)
        self.nn.batch_learn(inputs, outputs, lMul=lMul, lRate=lRate)

    def train(self, lRate, n, batchSize, lMul):
        self._pprint("Starting training...")
        self._pprint("\tSamples {}".format(n))
        self._pprint("\tBatch Size {}".format(batchSize))
        self._pprint("\tLearning Rate {}".format(lRate))
        self._pprint("\tLayer Multiplier {}".format(lMul))
        for i in range(int(n / batchSize)):
            print("Sprint {0}/{1}{2}".format(i, int(n/batchSize)," "*12), end="\r")
            self._train_sprint(batchSize, lMul, lRate)
        self._pprint("Finished Training")
        if self.save:
            networkName = self.nc.save(self.nn, name=self.nnName)
            self._pprint("")
            return networkName
        self._pprint("")

def parse_args():
    pass

def test():
    nn = MLP_debug([1600, 1400, 1200, 1000, 4])
    this = StageOne(nn, DATA_FOLDER, verbose=True)
    this.train(0.005, 1000, 1, 1.1)
    this.train(0.001, 1000, 1, 1)
    this.train(0.0005, 100000, 1, 0.9)

if __name__ == "__main__":
    test()
