# Author: Xuedan ZOU
# Date: 11/9/2021


# this is used to generate random map with the size to 50*50
# based on the generator in PA2 but have added the color part
# add the robot location by yourself after the generation

import random

# change here to set the wall number and the map size
# the higher the nowall_rate, the fewer walls would the map have
NOWALL_RATE = 10
SIZE = 4

# change the rate of different colors
# the list presents the probabilities of colors in the
# generated map, with the order of red, green, blue and
# yellow. The sum of these values should be 1.
rgby_distrucution = [0.25, 0.25, 0.25, 0.25]
color_list = ["r", "g", "b", "y"]

# change here to change the file to write in
f = open("maze2.maz", "w")

for i in range(0, SIZE):
    for j in range(0, SIZE):
      obstacle = random.randint(0, NOWALL_RATE)
      if (obstacle == 0):
        f.write("#")

      else:
        color_chance = random.random()
        sum = 0
        for k in range(0, 4):
            sum += rgby_distrucution[k]
            if color_chance <= sum :
                f.write(color_list[k])
                break

    if i < SIZE - 1:
      f.write("\n")

f.close()