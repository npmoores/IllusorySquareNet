import matplotlib.pyplot as plt

possible_dot_types = ['p', '*', 'h', '1', '2', '3', '4', '8', 's',  '.', ',', 'o', 'v', '^', '<', '>']

def getDotType(number):
	number = number % 16
	return possible_dot_types[number]