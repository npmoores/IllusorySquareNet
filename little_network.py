
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

# Network parameters
n = 30
l = 6
prob = 0.15
sou = [2, 10]

# Update parameters
lmda = .1
sw = 10.
k = 2.
alpha = .2
beta = 0.01

# Visualization parameters
visual_scaling = 5
expo = .25

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


# Set starting values.
# Add a square, or two, of activation in the input layer
network_functions.clampSquareInInput(network, sou, l, n)
network_functions.clampSquareInInput(network, [11, 11], l, n)

# Add noise to the input layer by flipping squares at random
network_functions.randomlyFlipInputUnits(network, prob, n)

# Visualize starting settup 
base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
scaled_base = visual_functions.rescaleNetwork(base, 5, picture_directory, "", True)


# Compute first net inputs
cD = network_functions.computeColumnDeltas(network, l, n, sw)
rD = network_functions.computeRowDeltas(network, l, n, sw)
sD = network_functions.computeSquareDeltas(network, l, n)

net_inputs = {'C':cD, 'R':rD, 'S':sD}

for epoch in range(100):
	newC = network_functions.computeColumnDeltas(network, l, n, sw)
	newR = network_functions.computeRowDeltas(network, l, n, sw)
	newS = network_functions.computeSquareDeltas(network, l, n)

	net_inputs['C'] = network_functions.updateNetInputs(net_inputs['C'], newC, lmda)
	net_inputs['R'] = network_functions.updateNetInputs(net_inputs['R'], newR, lmda)
	net_inputs['S'] = network_functions.updateNetInputs(net_inputs['S'], newS, lmda)
	
	network_functions.activateNetwork(network, net_inputs, alpha, beta)
	
	if epoch % 20 == 0:
		base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
		scaled_base = visual_functions.rescaleNetwork(base, visual_scaling, picture_directory, "", True) # "n30l6prob015lmda01sw10k2alpha01beta01sou2010_epoch" + str(epoch) + ".bmp"


