from NetworkController.MLP import MLP
import numpy as np
import math

# This is a verbose version of the MLP class
#
# This class will print out its status and export the error values to a csv file
#
#
#

class MLP_debug(MLP):

    def __init__(self, layers, outputFile="output.csv", verbose=False):
        self.outputFile = outputFile
        self.verbose = verbose
        self.itterationNumber = 0
        self.windowedAverageSize = 100
        self.cumError = 0
        with open(self.outputFile, "w") as f:
            f.write("Error\n")
        super().__init__(layers, verbose=self.verbose)

    def back_propigate(self, actual, layers):
        returnValue = []
        # Error in the output
        error = actual - self.transfer(layers[-1])
        compiledError = np.sum(np.abs(error)/4)

        if self.verbose:
            print("Actual: " + str(actual))
            print("Guessed: " + str(self.transfer(layers[-1])))
            print("Error: " + str(error))
            print("Compiled Error: " + str(compiledError))
            print("*"*50)

        self.cumError += compiledError
        self.itterationNumber += 1

        if self.itterationNumber >= self.windowedAverageSize:
            with open(self.outputFile, "a") as f:
                avgErr = self.cumError/self.windowedAverageSize
                if avgErr < 0.3:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                f.write(str(avgErr) + "\n")
            self.itterationNumber = 0
            self.cumError = 0

        for i in reversed(range(len(self.synapses))):
            delta = np.multiply(self.transfer_prime(self.transfer(layers[i+1])), error)
            change = np.dot(self.transfer(layers[i]).T, delta)
            returnValue.append(change)
            if i != 0:
                error = delta.dot(self.synapses[i].T)
        return returnValue


    def batch_learn(self, inputs, outputs, lMul=1.1, lRate=0.0005):
        for i in range(len(inputs)):
            layerOutputs = self.propigate(inputs[i], allLayers=True)
            newChange = self.back_propigate(outputs[i], layerOutputs)
            if i is 0:
                change = newChange
            else:
                for w in range(len(change)):
                    change[w] = np.add(change[w], newChange[w])
        if self.verbose:
            print("Last Synapse Change: {}".format(change[-1]))

        for w in range(len(self.synapses)):
            change[-w-1] = np.divide(change[-w-1], len(inputs))
            layerMul = math.pow(lMul, len(self.synapses) - (w+1))
            self.synapses[w] = np.add(self.synapses[w], change[-w-1] * lRate * layerMul)
