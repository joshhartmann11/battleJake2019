from NeuralNetStuff.networkController import networkController
from n

class battleJake2019():

    def __init__(self, fittedNetwork):
        nc = networkController()
        mlp = nc.load()

    def move(self, data):
        self.mlp.propigate()
        