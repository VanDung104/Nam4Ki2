import numpy as np
from matplotlib import pyplot as plt 

A = np.array([[1,3,5],[3,5,8]])
B = np.array([[2,4,8],[0,9,20]])
C = np.array([[0,3,1],[5,2,2]])
D = np.minimum.reduce([A,B,C]) 
print(D) 