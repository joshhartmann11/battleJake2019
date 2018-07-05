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

    """

    8888888 888b    888 8888888 88888888888 
    888   8888b   888   888       888     
    888   88888b  888   888       888     
    888   888Y88b 888   888       888     
    888   888 Y88b888   888       888     
    888   888  Y88888   888       888     
    888   888   Y8888   888       888     
    8888888 888    Y888 8888888     888                                        
                            
    """

    def __init__(self, layers, verbose=False):
        self.verbose=verbose
        self.synapses = []
        self.layers = layers
         
        for i in range(len(layers)-1):
            self.synapses.append(np.matrix((np.random.rand(layers[i], layers[i+1]))-0.5))


    def pprint(self, thing, header=None):
        if self.verbose:
            print("_" * 100)
            print("")
            if header:
                print(header)
                print("")
            print(thing)
            print("_" * 100)

    """

    88888888888 8888888b.         d8888 888b    888  .d8888b.  8888888888 8888888888 8888888b.  
        888     888   Y88b       d88888 8888b   888 d88P  Y88b 888        888        888   Y88b 
        888     888    888      d88P888 88888b  888 Y88b.      888        888        888    888 
        888     888   d88P     d88P 888 888Y88b 888  "Y888b.   8888888    8888888    888   d88P 
        888     8888888P"     d88P  888 888 Y88b888     "Y88b. 888        888        8888888P"  
        888     888 T88b     d88P   888 888  Y88888       "888 888        888        888 T88b   
        888     888  T88b   d8888888888 888   Y8888 Y88b  d88P 888        888        888  T88b  
        888     888   T88b d88P     888 888    Y888  "Y8888P"  888        8888888888 888   T88b 
                                                                                                
    """

    # Sigmoid activation function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    # Relu function
    def relu(self, x):
        # if > 0: x else 0
        pass
    
    def transfer(self, x):
        return self.sigmoid(x)

    """

    88888888888      8888888b.  8888888b.  8888888 888b     d888 8888888888 
        888          888   Y88b 888   Y88b   888   8888b   d8888 888        
        888          888    888 888    888   888   88888b.d88888 888        
        888          888   d88P 888   d88P   888   888Y88888P888 8888888    
        888          8888888P"  8888888P"    888   888 Y888P 888 888        
        888   888888 888        888 T88b     888   888  Y8P  888 888        
        888          888        888  T88b    888   888   "   888 888        
        888          888        888   T88b 8888888 888       888 8888888888 
                                                                                                                                            
    """
    
    # Derivative of the sigmoid function
    def sigmoid_prime(self, x):
        x = self.sigmoid(x)
        return np.multiply(x, (1 - x))

    def relu_prime(self, x):
        # if > 0: 1 else 0
        pass

    def transfer_prime(self, x):
        return self.sigmoid_prime(x)
        
    """

    8888888b.  8888888b.   .d88888b.  8888888b. 8888888 .d8888b.         d8888 88888888888 8888888888 
    888   Y88b 888   Y88b d88P" "Y88b 888   Y88b  888  d88P  Y88b       d88888     888     888        
    888    888 888    888 888     888 888    888  888  888    888      d88P888     888     888        
    888   d88P 888   d88P 888     888 888   d88P  888  888            d88P 888     888     8888888    
    8888888P"  8888888P"  888     888 8888888P"   888  888  88888    d88P  888     888     888        
    888        888 T88b   888     888 888         888  888    888   d88P   888     888     888        
    888        888  T88b  Y88b. .d88P 888         888  Y88b  d88P  d8888888888     888     888        
    888        888   T88b  "Y88888P"  888       8888888 "Y8888P88 d88P     888     888     8888888888                                                                                             
                                                                                                    
    """

    # Propagate input through the network
    def propigate(self, input, synapses, allLayers=False):
    
        input = np.matrix(input)
        
        if(allLayers):
            layerInputs = [input]
            output = input
            for syn in synapses:
                layerInputs.append(np.dot(output, syn))
                output = self.transfer(layerInputs[-1])
            self.pprint(self.sigmoid(layerInputs[-1]), "OUTPUT")
            return layerInputs
            
        else:
            output = input
            for syn in synapses:
                output = self.transfer(np.dot(output, syn))
            return output

    """

    888888b.         d8888  .d8888b.  888    d8P       8888888b.  8888888b.   .d88888b.  8888888b.  
    888  "88b       d88888 d88P  Y88b 888   d8P        888   Y88b 888   Y88b d88P" "Y88b 888   Y88b 
    888  .88P      d88P888 888    888 888  d8P         888    888 888    888 888     888 888    888 
    8888888K.     d88P 888 888        888d88K          888   d88P 888   d88P 888     888 888   d88P 
    888  "Y88b   d88P  888 888        8888888b         8888888P"  8888888P"  888     888 8888888P"  
    888    888  d88P   888 888    888 888  Y88b        888        888 T88b   888     888 888        
    888   d88P d8888888888 Y88b  d88P 888   Y88b       888        888  T88b  Y88b. .d88P 888        
    8888888P" d88P     888  "Y8888P"  888    Y88b      888        888   T88b  "Y88888P"  888                                                                                                     
                                                                                                    
    """

    # Back propagation of error
    # THIS ALGORITHM HAS NOTHING TO DO WITH THE SYNAPSES self.synapses SHOULD NOT BE MENTIONED HERE EXCEPT FOR FIGURING OUT THE NEXT ERROR
    def back_propigate(self, actual, layers):

        returnValue = []
        # Error in the output
        error = actual - self.transfer(layers[-1])

        for i in reversed(range(len(self.synapses))):
            delta = np.multiply(self.transfer_prime(self.transfer(layers[i+1])), error)
            change = np.dot(self.transfer(layers[i]).T, delta)
            returnValue.append(change)
            if i != 0:
                error = delta.dot(self.synapses[i].T)
        return returnValue
        """
        # The error in the input to the layer across the neuron
        # dy/dx = sig`(x) | dy = sig`(x)dx
        delta = np.multiply(self.transfer_prime(output), error)
        # The amount each synapse needs to change depends on the amount it contributes 
        change = np.dot(self.transfer(layers[1]).T, delta)
        # Append the change
        returnValue.append(change)
        
        #pprint(error, "ERROR 1")
        #pprint(delta, "DELTA 1")
        #pprint(change, "CHANGE 1")

        error = delta.dot(self.synapses[1].T)
        delta = np.multiply(self.transfer_prime(self.transfer(layers[1])), error)
        change = np.dot(self.transfer(layers[0]).T, delta)
        returnValue.append(change)
        
        #pprint(error, "ERROR 2")
        #pprint(delta, "DELTA 2")
        #pprint(change, "CHANGE 2")
        
        return(returnValue)
        """
    """

    888      8888888888        d8888 8888888b.  888b    888 
    888      888              d88888 888   Y88b 8888b   888 
    888      888             d88P888 888    888 88888b  888 
    888      8888888        d88P 888 888   d88P 888Y88b 888 
    888      888           d88P  888 8888888P"  888 Y88b888 
    888      888          d88P   888 888 T88b   888  Y88888 
    888      888         d8888888888 888  T88b  888   Y8888 
    88888888 8888888888 d88P     888 888   T88b 888    Y888 
                                                            
    """

    # Tweaks synapse weights for a given input and expected output
    # Input:
    #   input: np.matrix
    #   output: np.matrix
    #   lMul: Layer multiplier
    #   lRate: Learning rate
    def learn(self, input, output, lMul=1.1, lRate=0.0005):
        input = np.matrix(input)
        output = np.matrix(output)
        layerOutputs = self.propigate(input, self.synapses, allLayers=True)
        change = self.back_propigate(output, layerOutputs)
        for w in range(len(self.synapses)):
            self.synapses[w] = np.add(self.synapses[w], change[-w-1] * lRate)
        
        
if __name__ == "__main__":
    test = MLP([2, 1200, 20000, 4], verbose=True)
    for i in range(100000):
        test.learn(np.array([1, 1]), np.array([0.2, 0.8, 0.3, 1]))
    #import subprocess
    #subprocess.call(["python3", "testMLP.py"])


#mlp = MLP([2,3,4,2])
#for i in range(100000):
#    mlp.learn([np.array([0, 1]), np.array([1,0])], [np.array([0, 1]),np.array([1,0])])

