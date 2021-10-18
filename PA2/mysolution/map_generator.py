# Author: Xuedan ZOU
# Date: 10/1/2021


# this is used to generate random map with the size to 50*50

import random

# change here to set the wall number and the map size
NOWALL_RATE = 3
SIZE = 7

# change here to change the file to write in
f = open("maze_sensor7.maz", "w")

for i in range(0, SIZE):
    for j in range(0, SIZE):
      obstacle = random.randint(0, NOWALL_RATE)
      if (obstacle == 0):
        f.write("#")
      else:
        f.write(".")
    if i < SIZE - 1:
      f.write("\n")
f.close()

