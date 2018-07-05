import unittest
import numpy as np
from MLP import MLP

class testMLP(unittest.TestCase):

"""

       d8888  .d8888b.   .d8888b.  8888888888 8888888b. 88888888888 8888888 .d88888b.  888b    888  .d8888b.  
      d88888 d88P  Y88b d88P  Y88b 888        888   Y88b    888       888  d88P" "Y88b 8888b   888 d88P  Y88b 
     d88P888 Y88b.      Y88b.      888        888    888    888       888  888     888 88888b  888 Y88b.      
    d88P 888  "Y888b.    "Y888b.   8888888    888   d88P    888       888  888     888 888Y88b 888  "Y888b.   
   d88P  888     "Y88b.     "Y88b. 888        8888888P"     888       888  888     888 888 Y88b888     "Y88b. 
  d88P   888       "888       "888 888        888 T88b      888       888  888     888 888  Y88888       "888 
 d8888888888 Y88b  d88P Y88b  d88P 888        888  T88b     888       888  Y88b. .d88P 888   Y8888 Y88b  d88P 
d88P     888  "Y8888P"   "Y8888P"  8888888888 888   T88b    888     8888888 "Y88888P"  888    Y888  "Y8888P"  
                                                                                           
"""

    # Assert that two matrices are almost equal
    def assertMatrixAlmostEqual(self, first, second, places=7):
        self.assertEqual(first.shape, second.shape)

        for i in range(first.shape[0]):
            for j in range(first.shape[1]):
                self.assertAlmostEqual(first[i,j], second[i,j], places=places)

    # Assert that two vectors are almost equal
    def assertVectorAlmostEqual(self, first, second, places=7):
        self.assertEqual(first.shape, second.shape)

        for i in range(first.shape[0]):
            self.assertAlmostEqual(first[i], second[i], places=places)

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

    # Test the initialization method
    def _test_init(self, layers):
        test = MLP(layers)
        self.assertEqual(len(layers) - 1, len(test.synapses))
        for i in range(len(layers) - 1):
            self.assertTrue((layers[i], layers[i+1]), (len(test.synapses[i]), len(test.synapses[i][0])))
        del(test)

    def test_init(self):
        self._test_init([1])
        self._test_init([2,3,2])
        self._test_init([2234,332,2123,27])
    
"""

 .d8888b. 8888888 .d8888b.  888b     d888  .d88888b. 8888888 8888888b.  
d88P  Y88b  888  d88P  Y88b 8888b   d8888 d88P" "Y88b  888   888  "Y88b 
Y88b.       888  888    888 88888b.d88888 888     888  888   888    888 
 "Y888b.    888  888        888Y88888P888 888     888  888   888    888 
    "Y88b.  888  888  88888 888 Y888P 888 888     888  888   888    888 
      "888  888  888    888 888  Y8P  888 888     888  888   888    888 
Y88b  d88P  888  Y88b  d88P 888   "   888 Y88b. .d88P  888   888  .d88P 
 "Y8888P" 8888888 "Y8888P88 888       888  "Y88888P" 8888888 8888888P"  
                                                                        
"""

    # Test the sigmoid function
    def _test_sigmoid_scalar(self, x, y):
        test = MLP([1])
        self.assertAlmostEqual(test.sigmoid(x), y, places=5)
        del(test)
    
    def _test_sigmoid_vector(self, vec_x, vec_y):
        test = MLP([1])
        self.assertVectorAlmostEqual(test.sigmoid(np.array(vec_x)), np.array(vec_y), places=5)
        del(test)
    
    def _test_sigmoid_matrix(self, mat_x, mat_y):
        test = MLP([1])
        self.assertMatrixAlmostEqual(test.sigmoid(mat_x), mat_y, places=5)
        del(test)

    def test_sigmoid(self):
        self._test_sigmoid_scalar(2, 0.8807970)
        self._test_sigmoid_scalar(1, 0.7310585)
        self._test_sigmoid_scalar(0, 0.5)
        self._test_sigmoid_scalar(-1, 0.2689414)
        self._test_sigmoid_scalar(-2, 0.1192029)

        self._test_sigmoid_vector(np.array([2, 1, 0, -1, -2]), 
                                  np.array([0.8807970, 0.7310585, 0.5, 0.2689414, 0.1192029]))

        self._test_sigmoid_matrix(np.matrix([[2, 1],
                                             [1, 0],
                                             [0, -1]]),
                                  np.matrix([[0.8807970, 0.7310585],
                                             [0.7310585, 0.5],
                                             [0.5, 0.2689414]]))

        self._test_sigmoid_matrix(np.matrix([[2, 1, 0],
                                             [1, 0, -1],
                                             [0, -1, -2]]),
                                  np.matrix([[0.8807970, 0.7310585, 0.5],
                                             [0.7310585, 0.5, 0.2689414],
                                             [0.5, 0.2689414, 0.1192029]]))

