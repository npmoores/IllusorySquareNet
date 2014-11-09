
from PIL import Image, ImageFilter, ImageDraw
import random
import math

experimental_pattern_directory = "/Users/andesgomez/Documents/Experiments/vision_research/experiment_patterns/"


width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = (100*i / (j + 1)) % 256
		g = (100*i / (j + 1)) % 256
		b = (100*i / (j + 1)) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_3.bmp")



width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = (500*(i - 384) / (j + 1)) % 256
		g = (500* (i - 256) / (j + 1)) % 256
		b = (500*(i - 128) / (j + 1)) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_4.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = (500*(i - 384) / (abs(j - 256) + 1) ) % 256
		g = (500* (i - 256) / (abs(j - 256) + 1)) % 256
		b = (500*(i - 128) / (abs(j - 256) + 1)) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_5.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = (5*(i**2 - 384) / (abs(j - 256) + 1) ) % 256
		g = (5*(i**2 - 256) / (abs(j - 256) + 1)) % 256
		b = (5*(i**2 - 128) / (abs(j - 256) + 1)) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_6.bmp")



width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = (5*(i**2 - 1384) / (abs(j - 256) + 1) ) % 256
		g = (5*(i**2 - 5256) / (abs(j - 256) + 1)) % 256
		b = (5*(i**2 - 128) / (abs(j - 256) + 1)) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_7.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = ((i**3 - 128) / (15*abs(j - 256) + 1)) % 256
		g = ((i**3 - 65128) / (15*abs(j - 256) + 1)) % 256
		b = ((i**3 - 30128) / (15*abs(j - 256) + 1)) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_8.bmp")



width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int((i**2 + j**2)**.5) % 256
		g = int((i**2 + j**2)**.5) % 256
		b = int((i**2 + j**2)**.5) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_9.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int(((i - 128)**2 + (j - 128)**2)**.5) % 256
		g = int(((i - 256)**2 + (j - 256)**2)**.5) % 256
		b = int(((i - 384)**2 + (j - 384)**2)**.5) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_10.bmp")


width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int(((2*i - 2*128)**2 + (2*j - 2*128)**2)**.5) % 256
		g = int(((2*i - 2*256)**2 + (2*j - 2*256)**2)**.5) % 256
		b = int(((2*i - 2*384)**2 + (2*j - 2*384)**2)**.5) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_11.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int(((2*i - 2*128)**2 + (2*j - 2*128)**2)**.75) % 256
		g = int(((2*i - 2*256)**2 + (2*j - 2*256)**2)**.75) % 256
		b = int(((2*i - 2*384)**2 + (2*j - 2*384)**2)**.75) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_12.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int((abs(2*i - 2*128)**1.5 + abs(2*j - 2*128)**1.5)**.999) % 256
		g = int((abs(2*i - 2*256)**1.5 + abs(2*j - 2*256)**1.5)**.999) % 256
		b = int((abs(2*i - 2*384)**1.5 + abs(2*j - 2*384)**1.5)**.999) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_13.bmp")




width = 512
height = 512
base = Image.new('RGB', (width, height))
pixel_base = base.load()

for i in range(base.size[0]):
	for j in range(base.size[1]):
		r = int(((2*i - 2*128)**2 + (2*j - 2*128)**2 + 100*i + 100*j)**.75) % 256
		g = 0 # int(((2*i - 2*256)**2 + (2*j - 2*256)**2 + 50*i + 50*j)**.75) % 256
		b = 0 # int(((2*i - 2*384)**2 + (2*j - 2*384)**2 + 150*i + 150*j)**.75) % 256
		pixel_base[i,j] = (r, g, b)

base.show()
base.save(experimental_pattern_directory + "November_14.bmp")

