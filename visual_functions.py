
from PIL import Image, ImageFilter, ImageDraw
import random
import math
import sys
import os



def visualizeNetwork(network, n, l, picture_directory, expo, name_to_save, show):
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
			r = int(max(0, AUTOS[i][j])**expo * 255)
			g = int(max(0, AUTOS[i][j])**expo * 255)
			b = int(max(0, AUTOS[i][j])**expo * 255)
			pixel_base[i,j] = (r, g, b)
	for i in range(base.size[0]):
		pixel_base[i,n] = (0, 0, 255)
	for j in range(base.size[1]):
		pixel_base[n,j] = (0, 0, 255)
	if show:
		base.show()
	if name_to_save != "":
		base.save(picture_directory + name_to_save +".bmp")
	return base


def rescaleNetwork(base_image, scaling, picture_directory, name_to_save, show):
	pixel_base_original = base_image.load()
	x_dimension = base_image.size[0]
	y_dimension = base_image.size[1]
	new_x_dimension = x_dimension * scaling
	new_y_dimension = y_dimension * scaling
	scaled_base = Image.new('RGB', (new_x_dimension, new_y_dimension))
	pixel_scaled_base = scaled_base.load()
	for i in range(new_x_dimension):
		for j in range(new_y_dimension):
			current_x = i / scaling
			current_y = j / scaling
			pixel_scaled_base[i, j] = pixel_base_original[current_x, current_y]
	if show:
		scaled_base.show()
	if name_to_save != "":
		scaled_base.save(picture_directory + name_to_save +".bmp")
	return scaled_base