"""

 .d8888b. 8888888 .d8888b.  888b     d888  .d88888b. 8888888 8888888b.       8888888b.  8888888b.  8888888 888b     d888 8888888888 
d88P  Y88b  888  d88P  Y88b 8888b   d8888 d88P" "Y88b  888   888  "Y88b      888   Y88b 888   Y88b   888   8888b   d8888 888        
Y88b.       888  888    888 88888b.d88888 888     888  888   888    888      888    888 888    888   888   88888b.d88888 888        
 "Y888b.    888  888        888Y88888P888 888     888  888   888    888      888   d88P 888   d88P   888   888Y88888P888 8888888    
    "Y88b.  888  888  88888 888 Y888P 888 888     888  888   888    888      8888888P"  8888888P"    888   888 Y888P 888 888        
      "888  888  888    888 888  Y8P  888 888     888  888   888    888      888        888 T88b     888   888  Y8P  888 888        
Y88b  d88P  888  Y88b  d88P 888   "   888 Y88b. .d88P  888   888  .d88P      888        888  T88b    888   888   "   888 888        
 "Y8888P" 8888888 "Y8888P88 888       888  "Y88888P" 8888888 8888888P"       888        888   T88b 8888888 888       888 8888888888 
                                                                                                                                                                                                                                        
"""

    # Test the sigmoid prime function
    def _test_sigmoid_prime_scalar(self, x, y):
        test = MLP([1])
        self.assertAlmostEqual(test.sigmoid_prime(x), y, places=5)
        del(test)
    
    def _test_sigmoid_prime_vector(self, vec_x, vec_y):
        test = MLP([1])
        self.assertVectorAlmostEqual(test.sigmoid_prime(np.array(vec_x)), np.array(vec_y), places=5)
        del(test)
    
    def _test_sigmoid_prime_matrix(self, mat_x, mat_y):
        test = MLP([1])
        self.assertMatrixAlmostEqual(test.sigmoid_prime(mat_x), mat_y, places=5)
        del(test)

    def test_sigmoid_prime(self):
        self._test_sigmoid_prime_scalar(2, 0.1049935)
        self._test_sigmoid_prime_scalar(1, 0.1966116)
        self._test_sigmoid_prime_scalar(0, 0.25)
        self._test_sigmoid_prime_scalar(-1, 0.1966116)
        self._test_sigmoid_prime_scalar(-2, 0.1049935)

        self._test_sigmoid_prime_vector(np.array([2, 1, 0, -1, -2]), 
                                        np.array([0.1049935, 0.1966116, 0.25, 0.1966116, 0.1049935]))

        self._test_sigmoid_prime_matrix(np.matrix([[2, 1],
                                                   [1, 0],
                                                   [0, -1]]),
                                        np.matrix([[0.1049935, 0.1966116],
                                                   [0.1966116, 0.25],
                                                   [0.25, 0.1966116]]))

        self._test_sigmoid_prime_matrix(np.matrix([[2, 1, 0],
                                                   [1, 0, -1],
                                                   [0, -1, -2]]),
                                        np.matrix([[0.1049935, 0.1966116, 0.25],
                                                   [0.1966116, 0.25, 0.1966116],
                                                   [0.25, 0.1966116, 0.1049935]]))

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
ss
    # Test the propigation
    def _test_propigate_unit_synapses(self, layers):
        test = MLP(layers)
        for i in range(len(layers)-1):
            test.synapses[i] = np.matrix((np.ones((layers[i], layers[i+1]))))

        inputNumber = 5
        input = [inputNumber]*layers[0]
        output = inputNumber
        for i in range(len(layers) - 1):
            output = test.sigmoid(output)
        output = [output]*layers[-1]
        actual = test.propigate(input, test.synapses)
        self.assertEqual(set(output), set(actual))


    def test_propigate(self):
        self._test_propigate_unit_synapses([2,3,2])
        pass
    
"""

888888b.         d8888  .d8888b.  888    d8P       8888888b.  8888888b.   .d88888b.  8888888b. 8888888 .d8888b.         d8888 88888888888 8888888888 
888  "88b       d88888 d88P  Y88b 888   d8P        888   Y88b 888   Y88b d88P" "Y88b 888   Y88b  888  d88P  Y88b       d88888     888     888        
888  .88P      d88P888 888    888 888  d8P         888    888 888    888 888     888 888    888  888  888    888      d88P888     888     888        
8888888K.     d88P 888 888        888d88K          888   d88P 888   d88P 888     888 888   d88P  888  888            d88P 888     888     8888888    
888  "Y88b   d88P  888 888        8888888b         8888888P"  8888888P"  888     888 8888888P"   888  888  88888    d88P  888     888     888        
888    888  d88P   888 888    888 888  Y88b        888        888 T88b   888     888 888         888  888    888   d88P   888     888     888        
888   d88P d8888888888 Y88b  d88P 888   Y88b       888        888  T88b  Y88b. .d88P 888         888  Y88b  d88P  d8888888888     888     888        
8888888P" d88P     888  "Y8888P"  888    Y88b      888        888   T88b  "Y88888P"  888       8888888 "Y8888P88 d88P     888     888     8888888888 
                                                                                                                                                                                                                                                                        
"""

    # Test the propigation function
    def _test_back_propigate(self):
        pass

    def test_back_propigate(self):
        pass

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

    # Test the learning function
    def _test_learn(self):
        pass

    def test_learn(self):
        pass


if __name__ == "__main__":
    unittest.main()
