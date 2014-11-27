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



# Instead of updating progressively and modifying the network one layer at a time, the following
# methods will compute (1) delta values for each unit, (2) simultaneous addition of all those deltas
# and finally (3) normalization within each layer

# Note: It seems more ntural to normalize before updating. I.e. normalize 

# Firts, compute the deltas. Return "subnetworks" that are not added to the network until all the 
# deltas are computed


# Column Deltas
def computeColumnDeltaUnit(cUnit, network, l, n, sw):
	sum_of_activation = 0
	for i in range(l):
		sum_of_activation += network['I'][cUnit[0] + i][cUnit[1]]
	if cUnit[1] < n -l + 1:
		sum_of_activation += sw * network['S'][cUnit[0]][cUnit[1]]
	if cUnit[1] -l + 1 >= 0:
		sum_of_activation += sw * network['S'][cUnit[0]][cUnit[1] - l + 1]
	Cdelta = sum_of_activation
	return Cdelta

def computeColumnDeltas(network, l, n, sw):
	Cdeltas = []
	for i in range(n - l + 1):
		Cdeltas += [[0.0 for j in range(n)]]
	for i in range(n - l + 1):
		for j in range(n):
			Cdeltas[i][j] = computeColumnDeltaUnit([i, j], network, l, n, sw)
	return Cdeltas
 
# Row Deltas
def computeRowDeltaUnit(rUnit, network, l, n, sw):
	sum_of_activation = 0
	for j in range(l):
		sum_of_activation += network['I'][rUnit[0]][rUnit[1] + j]
	if rUnit[0] < n -l + 1:
		sum_of_activation += sw * network['S'][rUnit[0]][rUnit[1]]
	if rUnit[0] - l + 1 >= 0:
		sum_of_activation += sw * network['S'][rUnit[0] - l + 1][rUnit[1]]
	Rdelta = sum_of_activation
	return Rdelta

def computeRowDeltas(network, l, n, sw):
	Rdeltas = []
	for i in range(n):
		Rdeltas += [[0.0 for j in range(n - l + 1)]]
	for i in range(n):
		for j in range(n - l + 1):
			Rdeltas[i][j] = computeRowDeltaUnit([i, j], network, l, n, sw)
	return Rdeltas

# Square Deltas
def computeSquareDeltaUnits(sUnit, network, l, n):
	Sdelta = (
		network['R'][sUnit[0]][sUnit[1]] + 
		network['R'][sUnit[0] + l - 1][sUnit[1]] +
		network['C'][sUnit[0]][sUnit[1]] +
		network['C'][sUnit[0]][sUnit[1] + l - 1]
		)
	return Sdelta

def computeSquareDeltas(network, l, n):
	Sdeltas = []
	for i in range(n - l + 1):
		Sdeltas += [[0. for j in range(n - l + 1)]]
	for i in range(n - l + 1):
		for j in range(n - l + 1):
			Sdeltas[i][j] = computeSquareDeltaUnits([i, j], network, l, n)
	return Sdeltas


# Normalize a given layer of the deltas
def averageLayer(someDeltas, lmda, konstant):
	newDeltas = someDeltas
	total_number_of_units = len(someDeltas)*len(someDeltas[0])
	starting_total_activation = 0.
	for i in range(len(someDeltas)):
		starting_total_activation += sum(someDeltas[i])
	for i in range(len(someDeltas)):
		for j in range(len(someDeltas[i])):
			newDeltas[i][j] = lmda*total_number_of_units * someDeltas[i][j] / float(starting_total_activation)
	return newDeltas



# Normalize in a different way




# Update

def updateColumnsWithDeltas(network, Cdeltas, l, n, lmda):
	for i in range(n - l + 1):
		for j in range(n):
			network['C'][i][j] = (1 - lmda) * network['C'][i][j] + lmda * Cdeltas[i][j]
	return

def updateRowsWithDeltas(network, Rdeltas, l, n, lmda):
	for i in range(n):
		for j in range(n - l + 1):
			network['R'][i][j] = (1 - lmda) * network['R'][i][j] + lmda * Rdeltas[i][j]
	return

def updateSquaresWithDeltas(network, Sdeltas, l, n, lmda):
	for i in range(n - l + 1):
		for j in range(n - l + 1):
			network['S'][i][j] = (1 - lmda) * network['S'][i][j] + lmda * Sdeltas[i][j]
	return


