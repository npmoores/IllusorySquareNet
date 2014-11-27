
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
lmda = .9
sw = 1.
k = 4.
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

for epoch in range(5):
	cD = network_functions.computeColumnDeltas(network, l, n, sw)
	rD = network_functions.computeRowDeltas(network, l, n, sw)
	sD = network_functions.computeSquareDeltas(network, l, n)

	acD = network_functions.averageLayer(cD, lmda, k)
	arD = network_functions.averageLayer(rD, lmda, k)
	asD = network_functions.averageLayer(sD, lmda, k)

	network_functions.updateColumnsWithDeltas(network, acD, l, n, lmda)
	network_functions.updateRowsWithDeltas(network, arD, l, n, lmda)
	network_functions.updateSquaresWithDeltas(network, asD, l, n, lmda)

	base = visual_functions.visualizeNetwork(network, n, l, picture_directory, "", False)
	scaled_base = visual_functions.rescaleNetwork(base, 5, picture_directory, "", True)


# Normalize C, R, update S, normalize S unpdare C, R

# Andrew Ng - underflow, overflow, e^x such that it can be represented in 64 bit
# All the net inputs before the activation.  "Synchonous upadting" -> How to do in RBM
# "RBP?"- Rachel... No it is IAC. - JM

# Temperature parameter determines net activation. Change it to allow peaks of activations
# You want to change activation gradually. .01 granularity 100 time steps per second. 


# Extrinsic oscillation source?

# Inhibitory inner neurons - delayed normalization: This could allow for a peak if activation and then subsiding. 
# Transmission delays (also a possible source of oscillation).

