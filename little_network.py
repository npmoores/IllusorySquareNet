
"""
Authors: Andres Emilsson & Nicholas Moores

git repository: https://github.com/npmoores/IllusorySquareNet
command for new collaborator: git remote add origin https://github.com/npmoores/IllusorySquareNet
"""

from PIL import Image, ImageFilter, ImageDraw
import random
import math
import sys
import os
import visual_functions
import network_functions

picture_directory =  "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/visualization/"

# parameters
n = 10
l = 5
prob = 0.1
square_origin_unit = [2, 1]

# For each of the layers, the format is a list of lists. 
# Example: network[I][0][1] is the brightness value of the pixel in row 0, column 1, of the Input layer

#Initialize the network
network = {'I':[], 'C':[], 'R':[], 'S':[]}

for i in range(n):
	network['I'] += [[0 for j in range(n)]]

for i in range(n - l + 1):
	network['C'] += [[0.0 for j in range(n)]]

for i in range(n):
	network['R'] += [[0.0 for j in range(n - l + 1)]]

for i in range(n - l + 1):
	network['S'] += [[0. for j in range(n - l + 1)]]


#base = visual_functions.visualizeNetwork(network, n, l, picture_directory, "", True)
#visual_functions.visualizeNetwork(network, n, l, picture_directory, "test_function_2", False)
#scaled_base = visual_functions.rescaleNetwork(base, 5, picture_directory, "", True)


# Here BE code that Manages connections between the neurons 
# TODO: Decide on weight format. Probably use sparse coding of some sort. 

# Here Set starting values. For example, biases for the input units, or, alternatively, clamp the values of certainl input units
# Square clamped in input units

# Here run the update algorithm. Probably the Constraint Satisfaction Problem 

network_functions.clampSquareInInput(network, square_origin_unit, l, n)
network_functions.randomlyFlipInputUnits(network, prob, n)

network_functions.updateAllColumnUnits(network, l, n)
network_functions.updateAllRowUnits(network, l, n)
network_functions.updateAllSquareUnits(network, l, n)





# Visualize the network, and save images in intermediate iterations. Probably interleave this with the previous section
base = visual_functions.visualizeNetwork(network, n, l, picture_directory, "", False)
scaled_base = visual_functions.rescaleNetwork(base, 5, picture_directory, "", True)







# Backpropagation Algorithm

e = math.exp(1)






