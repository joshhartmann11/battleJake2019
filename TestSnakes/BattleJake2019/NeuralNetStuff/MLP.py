import numpy as np

'''

- Just a clasic implementation of a MLP, math used follows from David Kriesel's "An Introduction into Neural Networks".
- Both classical back propagation and rpropagation (a.k.a ADAM) are implemened.
- The first layer's activation function is unity the rest follow a sigmoid function.
- No bias, because bleh.

If you find any errors then let me know, this implementation was written from without reference other than the textbook
which only outlines the math. Thanks!

Josh Hartmann

'''

class MLP:

    def __init__(self, layers):
    
        #INITIAL_RPROP_RATE = 0.1

        self.synapses = []
        #self.rPropRates = []
        #self.previousChange = []
        self.layers = layers
         
        for i in range(len(layers)-1):
            self.synapses.append(np.matrix((np.random.rand(layers[i], layers[i+1]))-0.5))
            #self.rPropRates.append(np.matrix(np.full(layers[i+1], INITIAL_RPROP_RATE)))
            #self.previousChange.append(np.matrix((np.random.rand(layers[i], layers[i+1])) ))
        
    
    # Sigmoid activation function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
        
    
    # Derivative of the sigmoid function
    def sigmoid_prime(self, x):
	    x = self.sigmoid(x)
	    return np.multiply(x, (1 - x))
        
    
    # Propagate input through the network
    def propigate(self, input, synapses, allLayers = False):
    
        input = np.matrix(input)
        
        if(allLayers):
            layerInputs = [input]
            output = input
            for syn in synapses:
                layerInputs.append(np.dot(output, syn))
                output = self.sigmoid(layerInputs[-1])
            return layerInputs
            
        else:
            output = input
            for syn in synapses:
                output = self.sigmoid(np.dot(output, syn))
            return output


    # Back propagation of error
    def back_propigate(self, actual, layers):

        change = []
        error = self.sigmoid(layers[-1]) - actual
        print("Error:", np.sum(np.abs(error))/len(layers[-1]))
        
        for i in reversed(range(0,len(self.synapses)-1)):
            delta = np.multiply(self.sigmoid_prime(layers[i+2]), error)
            change.insert(0, np.dot(self.sigmoid(layers[i+1]).T, delta))
            error = np.dot(self.synapses[i+1], delta.T).T
            
        delta = np.multiply(self.sigmoid_prime(layers[1]), error)
        change.insert(0, np.dot(self.sigmoid(layers[0]).T, delta))
        
        return(change)


    # Tweaks synapse weights for a given input and expected output
    def learn(self, input, output, layerMul=1.1, lrate=0.1):
    
        if(type(input).__module__ == np.__name__):
            change = self.back_propigate(output, self.propigate(input, self.synapses, allLayers=True))
            
        else:
            change = self.back_propigate(output[0], self.propigate(input[0], self.synapses, allLayers=True))
            for i in range(1, len((input))):
                tempChange = self.back_propigate(output[i], self.propigate(input[i], allLayers=True))
                for i, t in enumerate(tempChange):
                    change[i] = np.add(change[i], t)

        for i, ch in enumerate(change):
            self.synapses[i] = np.add(self.synapses[i], ch * (-lrate - layerMul*i))
        
"""
    # Tweaks synapse weights for a given input and expected output using R propagation
    def learn_rprop(self, input, output, layerMul = 0, changeMul = 0.5, momentumMul=1.1):
        
        if(type(input).__module__ == np.__name__):
            change = self.back_propigate(output, self.propigate(input, allLayers=True))
        else:
            change = self.back_propigate(output[0], self.propigate(input[0], allLayers=True))
            for i in range(1, len((input))):
                tempChange = self.back_propigate(output[i], self.propigate(input[i], allLayers=True))
                for i, t in enumerate(tempChange):
                    change[i] = np.add(change[i], t)

        
        for i, ch in enumerate(change):
            self.synapses[i] = np.add(self.synapses[i], np.matrix(np.array(ch) * np.array(-self.rPropRates[i] - layerMul*i)))
        
            if(change[i][0,0] * self.previousChange[i][0,0] >= 0):
                self.rPropRates[i] *= 1.05
            else:
                self.rPropRates[i] *= 0.5
        """ 
        
        
        
#mlp = MLP([2,3,4,2])
#for i in range(100000):
#    mlp.learn([np.array([0, 1]), np.array([1,0])], [np.array([0, 1]),np.array([1,0])])

