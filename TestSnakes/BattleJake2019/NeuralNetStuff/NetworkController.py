import os
import time
import json
import numpy as np
from NameGenerator import *
from MLP import MLP

class NetworkController():

    def __init__(self, saveFolder="networks"):
        self.saveFolder = os.path.dirname(os.path.realpath(__file__)) + "/" + saveFolder
        self.extension = ".txt"
        if not os.path.exists(self.saveFolder):
            os.mkdir(self.saveFolder)
    
    
    def list(self):
        return(os.listdir(self.saveFolder.replace(self.extension, "")))
    
    
    def save(self, mlp):
        namesChoosenAlready = self.list()
        name = "mitch"
        while name in namesChoosenAlready or name == "mitch":
            name = generate_name().replace(" ", "")
        outputPath = self.saveFolder + "/" + name + self.extension
        outputData = {  "name": name,
                        "layers": mlp.layers,
                        "timestamp": str(time.localtime()),
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
        pass


