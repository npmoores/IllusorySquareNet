from PIL import Image, ImageFilter, ImageDraw
import random
import math
import sys
import os
import visual_functions



# Manipulate input
# This makes a square starting in square_origin_unit, an [a, b] list, in the input layer become fully active
def clampSquareInInput(network, square_origin_unit, l, n):
	for i in range(square_origin_unit[0], l +  square_origin_unit[0]):
		network['I'][i][square_origin_unit[1]] = 1.
		network['I'][i][square_origin_unit[1] + l -1] = 1.
	for j in range(square_origin_unit[1], l +  square_origin_unit[1]):
		network['I'][square_origin_unit[0]][j] = 1.
		network['I'][square_origin_unit[0] + l - 1][j] = 1.
	return


def randomlyFlipInputUnits(network, prob, n):
	for i in range(n):
		for j in range(n):
			if random.random() < prob:
				network['I'][i][j] = 1. - network['I'][i][j]
	return



# Propagate activity
# cUnit is an [i, j] coordinate within the C layer.
# i < n - l + 1 and j < n
def updateColumnUnit(cUnit, network, l, n):
	sum_of_activation = 0
	for i in range(l):
		sum_of_activation += network['I'][cUnit[0] + i][cUnit[1]]
	network['C'][cUnit[0]][cUnit[1]] = sum_of_activation / float(l)
	return

def updateAllColumnUnits(network, l, n):
	for i in range(n - l + 1):
		for j in range(n):
			updateColumnUnit([i, j], network, l, n)
	return

def updateRowUnit(rUnit, network, l, n):
	sum_of_activation = 0
	for i in range(l):
		sum_of_activation += network['I'][rUnit[0]][rUnit[1] + i]
	network['R'][rUnit[0]][rUnit[1]] = sum_of_activation / float(l)
	return

def updateAllRowUnits(network, l, n):
	for i in range(n):
		for j in range(n - l + 1):
			updateRowUnit([i, j], network, l, n)
	return

def updateSquareUnit(sUnit, network, l, n):
	network['S'][sUnit[0]][sUnit[1]] = (
		network['R'][sUnit[0]][sUnit[1]] + 
		network['R'][sUnit[0] + l - 1][sUnit[1]] +
		network['C'][sUnit[0]][sUnit[1]] +
		network['C'][sUnit[0]][sUnit[1] + l - 1]
		) / 4.
	return

def updateAllSquareUnits(network, l, n):
	for i in range(n - l + 1):
		for j in range(n - l + 1):
			updateSquareUnit([i, j], network, l, n)
	return






