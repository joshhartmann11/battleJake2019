import os
import time
import json
import numpy as np
from NetworkController.nameGenerator import *
from NetworkController.MLP import MLP

class networkController():

    def __init__(self, saveFolder="networks"):
        self.saveFolder = os.path.dirname(os.path.realpath(__file__)) + "/" + saveFolder
        self.extension = ".txt"
        if not os.path.exists(self.saveFolder):
            os.mkdir(self.saveFolder)


    def list(self):
        return(os.listdir(self.saveFolder.replace(self.extension, "")))


    def save(self, mlp, name=None):
        
        if not name:
            namesChoosenAlready = self.list()
            while name in namesChoosenAlready or name == None:
                name = generate_name().replace(" ", "")

        outputPath = self.saveFolder + "/" + name + self.extension
        outputData = {  "name": name,
                        "layers": mlp.layers,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                        "synapses": [k.tolist() for k in mlp.synapses] }

        with open(outputPath, "w") as f:
            f.write(json.dumps(outputData))

        print("Saving " + name + " at " + outputData['timestamp'])

        return name


    def load(self, name):
        inputFile = self.saveFolder + "/" + name + self.extension
        if os.path.isfile(inputFile):
            with open(inputFile, "r") as f:
                obj = json.loads(f.read())
            mlp = MLP(obj['layers'])
            mlp.synapses = [np.matrix(k) for k in obj['synapses']]
            print("Loaded " + name + " from ", obj['timestamp'])
            return mlp
        else:
            raise FileNotFoundError("File: " + inputFile + " Does not exist")

    def delete(self, name):
        os.remove(os.path.join(self.saveFolder, name + self.extension))

    def input_to_JSON(self, input):
        pass

    def JSON_to_input(self, JSON):
        pass


