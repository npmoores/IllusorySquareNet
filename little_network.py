
"""
https://github.com/npmoores/IllusorySquareNet
git remote add origin https://github.com/npmoores/IllusorySquareNet

Authors: Andres Emilsson & Nicholas Moores
"""

from PIL import Image, ImageFilter, ImageDraw
import random
import math
import sys
import os

picture_directory =  os.getcwd()


# parameters
n = 10
l = 5
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

visualizeNetwork(network)


# Here BE code that Manages connections between the neurons 
# TODO: Decide on weight format. Probably use sparse coding of some sort. 

# Here Set starting values. For example, biases for the input units, or, alternatively, clamp the values of certainl input units
# Square clamped in input units

# Here run the update algorithm. Probably the Constraint Satisfaction Problem 

clampSquareInInput(network, square_origin_unit)

updateAllColumnUnits(network, l)
updateAllRowUnits(network, l)
updateAllSquareUnits(network, l)

# Visualize the network, and save images in intermediate iterations. Probably interleave this with the previous section
visualizeNetwork(network)




################### Functions ####################

# This makes a square starting in square_origin_unit, an [a, b] list, in the input layer become fully active
def clampSquareInInput(network, square_origin_unit):
	for i in range(square_origin_unit[0], l +  square_origin_unit[0]):
		network['I'][i][square_origin_unit[1]] = 1.
		network['I'][i][square_origin_unit[1] + l -1] = 1.
	for j in range(square_origin_unit[1], l +  square_origin_unit[1]):
		network['I'][square_origin_unit[0]][j] = 1.
		network['I'][square_origin_unit[0] + l - 1][j] = 1.
	return


# cUnit is an [i, j] coordinate within the C layer.
# i < n - l + 1 and j < n
def updateColumnUnit(cUnit, network, l):
	sum_of_activation = 0
	for i in range(l):
		sum_of_activation += network['I'][cUnit[0] + i][cUnit[1]]
	network['C'][cUnit[0]][cUnit[1]] = sum_of_activation / float(l)
	return

def updateAllColumnUnits(network, l):
	for i in range(n - l + 1):
		for j in range(n):
			updateColumnUnit([i, j], network, l)
	return

def updateRowUnit(rUnit, network, l):
	sum_of_activation = 0
	for i in range(l):
		sum_of_activation += network['I'][rUnit[0]][rUnit[1] + i]
	network['R'][rUnit[0]][rUnit[1]] = sum_of_activation / float(l)
	return

def updateAllRowUnits(network, l):
	for i in range(n):
		for j in range(n - l + 1):
			updateRowUnit([i, j], network, l)
	return

def updateSquareUnit(sUnit, network, l):
	network['S'][sUnit[0]][sUnit[1]] = (
		network['R'][sUnit[0]][sUnit[1]] + 
		network['R'][sUnit[0] + l][sUnit[1]] +
		network['C'][sUnit[0]][sUnit[1]] +
		network['C'][sUnit[0]][sUnit[1] + l]
		) / 4.
	return

def updateAllSquareUnits(network, l):
	for i in range(n - l + 1):
		for j in range(n - l + 1):
			updateSquareUnit([i, j], network, l)
	return


#################### Visualization ####################


# As a function:
def visualizeNetwork(network):
	AUTOS = [[0 for i in range(2*n - l + 2)] for j in range(2*n - l + 2)]
	# Input layer
	for i in range(n):
		for j in range(n):
			AUTOS[i][j] = network['I'][i][j]
	# Column layer
	for i in range(n - l + 1):
		for j in range(n):
			AUTOS[n + 1 + i][j] = network['C'][i][j]
	# Row layer
	for i in range(n):
		for j in range(n - l + 1):
			AUTOS[i][n + 1 + j] = network['R'][i][j]
	# Square layer
	for i in range(n - l + 1):
		for j in range(n - l + 1):
			AUTOS[i + n + 1][j + n + 1] = network['S'][i][j]
	width = 2*n -l + 1
	height = 2*n -l + 1
	base = Image.new('RGB', (width, height))
	pixel_base = base.load()
	for i in range(base.size[0]):
		for j in range(base.size[1]):
			r = int(AUTOS[i][j] * 255)
			g = int(AUTOS[i][j] * 255)
			b = int(AUTOS[i][j] * 255)
			pixel_base[i,j] = (r, g, b)
	for i in range(base.size[0]):
		pixel_base[i,n] = (0, 0, 255)
	for j in range(base.size[1]):
		pixel_base[n,j] = (0, 0, 255)
	base.show()
	return



# *********** As procedure. ***********
# All units to one square: AUTOS
AUTOS = [[0 for i in range(2*n - l + 2)] for j in range(2*n - l + 2)]
# Input layer
for i in range(n):
	for j in range(n):
		AUTOS[i][j] = network['I'][i][j]

# Column layer
for i in range(n - l + 1):
	for j in range(n):
		AUTOS[n + 1 + i][j] = network['C'][i][j]

# Row layer
for i in range(n):
	for j in range(n - l + 1):
		AUTOS[i][n + 1 + j] = network['R'][i][j]

# Square layer
for i in range(n - l + 1):
	for j in range(n - l + 1):
		AUTOS[i + n + 1][j + n + 1] = network['S'][i][j]

# Little Image
width = 2*n -l + 1
height = 2*n -l + 1
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int(AUTOS[i][j] * 255)
		g = int(AUTOS[i][j] * 255)
		b = int(AUTOS[i][j] * 255)
		pixel_base[i,j] = (r, g, b)

for i in range(base.size[0]):
	pixel_base[i,n] = (0, 0, 255)

for j in range(base.size[1]):
	pixel_base[n,j] = (0, 0, 255)

base.show()
base.save(picture_directory + "network_test.bmp")


base.save(sys.path[0] + "/network_test1.bmp")






# Rescale Image for visual convinience (Not necessary, since you can zoom in the original display when you open it in preview or some image visualizer)
scaling = 5

pixel_base_original = base.load()
x_dimension = base.size[0]
y_dimension = base.size[1]
new_x_dimension = x_dimension * scaling
new_y_dimension = y_dimension * scaling
scaled_base = Image.new('RGB', (new_x_dimension, new_y_dimension))
pixel_scaled_base = scaled_base.load()
for i in range(new_x_dimension):
	for j in range(new_y_dimension):
		current_x = i / scaling
		current_y = j / scaling
		pixel_scaled_base[i, j] = pixel_base_original[current_x, current_y]

scaled_base.show()

