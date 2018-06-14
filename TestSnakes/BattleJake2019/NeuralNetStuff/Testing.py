from MLP import MLP
from NetworkController import NetworkController
import numpy as np

nc = NetworkController()
mlp1 = MLP([2,3,1])
for i in range(10000):
    mlp1.learn(np.array([1,0]), np.array([0]))
    mlp1.learn(np.array([0,1]), np.array([1]))
print("ONE")
print(mlp1.propigate(np.array([1,0])))
print(mlp1.propigate(np.array([0,1])))
name = nc.save(mlp1)
mlp2 = nc.load(name)
print("TWO")
print(mlp2.propigate(np.array([1,0])))
print(mlp1.propigate(np.array([0,1])))


