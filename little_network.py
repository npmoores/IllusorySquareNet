
"""
https://github.com/npmoores/IllusorySquareNet
git remote add origin https://github.com/npmoores/IllusorySquareNet

"""

from PIL import Image, ImageFilter, ImageDraw
import random
import math

picture_directory = "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/visualization"


# parameters
n = 10
l = 5

# For each of the layers, the format is a list of lists. 
# Example: network[I][0][1] is the brightness value of the pixel in row 0, column 1, of the Input layer

#Initialize the network
network = {'I':[], 'C':[], 'R':[], 'S':[]}

for i in range(n):
	network['I'] += [[0 for j in range(n)]]

for i in range(n - l + 1):
	network['C'] += [[0.5 for j in range(n)]]

for i in range(n):
	network['R'] += [[0.5 for j in range(n - l + 1)]]

for i in range(n - l + 1):
	network['S'] += [[1. for j in range(n - l + 1)]]



# Here BE code that Manages connections between the neurons 
# TODO: Decide on weight format. Probably use sparse coding of some sort. 

# Here Set starting values. For example, biases for the input units, or, alternatively, clamp the values of certainl input units

# Here run the update algorithm. Probably the Constraint Satisfaction Problem 




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
		pixel_base[i,n] = (0, 0, b)
	for j in range(base.size[1]):
		pixel_base[n,j] = (0, 0, b)
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
	pixel_base[i,n] = (0, 0, b)

for j in range(base.size[1]):
	pixel_base[n,j] = (0, 0, b)

base.show()






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

