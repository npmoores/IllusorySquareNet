
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
from images2gif import writeGif

picture_directory =  "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/visualization/"
gifs_directory =  "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/gifs/"



# Network parameters
n = 30
l = 6
prob = 0.2
sou = [[2, 10], [11, 11]]

# Update parameters
lmda = .05
sw = 10
k = 2.
alpha = .2
beta = 0.05

# Visualization parameters
visual_scaling = 5
expo = .25


parameter_description = "n" + str(n) + "_l" + str(l) + "_prob" + str(prob) + "_sq" 
for i in range(len(sou)):
	parameter_description += str(sou[i][0]) + "-" + str(sou[i][1]) + "a"
parameter_description += "_lmda" + str(lmda)[1:] + "_sw" + str(sw) + "_alpha" + str(alpha) + "_beta" + str(beta)
parameter_description +=  "_scaling" + str(visual_scaling)  + "_expo" + str(expo)
parameter_description = parameter_description.replace('.', '-')


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
for i in range(len(sou)):
	network_functions.clampSquareInInput(network, sou[i], l, n)

# Add noise to the input layer by flipping squares at random
network_functions.randomlyFlipInputUnits(network, prob, n)

# Visualize starting settup 
base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
scaled_base = visual_functions.rescaleNetwork(base, 5, picture_directory, "", False)

# Compute first net inputs
cD = network_functions.computeColumnDeltas(network, l, n, sw)
rD = network_functions.computeRowDeltas(network, l, n, sw)
sD = network_functions.computeSquareDeltas(network, l, n)

net_inputs = {'C':cD, 'R':rD, 'S':sD}

image_sequence = []
base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
scaled_base = visual_functions.rescaleNetwork(base, visual_scaling, picture_directory, "", False) # "n30l6prob015lmda01sw10k2alpha01beta01sou2010_epoch" + str(epoch) + ".bmp"
image_sequence += [scaled_base]
every_how_many_epochs = 1

for epoch in range(50):
	newC = network_functions.computeColumnDeltas(network, l, n, sw)
	newR = network_functions.computeRowDeltas(network, l, n, sw)
	newS = network_functions.computeSquareDeltas(network, l, n)

	net_inputs['C'] = network_functions.updateNetInputs(net_inputs['C'], newC, lmda)
	net_inputs['R'] = network_functions.updateNetInputs(net_inputs['R'], newR, lmda)
	net_inputs['S'] = network_functions.updateNetInputs(net_inputs['S'], newS, lmda)
	
	network_functions.activateNetwork(network, net_inputs, alpha, beta)
	
	if epoch % every_how_many_epochs == 0:
		base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
		scaled_base = visual_functions.rescaleNetwork(base, visual_scaling, picture_directory, "", False) # "n30l6prob015lmda01sw10k2alpha01beta01sou2010_epoch" + str(epoch) + ".bmp"
		image_sequence += [scaled_base]





writeGif(gifs_directory + parameter_description + ".gif", image_sequence, duration=0.2)
