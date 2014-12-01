
"""
Authors: Andres Emilsson & Nicholas Moores

git repository: https://github.com/npmoores/IllusorySquareNet
command for new collaborator: git remote add origin https://github.com/npmoores/IllusorySquareNet

This file in particular is intended to gather the data necessary for the experiment
"""

from PIL import Image, ImageFilter, ImageDraw
import random
import math
import sys
import os
import visual_functions
import network_functions
import plot_functions
from images2gif import writeGif
import matplotlib.pyplot as plt

picture_directory =  "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/visualization/"
gifs_directory =  "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/gifs/"
plots_directory = "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/plots/"

# Network parameters
n = 30
l = 10
prob = 0.0
sou = [[11,11]]

# Update parameters
lmda = .1
sw = 10.
k = 2.
alpha = .01
beta = .09
t = 1.7

# Visualization parameters
visual_scaling = 5
expo = .3
epochs_total = 50
every_how_many_epochs = 1



# Plotting parameters "voltemeters"
row_units_to_measure = [[20, 11]] # [[20, 10], [20, 11], [20, 12]] # , [11, 10], [11, 11]]
measurements_lists_rows = {}
for unit in range(len(row_units_to_measure)):
	measurements_lists_rows[unit] = []

square_units_to_measure =  [[11, 11]]
measurements_lists_square = {}
for unit in range(len(square_units_to_measure)):
	measurements_lists_square[unit] = []




# Fine detail network modifications
#black_input_suqares = []
black_input_suqares = [[20, 11], [20, 12], [20, 13], [20, 14], [20, 15], [20, 16], [20, 17], [20, 18], [20, 19], [20, 20]]
#black_input_suqares = [[20, 14], [20, 15], [20, 16], [20, 17]]
# black_input_suqares += [[11, 14], [11, 15], [11, 16], [11, 17]]
# black_input_suqares += [[14, 11], [15, 11], [16, 11], [17, 11]]
# black_input_suqares += [[14, 20], [15, 20], [16, 20], [17, 20]]

parameter_description = "n" + str(n) + "_l" + str(l) + "_prob" + str(prob) + "_sq" 
for i in range(len(sou)):
	parameter_description += str(sou[i][0]) + "-" + str(sou[i][1]) + "a"
parameter_description += "_lmda" + str(lmda)[1:] + "_sw" + str(sw) + "_alpha" + str(alpha) + "_beta" + str(beta)
parameter_description +=  "_scaling" + str(visual_scaling)  + "_expo" + str(expo) + "_t" + str(t)
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

# Fine detail changes
for i, j in black_input_suqares:
	network['I'][i][j] = 0.

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


for unit in range(len(row_units_to_measure)):
	i, j = row_units_to_measure[unit]
	measurements_lists_rows[unit] += [network['R'][i][j]]

for unit in range(len(square_units_to_measure)):
	i, j = square_units_to_measure[unit]
	measurements_lists_square[unit] += [network['S'][i][j]]



for epoch in range(epochs_total):
	newC = network_functions.computeColumnDeltas(network, l, n, sw)
	newR = network_functions.computeRowDeltas(network, l, n, sw)
	newS = network_functions.computeSquareDeltas(network, l, n)

	net_inputs['C'] = network_functions.updateNetInputs(net_inputs['C'], newC, lmda) # Change the net_inputs['C'] value in order to add an oscillation
	net_inputs['R'] = network_functions.updateNetInputs(net_inputs['R'], newR, lmda)
	net_inputs['S'] = network_functions.updateNetInputs(net_inputs['S'], newS, lmda)
	
	#network_functions.activateNetwork(network, net_inputs, alpha, beta)
	network_functions.activateNetworkWithTemperature(network, net_inputs, alpha, beta, t)

	for unit in range(len(row_units_to_measure)):
		i, j = row_units_to_measure[unit]
		measurements_lists_rows[unit] += [network['R'][i][j]]
	
	for unit in range(len(square_units_to_measure)):
		i, j = square_units_to_measure[unit]
		measurements_lists_square[unit] += [network['S'][i][j] / 500.]

	if epoch % every_how_many_epochs == 0:
		base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
		scaled_base = visual_functions.rescaleNetwork(base, visual_scaling, picture_directory, "", False) # "n30l6prob015lmda01sw10k2alpha01beta01sou2010_epoch" + str(epoch) + ".bmp"
		image_sequence += [scaled_base]



writeGif(gifs_directory + "one_side_missing_" + parameter_description + ".gif", image_sequence, duration=0.2)


x = range(epochs_total + 1)
plt.title('Activation of Row and Square units over time')
plt.ylabel('Unit activation')
plt.xlabel('Epoch')
#plt.axis([0, epochs_total + 1, 0, 1.2])
plot_list_ls = []

count = 0
for i in range(len(row_units_to_measure)):
	plot_list_ls += plt.plot(x, measurements_lists_rows[i], plot_functions.getDotType(i), label = "line " + str(row_units_to_measure[i]))
	count += 1

for i in range(len(square_units_to_measure)):
	plot_list_ls += plt.plot(x, measurements_lists_square[i], plot_functions.getDotType(i + count), label = "square " + str(square_units_to_measure[i]))

plt.legend(loc="lower right") #, bbox_to_anchor=(1,.5), shadow=True)
plt.savefig(plots_directory + "one_side_missing_" + parameter_description + ".png") # one_side_illusion_, complete_square_, all_sides_illusion_, one_side_missing_
plt.show()

