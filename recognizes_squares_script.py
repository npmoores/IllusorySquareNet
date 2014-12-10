
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
recognition_plots = "/Users/andesgomez/Documents/Stanford/Autumn2014-Masters/Psych209/project/recognition_plots/"

probability_sequence = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65] #[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9] # 0.04, 0.06, 0.08, 0.1, 0.12]
num_tests = 100
list_of_corners = []
for i in range(num_tests):
	list_of_corners += [[random.randint(0,20), random.randint(0,20)]]

fraction_success_per_prob = []

for probability_in_seq in range(len(probability_sequence)):
	succ_for_prob = 0
	for square_run in range(num_tests):
		# Network architecture parameters
		n = 30
		l = 10 # Recognized square length
		sl = 10 # Input square length
		prob = probability_sequence[probability_in_seq]
		sou =  [list_of_corners[square_run]] # [[20, 1]] # [[11, 11]]

		# Input parameters [0, 3] inclusive. 0 complete square, 1 one side missing, 2 one side illusion, 3 Kanicza
		sq = 0

		# Normalization. dnorm 0 = layer normalization, 1 = one gaussian, 2 = DOG mexican hat
		dnorm = 0
		amp1 = 1
		sd1 = .7
		amp2 = .5
		sd2 = 2

		# Update parameters
		lmda = .1
		sw = 0.
		k = 2.
		alpha = 0.1 #.31
		beta = .002
		t = 1.0

		# Visualization parameters
		visual_scaling = 5
		expo = .3
		epochs_total = 50
		every_how_many_epochs = 1



		# Plotting parameters "voltemeters"
		row_units_to_measure = [[sou[0][0] + l - 1, sou[0][1]]] # [[20, 11]] # [[20, 10], [20, 11], [20, 12]] # , [11, 10], [11, 11]]
		measurements_lists_rows = {}
		for unit in range(len(row_units_to_measure)):
			measurements_lists_rows[unit] = []

		square_units_to_measure =  [[sou[0][0], sou[0][1]]] # [[11, 11]]
		measurements_lists_square = {}
		for unit in range(len(square_units_to_measure)):
			measurements_lists_square[unit] = []




		# Fine detail network modifications
		black_input_suqares = []
		parameter_description = "complete_square_"
		if sq == 1:
			x, y = sou[0]
			for i in range(sl):
				black_input_suqares += [[x + sl - 1, y + i]]
			#black_input_suqares += [[20, 11], [20, 12], [20, 13], [20, 14], [20, 15], [20, 16], [20, 17], [20, 18], [20, 19], [20, 20]]
			parameter_description = "one_side_missing_"
		if sq == 2:
			x, y = sou[0]
			for i in range(1 + sl / 3):
				black_input_suqares += [[x + sl - 1, y + sl/3 + i ]]
			#black_input_suqares += [[20, 14], [20, 15], [20, 16], [20, 17]]
			parameter_description = "one_side_illusion_"
		if sq == 3:
			x, y = sou[0]
			for i in range(1 + sl / 3):
				black_input_suqares += [[x, y + sl/3 + i]]
				black_input_suqares += [[x + sl - 1, y + sl/3 + i]]
				black_input_suqares += [[x + sl/3 + i, y]]
				black_input_suqares += [[x + sl/3 + i, y  + sl - 1]]
			#black_input_suqares += [[20, 14], [20, 15], [20, 16], [20, 17]]
			#black_input_suqares += [[11, 14], [11, 15], [11, 16], [11, 17]]
			#black_input_suqares += [[14, 11], [15, 11], [16, 11], [17, 11]]
			#black_input_suqares += [[14, 20], [15, 20], [16, 20], [17, 20]]
			parameter_description = "all_sides_illusion_"

		parameter_description += "n" + str(n) + "_l" + str(l) + "_sl" + str(sl) + "_prob" + str(prob) + "_sou" 
		for i in range(len(sou)):
			parameter_description += str(sou[i][0]) + "-" + str(sou[i][1]) + "a"
		parameter_description += "_lmda" + str(lmda)[1:] + "_sw" + str(sw) + "_alpha" + str(alpha) + "_beta" + str(beta)
		parameter_description +=  "_scaling" + str(visual_scaling)  + "_expo" + str(expo) + "_t" + str(t) + "_dnorm" + str(dnorm)
		parameter_description +=  "_amp1" + str(amp1) + "_sd1" + str(sd1) + "_amp2" + str(amp2) + "_sd2" + str(sd2)
		parameter_description = parameter_description.replace('.', '-')


		# For each of the layers, the format is a list of lists. 
		# Example: network[I][0][1] is the brightness value of the pixel in row 0, column 1, of the Input layer

		#Initialize the network



		network = network_functions.initializeANetwork(n, l)


		# Set starting values.
		# Add a square, or two, of activation in the input layer
		for i in range(len(sou)):
			network_functions.clampSquareInInput(network, sou[i], sl, n)

		# Add noise to the input layer by flipping squares at random
		network_functions.randomlyReplaceInputUnits(network, prob, n)

		# Fine detail changes
		for i, j in black_input_suqares:
			network['I'][i][j] = 0.

		# Visualize starting settup 
		# base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
		# scaled_base = visual_functions.rescaleNetwork(base, 5, picture_directory, "", False)

		# Compute first net inputs
		cD = network_functions.computeColumnDeltas(network, l, n, sw)
		rD = network_functions.computeRowDeltas(network, l, n, sw)
		sD = network_functions.computeSquareDeltas(network, l, n)

		net_inputs = {'C':cD, 'R':rD, 'S':sD}

		# image_sequence = []
		# base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
		# scaled_base = visual_functions.rescaleNetwork(base, visual_scaling, picture_directory, "", False) # "n30l6prob015lmda01sw10k2alpha01beta01sou2010_epoch" + str(epoch) + ".bmp"
		# image_sequence += [scaled_base]


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
			if dnorm == 0:
				network_functions.activateNetworkWithTemperature(network, net_inputs, alpha, beta, t)
			if dnorm == 1:
				network_functions.activateNetworkWithGaussianKernel(network, net_inputs, alpha, beta, t, amp1, sd1)
			if dnorm == 2:
				network_functions.activateNetworkWithMexicanHatKernel(network, net_inputs, alpha, beta, t, amp1, sd1, amp2, sd2)

			for unit in range(len(row_units_to_measure)):
				i, j = row_units_to_measure[unit]
				measurements_lists_rows[unit] += [network['R'][i][j]]
			
			for unit in range(len(square_units_to_measure)):
				i, j = square_units_to_measure[unit]
				measurements_lists_square[unit] += [network['S'][i][j] / 1.]

			# if epoch % every_how_many_epochs == 0:
			# 	base = visual_functions.visualizeNetwork(network, n, l, picture_directory, expo, "", False)
			# 	scaled_base = visual_functions.rescaleNetwork(base, visual_scaling, picture_directory, "", False) # "n30l6prob015lmda01sw10k2alpha01beta01sou2010_epoch" + str(epoch) + ".bmp"
			# 	image_sequence += [scaled_base]

		# writeGif(gifs_directory + parameter_description + ".gif", image_sequence, duration=0.2)

		units_higher = network_functions.squareRecognitionSucess(network, sou[0])
		if units_higher <= 1:
			succ_for_prob += 1


		# x = range(epochs_total + 1)
		# plt.title('Activation of Row and Square units over time')
		# plt.ylabel('Unit activation')
		# plt.xlabel('Epoch')
		# #plt.axis([0, epochs_total + 1, 0, 1.2])
		# plot_list_ls = []

		# count = 0
		# for i in range(len(row_units_to_measure)):
		# 	plot_list_ls += plt.plot(x, measurements_lists_rows[i], plot_functions.getDotType(i), label = "line " + str(row_units_to_measure[i]))
		# 	count += 1

		# for i in range(len(square_units_to_measure)):
		# 	plot_list_ls += plt.plot(x, measurements_lists_square[i], plot_functions.getDotType(i + count), label = "square " + str(square_units_to_measure[i]))

		# plt.legend(loc="lower right") #, bbox_to_anchor=(1,.5), shadow=True)
		# plt.savefig(plots_directory +  parameter_description + ".png") # one_side_illusion_, complete_square_, all_sides_illusion_, one_side_missing_
		# #plt.show()
		# plt.close()
	fraction_success_per_prob += [succ_for_prob]



plt.title("Fraction of Squares Recognized by Amount of Noise")
plt.xlabel('Amount of noise')
plt.ylabel('Number of Squares Recognized (out of ' + str(num_tests) + ')')
plt.axis([-0.02 + probability_sequence[0], probability_sequence[-1] + 0.02, 0, num_tests + 0.01])

plt.plot(probability_sequence, fraction_success_per_prob, plot_functions.getDotType(0), label = "Squares recognized")
plt.savefig(recognition_plots + 'layer_divisive_-4_to_-65_' + parameter_description + ".png")
plt.show()
#plt.close()